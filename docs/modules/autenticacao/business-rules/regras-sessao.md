---
title: Autenticação - 3. Sessão e Dispositivos
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 3. Política de Sessão Única e Tokens JWT

### 3.1 Segurança de Conexão

#### RN-AUT-011: Regra de 1 Dispositivo Concorrente por Aluno
- Cada conta de aluno permite apenas **1 sessão ativa por vez**.
- Caso o usuário realize login em um segundo dispositivo, a sessão anterior é imediatamente invalidada no servidor.

#### RN-AUT-012: Mensagem Amigável de Desconexão
- Ao ser desconectado pela entrada em outro dispositivo, o usuário recebe a notificação: *"Sua conta foi conectada em outro dispositivo. Se não foi você, recomendamos redefinir sua senha."*

#### RN-AUT-013: Estrutura de Tokens JWT
- A autenticação utiliza par de tokens:
  - **Access Token**: Validade de 15 minutos, trafegado no header `Authorization: Bearer`.
  - **Refresh Token**: Validade de 7 dias, armazenado exclusivamente em cookie `HTTP-Only`, `Secure` e `SameSite=Strict`.

#### RN-AUT-014: Rotação Automática de Refresh Token
- A cada renovação de Access Token, o Refresh Token utilizado é invalidado e um novo é emitido, protegendo contra reutilização de tokens interceptados.

#### RN-AUT-015: Logout Remoto e Encerramento Global
- O usuário pode, a partir da tela de Perfil, solicitar "Desconectar de todos os dispositivos", invalidando todos os tokens e sessões ativas no banco.
