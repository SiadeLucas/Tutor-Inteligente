---
title: Painel do Professor - 2. Acompanhamento de Alunos
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Acompanhamento de Estudantes e Dossiê

### 2.1 Regras de Consulta do Dossiê do Aluno

#### RN-PRF-006: Visualização de Dados Cadastrais e Menoridade
- A Ficha do Aluno exibe os dados fornecidos no Onboarding (Nome, CPF, Idade, Endereço, Instituição e Série).
- Para estudantes menores de 18 anos, exibe obrigatoriamente a seção destacada com Nome e Contato dos Pais/Responsáveis.

#### RN-PRF-007: Dossiê Pedagógico Individual
- A ficha renderiza o progresso em modo de leitura para acompanhamento:
  - Gráfico Radar individual das Grandes Áreas da matéria ativa.
  - Heatmap de Domínio indicando capítulos concluídos e pendentes.
  - Histórico contínuo da evolução da proficiência ($\theta$).
  - Horas líquidas ativas de estudo acumuladas.

#### RN-PRF-008: Automação Pedagógica Total (Zero Intervenção Manual de Reteste ou Reforço)
- **Proibição de Gestão Operacional Manual**: O professor não precisa e não possui controles manuais para resetar cooldown do CAT ou atribuir listas avulsas de exercícios.
- **Autonomia da Plataforma (Piloto Automático)**:
  - O reteste da Prova Adaptativa Diagnóstica (CAT) é acionado de forma 100% automatizada pelo sistema a cada marco periódico de 7 dias e calibrado continuamente via micro-ajustes a cada exercício.
  - Os treinos de reforço são orquestrados dinamicamente pelo algoritmo a partir dos erros duplos arquivados na Caixa de Reforço e do Hub de Ação dos Top 3 Tópicos Críticos com Questões Gêmeas da IA.
  - A plataforma opera em modelo *Set & Forget*, liberando o professor de tarefas administrativas ou de correções repetitivas.

#### RN-PRF-009: Emissão de Boletim Docente em PDF
- O professor pode gerar e baixar o Boletim em PDF de qualquer estudante matriculado a qualquer momento para conferência ou envio formal aos responsáveis.
