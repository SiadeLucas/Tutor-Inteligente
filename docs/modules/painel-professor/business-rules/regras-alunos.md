---
title: Painel do Professor - 2. Gestão de Alunos
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 2. Gestão Individual de Estudantes e Intervenções

### 2.1 Regras da Ficha do Aluno

#### RN-PRF-006: Visualização Completa de Dados Cadastrais
- A Ficha do Aluno exibe os dados fornecidos no Onboarding (Nome, CPF, Idade, Endereço, Instituição e Série).
- Para estudantes menores de 18 anos, deve exibir obrigatoriamente a seção destacada com Nome e Contato dos Pais/Responsáveis.

#### RN-PRF-007: Dossiê Pedagógico Individual
- A ficha deve renderizar:
  - Gráfico Radar individual das 4 Grandes Áreas.
  - Heatmap dos 11 volumes indicando capítulos concluídos e pendentes.
  - Tabela com histórico de cada Prova CAT realizada (data, score $\theta$ e tempo de prova).

#### RN-PRF-008: Liberação Manual de Reteste do CAT
- O professor pode, a seu critério pedagógico, anular o cooldown de 7 dias e liberar imediatamente uma nova Prova CAT para o aluno.

#### RN-PRF-009: Atribuição de Listas de Reforço Personalizadas
- O professor pode selecionar um volume ou capítulo específico do Iezzi e despachar uma lista extra de Questões Gêmeas diretamente para a caixa de atividades do aluno.

#### RN-PRF-010: Emissão de Boletim Docente em PDF
- O professor tem permissão para gerar e baixar o Boletim em PDF de qualquer estudante matriculado a qualquer momento.
