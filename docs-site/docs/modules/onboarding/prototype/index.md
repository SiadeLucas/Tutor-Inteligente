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
last_updated: "2026-09-03"
updated_by: claude
---

<!-- ai-summary
Hub de protótipos de código do módulo de Onboarding.
Implementações técnicas de referência em Python 3.11 (FastAPI, Pydantic v2, SQLAlchemy asyncpg) e TypeScript:
1. Schemas e DTOs das 4 Etapas do Wizard e Menoridade Civil (Pydantic v2).
2. Algoritmo Matemático de Validação de CPF (Módulo 11).
3. Serviço de Criação Atômica de Conta e Inicialização da Prova CAT.
4. Endpoints REST da API FastAPI (Validação em Tempo Real e Finalização).
-->

# Onboarding — Protótipos de Código e Cadastro

Esta seção reúne as implementações de referência e o código-fonte executável do subsistema de **cadastro de estudantes em 4 etapas**, cálculo automático de **menoridade civil**, validação algorítmica de **CPF** e transição atômica para a **Prova Diagnóstica CAT de Entrada** na plataforma **Tutor Inteligente**.

---

## Estrutura dos Protótipos Técnicos

| Documento | Escopo Técnico | Linguagem / Stack |
|:---|:---|:---:|
| [1. Schemas & DTOs](schemas.md) | Contratos tipados de cada etapa do wizard, dados do responsável legal e tipos TypeScript | **Pydantic v2 / TypeScript** |
| [2. Validador de CPF (Módulo 11)](cpf-validator.md) | Algoritmo estrito de dígitos verificadores sem bibliotecas externas pesadas | **Python Puro** |
| [3. Serviço de Cadastro Atômico](onboarding-service.md) | Gravação atômica na tabela `usuarios`, hash de senha e inicialização da Prova CAT | **Python / SQLAlchemy / Argon2id** |
| [4. Endpoints da API FastAPI](endpoints.md) | Rotas assíncronas para validação em tempo real de cada passo e finalização | **FastAPI / Python** |

---

## Fluxo de Execução do Wizard

```mermaid
sequenceDiagram
    autonumber
    actor Aluno as 📱 Aluno (Frontend Next.js)
    participant Local as 💾 localStorage
    participant API as 🚀 FastAPI Router
    participant DB as 🐘 PostgreSQL (usuarios)
    participant CAT as 🧠 CAT Engine (TRI)

    Note over Aluno,Local: Etapas 1, 2 e 3: Validações Rápidas
    Aluno->>API: POST /api/v1/onboarding/validar-etapa (etapa: 1 | 2 | 3)
    API-->>Aluno: Validação OK (CPF/E-mail livres de duplicidade)
    Aluno->>Local: Salva rascunho temporário do wizard

    Note over Aluno,CAT: Etapa 4: Submissão Atômica e Entrada no CAT
    Aluno->>API: POST /api/v1/onboarding/finalizar-cadastro (Payload completo dos 4 passos)
    API->>DB: Inserção atômica na tabela usuarios (com menoridade calculada)
    API->>DB: Cria sessão inicial autorizada
    API->>CAT: Instancia sessão de Prova Diagnóstica (12 a 20 questões)
    API-->>Aluno: Retorna Tokens JWT + Primeira questão da Prova CAT
    Aluno->>Local: Limpa rascunho temporário
```
