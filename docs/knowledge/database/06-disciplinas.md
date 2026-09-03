---
title: Tabela 06 - disciplinas
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/onboarding/business-rules/escalabilidade.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 06: `disciplinas`

Tabela mestre que viabiliza a **escalabilidade nativa para qualquer matéria** (Matemática, Física, Química, etc.) e múltiplos níveis de ensino (Ensino Médio, Fundamental, Superior).

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE disciplinas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(50) UNIQUE NOT NULL,             -- 'matematica' | 'fisica' | 'quimica'
    nome VARCHAR(100) NOT NULL,                   -- 'Matemática'
    nivel_ensino VARCHAR(50) NOT NULL,            -- 'ensino_medio' | 'fundamental' | 'superior'
    icone VARCHAR(50) NOT NULL DEFAULT 'school',  -- Nome do ícone Material Symbols
    cor_tema VARCHAR(20) NOT NULL DEFAULT '#F57C00',
    ordem INT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,          -- Apenas 'matematica' ativo no MVP
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_disciplinas_slug ON disciplinas(slug);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador único da disciplina | UUID v4 |
| `slug` | VARCHAR(50) | Não | Identificador amigável em URLs | Único |
| `nome` | VARCHAR(100) | Não | Nome formal exibido na interface | Ex: 'Matemática' |
| `nivel_ensino` | VARCHAR(50) | Não | Grau de escolaridade atendido | RN-ESC-001 |
| `ativo` | BOOLEAN | Não | Flag de disponibilidade na plataforma | **Apenas Matemática ativa no MVP** |
