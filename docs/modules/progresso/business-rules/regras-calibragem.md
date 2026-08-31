---
title: Progresso - 2. Calibragem de Proficiência
type: module
status: draft
related:
  - modules/progresso/business-rules/index.md
last_updated: "2026-08-31"
updated_by: claude
---

# 2. Calibragem Contínua e Integração com CAT

### 2.1 Dinâmica de Atualização de Nível

#### RN-PRG-006: Micro-Ajuste Bayesiano Diário
- Cada lista de fixação ou treino de reforço ajusta incrementalmente o $\theta$ da respectiva área:
  - Acerto de questão difícil ($b > \theta$): incremento proporcional à discriminação $a$.
  - Erro em questão fácil ($b < \theta$): decremento proporcional.
- O fator de amortecimento $\alpha = 0.15$ evita oscilações bruscas no nível por variações diárias pontuais.

#### RN-PRG-007: Prova Adaptativa CAT de Marco Oficial
- A Prova CAT formal (disponível com cooldown de 7 dias) recalibra o $\theta$ com peso integral (100%), estabelecendo um novo marco oficial de proficiência.

#### RN-PRG-008: Preservação de Histórico de Evolução
- Todos os valores de $\theta$ são versionados com timestamp, permitindo traçar a série histórica de evolução temporal do aluno.

#### RN-PRG-009: Mapeamento Visual de Faixas de Habilidade
- Os níveis de proficiência exibidos na interface seguem os thresholds:
  - **Básico**: $\theta < -0.50$
  - **Intermediário**: $-0.50 \le \theta \le +1.00$
  - **Avançado**: $\theta > +1.00$

#### RN-PRG-010: Independência entre Volumes
- O progresso em um volume específico do Iezzi não reduz artificialmente o $\theta$ de outro volume não relacionado.
