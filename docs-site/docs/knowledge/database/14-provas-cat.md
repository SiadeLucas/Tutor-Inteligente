---
title: Tabela 14 - provas_cat
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/exercicios/business-rules/regras-cat.md
  - modules/onboarding/business-rules/proficiencia.md
last_updated: "2026-09-09"
updated_by: antigravity
---

# Tabela 14: `provas_cat`

Registra as sessões formais de **Teste Adaptativo Computadorizado (CAT)**, tanto no Onboarding Diagnóstico quanto nos marcos periódicos de recalibragem psicométrica de 7 dias, isoladas por disciplina.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE provas_cat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    disciplina_id UUID NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    tipo_prova VARCHAR(30) NOT NULL,                           -- 'onboarding_diagnostico' | 'marco_periodico'
    theta_geral DECIMAL(6, 3) NOT NULL,                        -- Theta convergido ao final do teste
    erro_padrao_se DECIMAL(6, 3) NOT NULL,                     -- Erro padrão (meta: < 0.30)
    scores_grandes_areas JSONB NOT NULL DEFAULT '{}',          -- {"algebra_funcoes": 0.45, "geometria": -0.20, ...}
    total_itens_aplicados INT NOT NULL DEFAULT 0,              -- Limite entre 12 e 20 itens
    itens_respondidos_ids JSONB NOT NULL DEFAULT '[]',         -- Lista de IDs dos itens aplicados
    respostas_detalhadas JSONB NOT NULL DEFAULT '[]',          -- Histórico completo para estimativa EAP Bayesiana
    iniciado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finalizado_em TIMESTAMPTZ
);


CREATE INDEX idx_provas_cat_usuario_disciplina 
ON provas_cat(usuario_id, disciplina_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador da sessão CAT | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Estudante avaliado |
| `disciplina_id` | UUID | Não | Chave estrangeira para `disciplinas(id)` | Isolamento por matéria |
| `tipo_prova` | VARCHAR(30) | Não | Finalidade do teste | `onboarding_diagnostico` ou `marco_periodico` |
| `theta_geral` | DECIMAL(6,3) | Não | Escore final da proficiência do aluno | Escala contínua de -3 a +3 |
| `erro_padrao_se` | DECIMAL(6,3) | Não | Erro de mensuração Bayesiano EAP | Critério de parada SE < 0.30 |
| `scores_grandes_areas` | JSONB | Não | Vetor de escores para o Gráfico Radar | Polígono do diagnóstico inicial |
| `total_itens_aplicados` | INT | Não | Quantidade de questões resolvidas | Mínimo 12, máximo 20 |
