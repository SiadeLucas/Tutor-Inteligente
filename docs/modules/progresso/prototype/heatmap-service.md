---
title: Progresso - Agregador de Heatmap e Hub de Ação Top 3
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Agregador de Heatmap e Hub de Ação (Top 3 Críticos)

Implementação executável da consulta da matriz de capítulos do Heatmap e da detecção automática dos 3 gargalos de aprendizagem conforme a regra de negócio **RN-PRG-016**.

---

## Código Fonte (`backend/app/modules/progress/heatmap_service.py`)

```python
from uuid import UUID
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.content import VolumeDidatico, Capitulo
from app.models.progress import HeatmapDominio
from app.models.exercise import CaixaReforco
from app.modules.progress.schemas import (
    HeatmapVolumeResponse,
    HeatmapCapituloItem,
    HubAcaoTop3Response,
    TopCriticoItem
)


class HeatmapService:
    """Consolidador de dados visuais de maestria por volume e capítulo."""

    @staticmethod
    async def obter_heatmap_volume(
        db: AsyncSession,
        usuario_id: UUID,
        volume_id: UUID
    ) -> HeatmapVolumeResponse:
        """
        Retorna todos os capítulos do volume com suas respectivas cores
        e taxas ponderadas consolidadas para renderização do grid visual.
        """
        # 1. Busca dados do volume
        stmt_volume = select(VolumeDidatico).where(VolumeDidatico.id == volume_id)
        result_v = await db.execute(stmt_volume)
        volume = result_v.scalar_one_or_none()
        if not volume:
            raise ValueError("Volume didático não localizado.")

        # 2. Busca capítulos do volume ordenados
        stmt_capitulos = (
            select(Capitulo)
            .where(Capitulo.volume_id == volume_id)
            .order_by(Capitulo.ordem.asc())
        )
        result_c = await db.execute(stmt_capitulos)
        capitulos = result_c.scalars().all()

        # 3. Busca estados do heatmap para esse usuário
        capitulos_ids = [c.id for c in capitulos]
        stmt_hm = select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario_id,
                HeatmapDominio.capitulo_id.in_(capitulos_ids)
            )
        )
        result_hm = await db.execute(stmt_hm)
        mapa_nos = {hm.capitulo_id: hm for hm in result_hm.scalars().all()}

        # 4. Constrói a lista tipada de nós do heatmap
        itens_capitulos = []
        total_concluidos = 0

        for cap in capitulos:
            no = mapa_nos.get(cap.id)
            taxa = float(no.taxa_acertos_ponderada) if no else 0.0
            cor = no.status_cor if no else "cinza"
            total_questoes = no.total_questoes_respondidas if no else 0
            concluida = no.aula_concluida if no else False

            if concluida:
                total_concluidos += 1

            itens_capitulos.append(
                HeatmapCapituloItem(
                    capitulo_id=cap.id,
                    numero_capitulo=cap.numero_capitulo,
                    titulo=cap.titulo,
                    taxa_acertos_ponderada=taxa,
                    status_cor=cor,
                    total_exercicios_respondidos=total_questoes,
                    aula_concluida=concluida
                )
            )

        total_capitulos = len(capitulos)
        completude = round((total_concluidos / total_capitulos) * 100.0, 1) if total_capitulos > 0 else 0.0

        return HeatmapVolumeResponse(
            volume_id=volume.id,
            numero_volume=volume.numero_volume,
            titulo_volume=volume.titulo,
            grande_area=volume.grande_area,
            completude_volume_percentual=completude,
            capitulos=itens_capitulos
        )

    @staticmethod
    async def obter_top_3_criticos(
        db: AsyncSession,
        usuario_id: UUID
    ) -> HubAcaoTop3Response:
        """
        Localiza os 3 tópicos com pior rendimento (taxa < 75%)
        e cruza com a quantidade de erros pendentes na Caixa de Reforço.
        """
        # Query que busca os capítulos com menor taxa de acerto ponderada
        stmt = (
            select(HeatmapDominio, Capitulo, VolumeDidatico)
            .join(Capitulo, HeatmapDominio.capitulo_id == Capitulo.id)
            .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
            .where(
                and_(
                    HeatmapDominio.usuario_id == usuario_id,
                    HeatmapDominio.total_questoes_respondidas >= 3,
                    HeatmapDominio.taxa_acertos_ponderada < 75.0
                )
            )
            .order_by(HeatmapDominio.taxa_acertos_ponderada.asc())
            .limit(3)
        )
        result = await db.execute(stmt)
        linhas = result.all()

        top_itens = []
        for no_hm, cap, vol in linhas:
            # Conta erros pendentes na caixa de reforço para este capítulo
            stmt_cr = select(func.count(CaixaReforco.id)).where(
                and_(
                    CaixaReforco.usuario_id == usuario_id,
                    CaixaReforco.capitulo_id == cap.id,
                    CaixaReforco.status == "pendente"
                )
            )
            res_cr = await db.execute(stmt_cr)
            erros_pendentes = res_cr.scalar() or 0

            top_itens.append(
                TopCriticoItem(
                    capitulo_id=cap.id,
                    titulo_capitulo=cap.titulo,
                    numero_volume=vol.numero_volume,
                    titulo_volume=vol.titulo,
                    taxa_acerto_ponderada=float(no_hm.taxa_acertos_ponderada),
                    total_erros_na_caixa_reforco=erros_pendentes,
                    acao_revisar_teoria_url=f"/aula/{cap.id}?aba=teoria",
                    acao_praticar_reforco_url=f"/exercicios/reforco/{cap.id}"
                )
            )

        return HubAcaoTop3Response(
            top_criticos=top_itens,
            tem_pendencias_criticas=len(top_itens) > 0
        )
```
