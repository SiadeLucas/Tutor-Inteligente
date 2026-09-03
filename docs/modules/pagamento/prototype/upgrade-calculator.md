---
title: Pagamento - Calculador de Upgrade Proporcional
type: module
status: draft
related:
  - modules/pagamento/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Calculador de Abatimento Proporcional (Upgrade)

Implementação executável da regra de negócio **RN-PAG-005**: 100% de dedução do valor já investido em capítulos avulsos na aquisição do volume completo correspondente.

---

## Código Fonte (`backend/app/modules/payment/upgrade_service.py`)

```python
from uuid import UUID
from typing import Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.commercial import MatriculaPagamento
from app.models.content import VolumeDidatico, Capitulo
from app.modules.payment.schemas import UpgradeCalculationResponse


class UpgradeService:
    """Calcula valores proporcionais de upgrade com renovação de vigência."""

    @staticmethod
    async def calcular_upgrade_volume(
        db: AsyncSession,
        usuario_id: UUID,
        volume_id: UUID
    ) -> UpgradeCalculationResponse:
        """
        Calcula o valor líquido a pagar pelo Volume Completo:
        Valor Final = max(0, Preço do Volume - Soma dos Capítulos Pagos)
        """
        # 1. Busca os dados do volume didático
        stmt_volume = select(VolumeDidatico).where(VolumeDidatico.id == volume_id)
        result_volume = await db.execute(stmt_volume)
        volume = result_volume.scalar_one_or_none()

        if not volume:
            raise ValueError("Volume didático não encontrado.")

        # 2. Busca todos os capítulos vinculados a esse volume
        stmt_capitulos = select(Capitulo.id).where(Capitulo.volume_id == volume_id)
        result_capitulos = await db.execute(stmt_capitulos)
        capitulos_ids = [row[0] for row in result_capitulos.all()]

        # 3. Busca as matrículas ativas do usuário para esses capítulos específicos
        stmt_matriculas = select(MatriculaPagamento).where(
            and_(
                MatriculaPagamento.usuario_id == usuario_id,
                MatriculaPagamento.tipo_produto == "capitulo_50min",
                MatriculaPagamento.referencia_produto_id.in_(capitulos_ids),
                MatriculaPagamento.status == "active"
            )
        )
        result_matriculas = await db.execute(stmt_matriculas)
        matriculas_capitulos = result_matriculas.scalars().all()

        # 4. Soma o total já investido pelo aluno nesses capítulos avulsos
        total_ja_investido = sum(float(m.valor_pago) for m in matriculas_capitulos)
        capitulos_pagos_ids = [m.referencia_produto_id for m in matriculas_capitulos]

        # 5. Aplica a dedução de 100%
        preco_tabela = float(volume.preco_padrao)  # Ex: 49.90
        valor_final = max(0.00, round(preco_tabela - total_ja_investido, 2))
        desconto_obtido = round(preco_tabela - valor_final, 2)

        return UpgradeCalculationResponse(
            volume_id=volume.id,
            titulo_volume=volume.titulo,
            preco_tabela_volume=preco_tabela,
            total_ja_investido_capitulos=total_ja_investido,
            capitulos_adquiridos_count=len(capitulos_pagos_ids),
            capitulos_adquiridos_ids=capitulos_pagos_ids,
            valor_final_com_abatimento=valor_final,
            desconto_obtido=desconto_obtido
        )
```
