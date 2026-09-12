"""
Rotas da API do Painel do Professor (Etapa 10).
Prefixo: /api/v1/teacher
Proteção: Exclusiva para usuários com perfil docente ou administrativo (require_teacher_role).
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_teacher_role
from app.models.user import Usuario
from app.modules.teacher.schemas import (
    TeacherAnalyticsResponse,
    AlunosPaginadosResponse,
    AlunoDossieDTO,
    CuradoriaVolumeDTO,
    CuradoriaAulaDetalheDTO,
    CuradoriaAulaUpdatePayload,
    ExtratoFinanceiroResponse,
    EstornoResponse,
)
from app.modules.teacher.service import TeacherService, _mascarar_cpf
from app.modules.progress.pdf_generator import BoletimPDFGenerator

router = APIRouter(
    prefix="/api/v1/teacher",
    tags=["Painel do Professor"],
    dependencies=[Depends(require_teacher_role)],
)


@router.get(
    "/analytics",
    response_model=TeacherAnalyticsResponse,
    summary="Obter indicadores e analytics globais consolidados",
    description="Retorna faturamento líquido/bruto, total de alunos, distribuição demográfica e faixas TRI com zero queries N+1.",
)
async def get_dashboard_analytics(
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.calcular_analytics(db)


@router.get(
    "/alunos",
    response_model=AlunosPaginadosResponse,
    summary="Listagem paginada de estudantes com busca e filtros",
    description="Permite pesquisar alunos por nome, CPF ou e-mail, filtrando por tipo de instituição e UF.",
)
async def listar_alunos(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(20, ge=1, le=100, description="Registros por página"),
    search: Optional[str] = Query(None, description="Termo de busca (nome, CPF ou e-mail)"),
    escola_tipo: Optional[str] = Query(None, description="Filtro por rede escolar"),
    uf: Optional[str] = Query(None, max_length=2, description="Filtro por Unidade Federativa (UF)"),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.listar_alunos(
        db=db,
        page=page,
        limit=limit,
        search=search,
        escola_tipo=escola_tipo,
        uf=uf,
    )


@router.get(
    "/alunos/{aluno_id}",
    response_model=AlunoDossieDTO,
    summary="Obter dossiê pedagógico individual do estudante",
    description="Retorna dados cadastrais, contato de responsáveis (menor de 18), histórico theta, radar e auditoria de submissões.",
)
async def get_dossie_aluno(
    aluno_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.obter_dossie_aluno(db, aluno_id)


@router.get(
    "/alunos/{aluno_id}/boletim",
    summary="Download do Boletim Docente em PDF",
    description="Gera dinamicamente o boletim formal vetorial em PDF do estudante via ReportLab.",
)
async def baixar_boletim_aluno(
    aluno_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    dossie = await TeacherService.obter_dossie_aluno(db, aluno_id)

    scores_areas = [
        {"nome_area": r["area"], "grau_dominio": r["dominio"] / 100.0}
        for r in dossie.radar_areas
    ]

    pdf_bytes = BoletimPDFGenerator.gerar_boletim_bytes(
        nome_aluno=dossie.nome_completo,
        cpf_aluno=dossie.cpf_mascarado,
        serie_ano=dossie.serie_ano,
        theta_geral=dossie.theta_atual,
        nivel_classificacao=dossie.faixa_tri.upper(),
        horas_liquidas=dossie.horas_liquidas_total,
        aulas_concluidas=dossie.total_exercicios_resolvidos,
        scores_areas=scores_areas,
    )

    nome_arquivo = f"Boletim_{dossie.nome_completo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{nome_arquivo}"'
        },
    )


@router.get(
    "/curadoria/volumes",
    response_model=List[CuradoriaVolumeDTO],
    summary="Listar 11 volumes e capítulos para curadoria",
    description="Retorna árvore completa de conteúdos didáticos com status de publicação das aulas.",
)
async def listar_curadoria_volumes(
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.listar_volumes_curadoria(db)


@router.get(
    "/curadoria/aulas/{capitulo_id}",
    response_model=CuradoriaAulaDetalheDTO,
    summary="Obter conteúdo instrucional KaTeX de uma aula",
    description="Retorna os blocos 1 (Teoria), 2 (Exemplos) e 3 (Dicas IA) para conferência ou edição split-screen.",
)
async def get_aula_curadoria(
    capitulo_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.obter_aula_curadoria(db, capitulo_id)


@router.put(
    "/curadoria/aulas/{capitulo_id}",
    response_model=CuradoriaAulaDetalheDTO,
    summary="Atualizar conteúdo instrucional KaTeX de uma aula",
    description="Permite ao professor editar textos com fórmulas matemáticas, vídeo URL e publicar o capítulo.",
)
async def atualizar_aula_curadoria(
    capitulo_id: UUID,
    payload: CuradoriaAulaUpdatePayload,
    db: AsyncSession = Depends(get_db),
    teacher: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.atualizar_aula_curadoria(
        db=db,
        capitulo_id=capitulo_id,
        payload=payload,
        teacher_id=teacher.id,
    )


@router.get(
    "/financeiro/extrato",
    response_model=ExtratoFinanceiroResponse,
    summary="Extrato contábil e financeiro consolidado",
    description="Detalhamento de entradas brutas, taxas do gateway Asaas retidas, saldo líquido e histórico de transações.",
)
async def get_extrato_financeiro(
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(30, ge=1, le=100, description="Itens por página"),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.obter_extrato_financeiro(db=db, page=page, limit=limit)


@router.post(
    "/matriculas/{matricula_id}/estorno",
    response_model=EstornoResponse,
    summary="Estorno e cancelamento administrativo de matrícula (CDC 7 dias)",
    description="Processa o reembolso integral com comunicação ao Asaas e revogação imediata de acesso.",
)
async def processar_estorno(
    matricula_id: UUID,
    db: AsyncSession = Depends(get_db),
    teacher: Usuario = Depends(require_teacher_role),
):
    return await TeacherService.processar_estorno(
        db=db,
        matricula_id=matricula_id,
        teacher_id=teacher.id,
    )
