---
title: Progresso - Protótipos de Código e Analytics
type: module
status: draft
related:
  - modules/progresso/index.md
  - modules/progresso/prototype/schemas.md
  - modules/progresso/prototype/theta-updater.md
  - modules/progresso/prototype/heatmap-service.md
  - modules/progresso/prototype/pdf-generator.md
  - modules/progresso/prototype/endpoints.md
last_updated: "2026-09-03"
updated_by: claude
---

<!-- ai-summary
Hub de protótipos de código do módulo de Progresso / Desempenho.
Implementações técnicas de referência em Python 3.11 (FastAPI, NumPy/SciPy, ReportLab) e TypeScript:
1. Schemas e DTOs de Métricas Tridimensionais e Heatmap (Pydantic v2).
2. Algoritmo de Micro-Ajuste Bayesiano de Theta e Taxa Ponderada de Acertos.
3. Agregador do Heatmap de Domínio e Detector dos Top 3 Tópicos Críticos com Hub de Ação.
4. Emissor de Boletim Oficial em PDF de Alta Resolução com ReportLab.
5. Endpoints REST da API FastAPI.
-->

# Progresso — Protótipos de Código e Analytics

Esta seção reúne as implementações de referência e o código-fonte executável do subsistema de **analytics pedagógico**, **calibragem bayesiana contínua da TRI ($\theta$)**, consolidação do **Heatmap de Domínio dos 11 Volumes** e emissão de **boletins escolares em PDF vetorial** da plataforma **Tutor Inteligente**.

---

## Estrutura dos Protótipos Técnicos

| Documento | Escopo Técnico | Linguagem / Stack |
|:---|:---|:---:|
| [1. Schemas & DTOs](schemas.md) | Contratos tipados de progresso geral, nós do heatmap, dados do radar e tipos TypeScript | **Pydantic v2 / TypeScript** |
| [2. Calibragem Contínua de Theta](theta-updater.md) | Algoritmo de micro-ajuste estocástico do $\theta$ a cada item respondido e pontuação ponderada | **Python / NumPy / SciPy** |
| [3. Agregador Heatmap & Top 3](heatmap-service.md) | Mapeamento dos 4 estados de cores, completude e Hub de Ação nos 3 tópicos mais frágeis | **Python / SQLAlchemy** |
| [4. Gerador de Boletim em PDF](pdf-generator.md) | Emissão em sub-100ms de relatório oficial com ReportLab sem dependências pesadas de SO | **Python / ReportLab** |
| [5. Endpoints da API FastAPI](endpoints.md) | Rotas assíncronas para consumo de dashboards, séries temporais e download do PDF | **FastAPI / Python** |

---

## Circuito Fechado de Métricas e Feedback Contínuo

```mermaid
sequenceDiagram
    autonumber
    actor Aluno as 📱 Aluno
    participant API as 🚀 FastAPI Router
    participant Service as 📊 Progress Service
    participant PDF as 📄 ReportLab Engine
    participant DB as 🐘 PostgreSQL (historico_theta / heatmap)

    Note over Aluno,API: 1. Conclusão de Exercício (Micro-Ajuste Imediato)
    Aluno->>API: Submete resposta da bateria
    API->>Service: Calcula score ponderado (1.0 vs 0.5) e resíduo TRI
    Service->>DB: Atualiza theta_estimado na tabela historico_theta
    Service->>DB: Recalcula cor do nó na tabela heatmap_dominio
    API-->>Aluno: Feedback visual imediato na barra de domínio

    Note over Aluno,API: 2. Consulta do Hub de Ação (Top 3 Críticos)
    Aluno->>API: GET /api/v1/progresso/top-criticos
    API->>Service: Filtra capítulos com taxa < 75%
    Service-->>API: Retorna os 3 gargalos com opções (Revisar Teoria vs Praticar Reforço)
    API-->>Aluno: Renderiza cards interativos de remediação

    Note over Aluno,API: 3. Download do Boletim Oficial em PDF
    Aluno->>API: GET /api/v1/progresso/boletim-pdf
    API->>PDF: Compila dados do aluno, Radar e série temporal em PDF vetorial
    PDF-->>API: Buffer binário de alta resolução
    API-->>Aluno: Download instantâneo (Content-Disposition: attachment)
```
