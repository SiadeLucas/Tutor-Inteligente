---
title: Tabela 10 - documentos_vetoriais_rag (pgvector 768d)
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/conteudo/business-rules/agentes-ia.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 10: `documentos_vetoriais_rag` (pgvector 768d)

Hospeda a base de conhecimento vetorial dos **11 Agentes Especialistas de IA**, indexada via extensão oficial `pgvector` do PostgreSQL com vetores densos de **768 dimensões** gerados pelo modelo gratuito **Google `text-embedding-004`**.

---

## 1. DDL SQL (PostgreSQL 16 com `pgvector`)

```sql
-- Ativação da extensão oficial de vetores
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documentos_vetoriais_rag (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    volume_id UUID NOT NULL REFERENCES volumes_didaticos(id) ON DELETE CASCADE,
    capitulo_id UUID REFERENCES capitulos(id) ON DELETE CASCADE,
    trecho_conteudo TEXT NOT NULL,                 -- Texto do livro, definições e fórmulas
    metadados JSONB NOT NULL DEFAULT '{}',         -- {"pagina": 42, "teorema": "Teorema de Tales"}
    embedding vector(768) NOT NULL,                -- Vetor de 768 dimensões (Google text-embedding-004)
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índice HNSW com distância cosseno para recuperação em sub-5ms
CREATE INDEX idx_rag_embedding_hnsw 
ON documentos_vetoriais_rag 
USING hnsw (embedding vector_cosine_ops);

-- Índice relacional para particionamento estrito por volume
CREATE INDEX idx_rag_volume ON documentos_vetoriais_rag(volume_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador do chunk vetorial | UUID v4 |
| `volume_id` | UUID | Não | Chave estrangeira para `volumes_didaticos(id)` | Particionamento do agente de IA |
| `trecho_conteudo` | TEXT | Não | Fragmento de 300 a 800 tokens do livro | Textos e fórmulas em KaTeX |
| `metadados` | JSONB | Não | Dicionário estruturado de autoria/página | Para citações no chat |
| `embedding` | `vector(768)` | Não | Vetor denso de 768 dimensões | **Google text-embedding-004 (Gratuito)** |

---

## 3. Justificativa Arquitetural das 768 Dimensões

> [!TIP]
> **Eficiência de Memória e Custo Zero no MVP**:
> - O uso de `vector(768)` permite consumir a cota gratuita da API de embeddings do Google AI Studio.
> - Vetores de 768 dimensões ocupam **50% menos memória RAM e armazenamento** que vetores de 1536 dimensões, permitindo que o índice HNSW caiba integralmente no cache da instância EC2 de entrada da AWS.
> - Caso o cliente deseje migrar para OpenAI (1536d) no futuro comercial, a reindexação dos 11 volumes leva apenas 2 minutos via script automatizado.
