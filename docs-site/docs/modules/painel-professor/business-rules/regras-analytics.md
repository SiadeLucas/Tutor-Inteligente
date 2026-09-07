---
title: Painel do Professor - 1. Analytics e Demografia
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 1. Analytics, Agregação e Cruzamento Demográfico

### 1.1 Regras de Processamento de Indicadores

#### RN-PRF-001: Controle de Acesso Restrito (Role Professor)
- Apenas usuários autenticados com o perfil `role = "professor"` ou `role = "admin"` possuem autorização para visualizar dados consolidados e acessar o Painel do Professor.

#### RN-PRF-002: Filtros Globais Dinâmicos
- Os filtros de período, volume do Iezzi, estado/cidade e instituição devem operar de forma cumulativa e atualizar todos os gráficos e tabelas do painel sem necessidade de recarregar a página.

#### RN-PRF-003: Agregação Geográfica por CEP/Município
- As métricas regionais utilizam os dados de endereço preenchidos no Onboarding para agrupar o desempenho por Unidade Federativa (UF), Região Geográfica e Município.

#### RN-PRF-004: Distribuição Qualitativa do CAT
- A distribuição de proficiência divide os alunos nas 3 faixas oficiais da TRI:
  - **Básico**: $\theta < -0.50$
  - **Intermediário**: $-0.50 \le \theta \le +1.00$
  - **Avançado**: $\theta > +1.00$

#### RN-PRF-005: Ranking Institucional
- Escolas com mais de 5 alunos cadastrados são ranqueadas pela média de proficiência ($\bar{\theta}$) e taxa de acerto nas listas do Iezzi, com segmentação entre rede pública e privada.
