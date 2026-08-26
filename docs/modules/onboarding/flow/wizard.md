---
title: Onboarding - 2. Wizard de Cadastro
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/fluxo-geral.md
last_updated: "2026-08-26"
updated_by: claude
---

# 2. Fluxo do Wizard de Cadastro

### 2.1 Etapa 1: Dados Pessoais
Nesta etapa, coletam-se os dados de identificação civil do aluno. A data de nascimento alimenta a lógica de checagem de maioridade para as etapas seguintes.

```mermaid
flowchart TD
    A["Início: Etapa 1"] --> B["Preenchimento: Nome Completo, CPF, Data de Nascimento e Gênero"]
    B --> C{"Deseja enviar Foto de Perfil?"}
    C -->|Sim| D["Upload da Imagem (JPG/PNG até 5MB)"]
    C -->|Não| E["Atribuição de Avatar Padrão com Iniciais"]
    D --> F["Validação Local e Backend de CPF e Formato"]
    E --> F
    F --> G{"Dados Válidos?"}
    G -->|Sim| H["Persistência dos Dados Pessoais → Avançar para Etapa 2"]
    G -->|Não| I["Exibição de Alertas de Validação"]
    I --> B
```

---

### 2.2 Etapa 2: Contato e Endereço
Coleta as informações de comunicação e localização geográfica do aluno, aproveitando o CEP para preenchimento ágil.

```mermaid
flowchart TD
    A["Início: Etapa 2"] --> B["Preenchimento: E-mail e Telefone/WhatsApp"]
    B --> C["Preenchimento do CEP"]
    C --> D["Consulta Automática à API de CEP"]
    D --> E{"CEP Encontrado?"}
    E -->|Sim| F["Auto-preenchimento: Estado, Cidade e Bairro"]
    E -->|Não| G["Habilita preenchimento manual dos campos de endereço"]
    F --> H["Revisão e Ajustes pelo Aluno"]
    G --> H
    H --> I["Validação de Formatos e Unicidade de E-mail"]
    I --> J{"Dados Válidos?"}
    J -->|Sim| K["Persistência de Contato → Avançar para Etapa 3"]
    J -->|Não| L["Exibição de Erros nos Campos"]
    L --> H
```

---

### 2.3 Etapa 3: Dados Acadêmicos e Menoridade
Coleta os dados escolares e insere dinamicamente os campos de responsável legal se o cálculo da idade for inferior a 18 anos.

```mermaid
flowchart TD
    A["Início: Etapa 3"] --> B["Seleção/Busca da Instituição de Ensino"]
    B --> C["Seleção da Rede (Pública / Privada) e Série/Ano"]
    C --> D{"Verificação: Idade < 18 anos?"}
    D -->|Sim| E["Exibição dos Campos do Responsável"]
    E --> F["Preenchimento: Nome, CPF e Telefone do Responsável"]
    D -->|Não| G["Prossegue sem campos adicionais"]
    F --> H["Validação dos Dados Escolares e do Responsável"]
    G --> H
    H --> I{"Formulário Válido?"}
    I -->|Sim| J["Persistência Acadêmica → Avançar para Etapa 4"]
    I -->|Não| K["Destaque dos Campos Incorretos"]
    K --> A
```
