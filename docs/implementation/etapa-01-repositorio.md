---
title: "Etapa 1: Repositório e Ambiente Local"
type: implementation
status: pending
related:
  - implementation/index.md
  - systems/folder-structure.md
last_updated: "2026-09-06"
updated_by: claude
---

# Etapa 1: Repositório e Ambiente Local

**Duração estimada:** 2-3 dias  
**Pré-requisitos:** Computador com Windows 10/11, conexão à internet  
**Entregável:** `docker compose ps` mostrando 4 containers `healthy`

---

## 1.1 Softwares Necessários

Antes de começar, instale os seguintes softwares no seu computador:

| Software | Versão Mínima | Download | Para quê |
|:---|:---|:---|:---|
| **Git** | 2.40+ | [git-scm.com](https://git-scm.com/download/win) | Controle de versão |
| **Docker Desktop** | 4.25+ | [docker.com](https://www.docker.com/products/docker-desktop/) | Rodar containers localmente |
| **Node.js** | 20 LTS | [nodejs.org](https://nodejs.org/) | Desenvolvimento frontend |
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) | Desenvolvimento backend |
| **VS Code** | Último | [code.visualstudio.com](https://code.visualstudio.com/) | Editor de código |

### Extensões recomendadas do VS Code

- **Python** (Microsoft) — IntelliSense e debug
- **Pylance** (Microsoft) — Type checking
- **ES7+ React/Redux/React-Native snippets** — Snippets React
- **Tailwind CSS IntelliSense** — Autocomplete Tailwind
- **Docker** (Microsoft) — Gerenciamento visual de containers
- **GitLens** — Histórico Git avançado
- **Thunder Client** — Testar APIs REST (alternativa ao Postman)

---

## 1.2 Criar o Repositório no GitHub

### Passo 1: Criar o repositório

1. Acesse [github.com/new](https://github.com/new)
2. Configure:
   - **Repository name:** `tutor-inteligente`
   - **Description:** `Plataforma EAD de Matemática do Ensino Médio com IA Socrática`
   - **Visibility:** `Private`
   - **Add .gitignore:** Selecione `Python`
   - **Add a license:** Selecione `MIT License` (ou nenhuma se preferir manter fechado)
3. Clique em **Create repository**

### Passo 2: Clonar no seu computador

Abra o terminal (PowerShell ou Git Bash) e execute:

```powershell
cd C:\Users\SeuUsuario\Documents\Projetos
git clone https://github.com/SEU_USUARIO/tutor-inteligente.git
cd tutor-inteligente
```

---

## 1.3 Criar a Estrutura de Pastas

Execute os comandos abaixo para criar toda a árvore de diretórios do Monorepo:

```powershell
# ============================================
# Raiz do projeto
# ============================================
mkdir -p .github/workflows
mkdir -p infra/nginx

# ============================================
# Backend (FastAPI + Python 3.11)
# ============================================
mkdir -p backend/alembic/versions
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/modules/auth
mkdir -p backend/app/modules/onboarding
mkdir -p backend/app/modules/content
mkdir -p backend/app/modules/exercises
mkdir -p backend/app/modules/progress
mkdir -p backend/app/modules/payment
mkdir -p backend/app/modules/teacher
mkdir -p backend/app/ai/agents
mkdir -p backend/app/ai/prompts
mkdir -p backend/app/sympy_engine
mkdir -p backend/app/cat_engine
mkdir -p backend/tests

# ============================================
# Frontend (Next.js 14 + TypeScript)
# ============================================
mkdir -p frontend/public/fonts
mkdir -p "frontend/src/app/(auth)/login"
mkdir -p "frontend/src/app/(auth)/cadastro"
mkdir -p "frontend/src/app/(auth)/redefinir-senha"
mkdir -p "frontend/src/app/(student)/onboarding"
mkdir -p "frontend/src/app/(student)/materias"
mkdir -p "frontend/src/app/(student)/aula/[id]"
mkdir -p "frontend/src/app/(student)/exercicios/[id]"
mkdir -p "frontend/src/app/(student)/progresso"
mkdir -p "frontend/src/app/(student)/checkout"
mkdir -p "frontend/src/app/(teacher)/teacher"
mkdir -p "frontend/src/app/(teacher)/teacher/alunos"
mkdir -p "frontend/src/app/(teacher)/teacher/curadoria"
mkdir -p "frontend/src/app/(teacher)/teacher/financeiro"
mkdir -p frontend/src/components/ui
mkdir -p frontend/src/components/math
mkdir -p frontend/src/components/charts
mkdir -p frontend/src/components/header
mkdir -p frontend/src/components/session
mkdir -p frontend/src/hooks
mkdir -p frontend/src/lib
mkdir -p frontend/src/types
```

---

## 1.4 Criar Arquivos de Configuração

### 1.4.1 Arquivo `.env.example` (raiz do projeto)

Crie o arquivo `.env.example` na raiz do projeto com todas as variáveis de ambiente:

```bash
# ==============================================================================
# Tutor Inteligente — Variáveis de Ambiente
# Copie este arquivo para .env e preencha os valores reais
# ==============================================================================

# --- Banco de Dados PostgreSQL ---
DB_USER=tutor_admin
DB_PASSWORD=TROQUE_POR_SENHA_FORTE_AQUI
DB_HOST=ti-database
DB_PORT=5432
DB_NAME=tutor_inteligente
DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# --- Redis (Sessões e Cache) ---
REDIS_PASSWORD=TROQUE_POR_SENHA_FORTE_REDIS
REDIS_URL=redis://:${REDIS_PASSWORD}@ti-redis:6379/0

# --- JWT e Segurança ---
JWT_SECRET_KEY=TROQUE_POR_CHAVE_SECRETA_JWT_256BITS
JWT_REFRESH_SECRET_KEY=TROQUE_POR_OUTRA_CHAVE_REFRESH_256BITS
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# --- Inteligência Artificial (Gemini Flash / Google) ---
GOOGLE_API_KEY=COLE_SUA_CHAVE_DA_API_GEMINI_AQUI

# --- Gateway de Pagamento (Asaas) ---
ASAAS_API_KEY=COLE_SUA_CHAVE_DA_API_ASAAS_AQUI
ASAAS_WEBHOOK_SECRET_TOKEN=TROQUE_POR_TOKEN_SECRETO_DO_WEBHOOK
ASAAS_ENVIRONMENT=sandbox

# --- AWS S3 (Armazenamento de Arquivos) ---
AWS_ACCESS_KEY_ID=COLE_SUA_ACCESS_KEY_AWS
AWS_SECRET_ACCESS_KEY=COLE_SUA_SECRET_KEY_AWS
AWS_S3_BUCKET=tutor-inteligente-assets
AWS_REGION=sa-east-1

# --- Amazon SES (E-mail Transacional) ---
SES_SENDER_EMAIL=noreply@tutorinteligente.com.br

# --- Configurações do Servidor ---
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,https://tutorinteligente.com.br
```

Depois de criar o `.env.example`, copie-o para `.env` real:

```powershell
cp .env.example .env
# Edite o .env com senhas reais (NÃO comite o .env no Git!)
```

### 1.4.2 Arquivo `.gitignore` (raiz do projeto)

Substitua o conteúdo do `.gitignore` gerado pelo GitHub:

```gitignore
# ==============================================================================
# Tutor Inteligente — .gitignore
# ==============================================================================

# --- Segredos (NUNCA comitar) ---
.env
*.pem
*.key

# --- Python ---
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
.pytest_cache/
.mypy_cache/

# --- Node.js / Next.js ---
node_modules/
.next/
out/
.turbo/

# --- Docker ---
postgres_data/
redis_data/

# --- IDE ---
.vscode/settings.json
.idea/
*.swp
*.swo

# --- OS ---
.DS_Store
Thumbs.db
desktop.ini

# --- MkDocs (site gerado) ---
site/
```

### 1.4.3 Arquivo `backend/requirements.txt`

```text
# ==============================================================================
# Tutor Inteligente — Dependências Python
# ==============================================================================

# --- Framework Web ---
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic[email]==2.9.0
pydantic-settings==2.5.0
python-multipart==0.0.9

# --- Banco de Dados (PostgreSQL Assíncrono) ---
sqlalchemy[asyncio]==2.0.35
asyncpg==0.30.0
alembic==1.13.0
pgvector==0.3.0

# --- Redis (Cache e Sessões Voláteis) ---
redis[hiredis]==5.1.0

# --- Segurança e Criptografia ---
python-jose[cryptography]==3.3.0
passlib[argon2]==1.7.4
argon2-cffi==23.1.0

# --- Álgebra Simbólica e Motor Psicométrico ---
sympy==1.13.0
numpy==2.1.0
scipy==1.14.0

# --- Inteligência Artificial e RAG ---
google-generativeai==0.8.0
langchain==0.3.0
langchain-google-genai==2.0.0

# --- HTTP e Utilitários ---
httpx==0.27.0
boto3==1.35.0
reportlab==4.2.0

# --- Testes ---
pytest==8.3.0
pytest-asyncio==0.24.0
httpx==0.27.0
```

### 1.4.4 Arquivo `backend/Dockerfile`

```dockerfile
# ==============================================================================
# Tutor Inteligente — Backend (Python 3.11 + FastAPI)
# ==============================================================================
FROM python:3.11-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte
COPY . .

# Expor porta do Uvicorn
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 1.4.5 Arquivo `frontend/Dockerfile`

```dockerfile
# ==============================================================================
# Tutor Inteligente — Frontend (Next.js 14 + TypeScript)
# ==============================================================================

# Etapa 1: Instalação de dependências
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Etapa 2: Build de produção
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Etapa 3: Imagem de produção enxuta
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Copiar apenas os artefatos necessários
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

### 1.4.6 Arquivo `infra/docker-compose.yml`

```yaml
# ==============================================================================
# Tutor Inteligente — Orquestração Docker Compose
# ==============================================================================
version: "3.9"

services:
  # ---------- Banco de Dados (PostgreSQL 16 + pgvector) ----------
  ti-database:
    image: pgvector/pgvector:pg16
    container_name: ti-database
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME:-tutor_inteligente}
      POSTGRES_USER: ${DB_USER:-tutor_admin}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"  # Exposto localmente para debug; remover em produção
    networks:
      - ti-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-tutor_admin} -d ${DB_NAME:-tutor_inteligente}"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ---------- Cache e Sessões Voláteis (Redis 7) ----------
  ti-redis:
    image: redis:7-alpine
    container_name: ti-redis
    restart: always
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "${REDIS_PASSWORD}"]
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"  # Exposto localmente para debug; remover em produção
    networks:
      - ti-network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ---------- Backend API (FastAPI + Python 3.11) ----------
  ti-backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: ti-backend
    restart: always
    env_file:
      - ../.env
    depends_on:
      ti-database:
        condition: service_healthy
      ti-redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    networks:
      - ti-network

  # ---------- Frontend Web (Next.js 14 + TypeScript) ----------
  ti-frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    container_name: ti-frontend
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:8000}
    depends_on:
      - ti-backend
    ports:
      - "3000:3000"
    networks:
      - ti-network

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  ti-network:
    driver: bridge
```

---

## 1.5 Criar o Esqueleto do Backend (FastAPI)

### 1.5.1 Arquivo `backend/app/__init__.py`

```python
# Pacote raiz da aplicação Tutor Inteligente
```

### 1.5.2 Arquivo `backend/app/main.py`

```python
"""
Tutor Inteligente — Ponto de Entrada da API FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title="Tutor Inteligente API",
    description="API da plataforma EAD de Matemática do Ensino Médio com IA Socrática",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Infraestrutura"])
async def health_check():
    """Endpoint de verificação de saúde para monitoramento."""
    return {
        "status": "healthy",
        "service": "tutor-inteligente-api",
        "version": "0.1.0"
    }
```

### 1.5.3 Arquivo `backend/app/core/__init__.py`

```python
# Módulo de configurações fundamentais
```

### 1.5.4 Arquivo `backend/app/core/config.py`

```python
"""
Configuração centralizada via variáveis de ambiente (Pydantic Settings).
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # --- Banco de Dados ---
    DATABASE_URL: str = "postgresql+asyncpg://tutor_admin:password@ti-database:5432/tutor_inteligente"

    # --- Redis ---
    REDIS_URL: str = "redis://:password@ti-redis:6379/0"

    # --- JWT ---
    JWT_SECRET_KEY: str = "CHANGE_ME"
    JWT_REFRESH_SECRET_KEY: str = "CHANGE_ME_TOO"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- IA ---
    GOOGLE_API_KEY: str = ""

    # --- Asaas ---
    ASAAS_API_KEY: str = ""
    ASAAS_WEBHOOK_SECRET_TOKEN: str = ""
    ASAAS_ENVIRONMENT: str = "sandbox"

    # --- AWS ---
    AWS_S3_BUCKET: str = "tutor-inteligente-assets"
    AWS_REGION: str = "sa-east-1"

    # --- Geral ---
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

## 1.6 Testar o Docker Compose Localmente

### Passo 1: Editar o `.env` com senhas temporárias

```powershell
# Na raiz do projeto, edite o .env:
notepad .env
```

Preencha pelo menos:
```
DB_PASSWORD=senhalocal123
REDIS_PASSWORD=redislocal123
JWT_SECRET_KEY=chave_temporaria_dev_apenas
JWT_REFRESH_SECRET_KEY=outra_chave_temporaria_dev
```

### Passo 2: Subir os containers

```powershell
cd infra
docker compose up --build -d
```

### Passo 3: Verificar a saúde dos containers

```powershell
docker compose ps
```

**Resultado esperado:**
```
NAME           IMAGE                      STATUS                   PORTS
ti-backend     infra-ti-backend           Up (healthy)             0.0.0.0:8000->8000/tcp
ti-database    pgvector/pgvector:pg16     Up (healthy)             0.0.0.0:5432->5432/tcp
ti-frontend    infra-ti-frontend          Up                       0.0.0.0:3000->3000/tcp
ti-redis       redis:7-alpine             Up (healthy)             0.0.0.0:6379->6379/tcp
```

### Passo 4: Testar o endpoint de saúde

```powershell
curl http://localhost:8000/health
```

**Resultado esperado:**
```json
{"status": "healthy", "service": "tutor-inteligente-api", "version": "0.1.0"}
```

### Passo 5: Acessar a documentação Swagger

Abra no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

Você deve ver a interface interativa do Swagger com o endpoint `/health` listado.

---

## 1.7 Primeiro Commit e Push

```powershell
cd ..  # Voltar para a raiz do projeto
git add -A
git commit -m "feat: estrutura inicial do monorepo com Docker Compose e FastAPI"
git push origin main
```

---

## 1.8 Critérios de Aceitação

Antes de avançar para a Etapa 2, confirme que todos os itens abaixo estão OK:

- [ ] Repositório GitHub criado e acessível
- [ ] `git clone` funciona no computador local
- [ ] Estrutura de pastas do Monorepo criada (backend/, frontend/, infra/, docs/)
- [ ] Arquivo `.env` criado com variáveis preenchidas (não comitado no Git)
- [ ] `docker compose up --build -d` executa sem erros
- [ ] `docker compose ps` mostra 4 containers com status `Up`
- [ ] Container `ti-database` reporta `healthy`
- [ ] Container `ti-redis` reporta `healthy`
- [ ] `curl http://localhost:8000/health` retorna `{"status": "healthy"}`
- [ ] Swagger acessível em `http://localhost:8000/docs`
- [ ] Primeiro commit e push realizados com sucesso no GitHub

> [!TIP]
> Se algum container não subir, use `docker compose logs ti-backend` (ou o nome do container com problema) para ver os logs de erro.
