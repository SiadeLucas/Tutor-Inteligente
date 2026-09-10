"""
Motor de atualização contínua em circuito fechado e micro-ajuste estocástico de Theta TRI (RN-PRG-006).
Em conformidade com docs-site/docs/modules/progresso/prototype/theta-updater.md.
"""
from typing import Optional
import numpy as np
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.exercise import ItemExercicio, TentativaExercicio
from app.models.progress import HistoricoTheta, HeatmapDominio
from app.models.content import VolumeDidatico, Capitulo


class ThetaUpdaterService:
    """Motor de calibragem contínua de proficiência psicométrica e domínio curricular."""

    D_CONSTANTE = 1.7

    @staticmethod
    def calcular_probabilidade_3pl(theta: float, a: float, b: float, c: float = 0.2) -> float:
        """
        Calcula a probabilidade esperada de acerto P_i(theta) segundo o modelo logístico 3PL da TRI:
        P_i(theta) = c + (1 - c) / (1 + exp(-D * a * (theta - b)))
        """
        expoente = -ThetaUpdaterService.D_CONSTANTE * a * (theta - b)
        expoente = float(np.clip(expoente, -30.0, 30.0))
        return float(c + (1.0 - c) * (1.0 / (1.0 + np.exp(expoente))))

    @staticmethod
    async def processar_micro_ajuste_exercicio(
        db: AsyncSession,
        usuario_id: UUID,
        disciplina_id: UUID,
        volume_id: Optional[UUID],
        capitulo_id: UUID,
        item: ItemExercicio,
        pontuacao_ponderada: float,  # 1.0 (1ª tent) | 0.5 (2ª tent com dica) | 0.0 (erro)
        total_questoes_respondidas_aluno: int,
        grande_area: Optional[str] = None,
    ) -> float:
        """
        Aplica a fórmula do micro-ajuste estocástico (RN-PRG-006):
        theta_novo = theta_antigo + (1 / sqrt(N + 10)) * a_i * (u_i - P_i(theta))
        """
        # 1. Recupera o último theta registrado para essa disciplina
        stmt_ultimo_theta = (
            select(HistoricoTheta.theta_estimado)
            .where(
                and_(
                    HistoricoTheta.usuario_id == usuario_id,
                    HistoricoTheta.disciplina_id == disciplina_id,
                )
            )
            .order_by(HistoricoTheta.registrado_em.desc())
            .limit(1)
        )
        result_theta = await db.execute(stmt_ultimo_theta)
        theta_anterior = result_theta.scalar_one_or_none()
        if theta_anterior is None:
            theta_anterior = 0.0  # Nível padrão de entrada

        theta_anterior = float(theta_anterior)

        # 2. Calcula a probabilidade esperada de acerto P_i(theta)
        a_param = float(item.parametro_a) if item.parametro_a else 1.0
        b_param = float(item.parametro_b) if item.parametro_b else 0.0
        c_param = float(item.parametro_c) if item.parametro_c else 0.2

        P_i = ThetaUpdaterService.calcular_probabilidade_3pl(
            theta=theta_anterior,
            a=a_param,
            b=b_param,
            c=c_param,
        )

        # 3. Fator de amortecimento com base no histórico de itens
        N = max(0, total_questoes_respondidas_aluno)
        fator_aprendizado = 1.0 / np.sqrt(N + 10)

        # 4. Resíduo ponderado entre resultado real e esperado
        residuo = pontuacao_ponderada - P_i

        # 5. Cálculo do novo Theta (limitado estritamente entre -3.000 e +3.000)
        delta_theta = fator_aprendizado * a_param * residuo
        novo_theta = float(np.clip(theta_anterior + delta_theta, -3.000, 3.000))
        novo_theta = round(novo_theta, 3)

        # 6. Determina a grande área dinâmica a partir do volume ou capítulo se omitida
        if not grande_area:
            if volume_id:
                stmt_vol = select(VolumeDidatico.grande_area).where(VolumeDidatico.id == volume_id)
                res_vol = await db.execute(stmt_vol)
                grande_area = res_vol.scalar_one_or_none()
            if not grande_area and capitulo_id:
                stmt_cap_vol = (
                    select(VolumeDidatico.grande_area)
                    .join(Capitulo, Capitulo.volume_id == VolumeDidatico.id)
                    .where(Capitulo.id == capitulo_id)
                )
                res_cap = await db.execute(stmt_cap_vol)
                grande_area = res_cap.scalar_one_or_none()
            if not grande_area:
                grande_area = "algebra_funcoes"

        # 7. Registra na série temporal da tabela historico_theta
        registro_theta = HistoricoTheta(
            id=uuid4(),
            usuario_id=usuario_id,
            disciplina_id=disciplina_id,
            volume_id=volume_id,
            grande_area=grande_area,
            theta_estimado=novo_theta,
            erro_padrao_se=0.250,
            origem_ajuste="micro_ajuste_exercicio",
            registrado_em=datetime.utcnow(),
        )
        db.add(registro_theta)

        # 8. Atualiza o nó correspondente na tabela heatmap_dominio
        await ThetaUpdaterService._atualizar_no_heatmap(
            db=db,
            usuario_id=usuario_id,
            capitulo_id=capitulo_id,
        )

        return novo_theta

    @staticmethod
    async def _atualizar_no_heatmap(db: AsyncSession, usuario_id: UUID, capitulo_id: UUID) -> None:
        """
        Recalcula a taxa de acertos ponderada e a cor do nó no Heatmap diretamente no PostgreSQL.
        Critérios canônicos (RN-PRG-012 / Tabela 15):
        - Cinza: menos de 3 itens respondidos
        - Vermelho: < 50% de taxa ponderada
        - Amarelo: 50% a 74.99%
        - Verde: >= 75%
        """
        stmt_agg = (
            select(
                func.count(TentativaExercicio.id).label("total_itens"),
                func.coalesce(func.sum(TentativaExercicio.pontuacao_obtida), 0.0).label("pontos_somados"),
            )
            .where(
                and_(
                    TentativaExercicio.usuario_id == usuario_id,
                    TentativaExercicio.capitulo_id == capitulo_id,
                )
            )
        )
        res_agg = await db.execute(stmt_agg)
        row = res_agg.first()
        total_itens = row[0] if row else 0
        pontos_somados = row[1] if row else 0.0

        if not total_itens or total_itens == 0:
            return

        taxa_ponderada = round((float(pontos_somados) / float(total_itens)) * 100.0, 2)

        # Aplica a regra das cores da RN-PRG-012
        if total_itens < 3:
            status_cor = "cinza"
        elif taxa_ponderada < 50.0:
            status_cor = "vermelho"
        elif taxa_ponderada < 75.0:
            status_cor = "amarelo"
        else:
            status_cor = "verde"

        # Conclusão da aula: se aproveitamento ponderado >= 60% e total_itens >= 3
        aula_concluida = (taxa_ponderada >= 60.0 and total_itens >= 3)

        # Atualiza ou cria o registro no heatmap_dominio
        stmt_heatmap = select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario_id,
                HeatmapDominio.capitulo_id == capitulo_id,
            )
        )
        res_hm = await db.execute(stmt_heatmap)
        no_hm = res_hm.scalar_one_or_none()

        if no_hm:
            no_hm.taxa_acertos_ponderada = taxa_ponderada
            no_hm.status_cor = status_cor
            no_hm.total_questoes_respondidas = total_itens
            no_hm.aula_concluida = no_hm.aula_concluida or aula_concluida
            no_hm.ultima_interacao = datetime.utcnow()
        else:
            no_hm = HeatmapDominio(
                id=uuid4(),
                usuario_id=usuario_id,
                capitulo_id=capitulo_id,
                taxa_acertos_ponderada=taxa_ponderada,
                status_cor=status_cor,
                total_questoes_respondidas=total_itens,
                aula_concluida=aula_concluida,
                ultima_interacao=datetime.utcnow(),
            )
            db.add(no_hm)
