---
title: Tabela 13 - caixa_reforco
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/exercicios/business-rules/regras-pratica.md
  - modules/progresso/business-rules/regras-recomendacoes.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 13: `caixa_reforco`

Armazena os itens nos quais o estudante cometeu **erro duplo** (esgotou as duas tentativas na aula), alimentando as baterias de reforço dinâmico e o Hub de Ação dos Top 3 tópicos críticos.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE caixa_reforco (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES itens_exercicios(id) ON DELETE CASCADE,
    capitulo_id UUID NOT NULL REFERENCES capitulos(id),
    total_erros INT NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',            -- 'pendente' | 'superado'
    arquivado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    superado_em TIMESTAMPTZ
);

CREATE INDEX idx_caixa_reforco_pendente 
ON caixa_reforco(usuario_id, status);

CREATE INDEX idx_caixa_reforco_capitulo 
ON caixa_reforco(usuario_id, capitulo_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Aluno com dificuldade no item |
| `item_id` | UUID | Não | Questão em que ocorreu erro duplo | Item matriz ou gêmeo |
| `total_erros` | INT | Não | Contador cumulativo de erros neste tópico | Severidade da lacuna |
| `status` | VARCHAR(20) | Não | Estado pedagógico (`pendente` ou `superado`) | RN-EXE-008.1 |
| `superado_em` | TIMESTAMPTZ | Sim | Data em que acertou uma Questão Gêmea equivalente | Resolução da pendência |
