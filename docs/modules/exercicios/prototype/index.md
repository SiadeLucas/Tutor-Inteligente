---
title: Exercícios - Protótipos de Código e Algoritmos
type: module
status: draft
related:
  - modules/exercicios/index.md
  - modules/exercicios/prototype/schemas.md
  - modules/exercicios/prototype/cat-engine.md
  - modules/exercicios/prototype/sympy-validator.md
  - modules/exercicios/prototype/endpoints.md
last_updated: "2026-09-02"
updated_by: claude
---

<!-- ai-summary
Hub de protótipos de código do módulo de Exercícios / Avaliações.
Implementações técnicas de referência em Python 3.11 (FastAPI, SymPy, NumPy/SciPy) e TypeScript:
1. Schemas e DTOs (Pydantic v2).
2. Motor Psicométrico CAT (TRI 2PL/3PL, Fisher Info, Estimador EAP).
3. Validador Determinístico de Álgebra e Gerador de Questões Gêmeas com SymPy.
4. Endpoints REST da API FastAPI.
-->

# Exercícios — Protótipos de Código e Algoritmos

Esta seção reúne as implementações de referência e o código-fonte executável do núcleo de avaliação adaptativa e computação simbólica da plataforma **Tutor Inteligente**.

---

## Estrutura dos Protótipos Técnicos

| Documento | Escopo Técnico | Linguagem / Stack |
|:---|:---|:---:|
| [1. Schemas & DTOs](schemas.md) | Modelos de dados de entrada/saída, validação de itens KaTeX e submissão ponderada | **Pydantic v2 / TypeScript** |
| [2. Motor Psicométrico CAT](cat-engine.md) | Equações da TRI (2PL/3PL), seleção por Máxima Informação de Fisher e estimativa EAP | **Python / NumPy / SciPy** |
| [3. Validador Algébrico SymPy](sympy-validator.md) | Parser LaTeX, checagem determinística de gabarito e mutação paramétrica de Questões Gêmeas | **Python / SymPy** |
| [4. Endpoints da API FastAPI](endpoints.md) | Rotas REST assíncronas para submissão, sessões adaptativas e geração de gêmeas | **FastAPI / Python** |

---

## Fluxo de Execução Técnica

```mermaid
sequenceDiagram
    autonumber
    actor Aluno as 📱 Aluno (Frontend Next.js)
    participant API as 🚀 FastAPI Router
    participant CAT as 🧠 CAT Engine (TRI)
    participant SymPy as 📐 SymPy Engine
    participant DB as 🐘 PostgreSQL 16

    Note over Aluno,API: 1. Resolução com 2ª Chance
    Aluno->>API: POST /api/v1/exercicios/submeter (tentativa: 1)
    API->>DB: Registra tentativa e calcula score (1.0 vs 0.5)
    API-->>Aluno: Retorno com feedback ou pista socrática
    
    Note over Aluno,API: 2. Recuperação com Questão Gêmea
    Aluno->>API: POST /api/v1/exercicios/gerar-gemea (item_matriz_id)
    API->>SymPy: Gera mutação paramétrica e valida gabarito determinístico
    SymPy-->>API: Item validado (tolerância ±0.01)
    API->>DB: Salva na tabela itens_exercicios (origem: gemea_ia)
    API-->>Aluno: Retorna nova questão em KaTeX

    Note over Aluno,API: 3. Prova Adaptativa (CAT)
    Aluno->>API: POST /api/v1/cat/responder
    API->>CAT: Atualiza Theta via Bayes EAP e calcula Fisher Info
    CAT-->>API: Próximo item ótimo selecionado ou encerra teste
    API-->>Aluno: Retorna próximo item ou Dossiê de Proficiência
```
