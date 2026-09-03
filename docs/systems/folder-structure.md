---
title: Estrutura Geral de Pastas do Repositório (Monorepo)
type: knowledge
status: complete
related:
  - systems/index.md
  - knowledge/data-architecture.md
last_updated: "2026-09-02"
updated_by: claude
---

<!-- ai-summary
Estrutura geral de pastas e organização física do código-fonte da plataforma Tutor Inteligente em arquitetura Monorepo.
Detalhamento completo dos diretórios de Backend (FastAPI Python 3.11), Frontend (Next.js 14 App Router TypeScript), Infraestrutura Docker (4 containers com Redis) e scripts de CI/CD.
-->

# Estrutura Geral de Pastas do Repositório (Monorepo)

Para garantir máxima produtividade, facilidade de deploy e alinhamento estrito com a arquitetura em containers Docker **(Frontend, Backend, Banco de Dados e Redis)**, o projeto adota o padrão de **Monorepo**.

---

## 1. Visão Geral da Raiz do Projeto

```text
tutor-inteligente/
├── .github/                      # Automações de CI/CD (GitHub Actions)
│   └── workflows/
│       ├── tests.yml             # Execução de testes de backend (pytest) e frontend (vitest)
│       └── deploy-aws.yml        # Pipeline de deploy automático na AWS EC2
├── backend/                      # 🐳 Container 2: FastAPI + Python 3.11 + SymPy + LangChain
├── frontend/                     # 🐳 Container 1: Next.js 14+ (App Router) + TypeScript + KaTeX
├── infra/                        # Orquestração de containers, proxies e scripts de nuvem
│   ├── docker-compose.yml        # Orquestração dos containers (ti-frontend, ti-backend, ti-database, ti-redis)
│   ├── deploy.sh                 # Script de atualização em 1 comando na AWS EC2
│   └── nginx/                    # Configurações de proxy reverso e headers de segurança
├── docs/                         # Documentação centralizada no MkDocs (este projeto)
├── .env.example                  # Variáveis de ambiente de exemplo
├── .gitignore
└── README.md
```

---

## 2. Estrutura Detalhada do Backend (`/backend`)

O backend é estruturado em **Python 3.11+ com FastAPI**, adotando arquitetura modular limpa (*Clean Architecture* modularizada por domínios de negócio):

```text
backend/
├── alembic/                      # Migrações do banco de dados relacional e vetorial
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                 # Scripts versionados de DDL das 17 tabelas
├── app/
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada FastAPI (CORS, middlewares, routers)
│   ├── core/                     # Configurações fundamentais e segurança
│   │   ├── config.py             # Leitura de variáveis de ambiente com Pydantic Settings
│   │   ├── security.py           # Hashing de senhas (Argon2id/bcrypt), criação e validação de JWT
│   │   └── database.py           # Conexão assíncrona SQLAlchemy (asyncpg) e pool de conexões
│   ├── models/                   # Mapeamento ORM SQLAlchemy das 17 Tabelas do PostgreSQL
│   │   ├── base.py
│   │   ├── user.py               # usuarios, sessoes_ativas, tokens_recuperacao_senha
│   │   ├── commercial.py         # matriculas_pagamentos, transacoes_financeiras
│   │   ├── content.py            # disciplinas, volumes_didaticos, capitulos, aulas, documentos_vetoriais_rag
│   │   ├── exercise.py           # itens_exercicios, tentativas_exercicios, caixa_reforco, provas_cat
│   │   └── progress.py           # heatmap_dominio, historico_theta, horas_estudo_diarias
│   ├── modules/                  # Módulos funcionais desacoplados (Routers, Schemas, Services)
│   │   ├── auth/                 # Login CPF/E-mail, link mágico, sessão única concorrente
│   │   ├── onboarding/           # Wizard multinível e cadastro adaptativo
│   │   ├── content/              # Árvore de habilidades, aulas em 4 blocos e leitor KaTeX
│   │   ├── exercises/            # Baterias de fixação, 2ª chance, Caixa de Reforço
│   │   ├── progress/             # Fórmulas de completude, micro-ajuste no theta, emissão de PDF
│   │   ├── payment/              # Gateway Asaas/MercadoPago, webhook PIX, upgrade proporcional
│   │   └── teacher/              # Analytics demográfico, curadoria split-screen e gestão
│   ├── ai/                       # Motor de Inteligência Artificial e RAG
│   │   ├── agents/               # 11 Agentes Especialistas da coleção Iezzi
│   │   ├── rag_engine.py         # Busca semântica HNSW particionada por volume (pgvector)
│   │   └── socratic_tutor.py     # Prompt engineering do método socrático (3 estágios de pistas)
│   ├── sympy_engine/             # Validação Simbólica Determinística de Matemática
│   │   ├── parser.py             # Conversão de LaTeX para expressões simbólicas do SymPy
│   │   ├── validator.py          # Checagem exata de equivalência algébrica (tolerância ±0.01)
│   │   └── twin_generator.py     # Algoritmo de mutação paramétrica para Questões Gêmeas
│   └── cat_engine/               # Motor Psicométrico da Teoria da Resposta ao Item (TRI)
│       ├── irt_models.py         # Equações logísticas 2PL e 3PL
│       ├── fisher_info.py        # Seleção gulosa de itens por Máxima Informação de Fisher
│       └── eap_estimator.py      # Estimador Bayesiano EAP para atualização do theta
├── tests/                        # Bateria de testes automatizados com Pytest
│   ├── test_cat_engine.py        # Testes de convergência do theta na TRI
│   ├── test_sympy_validator.py   # Testes de gabaritos matemáticos e gêmeas
│   └── test_auth_session.py      # Testes de sessão concorrente única
├── Dockerfile                    # Imagem de produção python:3.11-slim
├── requirements.txt              # Dependências Python estritas
└── alembic.ini
```

---

## 3. Estrutura Detalhada do Frontend (`/frontend`)

O frontend utiliza **Next.js 14+ com App Router, React Server Components (RSC) e TypeScript**:

```text
frontend/
├── public/                       # Assets estáticos, ilustrações, favicons
│   └── fonts/                    # Fontes do KaTeX e Inter
├── src/
│   ├── app/                      # Roteamento baseado em arquivos (App Router)
│   │   ├── (auth)/               # Grupo de rotas públicas
│   │   │   ├── login/            # Tela de Login (E-mail ou CPF com máscara)
│   │   │   ├── cadastro/         # Wizard de Onboarding em 4 passos
│   │   │   └── redefinir-senha/  # Validação do token de link mágico
│   │   ├── (student)/            # Grupo de rotas autenticadas do Aluno
│   │   │   ├── layout.tsx        # Shell do aluno: Sidebar fixa Khan Academy + Header
│   │   │   ├── onboarding/       # Prova Adaptativa Diagnóstica (CAT)
│   │   │   ├── materias/         # Skill Tree visual dos 11 volumes do Iezzi
│   │   │   ├── aula/[id]/        # Player de aula de 50 min em 4 blocos + Chat Socrático
│   │   │   ├── exercicios/[id]/  # Interface de fixação KaTeX com 2ª chance e Questões Gêmeas
│   │   │   ├── progresso/        # Heatmap, Gráfico Radar comparativo e botão Baixar PDF
│   │   │   └── checkout/         # Checkout in-app instantâneo (PIX dinâmico e Cartão)
│   │   ├── (teacher)/            # Grupo de rotas restritas do Professor (`/teacher`)
│   │   │   ├── layout.tsx        # Shell docente com botão "Modo Visão do Aluno"
│   │   │   ├── teacher/          # Dashboard de Analytics Demográfico
│   │   │   ├── teacher/alunos/   # Gestão individual e Dossiê do Aluno
│   │   │   ├── teacher/curadoria/# Editor split-screen com KaTeX em tempo real
│   │   │   └── teacher/financeiro# Extrato comercial e ranking de vendas
│   │   ├── layout.tsx            # Layout raiz (Provedores de tema, React Query, KaTeX CSS)
│   │   └── globals.css           # Estilos globais Tailwind e variáveis CSS do tema
│   ├── components/               # Componentes reutilizáveis
│   │   ├── ui/                   # Botões, modais, inputs com máscara, toasts
│   │   ├── math/                 # KaTeXRenderer (fórmulas inline e display) e KaTeXEditor
│   │   ├── charts/               # RadarChart (Recharts), HeatmapMatrix, TimelineTheta
│   │   ├── header/               # DisciplineSwitcher (Seletor Global de Matéria)
│   │   └── session/              # ConcurrentSessionModal (aviso de desconexão e rascunho)
│   ├── hooks/                    # Custom React Hooks
│   │   ├── useStudyTimer.ts      # Cronômetro de tempo líquido ativo com pausa em inatividade
│   │   ├── useSilentAuth.ts      # Interceptor HTTP para renovação automática de token JWT
│   │   └── useSocraticChat.ts    # Hook de conversação fluida com o Agente de IA da aula
│   ├── lib/                      # Utilitários e instâncias globais
│   │   ├── api.ts                # Cliente Axios/Fetch com interceptors de erro e refresh
│   │   ├── formatters.ts         # Máscara de CPF, CEP e conversão de moeda BRL
│   │   └── katex-helpers.ts      # Sanitização e parsing de expressões LaTeX
│   └── types/                    # Interfaces e tipos TypeScript de todo o sistema
│       ├── user.ts
│       ├── content.ts
│       ├── exercise.ts
│       └── progress.ts
├── Dockerfile                    # Imagem de produção multi-stage (Node.js 20 Alpine)
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## 4. Diretório de Infraestrutura (`/infra`)

Reúne os arquivos de implantação na **AWS EC2**:

```text
infra/
├── docker-compose.yml            # Orquestra ti-frontend (3000), ti-backend (8000) e ti-database (5432)
├── deploy.sh                     # Script shell de deploy automatizado em produção
└── nginx/
    └── default.conf              # Configuração do Nginx para servir certificados SSL e proxy
```
