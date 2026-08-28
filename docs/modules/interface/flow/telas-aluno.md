---
title: Interface - 2. Telas do Aluno
type: module
status: draft
related:
  - modules/interface/flow/index.md
  - modules/interface/flow/navegacao.md
last_updated: "2026-08-28"
updated_by: claude
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

```mermaid
flowchart TD
    A["Seção: Matérias"] --> B["Catálogo de Matérias"]
    B --> C{"Primeira vez nesta matéria?"}
    C -->|Sim| D["Sugere Prova de Proficiência (CAT)"]
    C -->|Não| E["Skill Tree da Matéria"]
    D -->|Fazer| F["Prova CAT"]
    D -->|Pular| G["Nível Básico em todas as áreas"]
    F --> E
    G --> E
    E --> H["Nó: Álgebra (Avançado)"]
    E --> I["Nó: Geometria (Básico)"]
    E --> J["Nó: Trigonometria (Intermediário)"]
    E --> K["Nó: Estatística (Básico)"]
    H -->|Clique| L["Lista de Aulas de Álgebra"]
    I -->|Clique| M["Lista de Aulas de Geometria"]
```

---

### 2.3 Tela de Aula / Conteúdo

Tela de consumo de conteúdo com vídeo, materiais e navegação entre aulas.

```mermaid
flowchart TD
    A["Tela de Aula"] --> B["Player de Vídeo / Conteúdo Teórico"]
    A --> C["Descrição + Anotações do Aluno"]
    A --> D["Materiais Complementares (PDF, Links)"]
    A --> E["Sidebar: Lista de Aulas do Tópico"]
    E --> F["Aula 1 ✅"]
    E --> G["Aula 2 ✅"]
    E --> H["Aula 3 (atual) ▶️"]
    E --> I["Aula 4 ⏳"]
    B --> J["Botão: Próxima Aula"]
    B --> K["Botão: Ir para Exercícios"]
```

---

### 2.4 Tela de Exercícios

Tela dedicada e focada (sem sidebar), uma questão por vez com feedback imediato.

```mermaid
flowchart TD
    A["Início do Exercício"] --> B["Barra de Progresso: Questão 1 de 10"]
    B --> C["Enunciado com KaTeX"]
    C --> D["Área de Resposta"]
    D --> E{"Tipo de Questão"}
    E -->|Múltipla Escolha| F["4-5 Alternativas"]
    E -->|Input Numérico| G["Campo de Digitação"]
    F --> H["Aluno Responde"]
    G --> H
    H --> I{"Correto?"}
    I -->|Sim| J["✅ Feedback Positivo + Explicação"]
    I -->|Não| K["❌ Feedback + Explicação Detalhada"]
    J --> L["Botão: Próxima Questão"]
    K --> L
    L --> M{"Acabou?"}
    M -->|Não| B
    M -->|Sim| N["Tela de Resultado Final"]
    N --> O["Score + Áreas para Revisar"]
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

```mermaid
flowchart TD
    A["Seção: Perfil"] --> B["Dados Pessoais (editar)"]
    A --> C["Foto de Perfil"]
    A --> D["Alterar Senha"]
    A --> E["Prova de Proficiência (refazer)"]
    A --> F["Toggle Dark Mode"]
    A --> G["Dados do Responsável (se menor)"]
```
