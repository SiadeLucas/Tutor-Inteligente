"""
Serviço de Controle de Acesso e Gating Comercial.
Verifica direitos de acesso baseados em perfil (Admin/Professor) e matrículas ativas.
"""
from uuid import UUID
from datetime import datetime, timezone
from typing import Set, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.user import Usuario
from app.models.content import Capitulo
from app.models.payment import MatriculaPagamento


async def verificar_acesso_capitulo(
    db: AsyncSession,
    usuario: Usuario,
    capitulo_id: UUID,
) -> bool:
    """
    Retorna True se o usuário possui acesso liberado ao capítulo.
    - Administradores e Professores possuem acesso total irrestrito (bypass).
    - Usuários com Passe Global ativo possuem acesso total irrestrito.
    - Usuários com o Volume correspondente ativo possuem acesso.
    - Usuários com o Capítulo avulso ativo possuem acesso.
    """
    if usuario.role in ("admin", "teacher"):
        return True

    agora = datetime.now(timezone.utc)

    # 1. Verifica Passe Global
    res_global = await db.execute(
        select(MatriculaPagamento.id).where(
            and_(
                MatriculaPagamento.usuario_id == usuario.id,
                MatriculaPagamento.tipo_produto == "passe_global",
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > agora,
            )
        )
    )
    if res_global.scalar_one_or_none():
        return True

    # 2. Verifica Capítulo Avulso
    res_cap = await db.execute(
        select(MatriculaPagamento.id).where(
            and_(
                MatriculaPagamento.usuario_id == usuario.id,
                MatriculaPagamento.tipo_produto == "capitulo_50min",
                MatriculaPagamento.referencia_produto_id == capitulo_id,
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > agora,
            )
        )
    )
    if res_cap.scalar_one_or_none():
        return True

    # 3. Descobre o volume_id do capítulo
    cap_res = await db.execute(select(Capitulo.volume_id).where(Capitulo.id == capitulo_id))
    volume_id = cap_res.scalar_one_or_none()
    if volume_id:
        res_vol = await db.execute(
            select(MatriculaPagamento.id).where(
                and_(
                    MatriculaPagamento.usuario_id == usuario.id,
                    MatriculaPagamento.tipo_produto == "volume_iezzi",
                    MatriculaPagamento.referencia_produto_id == volume_id,
                    MatriculaPagamento.status == "active",
                    MatriculaPagamento.data_expiracao > agora,
                )
            )
        )
        if res_vol.scalar_one_or_none():
            return True

    return False


async def obter_capitulos_desbloqueados(
    db: AsyncSession,
    usuario: Usuario,
    capitulo_ids: List[UUID],
) -> Set[UUID]:
    """
    Otimizado para consultas em lote (Skill Tree / catálogo).
    Retorna o conjunto de IDs de capítulos aos quais o usuário tem acesso comercial.
    """
    if not capitulo_ids:
        return set()

    if usuario.role in ("admin", "teacher"):
        return set(capitulo_ids)

    agora = datetime.now(timezone.utc)

    # Busca todas as matrículas ativas do usuário
    res_mat = await db.execute(
        select(MatriculaPagamento).where(
            and_(
                MatriculaPagamento.usuario_id == usuario.id,
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > agora,
            )
        )
    )
    matriculas = res_mat.scalars().all()

    # Se possui passe_global ativo, tudo está desbloqueado
    if any(m.tipo_produto == "passe_global" for m in matriculas):
        return set(capitulo_ids)

    desbloqueados: Set[UUID] = set()

    # Capítulos diretos
    for m in matriculas:
        if m.tipo_produto == "capitulo_50min" and m.referencia_produto_id:
            desbloqueados.add(m.referencia_produto_id)

    # Volumes adquiridos
    volumes_comprados = [
        m.referencia_produto_id for m in matriculas
        if m.tipo_produto == "volume_iezzi" and m.referencia_produto_id
    ]
    if volumes_comprados:
        caps_vol_res = await db.execute(
            select(Capitulo.id).where(
                and_(
                    Capitulo.id.in_(capitulo_ids),
                    Capitulo.volume_id.in_(volumes_comprados),
                )
            )
        )
        for cid in caps_vol_res.scalars().all():
            desbloqueados.add(cid)

    return desbloqueados
