---
title: Interface
type: module
status: draft
related:
  - modules/interface/flow/index.md
  - modules/interface/business-rules/index.md
  - modules/onboarding/index.md
  - modules/conteudo/index.md
  - modules/exercicios/index.md
  - modules/painel-professor/index.md
last_updated: "2026-08-28"
updated_by: claude
---

<!-- ai-summary
Módulo Interface. Design system e UX da plataforma Tutor Inteligente.
Paradigma visual: estilo Khan Academy — limpo, minimalista, foco no conteúdo.
Navegação: sidebar fixa esquerda (colapsável no mobile → hamburger menu).
Seções da sidebar: Dashboard, Matérias, Progresso, Exercícios, Perfil.
Paleta: laranja (#F57C00) + neutros + dark mode.
Tipografia: Inter.
Renderização matemática: KaTeX.
Responsividade: mobile-first, 3 breakpoints (mobile <768px, tablet 768-1024px, desktop >1024px).
Dashboard: cards modulares + progresso visual (gráfico radar, continue de onde parou, recomendados, exercícios pendentes).
Dashboard da Matéria: árvore de habilidades visual (skill tree) com nós por área/tópico.
Tela de Aula: vídeo principal + materiais complementares + lista de aulas lateral.
Tela de Exercícios: tela dedicada focada, uma questão por vez, feedback imediato, KaTeX.
Painel do Professor: dashboard com cards de métricas (região, idade, instituição, CAT) + filtros.
Roadmap de Interface: Calendário/Agenda, Comunidade/Fórum.
-->

# Interface

Design system, UI/UX e diretrizes visuais da plataforma Tutor Inteligente.

## Paradigma Visual

**Estilo Khan Academy** — interface limpa, minimalista e focada no conteúdo. Redução de carga cognitiva para que o aluno foque no aprendizado de Matemática.

## Referências de Design

| Referência | O que inspira |
|---|---|
| Khan Academy | Árvore de habilidades, interface limpa, foco em matemática |
| Brilliant.org | Exercícios interativos, microlearning |
| Notion | Sidebar fixa, organização clara |
| Discord | Sidebar colapsável responsiva |

## Design Tokens

### Paleta de Cores

| Token | Valor | Uso |
|---|---|---|
| `--ti-primary` | `#F57C00` | Cor principal, CTAs, destaques |
| `--ti-primary-dark` | `#EF6C00` | Tabs, footer, header |
| `--ti-primary-light` | `#FB8C00` | Links, hovers |
| `--ti-accent` | `#FFB74D` | Acentos, badges, scrollbars |
| `--ti-deep` | `#E65100` | Texto em destaque |
| `--ti-tint` | `#FFF3E0` | Fundos sutis, code blocks |
| `--ti-bg-dark` | `#1a1408` | Fundo dark mode |
| `--ti-text-dark` | `#FFCC80` | Texto claro em dark mode |

### Tipografia

| Propriedade | Valor |
|---|---|
| Fonte principal | Inter |
| Fallback | -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif |
| Peso títulos | 600-700 |
| Peso corpo | 400 |
| Renderização matemática | KaTeX (client-side) |

### Breakpoints Responsivos

| Dispositivo | Largura | Comportamento |
|---|---|---|
| Mobile | < 768px | Sidebar → hamburger menu, cards empilhados, conteúdo full-width |
| Tablet | 768px - 1024px | Sidebar colapsável, grid 2 colunas |
| Desktop | > 1024px | Sidebar fixa expandida, grid 2-3 colunas, sidebar de conteúdo |

## Estrutura de Navegação

### Sidebar Principal (Aluno)

| Ícone | Item | Descrição |
|---|---|---|
| 🏠 | Dashboard | Tela principal, resumo do progresso |
| 📚 | Matérias | Catálogo de matérias → skill tree por área |
| 📊 | Progresso | Visão consolidada, gráfico radar, barras |
| ✍️ | Exercícios | Exercícios pendentes, concluídos, recomendados |
| 👤 | Perfil | Dados pessoais, configurações, prova CAT |

### Dark Mode

- Toggle disponível na sidebar ou perfil
- Respeita `prefers-color-scheme` do sistema operacional
- Tokens de dark mode já definidos no design system

## Telas Principais

### Dashboard (Home)

Layout em **grid de cards modulares** (2-3 colunas desktop, 1 coluna mobile):

| Card | Conteúdo |
|---|---|
| Progresso Geral | Gráfico radar mini + percentual geral |
| Continue de onde parou | Última aula/exercício + botão continuar |
| Recomendados para você | Conteúdos baseados nas áreas mais fracas (CAT) |
| Exercícios pendentes | Lista de exercícios não concluídos |

### Dashboard da Matéria (Skill Tree)

**Árvore de habilidades visual** onde cada matéria mostra suas áreas como nós interconectados:

- Cada nó exibe o nível atual (Básico/Intermediário/Avançado) com cor indicativa
- Ao clicar num nó, abre os conteúdos/aulas daquela área
- Similar a Khan Academy e tech trees de jogos RPG

### Tela de Aula/Conteúdo

- **Área principal**: player de vídeo (ou texto/imagem para conteúdo teórico)
- **Abaixo do vídeo**: descrição, anotações do aluno, materiais complementares (PDF, links)
- **Sidebar direita** (ou abaixo no mobile): lista de aulas do tópico com checkmarks de conclusão
- **Botões**: "Próxima aula" e "Ir para exercícios" no final

### Tela de Exercícios

**Tela dedicada focada** (sem sidebar), uma questão por vez:

- Enunciado com renderização KaTeX para fórmulas
- Área de resposta (múltipla escolha ou input numérico)
- Barra de progresso (questão 3 de 10)
- Feedback imediato após responder (certo/errado + explicação)
- Resultado final com score e áreas para revisar

### Painel do Professor

**Dashboard de métricas** com cards e filtros:

| Card | Conteúdo |
|---|---|
| Alunos Ativos | Total, novos esta semana, por matéria |
| Desempenho por Região | Mapa ou tabela com estados/cidades |
| Desempenho por Faixa Etária | Gráfico de barras |
| Desempenho por Instituição | Ranking de escolas |
| Nível de Entrada (CAT) | Distribuição Básico/Intermediário/Avançado |

Filtros: por matéria, período, região, instituição.

## Seções Detalhadas

| Seção | Descrição |
|---|---|
| [Fluxo](flow/index.md) | Fluxos de navegação e transição entre telas |
| [Regras de Negócio](business-rules/index.md) | Design tokens, responsividade e padrões visuais |
