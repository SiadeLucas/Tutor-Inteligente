---
title: Autenticação - Visão Geral das Regras de Negócio
type: module
status: draft
related:
  - modules/autenticacao/business-rules/regras-credenciais.md
  - modules/autenticacao/business-rules/regras-perfis.md
  - modules/autenticacao/business-rules/regras-sessao.md
  - modules/autenticacao/business-rules/regras-recuperacao.md
last_updated: "2026-09-01"
updated_by: claude
---

# Regras de Negócio de Autenticação — Visão Geral

| Sub-domínio | Descrição | Regras Principais |
|:---|:---|:---|
| [1. Credenciais e Cadastro](regras-credenciais.md) | Validação de CPF, formato de e-mail e requisitos de senha | RN-AUT-001 a RN-AUT-005 |
| [2. Perfis e Permissões](regras-perfis.md) | Separação estrita entre papéis `student` e `teacher` | RN-AUT-006 a RN-AUT-010 |
| [3. Sessão e Dispositivos](regras-sessao.md) | Política de 1 dispositivo concorrente, JWT e expiração | RN-AUT-011 a RN-AUT-015 |
| [4. Recuperação e Antifraude](regras-recuperacao.md) | Link mágico por e-mail, tokens de 15 min e Rate Limiting | RN-AUT-016 a RN-AUT-020 |
