---
title: Interface - 3. Telas do Professor
type: module
status: draft
related:
  - modules/interface/flow/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 3. Telas do Professor

### 3.1 Painel do Professor — Dashboard de Métricas

O professor acessa um dashboard dedicado com cards de métricas, gráficos e filtros avançados.

```mermaid
flowchart TD
    A["Painel do Professor"] --> B["Card: Alunos Ativos \n Total, novos esta semana, por matéria"]
    A --> C["Card: Desempenho por Região \n Mapa ou tabela com estados/cidades"]
    A --> D["Card: Desempenho por Faixa Etária \n Gráfico de barras"]
    A --> E["Card: Desempenho por Instituição \n Ranking de escolas"]
    A --> F["Card: Nível de Entrada (CAT) \n Distribuição Básico/Interm./Avançado"]
    A --> G["Barra de Filtros"]
    G --> H["Filtro: Matéria"]
    G --> I["Filtro: Período"]
    G --> J["Filtro: Região"]
    G --> K["Filtro: Instituição"]
```

### 3.2 Navegação do Professor

```mermaid
flowchart TD
    A["Login como Professor"] --> B["Dashboard de Métricas"]
    B --> C["Detalhamento por Região"]
    B --> D["Detalhamento por Instituição"]
    B --> E["Lista de Alunos"]
    E --> F["Perfil Individual do Aluno"]
    F --> G["Progresso, Nível CAT, Atividades"]
    B --> H["Gestão de Conteúdos"]
    H --> I["Adicionar/Editar Aulas"]
    H --> J["Adicionar/Editar Exercícios"]
```
