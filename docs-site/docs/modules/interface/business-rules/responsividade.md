---
title: Interface - 2. Responsividade
type: module
status: draft
related:
  - modules/interface/business-rules/index.md
last_updated: "2026-09-10"
updated_by: antigravity
---

# 2. Responsividade

### 2.1 Breakpoints e Layouts

#### RN-INT-006: Definição de Breakpoints
- A plataforma segue estratégia **mobile-first** com 3 breakpoints:

| Breakpoint | Largura | Classe |
|:---|:---|:---|
| Mobile | < 768px | `.layout-mobile` |
| Tablet | 768px - 1024px | `.layout-tablet` |
| Desktop | > 1024px | `.layout-desktop` |

#### RN-INT-007 (revisada 2026-09-10): Navegação Primária por Breakpoint

A navegação primária é renderizada pelo `AppShell` (`frontend/src/components/nav/AppShell.tsx`),
composto por `GlobalHeader` (topo) + `SideNav` (desktop) + `BottomNav` (mobile).

| Breakpoint | Componente | Comportamento |
|:---|:---|:---|
| Mobile (< 768px) | `BottomNav` fixa na base + `GlobalHeader` compacto (h-14) no topo | Tab bar com 4 itens (Matérias, Praticar, Progresso, Perfil), dentro da zona do polegar; **sem hamburger** |
| Tablet (768–1024px) | Mesmo padrão do mobile | BottomNav + header; grid de 2 colunas (RN-INT-008) |
| Desktop (> 1024px) | `SideNav` fixa de 256px | Sempre visível, ícones + labels; conteúdo deslocado (`lg:pl-64`); BottomNav oculta |

Regras adicionais:
- **Focus-mode:** `/exercicios` e `/onboarding/cat` não exibem navegação primária
  (nem SideNav nem BottomNav) — telas dedicadas e focadas, conforme protótipos de
  Exercícios e CAT. O GlobalHeader permanece para contexto e logout.
- **Safe areas:** o root layout declara `viewportFit: "cover"`; a BottomNav aplica
  `env(safe-area-inset-bottom)` e as páginas usam utilitário `.pb-safe-bottom`
  (56px + safe-area) para conteúdo não ficar sob a tab bar.
- **Páginas não renderizam header:** o header vive no layout da rota (`(student)/layout.tsx`,
  `(teacher)/layout.tsx`); imports por página são proibidos (fonte de duplicação).
- Itens ativos da navegação usam estado visual com tokens da disciplina
  (`subject-wash` + `text-subject-600`), nunca cores fixas.

#### RN-INT-008: Grid de Cards

| Breakpoint | Colunas | Comportamento |
|:---|:---|:---|
| Mobile | 1 coluna | Cards empilhados, full-width |
| Tablet | 2 colunas | Grid flexível |
| Desktop | 2-3 colunas | Grid responsivo com `auto-fill, minmax(300px, 1fr)` |

---

### 2.2 Touch e Acessibilidade

#### RN-INT-009: Touch Targets
- Todos os elementos interativos devem ter área mínima de **44x44px** (WCAG 2.5.5).
- Espaçamento mínimo entre elementos clicaveis: 8px.
- Botões de ação primária: altura mínima de 48px.

#### RN-INT-010: Acessibilidade
- Contraste mínimo de **4.5:1** para texto normal e **3:1** para texto grande (WCAG AA).
- Todos os ícones devem ter `aria-label` descritivo.
- Navegação por teclado (Tab, Enter, Escape) deve funcionar em todas as telas.
- Fórmulas KaTeX devem incluir `aria-label` com a descrição textual da fórmula.
