---
title: Tabela 15 - heatmap_dominio
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/progresso/business-rules/regras-heatmap.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 15: `heatmap_dominio`

Consolida o estado visual dos nós do **Heatmap de Domínio** por estudante e capítulo, mantendo as taxas ponderadas de acerto e o status da conclusão da aula.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE heatmap_dominio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    capitulo_id UUID NOT NULL REFERENCES capitulos(id) ON DELETE CASCADE,
    total_questoes_respondidas INT NOT NULL DEFAULT 0,
    taxa_acertos_ponderada DECIMAL(5, 2) NOT NULL DEFAULT 0.00,-- 0.00% a 100.00%
    status_cor VARCHAR(20) NOT NULL DEFAULT 'cinza',            -- 'cinza' | 'vermelho' | 'amarelo' | 'verde'
    aula_concluida BOOLEAN NOT NULL DEFAULT FALSE,              -- True se entregou a bateria de fixação
    ultima_interacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uk_heatmap_usuario_capitulo UNIQUE (usuario_id, capitulo_id)
);

CREATE INDEX idx_heatmap_usuario ON heatmap_dominio(usuario_id);
CREATE INDEX idx_heatmap_usuario_cor ON heatmap_dominio(usuario_id, status_cor);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador do registro | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Estudante |
| `capitulo_id` | UUID | Não | Chave estrangeira para `capitulos(id)` | Capítulo avaliado |
| `taxa_acertos_ponderada`| DECIMAL(5,2) | Não | Pontuação ponderada somada / Total itens | RN-PRG-002 |
| `status_cor` | VARCHAR(20) | Não | Cor renderizada no nó do Heatmap | **Cinza (<3 itens), Vermelho (<50%), Amarelo (<75%), Verde (>=75%)** (RN-PRG-012) |
| `aula_concluida` | BOOLEAN | Não | Conclusão condicionada à entrega da bateria (aproveitamento >= 60%) | RN-CNT-010 / RN-PRG-001 |

