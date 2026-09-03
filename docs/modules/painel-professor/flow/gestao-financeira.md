---
title: Painel do Professor - 4. Gestão Financeira
type: module
status: draft
related:
  - modules/painel-professor/flow/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 4. Gestão Financeira e Controle de Matrículas

### 4.1 Acompanhamento de Assinaturas e Acessos

```mermaid
flowchart TD
    A["Professor acessa Aba Financeira"] --> B["Visualização de Receita Mensal (MRR) e Vendas Totais"]
    
    B --> C["Tabela de Status de Matrículas: Ativas, Inadimplentes e Canceladas"]
    
    C --> D{"Auditoria e Gestão Administrativa"}
    D -->|"Consultar Vigência"| E["Verifica período restante de 365 dias"]
    D -->|"Solicitar Estorno (CDC 7 dias)"| F["Processa estorno administrativo legal"]
    D -->|"Suspender por Inadimplência"| G["Transição automática para status past_due"]
    
    B --> H["Extrato Detalhado de Cobranças (PIX e Cartão de Crédito)"]
```
