"""
Roteador FastAPI do Módulo de Progresso & Analytics.
Em conformidade com docs-site/docs/modules/progresso/prototype/endpoints.md.
"""
from uuid import UUID, uuid4
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import Usuario
from app.models.progress import HistoricoTheta, HeatmapDominio, HorasEstudoDiarias
from app.models.content import Capitulo
from app.models.exercise import ProvaCat
from app.modules.progress.schemas import (
    ProgressoGeralResponse,
    HeatmapVolumeResponse,
    HubAcaoTop3Response,
    RadarAreaItem,
    TimelineThetaItem,
    VolumeResumoItem,
    RegistrarTempoEstudoRequest,
    RegistrarTempoEstudoResponse,
)
from app.modules.progress.heatmap_service import HeatmapService
from app.modules.progress.pdf_generator import BoletimPDFGenerator

router = APIRouter(prefix="/api/v1/progresso", tags=["Progresso & Analytics"])


# ============================================================================
# 1. Visão Geral de Métricas Tridimensionais e Radar
# ============================================================================

@router.get("/geral", response_model=ProgressoGeralResponse)
async def obter_progresso_geral(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna os indicadores unificados do estudante:
    - Theta geral contínuo da TRI (-3.0 a +3.0)
    - Tempo líquido ativo acumulado
    - Streak de dias consecutivos
    - Dados multiaxiais para o Gráfico Radar comparativo (Entrada vs Atual)
    - Série temporal para o gráfico de evolução
    """
    # 1. Busca o último theta global registrado
    stmt_theta = (
        select(HistoricoTheta.theta_estimado, HistoricoTheta.erro_padrao_se)
        .where(
            and_(
                HistoricoTheta.usuario_id == current_user.id,
                HistoricoTheta.grande_area == "geral",
            )
        )
        .order_by(HistoricoTheta.registrado_em.desc())
        .limit(1)
    )
    res_theta = await db.execute(stmt_theta)
    theta_row = res_theta.first()

    # Fallback se ainda não houver 'geral' explícito: busca o último de qualquer área ou ProvaCat
    if not theta_row:
        stmt_any = (
            select(HistoricoTheta.theta_estimado, HistoricoTheta.erro_padrao_se)
            .where(HistoricoTheta.usuario_id == current_user.id)
            .order_by(HistoricoTheta.registrado_em.desc())
            .limit(1)
        )
        theta_row = (await db.execute(stmt_any)).first()

    if not theta_row:
        # Fallback para prova CAT concluída se houver
        stmt_cat = (
            select(ProvaCat.theta_geral, ProvaCat.erro_padrao_se)
            .where(
                and_(
                    ProvaCat.usuario_id == current_user.id,
                    ProvaCat.finalizado_em.isnot(None),
                )
            )
            .order_by(ProvaCat.finalizado_em.desc())
            .limit(1)
        )
        cat_row = (await db.execute(stmt_cat)).first()
        if cat_row:
            theta_atual = float(cat_row[0])
            se_atual = float(cat_row[1])
        else:
            theta_atual = 0.00
            se_atual = 0.35
    else:
        theta_atual = float(theta_row[0])
        se_atual = float(theta_row[1])

    # Classificação de maestria (RN-PRG-009)
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
            HeatmapDominio.aula_concluida == True,
        )
    )
    caps_concluidos = (await db.execute(stmt_concluidos)).scalar() or 0
    completude_real = round((caps_concluidos / total_caps) * 100.0, 1)

    # 4. Cálculo de Sequência de Dias Ativos (Streaks - RN-PRG-005)
    # Um dia é "ativo" se o aluno registrou tempo de estudo OU submeteu exercícios.
    # A sequência conta dias consecutivos terminando hoje ou ontem; se o último dia
    # ativo for mais antigo que ontem, o streak é zero.
    stmt_dias = (
        select(
            HorasEstudoDiarias.data_registro,
        )
        .where(
            and_(
                HorasEstudoDiarias.usuario_id == current_user.id,
                # RN-PRG-005: dia ativo = concluir ao menos 1 aula OU submeter
                # ao menos 1 lista/bateria de exercícios (OU-lógico).
                or_(
                    HorasEstudoDiarias.aulas_concluidas > 0,
                    HorasEstudoDiarias.exercicios_submetidos > 0,
                ),
            )
        )
        .order_by(HorasEstudoDiarias.data_registro.desc())
    )
    dias_ativos = (await db.execute(stmt_dias)).scalars().all()
    streak = 0
    hoje = date.today()
    dia_esperado = hoje

    for d in dias_ativos:
        if d == hoje or d == hoje - timedelta(days=1):
            if streak == 0:
                # Ancora a sequência: hoje ou ontem são os únicos pontos de partida válidos
                dia_esperado = d
                streak = 1
            elif d == dia_esperado:
                continue  # Dia já contabilizado
            elif d == dia_esperado - timedelta(days=1):
                streak += 1
                dia_esperado = d
            else:
                break  # Lacuna encontrada: sequência interrompida
        else:
            break  # Registro anterior ao ponto de partida válido

    # 5. 4 Eixos Canônicos do Gráfico Radar (RN-PRG-013)
    areas_mapeadas = [
        ("algebra_funcoes", "Álgebra e Funções"),
        ("geometria", "Geometria e Trigonometria"),
        ("algebra_linear", "Álgebra Linear e Sequências"),
        ("aplicada", "Matemática Aplicada e Estatística"),
    ]
    slugs_areas = [slug for slug, _ in areas_mapeadas]

    # Scores em lote com DISTINCT ON (2 queries no total, sem N+1 por área):
    # "atual" = último theta por área; "entrada" = primeiro onboarding_cat por área.
    stmt_atual = (
        select(
            HistoricoTheta.grande_area,
            HistoricoTheta.theta_estimado,
        )
        .distinct(HistoricoTheta.grande_area)
        .where(
            and_(
                HistoricoTheta.usuario_id == current_user.id,
                HistoricoTheta.grande_area.in_(slugs_areas),
            )
        )
        .order_by(HistoricoTheta.grande_area, HistoricoTheta.registrado_em.desc())
    )
    atual_por_area = {
        area: float(theta)
        for area, theta in (await db.execute(stmt_atual)).all()
    }

    stmt_entrada = (
        select(
            HistoricoTheta.grande_area,
            HistoricoTheta.theta_estimado,
        )
        .distinct(HistoricoTheta.grande_area)
        .where(
            and_(
                HistoricoTheta.usuario_id == current_user.id,
                HistoricoTheta.grande_area.in_(slugs_areas),
                HistoricoTheta.origem_ajuste == "onboarding_cat",
            )
        )
        .order_by(HistoricoTheta.grande_area, HistoricoTheta.registrado_em.asc())
    )
    entrada_por_area = {
        area: float(theta)
        for area, theta in (await db.execute(stmt_entrada)).all()
    }

    radar_areas = []
    for slug_area, nome_exibicao in areas_mapeadas:
        score_atual_val = (
            round(atual_por_area[slug_area], 2)
            if slug_area in atual_por_area
            else round(theta_atual, 2)
        )
        score_entrada_val = (
            round(entrada_por_area[slug_area], 2)
            if slug_area in entrada_por_area
            else round(score_atual_val - 0.20, 2)
        )

        radar_areas.append(
            RadarAreaItem(
                area=nome_exibicao,
                slug_area=slug_area,
                score_entrada_cat=score_entrada_val,
                score_atual=score_atual_val,
            )
        )

    # 6. Linha do Tempo (últimos registros para o gráfico)
    # Subquery pega os 30 registros MAIS RECENTES (desc) e o wrapper reordena
    # em asc para o gráfico. Um .limit() direto em asc pegaria os 30 mais
    # antigos e a timeline congelaria no passado após o 31º registro.
    subq_ultimos = (
        select(HistoricoTheta.id)
        .where(HistoricoTheta.usuario_id == current_user.id)
        .order_by(HistoricoTheta.registrado_em.desc(), HistoricoTheta.id.desc())
        .limit(30)
        .subquery()
    )
    stmt_timeline = (
        select(HistoricoTheta)
        .join(subq_ultimos, HistoricoTheta.id == subq_ultimos.c.id)
        .order_by(HistoricoTheta.registrado_em.asc(), HistoricoTheta.id.asc())
    )
    registros_timeline = (await db.execute(stmt_timeline)).scalars().all()
    timeline_items = [
        TimelineThetaItem(
            data=reg.registrado_em.strftime("%d/%m %H:%M") if reg.registrado_em else "",
            theta_estimado=round(float(reg.theta_estimado), 2),
            origem_ajuste=reg.origem_ajuste,
        )
        for reg in registros_timeline
    ]

    return ProgressoGeralResponse(
        usuario_id=current_user.id,
        theta_atual=round(theta_atual, 2),
        erro_padrao_se=round(se_atual, 2),
        classificacao_nivel=nivel,
        completude_global_percentual=completude_real,
        horas_estudo_liquidas_total=horas_liquidas,
        aulas_concluidas_count=caps_concluidos,
        streak_dias_consecutivos=streak,
        radar_areas=radar_areas,
        timeline=timeline_items,
    )


# ============================================================================
# 2. Resumo de Volumes (Navegação de Abas)
# ============================================================================

@router.get("/volumes", response_model=List[VolumeResumoItem])
async def listar_volumes_resumo(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retorna os volumes didáticos disponíveis com métricas de completude para as abas."""
    return await HeatmapService.listar_resumo_volumes(db, current_user.id)


# ============================================================================
# 3. Heatmap por Volume
# ============================================================================

@router.get("/heatmap/{volume_id}", response_model=HeatmapVolumeResponse)
async def obter_heatmap_volume(
    volume_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retorna os nós e as cores consolidadas do Heatmap para o volume selecionado."""
    try:
        return await HeatmapService.obter_heatmap_volume(db, current_user.id, volume_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


# ============================================================================
# 4. Hub de Ação nos Top 3 Gargalos Críticos
# ============================================================================

@router.get("/top-criticos", response_model=HubAcaoTop3Response)
async def obter_top_criticos(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """RN-PRG-016: Retorna os 3 capítulos que mais exigem atenção com opções de ação direta."""
    return await HeatmapService.obter_top_3_criticos(db, current_user.id)


# ============================================================================
# 5. Download do Boletim Escolar em PDF
# ============================================================================

@router.get("/boletim-pdf")
async def baixar_boletim_pdf(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Compila dinamicamente o boletim formal do estudante em PDF vetorial via ReportLab.
    Retorna o binário para download imediato.
    """
    progresso = await obter_progresso_geral(current_user, db)

    areas_formatadas = [
        {"area": item.area, "score_entrada": item.score_entrada_cat, "score_atual": item.score_atual}
        for item in progresso.radar_areas
    ]

    nome_estudante = current_user.nome if hasattr(current_user, "nome") and current_user.nome else "Estudante"
    serie_ano = getattr(current_user, "ano_escolar", "Ensino Médio")

    pdf_bytes = BoletimPDFGenerator.gerar_boletim_bytes(
        nome_aluno=nome_estudante,
        cpf_aluno=current_user.cpf or "",
        serie_ano=serie_ano,
        theta_geral=progresso.theta_atual,
        nivel_classificacao=progresso.classificacao_nivel,
        horas_liquidas=progresso.horas_estudo_liquidas_total,
        aulas_concluidas=progresso.aulas_concluidas_count,
        scores_areas=areas_formatadas,
    )

    nome_sanitizado = nome_estudante.replace(" ", "_")
    nome_arquivo = f"Boletim_{nome_sanitizado}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )


# ============================================================================
# 6. Registro Contínuo de Tempo de Estudo Ativo
# ============================================================================

@router.post("/tempo-estudo", response_model=RegistrarTempoEstudoResponse)
async def registrar_tempo_estudo(
    payload: RegistrarTempoEstudoRequest,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    RN-PRG-003: Recebe blocos incrementais de tempo líquido de estudo ativo
    enviados periodicamente pelo cronômetro inteligente da tela de aula.
    Utiliza UPSERT (ON CONFLICT DO UPDATE) somando os segundos do dia.
    """
    hoje = date.today()

    stmt = (
        pg_insert(HorasEstudoDiarias)
        .values(
            id=uuid4(),
            usuario_id=current_user.id,
            data_registro=hoje,
            segundos_ativos=payload.segundos_ativos,
            aulas_concluidas=0,
            exercicios_submetidos=0,
        )
        .on_conflict_do_update(
            constraint="uk_horas_usuario_data",
            set_={"segundos_ativos": HorasEstudoDiarias.segundos_ativos + payload.segundos_ativos},
        )
    )
    await db.execute(stmt)
    await db.commit()

    return RegistrarTempoEstudoResponse(
        sucesso=True,
        segundos_adicionados=payload.segundos_ativos,
        data=hoje.isoformat(),
    )
