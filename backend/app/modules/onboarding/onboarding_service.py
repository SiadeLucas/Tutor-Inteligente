"""
Serviço de Onboarding: cálculo de menoridade, rascunhos no Redis (TTL 48h)
e criação atômica da conta + sessão única no PostgreSQL.
Especificação canônica: docs-site/docs/modules/onboarding/prototype/onboarding-service.md
"""
import hashlib
import re
from datetime import date
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

import redis.asyncio as aioredis
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenService, hash_senha
from app.core.validators import CPFValidator
from app.models.user import Usuario
from app.modules.auth.session_manager import SessionManager
from app.modules.onboarding.schemas import CadastroConcluidoResponse, FinalizarCadastroRequest

# TTL do rascunho do wizard: 48 horas (RN: expiração automática)
DRAFT_TTL_SEGUNDOS = 172800


class ResultadoCadastro(BaseModel):
    """
    Resultado interno do cadastro. O refresh_token é injetado em cookie HTTP-Only
    pelo router e NUNCA retornado no corpo da resposta (padrão do módulo de autenticação).
    """
    usuario_id: UUID
    nome_completo: str
    access_token: str
    refresh_token: str
    sessao_id: UUID


class OnboardingService:
    """Orquestrador da finalização de cadastro do wizard de 3 etapas (sem CAT)."""

    # ------------------------------------------------------------------
    # Idade e menoridade (RN-ONB-004)
    # ------------------------------------------------------------------
    @staticmethod
    def calcular_idade(data_nascimento: date) -> int:
        """Idade exata em anos completos, considerando o aniversário do ano corrente."""
        hoje = date.today()
        return hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )

    # ------------------------------------------------------------------
    # Rascunho do wizard no Redis (TTL 48h)
    # ------------------------------------------------------------------
    @staticmethod
    async def salvar_rascunho(redis: aioredis.Redis, session_id: str, dados: Dict[str, Any]) -> None:
        await redis.set(
            f"onboarding_draft:{session_id}",
            json_dumps_compacto(dados),
            ex=DRAFT_TTL_SEGUNDOS,
        )

    @staticmethod
    async def obter_rascunho(redis: aioredis.Redis, session_id: str) -> Dict[str, Any]:
        dados = await redis.get(f"onboarding_draft:{session_id}")
        if not dados:
            return {}
        import json

        return json.loads(dados)

    @staticmethod
    async def deletar_rascunho(redis: aioredis.Redis, session_id: str) -> None:
        await redis.delete(f"onboarding_draft:{session_id}")

    # ------------------------------------------------------------------
    # Finalização atômica do cadastro
    # ------------------------------------------------------------------
    @staticmethod
    async def finalizar_cadastro(
        db: AsyncSession,
        redis: Optional[aioredis.Redis],
        payload: FinalizarCadastroRequest,
        ip_cliente: str,
        user_agent: str,
        draft_session_id: Optional[str] = None,
    ) -> ResultadoCadastro:
        """
        Revalida unicidade (CPF/e-mail), calcula menoridade, grava o usuário
        e abre a sessão única. Commit único ao final (atomicidade total).
        """
        # 1. Validação matemática estrita do CPF (Módulo 11)
        if not CPFValidator.validar(payload.etapa1.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O CPF informado é matematicamente inválido."
            )

        # 2. Data de nascimento deve ser estritamente no passado (RN-ONB-004)
        if payload.etapa1.data_nascimento >= date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de nascimento deve ser uma data no passado."
            )

        # 3. Menoridade exige responsável legal (RN-ONB-005)
        idade = OnboardingService.calcular_idade(payload.etapa1.data_nascimento)
        if idade < 6 or idade > 120:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de nascimento inválida. O estudante deve ter entre 6 e 120 anos."
            )
        eh_menor = idade < 18

        if eh_menor and not payload.etapa2.dados_responsavel:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estudantes menores de 18 anos exigem obrigatoriamente os dados do responsável legal."
            )

        # 4. Checagem de unicidade dentro da transação final (409 detalhado)
        stmt_existente = select(Usuario).where(
            or_(
                Usuario.email == payload.etapa2.email.lower(),
                Usuario.cpf == payload.etapa1.cpf
            )
        )
        res_existente = await db.execute(stmt_existente)
        usuario_duplicado = res_existente.scalar_one_or_none()

        if usuario_duplicado:
            if usuario_duplicado.cpf == payload.etapa1.cpf:
                detalhe = "Já existe uma conta cadastrada com este CPF."
            else:
                detalhe = "Já existe uma conta cadastrada com este endereço de e-mail."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detalhe)

        dados_resp = (
            payload.etapa2.dados_responsavel.model_dump() if payload.etapa2.dados_responsavel else None
        )

        # 5. Criação atômica do usuário com senha hasheada (Argon2id)
        novo_usuario = Usuario(
            id=uuid4(),
            cpf=payload.etapa1.cpf,
            email=payload.etapa2.email.lower(),
            senha_hash=hash_senha(payload.etapa2.senha),
            nome_completo=payload.etapa1.nome_completo,
            data_nascimento=payload.etapa1.data_nascimento,
            idade_anos=idade,
            eh_menor_idade=eh_menor,
            dados_responsavel=dados_resp,
            genero=payload.etapa1.genero,
            telefone=re.sub(r"\D", "", payload.etapa2.telefone),
            uf=payload.etapa3.uf.upper(),
            cidade=payload.etapa3.cidade,
            bairro=payload.etapa3.bairro,
            logradouro=payload.etapa3.logradouro,
            numero=payload.etapa3.numero,
            cep=payload.etapa3.cep,
            escola_tipo=payload.etapa3.escola_tipo,
            nome_escola=payload.etapa3.nome_escola,
            serie_ano=payload.etapa3.serie_ano,
            role="student",
            avatar_url=payload.etapa1.foto_perfil,
            ativo=True
        )
        db.add(novo_usuario)
        await db.flush()

        # 6. Sessão única ativa (revoga sessões anteriores; grava no PG + Redis)
        sessao = await SessionManager.registrar_nova_sessao(
            db=db,
            redis=redis,
            usuario_id=novo_usuario.id,
            ip_address=ip_cliente,
            user_agent=user_agent,
            refresh_token_hash="pendente"
        )

        # 7. Emissão dos tokens + persistência do hash SHA-256 do refresh token
        access_token = TokenService.criar_access_token(
            usuario_id=novo_usuario.id,
            role=novo_usuario.role,
            session_id=sessao.id
        )
        refresh_token = TokenService.criar_refresh_token(
            usuario_id=novo_usuario.id,
            session_id=sessao.id
        )
        sessao.refresh_token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

        await db.commit()
        await db.refresh(novo_usuario)

        # 8. Rascunho consumido com sucesso: remove do Redis
        if redis and draft_session_id:
            try:
                await OnboardingService.deletar_rascunho(redis, draft_session_id)
            except Exception:
                pass

        return ResultadoCadastro(
            usuario_id=novo_usuario.id,
            nome_completo=novo_usuario.nome_completo,
            access_token=access_token,
            refresh_token=refresh_token,
            sessao_id=sessao.id
        )


def json_dumps_compacto(dados: Dict[str, Any]) -> str:
    """Serialização determinística e compacta para o rascunho no Redis."""
    import json

    return json.dumps(dados, ensure_ascii=False, separators=(",", ":"))


# Exportação explícita para tipagem de rotas
__all__ = ["OnboardingService", "ResultadoCadastro", "CadastroConcluidoResponse", "DRAFT_TTL_SEGUNDOS"]
