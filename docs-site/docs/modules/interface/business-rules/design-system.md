---
title: Interface - 1. Design System
type: module
status: draft
related:
  - modules/interface/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 1. Design System

### 1.1 Paleta de Cores

#### RN-INT-001: Cores Primárias e Tokens
- A cor primária da plataforma é **laranja** (`#F57C00`), consistente com a documentação MkDocs.
- Todos os componentes devem referenciar tokens CSS custom properties (ex: `var(--ti-primary)`) ao invés de valores hex diretos.
- Tokens obrigatórios:

| Token | Valor Light | Valor Dark | Uso |
|:---|:---|:---|:---|
| `--ti-primary` | `#F57C00` | `#FFB74D` | CTAs, botões, links ativos |
| `--ti-primary-dark` | `#EF6C00` | `#FB8C00` | Header, footer, tabs |
| `--ti-primary-light` | `#FB8C00` | `#FFCC80` | Hovers, destaques |
| `--ti-accent` | `#FFB74D` | `#FFCC80` | Badges, scrollbars |
| `--ti-deep` | `#E65100` | `#FF9800` | Texto em destaque |
| `--ti-tint` | `#FFF3E0` | `rgba(255,183,77,0.1)` | Fundos sutis |
| `--ti-bg` | `#FFFFFF` | `#1a1408` | Fundo principal |
| `--ti-text` | `#212121` | `#E0E0E0` | Texto principal |

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
