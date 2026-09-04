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

### 2.2 Etapa 2: Contato, Credenciais e Responsável Legal
Coleta as informações de comunicação, segurança de acesso (e-mail, senha e confirmação), localização geográfica por CEP e, condicionalmente para estudantes menores de 18 anos, os dados obrigatórios do responsável civil.

```mermaid
flowchart TD
    A["Início: Etapa 2"] --> B["Preenchimento: E-mail, Senha e Confirmação"]
    B --> C["Preenchimento: Telefone / WhatsApp"]
    C --> D["Preenchimento do CEP"]
    D --> E["Consulta Automática à API ViaCEP"]
    E --> F{"CEP Encontrado?"}
    F -->|Sim| G["Auto-preenchimento: UF, Cidade, Bairro e Logradouro"]
    F -->|Não| H["Habilita preenchimento manual dos campos de endereço"]
    G --> I{"Estudante menor de 18 anos? (Idade da Etapa 1)"}
    H --> I
    I -->|Sim| J["Exibição Obrigatória dos Campos do Responsável: \n Nome, CPF, Telefone e E-mail"]
    I -->|Não| K["Prossegue diretamente para validação"]
    J --> L["Validação Matemática do CPF do Responsável"]
    L --> M["Validação de Unicidade de E-mail e Força da Senha (RN-AUT-005)"]
    K --> M
    M --> N{"Etapa 2 Válida?"}
    N -->|Sim| O["Persistência de Contato/Credenciais → Avançar para Etapa 3"]
    N -->|Não| P["Exibição de Erros e Alertas"]
    P --> B
```

---

### 2.3 Etapa 3: Dados Acadêmicos e Escolaridade
Coleta os dados escolares do estudante com validação dinâmica da série/ano conforme o nível de ensino da matéria selecionada.

```mermaid
flowchart TD
    A["Início: Etapa 3"] --> B["Seleção da Rede de Ensino (Pública / Privada)"]
    B --> C["Preenchimento do Nome da Instituição de Ensino"]
    C --> D["Seleção Dinâmica da Série / Ano"]
    D --> E["Submissão da Validação da Etapa 3"]
    E --> F{"Formulário Válido?"}
    F -->|Sim| G["Finalização Atômica do Cadastro → Disparo da Prova CAT (Etapa 4)"]
    F -->|Não| H["Destaque dos Campos Incorretos"]
    H --> B
```

