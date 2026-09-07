---
title: Onboarding - 3. Escalabilidade
type: module
status: draft
related:
  - modules/onboarding/business-rules/index.md
  - modules/onboarding/business-rules/proficiencia.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 3. Escalabilidade e Arquitetura de Domínio

### 3.1 Modelo Hierárquico de Ensino

#### RN-ESC-001: Hierarquia Nível → Disciplina → Volumes Didáticos
A arquitetura do domínio educacional é estritamente desacoplada em níveis hierárquicos genéricos no banco de dados e na API:

```
[ Nível de Ensino ] ──(1:N)──> [ Disciplina ] ──(1:N)──> [ Volumes Didáticos ] ──(1:N)──> [ Capítulos 50 min ]
```

- A inclusão de novas disciplinas (ex: Física, Química) ou coleções didáticas exige apenas a inserção de registros nas tabelas `disciplinas` e `volumes_didaticos`, sem necessidade de refatorar schemas ou reescrever APIs.
- O motor psicométrico da TRI (CAT), os agentes de IA e as interfaces de Skill Tree consomem os metadados da disciplina ativa de forma agnóstica.

#### RN-ESC-001.1: Configuração Ativa de Lançamento (Foco Exclusivo em Matemática do 2º Grau)
- Embora o sistema seja nativamente multidisciplinar e multinível, **no lançamento da plataforma apenas a disciplina "Matemática do Ensino Médio" (Coleção Gelson Iezzi - 11 Volumes) permanece com `ativo = TRUE`**.
- As demais disciplinas e níveis de ensino ficam pré-estruturadas no sistema em estado inativo (`ativo = FALSE`), aguardando futura liberação estratégica pelo professor sem retrabalho técnico.

---

### 3.2 Políticas de Acesso e Expansão

#### RN-ESC-002: Matrículas e Acessos por Disciplina
- O estudante pode adquirir capítulos ou volumes de qualquer disciplina ativa na plataforma.
- A gestão comercial e o status da matrícula operam de forma independente por disciplina e por volume.

#### RN-ESC-003: Extensibilidade de Níveis de Ensino
- O sistema é modelado para suportar nativamente:
  - **Ensino Médio** (disciplina ativa no lançamento)
  - Ensino Fundamental II (6º ao 9º ano)
  - Pré-Vestibular / Concursos
  - Ensino Superior (Cálculo e Álgebra Linear)
