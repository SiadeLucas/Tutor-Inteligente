---
title: Tabela 17 - horas_estudo_diarias
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/progresso/business-rules/regras-metricas.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 17: `horas_estudo_diarias`

Consolida o **tempo líquido de estudo ativo** por dia, aplicando a regra de pausa automática em inatividades superiores a 3 minutos, alimentando os streaks e o Boletim Escolar em PDF.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE horas_estudo_diarias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data_registro DATE NOT NULL,
    segundos_ativos INT NOT NULL DEFAULT 0,                    -- Tempo líquido ativo (pausa em inatividade > 3min)
    aulas_concluidas INT NOT NULL DEFAULT 0,
    exercicios_submetidos INT NOT NULL DEFAULT 0,
    CONSTRAINT uk_horas_usuario_data UNIQUE (usuario_id, data_registro)
);

CREATE INDEX idx_horas_estudo_usuario 
ON horas_estudo_diarias(usuario_id, data_registro);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Aluno monitorado |
| `data_registro` | DATE | Não | Data do calendário civil (YYYY-MM-DD) | Chave única com usuario_id |
| `segundos_ativos` | INT | Não | Segundos líquidos com interação ativa | **Pausa automática se inativo > 3 min (RN-PRG-003)** |
| `aulas_concluidas` | INT | Não | Total de aulas concluídas neste dia | Contador diário |
| `exercicios_submetidos`| INT | Não | Total de questões respondidas neste dia | Contador diário |
