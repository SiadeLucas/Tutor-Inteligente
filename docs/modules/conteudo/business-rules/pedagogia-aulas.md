---
title: Conteúdo - 3. Pedagogia e Tutoria
type: module
status: draft
related:
  - modules/conteudo/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 3. Estrutura Pedagógica e Método Socrático

### 3.1 Padrão das Aulas

#### RN-CNT-010: Estrutura Mandatória em 4 Blocos e Condição de Conclusão
Toda aula gerada deve conter sem exceção os 4 blocos sequenciais:
1. **Bloco 1 - Conceito & Teoremas**: Apresentação formal da definição com equações em KaTeX, acompanhada de contextualização geométrica/intuitiva (10 min).
2. **Bloco 2 - Exemplos Resolvidos Passo a Passo**: No mínimo 2 exemplos dissecados detalhadamente (Passo 1: Identificação de dados $\rightarrow$ Passo 2: Aplicação de fórmula/teorema $\rightarrow$ Passo 3: Conclusão) (15 min).
3. **Bloco 3 - Dicas do Tutor IA**: Seção de "Onde os alunos costumam errar", pegadinhas clássicas e aplicabilidade em vestibulares/ENEM (10 min).
4. **Bloco 4 - Bateria de Exercícios de Fixação**: Conjunto de 3 a 5 exercícios do Iezzi com resolução comentada (15 min).

> [!IMPORTANT]
> **Condição de Conclusão Curricular**: Uma aula/capítulo **só é considerada 100% concluída** no módulo de Progresso e libera o próximo nó da Skill Tree quando o estudante **submete a Bateria de Fixação** do Bloco 4 e atinge um **aproveitamento ponderado mínimo de 60%** ($\text{Score Ponderado} \ge 0.60$). O avanço puramente passivo pela leitura da teoria ou submissões com aproveitamento inferior a 60% não concluem o capítulo, incentivando o ciclo de recuperação ativa via Questões Gêmeas.

#### RN-CNT-011: Renderização de Fórmulas com KaTeX
- 100% dos símbolos matemáticos, frações, matrizes, integrais, somatórios e expoentes devem utilizar sintaxe LaTeX padronizada e renderizar client-side via KaTeX.

### 3.2 Tutor Socrático

#### RN-CNT-012: Princípio da Ajuda Gradual (Método Socrático)
- O Tutor de IA **nunca deve fornecer imediatamente o resultado numérico final** ou o gabarito de uma questão em andamento.
- O fluxo de ajuda deve seguir 3 estágios:
  1. *Estágio 1*: Pista lógica ou pergunta orientadora (ex: *"Qual é a condição de existência para um logaritmo ter base válida?"*).
  2. *Estágio 2*: Identificação do teorema ou propriedade do Iezzi aplicável ao caso.
  3. *Estágio 3*: Demonstração passo a passo completa (liberada apenas se o aluno expressamente solicitar após as pistas ou após esgotar as tentativas).

#### RN-CNT-013: Contexto Ativo de Aula
- O chat do tutor recebe automaticamente os metadados da aula/exercício atual do aluno (ID do volume, ID do capítulo, enunciado da questão atual e alternativas).

#### RN-CNT-014: Suporte à Seleção de Trechos Matemáticos
- O aluno pode selecionar qualquer fórmula na tela e acionar a ação *"Explicar este passo"*, enviando o trecho exato como contexto prioritário para a IA.
