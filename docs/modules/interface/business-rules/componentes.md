---
title: Interface - 3. Componentes e Telas
type: module
status: draft
related:
  - modules/interface/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 3. Componentes e Telas

### 3.1 Dashboard (Home)

#### RN-INT-011: Cards do Dashboard
- O Dashboard exibe 4 cards modulares em grid responsivo:
  1. **Progresso Geral**: gráfico radar mini + percentual geral de conclusão.
  2. **Continue de onde parou**: último conteúdo acessado com botão "Continuar".
  3. **Recomendados para você**: 3-5 conteúdos recomendados com base nas áreas mais fracas (CAT).
  4. **Exercícios pendentes**: lista dos próximos exercícios não concluídos.
- Se o aluno não tiver histórico, exibir cards com estado vazio ("Comece sua primeira aula!").

---

### 3.2 Skill Tree (Dashboard da Matéria)

#### RN-INT-012: Visualização da Árvore de Habilidades
- Cada matéria exibe uma árvore de habilidades visual (skill tree) com nós interconectados.
- Cada nó representa uma **área/tópico** da matéria (ex: Álgebra, Geometria).
- O nó exibe: nome da área, nível atual e cor indicativa:

| Nível | Cor do Nó |
|:---|:---|
| Básico | Cinza / Laranja claro |
| Intermediário | Laranja |
| Avançado | Verde / Dourado |

- Ao clicar num nó, expande a lista de aulas/conteúdos daquela área.
- No mobile, o skill tree deve ser scrollável horizontalmente ou adaptar para layout vertical.

---

### 3.3 Tela de Aula

#### RN-INT-013: Layout da Tela de Aula
- Área principal (70%): player de vídeo ou conteúdo teórico.
- Sidebar direita (30%): lista de aulas do tópico com checkmarks de conclusão.
- No mobile: sidebar fica abaixo do player (empilhado).
- Abaixo do player: descrição, anotações do aluno, materiais complementares.
- Botões de ação: "Próxima Aula" e "Ir para Exercícios".

#### RN-INT-014: Player de Vídeo
- O player deve suportar: play/pause, controle de velocidade (0.5x a 2x), fullscreen e legendas.
- Salvar automaticamente a posição do vídeo para retomar depois.
- No mobile, o player deve ocupar a largura total da tela.

---

### 3.4 Tela de Exercícios

#### RN-INT-015: Layout do Exercício
- Tela dedicada e focada (sem sidebar de navegação principal).
- Uma questão por vez, com barra de progresso no topo.
- Feedback imediato após cada resposta (certo/errado + explicação).
- Fórmulas renderizadas com KaTeX.
- No mobile, as alternativas de múltipla escolha devem ser botões full-width empilhados.

#### RN-INT-016: Tela de Resultado
- Após a última questão, exibir:
  - Score geral (ex: 7/10 corretas).
  - Lista de questões com acerto/erro e link para revisão.
  - Botão: "Voltar para a trilha" e "Refazer exercício".

---

### 3.5 Painel do Professor

#### RN-INT-017: Dashboard de Métricas
- O painel do professor é uma tela separada acessível apenas por perfis com role `professor`.
- Layout de cards com métricas (similar a Google Analytics / Metabase).
- Filtros globais no topo: matéria, período, região, instituição.
- Cards de métricas:
  - Alunos Ativos (total, novos, por matéria).
  - Desempenho por Região (mapa ou tabela).
  - Desempenho por Faixa Etária (gráfico de barras).
  - Desempenho por Instituição (ranking).
  - Nível de Entrada CAT (distribuição por área).

#### RN-INT-018: Gestão de Conteúdo
- O professor deve poder adicionar, editar e remover aulas e exercícios.
- Interface de edição com suporte a KaTeX para fórmulas.
- Preview em tempo real do conteúdo antes de publicar.
