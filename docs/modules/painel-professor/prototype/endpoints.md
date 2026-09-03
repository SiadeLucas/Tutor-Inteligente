---
title: Painel do Professor - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/painel-professor/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 5. Endpoints Administrativos da API FastAPI

Implementação das rotas exclusivas do professor com **autorização estrita (`role == 'teacher'`)**, consulta de analytics, curadoria KaTeX e conciliação financeira (`app/modules/teacher/router.py`).

---

## Código Fonte (`backend/app/modules/teacher/router.py`)

```python
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, desc

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.models.user import Usuario
from app.models.content import Aula
from app.models.payment import TransacaoFinanceira, MatriculaPagamento
from app.modules.teacher.schemas import (
    DashboardAnalyticsResponse,
    AlunoFichaResponse,
    ExtratoFinanceiroResponse,
    TransacaoExtratoItem,
    CuradoriaAulaRequest
)
from app.modules.teacher.analytics_service import TeacherAnalyticsService

router = APIRouter(prefix="/api/v1/teacher", tags=["Painel do Professor"])


def require_teacher_role(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Garante que apenas contas docentes acessem este ecossistema."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao perfil de Professor."
        )
    return current_user


# ============================================================================
# 1. Dashboard de Analytics Executivo
# ============================================================================

@router.get("/analytics", response_model=DashboardAnalyticsResponse)
async def obter_dashboard_docente(
    teacher: Usuario = Depends(require_teacher_role),
    db: AsyncSession = Depends(get_db)
):
    """Retorna os indicadores consolidados de faturamento e demografia."""
    return await TeacherAnalyticsService.obter_dashboard_analytics(db)


# ============================================================================
# 2. Listagem e Dossiê de Estudantes (Somente Leitura)
# ============================================================================

@router.get("/alunos", response_model=List[AlunoFichaResponse])
async def listar_estudantes(
    busca: Optional[str] = Query(None, description="Filtra por Nome, CPF ou E-mail"),
    limite: int = Query(50, le=100),
    teacher: Usuario = Depends(require_teacher_role),
    db: AsyncSession = Depends(get_db)
):
    """Lista os estudantes matriculados para supervisão passiva."""
    stmt = select(Usuario).where(Usuario.role == "student")
    if busca:
        termo = f"%{busca}%"
        stmt = stmt.where(
            or_(
                Usuario.nome_completo.ilike(termo),
                Usuario.email.ilike(termo),
                Usuario.cpf.like(termo)
            )
        )
    stmt = stmt.order_by(desc(Usuario.criado_em)).limit(limite)
    result = await db.execute(stmt)
    alunos = result.scalars().all()

    return [await TeacherAnalyticsService.obter_ficha_aluno(db, a.id) for a in alunos]


@router.get("/alunos/{aluno_id}", response_model=AlunoFichaResponse)
async def obter_dossie_estudante(
    aluno_id: UUID,
    teacher: Usuario = Depends(require_teacher_role),
    db: AsyncSession = Depends(get_db)
):
    """Abre a ficha pedagógica do estudante (dados, proficiência e horas)."""
    try:
        return await TeacherAnalyticsService.obter_ficha_aluno(db, aluno_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


# ============================================================================
# 3. Curadoria de Conteúdos KaTeX
# ============================================================================

@router.put("/curadoria/aulas/{capitulo_id}")
async def salvar_curadoria_aula(
    capitulo_id: UUID,
    payload: CuradoriaAulaRequest,
    teacher: Usuario = Depends(require_teacher_role),
    db: AsyncSession = Depends(get_db)
):
    """Permite ao professor refinar o material instrucional KaTeX de um capítulo."""
    stmt = select(Aula).where(Aula.capitulo_id == capitulo_id)
    res = await db.execute(stmt)
    aula = res.scalar_one_or_none()

    if not aula:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não localizada.")

    aula.bloco1_teoria_katex = payload.bloco1_teoria_katex
    aula.bloco2_exemplos_katex = payload.bloco2_exemplos_katex
    aula.bloco3_dicas_ia = payload.bloco3_dicas_ia
    if payload.video_url:
        aula.video_url = payload.video_url
    aula.atualizado_por = teacher.id

    await db.commit()
    return {"sucesso": True, "mensagem": "Conteúdo instrucional atualizado com sucesso."}


# ============================================================================
# 4. Extrato Financeiro de Vendas
# ============================================================================

@router.get("/financeiro/extrato", response_model=ExtratoFinanceiroResponse)
async def obter_extrato_vendas(
    teacher: Usuario = Depends(require_teacher_role),
    db: AsyncSession = Depends(get_db)
):
    """Extrato financeiro com taxa de gateway e valores líquidos repassados."""
    stmt = (
        select(TransacaoFinanceira, Usuario.nome_completo, MatriculaPagamento.tipo_produto)
        .join(Usuario, TransacaoFinanceira.usuario_id == Usuario.id)
        .outerjoin(MatriculaPagamento, TransacaoFinanceira.matricula_id == MatriculaPagamento.id)
        .order_by(desc(TransacaoFinanceira.criado_em))
        .limit(100)
    )
    result = await db.execute(stmt)
    linhas = result.all()

    total_liquido = sum(float(tx.valor_liquido) for tx, _, _ in linhas if tx.status_transacao == "paid")

    itens = [
        TransacaoExtratoItem(
            id=tx.id,
            aluno_nome=nome,
            tipo_produto=produto or "capitulo_avulso",
            metodo=tx.metodo,
            valor_bruto=float(tx.valor_bruto),
            taxa_gateway=float(tx.taxa_gateway),
            valor_liquido=float(tx.valor_liquido),
            status_transacao=tx.status_transacao,
            pago_em=tx.pago_em
        )
        for tx, nome, produto in linhas
    ]

    return ExtratoFinanceiroResponse(
        total_liquido_acumulado=round(total_liquido, 2),
        saldo_disponivel_repasse=round(total_liquido * 0.95, 2),
        transacoes=itens
    )
```
