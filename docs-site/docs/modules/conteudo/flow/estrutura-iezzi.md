---
title: Conteúdo - 1. Estrutura e Mapeamento Iezzi
type: module
status: draft
related:
  - modules/conteudo/flow/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 1. Estrutura e Mapeamento da Coleção Iezzi

### 1.1 Hierarquia de Conteúdo

A plataforma estrutura o conhecimento em uma árvore multinível que conecta a coleção física à interface do aluno:

```mermaid
graph TD
    Matematica["Matemática (Ensino Médio / 2º Grau)"]
    
    Matematica --> Area1["1. Álgebra e Funções"]
    Matematica --> Area2["2. Geometria e Trigonometria"]
    Matematica --> Area3["3. Álgebra Linear e Sequências"]
    Matematica --> Area4["4. Matemática Aplicada e Estatística"]
    
    Area1 --> V1["Vol 1: Conjuntos e Funções"]
    Area1 --> V2["Vol 2: Logaritmos"]
    Area1 --> V6["Vol 6: Complexos, Polinômios e Equações"]
    Area1 --> V8["Vol 8: Limites, Derivadas e Integrais"]
    
    Area2 --> V3["Vol 3: Trigonometria"]
    Area2 --> V7["Vol 7: Geometria Analítica"]
    Area2 --> V9["Vol 9: Geometria Plana"]
    Area2 --> V10["Vol 10: Geometria Espacial"]
    
    Area3 --> V4["Vol 4: Sequências, Matrizes, Determinantes e Sistemas"]
    
    Area4 --> V5["Vol 5: Combinatória e Probabilidade"]
    Area4 --> V11["Vol 11: Financeira e Estatística Descritiva"]
```

### 1.2 Navegação do Aluno na Skill Tree

```mermaid
flowchart TD
    A["Aluno acessa Matéria: Matemática"] --> B["Visualização da Skill Tree com as 4 Áreas"]
    B --> C["Seleção de uma Grande Área (ex: Geometria)"]
    C --> D["Exibição dos Volumes Correspondentes (Vols 3, 7, 9, 10)"]
    D --> E["Seleção do Volume (ex: Vol 9 - Geometria Plana)"]
    E --> F["Lista de Capítulos e Lições com Status de Domínio"]
    F --> G["Abertura da Tela de Aula Estruturada em 4 Blocos"]
```
