---
title: Autenticação - 1. Credenciais e Cadastro
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 1. Validação de Credenciais e Políticas de Senha

### 1.1 Regras de Identificação

#### RN-AUT-001: Identificador Flexível (E-mail ou CPF)
- O usuário pode efetuar login informando tanto seu endereço de e-mail quanto seu CPF (com ou sem pontuação).

#### RN-AUT-002: Validação de Algoritmo de CPF
- Todo CPF cadastrado passa pela validação algorítmica dos dois dígitos verificadores da Receita Federal. CPFs inválidos são recusados no momento do cadastro.

#### RN-AUT-003: Unicidade de E-mail e CPF
- Não é permitido o cadastro de contas duplicadas com o mesmo e-mail ou mesmo CPF.

#### RN-AUT-004: Política de Complexidade de Senha
- A senha deve possuir no mínimo 8 caracteres, contendo ao menos uma letra e um número.

#### RN-AUT-005: Armazenamento Criptográfico Seguro
- As senhas são obrigatoriamente armazenadas utilizando função de derivação de chave segura (`bcrypt` com fator de custo 12 ou `Argon2id`) com salt único gerado por usuário.
