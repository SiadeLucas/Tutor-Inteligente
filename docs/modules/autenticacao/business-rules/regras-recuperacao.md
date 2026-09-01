---
title: Autenticação - 4. Recuperação e Antifraude
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 4. Link Mágico e Proteção contra Força Bruta

### 4.1 Redefinição Segura de Credenciais

#### RN-AUT-016: Recuperação via Link Mágico por E-mail
- A recuperação de senha ocorre por envio de um link com botão seguro para o e-mail cadastrado, sem necessidade de digitação de código numérico.

#### RN-AUT-017: Validade e Uso Único do Token de Recuperação
- O link mágico contém um token criptográfico que expira em exatamente **15 minutos** ou imediatamente após a primeira utilização com sucesso.

#### RN-AUT-018: Invalidação de Sessões Ativas após Troca de Senha
- Assim que uma nova senha é cadastrada com sucesso via link mágico, todas as sessões anteriores ativas em qualquer dispositivo são encerradas imediatamente.

#### RN-AUT-019: Rate Limiting Anti-Força Bruta
- O sistema bloqueia novas tentativas de login pelo período de **15 minutos** após 5 erros consecutivos de senha para o mesmo IP ou conta.

#### RN-AUT-020: Auditoria e Logs de Segurança
- Eventos de login bem-sucedido, falhas repetidas de autenticação, solicitações de link mágico e alterações de senha são registrados com timestamp, IP e User-Agent para fins de auditoria.
