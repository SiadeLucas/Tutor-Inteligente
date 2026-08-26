---
title: Onboarding - Fluxo
type: module
status: draft
related:
  - modules/onboarding/index.md
  - modules/onboarding/business-rules.md
last_updated: "2026-08-26"
updated_by: claude
---

<!-- ai-summary
Fluxo do módulo Onboarding. Wizard de 4 etapas: Dados Pessoais → Contato → Acadêmico → Prova de Proficiência.
Cadastro com validação por etapa. Dados do responsável condicionais (menor de 18). Prova CAT adaptativa ao entrar na matéria.
Pós-prova: resultado visual (gráfico radar) → dashboard da matéria com trilha personalizada.
-->

# Onboarding — Fluxo

## Fluxo Geral

```mermaid
flowchart TD
    A["Início"] --> B["Etapa 1: Dados Pessoais"]
    B --> C["Etapa 2: Contato"]
    C --> D["Etapa 3: Acadêmico"]
    D --> E{"Menor de 18?"}
    E -->|Sim| F["Dados do Responsável"]
    E -->|Não| G["Etapa 4: Prova de Proficiência"]
    F --> G
    G --> H{"Aluno quer fazer?"}
    H -->|Sim| I["Prova CAT Adaptativa"]
    H -->|Pular| J["Classificado como Básico"]
    I --> K["Resultado da Prova"]
    J --> L["Dashboard da Matéria"]
    K --> L
    L --> M["Onboarding Concluído ✅"]
```

## Etapa 1: Dados Pessoais

```mermaid
flowchart TD
    A["Formulário: Dados Pessoais"] --> B["Preenche: nome, CPF, nascimento, gênero"]
    B --> C{"Foto de perfil?"}
    C -->|Sim| D["Upload da foto"]
    C -->|Não| E["Continuar sem foto"]
    D --> F["Validação dos campos"]
    E --> F
    F --> G{"Válido?"}
    G -->|Sim| H["→ Etapa 2"]
    G -->|Não| I["Exibe erros"]
    I --> A
```

## Etapa 2: Contato

```mermaid
flowchart TD
    A["Formulário: Contato"] --> B["Preenche: e-mail, telefone"]
    B --> C["Preenche: CEP"]
    C --> D["Auto-preenche: estado, cidade, bairro"]
    D --> E["Validação dos campos"]
    E --> F{"Válido?"}
    F -->|Sim| G["→ Etapa 3"]
    F -->|Não| H["Exibe erros"]
    H --> A
```

## Etapa 3: Acadêmico

```mermaid
flowchart TD
    A["Formulário: Acadêmico"] --> B["Preenche: instituição, série, rede"]
    B --> C{"Idade < 18?"}
    C -->|Sim| D["Exibe campos do responsável"]
    D --> E["Preenche: nome, CPF, telefone do responsável"]
    E --> F["Validação"]
    C -->|Não| F
    F --> G{"Válido?"}
    G -->|Sim| H["→ Etapa 4"]
    G -->|Não| I["Exibe erros"]
    I --> A
```

## Etapa 4: Prova de Proficiência

```mermaid
flowchart TD
    A["Tela: Prova de Proficiência"] --> B["Explicação: o que é, por que fazer"]
    B --> C{"Aluno decide"}
    C -->|"Fazer prova"| D["Inicia prova CAT"]
    C -->|"Pular"| E["Todas as áreas → Básico"]

    D --> F["Questão de nível médio"]
    F --> G{"Acertou?"}
    G -->|Sim| H["Próxima: mais difícil"]
    G -->|Não| I["Próxima: mais fácil"]
    H --> J{"Atingiu ~15-20 questões?"}
    I --> J
    J -->|Não| F
    J -->|Sim| K["Calcula nível por área"]

    K --> L["Tela de Resultado"]
    L --> M["Gráfico radar + resumo"]
    M --> N["Botão: Ir para minha trilha"]
    E --> O["Dashboard da matéria"]
    N --> O
```

## Fluxo de Prova para Novas Matérias (futuro)

```mermaid
flowchart TD
    A["Aluno navega para nova matéria"] --> B{"Já fez prova?"}
    B -->|Sim| C["Dashboard da matéria"]
    B -->|Não| D["Sugere prova de proficiência"]
    D --> E{"Aceita?"}
    E -->|Sim| F["Prova CAT da matéria"]
    E -->|Pular| G["Todas as áreas → Básico"]
    F --> H["Resultado + Dashboard"]
    G --> C
    H --> C
```

## Fluxo de Refazer Prova

```mermaid
flowchart TD
    A["Aluno quer refazer prova"] --> B{"Última tentativa > 7 dias?"}
    B -->|Sim| C["Inicia nova prova CAT"]
    B -->|Não| D["Bloqueado: aguarde X dias"]
    C --> E["Resultado atualizado"]
    E --> F["Nível ativo = última tentativa"]
    F --> G["Histórico salvo"]
```
