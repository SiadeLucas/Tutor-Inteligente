---
title: Onboarding - Protótipos de Código e Cadastro
type: module
status: draft
related:
  - modules/onboarding/index.md
  - modules/onboarding/prototype/schemas.md
  - modules/onboarding/prototype/cpf-validator.md
  - modules/onboarding/prototype/onboarding-service.md
  - modules/onboarding/prototype/endpoints.md
last_updated: "2026-09-07"
updated_by: buffy
---

<!-- ai-summary
Hub de protótipos de código do módulo de Onboarding.
Implementações técnicas de referência em Python 3.11 (FastAPI, Pydantic v2, SQLAlchemy asyncpg) e TypeScript:
1. Schemas e DTOs do Wizard de Cadastro em 3 Etapas e Menoridade Civil (Pydantic v2).
2. Algoritmo Matemático de Validação de CPF (Módulo 11).
3. Serviço de Criação Atômica de Conta e Abertura da Sessão Única (sem CAT).
4. Endpoints REST da API FastAPI (Validação em Tempo Real, Rascunho Redis e Finalização).
-->

# Onboarding — Protótipos de Código e Cadastro

Esta seção reúne as implementações de referência e o código-fonte executável do subsistema de **cadastro de estudantes em 3 etapas** (wizard sem CAT), cálculo automático de **menoridade civil**, validação algorítmica de **CPF** e persistência de **rascunhos no Redis (TTL 48h)** na plataforma **Tutor Inteligente**. A Prova Diagnóstica CAT é disparada apenas no primeiro acesso do aluno a uma matéria (Etapa 7).

---

## Estrutura dos Protótipos Técnicos

| Documento | Escopo Técnico | Linguagem / Stack |
|:---|:---|:---:|
| [1. Schemas & DTOs](schemas.md) | Contratos tipados de cada etapa do wizard, dados do responsável legal e tipos TypeScript | **Pydantic v2 / TypeScript** |
| [2. Validador de CPF (Módulo 11)](cpf-validator.md) | Algoritmo estrito de dígitos verificadores sem bibliotecas externas pesadas | **Python Puro** |
| [3. Serviço de Cadastro Atômico](onboarding-service.md) | Gravação atômica na tabela `usuarios`, hash de senha e abertura da sessão única (sem CAT) | **Python / SQLAlchemy / Argon2id** |
| [4. Endpoints da API FastAPI](endpoints.md) | Rotas assíncronas para validação em tempo real de cada passo e finalização | **FastAPI / Python** |

---

## Fluxo de Execução do Wizard

```mermaid
sequenceDiagram
    autonumber
    actor Aluno as 📱 Aluno (Frontend Next.js)
    participant Local as 💾 localStorage
    participant API as 🚀 FastAPI Router
    participant Redis as ⚡ Redis (rascunho 48h)
    participant DB as 🐘 PostgreSQL (usuarios)

    Note over Aluno,Local: Etapas 1, 2 e 3: Validações Rápidas
    Aluno->>API: POST /api/v1/onboarding/validar-etapa-{1,2,3}
    API-->>Aluno: Validação OK (CPF/E-mail livres de duplicidade)
    Aluno->>API: POST /api/v1/onboarding/salvar-rascunho (X-Draft-Session-ID)
    API->>Redis: setex onboarding_draft:{id} TTL 48h

    Note over Aluno,DB: Submissão Atômica (sem CAT)
    Aluno->>API: POST /api/v1/onboarding/finalizar-cadastro (payload completo)
    API->>DB: Inserção atômica na tabela usuarios (com menoridade calculada)
    API->>DB: Cria sessão única ativa (SessionManager) + hash do refresh token
    API->>Redis: Deleta rascunho (onboarding_draft:{id})
    API-->>Aluno: Access Token + Refresh Token em cookie HTTP-Only
    Aluno->>Local: Limpa rascunho e redireciona ao dashboard de matérias
```
