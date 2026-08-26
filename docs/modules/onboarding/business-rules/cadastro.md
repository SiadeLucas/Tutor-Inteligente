---
title: Onboarding - 1. Cadastro e Validação
type: module
status: draft
related:
  - modules/onboarding/business-rules/index.md
  - modules/onboarding/business-rules/proficiencia.md
last_updated: "2026-08-26"
updated_by: claude
---

# 1. Cadastro e Validação de Dados

### 1.1 Dados Pessoais e Identificação

#### RN-ONB-001: Validação e Preenchimento por Etapas
Todos os campos sinalizados como obrigatórios devem ser completamente validados antes de liberar a transição para o próximo passo do wizard de cadastro. Erros impedem o avanço e são sinalizados visualmente no campo correspondente.

#### RN-ONB-002: Validação de CPF
- O CPF é submetido ao algoritmo padrão de validação de dígitos verificadores (módulo 11).
- CPFs duplicados (já registrados em contas ativas ou suspensas) são rejeitados com mensagem amigável.
- A validação se aplica de forma idêntica ao CPF do aluno e ao CPF do responsável legal.

#### RN-ONB-004: Validação de Data de Nascimento e Idade
- A data de nascimento deve ser uma data cronológica válida no passado.
- O sistema calcula dinamicamente a idade exata com base na data do cadastro:
  $$\text{Idade} = \text{Data Atual} - \text{Data de Nascimento}$$
- A idade calculada orienta a exibição condicional dos campos de menoridade (vide RN-ONB-005).

#### RN-ONB-007: Foto de Perfil e Avatar Padrão
- O envio de imagem de perfil é opcional na etapa de onboarding.
- Formatos aceitos: JPEG e PNG, com limite máximo de 5 MB por arquivo.
- Caso o aluno não envie imagem, o sistema gera dinamicamente um avatar vetorial com as iniciais do seu primeiro e último nome.

---

### 1.2 Comunicação e Localização

#### RN-ONB-003: Validação e Unicidade de E-mail
- O endereço de e-mail deve respeitar a sintaxe padrão RFC 5322.
- É verificado se o e-mail já existe na base de dados (chave de unicidade).
- Dispara-se um e-mail assíncrono de confirmação, sem bloquear a continuidade imediata do onboarding.

#### RN-ONB-006: Auto-preenchimento por Consulta de CEP
- Ao inserir o CEP válido (8 dígitos), o sistema consulta a API de logradouros (ex: ViaCEP) para preencher automaticamente:
  - **Estado (UF)**
  - **Cidade**
  - **Bairro**
- O usuário mantém permissão para editar os campos caso haja divergência.
- Na indisponibilidade da API externa, os campos são liberados imediatamente para preenchimento manual.

---

### 1.3 Perfil Acadêmico e Menoridade

#### RN-ONB-005: Responsável Legal para Menores de 18 Anos
- Se a idade calculada for **menor que 18 anos**, o formulário torna mandatório o preenchimento de:
  - **Nome Completo do Responsável**
  - **CPF do Responsável** (validado conforme RN-ONB-002)
  - **Telefone/WhatsApp do Responsável**
- Para usuários com **18 anos completos ou mais**, esses campos permanecem ocultos e dispensados.

#### RN-ONB-008: Instituição de Ensino e Autocomplete
- O campo de instituição oferece busca com autocomplete conectada a uma base padronizada de escolas.
- Caso a escola do aluno não conste na lista, é permitido o cadastro em texto livre, armazenando o novo registro para futura curadoria.

#### RN-ONB-009: Série/Ano Dinâmico
- A lista de opções de série/ano é alimentada dinamicamente conforme o nível de ensino selecionado.
- No escopo de Ensino Médio, contempla: 1º Ano, 2º Ano e 3º Ano.
