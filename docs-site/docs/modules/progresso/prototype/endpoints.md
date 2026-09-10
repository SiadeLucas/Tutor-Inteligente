---
title: Progresso - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-10"
updated_by: buffy
---

# 5. Endpoints da API FastAPI

Implementação das rotas assíncronas de métricas tridimensionais, heatmap, tópicos críticos e download do boletim escolar em PDF (`app/modules/progress/router.py`).

---

## Código Fonte (`backend/app/modules/progress/router.py`)

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.models.progress import HistoricoTheta, HeatmapDominio, HorasEstudoDiarias
from app.models.content import Capitulo, VolumeDidatico
from app.modules.progress.schemas import (
    ProgressoGeralResponse,
    HeatmapVolumeResponse,
    HubAcaoTop3Response,
    RadarAreaItem
)
from app.modules.progress.heatmap_service import HeatmapService
from app.modules.progress.pdf_generator import BoletimPDFGenerator

router = APIRouter(prefix="/api/v1/progresso", tags=["Progresso & Analytics"])


# ============================================================================
# 1. Visão Geral de Métricas Tridimensionais
# ============================================================================

@router.get("/geral", response_model=ProgressoGeralResponse)
async def obter_progresso_geral(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna os indicadores unificados do estudante:
    - Theta geral contínuo da TRI (-3.0 a +3.0)
    - Tempo líquido ativo acumulado
    - Streak de dias consecutivos
    - Dados multiaxiais para o Gráfico Radar comparativo
    """
    # 1. Busca o último theta registrado
    stmt_theta = (
        select(HistoricoTheta.theta_estimado, HistoricoTheta.erro_padrao_se)
        .where(HistoricoTheta.usuario_id == current_user.id)
        .order_by(HistoricoTheta.registrado_em.desc())
        .limit(1)
    )
    res_theta = await db.execute(stmt_theta)
    theta_row = res_theta.first()
    theta_atual = float(theta_row[0]) if theta_row else 0.00
    se_atual = float(theta_row[1]) if theta_row else 0.35

    # Classificação de maestria
    if theta_atual < -0.5:
        nivel = "Básico"
    elif theta_atual <= 1.0:
        nivel = "Intermediário"
    else:
        nivel = "Avançado"

    # 2. Soma de horas ativas líquidas
    stmt_horas = select(func.sum(HorasEstudoDiarias.segundos_ativos)).where(
        HorasEstudoDiarias.usuario_id == current_user.id
    )
    res_horas = await db.execute(stmt_horas)
    segundos_totais = res_horas.scalar() or 0
    horas_liquidas = round(segundos_totais / 3600.0, 1)

    # 3. Cálculo dinâmico da Completude Curricular Global
    stmt_total_capitulos = select(func.count(Capitulo.id))
    total_caps = (await db.execute(stmt_total_capitulos)).scalar() or 1
    
    stmt_concluidos = select(func.count(HeatmapDominio.id)).where(
        and_(
            HeatmapDominio.usuario_id == current_user.id,
            HeatmapDominio.taxa_acertos_ponderada >= 60.0
        )
    )
    caps_concluidos = (await db.execute(stmt_concluidos)).scalar() or 0
    completude_real = round((caps_concluidos / total_caps) * 100.0, 1)

    # 4. Dados para os 4 eixos do Gráfico Radar (consultando a última calibragem por área)
    # Slugs CANÔNICOS da taxonomia do projeto (data-architecture.md, Tabela 07, seed de
    # conteúdo e scores_grandes_areas gravado pelo CAT da Etapa 7). Os rótulos de exibição
    # podem ser mais descritivos, mas o slug persistido é sempre o canônico.
    areas_mapeadas = [
        ("algebra_funcoes", "Álgebra e Funções"),
        ("geometria", "Geometria e Trigonometria"),
        ("algebra_linear", "Álgebra Linear e Sequências"),
        ("aplicada", "Matemática Aplicada e Estatística"),
    ]
    
    radar_areas = []
    for slug_area, nome_exibicao in areas_mapeadas:
        stmt_area = (
            select(HistoricoTheta.theta_estimado)
            .where(
                and_(
                    HistoricoTheta.usuario_id == current_user.id,
                    HistoricoTheta.grande_area == slug_area
                )
            )
            .order_by(HistoricoTheta.registrado_em.desc())
            .limit(1)
        )
        theta_area = (await db.execute(stmt_area)).scalar_one_or_none()
        score_val = round(float(theta_area), 2) if theta_area is not None else round(theta_atual, 2)
        radar_areas.append(
            RadarAreaItem(
                area=nome_exibicao,
                score_entrada_cat=round(score_val - 0.25, 2),
                score_atual=score_val
            )
        )

    return ProgressoGeralResponse(
        usuario_id=current_user.id,
        theta_atual=round(theta_atual, 2),
        erro_padrao_se=round(se_atual, 2),
        classificacao_nivel=nivel,
        completude_global_percentual=completude_real,
        horas_estudo_liquidas_total=horas_liquidas,
        streak_dias_consecutivos=1,
        radar_areas=radar_areas
    )


# ============================================================================
# 2. Heatmap por Volume
# ============================================================================

@router.get("/heatmap/{volume_id}", response_model=HeatmapVolumeResponse)
async def obter_heatmap_volume(
    volume_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retorna os nós e as cores consolidadas do Heatmap para o volume selecionado."""
    try:
        return await HeatmapService.obter_heatmap_volume(db, current_user.id, volume_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


# ============================================================================
# 3. Hub de Ação nos Top 3 Tópicos Críticos
# ============================================================================

@router.get("/top-criticos", response_model=HubAcaoTop3Response)
async def obter_top_criticos(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retorna os 3 capítulos que mais exigem atenção com opções de ação direta."""
    return await HeatmapService.obter_top_3_criticos(db, current_user.id)


# ============================================================================
# 4. Download do Boletim Oficial em PDF
# ============================================================================

@router.get("/boletim-pdf")
async def baixar_boletim_pdf(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Compila dinamicamente o boletim formal do estudante em PDF vetorial de alta definição.
    Retorna o binário com download automático (Content-Disposition: attachment).
    """
    progresso = await obter_progresso_geral(current_user, db)

    areas_formatadas = [
        {"area": item.area, "score_entrada": item.score_entrada_cat, "score_atual": item.score_atual}
        for item in progresso.radar_areas
    ]

    pdf_bytes = BoletimPDFGenerator.gerar_boletim_bytes(
        nome_aluno=current_user.nome_completo,
        cpf_aluno=current_user.cpf,
        serie_ano=getattr(current_user, "serie_ano", "Ensino Médio"),
        theta_geral=progresso.theta_atual,
        nivel_classificacao=progresso.classificacao_nivel,
        horas_liquidas=progresso.horas_estudo_liquidas_total,
        aulas_concluidas=progresso.aulas_concluidas_count,
        scores_areas=areas_formatadas
    )

    nome_arquivo = f"Boletim_{current_user.nome_completo.replace(' ', '_')}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'}
    )


# ============================================================================
# 5. Registro Contínuo de Tempo de Estudo Ativo
# ============================================================================

from pydantic import BaseModel, Field
from datetime import date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import insert as pg_insert


class RegistrarTempoEstudoRequest(BaseModel):
    segundos_ativos: int = Field(..., ge=1, le=3600, description="Tempo ativo medido sem ociosidade")


@router.post("/tempo-estudo")
async def registrar_tempo_estudo(
    payload: RegistrarTempoEstudoRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-PRG-003: Recebe blocos incrementais de tempo líquido de estudo ativo
    enviados periodicamente pelo cronômetro inteligente (useStudyTimer).
    Este endpoint é o ESCRITOR EXCLUSIVO de segundos_ativos (Tabela 17); a
    fixação e a submissão de exercícios NÃO gravam tempo (sem contagem dupla).
    """
    hoje = date.today()

    stmt = (
        pg_insert(HorasEstudoDiaria)
        .values(
            id=uuid4(),
            usuario_id=current_user.id,
            data_registro=hoje,
            segundos_ativos=payload.segundos_ativos,
            aulas_concluidas=0,
            exercicios_submetidos=0
        )
        .on_conflict_do_update(
            constraint="uk_horas_usuario_data",
            set_={"segundos_ativos": HorasEstudoDiaria.segundos_ativos + payload.segundos_ativos}
        )
    )
    await db.execute(stmt)
    await db.commit()

    return {"sucesso": True, "segundos_adicionados": payload.segundos_ativos, "data": hoje.isoformat()}
```
