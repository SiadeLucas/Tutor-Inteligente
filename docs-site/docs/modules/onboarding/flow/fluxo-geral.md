---
title: Onboarding - 1. Fluxo Geral
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/wizard.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 1. Fluxo Geral de Onboarding

### 1.1 Visão Macro do Processo
O fluxo guia o aluno desde o primeiro acesso através de um **wizard de 3 etapas**, garantindo a coleta de dados cadastrais. A calibragem do nível de aprendizado (teste adaptativo CAT) ocorre no primeiro ingresso em uma matéria, após a conclusão do cadastro.

```mermaid
flowchart TD
    A["Início: Acesso ao Cadastro"] --> B["1. Dados Pessoais (Nome, CPF, Nascimento, Gênero, Foto opcional)"]
    B --> C["2. Contato e Credenciais (E-mail, Senha, Telefone)"]
    C --> D{"Menor de 18 anos?"}
    D -->|Sim| E["2.1 Dados do Responsável Legal"]
    D -->|Não| F["3. Acadêmico e Endereço (CEP/ViaCEP, Rede, Série)"]
    E --> F
    F --> G["Finalização Atômica do Cadastro (usuário + sessão ativa)"]
    G --> H["Dashboard de Matérias"]
    H --> I{"Primeiro Acesso a uma Matéria?"}
    I -->|Sim| J{"Decisão do Aluno"}
    J -->|Fazer Prova| K["Execução do Teste CAT"]
    J -->|Pular Prova| L["Classificação Padrão: Básico"]
    K --> M["Exibição de Resultados (Radar)"]
    L --> N["Acesso ao Dashboard da Matéria"]
    M --> N
    N --> O["Onboarding Concluído ✅"]
```

### 1.2 Transição entre Etapas e Persistência
Cada etapa do formulário é validada no backend e o rascunho parcial é sincronizado com o Redis (TTL de 48 horas). Se o aluno interromper o cadastro antes da conclusão, seu progresso é preservado para retomada posterior.
