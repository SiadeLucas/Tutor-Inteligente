---
title: Progresso - 3. Heatmap e Radar
type: module
status: draft
related:
  - modules/progresso/business-rules/index.md
last_updated: "2026-08-31"
updated_by: claude
---

# 3. Parametrização do Heatmap do Iezzi e Gráfico Radar

### 3.1 Regras Visuais do Heatmap de Domínio

#### RN-PRG-011: Estrutura da Matriz de Capítulos dos 11 Volumes
O Heatmap exibe todos os capítulos dos 11 volumes categorizados em cores:

| Faixa de Taxa de Acertos | Nível de Maestria | Cor no Heatmap |
|:---|:---|:---|
| 0% a 49% | Crítico / Não Iniciado | 🔴 Vermelho |
| 50% a 74% | Em Desenvolvimento | 🟡 Amarelo |
| 75% a 100% | Consolidado / Avançado | 🟢 Verde |

#### RN-PRG-012: Critério de Desbloqueio de Cor do Capítulo
- Um capítulo só é colorido em Amarelo ou Verde após a submissão de no mínimo 3 exercícios correspondentes àquele capítulo. Antes disso, permanece em estado neutro/cinza.

#### RN-PRG-013: Gráfico Radar Multiaxial
- O Gráfico Radar possui 4 eixos principais correspondentes às 4 Grandes Áreas:
  1. *Álgebra e Funções*
  2. *Geometria e Trigonometria*
  3. *Álgebra Linear e Sequências*
  4. *Matemática Aplicada e Estatística*
- Exibe sobreposição de duas camadas: Polígono Cinza pontilhado (Diagnóstico de Entrada) e Polígono Laranja preenchido (Nível Atual).

#### RN-PRG-014: Gráfico de Linha Histórico
- Plota a trajetória de $\theta$ nas últimas semanas, com linha de meta indicativa para o nível Avançado ($\theta = +1.0$).

#### RN-PRG-015: Tooltip Informativo
- Ao passar o mouse ou tocar em qualquer nó do Heatmap ou Radar, exibe: Nome do Volume, Capítulo, Total de Questões Resolvidas e Nota Média.
