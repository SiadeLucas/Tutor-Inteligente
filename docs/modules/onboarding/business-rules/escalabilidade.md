---
title: Onboarding - 3. Escalabilidade
type: module
status: draft
related:
  - modules/onboarding/business-rules/index.md
  - modules/onboarding/business-rules/proficiencia.md
last_updated: "2026-08-26"
updated_by: claude
---

# 3. Escalabilidade e Arquitetura de Domínio

### 3.1 Modelo Hierárquico de Ensino

#### RN-ESC-001: Hierarquia Nível → Matéria → Área
A arquitetura do domínio educacional é estritamente desacoplada em 3 níveis hierárquicos genéricos:

```
[ Nível de Ensino ] ──(1:N)──> [ Matéria ] ──(1:N)──> [ Área / Tópico ]
```

- Adição de nova disciplina requer apenas a criação dos registros de Matéria, suas Áreas correspondentes e a carga do banco de questões CAT.
- A lógica de negócio do onboarding, adaptação de testes e dashboard consome a hierarquia de forma totalmente agnóstica.

---

### 3.2 Políticas de Acesso e Expansão

#### RN-ESC-002: Acesso Livre Universal
- O estudante possui acesso irrestrito para navegar entre todas as matérias e níveis curriculares disponibilizados na plataforma.
- Não há bloqueios no cadastro exigindo matrícula prévia em disciplinas específicas.

#### RN-ESC-003: Extensibilidade de Níveis de Ensino
- A estrutura de banco e interface é preparada para expansão sem refatoração de schema, suportando futuros níveis:
  - Ensino Fundamental I e II
  - Ensino Médio (padrão atual)
  - Pré-Vestibular / ENEM
  - Ensino Superior e Pós-Graduação
