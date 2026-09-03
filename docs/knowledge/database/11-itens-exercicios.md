---
title: Tabela 11 - itens_exercicios
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/exercicios/business-rules/regras-cat.md
  - modules/exercicios/business-rules/regras-validacao.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 11: `itens_exercicios`

Banco de itens avaliativos calibrados pela **Teoria da Resposta ao Item (TRI)**, contendo tanto questões originais da coleção Iezzi quanto Questões Gêmeas geradas por IA e validadas deterministicamente pelo SymPy.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE itens_exercicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    capitulo_id UUID NOT NULL REFERENCES capitulos(id) ON DELETE CASCADE,
    tipo_origem VARCHAR(30) NOT NULL DEFAULT 'iezzi_original', -- 'iezzi_original' | 'gemea_ia'
    item_matriz_id UUID REFERENCES itens_exercicios(id),       -- Aponta para o item matriz se for gêmea
    enunciado_katex TEXT NOT NULL,                             -- Enunciado formatado em KaTeX
    alternativas JSONB NOT NULL,                               -- [{"letra": "A", "texto": "...", "correta": false}, ...]
    resposta_correta VARCHAR(5) NOT NULL,                      -- 'A' | 'B' | 'C' | 'D' | 'E'
    resolucao_passo_a_passo TEXT NOT NULL,                     -- Resolução em etapas lógicas KaTeX
    parametro_a DECIMAL(6, 3) NOT NULL DEFAULT 1.000,          -- Discriminação da TRI (típico: 0.5 a 2.5)
    parametro_b DECIMAL(6, 3) NOT NULL DEFAULT 0.000,          -- Dificuldade da TRI (escala -3.0 a +3.0)
    parametro_c DECIMAL(6, 3) NOT NULL DEFAULT 0.200,          -- Acerto casual (20% para 5 alternativas)
    metadados_sympy JSONB,                                     -- Expressão simbólica formal para validação
    validado_sympy BOOLEAN NOT NULL DEFAULT TRUE,              -- Atestado de convergência determinística (±0.01)
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_itens_capitulo ON itens_exercicios(capitulo_id, ativo);
CREATE INDEX idx_itens_matriz ON itens_exercicios(item_matriz_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário do item | UUID v4 |
| `capitulo_id` | UUID | Não | Chave estrangeira para `capitulos(id)` | Tópico curricular avaliado |
| `tipo_origem` | VARCHAR(30) | Não | Origem do item (`iezzi_original` ou `gemea_ia`) | Rastreabilidade pedagógica |
| `enunciado_katex` | TEXT | Não | Texto e expressões da questão | Fórmulas delimitadas por $...$ |
| `alternativas` | JSONB | Não | Vetor com as 5 alternativas | RN-EXE-001 |
| `parametro_a` | DECIMAL(6,3) | Não | Discriminação do item na TRI | Curva característica do item |
| `parametro_b` | DECIMAL(6,3) | Não | Dificuldade intrínseca na TRI | Escala contínua de -3 a +3 |
| `parametro_c` | DECIMAL(6,3) | Não | Probabilidade de acerto ao acaso | Padrão 0.200 (1 em 5) |
| `validado_sympy` | BOOLEAN | Não | Flag de validação determinística | RN-EXE-013 (tolerância ±0.01) |
