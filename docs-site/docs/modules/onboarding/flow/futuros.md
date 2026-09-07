---
title: Onboarding - 4. Fluxos Futuros
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/flow/proficiencia.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 4. Fluxos Contínuos e Futuros

### 4.1 Descoberta e Avaliação em Novas Matérias
Com a expansão da plataforma para outras disciplinas, a prova de proficiência é disparada no primeiro ingresso do aluno em cada nova matéria (o mesmo gatilho aplicado à Matemática imediatamente após o cadastro).

```mermaid
flowchart TD
    A["Navegação para Nova Matéria (ex: Português)"] --> B{"Matéria já possui diagnóstico do aluno?"}
    B -->|Sim| C["Carrega Dashboard da Matéria com Níveis Atuais"]
    B -->|Não| D["Modal: Apresentar Prova Diagnóstica da Matéria"]
    D --> E{"Aluno Aceita?"}
    E -->|Sim| F["Inicia CAT específico da Matéria"]
    E -->|Pular| G["Aplica Nível 'Básico' para as áreas da Matéria"]
    F --> H["Gera Radar da Matéria e Salva Níveis"]
    G --> C
    H --> C
```

---

### 4.2 Reavaliação e Política de Cooldown
Permite que o estudante refaça a avaliação diagnóstica para recalibrar sua trilha conforme avança nos estudos, respeitando o intervalo de segurança de 7 dias.

```mermaid
flowchart TD
    A["Solicitação de Reavaliação Diagnóstica"] --> B{"Tempo desde a última prova >= 7 dias?"}
    B -->|Sim| C["Habilita Nova Sessão de Prova CAT"]
    B -->|Não| D["Exibe Bloqueio Temporal: 'Disponível em X dias'"]
    C --> E["Execução da Prova Adaptativa"]
    E --> F["Atualização dos Níveis Ativos do Aluno"]
    F --> G["Manutenção de Registro no Histórico de Desempenho"]
    G --> H["Atualização Instantânea da Trilha de Aprendizado"]
```
