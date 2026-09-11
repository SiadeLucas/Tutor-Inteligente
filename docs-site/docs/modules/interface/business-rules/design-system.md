---
title: Interface - 1. Design System
type: module
status: active
related:
  - modules/interface/business-rules/index.md
last_updated: "2026-09-10"
updated_by: antigravity
---

# 1. Design System

### 1.1 Paleta de Cores

#### RN-INT-001 (revisada 2026-09-10): Cor como Dado — Tokens por Disciplina
- **Fonte da verdade:** a coluna `disciplinas.cor_tema` (banco de dados). A cor da matéria é DADO, não código.
- O motor de cor (`frontend/src/lib/color.ts`) deriva, em OKLCH, uma escala completa `50–900` a partir desse único hex, com lightness e croma fixos por step.
- Como a lightness é idêntica entre disciplinas, o contraste (WCAG AA) é garantido por construção para qualquer matéria cadastrada.
- O `DisciplineThemeProvider` (carregado no `layout.tsx` raiz) busca a disciplina em `GET /api/v1/conteudo/disciplinas/{slug}` e injeta as variáveis na `<html>`.
- **Camadas de tokens (Tailwind):**
  - `subject-{50..900}` + `subject-wash`/`subject-wash-strong` — identidade da matéria (laranja = Matemática hoje).
  - `ink-{text,muted,faint}` — texto estrutural.
  - `surface-{bg,card,elevated}` — fundos.
  - `line` / `line-strong` — bordas e hairlines.
- **Cores semânticas universais permanecem globais** (não variam por matéria): `emerald` = sucesso, `rose` = erro, `amber` = alerta/pontuação parcial. O heatmap de domínio (RN-PRG-012: cinza/vermelho/amarelo/verde) é semântico e não é tematizado.
- **Dark mode neutro:** superfícies escuras não são tingidas pela matéria; apenas a escala `subject-*` carrega a identidade. Neutros recebem matiz sutil do hue da disciplina (croma ≤ 0.014).
- **Proibido em componentes:** hex de marca e classes `orange-*`/`amber-*` como cor de marca. Ícones são sempre vetoriais (Lucide/Material) — nunca emoji (RN-INT-004).
- Tokens legados `--ti-*` foram removidos; componentes que os referenciavam foram migrados.

| Token (classe Tailwind) | Variável CSS | Uso |
|:---|:---|:---|
| `subject-{50..900}` | `--subject-{50..900}` | Identidade da matéria: CTAs (`500`/`600` hover), destaque textual (`600`/`700`), tintas (`100`/`200`) |
| `subject-wash` / `subject-wash-strong` | `--subject-wash` / `--subject-wash-strong` | Fundos tingidos com alfa pré-computado (essencial no dark mode) |
| `ink-text` / `ink-muted` / `ink-faint` | `--ink-text` / `--ink-muted` / `--ink-faint` | Texto principal, secundário e apagado |
| `surface-bg` / `surface-card` / `surface-elevated` | `--surface-bg` / `--surface-card` / `--surface-elevated` | Fundo da página, cards, elementos elevados/hover |
| `line` / `line-strong` | `--line-border` / `--line-strong` | Bordas e hairlines |

Para novas disciplinas (ex: Física, Química), basta inserir o registro com o hex desejado em `disciplinas.cor_tema` — a escala completa é derivada automaticamente, sem alteração de código ou CSS.

---

### 1.2 Tipografia

#### RN-INT-002: Fonte e Hierarquia Tipográfica
- A fonte principal é **Inter** com fallback para system fonts.
- Hierarquia tipográfica:

| Elemento | Tamanho | Peso | Uso |
|:---|:---|:---|:---|
| H1 | 2rem (32px) | 700 | Título de página |
| H2 | 1.5rem (24px) | 600 | Seções |
| H3 | 1.25rem (20px) | 600 | Sub-seções |
| Body | 1rem (16px) | 400 | Texto corrido |
| Caption | 0.875rem (14px) | 400 | Labels, legendas |
| Small | 0.75rem (12px) | 400 | Metadados, timestamps |

#### RN-INT-003: Renderização Matemática com KaTeX
- Todas as fórmulas e expressões matemáticas devem ser renderizadas via **KaTeX** (client-side).
- Fórmulas inline: delimitadores `$...$` ou `\\(...\\)`.
- Fórmulas em bloco: delimitadores `$$...$$` ou `\\[...\\]`.
- O KaTeX deve ser carregado de forma assíncrona para não bloquear o carregamento da página.
- O tamanho da fonte matemática deve acompanhar o tamanho do texto ao redor.

---

### 1.3 Ícones e Elementos Visuais

#### RN-INT-004: Sistema de Ícones
- Utilizar **Material Icons Outlined** como biblioteca padrão de ícones (consistência com o MkDocs).
- Cada item da sidebar deve ter um ícone associado para identificação rápida.
- Ícones devem ter tamanho mínimo de 24x24px para touch targets em mobile.

---

### 1.4 Dark Mode

#### RN-INT-005: Implementação de Dark Mode
- O dark mode deve ser ativado por:
  1. **Preferência do SO** (`prefers-color-scheme: dark`) como padrão inicial.
  2. **Toggle manual** disponível na sidebar ou perfil.
- A preferência manual é salva no perfil do usuário e prevalece sobre a do SO.
- Todos os componentes devem ter variantes light e dark usando os tokens CSS.
- Transição suave de 0.4s ao alternar entre modos.
