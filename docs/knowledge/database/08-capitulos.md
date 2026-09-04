---
title: Tabela 08 - capitulos
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/conteudo/business-rules/pedagogia-aulas.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 08: `capitulos`

Estrutura os capítulos de conteúdo didático dimensionados pedagogicamente para **sessões de estudo de 50 minutos**, contendo o grafo de pré-requisitos recomendados.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE capitulos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    volume_id UUID NOT NULL REFERENCES volumes_didaticos(id) ON DELETE CASCADE,
    numero_capitulo INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,                  -- Ex: 'Função Quadrática e Parábola'
    tempo_estimado_min INT NOT NULL DEFAULT 50,    -- 50 minutos (RN-CNT-010)
    preco_avulso DECIMAL(10, 2) NOT NULL DEFAULT 9.90,
    pre_requisitos_ids UUID[] DEFAULT '{}',        -- Array com IDs de capítulos recomendados
    ordem INT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_capitulos_volume ON capitulos(volume_id, ordem);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador do capítulo | UUID v4 |
| `volume_id` | UUID | Não | Chave estrangeira para `volumes_didaticos(id)` | Volume ao qual pertence |
| `titulo` | VARCHAR(200) | Não | Tema central da sessão | Ex: 'Progressões Aritméticas' |
| `tempo_estimado_min` | INT | Não | Duração pedagógica recomendada | Fixo em 50 minutos (RN-CNT-010) |
| `preco_avulso` | DECIMAL(10,2) | Não | Valor avulso de venda do capítulo | R$ 9,90 (RN-PAG-001) |
| `pre_requisitos_ids` | UUID[] | Sim | Array de IDs de capítulos recomendados | Alerta pedagógico flexível |
