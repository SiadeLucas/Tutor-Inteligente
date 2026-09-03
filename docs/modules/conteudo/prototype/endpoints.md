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

    # 2. Busca trechos no RAG particionados pelo volume_id
    chunks = await RAGEngine.buscar_trechos_relevantes(
        db=db,
        volume_id=volume.id,
        query_aluno=payload.mensagem,
        limite_chunks=3
    )

    trechos_formatados = "\n\n".join([f"Página {c.pagina}: {c.trecho}" for c in chunks])
    if not trechos_formatados:
        trechos_formatados = f"Conceitos gerais do Volume {volume.numero_volume}: {volume.titulo}."

    # 3. Determina o estágio socrático com base no tamanho do histórico recente
    total_mensagens = len(payload.historico_recente)
    estagio_ajuda = 1 if total_mensagens <= 2 else (2 if total_mensagens <= 4 else 3)

    # 4. Constrói a instrução de sistema
    system_instruction = SYSTEM_PROMPT_SOCRATICO.format(
        numero_volume=volume.numero_volume,
        titulo_volume=volume.titulo,
        trechos_rag=trechos_formatados,
        estagio_ajuda=estagio_ajuda
    )

    # 5. Chama o provedor de IA via Fábrica (Gemini Flash gratuito no MVP)
    provedor_llm = LLMFactory.obter_provedor()
    historico_dicts = [{"papel": m.papel, "conteudo": m.conteudo} for m in payload.historico_recente]

    resposta_texto = await provedor_llm.gerar_resposta(
        prompt_usuario=payload.mensagem,
        system_instruction=system_instruction,
        historico_dialogo=historico_dicts,
        temperatura=0.2
    )

    return ChatAulaResponse(
        resposta_katex=resposta_texto,
        chunks_utilizados=chunks,
        nivel_ajuda_socratico=estagio_ajuda
    )
```
