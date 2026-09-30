# Deploy na AWS EC2 — Tutor Inteligente

Guia para subir a aplicação do zero em uma instância EC2 e ativar o deploy contínuo via GitHub Actions.

## Arquitetura

```
Internet ──> :80 (nginx na EC2)
              ├── /api/  ──> backend  (127.0.0.1:8000)
              ├── /docs  ──> backend  (127.0.0.1:8000)
              └── /      ──> frontend (127.0.0.1:3000)
              Postgres+pgvector e Redis ficam internos (sem porta pública)
```

Postgres, Redis, backend e frontend rodam via `docker-compose.prod.yml`. O nginx ([infra/nginx/tutor.conf](../infra/nginx/tutor.conf)) é instalado direto na EC2 e faz o reverse proxy na porta 80. Migrações Alembic + seeds (63 aulas, 315 itens TRI) rodam automaticamente no deploy.

---

## Etapa 1 — Criar a instância no Console AWS

1. **EC2 → Launch instance**
   - **Name**: `tutor-inteligente-prod`
   - **AMI**: Ubuntu Server 24.04 LTS (ou 22.04), arquitetura `x86_64` — *evite ARM/Graviton: as imagens do compose foram testadas em amd64*
   - **Instance type**: mínimo `t3.medium` (2 vCPU / 4 GB RAM — o build do Next.js + Postgres não cabem bem em `t2.micro`)
   - **Key pair**: crie um novo (ex.: `tutor-ec2`) e **baixe o `.pem`** — é a única chance
   - **Security Group** (crie um novo, ex.: `tutor-sg`):
     | Tipo  | Porta | Source    | Motivo                     |
     |-------|-------|-----------|----------------------------|
     | SSH   | 22    | Seu IP/32 | Administração              |
     | HTTP  | 80    | 0.0.0.0/0 | Site (nginx)               |
     | HTTPS | 443   | 0.0.0.0/0 | Futuro (após Certbot)      |
     - ❌ **NÃO abra** 5432 (Postgres), 6379 (Redis) nem 8000/3000 — tudo fica atrás do nginx
   - **Storage**: 30 GB gp3 (o build do backend consome ~8 GB de imagens)
2. (Recomendado) **EC2 → Elastic IPs → Allocate**: reserve um IP fixo e associe à instância. Sem isso, o IP muda a cada stop/start e o frontend quebra (a URL da API é compilada no build).
3. Lance a instância e anote o **IP público**.

## Etapa 2 — Conectar e rodar o bootstrap

No seu computador (Git Bash / WSL / Linux):

```bash
chmod 400 tutor-ec2.pem
ssh -i tutor-ec2.pem ubuntu@SEU_IP_ELASTICO
```

Dentro da instância, o script [infra/scripts/bootstrap-ec2.sh](../infra/scripts/bootstrap-ec2.sh) faz todo o resto (Docker, UFW, clone, .env, primeiro build):

```bash
git clone https://github.com/SiadeLucas/Tutor-Inteligente.git
bash Tutor-Inteligente/infra/scripts/bootstrap-ec2.sh
```

Durante o bootstrap ele pedirá para editar o `.env`. **Obrigatório**:

```bash
nano ~/tutor-inteligente/.env
```

- Substitua cada `TROQUE_*` por um segredo real: `openssl rand -base64 32`
- Cole a `GOOGLE_API_KEY` (sem ela, tutor IA/RAG/pistas não funcionam)
- Troque **todas** as ocorrências de `SEU_IP_ELASTICO` pelo IP real (afeta `CORS_ORIGINS` e `NEXT_PUBLIC_API_URL`, que é compilada no build do frontend)

## Etapa 3 — Instalar o nginx (reverse proxy na porta 80)

```bash
sudo apt-get install -y nginx
sudo cp ~/tutor-inteligente/infra/nginx/tutor.conf /etc/nginx/sites-available/tutor
sudo sed -i 's/seu-dominio.com.br/SEU_IP_ELASTICO/g; /www\.seu-dominio/d' /etc/nginx/sites-available/tutor
sudo ln -sf /etc/nginx/sites-available/tutor /etc/nginx/sites-enabled/tutor
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

Teste no navegador: `http://SEU_IP_ELASTICO` (frontend) e `http://SEU_IP_ELASTICO/docs` (Swagger).

## Etapa 4 — Ativar o deploy contínuo (GitHub Actions)

1. No servidor, gere uma chave **só para o deploy** e copie a parte privada:

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""
   cat ~/.ssh/github_deploy
   ```

   Adicione a pública ao authorized_keys:

   ```bash
   cat ~/.ssh/github_deploy.pub >> ~/.ssh/authorized_keys
   ```

2. No GitHub: **Settings → Secrets and variables → Actions → New repository secret**:

   | Secret        | Valor                                            |
   |---------------|--------------------------------------------------|
   | `EC2_HOST`    | IP elástico da instância                         |
   | `EC2_USER`    | `ubuntu`                                         |
   | `EC2_SSH_KEY` | Conteúdo **completo** de `~/.ssh/github_deploy` (incluindo `BEGIN`/`END`) |

3. Faça push em `main` (ou use **Actions → Deploy to AWS EC2 → Run workflow**). O workflow [deploy-aws.yml](../.github/workflows/deploy-aws.yml) fará: `git pull` → build → up → `alembic upgrade head` → seeds.

## Etapa 5 — Rotinas de operação

**Backup diário no S3** (script pronto em [infra/scripts/backup.sh](../infra/scripts/backup.sh)):

```bash
# Bucket (uma vez)
aws s3 mb s3://tutor-inteligente-backups --region sa-east-1   # na EC2 com IAM role ou credenciais
# Cron (na EC2)
crontab -e
0 3 * * * /home/ubuntu/tutor-inteligente/infra/scripts/backup.sh >> /var/log/tutor_backup.log 2>&1
```

Comandos úteis na EC2:

```bash
cd ~/tutor-inteligente
docker compose -f docker-compose.prod.yml ps                 # status + healthchecks
docker compose -f docker-compose.prod.yml logs -f backend    # logs da API
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
docker compose -f docker-compose.prod.yml down               # para tudo (dados ficam nos volumes)
```

## Próximos passos (quando houver domínio)

1. Aponte o DNS (A record) do domínio para o IP elástico
2. Edite `/etc/nginx/sites-available/tutor`: restaure `server_name` e a linha `return 301 https://...`
3. Emita TLS gratuito:

   ```bash
   sudo apt-get install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br
   ```

4. Atualize no `.env`: `CORS_ORIGINS=https://seu-dominio.com.br` e `NEXT_PUBLIC_API_URL=https://seu-dominio.com.br`, depois `docker compose -f docker-compose.prod.yml up -d --build frontend backend`

## Checklist rápido de problemas

| Sintoma | Causa provável |
|---|---|
| `502 Bad Gateway` | Containers não subiram — `docker compose -f docker-compose.prod.yml ps` |
| Frontend abre mas login falha | `NEXT_PUBLIC_API_URL` errada no build — recompile o frontend |
| Erro CORS | `CORS_ORIGINS` no `.env` não inclui a origem que acessa |
| Backend reinicia em loop | Ver `.env` faltando variável; `logs -f backend` |
| Disco cheio após builds | `docker system prune -af` (cuidado: remove imagens não usadas) |
