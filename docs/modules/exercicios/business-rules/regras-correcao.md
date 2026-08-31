---
title: Exercícios - 4. Correção e KaTeX
type: module
status: draft
related:
  - modules/exercicios/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 4. Critérios de Correção, KaTeX e Métricas

### 4.1 Regras de Correção e Formatação

#### RN-EXE-017: Tolerância em Respostas Numéricas
- Para questões do tipo `numeric_input`, a correção aceita valores com tolerância de $\pm 0.01$ para compensar aproximações de arredondamento.
- Expressões exatas fracionárias (ex: `3/4`) ou radicais simplificados devem ser suportados pelo parser de entrada.

#### RN-EXE-018: Renderização Rigorosa com KaTeX
- Todos os enunciados, fórmulas de alternativas e resoluções devem ser formatados em LaTeX padronizado e renderizados via KaTeX client-side sem quebra de diagramação.

#### RN-EXE-019: Registro de Fluência Temporal
- O tempo gasto em segundos em cada questão é registrado em segundo plano para compor a métrica de fluência e agilidade no Painel do Professor, sem gerar ansiedade com contadores regressivos punitivos no modo treino.

#### RN-EXE-020: Relatório Analítico Consolidado
- Ao finalizar qualquer avaliação adaptativa ou simulado, a plataforma gera:
  - Nível consolidado por área temática.
  - Gráfico Radar comparativo.
  - Taxa de acerto por sub-tópico.
  - Lista de recomendações imediatas de revisão.
