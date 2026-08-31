---
title: Exercícios - 1. Motor Adaptativo (CAT)
type: module
status: draft
related:
  - modules/exercicios/flow/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 1. Motor Adaptativo (Computerized Adaptive Testing)

### 1.1 Ciclo de Execução do CAT

```mermaid
flowchart TD
    A["Início do Teste Adaptativo"] --> B["Inicializa Estimativa de Habilidade: \n Theta_0 = 0.0, Erro Padrão SE = 1.0"]
    B --> C["Busca no Banco o Item que Maximiza a Informação de Fisher I(Theta)"]
    C --> D["Apresenta Questão ao Aluno"]
    D --> E["Aluno Seleciona Alternativa ou Insere Valor Numérico"]
    E --> F["Sistema Avalia Resposta: Correto (1) ou Incorreto (0)"]
    F --> G["Atualiza Habilidade Estimada (Theta) via EAP / MLE"]
    G --> H["Recalcula Erro Padrão SE(Theta) e Contabiliza Itens Respondidos (N)"]
    H --> I{"Critério de Parada: \n (N >= 12 e SE <= 0.30) ou N == 20?"}
    I -->|Não| C
    I -->|Sim| J["Finaliza Teste e Mapeia Theta para Nível: \n Básico, Intermediário ou Avançado"]
    J --> K["Exibe Relatório Diagnóstico com Gráfico Radar"]
```

### 1.2 Curva de Informação do Item (Fisher Information)

O algoritmo busca sempre o item $i$ que fornece a máxima informação no ponto $\theta$:

$$I_i(\theta) = \frac{D^2 a_i^2 (1 - c_i) P_i(\theta) [1 - P_i(\theta)]}{[P_i(\theta) - c_i]^2}$$
