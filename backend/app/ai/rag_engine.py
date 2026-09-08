"""
Motor RAG com pgvector (768 Dimensões) e Índice HNSW.
Conforme especificação em docs-site/docs/modules/conteudo/prototype/rag-engine.md
e docs-site/docs/implementation/etapa-06-ia-rag.md.
"""
from typing import List, Optional
from uuid import UUID
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.ai.llm_factory import LLMFactory
from app.schemas.content import ChunkRAGResponse

logger = logging.getLogger("app.ai.rag_engine")


class RAGEngine:
    """Motor de busca semântica em sub-5ms sobre os livros da coleção Iezzi via pgvector."""

    @staticmethod
    async def buscar_trechos_relevantes(
        db: AsyncSession,
        volume_id: UUID,
        query_aluno: str,
        limite_chunks: int = 3,
        threshold_similaridade: float = 0.40,
    ) -> List[ChunkRAGResponse]:
        """
        Converte a dúvida do aluno em vetor denso (768d) e executa busca
        vetorial particionada estritamente pelo volume ativo no PostgreSQL.
        """
        try:
            # 1. Gera o vetor da query via LLMFactory ativa (task_type de consulta)
            provedor = LLMFactory.obter_provedor()
            vetor_query = await provedor.gerar_embedding(query_aluno, task_type="retrieval_query")
        except Exception as e:
            logger.warning(f"Falha ao gerar embedding para busca RAG: {e}")
            return []

        try:
            # Formata vetor float como string para casting do pgvector [v1, v2, ...]
            vetor_str = "[" + ",".join(str(f) for f in vetor_query) + "]"

            # 2. Query SQL com operador de distância cosseno (<=>) do pgvector
            # Similaridade cosseno: 1 - (embedding <=> vetor_query)
            sql_query = text("""
                SELECT 
                    trecho_conteudo,
                    metadados->>'pagina' as pagina,
                    metadados->>'teorema' as teorema,
                    1 - (embedding <=> CAST(:vetor_param AS vector)) as similaridade
                FROM documentos_vetoriais_rag
                WHERE volume_id = :volume_id
                  AND (1 - (embedding <=> CAST(:vetor_param AS vector))) >= :threshold
                ORDER BY embedding <=> CAST(:vetor_param AS vector) ASC
                LIMIT :limite;
            """)

            result = await db.execute(
                sql_query,
                {
                    "volume_id": volume_id,
                    "vetor_param": vetor_str,
                    "threshold": threshold_similaridade,
                    "limite": limite_chunks,
                },
            )

            chunks: List[ChunkRAGResponse] = []
            for row in result.mappings():
                pagina_val = row["pagina"]
                chunks.append(
                    ChunkRAGResponse(
                        trecho=row["trecho_conteudo"],
                        pagina=int(pagina_val) if (pagina_val and str(pagina_val).isdigit()) else None,
                        teorema_ou_topico=row["teorema"] or "Fundamentos de Matemática Elementar",
                        score_similaridade=round(float(row["similaridade"]), 3),
                    )
                )

            return chunks
        except Exception as e:
            logger.error(f"Erro ao consultar documentos_vetoriais_rag no pgvector: {e}")
            return []
