---
title: Sistemas e Arquitetura Tecnológica
type: knowledge
status: complete
related:
  - knowledge/data-architecture.md
  - knowledge/project-context.md
  - modules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

<!-- ai-summary
Especificação técnica da stack, containers Docker e infraestrutura AWS da plataforma Tutor Inteligente.
Arquitetura em 3 containers:
1. Frontend Web Responsivo (Next.js 14, TypeScript, Tailwind CSS e KaTeX).
2. Backend API & Motor de IA (Python 3.11, FastAPI, SymPy, LangChain e NumPy/SciPy para TRI).
3. Banco de Dados Unificado (PostgreSQL 16 com extensão pgvector para RAG e dados relacionais).
Infraestrutura em nuvem na AWS: EC2 com Docker Compose, Amazon S3 para PDFs e Amazon CloudFront CDN com SSL/TLS.
-->

# Sistemas e Arquitetura Tecnológica

Documentação técnica oficial das linguagens, frameworks, orquestração em containers Docker e infraestrutura em nuvem na **Amazon Web Services (AWS)** da plataforma **Tutor Inteligente**.

---

## 1. Visão Geral da Stack Tecnológica

A plataforma é dividida em 3 camadas de software desacopladas, orquestradas em containers Docker e integradas a serviços gerenciados da AWS:

```mermaid
graph TD
    Client["📱 Navegador Web (Mobile & Desktop) \n Aluno e Professor"]
    
    subgraph AWS["☁️ Nuvem AWS"]
        CF["Amazon CloudFront (CDN + SSL HTTPS)"]
        S3["Amazon S3 (PDFs de Apostilas e Imagens)"]
        
        subgraph EC2["Instância AWS EC2 (Docker Compose)"]
            subgraph Net["Rede Interna: ti-network"]
                C1["🐳 Container 1: ti-frontend \n Next.js 14 + Tailwind + KaTeX \n Porta 3000"]
                C2["🐳 Container 2: ti-backend \n Python 3.11 + FastAPI + SymPy \n Porta 8000"]
                C3["🐳 Container 3: ti-database \n PostgreSQL 16 + pgvector \n Porta 5432"]
            end
        end
    end
    
    Client -->|HTTPS| CF
    CF --> C1
    CF --> S3
    C1 -->|API REST / JSON| C2
    C2 -->|SQL & Vetores| C3
    C2 -->|Upload / Assinatura de URL| S3
```

---

## 2. As 4 Camadas Técnicas Detalhadas

### Camada 1: Frontend Web Responsivo (`ti-frontend`)

- **Linguagem & Framework**: **TypeScript** com **Next.js 14+ (React)** utilizando *App Router*.
- **Estilização & UI**: **Tailwind CSS** com suporte a Dark Mode e identidade visual no estilo Khan Academy (paleta Laranja `#F57C00` e fundos escuros `#1a1408`).
- **Renderização Matemática**: **KaTeX** client-side para fórmulas instantâneas, frações, matrizes e símbolos gregos ($\theta$) sem lentidão.
- **Gráficos & Visualização**: **Recharts** e **Chart.js** para o Gráfico Radar Multiaxial de Proficiência, Linha do Tempo e Heatmap dos 11 Volumes.
- **Dockerização**: Multi-stage build com imagem base `node:20-alpine`, gerando container final de produção enxuto (< 150MB).

### Camada 2: Backend API & Motor de IA (`ti-backend`)

- **Linguagem & Framework**: **Python 3.11+** com **FastAPI** assíncrono (`async/await`) e **Pydantic v2** para validação estrita de dados e documentação Swagger automática em `/docs`.
- **Álgebra Simbólica & Validação**: **SymPy** para computação simbólica determinística (validação matemática exata de gabaritos e geração de Questões Gêmeas com tolerância $\pm 0.01$).
- **Inteligência Artificial (RAG)**: **LangChain** / **LlamaIndex** para orquestração da rede de **11 Agentes Especialistas** da coleção Iezzi e mediação socrática em 3 estágios.
- **Motor Psicométrico (TRI)**: **SciPy** e **NumPy** para implementação do modelo logístico 2PL/3PL da Teoria da Resposta ao Item, estimativa bayesiana EAP e seleção por Máxima Informação de Fisher no CAT.
- **Dockerização**: Imagem base `python:3.11-slim` rodando com servidor **Uvicorn** multi-worker.

### Camada 3: Banco de Dados Unificado (`ti-database`)

- **SGBD**: **PostgreSQL 16** com a extensão oficial **`pgvector`** (imagem `pgvector/pgvector:pg16`).
- **Híbrido Relacional e Vetorial**:
  - *Dados Relacionais*: Tabelas transacionais ACID (Usuários, CPFs, Matrículas, Cobranças PIX/Cartão, Histórico de Notas e Sessões).
  - *Dados Vetoriais*: Tabelas de embeddings dos 11 volumes do Iezzi indexadas com algoritmos HNSW para busca semântica em milissegundos.
- **Persistência**: Volume Docker montado (`postgres_data`) acoplado a disco EBS criptografado na AWS.

### Camada 4: Infraestrutura AWS & Nuvem

| Componente AWS | Função na Arquitetura | Vantagem / Motivação |
|:---|:---|:---|
| **AWS EC2 (Ubuntu Linux)** | Hospeda os 3 containers Docker via `docker-compose` | Simplicidade operacional, controle total e custo previsível |
| **Amazon S3** | Armazenamento de arquivos estáticos (PDFs de apostilas e imagens) | Alta durabilidade (99.999999999%), URLs pré-assinadas seguras |
| **Amazon CloudFront** | CDN global com cache de borda e certificado SSL | Latência ultrabaixa para entrega de páginas no Brasil com HTTPS |
| **AWS Certificate Manager (ACM)** | Emissão e renovação automática de certificado SSL gratuito | Criptografia ponta a ponta (TLS 1.3) para domínio personalizado |
| **Amazon Route 53** | Gestão de DNS do domínio da plataforma | Resolução de nomes de alta disponibilidade e roteamento |

---

## 3. Orquestração em Containers: `docker-compose.yml`

Os 3 containers operam em rede interna isolada, expondo publicamente apenas as portas estritamente necessárias:

```yaml
version: "3.9"

services:
  ti-database:
    image: pgvector/pgvector:pg16
    container_name: ti-database
    restart: always
    environment:
      POSTGRES_DB: tutor_inteligente
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ti-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d tutor_inteligente"]
      interval: 5s
      timeout: 5s
      retries: 5

  ti-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ti-backend
    restart: always
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@ti-database:5432/tutor_inteligente
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      AWS_S3_BUCKET: ${AWS_S3_BUCKET}
    depends_on:
      ti-database:
        condition: service_healthy
    networks:
      - ti-network
    expose:
      - "8000"

  ti-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: ti-frontend
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: https://api.tutorinteligente.com.br
    ports:
      - "80:3000"
    depends_on:
      - ti-backend
    networks:
      - ti-network

volumes:
  postgres_data:
    driver: local

networks:
  ti-network:
    driver: bridge
```

---

## 4. Pipeline de Deploy Automatizado (`deploy.sh`)

Para atualizações rápidas na instância EC2 da AWS:

```bash
#!/bin/bash
set -e

echo "🚀 Iniciando Deploy do Tutor Inteligente na AWS..."

# 1. Atualizar repositório Git
git pull origin main

# 2. Reconstruir e subir os containers em background
docker compose down
docker compose build --no-cache
docker compose up -d

# 3. Executar migrações do banco de dados (Alembic)
docker compose exec ti-backend alembic upgrade head

echo "✅ Deploy concluído com sucesso! Containers ativos."
docker compose ps
```
