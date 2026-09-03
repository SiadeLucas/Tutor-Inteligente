---
title: Autenticação - 3. Sessão e Dispositivos
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 3. Política de Sessão Única e Tokens JWT

### 3.1 Segurança de Conexão

#### RN-AUT-011: Regra de 1 Dispositivo Concorrente por Aluno
- Cada conta de aluno permite apenas **1 sessão ativa por vez**.
- Caso o usuário realize login em um segundo dispositivo, a sessão anterior é imediatamente invalidada no servidor para coibir o rateio de contas pagas.

#### RN-AUT-012: Modal de Desconexão e Salvamento de Rascunho
- No instante em que um segundo aparelho conecta, a tela do dispositivo anterior congela com um backdrop escuro e exibe o modal explicativo:
  > *"Sua conta foi conectada em outro dispositivo às HH:MM. Se não foi você, recomendamos redefinir sua senha imediatamente."*
- **Persistência de Progresso**: As respostas de exercícios já assinaladas e o tempo líquido de estudo até o segundo exato são persistidos no banco de dados, evitando perda de trabalho caso o próprio estudante tenha trocado de aparelho.
- **Pausa do Cronômetro**: O cronômetro de estudo é pausado na hora para não inflar artificialmente as métricas de tempo líquido no Painel do Professor.

#### RN-AUT-013: Estrutura de Tokens JWT e Renovação Silenciosa (Silent Refresh)
- A autenticação utiliza par de tokens:
  - **Access Token**: Validade de 15 minutos, trafegado no header `Authorization: Bearer`.
  - **Refresh Token**: Validade de 7 dias, armazenado exclusivamente em cookie seguro `HTTP-Only`, `Secure` e `SameSite=Strict`.
- **Renovação Silenciosa (Zero Interrupção)**: O frontend possui um interceptor HTTP que renova o Access Token automaticamente em background antes de expirar. O aluno realiza Provas Adaptativas (CAT) e sessões longas de estudo sem qualquer flicker, travamento de tela ou perda de foco.
- Caso o Refresh Token expire por inatividade prolongada (7 dias), o sistema apresenta um modal suave de confirmação de credenciais preservando todas as respostas da tela.

#### RN-AUT-014: Rotação Automática de Refresh Token
- A cada renovação de Access Token, o Refresh Token utilizado é invalidado e um novo é emitido, protegendo contra reutilização de tokens interceptados.

#### RN-AUT-015: Logout Remoto e Encerramento Global
- O usuário pode, a partir da tela de Perfil, solicitar "Desconectar de todos os dispositivos", invalidando todos os tokens e sessões ativas no banco.
