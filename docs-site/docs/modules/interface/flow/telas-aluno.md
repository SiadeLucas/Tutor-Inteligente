---
title: Interface - 2. Telas do Aluno
type: module
status: draft
related:
  - modules/interface/flow/index.md
  - modules/interface/flow/navegacao.md
last_updated: "2026-09-10"
updated_by: antigravity
---

# 2. Telas do Aluno

### 2.1 Dashboard (Home)

Primeira tela após o login. Grid de cards modulares com resumo do progresso e ações rápidas.

```mermaid
flowchart TD
    A["Dashboard"] --> B["Card: Progresso Geral \n Radar mini + % geral"]
    A --> C["Card: Continue de onde parou \n Última aula + botão Continuar"]
    A --> D["Card: Recomendados \n Conteúdos baseados no CAT"]
    A --> E["Card: Exercícios Pendentes \n Lista de não concluídos"]
    C -->|Clique| F["Tela de Aula"]
    D -->|Clique| G["Tela de Conteúdo"]
    E -->|Clique| H["Tela de Exercício"]
```

---

### 2.2 Matérias e Skill Tree

O aluno navega pelo catálogo de matérias e visualiza a árvore de habilidades.

**Layout revisado (2026-09-10, diretriz "Caderno de Foco"):** header tipográfico flat
(sem banner-card), stats inline com `tabular-nums`, e cada volume exibe uma
**mastery strip** — uma célula na cor canônica do heatmap (RN-PRG-012) por capítulo —
para leitura de domínio de um relance. Capítulos são linhas com hairlines
(sem card-in-card). Callouts de CAT pendente e Caixa de Reforço aparecem como
faixas planas acima da lista.

```mermaid
flowchart TD
    A["Seção: Matérias"] --> B["Header tipográfico + stats + filtro por Grande Área"]
    B --> C{"Primeira vez nesta matéria?"}
    C -->|Sim| D["Callout flat: Prova de Proficiência (CAT)"]
    C -->|Não| E["Lista de Volumes com Mastery Strip"]
    D -->|Fazer| F["Prova CAT"]
    D -->|Pular| G["Nível Básico em todas as áreas"]
    F --> E
    G --> E
    E --> H["Volume: strip de células heatmap + % domínio"]
    H -->|Expande| I["Linhas de capítulos: dot de domínio + título + ações"]
    I -->|Clique na linha| J["Tela de Aula"]
    I -->|Ícone exercício| K["Tela de Exercícios (focus-mode)"]
```

---

### 2.3 Tela de Aula / Conteúdo (Sessão de 50 Minutos em Split-Screen)

Tela de aprendizado com leitor KaTeX modular e chat socrático contextualizado com IA.

**Layout revisado (2026-09-10, diretriz "Caderno de Foco"):**
- Subheader sticky: breadcrumb (Vol/Cap) + cronômetro compacto + 4 pips de
  progresso dos blocos visitados; barra de progresso de leitura no topo absoluto.
- Abas dos 4 blocos como **segmented control** sticky (não tabs de borda).
- Medida de leitura única (`max-w-[65ch]`) com tipografia sustentada.
- **Chat socrático:** docked a 35% no desktop (>= lg); no mobile, FAB flutuante
  abre slide-over full-height (sem split-screen espremido).

```mermaid
flowchart TD
    A["Tela de Aula"] --> B["Desktop: Painel Leitura (65%) + Chat Docked (35%)"]
    A --> B2["Mobile: Leitura full-width + FAB abre Chat slide-over"]
    
    B --> B1["Bloco 1: Teoria e Teoremas (10 min)"]
    B --> B3["Bloco 2: Exemplos Resolvidos (15 min)"]
    B --> B4["Bloco 3: Dicas IA e Armadilhas (10 min)"]
    B --> B5["Bloco 4: Bateria de Fixação 3 a 5 itens (15 min)"]
    
    B2 --> C1["Nível 1: Pergunta reflexiva"]
    B2 --> C2["Nível 2: Dica conceitual"]
    B2 --> C3["Nível 3: Passo guiado"]
    
    B5 --> D["Critério de Conclusão: Submissão com Aproveitamento >= 60%"]
```

---

### 2.4 Tela de Exercícios

Tela dedicada e focada (sem navegação primária — AppShell focus-mode), uma questão por vez com feedback imediato.

**Layout revisado (2026-09-10, diretriz "Caderno de Foco"):**
- Faixa de progresso sticky sob o header (questão N de M + pontos, sair com ←).
- Coluna única `max-w-2xl`: a questão É a página (sem card-in-card).
- Enunciado KaTeX oversized (`text-base sm:text-lg`); alternativas com chip de letra.
- **CTA único full-width na base** (>= 52px de altura) enquanto responde.
- Conclusão: hero tipográfico com o aproveitamento como protagonista (`tabular-nums`)
  e badge semântico >= 60% (RN-CNT-010).

```mermaid
flowchart TD
    A["Início da Bateria"] --> B["Faixa sticky: Questão 1 de 10 + pontos"]
    B --> C["Enunciado KaTeX oversized"]
    C --> D{"Tipo de Questão"}
    D -->|Múltipla Escolha| F["Alternativas com chip de letra"]
    D -->|Input Numérico| G["Campo mono + preview KaTeX"]
    F --> H["CTA único: Confirmar Resposta"]
    G --> H
    H --> I{"Correto?"}
    I -->|1ª errada com 2ª chance| K["Pista socrática + Tentar 2ª chance"]
    I -->|Sim| J["Feedback + Resolução passo a passo"]
    I -->|Esgotado| J2["Gabarito + Caixa de Reforço"]
    J --> L["Próxima Questão / Questão Gêmea"]
    J2 --> L
    K --> H
    L --> M{"Acabou?"}
    M -->|Não| B
    M -->|Sim| N["Hero de Resultado: aproveitamento em destaque"]
```

---

### 2.5 Progresso Consolidado

Visão geral do progresso do aluno por matéria e área.

```mermaid
flowchart TD
    A["Seção: Progresso"] --> B["Gráfico Radar por Matéria"]
    A --> C["Barras de Progresso por Área"]
    A --> D["Histórico de Atividades"]
    A --> E["Histórico de Provas CAT"]
    B --> F["Detalhamento: Clique na área"]
    F --> G["Aulas concluídas, exercícios feitos, nota média"]
```

---

### 2.6 Perfil e Configurações

Tela em modo leitura (`max-w-3xl`), seções flat separadas por hairlines — mesma linguagem das telas 2.2–2.5.

```mermaid
flowchart TD
    A["Seção: Perfil"] --> B["Identidade: avatar de iniciais + nome + membro desde"]
    A --> C["Acesso: e-mail/CPF (leitura) + telefone editável — PATCH /auth/me"]
    A --> D["Contexto acadêmico: escola, série, cidade (leitura)"]
    A --> G["Responsável legal (exibido se eh_menor_idade)"]
    A --> E["Aparência: Claro / Escuro / Sistema — persistido (RN-INT-005)"]
    A --> H["Prova de proficiência: refazer CAT → /onboarding/cat"]
    A --> F["Segurança: alterar senha (PATCH /auth/me/senha) + logout remoto (RN-AUT-015)"]
```

Notas de implementação:

- **Somente leitura:** e-mail, CPF e contexto acadêmico não são editáveis
  na tela (integridade de recuperação de conta e dados acadêmicos).
- **Tema:** o modo escolhido (light/dark/system) persiste em
  `localStorage` (`ti-theme`) e é aplicado pelo `DisciplineThemeProvider`,
  que recalcula as superfícies neutras ao trocar de modo. Em `system`,
  mudanças do SO aplicam ao vivo.
- **Logout remoto:** exige confirmação explícita inline — encerra TODAS as
  sessões (inclusive a atual) e redireciona para `/login`.
