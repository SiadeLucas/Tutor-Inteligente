---
title: Onboarding - 3. Prova de Proficiência
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/wizard.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 3. Fluxo da Avaliação de Proficiência (Pós-Cadastro)

> [!NOTE]
> A prova de proficiência **não integra o wizard de cadastro (3 etapas)**. Ela é disparada **ao entrar numa matéria pela primeira vez** — imediatamente após o cadastro (com apenas Matemática disponível) ou ao ingressar em novas matérias no futuro. A criação da sessão CAT ocorre neste momento (motor implementado na Etapa 7).

### 3.1 Iniciação e Decisão de Execução
Apresenta o objetivo pedagógico do teste e permite que o aluno escolha entre fazer o diagnóstico adaptativo imediato ou pular para o nível introdutório.

```mermaid
flowchart TD
    A["Primeiro Acesso a uma Matéria"] --> B["Apresentação: Benefícios do Diagnóstico Personalizado"]
    B --> C{"Opção Escolhida pelo Aluno"}
    C -->|"Fazer Prova Agora"| D["Carregamento do Motor de Questões CAT"]
    C -->|"Pular Diagnóstico"| E["Atribuição do Nível 'Básico' em todas as Áreas"]
    E --> F["Registro de Status: Prova Pendente"]
    F --> G["Redirecionamento ao Dashboard da Matéria"]
    D --> H["Inicia Primeira Questão (Nível Médio)"]
```

---

### 3.2 Execução do Teste Adaptativo (CAT)
O algoritmo CAT seleciona dinamicamente cada questão subsequente com base na resposta anterior, calibrando com precisão a proficiência por área.

```mermaid
flowchart TD
    A["Início da Questão"] --> B["Apresentação do Item (Múltipla Escolha ou Entrada Numérica)"]
    B --> C["Aluno Submete Resposta"]
    C --> D{"Avaliação da Resposta"}
    D -->|Correta| E["Incrementa Parâmetro de Habilidade (Theta)"]
    D -->|Incorreta| F["Reduz Parâmetro de Habilidade (Theta)"]
    E --> G["Motor seleciona questão com discriminação mais alta"]
    F --> G
    G --> H{"Critério de Parada: 15-20 Questões Respondidas?"}
    H -->|Não| A
    H -->|Sim| I["Consolidação dos Índices por Área/Tópico"]
```

---

### 3.3 Apresentação de Resultados e Redirecionamento
Finalizada a prova, a plataforma sintetiza os domínios do aluno e faz a transição para a trilha recomendada.

```mermaid
flowchart TD
    A["Consolidação dos Níveis"] --> B["Renderização do Gráfico Radar de Competências"]
    B --> C["Geração de Síntese Qualitativa (Pontos Fortes e Oportunidades)"]
    C --> D["Exibição do Botão 'Ir para minha trilha personalizada'"]
    D --> E["Clique do Aluno"]
    E --> F["Criação da Trilha Customizada no Dashboard"]
    F --> G["Marcação de Onboarding 100% Concluído"]
```
