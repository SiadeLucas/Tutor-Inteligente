---
title: Interface - Protótipos de Componentes e UI/UX
type: module
status: draft
related:
  - modules/interface/index.md
  - modules/interface/prototype/katex-renderer.md
  - modules/interface/prototype/skill-tree.md
  - modules/interface/prototype/lesson-player.md
  - modules/interface/prototype/session-modal.md
  - modules/interface/prototype/header-switcher.md
last_updated: "2026-09-03"
updated_by: claude
---

<!-- ai-summary
Hub de protótipos de código do módulo de Interface e UI/UX.
Implementações técnicas de referência em React 18, Next.js 14 App Router, TypeScript, Tailwind CSS e KaTeX:
1. Renderizador KaTeX Seguro com Suporte a SSR.
2. Skill Tree Visual Interativa com SVG e Nós de Domínio.
3. Player de Aula de 50 Minutos em Split-Screen (65% Leitor / 35% Chat de IA).
4. Modal de Congelamento por Sessão Única e Salvamento de Rascunho.
5. Header com Seletor Global de Disciplinas e Menu de Perfil.
-->

# Interface — Protótipos de Componentes e UI/UX

Esta seção reúne as implementações de referência e o código-fonte executável dos componentes do frontend em **Next.js 14+ (App Router)**, **TypeScript**, **Tailwind CSS com Glassmorphism** e **KaTeX** da plataforma **Tutor Inteligente**.

---

## Estrutura dos Protótipos Visuais

| Componente | Função de UI/UX | Tecnologias |
|:---|:---|:---:|
| [1. Renderizador KaTeX Seguro](katex-renderer.md) | Parser e renderizador de fórmulas inline (`$...$`) e em destaque (`$$...$$`) com sanitização | **React / KaTeX** |
| [2. Skill Tree dos 11 Volumes](skill-tree.md) | Grafo interativo de nós com linhas conectoras em SVG, estados de bloqueio e tooltips | **React / Tailwind / SVG** |
| [3. Player de Aula em Split-Screen](lesson-player.md) | Tela de 50 min: Leitor KaTeX à esquerda (65%) + Chat Socrático fixo à direita (35%) | **Next.js 14 / TypeScript** |
| [4. Modal de Sessão Concorrente](session-modal.md) | Overlay congelante que bloqueia a tela, salva rascunhos preenchidos e pausa o cronômetro | **React Portal / Tailwind** |
| [5. Header e Seletor de Matéria](header-switcher.md) | Barra superior com badge institucional `[ 📐 Matemática ]` expansível e perfil | **React / Headless UI** |

---

## Wireframe Arquitetural da Tela de Aula (Split-Screen)

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 📐 Tutor Inteligente   [ Matemática (Ensino Médio) ]         ⏱️ 42:15 restantes  [ Perfil ] │
├───────────────────────────────────────────────────────────────┬─────────────────────────────┤
│ 📚 PAINEL DE LEITURA E CONTEÚDO (65%)                         │ 🤖 TUTOR SOCRÁTICO (35%)    │
│                                                               │                             │
│ [ 1. Teoria (10m) ] [ 2. Exemplos (15m) ] [ 3. Dicas IA ]    │ Volume 1: Iezzi IA          │
│ ───────────────────────────────────────────────────────────── │ ─────────────────────────── │
│ # Função Quadrática e Vértice da Parábola                     │ Aluno:                      │
│                                                               │ "Como acho o ponto máximo   │
│ Seja a função real $f(x) = ax^2 + bx + c$, com $a \neq 0$.    │ dessa função?"              │
│ O vértice $V(x_v, y_v)$ é dado formalmente por:               │                             │
│                                                               │ Tutor de IA:                │
│ $$x_v = -\frac{b}{2a} \quad \text{e} \quad y_v = -\frac{\Delta}{4a}$$ │ "Excelente pergunta! Para que │
│                                                               │ a parábola tenha um ponto   │
│ Como $a < 0$, a concavidade é voltada para baixo,             │ de máximo, qual deve ser o  │
│ determinando um ponto de máximo absoluto no vértice.          │ sinal do coeficiente $a$?"  │
│                                                               │                             │
│ [ Exemplo Resolvido 01 ] ▾                                    │ ┌─────────────────────────┐ │
│ Seja $f(x) = -2x^2 + 8x - 3$. Determine as coordenadas de $V$.│ │ Digite sua dúvida...    │ │
│                                                               │ └─────────────────────────┘ │
│ [ Ir para a Bateria de Fixação (3 a 5 exercícios) ➔ ]          │ [ Enviar ]                  │
└───────────────────────────────────────────────────────────────┴─────────────────────────────┘
```
