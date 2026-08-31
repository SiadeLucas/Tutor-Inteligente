---
title: Exercícios - 3. Questões Gêmeas
type: module
status: draft
related:
  - modules/exercicios/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 3. Geração e Validação de Questões Gêmeas

### 3.1 Dupla Validação Computacional

#### RN-EXE-012: Variação a partir de Item Matriz do Iezzi
- Toda questão gerada por IA deve obrigatoriamente referenciar um item matriz da coleção Iezzi, preservando:
  - O objetivo pedagógico e a competência matemática.
  - A estrutura algébrica/geométrica de resolução.

#### RN-EXE-013: Validação Simbólica Determinística Obrigatória
- Nenhuma questão gerada por IA pode ser disponibilizada aos estudantes sem que o motor de computação algébrica (SymPy) resolva a expressão e ateste convergência exata com o gabarito alegado pela IA.
- Questões com qualquer ambiguidade ou divergência de gabarito são automaticamente descartadas.

#### RN-EXE-014: Harmonia dos Valores Numéricos
- A geração paramétrica deve priorizar valores numéricos limpos (raízes inteiras ou frações irredutíveis simples), exceto quando o objetivo didático for especificamente o tratamento de dízimas ou aproximações irracionais.

#### RN-EXE-015: Herança de Parâmetros de TRI
- As questões gêmeas validadas herdam provisoriamente os parâmetros de discriminação ($a$) e dificuldade ($b$) do item matriz do Iezzi, sendo recalibradas empiricamente após amostragem de respostas reais.

#### RN-EXE-016: Resolução Passo a Passo Obrigatória
- Toda questão gerada deve conter a demonstração analítica completa em KaTeX dividida em etapas lógicas claras.
