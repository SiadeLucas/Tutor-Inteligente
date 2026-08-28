---
title: Interface - 2. Responsividade
type: module
status: draft
related:
  - modules/interface/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
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

#### RN-INT-007: Comportamento da Sidebar por Breakpoint

| Breakpoint | Sidebar | Comportamento |
|:---|:---|:---|
| Mobile | Oculta | Hamburger menu no topo. Abre como overlay lateral com animação slide-in |
| Tablet | Colapsável | Ícones visíveis, expande ao hover ou clique. Overlay no conteúdo |
| Desktop | Fixa expandida | Sempre visível com ícones + labels. Largura fixa de 240-280px |

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
