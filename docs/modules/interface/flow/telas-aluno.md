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

### 2.3 Tela de Aula / Conteúdo (Sessão de 50 Minutos em Split-Screen)

Tela de aprendizado com leitor KaTeX modular e chat socrático contextualizado com IA.

```mermaid
flowchart TD
    A["Tela de Aula Split-Screen"] --> B["Painel Esquerdo (65%): Leitor KaTeX"]
    A --> C["Painel Direito (35%): Chat Socrático IA"]
    
    B --> B1["Bloco 1: Teoria e Teoremas (10 min)"]
    B --> B2["Bloco 2: Exemplos Resolvidos (15 min)"]
    B --> B3["Bloco 3: Dicas IA e Armadilhas (10 min)"]
    B --> B4["Bloco 4: Bateria de Fixação 3 a 5 itens (15 min)"]
    
    C --> C1["Nível 1: Pergunta reflexiva"]
    C --> C2["Nível 2: Dica conceitual"]
    C --> C3["Nível 3: Passo guiado"]
    
    B4 --> D["Critério de Conclusão: Submissão com Aproveitamento >= 60%"]
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
