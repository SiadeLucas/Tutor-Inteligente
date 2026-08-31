---
title: Exercícios - 1. Motor Adaptativo (CAT)
type: module
status: draft
related:
  - modules/exercicios/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 1. Parametrização do Motor Adaptativo (CAT) e TRI

### 1.1 Modelo Psicométrico de TRI

#### RN-EXE-001: Modelo Logístico de 2/3 Parâmetros
A probabilidade de um aluno com nível de habilidade $\theta$ acertar um item $i$ é calculada por:

$$P_i(\theta) = c_i + \frac{1 - c_i}{1 + e^{-D a_i (\theta - b_i)}}$$

Onde:
- $\theta \in [-3.0, +3.0]$: Nível de proficiência estimado do aluno.
- $b_i \in [-3.0, +3.0]$: Índice de dificuldade do item.
- $a_i \in [0.5, 2.5]$: Índice de discriminação do item.
- $c_i \in [0.0, 0.25]$: Parâmetro de acerto casual (chute), nulo para respostas numéricas ($c_i = 0$).
- $D = 1.7$: Fator de escala métrico.

#### RN-EXE-002: Seleção por Máxima Informação de Fisher
- A cada iteração do CAT, o motor deve selecionar do banco de itens disponíveis aquele que apresentar o maior valor de Informação de Fisher $I_i(\theta)$ para o $\theta$ atual do estudante.
- Devem ser evitadas repetições de itens já respondidos pelo aluno em tentativas anteriores.

#### RN-EXE-003: Estimador de Proficiência (EAP / MLE)
- A estimativa contínua de habilidade deve utilizar o método Bayesiano **EAP (Expected A Posteriori)** durante o teste para garantir estabilidade mesmo com sequências de apenas acertos ou apenas erros.
- A distribuição a priori adotada é normal padrão $\mathcal{N}(0, 1)$.

#### RN-EXE-004: Critério de Parada Híbrido
O teste adaptativo deve encerrar quando qualquer uma das seguintes condições for satisfeita:
1. O aluno responder o limite máximo de **20 questões**.
2. O aluno responder no mínimo **12 questões** E o erro padrão da estimativa for $\text{SE}(\theta) \le 0.30$.

#### RN-EXE-005: Mapeamento de Níveis de Domínio
Ao finalizar o CAT, o $\theta$ consolidado é convertido para a escala qualitativa:

| Nível de Proficiência | Intervalo de Habilidade ($\theta$) |
|:---|:---|
| **Básico** | $\theta < -0.50$ |
| **Intermediário** | $-0.50 \le \theta \le +1.00$ |
| **Avançado** | $\theta > +1.00$ |

#### RN-EXE-006: Granularidade por Área/Volume
- A pontuação de proficiência do CAT é calculada e persistida **de forma independente para cada uma das 4 Grandes Áreas** e seus respectivos volumes da coleção Iezzi.
