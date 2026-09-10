---
title: Progresso - 3. Heatmap e Radar
type: module
status: draft
related:
  - modules/progresso/business-rules/index.md
last_updated: "2026-09-10"
updated_by: buffy
---

# 3. Parametrização do Heatmap de Domínio e Gráfico Radar

### 3.1 Regras Visuais do Heatmap de Domínio

#### RN-PRG-011: Estrutura da Matriz de Capítulos por Volume
O Heatmap exibe todos os capítulos da coleção didática da disciplina ativa, categorizados em cores:

| Faixa de Taxa de Acertos | Nível de Maestria | Cor no Heatmap |
|:---|:---|:---|
| 0% a 49% | Crítico / Não Iniciado | 🔴 Vermelho |
| 50% a 74% | Em Desenvolvimento | 🟡 Amarelo |
| 75% a 100% | Consolidado / Avançado | 🟢 Verde |

> [!NOTE]
> No lançamento da plataforma, o Heatmap renderiza os capítulos dos 11 volumes da coleção *Gelson Iezzi* (Matemática). A arquitetura é agnóstica e renderiza os volumes da disciplina selecionada no Seletor de Disciplina do Header.

#### RN-PRG-012: Critério de Desbloqueio de Cor do Capítulo
- Um capítulo só é colorido em Amarelo ou Verde após a submissão de no mínimo 3 exercícios correspondentes àquele capítulo. Antes disso, permanece em estado neutro/cinza.

#### RN-PRG-013: Gráfico Radar Multiaxial Dinâmico
- O Gráfico Radar constrói seus eixos dinamicamente com base nas macro-áreas da disciplina selecionada no Header:
  - **Configuração Ativa no Lançamento (Matemática do 2º Grau)**: 4 eixos canônicos (slugs canônicos do projeto, em conformidade com `knowledge/data-architecture.md`, Tabela 07 e com o `scores_grandes_areas` gravado pelo CAT da Etapa 7):
    1. `algebra_funcoes` — *Álgebra e Funções*
    2. `geometria` — *Geometria e Trigonometria*
    3. `algebra_linear` — *Álgebra Linear e Sequências*
    4. `aplicada` — *Matemática Aplicada e Estatística*
  - **Expansões Futuras**: Carrega os eixos cadastrados na tabela `disciplinas` (ex: em Física: *Mecânica*, *Termologia*, *Óptica*, *Eletromagnetismo*).
- Exibe sobreposição de duas camadas: Polígono Cinza pontilhado (Diagnóstico de Entrada) e Polígono Laranja preenchido (Nível Atual).

#### RN-PRG-014: Gráfico de Linha Histórico
- Plota a trajetória de $\theta$ nas últimas semanas, com linha de meta indicativa para o nível Avançado ($\theta = +1.0$).

#### RN-PRG-015: Tooltip Informativo
- Ao passar o mouse ou tocar em qualquer nó do Heatmap ou Radar, exibe: Nome do Volume, Capítulo, Total de Questões Resolvidas e Nota Média.
