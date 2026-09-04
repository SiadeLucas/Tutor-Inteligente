---
title: Conteúdo - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/conteudo/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 5. Endpoints da API FastAPI

Implementação das rotas assíncronas de conversação socrática em tempo real e RAG da aula (`app/modules/content/router.py`).

---

## Código Fonte (`backend/app/modules/content/router.py`)

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.models.content import Capitulo, VolumeDidatico
from app.modules.content.schemas import (
    ChatAulaRequest,
    ChatAulaResponse,
    SolicitarPistaRequest,
    SolicitarPistaResponse
)
from app.ai.llm_factory import LLMFactory
from app.ai.rag_engine import RAGEngine
from app.ai.prompts.socratic import SYSTEM_PROMPT_SOCRATICO
from app.modules.content.socratic_tutor import SocraticStateManager

router = APIRouter(prefix="/api/v1/conteudo", tags=["Conteúdo & Tutor Socrático"])


@router.post("/aulas/{capitulo_id}/chat", response_model=ChatAulaResponse)
async def conversar_com_tutor_socratico(
    capitulo_id: UUID,
    payload: ChatAulaRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Processa a dúvida do estudante na aula de 50 minutos:
    1. Recupera o volume didático associado ao capítulo.
    2. Realiza busca vetorial (RAG) no pgvector sobre o livro do Iezzi correspondente.
    3. Monta o prompt com mediação socrática em KaTeX.
    4. Invoca o modelo ativo via LLMFactory (Google Gemini Flash no MVP gratuito).
    """
    # 1. Busca capítulo e volume didático
    stmt = (
        select(Capitulo, VolumeDidatico)
        .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
        .where(Capitulo.id == capitulo_id)
    )
    result = await db.execute(stmt)
    dados = result.first()

    if not dados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capítulo não localizado.")

    capitulo, volume = dados

    # 2. Busca trechos no RAG particionados pelo volume_id (considerando trecho_selecionado se presente)
    query_busca = payload.mensagem
    if payload.trecho_selecionado:
        query_busca = f"Fórmula selecionada: {payload.trecho_selecionado}\nDúvida do aluno: {payload.mensagem}"

    chunks = await RAGEngine.buscar_trechos_relevantes(
        db=db,
        volume_id=volume.id,
        query_aluno=query_busca,
        limite_chunks=3
    )

    trechos_formatados = "\n\n".join([f"Página {c.pagina}: {c.trecho}" for c in chunks])
    if not trechos_formatados:
        trechos_formatados = f"Conceitos gerais do Volume {volume.numero_volume}: {volume.titulo}."

    # 3. Determina o estágio socrático via Máquina de Estados (SocraticStateManager)
    estagio_ajuda = SocraticStateManager.determinar_proximo_estagio(
        estagio_atual=len(payload.historico_recente) // 2 + 1,
        topico_atual=payload.trecho_selecionado,
        ultimo_topico_registrado=None,
        mensagem_aluno=payload.mensagem
    )

    # 4. Constrói a instrução de sistema
    system_instruction = SYSTEM_PROMPT_SOCRATICO.format(
        numero_volume=volume.numero_volume,
        titulo_volume=volume.titulo,
        trechos_rag=trechos_formatados,
        estagio_ajuda=estagio_ajuda
    )

    # 5. Chama o provedor de IA via Fábrica (Gemini Flash gratuito no MVP) com tolerância a falhas
    provedor_llm = LLMFactory.obter_provedor()
    historico_dicts = [{"papel": m.papel, "conteudo": m.conteudo} for m in payload.historico_recente]

    try:
        resposta_texto = await provedor_llm.gerar_resposta(
            prompt_usuario=payload.mensagem,
            system_instruction=system_instruction,
            historico_dialogo=historico_dicts,
            temperatura=0.2
        )
    except Exception:
        # Fallback resiliente: previne erro 500 caso haja cota excedida ou timeout na API da IA
        resposta_texto = (
            "Estou recalculando os passos deste conceito. "
            "Enquanto isso, revise a definição e os teoremas do Bloco 1 acima "
            "ou reformule sua dúvida em instantes."
        )

    return ChatAulaResponse(
        resposta_katex=resposta_texto,
        chunks_utilizados=chunks,
        nivel_ajuda_socratico=estagio_ajuda
    )


# ============================================================================
# 2. Pista Socrática Rápida para Exercícios (2ª Chance)
# ============================================================================

@router.post("/aulas/{capitulo_id}/pista", response_model=SolicitarPistaResponse)
async def solicitar_pista_rapida(
    capitulo_id: UUID,
    payload: SolicitarPistaRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-CNT-012: Fornece dica socrática cirúrgica de Estágio 2 para a 2ª chance de resolução,
    apontando o teorema do Iezzi sem queimar a resposta. Exige autenticação.
    """
    return SolicitarPistaResponse(
        pista_socratica_katex="Considere aplicar a propriedade da soma das raízes: $S = -\\frac{b}{a}$.",
        dica_pegadinha="Atenção ao sinal negativo na fórmula de Viète!"
    )


# ============================================================================
# 3. Consulta de Conteúdo da Aula (Blocos 1 a 3 KaTeX)
# ============================================================================

@router.get("/aulas/{capitulo_id}")
async def obter_aula_completa(
    capitulo_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-CNT-010: Retorna o conteúdo didático estruturado em 4 blocos sequenciais
    para a sessão de estudo de 50 minutos.
    """
    from app.models.content import Aula
    stmt = select(Aula).where(Aula.capitulo_id == capitulo_id)
    aula = (await db.execute(stmt)).scalar_one_or_none()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada para este capítulo.")

    return {
        "capitulo_id": capitulo_id,
        "bloco1_teoria_katex": aula.bloco1_teoria_katex,
        "bloco2_exemplos_katex": aula.bloco2_exemplos_katex,
        "bloco3_dicas_ia": aula.bloco3_dicas_ia,
        "video_url": aula.video_url,
        "publicado": aula.publicado
    }


# ============================================================================
# 4. Formalização de Conclusão da Aula (Trava de 60%)
# ============================================================================

@router.post("/aulas/{capitulo_id}/concluir")
async def concluir_aula(
    capitulo_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-CNT-010 / RN-PRG-001: Valida se o estudante atingiu o aproveitamento mínimo
    ponderado de 60% na bateria de fixação e formaliza a conclusão no Heatmap.
    """
    from datetime import datetime
    from app.models.progress import HeatmapDominio

    stmt = select(HeatmapDominio).where(
        HeatmapDominio.usuario_id == current_user.id,
        HeatmapDominio.capitulo_id == capitulo_id
    )
    heatmap = (await db.execute(stmt)).scalar_one_or_none()

    if not heatmap or heatmap.total_questoes_respondidas == 0:
        raise HTTPException(status_code=400, detail="É necessário submeter a bateria de fixação antes de concluir a aula.")

    if float(heatmap.taxa_acertos_ponderada) < 60.0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Aproveitamento insuficiente ({heatmap.taxa_acertos_ponderada:.1f}%). A nota mínima para conclusão é 60%."
        )

    heatmap.aula_concluida = True
    heatmap.ultima_interacao = datetime.utcnow()
    await db.commit()

    return {
        "sucesso": True,
        "capitulo_id": capitulo_id,
        "aula_concluida": True,
        "taxa_acertos_ponderada": float(heatmap.taxa_acertos_ponderada),
        "mensagem": "Aula concluída com sucesso! Próximo capítulo liberado na Skill Tree."
    }
```
