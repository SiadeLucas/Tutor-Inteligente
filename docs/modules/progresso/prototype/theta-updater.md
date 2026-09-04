---
title: Progresso - Calibragem Contínua de Theta e Pontuação Ponderada
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Calibragem Contínua de Theta e Pontuação Ponderada

Implementação executável da regra de negócio **RN-PRG-006**: micro-ajustes imediatos no nível psicométrico do aluno ($\theta$) a cada exercício submetido na plataforma, sem necessidade de esperar uma nova prova formal.

---

## Código Fonte (`backend/app/modules/progress/theta_updater.py`)

```python
from typing import Optional, List, Tuple
import numpy as np
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.exercise import ItemExercicio, TentativaExercicio
from app.models.progress import HistoricoTheta, HeatmapDominio
from app.models.content import VolumeDidatico


class ThetaUpdaterService:
    """Motor de atualização contínua em circuito fechado."""

    D_CONSTANTE = 1.7

    @staticmethod
    def calcular_probabilidade_3pl(theta: float, a: float, b: float, c: float = 0.2) -> float:
        """Calcula P_i(theta) segundo a TRI."""
        expoente = -ThetaUpdaterService.D_CONSTANTE * a * (theta - b)
        expoente = np.clip(expoente, -30.0, 30.0)
        return c + (1.0 - c) * (1.0 / (1.0 + np.exp(expoente)))

    @staticmethod
    async def processar_micro_ajuste_exercicio(
        db: AsyncSession,
        usuario_id: UUID,
        disciplina_id: UUID,
        volume_id: UUID,
        capitulo_id: UUID,
        item: ItemExercicio,
        pontuacao_ponderada: float,  # 1.0 (1ª tent) | 0.5 (2ª tent com dica) | 0.0 (erro)
        total_questoes_respondidas_aluno: int,
        grande_area: Optional[str] = None
    ) -> float:
        """
        Aplica a fórmula do micro-ajuste estocástico:
        theta_novo = theta_antigo + (1 / sqrt(N + 10)) * a_i * (u_i - P_i(theta))
        """
        # 1. Recupera o último theta registrado para essa disciplina
        stmt_ultimo_theta = (
            select(HistoricoTheta.theta_estimado)
            .where(
                and_(
                    HistoricoTheta.usuario_id == usuario_id,
                    HistoricoTheta.disciplina_id == disciplina_id
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
        P_i = ThetaUpdaterService.calcular_probabilidade_3pl(
            theta=theta_anterior,
            a=float(item.parametro_a),
            b=float(item.parametro_b),
            c=float(item.parametro_c)
        )

        # 3. Fator de amortecimento com base no histórico de itens
        N = total_questoes_respondidas_aluno
        fator_aprendizado = 1.0 / np.sqrt(N + 10)

        # 4. Resíduo ponderado entre resultado real e esperado
        residuo = pontuacao_ponderada - P_i

        # 5. Cálculo do novo Theta (limitado estritamente entre -3.000 e +3.000)
        delta_theta = fator_aprendizado * float(item.parametro_a) * residuo
        novo_theta = float(np.clip(theta_anterior + delta_theta, -3.000, 3.000))
        novo_theta = round(novo_theta, 3)

        # 6. Determina a grande área dinâmica a partir do volume se omitida
        if not grande_area:
            stmt_vol = select(VolumeDidatico.grande_area).where(VolumeDidatico.id == volume_id)
            res_vol = await db.execute(stmt_vol)
            grande_area = res_vol.scalar_one_or_none() or "geral"

        # 7. Registra na série temporal da tabela historico_theta
        registro_theta = HistoricoTheta(
            id=uuid4(),
            usuario_id=usuario_id,
            disciplina_id=disciplina_id,
            volume_id=volume_id,
            grande_area=grande_area,
            theta_estimado=novo_theta,
            erro_padrao_se=0.25,
            origem_ajuste="micro_ajuste_exercicio",
            registrado_em=datetime.utcnow()
        )
        db.add(registro_theta)

        # 7. Atualiza o nó correspondente na tabela heatmap_dominio
        await ThetaUpdaterService._atualizar_no_heatmap(
            db=db,
            usuario_id=usuario_id,
            capitulo_id=capitulo_id
        )

        await db.commit()
        return novo_theta

    @staticmethod
    async def _atualizar_no_heatmap(db: AsyncSession, usuario_id: UUID, capitulo_id: UUID) -> None:
        """Recalcula a taxa de acertos ponderada e a cor do nó no Heatmap diretamente no PostgreSQL."""
        stmt_agg = (
            select(
                func.count(TentativaExercicio.id).label("total_itens"),
                func.coalesce(func.sum(TentativaExercicio.pontuacao_obtida), 0.0).label("pontos_somados")
            )
            .where(
                and_(
                    TentativaExercicio.usuario_id == usuario_id,
                    TentativaExercicio.capitulo_id == capitulo_id
                )
            )
        )
        res_agg = await db.execute(stmt_agg)
        total_itens, pontos_somados = res_agg.first()

        if not total_itens or total_itens == 0:
            return

        taxa_ponderada = round((float(pontos_somados) / total_itens) * 100.0, 2)

        # Aplica a regra das cores da RN-PRG-011
        if total_itens < 3:
            status_cor = "cinza"
        elif taxa_ponderada < 50.0:
            status_cor = "vermelho"
        elif taxa_ponderada < 75.0:
            status_cor = "amarelo"
        else:
            status_cor = "verde"

        # Atualiza ou cria o registro no heatmap_dominio
        stmt_heatmap = select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario_id,
                HeatmapDominio.capitulo_id == capitulo_id
            )
        )
        res_hm = await db.execute(stmt_heatmap)
        no_hm = res_hm.scalar_one_or_none()

        if no_hm:
            no_hm.taxa_acertos_ponderada = taxa_ponderada
            no_hm.status_cor = status_cor
            no_hm.total_questoes_respondidas = total_itens
            no_hm.ultima_interacao = datetime.utcnow()
        else:
            no_hm = HeatmapDominio(
                id=uuid4(),
                usuario_id=usuario_id,
                capitulo_id=capitulo_id,
                taxa_acertos_ponderada=taxa_ponderada,
                status_cor=status_cor,
                total_questoes_respondidas=total_itens
            )
            db.add(no_hm)
```
