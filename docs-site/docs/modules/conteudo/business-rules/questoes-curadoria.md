---
title: Conteúdo - 4. Questões e Curadoria
type: module
status: draft
related:
  - modules/conteudo/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 4. Banco de Questões, Questões Gêmeas e Curadoria Docente

### 4.1 Banco de Questões e Geração Paramétrica

#### RN-CNT-015: Banco Oficial do Iezzi
- O sistema mantém catalogados todos os exercícios propostos, testes de vestibulares e questões dissertativas originais da coleção FME.
- Cada questão possui metadados de: Volume de Origem, Capítulo, Grau de Dificuldade (Fácil, Médio, Difícil), Tipo (Múltipla Escolha / Numérica) e Gabarito com Resolução Passo a Passo.

#### RN-CNT-016: Geração de Questões Gêmeas (Twin Questions)
- O Agente Especialista do volume é capaz de gerar variações matemáticas preservando a mesma estrutura lógica e grau de complexidade do exercício do Iezzi, alterando valores numéricos, funções ou contextos.
- Todas as questões gêmeas geradas acompanham automaticamente o gabarito e resolução analítica completa gerada pela IA.

#### RN-CNT-017: Provas de Auxílio e Simulados Dinâmicos
- A plataforma pode gerar sob demanda listas de reforço e simulados personalizados combinando questões originais do Iezzi e questões gêmeas, priorizando as áreas com menor desempenho do aluno no teste CAT.

### 4.2 Curadoria Docente (Human-in-the-Loop)

#### RN-CNT-018: Estados de Publicação do Conteúdo
- Todo conteúdo, aula ou bateria de questões gerada pela IA transita pelos seguintes estados:
  - `draft_ai`: Gerado pela IA, aguardando revisão.
  - `reviewed_teacher`: Aprovado e/ou editado pelo professor.
  - `published`: Ativo e visível para os alunos na Skill Tree.
  - `archived`: Desativado.

#### RN-CNT-019: Painel de Curadoria do Professor
- O professor pode pré-visualizar aulas e questões exatamente como o aluno as verá, com KaTeX ativo.
- O professor tem permissão para editar qualquer texto, fórmula, adicionar notas de rodapé personalizadas ou gravar/anexar links de vídeo próprios.

#### RN-CNT-020: Aprovação Rápida (1-Click Publish)
- O painel oferece a funcionalidade de aprovação e publicação em lote de capítulos inteiros gerados por IA após rápida inspeção visual do professor.
