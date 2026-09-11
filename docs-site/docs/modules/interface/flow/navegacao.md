---
title: Interface - 1. Navegação e Layout
type: module
status: draft
related:
  - modules/interface/flow/index.md
last_updated: "2026-09-10"
updated_by: antigravity
---

# 1. Navegação e Layout

### 1.1 Estrutura Geral da Interface

A plataforma segue o padrão **sidebar fixa + área de conteúdo**, com comportamento adaptativo por dispositivo.

```mermaid
flowchart LR
    A["Sidebar Fixa (Desktop)"] --> B["Dashboard"]
    A --> C["Matérias"]
    A --> D["Progresso"]
    A --> E["Exercícios"]
    A --> F["Perfil"]
    B --> G["Área de Conteúdo Central"]
    C --> G
    D --> G
    E --> G
    F --> G
```

### 1.2 Comportamento Responsivo por Breakpoint

```mermaid
flowchart TD
    A["Usuário acessa a plataforma"] --> B{"Largura da tela?"}
    B -->|"< 768px (Mobile)"| C["BottomNav fixa na base (sem hamburger) \n Header compacto no topo \n Cards empilhados (1 coluna) \n Conteúdo full-width"]
    B -->|"768-1024px (Tablet)"| D["Sidebar colapsável \n Grid de 2 colunas \n Sidebar de conteúdo sobreposta"]
    B -->|"> 1024px (Desktop)"| E["Sidebar fixa expandida \n Grid de 2-3 colunas \n Sidebar de conteúdo visível"]
```

### 1.3 Transição entre Telas

```mermaid
flowchart TD
    A["Login"] --> B["Dashboard (Home)"]
    B --> C["Matérias"]
    C --> D["Skill Tree da Matéria"]
    D --> E["Lista de Aulas da Área"]
    E --> F["Tela de Aula: Split-screen KaTeX (4 Blocos) + Chat IA"]
    F --> G["Bateria de Fixação (Bloco 4 com Pistas IA)"]
    G --> H["Resultado + Atualização Heatmap (>=60%)"]
    H --> D
    B --> I["Progresso"]
    B --> J["Exercícios Pendentes"]
    B --> K["Perfil / Config"]
```

### 1.4 Dark Mode

```mermaid
flowchart TD
    A["Usuário abre a plataforma"] --> B{"Preferência do SO?"}
    B -->|"prefers-color-scheme: dark"| C["Aplica Dark Mode automaticamente"]
    B -->|"prefers-color-scheme: light"| D["Aplica Light Mode"]
    C --> E{"Toggle manual?"}
    D --> E
    E -->|Sim| F["Salva preferência no perfil do usuário"]
    E -->|Não| G["Mantém preferência do SO"]
```
