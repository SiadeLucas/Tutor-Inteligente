"""
Calculadora de Upgrade Proporcional (RN-PAG-005).
Abate 100% do valor investido em capítulos avulsos na compra do Volume Didático completo.
"""
from decimal import Decimal
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.content import VolumeDidatico, Capitulo
from app.models.payment import MatriculaPagamento


async def calcular_abatimento_volume(
    db: AsyncSession,
    usuario_id: UUID,
    volume_id: UUID,
) -> dict:
    """
    Soma o valor das matrículas ativas de capítulos do volume_id
    e desconta do preço padrão do volume.
    Retorna o valor original, abatimento, valor final e se é 100% gratuito.
    """
    # 1. Recupera o volume
    vol_res = await db.execute(select(VolumeDidatico).where(VolumeDidatico.id == volume_id))
    volume = vol_res.scalar_one_or_none()
    if not volume:
        return {
            "volume_id": volume_id,
            "preco_original": Decimal("0.00"),
            "total_abatimento": Decimal("0.00"),
            "valor_final": Decimal("0.00"),
            "capitulos_abatidos_count": 0,
            "gratis_por_upgrade": False,
            "volume_encontrado": False,
        }

    preco_volume = Decimal(str(volume.preco_padrao))

    # 2. Recupera os IDs dos capítulos do volume
    caps_res = await db.execute(
        select(Capitulo.id).where(Capitulo.volume_id == volume_id)
    )
    capitulo_ids = caps_res.scalars().all()

    if not capitulo_ids:
        return {
            "volume_id": volume_id,
            "preco_original": preco_volume,
            "total_abatimento": Decimal("0.00"),
            "valor_final": preco_volume,
            "capitulos_abatidos_count": 0,
            "gratis_por_upgrade": False,
            "volume_encontrado": True,
        }

    # 3. Busca matrículas ativas de capítulos desse volume adquiridas pelo usuário
    agora = datetime.now(timezone.utc)
    stmt = select(MatriculaPagamento).where(
        and_(
            MatriculaPagamento.usuario_id == usuario_id,
            MatriculaPagamento.tipo_produto == "capitulo_50min",
            MatriculaPagamento.referencia_produto_id.in_(capitulo_ids),
            MatriculaPagamento.status == "active",
            MatriculaPagamento.data_expiracao > agora,
        )
    )
    mat_res = await db.execute(stmt)
    matriculas_ativas = mat_res.scalars().all()

    total_abatimento = sum(Decimal(str(m.valor_pago)) for m in matriculas_ativas)
    abatimento_efetivo = min(preco_volume, total_abatimento)
    valor_final = max(Decimal("0.00"), preco_volume - total_abatimento)

    return {
        "volume_id": volume_id,
        "preco_original": preco_volume,
        "total_abatimento": abatimento_efetivo,
        "valor_final": valor_final,
        "capitulos_abatidos_count": len(matriculas_ativas),
        "gratis_por_upgrade": valor_final == Decimal("0.00"),
        "volume_encontrado": True,
    }
