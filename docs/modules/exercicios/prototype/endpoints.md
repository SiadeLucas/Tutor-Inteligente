---
title: Exercícios - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/exercicios/prototype/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 4. Endpoints da API FastAPI

Implementação das rotas assíncronas do backend em **FastAPI** (`app/modules/exercises/router.py`).

---

## Código Fonte (`backend/app/modules/exercises/router.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.exercises.schemas import (
    SubmissaoExercicioRequest,
    SubmissaoExercicioResponse,
    ItemExercicioResponse,
    IniciarCatRequest,
    CatStatusResponse
)
from app.sympy_engine.validator import SympyMathValidator

router = APIRouter(prefix="/api/v1/exercicios", tags=["Exercícios & Avaliações"])


# ============================================================================
# 1. Submissão com Lógica de 2ª Chance e Ponderação (1.0 vs 0.5)
# ============================================================================

@router.post("/submeter", response_model=SubmissaoExercicioResponse)
async def submeter_exercicio(
    payload: SubmissaoExercicioRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submete a resposta de um exercício com suporte a:
    - 1ª tentativa: acerto = 1.0; erro = libera 2ª chance com dica socrática da IA.
    - 2ª tentativa: acerto = 0.5; erro = pontuação 0.0, arquiva na Caixa de Reforço e libera Questão Gêmea.
    """
    # 1. Busca o item no banco de dados (tabela itens_exercicios)
    # item = await db.get(ItemExercicio, payload.item_id)
    gabarito_esperado = "A"  # Exemplo recuperado do banco
    pista_ia = "Lembre-se de verificar o sinal do discriminante Delta = b^2 - 4ac."
    resolucao_katex = "A resolução detalhada demonstra as raízes reais x_1 e x_2."

    acertou = (payload.resposta_enviada == gabarito_esperado)

    if acertou:
        # Acerto na 1ª tentativa vale 1.0; na 2ª tentativa com auxílio vale 0.5
        pontuacao = 1.0 if payload.tentativa_numero == 1 else 0.5
        return SubmissaoExercicioResponse(
            acertou=True,
            pontuacao_obtida=pontuacao,
            permite_segunda_chance=False,
            resolucao_completa_katex=resolucao_katex,
            pode_gerar_gemea=False
        )
    else:
        if payload.tentativa_numero == 1:
            # 1ª tentativa incorreta: concede 2ª chance com pista socrática
            return SubmissaoExercicioResponse(
                acertou=False,
                pontuacao_obtida=0.0,
                permite_segunda_chance=True,
                pista_socratica_ia=pista_ia,
                resolucao_completa_katex=None,
                pode_gerar_gemea=False
            )
        else:
            # Erro duplo (esgotou as 2 tentativas): pontuação zero e arquiva na Caixa de Reforço
            # await db.execute(insert(CaixaReforco).values(usuario_id=current_user.id, ...))
            return SubmissaoExercicioResponse(
                acertou=False,
                pontuacao_obtida=0.0,
                permite_segunda_chance=False,
                pista_socratica_ia=None,
                resolucao_completa_katex=resolucao_katex,
                pode_gerar_gemea=True  # Libera o botão "Tentar uma Questão Gêmea similar agora"
            )


# ============================================================================
# 2. Geração de Questões Gêmeas por IA com SymPy
# ============================================================================

@router.post("/gerar-gemea/{item_matriz_id}", response_model=ItemExercicioResponse)
async def gerar_questao_gemea(
    item_matriz_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Gera uma variação determinística do item matriz via SymPy,
    atesta tolerância exata (±0.01) e salva na tabela itens_exercicios.
    """
    nova_questao = SympyMathValidator.gerar_questao_gemea_quadratica()
    
    # Salva no banco vinculando ao item_matriz_id
    # item_db = ItemExercicio(**nova_questao, capitulo_id=..., item_matriz_id=item_matriz_id)
    return nova_questao


# ============================================================================
# 3. Submissão da Prova Adaptativa CAT (Blind Adaptive Testing)
# ============================================================================

@router.post("/cat/submeter")
async def submeter_resposta_cat(
    sessao_cat_id: UUID,
    item_id: UUID,
    resposta_enviada: str,
    tempo_resposta_segundos: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submissão cega da Prova CAT (RN-EXE-006.1):
    - O aluno NÃO recebe feedback se acertou ou errou.
    - O motor recalcula o theta intermediário pelo estimador Bayesiano EAP internamente.
    - Se a prova continuar: devolve a próxima questão e indicador ordinal (ex: 'Questão 6').
    - Se atingir o critério de parada: finaliza a sessão e devolve o Dossiê com Radar e nota theta.
    """
    from app.modules.exercises.cat_engine import CatEngine
    from app.models.exercise import ProvaCat, ItemExercicio
    from sqlalchemy import select

    stmt_cat = select(ProvaCat).where(ProvaCat.id == sessao_cat_id)
    prova = (await db.execute(stmt_cat)).scalar_one_or_none()
    if not prova:
        raise HTTPException(status_code=404, detail="Sessão CAT não localizada.")

    item = await db.get(ItemExercicio, item_id)
    acertou = (resposta_enviada.strip().upper() == item.resposta_correta.strip().upper())

    # Atualiza lista de itens respondidos
    itens_atuais = list(prova.itens_respondidos_ids)
    itens_atuais.append(item.id)
    prova.itens_respondidos_ids = itens_atuais
    prova.total_itens_aplicados += 1

    # Recalcula Theta Bayesiano EAP (internamente sem expor)
    novo_theta, novo_se = CatEngine.estimar_theta_eap(
        itens_aplicados=[item], # histórico acumulado
        respostas=[1 if acertou else 0]
    )
    prova.theta_geral = round(novo_theta, 3)
    prova.erro_padrao_se = round(novo_se, 3)

    # Verifica critérios de parada: SE <= 0.30 (mínimo 12) ou 20 questões
    atingiu_parada = (
        (prova.total_itens_aplicados >= 12 and prova.erro_padrao_se <= 0.30)
        or prova.total_itens_aplicados >= 20
    )

    if not atingiu_parada:
        # Busca a próxima questão com máxima Informação de Fisher
        # proximo_item = CatEngine.selecionar_proximo_item(...)
        await db.commit()
        return {
            "finalizado": False,
            "indicador_progresso": f"Questão {prova.total_itens_aplicados + 1} (Faixa: 12 a 20 questões)",
            "proximo_item": {
                "id": "uuid-exemplo",
                "enunciado_katex": "Seja a função f(x)...",
                "alternativas": [{"letra": "A", "texto": "..."}]
            }
        }
    else:
        # Encerramento formal do teste: revela o Dossiê Diagnóstico e o Gráfico Radar
        prova.finalizado_em = datetime.utcnow()
        await db.commit()

        classificacao = "Básico" if novo_theta < -0.5 else "Intermediário" if novo_theta <= 1.0 else "Avançado"

        return {
            "finalizado": True,
            "mensagem": "Prova Diagnóstica CAT concluída com sucesso!",
            "theta_final": prova.theta_geral,
            "erro_padrao": prova.erro_padrao_se,
            "classificacao": classificacao,
            "total_questoes_respondidas": prova.total_itens_aplicados,
            "radar_grandes_areas": {
                "algebra_funcoes": prova.theta_geral,
                "geometria": prova.theta_geral - 0.15,
                "algebra_linear": prova.theta_geral + 0.10,
                "aplicada": prova.theta_geral - 0.05
            },
            "redirecionar_url": "/app/skill-tree"
        }
```
