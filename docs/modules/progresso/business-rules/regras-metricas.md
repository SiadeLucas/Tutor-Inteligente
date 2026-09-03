---
title: Progresso - 1. Métricas Tridimensionais
type: module
status: draft
related:
  - modules/progresso/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 1. Fórmulas de Cálculo e Métricas de Desempenho

### 1.1 Regras de Mensuração

#### RN-PRG-001: Taxa de Completude Curricular
A completude curricular de um volume ou grande área é calculada por:

$$\text{Completude} (\%) = \left( \frac{\text{Aulas Concluídas com Listas de Fixação Entregues}}{\text{Total de Capítulos do Volume}} \right) \times 100$$

> [!IMPORTANT]
> Um capítulo/aula só é contabilizado como concluído quando o aluno confirma a leitura da teoria E submete com sucesso a Bateria de Fixação (3 a 5 exercícios do Iezzi).

#### RN-PRG-002: Taxa de Acerto Ponderada e Precisão na 1ª Tentativa
- **Taxa de Acertos do Capítulo (Heatmap)**: Utiliza pontuação ponderada:
  - Questões acertadas na 1ª tentativa contam peso $1.0$.
  - Questões acertadas na 2ª tentativa (com auxílio da dica socrática) contam peso $0.5$.
  - Erros contam $0.0$.
- **Precisão Bruta (1ª Tentativa)**: Mede o domínio autônomo sem qualquer assistência:

$$\text{Precisão 1ª Tentativa} (\%) = \left( \frac{\text{Questões acertadas na 1ª tentativa}}{\text{Total de Questões Submetidas}} \right) \times 100$$

#### RN-PRG-003: Contabilização de Horas Líquidas de Estudo
- O cronômetro de estudo contabiliza apenas tempo ativo em telas de aula, teoria ou resolução de exercícios.
- Inatividade (sem cliques, digitação ou scroll por mais de 3 minutos) pausa automaticamente o contador de tempo líquido.

#### RN-PRG-004: Índice de Fluência e Velocidade
- Calcula o tempo médio em segundos gasto por questão em cada volume da coleção Iezzi.
- Serve como métrica comparativa para identificar hesitação ou rapidez excessiva com erros por descuido.

#### RN-PRG-005: Sequência de Dias Ativos (Streaks)
- Um dia é contabilizado como "Ativo" se o aluno concluir ao menos 1 aula ou submeter 1 lista de exercícios/treino.
