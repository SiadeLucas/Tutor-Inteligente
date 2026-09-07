---
title: Onboarding - 2. Wizard de Cadastro
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/fluxo-geral.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 2. Fluxo do Wizard de Cadastro

### 2.1 Etapa 1: Dados Pessoais
Nesta etapa, coletam-se os dados de identificação civil do aluno (incluindo o gênero, usado nas métricas demográficas do Painel do Professor). A data de nascimento alimenta a lógica de checagem de maioridade para as etapas seguintes.

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

### 2.2 Etapa 2: Contato, Credenciais e Responsável Legal
Coleta as informações de comunicação (telefone/WhatsApp obrigatório), segurança de acesso (e-mail, senha e confirmação) e, condicionalmente para estudantes menores de 18 anos, os dados obrigatórios do responsável civil.

```mermaid
flowchart TD
    A["Início: Etapa 2"] --> B["Preenchimento: E-mail, Senha e Confirmação"]
    B --> C["Preenchimento: Telefone / WhatsApp (obrigatório)"]
    C --> I{"Estudante menor de 18 anos? (Idade da Etapa 1)"}
    I -->|Sim| J["Exibição Obrigatória dos Campos do Responsável: \n Nome, CPF, Telefone e E-mail (opcional)"]
    I -->|Não| K["Prossegue diretamente para validação"]
    J --> L["Validação Matemática do CPF do Responsável"]
    L --> M["Validação de Unicidade de E-mail e Força da Senha (RN-AUT-005)"]
    K --> M
    M --> N{"Etapa 2 Válida?"}
    N -->|Sim| O["Persistência de Contato/Credenciais → Avançar para Etapa 3"]
    N -->|Não| P["Exibição de Erros e Alertas"]
    P --> B
```

> [!NOTE]
> O endereço (CEP com auto-preenchimento via ViaCEP) foi consolidado na **Etapa 3**, junto dos dados acadêmicos — conforme o escopo canônico da Etapa 4 do plano de implementação.

---

### 2.3 Etapa 3: Acadêmico e Endereço
Coleta os dados escolares do estudante (com validação dinâmica da série/ano) e o endereço completo via CEP com auto-preenchimento pela API ViaCEP.

```mermaid
flowchart TD
    A["Início: Etapa 3"] --> B["Preenchimento do CEP"]
    B --> C["Consulta Automática à API ViaCEP (timeout 4s)"]
    C --> D{"CEP Encontrado?"}
    D -->|Sim| E["Auto-preenchimento: UF, Cidade, Bairro e Logradouro"]
    D -->|Não| F["Habilita preenchimento manual dos campos de endereço"]
    E --> G["Preenchimento do Número e Seleção da Rede de Ensino (Pública / Privada)"]
    F --> G
    G --> H["Preenchimento do Nome da Instituição + Seleção Dinâmica da Série / Ano"]
    H --> I["Submissão da Validação da Etapa 3"]
    I --> J{"Formulário Válido?"}
    J -->|Sim| K["Finalização Atômica do Cadastro → Sessão criada → Dashboard de Matérias"]
    J -->|Não| L["Destaque dos Campos Incorretos"]
    L --> B
```

> [!IMPORTANT]
> A prova de proficiência (CAT) **não é disparada no cadastro**. A sessão CAT é criada apenas quando o aluno entra em uma matéria pela primeira vez (motor CAT implementado na Etapa 7 do plano de implementação).

