---
title: Conteúdo - Schemas e DTOs de IA
type: module
status: draft
related:
  - modules/conteudo/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs de IA (Pydantic v2 & TypeScript)

Contratos tipados para o chat socrático lateral da aula, recuperação de chunks via RAG e solicitação de pistas graduais.

---

## 1. Modelos Backend em Python (`app/modules/content/schemas.py`)

```python
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# 1. Mensagens e Conversação Socrática
# ============================================================================

class MensagemChat(BaseModel):
    papel: Literal["user", "assistant", "system"]
    conteudo: str = Field(..., description="Texto da mensagem com fórmulas KaTeX delimitadas por $...$ ou $$...$$")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatAulaRequest(BaseModel):
    capitulo_id: UUID = Field(..., description="ID do capítulo atual para ancorar a busca semântica")
    mensagem: str = Field(..., min_length=2, max_length=1000, description="Dúvida ou questionamento do estudante")
    trecho_selecionado: Optional[str] = Field(
        default=None, 
        description="Fórmula ou trecho LaTeX selecionado pelo aluno na tela para 'Explicar este passo' (RN-CNT-014)"
    )
    historico_recente: List[MensagemChat] = Field(
        default=[], 
        max_length=6, 
        description="Últimas mensagens trocadas na sessão para manter o contexto conversacional"
    )


class ChunkRAGResponse(BaseModel):
    trecho: str = Field(..., description="Fragmento textual do livro do Iezzi")
    pagina: Optional[int] = None
    teorema_ou_topico: Optional[str] = None
    score_similaridade: float = Field(..., description="Similaridade cosseno (0.0 a 1.0)")


class ChatAulaResponse(BaseModel):
    resposta_katex: str = Field(..., description="Resposta pedagógica do tutor socrático formatada em KaTeX")
    chunks_utilizados: List[ChunkRAGResponse] = Field(default=[])
    nivel_ajuda_socratico: Literal[1, 2, 3] = Field(
        ..., 
        description="1: Pergunta reflexiva | 2: Dica conceitual | 3: Passo guiado"
    )


# ============================================================================
# 2. Pistas Rápidas para Exercícios (2ª Chance)
# ============================================================================

class SolicitarPistaRequest(BaseModel):
    item_id: UUID
    resposta_incorreta_enviada: str = Field(..., description="Alternativa assinalada pelo aluno na 1ª tentativa")


class SolicitarPistaResponse(BaseModel):
    pista_socratica_katex: str
    dica_pegadinha: Optional[str] = None
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/chat.ts`)

```typescript
export interface Mensagem {
  papel: "user" | "assistant" | "system";
  conteudo: string;
  timestamp?: string;
}

export interface ChatAulaRequest {
  capitulo_id: string;
  mensagem: string;
  trecho_selecionado?: string;
  historico_recente?: Mensagem[];
}

export interface ChatAulaResponse {
  resposta_katex: string;
  chunks_utilizados: Array<{
    trecho: string;
    pagina?: number;
    score_similaridade: number;
  }>;
  nivel_ajuda_socratico: 1 | 2 | 3;
}

export interface SolicitarPistaRequest {
  item_id: string;
  resposta_incorreta_enviada: string;
}

export interface SolicitarPistaResponse {
  pista_socratica_katex: string;
  dica_pegadinha?: string;
}
```
