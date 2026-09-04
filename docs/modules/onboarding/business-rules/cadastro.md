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

### 1.1 Etapa 1: Dados Pessoais e Identificação

#### RN-ONB-001: Validação e Preenchimento por Etapas
Todos os campos sinalizados como obrigatórios devem ser completamente validados antes de liberar a transição para o próximo passo do wizard de cadastro. Erros impedem o avanço e são sinalizados visualmente no campo correspondente.

#### RN-ONB-002: Validação de CPF (Algoritmo e Unicidade)
- O CPF é submetido ao algoritmo padrão de validação de dígitos verificadores (módulo 11).
- CPFs duplicados (já registrados em contas ativas ou suspensas) são rejeitados com status HTTP 409 e mensagem amigável.
- A validação se aplica de forma idêntica ao CPF do aluno e ao CPF do responsável legal.

#### RN-ONB-004: Validação de Data de Nascimento e Idade
- A data de nascimento deve ser uma data cronológica válida no passado.
- O sistema calcula dinamicamente a idade exata com base na data do cadastro:
  $$\text{Idade} = \text{Data Atual} - \text{Data de Nascimento}$$
- A idade calculada orienta a exibição condicional obrigatória dos campos de responsável legal na Etapa 2 (vide RN-ONB-005).

#### RN-ONB-007: Foto de Perfil e Avatar Padrão
- O envio de imagem de perfil é opcional na etapa de onboarding.
- Formatos aceitos: JPEG e PNG, com limite máximo de 5 MB por arquivo.
- Caso o aluno não envie imagem, o sistema gera dinamicamente um avatar vetorial com as iniciais do seu primeiro e último nome.

---

### 1.2 Etapa 2: Contato, Credenciais e Responsável Legal

#### RN-ONB-003: Validação de E-mail, Unicidade e Criação de Senha
- O endereço de e-mail deve respeitar a sintaxe padrão RFC 5322 e ser único na plataforma (HTTP 409 em caso de duplicidade).
- A senha deve conter no mínimo 8 caracteres, validada contra confirmação de senha idêntica e armazenada sob hash Argon2id (RN-AUT-005).
- Dispara-se um e-mail assíncrono de boas-vindas sem bloquear a continuidade imediata do onboarding.

#### RN-ONB-005: Responsável Legal para Menores de 18 Anos (Condicional)
- Se a idade calculada na Etapa 1 for **menor que 18 anos**, a Etapa 2 torna mandatório o preenchimento de:
  - **Nome Completo do Responsável**
  - **CPF do Responsável** (validado conforme RN-ONB-002)
  - **Telefone/WhatsApp do Responsável**
  - **E-mail do Responsável** (opcional)
- Para usuários com **18 anos completos ou mais**, esses campos permanecem ocultos e dispensados.

#### RN-ONB-006: Auto-preenchimento por Consulta de CEP e Endereço
- Ao inserir o CEP válido (8 dígitos), o sistema consulta a API ViaCEP para preencher automaticamente:
  - **Estado (UF)**
  - **Cidade**
  - **Bairro**
  - **Logradouro**
- O usuário mantém permissão para editar os campos caso haja divergência.
- Na indisponibilidade da API externa (timeout 4s), os campos são liberados imediatamente para preenchimento manual.

---

### 1.3 Etapa 3: Perfil Acadêmico e Escolaridade

#### RN-ONB-008: Instituição de Ensino e Rede
- Coleta obrigatoriamente a rede de ensino (**Pública** ou **Privada**) para consolidação das métricas demográficas docentes.
- O campo de instituição oferece busca com autocomplete conectada a uma base padronizada de escolas (preenchimento opcional).
- Caso a escola do aluno não conste na lista, é permitido o cadastro em texto livre.

#### RN-ONB-009: Validação Dinâmica de Série/Ano
- A lista de opções de série/ano é alimentada dinamicamente pelo backend conforme o nível de ensino da disciplina selecionada (Ensino Médio: 1º, 2º ou 3º Ano; Fundamental: 6º a 9º Ano; Superior/Outro).

