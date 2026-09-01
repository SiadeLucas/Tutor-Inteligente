---
title: Painel do Professor - 3. Central de Curadoria
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 3. Central de Curadoria e Gestão de Conteúdo

### 3.1 Ciclo de Publicação e Edição KaTeX

#### RN-PRF-011: Estados de Publicação (Workflow Draft & Publish)
- Todo conteúdo gerado pelas IAs dos 11 volumes obedece ao ciclo de estados:
  - `draft_ai`: Gerado por IA, visível apenas para o professor.
  - `reviewed_teacher`: Editado e aprovado pelo professor.
  - `published`: Publicado e liberado para os estudantes.
  - `archived`: Desativado da Skill Tree.

#### RN-PRF-012: Editor Split-Screen com Preview KaTeX
- O painel administrativo deve oferecer editor em duas colunas:
  - Coluna 1: Entrada de texto em Markdown e código LaTeX.
  - Coluna 2: Renderização em tempo real via KaTeX com atualização a cada digitação.

#### RN-PRF-013: Aprovação em Lote (1-Click Publish)
- O professor pode aprovar capítulos inteiros ou múltiplos exercícios de uma só vez após conferência rápida.

#### RN-PRF-014: Curadoria do Banco de Questões Gêmeas
- O professor pode visualizar o enunciado, o gabarito e a resolução passo a passo gerada pela IA/SymPy, com opção de aprovar, editar ou solicitar regeração do item.

#### RN-PRF-015: Anexo de Materiais e Links Docentes
- É permitido ao professor fazer upload de apostilas em PDF (limite de 50MB por arquivo) e adicionar links de transmissões de vídeo complementares para qualquer aula dos 11 volumes.
