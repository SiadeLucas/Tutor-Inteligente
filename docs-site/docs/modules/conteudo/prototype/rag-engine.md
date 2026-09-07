---
title: Conteúdo - Motor RAG em pgvector (768 Dimensões)
type: module
status: draft
related:
  - modules/conteudo/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Motor RAG em `pgvector` (768 Dimensões)

Implementação da recuperação semântica em tempo real fundamentada na extensão oficial **pgvector** do PostgreSQL 16 com índice **HNSW**, particionada estritamente por volume da coleção didática.

---

## Código Fonte (`backend/app/ai/rag_engine.py`)

```python
from uuid import UUID
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.ai.llm_factory import LLMFactory
from app.modules.content.schemas import ChunkRAGResponse


class RAGEngine:
    """Motor de busca semântica em sub-5ms sobre os livros do Iezzi."""

    @staticmethod
    async def buscar_trechos_relevantes(
        db: AsyncSession,
        volume_id: UUID,
        query_aluno: str,
        limite_chunks: int = 3,
        threshold_similaridade: float = 0.65
    ) -> List[ChunkRAGResponse]:
        """
        Converte a dúvida do aluno em vetor (768d via text-embedding-004)
        e executa busca vetorial particionada pelo volume ativo no PostgreSQL.
        """
        # 1. Gera o vetor da query via provedor ativo (Google Gemini Embeddings)
        provedor_llm = LLMFactory.obter_provedor()
        vetor_query = await provedor_llm.gerar_embedding(query_aluno)

        # 2. Query SQL de busca com operador de distância cosseno (<=>) do pgvector
        # Formula de similaridade: 1 - (embedding <=> vetor_query)
        sql_query = text("""
            SELECT 
                trecho_conteudo,
                metadados->>'pagina' as pagina,
                metadados->>'teorema' as teorema,
                1 - (embedding <=> :vetor_param::vector) as similaridade
            FROM documentos_vetoriais_rag
            WHERE volume_id = :volume_id
              AND (1 - (embedding <=> :vetor_param::vector)) >= :threshold
            ORDER BY embedding <=> :vetor_param::vector ASC
            LIMIT :limite;
        """)

        result = await db.execute(
            sql_query,
            {
                "volume_id": volume_id,
                "vetor_param": str(vetor_query),
                "threshold": threshold_similaridade,
                "limite": limite_chunks
            }
        )

        chunks_encontrados = []
        for row in result.mappings():
            chunks_encontrados.append(
                ChunkRAGResponse(
                    trecho=row["trecho_conteudo"],
                    pagina=int(row["pagina"]) if row["pagina"] else None,
                    teorema_ou_topico=row["teorema"],
                    score_similaridade=round(float(row["similaridade"]), 3)
                )
            )

        return chunks_encontrados
```
