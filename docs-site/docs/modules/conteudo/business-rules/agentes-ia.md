---
title: Conteúdo - 2. Agentes de IA e RAG
type: module
status: draft
related:
  - modules/conteudo/business-rules/index.md
last_updated: "2026-08-28"
updated_by: claude
---

# 2. Agentes Especialistas de IA e Arquitetura RAG

### 2.1 Especialização dos Agentes

#### RN-CNT-005: 11 Agentes Especialistas Independentes
- Deve existir exatamente **1 Agente de IA Especialista para cada volume da coleção Iezzi**.
- Cada agente opera com um *System Prompt* hiper-especializado contendo o escopo teórico, terminologias e convenções do respectivo volume.

#### RN-CNT-006: Base Vetorial RAG Dedicada por Volume
- Cada agente especialista possui um índice vetorial isolado (RAG) alimentado com:
  - Textos de teoria, definições formais e demonstrações de teoremas do respectivo volume.
  - Exemplos resolvidos e notas de rodapé do autor.
  - Banco integral de exercícios propostos e testes com resolução detalhada.

#### RN-CNT-007: Agente Orquestrador Central
- Um agente orquestrador analisa o contexto de entrada do aluno (disciplina, volume atual, aula aberta ou exercício em execução) e despacha a requisição para o agente especialista correspondente.
- Em dúvidas interdisciplinares, o orquestrador sintetiza os retornos de múltiplos agentes especialistas antes de entregar a resposta ao aluno.

#### RN-CNT-008: Citação Formal de Fontes
- As respostas dos agentes de IA devem, sempre que aplicável, incluir a referência textual formal (ex: *"Conforme demonstrado no Teorema do Volume 9, Capítulo IV, § 35..."*).

#### RN-CNT-009: Prevenção de Alucinação Algébrica
- Cálculos numéricos e manipulações algébricas críticas devem ser validados pelo motor de computação simbólica antes do envio da resposta final.
