"""
Gerenciador de sessões ativas, controle de concorrência única e rate limit com Redis.
"""
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_
import redis.asyncio as aioredis

from app.models.user import SessaoAtiva, Usuario


class SessionManager:
    """Gerenciador híbrido (PostgreSQL + Redis) para controle de sessão única e proteção anti-força-bruta."""

    @staticmethod
    def _rate_limit_key(identificador: str, ip: str) -> str:
        return f"rate_limit:login:{identificador}:{ip}"

    @classmethod
    async def obter_tentativas_login(cls, redis: Optional[aioredis.Redis], identificador: str, ip: str) -> int:
        """Obtém o número de tentativas falhas de login nos últimos 15 minutos."""
        if not redis:
            return 0
        try:
            chave = cls._rate_limit_key(identificador, ip)
            val = await redis.get(chave)
            return int(val) if val else 0
        except Exception:
            return 0

    @classmethod
    async def incrementar_tentativa_login(
        cls,
        redis: Optional[aioredis.Redis],
        identificador: str,
        ip: str,
        ttl_segundos: int = 900
    ) -> int:
        """Incrementa contador de tentativas falhas e estabelece janela de 15 minutos."""
        if not redis:
            return 1
        try:
            chave = cls._rate_limit_key(identificador, ip)
            total = await redis.incr(chave)
            if total == 1:
                await redis.expire(chave, ttl_segundos)
            return total
        except Exception:
            return 1

    @classmethod
    async def limpar_tentativas_login(cls, redis: Optional[aioredis.Redis], identificador: str, ip: str) -> None:
        """Reseta o contador de tentativas após autenticação bem-sucedida."""
        if not redis:
            return
        try:
            chave = cls._rate_limit_key(identificador, ip)
            await redis.delete(chave)
        except Exception:
            pass

    @classmethod
    async def registrar_nova_sessao(
        cls,
        db: AsyncSession,
        redis: Optional[aioredis.Redis],
        usuario_id: UUID,
        ip_address: str,
        user_agent: str,
        refresh_token_hash: str
    ) -> SessaoAtiva:
        """
        Cria uma nova sessão autorizada para o usuário e revoga atomicamente
        qualquer sessão anterior (Regra de 1 dispositivo concorrente).
        """
        # 1. Revoga todas as sessões anteriores no banco
        stmt_revogar = (
            update(SessaoAtiva)
            .where(
                and_(
                    SessaoAtiva.usuario_id == usuario_id,
                    SessaoAtiva.revogado == False
                )
            )
            .values(revogado=True)
        )
        await db.execute(stmt_revogar)

        # 2. Cria nova sessão ativa
        session_id = uuid4()
        session_token = str(uuid4())
        nova_sessao = SessaoAtiva(
            id=session_id,
            usuario_id=usuario_id,
            session_token=session_token,
            refresh_token_hash=refresh_token_hash,
            ip_address=ip_address,
            user_agent=user_agent,
            ultimo_heartbeat=datetime.utcnow(),
            revogado=False
        )
        db.add(nova_sessao)
        await db.commit()
        await db.refresh(nova_sessao)

        # 3. Atualiza camada volátil no Redis
        if redis:
            try:
                # Remove chaves legadas de heartbeat do usuário
                keys = await redis.keys(f"heartbeat:{usuario_id}:*")
                if keys:
                    await redis.delete(*keys)

                # Define a sessão ativa e o heartbeat com TTL de 45 segundos
                await redis.set(f"session:{usuario_id}:active", str(session_id), ex=7 * 86400)
                await redis.set(f"heartbeat:{usuario_id}:{session_id}", "1", ex=45)
            except Exception:
                pass

        return nova_sessao

    @classmethod
    async def validar_sessao_ativa(
        cls,
        db: AsyncSession,
        session_id: UUID,
        usuario_id: UUID
    ) -> SessaoAtiva:
        """
        Verifica se a sessão informada ainda é a autorizada para o usuário.
        Se revogada por login posterior em outro aparelho, dispara 401 com CONCURRENT_SESSION_REVOKED.
        """
        stmt = select(SessaoAtiva).where(
            and_(
                SessaoAtiva.id == session_id,
                SessaoAtiva.usuario_id == usuario_id
            )
        )
        result = await db.execute(stmt)
        sessao = result.scalar_one_or_none()

        if not sessao or sessao.revogado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CONCURRENT_SESSION_REVOKED"
            )

        return sessao

    @classmethod
    async def atualizar_heartbeat(
        cls,
        db: AsyncSession,
        redis: Optional[aioredis.Redis],
        session_id: UUID,
        usuario_id: UUID
    ) -> None:
        """
        Registra presença na camada volátil (Redis TTL 45s)
        e atualiza estampa de auditoria no PostgreSQL.
        """
        if redis:
            try:
                await redis.set(f"heartbeat:{usuario_id}:{session_id}", "1", ex=45)
                await redis.set(f"session:{usuario_id}:active", str(session_id), ex=7 * 86400)
            except Exception:
                pass

        stmt = (
            update(SessaoAtiva)
            .where(SessaoAtiva.id == session_id)
            .values(ultimo_heartbeat=datetime.utcnow())
        )
        await db.execute(stmt)
        await db.commit()

    @classmethod
    async def revogar_sessao(
        cls,
        db: AsyncSession,
        redis: Optional[aioredis.Redis],
        session_id: UUID,
        usuario_id: Optional[UUID] = None
    ) -> None:
        """Revoga uma sessão específica (Logout local)."""
        stmt = (
            update(SessaoAtiva)
            .where(SessaoAtiva.id == session_id)
            .values(revogado=True)
        )
        await db.execute(stmt)
        await db.commit()

        if redis and usuario_id:
            try:
                await redis.delete(f"heartbeat:{usuario_id}:{session_id}")
                active = await redis.get(f"session:{usuario_id}:active")
                if active == str(session_id):
                    await redis.delete(f"session:{usuario_id}:active")
            except Exception:
                pass

    @classmethod
    async def revogar_todas_sessoes_usuario(
        cls,
        db: AsyncSession,
        redis: Optional[aioredis.Redis],
        usuario_id: UUID
    ) -> int:
        """Revoga todas as sessões ativas do usuário em todos os dispositivos (Logout remoto)."""
        stmt = (
            update(SessaoAtiva)
            .where(
                and_(
                    SessaoAtiva.usuario_id == usuario_id,
                    SessaoAtiva.revogado == False
                )
            )
            .values(revogado=True)
        )
        result = await db.execute(stmt)
        await db.commit()

        if redis:
            try:
                keys = await redis.keys(f"heartbeat:{usuario_id}:*")
                if keys:
                    await redis.delete(*keys)
                await redis.delete(f"session:{usuario_id}:active")
            except Exception:
                pass

        return result.rowcount
