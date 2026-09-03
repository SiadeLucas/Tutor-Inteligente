---
title: Autenticação - Protótipos de Código e Segurança
type: module
status: draft
related:
  - modules/autenticacao/index.md
  - modules/autenticacao/prototype/schemas.md
  - modules/autenticacao/prototype/session-manager.md
  - modules/autenticacao/prototype/jwt-service.md
  - modules/autenticacao/prototype/endpoints.md
last_updated: "2026-09-03"
updated_by: claude
---

<!-- ai-summary
Hub de protótipos de código do módulo de Autenticação e Segurança.
Implementações técnicas de referência em Python 3.11 (FastAPI, PyJWT, Argon2id) e TypeScript:
1. Schemas e DTOs (Pydantic v2).
2. Gestão de Sessão Única e Heartbeat (Desconexão Concorrente).
3. Serviço de Tokens JWT e Rotação de Refresh Token (Silent Refresh).
4. Endpoints REST da API FastAPI.
-->

# Autenticação — Protótipos de Código e Segurança

Esta seção reúne as implementações de referência e o código-fonte executável do subsistema de segurança, autenticação híbrida (E-mail/CPF), controle de **sessão única concorrente** e tokens criptográficos da plataforma **Tutor Inteligente**.

---

## Estrutura dos Protótipos Técnicos

| Documento | Escopo Técnico | Linguagem / Stack |
|:---|:---|:---:|
| [1. Schemas & DTOs](schemas.md) | Contratos tipados de login flexível, par de tokens, recuperação de senha e tipos TypeScript | **Pydantic v2 / TypeScript** |
| [2. Gestão de Sessão Única](session-manager.md) | Invalidação atômica de sessões anteriores, heartbeat de 30s e salvamento de rascunho | **Python / FastAPI / SQLAlchemy** |
| [3. Serviço JWT & Silent Refresh](jwt-service.md) | Emissão de Access Token (15 min), Refresh Token seguro (7 dias em cookie HTTP-Only) e rotação | **Python / PyJWT / Cryptography** |
| [4. Endpoints da API FastAPI](endpoints.md) | Rotas assíncronas de login, refresh, logout, heartbeat e link mágico | **FastAPI / Python** |

---

## Fluxo de Autenticação e Desconexão Concorrente

```mermaid
sequenceDiagram
    autonumber
    actor Aluno1 as 💻 Aluno (Dispositivo 1)
    actor Aluno2 as 📱 Aluno (Dispositivo 2)
    participant API as 🚀 FastAPI Auth API
    participant DB as 🐘 PostgreSQL (sessoes_ativas)

    Aluno1->>API: POST /api/v1/auth/login (E-mail ou CPF + Senha)
    API->>DB: Cria Sessão A (ativa=true)
    API-->>Aluno1: Retorna Access Token (15 min) + Cookie Refresh Token (7 dias)
    
    Note over Aluno1,API: Dispositivo 1 estuda e envia Heartbeat a cada 30s

    Note over Aluno2,API: Login do mesmo aluno em um segundo aparelho
    Aluno2->>API: POST /api/v1/auth/login (Credenciais corretas)
    API->>DB: Revoga Sessão A (ativa=false) e Cria Sessão B (ativa=true)
    API-->>Aluno2: Sessão B iniciada com sucesso

    Note over Aluno1,API: Detecção Híbrida de Concorrência
    Aluno1->>API: GET /api/v1/auth/heartbeat (Sessão A)
    API-->>Aluno1: Erro 401 Unauthorized: {"detail": "CONCURRENT_SESSION_REVOKED"}
    
    Note over Aluno1: 1. Congela tela com modal explicativo<br/>2. Salva rascunho de respostas preenchidas<br/>3. Pausa cronômetro de estudo
```
