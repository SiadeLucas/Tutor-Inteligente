---
title: Tabela 07 - volumes_didaticos
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/conteudo/business-rules/mapeamento-volumes.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 07: `volumes_didaticos`

Organiza as coleções de livros ou apostilas associadas a uma disciplina. Na disciplina de Matemática, abriga os **11 volumes canônicos da coleção *Fundamentos de Matemática Elementar* (Gelson Iezzi)**.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE volumes_didaticos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    disciplina_id UUID NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    nome_colecao VARCHAR(150) NOT NULL,           -- 'Fundamentos de Matemática Elementar - Gelson Iezzi'
    numero_volume INT NOT NULL,                   -- 1 a 11
    titulo VARCHAR(150) NOT NULL,                 -- Ex: 'Conjuntos e Funções'
    grande_area VARCHAR(50) NOT NULL,             -- 'algebra_funcoes' | 'geometria' | 'algebra_linear' | 'aplicada'
    ordem_exibicao INT NOT NULL,
    preco_padrao DECIMAL(10, 2) NOT NULL DEFAULT 49.90,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uk_volume_disciplina_numero UNIQUE (disciplina_id, numero_volume)
);

CREATE INDEX idx_volumes_disciplina ON volumes_didaticos(disciplina_id, ordem_exibicao);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador do volume didático | UUID v4 |
| `disciplina_id` | UUID | Não | Chave estrangeira para `disciplinas(id)` | Cascata na exclusão |
| `numero_volume` | INT | Não | Número sequencial (1 a 11) | RN-CNT-001 |
| `titulo` | VARCHAR(150) | Não | Título oficial da obra | Ex: 'Trigonometria' |
| `grande_area` | VARCHAR(50) | Não | Macro-área do conhecimento | Eixos do Radar |
| `preco_padrao` | DECIMAL(10,2) | Não | Valor de tabela do volume avulso | Padrão R$ 49,90 (RN-PAG-001) |
