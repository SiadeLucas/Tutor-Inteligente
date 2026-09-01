---
title: Autenticação - 2. Perfis e Permissões
type: module
status: draft
related:
  - modules/autenticacao/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 2. Perfis de Usuário e Controle de Acesso (RBAC)

### 2.1 Matriz de Permissões Binária

#### RN-AUT-006: Definição do Perfil Aluno (`student`)
- O usuário com perfil `student` possui permissão para:
  - Visualizar a Skill Tree e catálogo de volumes.
  - Acessar conteúdos, aulas e baterias de fixação liberados.
  - Interagir com os 11 Agentes Especialistas de IA.
  - Realizar Provas Adaptativas (CAT) e consultar seu histórico e boletim.

#### RN-AUT-007: Definição do Perfil Professor (`teacher`)
- O usuário com perfil `teacher` acumula plenos poderes pedagógicos e administrativos:
  - Acesso ao Painel do Professor e Dashboard de Analytics.
  - Curadoria e edição KaTeX dos 11 volumes do Iezzi.
  - Gestão de alunos, liberação de reteste do CAT e concessão de cortesias.
  - Gestão de faturamento e visualização de extratos comerciais.

#### RN-AUT-008: Isolamento de Rotas Administrativas
- Tentativas de acesso direto por usuários com perfil `student` a rotas `/admin/*` ou `/teacher/*` retornam erro `403 Forbidden` com log de segurança.

#### RN-AUT-009: Bloqueio de Auto-Elevação de Privilégios
- Nenhum usuário pode alterar sua própria role através de chamadas de API de atualização de perfil.

#### RN-AUT-010: Persistência de Dados em Caso de Bloqueio
- Alunos com acesso suspenso (por atraso ou cancelamento de pagamento) mantêm suas credenciais de login ativas para visualização do extrato e histórico anterior.
