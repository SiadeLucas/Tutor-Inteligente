---
title: Tabela 12 - tentativas_exercicios
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/exercicios/business-rules/regras-pratica.md
  - modules/progresso/business-rules/regras-metricas.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 12: `tentativas_exercicios`

Registra todas as respostas submetidas pelos estudantes, viabilizando o cálculo da **pontuação ponderada** (1.0 na 1ª tentativa vs 0.5 na 2ª com auxílio de IA) e alimentando os micro-ajustes psicométricos.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE tentativas_exercicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES itens_exercicios(id) ON DELETE CASCADE,
    capitulo_id UUID NOT NULL REFERENCES capitulos(id),
    tentativa_numero INT NOT NULL,                             -- 1 ou 2
    resposta_enviada VARCHAR(5) NOT NULL,                      -- 'A' | 'B' | 'C' | 'D' | 'E'
    acertou BOOLEAN NOT NULL,
    pontuacao_obtida DECIMAL(3, 1) NOT NULL,                   -- 1.0 (1ª tent) | 0.5 (2ª tent com dica) | 0.0 (erro)
    usou_dica_ia BOOLEAN NOT NULL DEFAULT FALSE,
    tempo_resposta_segundos INT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tentativas_usuario_capitulo 
ON tentativas_exercicios(usuario_id, capitulo_id);

CREATE INDEX idx_tentativas_item 
ON tentativas_exercicios(item_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador da tentativa | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Aluno respondente |
| `item_id` | UUID | Não | Chave estrangeira para `itens_exercicios(id)` | Questão submetida |
| `tentativa_numero` | INT | Não | Número da tentativa (1 ou 2) | RN-EXE-008 |
| `acertou` | BOOLEAN | Não | Flag indicando se acertou o gabarito | Booleano |
| `pontuacao_obtida` | DECIMAL(3,1) | Não | Pontos atribuídos para a média ponderada | **1.0 (1ª) / 0.5 (2ª) / 0.0 (erro)** |
| `usou_dica_ia` | BOOLEAN | Não | Flag se acionou a dica socrática | Estatística de autonomia |
| `tempo_resposta_segundos` | INT | Não | Duração da resolução em segundos | Indicador de fluência |
