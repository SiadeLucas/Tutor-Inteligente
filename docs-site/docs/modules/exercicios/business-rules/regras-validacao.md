---
title: Exercícios - 3. Questões Gêmeas
type: module
status: draft
related:
  - modules/exercicios/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 3. Geração e Validação de Questões Gêmeas

### 3.1 Validação Plugável por Disciplina

#### RN-EXE-012: Variação a partir de Item Matriz da Coleção
- Toda questão gerada por IA deve obrigatoriamente referenciar um item matriz da coleção didática ativa, preservando:
  - O objetivo pedagógico e a competência avaliada.
  - A estrutura conceitual de resolução.

#### RN-EXE-013: Validação Simbólica Determinística e Validadores Plugáveis
- Nenhuma questão gerada por IA pode ser disponibilizada aos estudantes sem passar pelo pipeline de validação determinística:
  - **Validador Ativo de Lançamento (Matemática - SymPy)**: O motor de computação algébrica SymPy recalcula a expressão analiticamente, atestando convergência exata (tolerância $\pm 0.01$) com o gabarito alegado pela IA.
  - **Validadores de Escalabilidade Futura**: A arquitetura do backend suporta validadores especializados por matéria (parsers de estequiometria para Química, analisadores gramaticais/semânticos determinísticos com temperatura zero para Linguagens).
- Questões com qualquer ambiguidade ou divergência de gabarito são descartadas automaticamente antes de chegarem ao aluno.

#### RN-EXE-014: Harmonia dos Valores Numéricos
- A geração paramétrica deve priorizar valores numéricos limpos (raízes inteiras ou frações irredutíveis simples), exceto quando o objetivo didático for especificamente o tratamento de dízimas ou aproximações irracionais.

#### RN-EXE-015: Herança de Parâmetros de TRI
- As questões gêmeas validadas herdam provisoriamente os parâmetros de discriminação ($a$) e dificuldade ($b$) do item matriz do Iezzi, sendo recalibradas empiricamente após amostragem de respostas reais.

#### RN-EXE-016: Resolução Passo a Passo Obrigatória
- Toda questão gerada deve conter a demonstração analítica completa em KaTeX dividida em etapas lógicas claras.
