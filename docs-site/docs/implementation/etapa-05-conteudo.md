---
title: "Etapa 5: Conteúdo Didático"
type: "Implementation Guide"
status: "Completed"
<!-- Consolidação pós-revisão: migração 003 unificada (heatmap_dominio + horas_estudo_diarias incluídas), auth obrigatória, fixação server-side e heatmap real integrados. -->
related: ["etapa-03-autenticacao.md", "etapa-06-agente.md"]
last_updated: "2026-09-07"
updated_by: "antigravity"
---

<!-- ai-summary
Guia detalhado de implementação da Etapa 5 (Conteúdo Didático) do Tutor Inteligente. Cobre a criação das tabelas de banco de dados (disciplinas, volumes, capítulos, aulas, vetores RAG), modelos SQLAlchemy, migrações Alembic, endpoints FastAPI de conteúdo, e interfaces React no frontend incluindo a Árvore de Habilidades (Skill Tree) e a Tela de Aula em formato Split-Screen com suporte a KaTeX.
-->

# Etapa 5: Conteúdo Didático

Esta etapa estabelece a base de conhecimento do Tutor Inteligente, introduzindo o catálogo de disciplinas, volumes, capítulos e o conteúdo textual das aulas formatado em KaTeX.

**Duração Estimada:** 1-2 semanas  
**Pré-requisito:** [Etapa 3: Autenticação](etapa-03-autenticacao.md) concluída (O sistema precisa identificar os usuários para rastrear progresso).  
**Entregável:** Navegação funcional da Skill Tree (Árvore de Habilidades) e visualização completa de uma aula estruturada em 4 blocos.

---

## 1. Tabelas de Banco de Dados

A arquitetura de conteúdo é hierárquica: `Disciplina -> Volume Didático -> Capítulo -> Aula`. 
Além disso, incluiremos a tabela base para RAG (Retrieval-Augmented Generation), que será de fato populada na Etapa 6.

> [!IMPORTANT]
> A tabela `documentos_vetoriais_rag` requer a extensão `pgvector` instalada e ativada no PostgreSQL.

### Modelo de Dados Relacional

```mermaid
erDiagram
    DISCIPLINAS ||--o{ VOLUMES_DIDATICOS : possui
    VOLUMES_DIDATICOS ||--o{ CAPITULOS : contem
    CAPITULOS ||--|| AULAS : detalha
    VOLUMES_DIDATICOS ||--o{ DOCUMENTOS_VETORIAIS_RAG : referencia
    CAPITULOS ||--o{ DOCUMENTOS_VETORIAIS_RAG : referencia_opcional
    USUARIOS ||--o{ AULAS : atualiza
```

### Detalhamento das Tabelas

| Tabela | Chave Primária | Relacionamentos | Colunas Principais |
|---|---|---|---|
| `disciplinas` | `id` (UUID) | N/A | `slug` (UNIQUE), `nome`, `nivel_ensino`, `cor_tema`, `ordem` |
| `volumes_didaticos` | `id` (UUID) | FK `disciplina_id` | `nome_colecao`, `numero_volume` (1-11), `titulo`, `grande_area`, `preco_padrao` |
| `capitulos` | `id` (UUID) | FK `volume_id` | `numero_capitulo`, `titulo`, `duracao_estimada_minutos` (default 50), `pre_requisitos_ids` (UUID[]) |
| `aulas` (1:1 c/ caps) | `id` (UUID) | FK `capitulo_id` (UNIQUE), FK `atualizado_por` | `bloco_1_teoria` (KaTeX), `bloco_2_exemplos` (KaTeX), `bloco_3_dicas` (KaTeX), `video_url` |
| `documentos_vetoriais_rag` | `id` (UUID) | FK `volume_id`, FK `capitulo_id` (null) | `conteudo_texto`, `embedding` (VECTOR(768)), `metadata` (JSONB) |

---

## 2. Modelos SQLAlchemy e Migração

Crie os modelos SQLAlchemy correspondentes no arquivo `backend/app/models/content.py`.

> [!TIP]
> Utilize tipos do PostgreSQL nativos via SQLAlchemy, como `ARRAY` e `JSONB`. Para a coluna de vetores, você precisará da biblioteca `pgvector`.

### Passo 2.1: Instalar dependências de vetor

Execute no terminal do backend (PowerShell):

```powershell
poetry add pgvector
```

### Passo 2.2: Criar a Migração Alembic

Gere o script de migração usando a ferramenta do Alembic.

```powershell
alembic revision --autogenerate -m "002_content_tables"
```

> [!WARNING]
> Abra o arquivo de migração gerado em `backend/alembic/versions/` e **adicione a criação da extensão pgvector** na função `upgrade()`, ANTES da criação das tabelas:
> ```python
> def upgrade():
>     op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
>     # ... resto do código gerado pelo alembic
> ```

Aplique as mudanças ao banco:

```powershell
alembic upgrade head
```

---

## 3. Schemas de Resposta (Pydantic)

Crie os schemas Pydantic em `backend/app/schemas/content.py`.

Você precisará de schemas de leitura (Responses) para listagem e detalhamento:
- `DisciplinaResponse`
- `VolumeResponse`
- `CapituloResponse`
- `AulaCompletaResponse`
- `SkillTreeNodeResponse`: Este schema será uma composição do `CapituloResponse` acrescido de campos voltados ao mapa de habilidades (como status de cor do mapa de calor do usuário: "green", "yellow", "red", "grey").

---

## 4. Endpoints de Conteúdo (FastAPI)

Crie as rotas em `backend/app/api/v1/endpoints/conteudo.py`.
Você deve implementar tanto rotas de navegação de estrutura (para alimentar a UI) quanto as rotas de interação da aula.

### Rotas de Listagem (Skill Tree e Catálogo)
- `GET /api/v1/conteudo/disciplinas` - Retorna todas as disciplinas ativas.
- `GET /api/v1/conteudo/volumes/{disciplina_id}` - Retorna a coleção de volumes.
- `GET /api/v1/conteudo/capitulos/{volume_id}` - Retorna os capítulos formatados para a Skill Tree.

### Rotas Interativas da Aula
- `GET /api/v1/conteudo/aulas/{capitulo_id}` - Recupera a aula (os 4 blocos) pertinente àquele capítulo.
- `GET /api/v1/conteudo/aulas/{capitulo_id}/fixacao` - Serve a bateria de fixação **sem expor o gabarito** (correção server-side, anti-trapaça).
- `POST /api/v1/conteudo/aulas/{capitulo_id}/fixacao` - Corrige as respostas no servidor (RN-CNT-010) e persiste o `heatmap_dominio` (RN-PRG-012) + counters do dia (`exercicios_submetidos`, `aulas_concluidas`). **Não** grava tempo: `segundos_ativos` tem escritor exclusivo (auto-sync do `useStudyTimer` via `POST /api/v1/progresso/tempo-estudo`, contrato da Etapa 8 — o campo legado `segundos_estudo` é aceito mas ignorado).
- `POST /api/v1/conteudo/aulas/{capitulo_id}/concluir` - Rota legada de conclusão manual com trava de 60%; persiste `aula_concluida` no heatmap.
- `POST /api/v1/conteudo/aulas/{capitulo_id}/chat` - **(Placeholder)** Ponto de entrada do tutor socrático (Etapa 6). Retorna dummy data por enquanto.
- `POST /api/v1/conteudo/aulas/{capitulo_id}/pista` - **(Placeholder)** Dica rápida contextual.

> [!IMPORTANT]
> **Todos os endpoints de conteúdo exigem autenticação** (`get_current_user` da Etapa 3). O status do heatmap na Skill Tree é real e por usuário — não há mais status mockado.

---

## 5. Script de Seed do Banco de Dados

Crie um script em `backend/scripts/seed_content.py` para popular o banco de dados inicial, essencial para testes e desenvolvimento do Frontend.

### Dados a serem populados:
- **Disciplina:** "Matemática" (`slug`: matematica)
- **11 Volumes Baseados na Coleção Iezzi:**
  1. Conjuntos e Funções (`grande_area`: algebra_funcoes)
  2. Logaritmos (`grande_area`: algebra_funcoes)
  3. Trigonometria (`grande_area`: geometria)
  4. Sequências, Matrizes e Determinantes (`grande_area`: algebra_linear)
  5. Combinatória e Probabilidade (`grande_area`: aplicada)
  6. Complexos e Polinômios (`grande_area`: algebra_funcoes)
  7. Geometria Analítica (`grande_area`: geometria)
  8. Limites e Derivadas (`grande_area`: algebra_funcoes)
  9. Geometria Plana (`grande_area`: geometria)
  10. Geometria Espacial (`grande_area`: geometria)
  11. Matemática Financeira e Estatística (`grande_area`: aplicada)
- **Capítulos/Aulas de Exemplo:** Crie ao menos 3-5 capítulos completos no "Volume 1" preenchidos com markdowns e fórmulas KaTeX válidas.

Execute o seed via PowerShell:

```powershell
python backend/scripts/seed_content.py
```

---

## 6. Frontend: Árvore de Habilidades (Skill Tree)

Em `frontend/src/app/(student)/materias/page.tsx`, implemente a visualização da árvore de conteúdo.

### Componentes Principais
1. **Grid de Áreas:** Organize os 11 volumes visivelmente por grandes áreas (Álgebra, Geometria, Aplicada).
2. **Nós Colapsáveis (Accordion):** Cada volume, ao ser clicado, expande a lista de capítulos.
3. **Indicador de Status (Heatmap):** 
   - 🟩 **Verde:** Domínio alcançado (80%+)
   - 🟨 **Amarelo:** Em progresso aceitável (40%-79%)
   - 🟥 **Vermelho:** Dificuldade crítico (<40%)
   - ⬜ **Cinza/Desbotado:** Não iniciado

Ao clicar em um nó de capítulo, o usuário é direcionado para a rota da aula correspondente.

---

## 7. Frontend: Tela de Aula Split-Screen

Em `frontend/src/app/(student)/aula/[id]/page.tsx`, crie uma experiência de aula imersiva com tela dividida.

### Layout Split-Screen
- **Painel Esquerdo (65%):** Visualização de conteúdo principal.
- **Painel Direito (35%):** Sidebar com Chat Socrático (mock visual nesta etapa) e temporizador.

### Funcionalidades do Painel Esquerdo
Implemente um componente de abas (Tabs) para navegar entre:
1. **Teoria**
2. **Exemplos (Passo-a-passo)**
3. **Dicas e Armadilhas**
4. **Fixação (Exercícios)**

> [!NOTE]
> Você precisará de uma biblioteca React para renderizar as equações matemáticas das strings markdown retornadas pelo back-end. Recomenda-se o uso de `react-katex` ou `rehype-katex` integrado com um renderizador markdown (como `react-markdown`).

### Painel Direito e Lógica Auxiliar
- **useStudyTimer Hook:** Hook customizado React (`frontend/src/hooks/useStudyTimer.ts`) que cronometra o tempo líquido ativo da sessão (pausa após 3 min de inatividade) e persiste via `POST /api/v1/progresso/tempo-estudo`. Desde a Etapa 8 é o **único escritor** de `segundos_ativos` (ver etapa-08, seção 8.7).
- **Botão de Conclusão:** Ficará localizado ao final da aba "Fixação", sendo ativado apenas quando o usuário simular/submeter um acerto de 60%+ na avaliação.

---

## 8. Critérios de Aceitação

- [x] A migração Alembic para todas as tabelas de conteúdo é executada sem erros no Windows.
- [x] A extensão `pgvector` é habilitada corretamente pela migração.
- [x] O script de seed popula o banco com 1 disciplina, 11 volumes categorizados e ao menos 3 aulas de exemplo com marcações KaTeX (11 volumes, 63 capítulos e 4 aulas completas com KaTeX).
- [x] O endpoint de `/capitulos/{volume_id}` retorna a estrutura com dados de progresso (status da árvore).
- [x] A interface da Skill Tree no Frontend agrupa os 11 volumes por grandes áreas (ex: Álgebra).
- [x] A coloração dos nós dos capítulos muda adequadamente com base nos dados mockados de desempenho.
- [x] A página de aula divide a tela (65/35) em telas grandes.
- [x] Equações em sintaxe KaTeX são perfeitamente renderizadas no conteúdo dos blocos de aula.
- [x] O botão "Concluir Aula" faz um POST bem-sucedido para `/aulas/{id}/concluir`.
