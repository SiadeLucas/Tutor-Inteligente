---
title: Tabela 16 - historico_theta
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/progresso/business-rules/regras-calibragem.md
last_updated: "2026-09-10"
updated_by: buffy
---

# Tabela 16: `historico_theta`

Série temporal contínua da evolução psicométrica do estudante ($\theta$) ao longo de toda a sua jornada, isolada por disciplina e volume.

> [!IMPORTANT]
> **Valores canônicos de `grande_area`:** os 4 slugs das Grandes Áreas
> (`algebra_funcoes`, `geometria`, `algebra_linear`, `aplicada`) **mais** o agregado
> **`'geral'`** (theta global da prova CAT). O valor `'geral'` é gravado pela migração
> `005_progress_tables` (backfill de `provas_cat` concluídas), por
> `ExercisesService._registrar_historico_cat` e consumido como fonte primária de leitura
> do theta geral em `GET /api/v1/progresso/geral`.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE historico_theta (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    disciplina_id UUID NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    volume_id UUID REFERENCES volumes_didaticos(id) ON DELETE SET NULL,
    grande_area VARCHAR(50) NOT NULL,                          -- Macro-área associada
    theta_estimado DECIMAL(6, 3) NOT NULL,                     -- Escala contínua de -3.000 a +3.000
    erro_padrao_se DECIMAL(6, 3) NOT NULL,                     -- Erro padrão de mensuração
    origem_ajuste VARCHAR(40) NOT NULL,                        -- 'onboarding_cat' | 'marco_cat' | 'micro_ajuste_exercicio'
    registrado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_historico_theta_usuario_disciplina 
ON historico_theta(usuario_id, disciplina_id, registrado_em);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador do registro | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Estudante |
| `disciplina_id` | UUID | Não | Chave estrangeira para `disciplinas(id)` | Isolamento por matéria |
| `volume_id` | UUID | Sim | Volume associado (se micro-ajuste de aula) | Nullable |
| `theta_estimado` | DECIMAL(6,3) | Não | Valor de proficiência estimado | Escala de -3.0 a +3.0 |
| `erro_padrao_se` | DECIMAL(6,3) | Não | Erro padrão da estimativa Bayesiana | Confiabilidade |
| `grande_area` | VARCHAR(50) | Não | Macro-área do registro | 4 slugs canônicos + agregado `'geral'` |
| `origem_ajuste` | VARCHAR(40) | Não | Fonte do ajuste no theta (`onboarding_cat` \| `marco_cat` \| `micro_ajuste_exercicio`) | RN-PRG-006 |
