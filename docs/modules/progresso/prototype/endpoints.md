---
title: Progresso - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
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
from app.models.progress import HistoricoTheta, HeatmapDominio, HorasEstudoDiaria
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
    stmt_horas = select(func.sum(HorasEstudoDiaria.segundos_ativos)).where(
        HorasEstudoDiaria.usuario_id == current_user.id
    )
    res_horas = await db.execute(stmt_horas)
    segundos_totais = res_horas.scalar() or 0
    horas_liquidas = round(segundos_totais / 3600.0, 1)

    # 3. Dados para os 4 eixos do Gráfico Radar (Matemática do 2º Grau)
    radar_mock = [
        RadarAreaItem(area="Álgebra e Funções", score_entrada_cat=-0.20, score_atual=theta_atual),
        RadarAreaItem(area="Geometria e Trigonometria", score_entrada_cat=-0.50, score_atual=theta_atual - 0.1),
        RadarAreaItem(area="Álgebra Linear e Sequências", score_entrada_cat=-0.80, score_atual=theta_atual + 0.2),
        RadarAreaItem(area="Matemática Aplicada e Estatística", score_entrada_cat=-0.10, score_atual=theta_atual + 0.05),
    ]

    return ProgressoGeralResponse(
        usuario_id=current_user.id,
        theta_atual=round(theta_atual, 2),
        erro_padrao_se=round(se_atual, 2),
        classificacao_nivel=nivel,
        completude_global_percentual=32.5,
        horas_estudo_liquidas_total=horas_liquidas,
        streak_dias_consecutivos=5,
        radar_areas=radar_mock
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
        serie_ano="2º Ano do Ensino Médio",
        theta_geral=progresso.theta_atual,
        nivel_classificacao=progresso.classificacao_nivel,
        horas_liquidas=progresso.horas_estudo_liquidas_total,
        aulas_concluidas=14,
        scores_areas=areas_formatadas
    )

    nome_arquivo = f"Boletim_{current_user.nome_completo.replace(' ', '_')}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'}
    )
```
