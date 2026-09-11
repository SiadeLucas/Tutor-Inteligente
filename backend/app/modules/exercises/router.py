"""
Endpoints da API FastAPI para o Módulo de Exercícios e Motor CAT.
Rotas sob prefixo /api/v1/exercicios conforme docs-site/docs/implementation/etapa-07-exercicios.md.
"""
from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import Usuario
from app.modules.exercises.schemas import (
    SubmissaoExercicioRequest,
    SubmissaoExercicioResponse,
    IniciarCatRequest,
    IniciarCatResponse,
    AbandonarCatResponse,
    SubmeterCatRequest,
    CatStatusResponse,
    ItemExercicioResponse,
)
from app.modules.exercises.service import ExercisesService

router = APIRouter(prefix="/api/v1/exercicios", tags=["Exercícios & Avaliações"])


# ============================================================================
# 1. Submissão de Fixação com 2ª Chance (1.0 vs 0.5 vs 0.0)
# ============================================================================

@router.post("/submeter", response_model=SubmissaoExercicioResponse, summary="Submeter exercício com lógica de 2ª chance")
async def submeter_exercicio(
    payload: SubmissaoExercicioRequest,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submete a resolução de um item:
    - 1ª tentativa: acerto = 1.0; erro = concede 2ª chance com pista socrática.
    - 2ª tentativa: acerto = 0.5; erro = 0.0, adiciona à Caixa de Reforço e libera Questão Gêmea.
    """
    return await ExercisesService.submeter_exercicio(payload, current_user, db)


# ============================================================================
# 2. Geração de Questões Gêmeas
# ============================================================================

@router.post("/gerar-gemea/{item_matriz_id}", response_model=ItemExercicioResponse, summary="Gerar Questão Gêmea determinística")
async def gerar_questao_gemea(
    item_matriz_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Gera uma Questão Gêmea a partir do item matriz via mutação paramétrica determinística SymPy,
    atestando tolerância analítica exata (±0.01) e herdando os parâmetros TRI.
    """
    return await ExercisesService.gerar_questao_gemea(item_matriz_id, current_user, db)


# ============================================================================
# 3. Inicialização e Submissão do Teste Adaptativo CAT
# ============================================================================

@router.post("/cat/iniciar", response_model=IniciarCatResponse, summary="Iniciar sessão de Prova Adaptativa CAT")
async def iniciar_sessao_cat(
    payload: IniciarCatRequest,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Instancia uma nova sessão de Prova Diagnóstica CAT com prior N(0, 1),
    selecionando o 1º item por máxima Informação de Fisher (MFI).

    Se o aluno já possui uma sessão pendente (ex.: fechou a aba no meio da
    prova), RETOMA automaticamente de onde parou, preservando o theta já
    calibrado (RN-EXE-010 — resiliência de sessão).
    """
    return await ExercisesService.iniciar_sessao_cat(payload, current_user, db)


@router.delete("/cat/{sessao_id}", response_model=AbandonarCatResponse, summary="Abandonar sessão CAT em andamento")
async def abandonar_sessao_cat(
    sessao_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Descarta uma sessão CAT pendente (saída de emergência). A calibragem
    parcial é perdida: a próxima prova recomeça de theta=0.
    """
    return await ExercisesService.abandonar_sessao_cat(sessao_id, current_user, db)


@router.get("/cat/historico", response_model=List[Dict[str, Any]], summary="Histórico de provas CAT finalizadas do estudante")
async def historico_provas_cat(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna as provas CAT já concluídas do estudante (mais recente primeiro).
    Usado pelo frontend para verificar a pendência da prova diagnóstica de onboarding
    (disparo no primeiro acesso a uma matéria, conforme etapa-04-onboarding.md).
    """
    return await ExercisesService.listar_historico_cat(current_user, db)


@router.post("/cat/submeter", response_model=CatStatusResponse, summary="Submeter resposta na Prova CAT (Submissão Cega)")
async def submeter_resposta_cat(
    payload: SubmeterCatRequest,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submissão cega CAT (sem feedback intermediário imediato):
    - Atualiza a proficiência theta Bayesiana pelo estimador EAP.
    - Se continuar: devolve a próxima questão e indicador de progresso.
    - Se atingir o critério de parada (SE <= 0.30 ou N=20): finaliza a sessão e devolve o Radar Chart.
    """
    return await ExercisesService.submeter_resposta_cat(payload, current_user, db)


# ============================================================================
# 4. Bateria de Fixação do Capítulo
# ============================================================================

@router.get("/capitulo/{capitulo_id}", response_model=List[ItemExercicioResponse], summary="Obter bateria de exercícios do capítulo")
async def obter_bateria_capitulo(
    capitulo_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna 3 a 5 exercícios de fixação do capítulo ordenados por dificuldade crescente (parâmetro b).
    Gabarito ocultado para validação server-side.
    """
    return await ExercisesService.obter_bateria_fixacao(capitulo_id, db)


# ============================================================================
# 5. Consulta da Caixa de Reforço
# ============================================================================

@router.get("/caixa-reforco", response_model=List[Dict[str, Any]], summary="Listar itens pendentes na Caixa de Reforço")
async def listar_caixa_reforco(
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna os itens arquivados na Caixa de Reforço nos quais o estudante cometeu erro duplo.
    """
    return await ExercisesService.listar_caixa_reforco(current_user, db)
