---
title: Autenticação - 2. Perfis e Permissões
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 2. Perfis de Usuário e Controle de Acesso (RBAC)

### 2.1 Matriz de Permissões Binária

#### RN-AUT-006: Definição do Perfil Aluno (`student`)
- O usuário com perfil `student` possui permissão para:
  - Visualizar a Skill Tree e catálogo de volumes.
  - Acessar conteúdos, aulas e baterias de fixação com pagamento vigente.
  - Interagir com os 11 Agentes Especialistas de IA nos volumes adquiridos.
  - Realizar Provas Adaptativas (CAT) e consultar seu histórico e boletim em PDF.

#### RN-AUT-007: Definição do Perfil Professor (`teacher`) e Modo "Visão do Aluno"
- O usuário com perfil `teacher` acumula plenos poderes pedagógicos e administrativos:
  - Acesso irrestrito ao Painel do Professor (`/teacher`) e Dashboard de Analytics.
  - Curadoria e edição KaTeX dos 11 volumes do Iezzi.
  - Gestão de alunos, liberação manual de reteste do CAT e atribuição de reforço.
  - Gestão de faturamento e visualização de extratos comerciais.
- **Modo de Pré-visualização do Aluno**: A barra superior do painel disponibiliza o botão *"Visualizar como Aluno"*, permitindo ao professor navegar pela Skill Tree e testar os exercícios com a experiência exata do estudante, sem perder sua autenticação docente.

#### RN-AUT-008: Isolamento de Rotas Administrativas e Redirecionamento Suave
- Tentativas de acesso direto por usuários com perfil `student` a rotas `/teacher/*` ou `/admin/*` são bloqueadas pelo middleware de autorização:
  - O sistema registra um log de auditoria com IP, User-Agent e timestamp.
  - O estudante é redirecionado suavemente para a Skill Tree (`/dashboard/materias`).
  - Um toast informativo é exibido na tela: *"Área restrita à gestão docente."*

#### RN-AUT-009: Bloqueio de Auto-Elevação de Privilégios
- Nenhum usuário pode alterar sua própria role através de chamadas de API de atualização de perfil.

#### RN-AUT-010: Persistência de Dados em Caso de Bloqueio
- Alunos com acesso suspenso (por expiração da vigência de 12 meses ou cancelamento) mantêm suas credenciais de login ativas para visualização do extrato e histórico anterior.
