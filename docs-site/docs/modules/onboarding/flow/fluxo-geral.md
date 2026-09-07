---
title: Onboarding - 1. Fluxo Geral
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/wizard.md
last_updated: "2026-08-26"
updated_by: claude
---

# 1. Fluxo Geral de Onboarding

### 1.1 Visão Macro do Processo
O fluxo guia o aluno desde o primeiro acesso através de um wizard estruturado, garantindo a coleta de dados cadastrais e a calibragem do seu nível de aprendizado através do teste adaptativo.

```mermaid
flowchart TD
    A["Início: Acesso ao Cadastro"] --> B["1. Dados Pessoais"]
    B --> C["2. Contato e Endereço"]
    C --> D["3. Dados Acadêmicos"]
    D --> E{"Menor de 18 anos?"}
    E -->|Sim| F["3.1 Dados do Responsável"]
    E -->|Não| G["4. Prova de Proficiência"]
    F --> G
    G --> H{"Decisão do Aluno"}
    H -->|Fazer Prova| I["Execução do Teste CAT"]
    H -->|Pular Prova| J["Classificação Padrão: Básico"]
    I --> K["Exibição de Resultados"]
    J --> L["Acesso ao Dashboard da Matéria"]
    K --> L
    L --> M["Onboarding Concluído ✅"]
```

### 1.2 Transição entre Etapas e Persistência
Cada etapa do formulário é validada e salva incrementalmente no backend. Se o aluno interromper o cadastro antes da conclusão, seu progresso nas etapas concluídas é preservado para retomada posterior.
