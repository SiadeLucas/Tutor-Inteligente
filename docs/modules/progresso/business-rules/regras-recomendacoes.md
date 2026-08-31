---
title: Progresso - 4. Recomendações e Relatórios
type: module
status: draft
related:
  - modules/progresso/business-rules/index.md
last_updated: "2026-08-31"
updated_by: claude
---

# 4. Recomendações e Emissão de Boletim em PDF

### 4.1 Recomendações e Exportação

#### RN-PRG-016: Regra dos 3 Tópicos com Menor Desempenho
- O card de recomendações varre os capítulos que já tiveram ao menos 1 tentativa de exercício e seleciona os 3 com menor percentual de acerto acumulado.
- Cada item sugerido exibe:
  - Identificação: Volume do Iezzi e Nome do Capítulo.
  - Taxa de acerto atual (ex: `38% de acertos`).
  - Botão de Ação: *"Revisar Conteúdo"* (leva à aula) e *"Praticar Questões"* (abre lista de treino).

#### RN-PRG-017: Formato do Boletim em PDF do Aluno
- O relatório exportável em PDF deve conter:
  - Cabeçalho institucional da plataforma Tutor Inteligente.
  - Dados de identificação do aluno (Nome, Série/Ano e Instituição).
  - Foto do Gráfico Radar atualizado.
  - Tabela consolidada dos 11 Volumes com status de completude e nível ($\theta$).
  - Total de horas líquidas de estudo acumuladas e data de emissão.

#### RN-PRG-018: Autonomia de Download
- O download do PDF é feito diretamente pelo estudante via botão de ação primária *"Baixar Boletim em PDF"*, sem dependência de processamento assíncrono demorado.

#### RN-PRG-019: Privacidade dos Dados de Desempenho
- As métricas de progresso individual são confidenciais, acessíveis apenas pelo próprio aluno e pelo professor gestor no Painel do Professor.

#### RN-PRG-020: Atualização em Tempo Real
- A conclusão de qualquer atividade ou exercício atualiza os dados analíticos de progresso no mesmo instante na sessão do aluno.
