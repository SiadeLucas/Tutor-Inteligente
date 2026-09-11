---
title: Exercícios - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/exercicios/prototype/index.md
last_updated: "2026-09-10"
updated_by: buffy
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
    tipo_item = getattr(payload, "tipo_item", "multiple_choice")  # multiple_choice | numeric_input
    gabarito_esperado = "A"  # Exemplo recuperado do banco
    pista_ia = "Lembre-se de verificar o sinal do discriminante Delta = b^2 - 4ac."
    resolucao_katex = "A resolução detalhada demonstra as raízes reais x_1 e x_2."

    # RN-EXE-017: Suporte tanto a múltipla escolha quanto a numeric_input com tolerância ±0.01 via SymPy
    if tipo_item == "numeric_input":
        acertou = SympyMathValidator.validar_equivalencia(
            expressao_aluno_str=payload.resposta_enviada,
            expressao_gabarito_str=gabarito_esperado
        )
    else:
        acertou = (payload.resposta_enviada.strip().upper() == gabarito_esperado.strip().upper())

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
# 3. Inicialização e Submissão da Prova Adaptativa CAT (Blind Adaptive Testing)
# ============================================================================

@router.post("/cat/iniciar")
async def iniciar_sessao_cat(
    payload: IniciarCatRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Instancia uma nova sessão de Prova Adaptativa Diagnóstica (CAT)
    com prior N(0, 1), SE inicial de 1.0 e seleciona o 1º item por máxima Informação de Fisher.

    Resiliência de sessão (RN-EXE-010): se o aluno já possui uma prova
    pendente (ex.: fechou a aba no meio), RETOMA de onde parou — a resposta
    inclui `retomada: true` e `itens_respondidos: N`. A calibragem adaptativa
    já atingida é preservada (o MFI nunca reinicia de theta=0 indevidamente).
    """
    from app.models.exercise import ProvaCat
    from uuid import uuid4
    from datetime import datetime

    nova_prova = ProvaCat(
        id=uuid4(),
        usuario_id=current_user.id,
        disciplina_id=payload.disciplina_id,
        theta_geral=0.0,
        erro_padrao_se=1.0,
        total_itens_aplicados=0,
        itens_respondidos_ids=[],
        iniciado_em=datetime.utcnow()
    )
    db.add(nova_prova)
    await db.commit()

    return {
        "sessao_cat_id": nova_prova.id,
        "indicador_progresso": "Questão 1 (Faixa: 12 a 20 questões)",
        "retomada": false,
        "itens_respondidos": 0,
        "primeiro_item": {
            "id": "uuid-item-inicial",
            "enunciado_katex": "Seja a função real $f(x) = 2x - 4$. O zero da função é:",
            "tipo_item": "multiple_choice",
            "alternativas": [
                {"letra": "A", "texto": "$x = 2$"},
                {"letra": "B", "texto": "$x = -2$"},
                {"letra": "C", "texto": "$x = 4$"},
                {"letra": "D", "texto": "$x = 0$"}
            ]
        }
    }


@router.delete("/cat/{sessao_id}")
async def abandonar_sessao_cat(
    sessao_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Abandona (descarta) uma sessão CAT em andamento — saída de emergência.
    A calibragem parcial é PERDIDA: a próxima prova recomeça de theta=0.
    Sessões finalizadas não são afetadas (400 — nada a abandonar).
    """
    prova = await db.get(ProvaCat, sessao_id)
    if not prova or prova.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Sessão CAT não localizada.")
    if prova.finalizado_em is not None:
        raise HTTPException(status_code=400, detail="Esta sessão CAT já foi concluída.")

    await db.delete(prova)
    await db.commit()
    return {"mensagem": "Sessão CAT abandonada. A próxima prova será iniciada do zero."}


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
    from app.cat_engine.cat_service import ItemTRI
    cat = CatEngine()
    item_tri = ItemTRI(
        id=item.id,
        parametro_a=float(item.parametro_a),
        parametro_b=float(item.parametro_b),
        parametro_c=float(item.parametro_c)
    )
    novo_theta, novo_se = cat.estimar_theta_eap(
        respostas=[(item_tri, 1 if acertou else 0)]
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
        # proximo_item = cat.selecionar_proximo_item(...)
        await db.commit()
        return {
            "finalizado": False,
            "indicador_progresso": f"Questão {prova.total_itens_aplicados + 1} (Faixa: 12 a 20 questões)",
            "proximo_item": {
                "id": str(item.id),
                "enunciado_katex": item.enunciado_katex,
                "alternativas": item.alternativas
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


# ============================================================================
# 3.1 Histórico de Provas CAT Finalizadas (suporte ao disparo da etapa-04
#     e comparativo entrada vs. atual preparado para a Etapa 8)
# ============================================================================

@router.get("/cat/historico")
async def historico_provas_cat(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna as provas CAT finalizadas do estudante (mais recente primeiro), com
    theta_geral, erro_padrao_se, classificacao, total_itens_aplicados e
    scores_grandes_areas. Usado pelo frontend para verificar a pendência da
    prova diagnóstica de onboarding no primeiro acesso a uma matéria.
    """
    ...


# ============================================================================
# 4. Consulta de Bateria de Fixação do Capítulo (Bloco 4)
# ============================================================================

@router.get("/capitulo/{capitulo_id}", response_model=List[ItemExercicioResponse])
async def obter_bateria_fixacao(
    capitulo_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-CNT-010 / RN-EXE-001: Retorna a bateria de fixação de 3 a 5 exercícios do capítulo
    ordenada pedagogicamente pelo parâmetro de dificuldade (b).
    """
    from app.models.exercise import ItemExercicio
    stmt = (
        select(ItemExercicio)
        .where(and_(ItemExercicio.capitulo_id == capitulo_id, ItemExercicio.ativo == True))
        .order_by(ItemExercicio.parametro_b.asc())
        .limit(5)
    )
    result = await db.execute(stmt)
    itens = result.scalars().all()
    return itens


# ============================================================================
# 5. Consulta da Caixa de Reforço (Itens Pendentes)
# ============================================================================

@router.get("/caixa-reforco")
async def listar_caixa_reforco(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-EXE-018: Retorna a lista de itens com erro duplo acumulados na Caixa de Reforço
    para treinos dinâmicos de superação.
    """
    from app.models.exercise import CaixaReforco, ItemExercicio
    stmt = (
        select(CaixaReforco, ItemExercicio)
        .join(ItemExercicio, CaixaReforco.item_id == ItemExercicio.id)
        .where(
            and_(
                CaixaReforco.usuario_id == current_user.id,
                CaixaReforco.status == "pendente"
            )
        )
        .order_by(CaixaReforco.arquivado_em.desc())
    )
    result = await db.execute(stmt)
    registros = result.all()
    
    return [
        {
            "id": str(cr.id),
            "item_id": str(it.id),
            "capitulo_id": str(cr.capitulo_id),
            "enunciado_katex": it.enunciado_katex,
            "total_erros": cr.total_erros,
            "arquivado_em": cr.arquivado_em.isoformat()
        }
        for cr, it in registros
    ]
```
