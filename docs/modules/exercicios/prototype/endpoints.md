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
    # await db.commit()
    
    return nova_questao
```
