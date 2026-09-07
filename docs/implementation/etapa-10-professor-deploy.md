---
title: "Etapa 10: Painel do Professor e Deploy Final"
type: implementation-step
status: planned
related: []
last_updated: "2026-09-06"
---

<!-- ai-summary
Implementação da área de gestão para docentes (analytics, curadoria e financeiro), estruturação das pipelines de CI/CD via GitHub Actions e deploy completo na AWS com domínio próprio e rotinas de backup.
-->

# Etapa 10: Painel do Professor e Deploy Final

**Duração Estimada:** 1 a 2 semanas  
**Pré-requisitos:** [Etapas 1 a 9](etapa-09-pagamento.md) concluídas  
**Entregável:** Plataforma em produção com domínio próprio configurado, rotinas de backup, CI/CD automatizado e painel de gestão do professor funcionando plenamente.

Nesta etapa final, vamos construir a visão administrativa (Painel do Professor) e colocar nossa aplicação no ar de forma profissional, segura e escalável utilizando a infraestrutura da AWS.

---

## 10.1 Backend: Painel do Professor (Endpoints e Analytics Otimizado)

O painel do professor é a central de comando da plataforma. Ele precisa de proteção específica e de consultas de banco de dados muito bem otimizadas (evitando o temido problema N+1), pois consolidará dados de toda a plataforma.

### 10.1.1 Proteção de Rota (Middleware/Dependency)

Crie uma dependência no FastAPI que verifique se o usuário logado possui a role (perfil) de professor.

```python
# app/api/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from app.api.dependencies.auth import get_current_user
from app.models.user import User

async def require_teacher_role(current_user: User = Depends(get_current_user)):
    """Garante que apenas professores acessem o endpoint."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao corpo docente."
        )
    return current_user
```

### 10.1.2 Endpoints do Professor

Vamos implementar 6 endpoints estratégicos no router `teacher.py`:

```python
# app/api/v1/endpoints/teacher.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_session
from app.api.dependencies.auth import require_teacher_role

router = APIRouter(prefix="/teacher", tags=["Professor"], dependencies=[Depends(require_teacher_role)])

@router.get("/analytics")
async def get_dashboard_analytics(session: AsyncSession = Depends(get_session)):
    """
    1. Dashboard com faturamento líquido, alunos ativos e distribuição demográfica 
    (escola pública vs privada, UF).
    Use subqueries e GROUP BY para agregar esses dados eficientemente.
    """
    pass

@router.get("/alunos")
async def listar_alunos(page: int = 1, limit: int = 20, search: str = None, session: AsyncSession = Depends(get_session)):
    """
    2. Listagem paginada SEM N+1 queries.
    Utilize `selectinload` ou `joinedload` do SQLAlchemy e queries de contagem agregadas.
    """
    pass

@router.get("/alunos/{aluno_id}")
async def get_dossie_aluno(aluno_id: int, session: AsyncSession = Depends(get_session)):
    """
    3. Dossiê pedagógico individual (desempenho em exercícios, progresso de aulas).
    """
    pass

@router.put("/curadoria/aulas/{capitulo_id}")
async def atualizar_aula(capitulo_id: int, payload: dict, session: AsyncSession = Depends(get_session)):
    """
    4. Curadoria de conteúdo KaTeX dos blocos 1, 2, 3 e URL de vídeo.
    Permite ao professor editar o conteúdo instrucional da aula.
    """
    pass

@router.get("/financeiro/extrato")
async def get_extrato_financeiro(session: AsyncSession = Depends(get_session)):
    """
    5. Extrato financeiro, detalhando entradas, taxas do Asaas retidas e saldo líquido.
    """
    pass

@router.post("/matriculas/{matricula_id}/estorno")
async def processar_estorno(matricula_id: int, session: AsyncSession = Depends(get_session)):
    """
    6. Estorno administrativo dentro dos 7 dias (CDC).
    Comunica com a API do Asaas para realizar o reembolso (refund).
    """
    pass
```

> [!TIP]
> **Performance:** Para o dashboard analítico, crie índices compostos no banco (ex: status do usuário + tipo de escola) para acelerar a geração dos gráficos de distribuição demográfica.

---

## 10.2 Frontend: Telas do Professor (`/teacher`)

Crie uma área restrita no Next.js (`app/teacher/layout.tsx`) com navegação lateral específica.

### Funcionalidades do Frontend

1. **Modo Visão do Aluno:** 
   Um botão no header que, ao ser clicado, altera um estado no contexto de autenticação e redireciona o professor para o `/dashboard` com uma flag (ex: `?view=student`), permitindo-lhe navegar como se fosse um aluno para validar o conteúdo.
2. **Dashboard Demográfico:**
   Use a biblioteca [Recharts](https://recharts.org/) para plotar gráficos de pizza (Pública vs Privada) e gráficos de barra (alunos por UF e faturamento mensal).
3. **Gestão de Alunos:**
   Uma tabela usando Tailwind (ou Shadcn UI) com campo de busca (nome, CPF, email) com debounce, e modais para abrir o "Dossiê do Aluno" detalhando acertos e erros na Antigravity.
4. **Painel Financeiro:**
   Exibição clara de saldo, lista de transações recentes, e um botão vermelho cauteloso para "Realizar Estorno" (com duplo modal de confirmação).

### Central de Curadoria (Editor Split-Screen)

Para a edição de aulas, crie um editor visual em tempo real para o KaTeX.

```tsx
// app/teacher/curadoria/page.tsx (Simplificado)
"use client";
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

export default function CuradoriaEditor() {
  const [content, setContent] = useState<string>("## Bloco 1\nFórmula da Gravitação Universal:\n$$ F = G \\frac{m_1 m_2}{d^2} $$");

  return (
    <div className="flex h-screen w-full">
      {/* Editor à esquerda */}
      <div className="w-1/2 p-4 border-r">
        <textarea 
          className="w-full h-full p-4 font-mono text-sm bg-gray-50 border rounded-md"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
      </div>
      
      {/* Preview à direita */}
      <div className="w-1/2 p-8 overflow-y-auto bg-white prose prose-slate max-w-none">
        <ReactMarkdown 
          remarkPlugins={[remarkMath]} 
          rehypePlugins={[rehypeKatex]}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}
```

---

## 10.3 Pipeline de CI/CD Completo (GitHub Actions)

A automação é essencial para um solo developer. Vamos configurar duas pipelines no GitHub.

### 1. Pipeline de Testes (`.github/workflows/tests.yml`)

Valida todo o código antes de qualquer merge.

```yaml
name: Tests and Lint

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: tutor_test
        ports:
          - 5432:5432
      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest flake8
    - name: Lint with flake8
      run: flake8 backend/
    - name: Test with pytest
      env:
        DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/tutor_test
        REDIS_URL: redis://localhost:6379/0
      run: pytest backend/tests/

  frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    - name: Install dependencies
      run: cd frontend && npm ci
    - name: Lint and Typecheck
      run: |
        cd frontend
        npm run lint
        npx tsc --noEmit
    - name: Test (Vitest)
      run: cd frontend && npm run test
```

### 2. Pipeline de Deploy (`.github/workflows/deploy-aws.yml`)

Publica as alterações na AWS após o sucesso dos testes.

```yaml
name: Deploy to AWS EC2

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    needs: [backend, frontend] # Requer que a pipeline anterior passe
    runs-on: ubuntu-latest
    steps:
    - name: Deploy via SSH
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ${{ secrets.EC2_USER }}
        key: ${{ secrets.EC2_SSH_KEY }}
        script: |
          cd /home/ubuntu/tutor-inteligente
          git pull origin main
          docker compose -f docker-compose.prod.yml build
          docker compose -f docker-compose.prod.yml up -d
          docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

> [!IMPORTANT]
> Nunca "commite" chaves SSH ou IPs diretamente. Use a aba **Settings > Secrets and variables > Actions** do seu repositório no GitHub para configurar `EC2_HOST`, `EC2_USER` e `EC2_SSH_KEY`.

---

## 10.4 Configuração de Produção na AWS

### Nginx e Headers de Segurança

Na sua instância EC2, configure o Nginx como proxy reverso para o Docker e adicione as regras de segurança padrão.

```nginx
# /etc/nginx/sites-available/tutor
server {
    server_name seu-dominio.com.br;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self' https://api.asaas.com; img-src 'self' data: https:;";

    # Frontend (Next.js)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

- Execute `certbot --nginx -d seu-dominio.com.br` para gerar e configurar o certificado SSL gratuito (Let's Encrypt).

### Backup Automatizado para S3

Crie um script na EC2 (`/home/ubuntu/backup.sh`) e adicione no cron (`crontab -e`) para rodar diariamente às 03:00 da manhã.

```bash
#!/bin/bash
# Requer aws-cli configurado (aws configure) na EC2
BACKUP_NAME="db_$(date +%Y%m%d_%H%M%S).sql.gz"
S3_BUCKET="s3://tutor-inteligente-backups"

# Extrai o dump do container Postgres em execução
docker exec tutor-db pg_dump -U tutor_admin tutor_inteligente | gzip > /tmp/$BACKUP_NAME

# Envia pro S3
aws s3 cp /tmp/$BACKUP_NAME $S3_BUCKET/$BACKUP_NAME

# Limpa o arquivo local
rm /tmp/$BACKUP_NAME
```

Linha do cron (`0 3 * * * /home/ubuntu/backup.sh`).

---

## 10.5 Homologação Final e Checklist de Go-Live

Antes de abrir o domínio para o público, execute os seguintes roteiros em ambiente de produção:

### Roteiro Aluno End-to-End
1. Acessar a landing page e criar conta de aluno.
2. Realizar o teste CAT (Computerized Adaptive Testing) de nivelamento.
3. Acessar a primeira aula sugerida e ler o bloco teórico.
4. Responder a um exercício (errar de propósito).
5. Interagir com a IA Antigravity pedindo uma dica para a segunda chance.
6. Acertar o exercício.
7. Acessar a área de pagamentos e gerar um PIX (usar ambiente sandbox do Asaas se preferir, ou PIX de centavos em produção).
8. Confirmar a visualização do boletim de desempenho.

### Roteiro Professor
1. Fazer login com credenciais de admin/professor.
2. Acessar o Dashboard e verificar se o aluno recém-criado reflete nos gráficos.
3. Abrir o Dossiê do aluno e ver o histórico do exercício respondido.
4. Editar o conteúdo KaTeX de uma aula via Curadoria e salvar.
5. Usar o botão "Visão do Aluno" para checar a aula alterada.
6. (Opcional) Realizar o estorno da compra teste.

---

## Critérios de Aceitação

- [ ] Rota `/api/v1/teacher/*` protegida exclusivamente para usuários com `role == 'teacher'`.
- [ ] Analytics backend consolidando faturamento, matrículas e dados demográficos em query única ou cacheada.
- [ ] Editor split-screen com renderização de KaTeX em tempo real funcional.
- [ ] Painel do Professor listando alunos com busca e filtros funcionando perfeitamente.
- [ ] GitHub Actions configurado executando lint e testes (Backend + Frontend) via `.github/workflows/tests.yml`.
- [ ] Deploy automatizado via SSH na EC2 acionado após commits na branch `main`.
- [ ] Nginx configurado com proxy reverso, Headers de Segurança e Certificado SSL ativo (HTTPS).
- [ ] DNS apontado corretamente para o IP elástico da EC2 (ou Load Balancer/CloudFront).
- [ ] Script de dump de banco de dados e upload para bucket S3 testado e agendado no Crontab.
- [ ] Roteiros de teste End-to-End do Aluno e do Professor concluídos com sucesso em ambiente de produção.
