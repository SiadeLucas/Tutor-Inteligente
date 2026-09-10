"""
Serviço agregador do Heatmap de Domínio e Hub de Ação nos Top 3 Tópicos Críticos.
Em conformidade com docs-site/docs/modules/progresso/prototype/heatmap-service.md.
"""
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.content import VolumeDidatico, Capitulo
from app.models.progress import HeatmapDominio
from app.models.exercise import CaixaReforco
from app.modules.progress.schemas import (
    HeatmapVolumeResponse,
    HeatmapCapituloItem,
    HubAcaoTop3Response,
    TopCriticoItem,
    VolumeResumoItem,
)


class HeatmapService:
    """Consolidador de dados visuais de maestria por volume e capítulo."""

    @staticmethod
    async def obter_heatmap_volume(
        db: AsyncSession,
        usuario_id: UUID,
        volume_id: UUID,
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
        mapa_nos = {}
        if capitulos_ids:
            stmt_hm = select(HeatmapDominio).where(
                and_(
                    HeatmapDominio.usuario_id == usuario_id,
                    HeatmapDominio.capitulo_id.in_(capitulos_ids),
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

            if concluida or (taxa >= 60.0 and total_questoes >= 3):
                total_concluidos += 1
                concluida = True

            itens_capitulos.append(
                HeatmapCapituloItem(
                    capitulo_id=cap.id,
                    numero_capitulo=cap.numero_capitulo,
                    titulo=cap.titulo,
                    taxa_acertos_ponderada=taxa,
                    status_cor=cor,
                    total_exercicios_respondidos=total_questoes,
                    aula_concluida=concluida,
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
            capitulos=itens_capitulos,
        )

    @staticmethod
    async def listar_resumo_volumes(
        db: AsyncSession,
        usuario_id: UUID,
        disciplina_id: Optional[UUID] = None,
    ) -> List[VolumeResumoItem]:
        """
        Retorna a lista de volumes (ex: 11 volumes Iezzi) com estatísticas
        de completude para navegação em abas no frontend.
        """
        stmt = select(VolumeDidatico)
        if disciplina_id:
            stmt = stmt.where(VolumeDidatico.disciplina_id == disciplina_id)
        stmt = stmt.order_by(VolumeDidatico.numero_volume.asc())
        volumes = (await db.execute(stmt)).scalars().all()
        volume_ids = [vol.id for vol in volumes]

        # Agregações em lote (evita N+1): total de capítulos e concluídos por volume
        # em 2 queries agrupadas, independentemente do número de volumes.
        total_por_volume: dict = {}
        concluidos_por_volume: dict = {}

        if volume_ids:
            stmt_totais = (
                select(Capitulo.volume_id, func.count(Capitulo.id))
                .where(Capitulo.volume_id.in_(volume_ids))
                .group_by(Capitulo.volume_id)
            )
            for vol_id, total in (await db.execute(stmt_totais)).all():
                total_por_volume[vol_id] = total

            stmt_concluidos = (
                select(
                    Capitulo.volume_id,
                    func.count(func.distinct(HeatmapDominio.capitulo_id)),
                )
                .join(HeatmapDominio, HeatmapDominio.capitulo_id == Capitulo.id)
                .where(
                    and_(
                        Capitulo.volume_id.in_(volume_ids),
                        HeatmapDominio.usuario_id == usuario_id,
                        HeatmapDominio.aula_concluida == True,  # noqa: E712
                    )
                )
                .group_by(Capitulo.volume_id)
            )
            for vol_id, concluidos in (await db.execute(stmt_concluidos)).all():
                concluidos_por_volume[vol_id] = concluidos

        resumos = []
        for vol in volumes:
            total_caps = total_por_volume.get(vol.id, 0)
            concluidos = concluidos_por_volume.get(vol.id, 0)

            comp_pct = round((concluidos / total_caps) * 100.0, 1) if total_caps > 0 else 0.0
            resumos.append(
                VolumeResumoItem(
                    volume_id=vol.id,
                    numero_volume=vol.numero_volume,
                    titulo_volume=vol.titulo,
                    grande_area=vol.grande_area,
                    completude_percentual=comp_pct,
                    total_capitulos=total_caps,
                    capitulos_concluidos=concluidos,
                )
            )

        return resumos

    @staticmethod
    async def obter_top_3_criticos(
        db: AsyncSession,
        usuario_id: UUID,
    ) -> HubAcaoTop3Response:
        """
        RN-PRG-016: Localiza os 3 tópicos com pior rendimento (taxa < 75%)
        e cruza com a quantidade de erros pendentes na Caixa de Reforço.
        """
        stmt = (
            select(HeatmapDominio, Capitulo, VolumeDidatico)
            .join(Capitulo, HeatmapDominio.capitulo_id == Capitulo.id)
            .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
            .where(
                and_(
                    HeatmapDominio.usuario_id == usuario_id,
                    HeatmapDominio.total_questoes_respondidas >= 1,
                    HeatmapDominio.taxa_acertos_ponderada < 75.0,
                )
            )
            .order_by(HeatmapDominio.taxa_acertos_ponderada.asc())
            .limit(3)
        )
        result = await db.execute(stmt)
        linhas = result.all()

        top_itens = []
        if linhas:
            # Contagem de pendências na Caixa de Reforço em UMA query agrupada
            # (evita N+1: 1 query por capítulo crítico)
            caps_ids = [cap.id for _, cap, _ in linhas]
            stmt_cr = (
                select(CaixaReforco.capitulo_id, func.count(CaixaReforco.id))
                .where(
                    and_(
                        CaixaReforco.usuario_id == usuario_id,
                        CaixaReforco.capitulo_id.in_(caps_ids),
                        CaixaReforco.status == "pendente",
                    )
                )
                .group_by(CaixaReforco.capitulo_id)
            )
            erros_por_capitulo = {
                cap_id: total
                for cap_id, total in (await db.execute(stmt_cr)).all()
            }

            for no_hm, cap, vol in linhas:
                top_itens.append(
                    TopCriticoItem(
                        capitulo_id=cap.id,
                        titulo_capitulo=cap.titulo,
                        numero_volume=vol.numero_volume,
                        titulo_volume=vol.titulo,
                        taxa_acerto_ponderada=float(no_hm.taxa_acertos_ponderada),
                        total_erros_na_caixa_reforco=erros_por_capitulo.get(cap.id, 0),
                        acao_revisar_teoria_url=f"/aula/{cap.id}?aba=teoria",
                        acao_praticar_reforco_url=f"/exercicios?capitulo_id={cap.id}&modo=reforco",
                    )
                )

        return HubAcaoTop3Response(
            top_criticos=top_itens,
            tem_pendencias_criticas=len(top_itens) > 0,
        )
