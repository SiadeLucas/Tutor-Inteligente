---
title: "Etapa 11: Guia Operacional de Go-Live e Entrega ao Cliente na AWS"
type: implementation-step
status: active
related:
  - implementation/index.md
  - implementation/etapa-10-professor-deploy.md
last_updated: "2026-09-11"
updated_by: "antigravity"
---

<!-- ai-summary
Manual técnico e operacional para provisionamento definitivo na nuvem AWS, configuração de domínio próprio com SSL gratuito, inicialização do banco de dados em produção e roteiro formal de entrega da plataforma ao cliente contratante.
-->

# Etapa 11: Guia Operacional de Go-Live e Entrega ao Cliente na AWS

**Público-alvo:** Desenvolvedor responsável pelo deploy e Administrador/Cliente Contratante da plataforma.  
**Momento de Execução:** Imediatamente após a ativação da conta na AWS (com cartão de crédito cadastrado).  
**Duração Estimada:** 2 a 4 horas para o deploy completo.  
**Custo Estimado Inicial:** R$ 0,00 a ~R$ 30,00/mês (dentro da faixa de 12 meses do AWS Free Tier).

---

## 1. Contexto e Objetivo desta Etapa

Todas as 10 etapas de desenvolvimento de software da plataforma **Tutor Inteligente** estão 100% concluídas, testadas e integradas no monorepo:
- **Backend:** Autenticação por sessão única via Redis, motor CAT com TRI 3PL Bayesiano, IA Socrática com Gemini Flash via `LLMFactory`, integração com gateway Asaas (PIX e Cartão), geração de Boletim PDF e Painel do Professor analítico.
- **Frontend:** Next.js 14 com design institucional Khan Academy, Skill Tree com 11 volumes didáticos canônicos e 63 aulas KaTeX, editor split-screen de curadoria e painel docente com Recharts.
- **Infraestrutura Pronta:** Arquivos `docker-compose.prod.yml`, `.github/workflows/deploy-aws.yml`, `infra/nginx/tutor.conf` e `infra/scripts/backup.sh` já estão versionados.

Este manual descreve o roteiro exato, passo a passo e sem ambiguidades, para transferir todo o sistema do ambiente local para a nuvem da AWS, publicar com domínio e SSL e fazer a entrega formal com a chave de acesso do cliente.

---

## 2. Visão Geral da Arquitetura em Produção na AWS

```mermaid
flowchart TD
    subgraph Internet["Tráfego Público e Usuários"]
        User["Alunos & Professores\n(Navegador / Mobile)"]
        DNS["DNS do Domínio\n(ex: tutorinteligente.com.br)"]
        AsaasHook["Webhooks de Pagamento\n(api.asaas.com)"]
    end

    subgraph AWS["Infraestrutura na AWS (Cloud)"]
        EIP["IP Elástico Público (IPv4 Fixo)"]
        SG["Security Group\n(Portas 22, 80, 443)"]

        subgraph EC2["Instância EC2 (Ubuntu 24.04 LTS)"]
            Nginx["Proxy Reverso Nginx\n+ Certbot SSL (Let's Encrypt)\nHeaders OWASP (HSTS, CSP)"]
            
            subgraph Docker["Docker Compose de Produção"]
                Front["ti-frontend-prod\n(Next.js 14 - Porta 3000)"]
                Back["ti-backend-prod\n(FastAPI - Porta 8000)"]
                DB["ti-db-prod\n(PostgreSQL 16 + pgvector)"]
                Redis["ti-redis-prod\n(Redis 7 AOF com Senha)"]
            end
            
            Cron["Rotina Cron (03:00)\ninfra/scripts/backup.sh"]
        end

        S3["Bucket S3 Privado\n(Backups Diários compactados)"]
    end

    User --> DNS --> EIP --> SG --> Nginx
    AsaasHook --> DNS
    Nginx -->|/ (Páginas Web)| Front
    Nginx -->|/api/* (REST API)| Back
    Front <--> Back
    Back <--> DB
    Back <--> Redis
    Cron -->|pg_dump + gzip| DB
    Cron -->|aws s3 cp| S3
```

---

## 3. Passo a Passo de Implementação na AWS

### Fase A: Criação e Proteção da Conta AWS

1. **Criar a Conta:**
   - Acesse [aws.amazon.com](https://aws.amazon.com/) e clique em **Criar uma conta da AWS**.
   - Preencha os dados cadastrais e insira o cartão de crédito para verificação de identidade (a AWS realiza uma cobrança temporária de ~$1 USD para validação e estorna em seguida).
   - O plano padrão concede **12 meses de nível gratuito (Free Tier)** para serviços como EC2 (`t3.micro`), EBS (30GB), S3 (5GB) e CloudFront.

2. **Ativar Autenticação Multifator (MFA) na Conta Raiz:**
   - Acesse o console com o e-mail raiz.
   - Navegue até **IAM > Security credentials** e ative o MFA usando um aplicativo autenticador (Google Authenticator, Microsoft Authenticator ou 1Password).

3. **Configurar Alarme de Custos no AWS Budgets (Prevenção de Surpresas):**
   - Acesse **AWS Billing and Cost Management > Budgets**.
   - Clique em **Create budget** > selecione **Zero spend budget** ou **Cost budget**:
     - Defina um limite mensal de **US$ 5.00**.
     - Configure notificações por e-mail para alertar quando o gasto atingir 80%, 100% e 120% do limite.

4. **Criar Usuário IAM para Deploy:**
   - Vá em **IAM > Users > Create user**.
   - Nome: `deploy-tutor`.
   - Permissões: anexar diretamente a política `AdministratorAccess` (ou permissões restritas a EC2 e S3).
   - Na aba **Security credentials**, crie uma **Access Key** (CLI) e guarde com segurança a `Access Key ID` e a `Secret Access Key`.

---

### Fase B: Provisionamento da Instância EC2 e Rede

1. **Selecionar a Região:**
   - No topo superior direito do console, selecione:
     - `us-east-1` (Norte da Virgínia): Mais barato e 100% compatível com Free Tier.
     - Ou `sa-east-1` (São Paulo): Menor latência para o Brasil (latência ~15ms vs ~110ms).

2. **Criar o Par de Chaves SSH (Key Pair):**
   - Acesse **EC2 > Key Pairs > Create key pair**.
   - Nome: `tutor-key`.
   - Formato: `.pem` (para OpenSSH).
   - O arquivo `tutor-key.pem` será baixado na sua máquina. Guarde-o em local seguro (ex: `~/.ssh/tutor-key.pem`).
   - No terminal Linux/macOS ou WSL, ajuste as permissões:
     ```bash
     chmod 400 ~/.ssh/tutor-key.pem
     ```

3. **Criar o Security Group (`tutor-prod-sg`):**
   - Acesse **EC2 > Security Groups > Create security group**.
   - Nome: `tutor-prod-sg`.
   - **Inbound Rules (Regras de Entrada):**
     | Tipo | Protocolo | Porta | Origem | Descrição |
     |:---|:---|:---|:---|:---|
     | **SSH** | TCP | 22 | `Seu IP` (ou `0.0.0.0/0` se IP for dinâmico) | Acesso terminal remoto |
     | **HTTP** | TCP | 80 | `0.0.0.0/0` | Acesso web e desafio Let's Encrypt |
     | **HTTPS** | TCP | 443 | `0.0.0.0/0` | Tráfego criptografado seguro |
   - **Outbound Rules:** Manter `All traffic` liberado para 0.0.0.0/0.

4. **Lançar a Instância EC2:**
   - Acesse **EC2 > Instances > Launch instances**.
   - **Nome:** `tutor-prod-server`.
   - **AMI:** Ubuntu Server 24.04 LTS (HVM), SSD Volume Type, 64-bit (x86).
   - **Tipo de Instância:**
     - `t3.micro` (1 vCPU, 1 GB RAM — 100% gratuita no Free Tier) com Swapfile de 2GB.
     - Ou `t3.small` (2 vCPUs, 2 GB RAM — ~US$ 15/mês, recomendada para maior folga em picos).
   - **Key Pair:** Selecione `tutor-key`.
   - **Network Settings:** Selecione o security group `tutor-prod-sg`.
   - **Armazenamento:** 25 GiB do tipo `gp3` (dentro dos 30 GiB gratuitos).
   - Clique em **Launch instance**.

5. **Alocar e Associar IP Elástico (Elastic IP):**
   > [!IMPORTANT]
   > O IP público padrão da EC2 muda se a máquina for parada. O IP Elástico garante um IPv4 estático definitivo e é **100% gratuito** enquanto estiver associado a uma instância ligada.
   - Acesse **EC2 > Elastic IPs > Allocate Elastic IP address** > clique em **Allocate**.
   - Selecione o IP criado > **Actions > Associate Elastic IP address**.
   - Escolha a instância `tutor-prod-server` e confirme. Anote o IP gerado (ex: `54.232.120.45`).

---

### Fase C: Configuração de Domínio e DNS

1. **Registrar ou Utilizar Domínio Existente:**
   - Exemplo: `tutorinteligente.com.br` no Registro.br, Cloudflare ou AWS Route 53.

2. **Criar os Apontamentos Tipo A na Zona de DNS:**
   - Acesse a gestão de DNS do provedor do domínio e crie dois registros:
     - **Registro A:** Nome `@` (ou vazio) apontando para o seu **IP Elástico** (ex: `54.232.120.45`).
     - **Registro A (ou CNAME):** Nome `www` apontando para o seu **IP Elástico** (ou CNAME para `tutorinteligente.com.br`).
   - A propagação de DNS leva de 5 minutos a 2 horas. Você pode testar se já propagou rodando localmente:
     ```bash
     ping tutorinteligente.com.br
     ```

---

### Fase D: Acesso e Configuração da Instância EC2

1. **Conectar via SSH:**
   ```bash
   ssh -i ~/.ssh/tutor-key.pem ubuntu@54.232.120.45
   ```

2. **Atualizar o Sistema Operacional:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Configurar o Swapfile de 2GB (Essencial para Next.js build):**
   Como a instância `t3.micro` possui 1GB de RAM, o Swap previne estouro de memória durante a compilação do frontend:
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
   Verifique com `free -h` se a memória Swap aparece como 2.0Gi.

4. **Instalar Docker Engine e Docker Compose Plugin:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   # Aplica o grupo sem precisar deslogar:
   newgrp docker
   ```
   Valide com `docker --version` e `docker compose version`.

---

### Fase E: Clonagem do Projeto e Configuração do `.env` de Produção

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/Tutor-Inteligente.git /home/ubuntu/tutor-inteligente
   cd /home/ubuntu/tutor-inteligente
   ```

2. **Criar o Arquivo `.env` de Produção:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   Preencha os valores de produção:
   ```ini
   # Ambiente de Execução
   ENVIRONMENT=production
   DEBUG=False

   # Banco de Dados PostgreSQL de Produção
   DB_NAME=tutor_inteligente
   DB_USER=tutor_admin
   DB_PASSWORD=GereUmaSenhaForteComOpensslAqui_12345
   DATABASE_URL=postgresql+asyncpg://tutor_admin:GereUmaSenhaForteComOpensslAqui_12345@database:5432/tutor_inteligente

   # Cache e Sessões (Redis 7)
   REDIS_PASSWORD=GereOutraSenhaForteRedisAqui_12345
   REDIS_URL=redis://:GereOutraSenhaForteRedisAqui_12345@redis:6379/0

   # Segurança e Tokens JWT
   JWT_SECRET_KEY=ChaveSecretaDePeloMenos64CaracteresAleatoriosGeradaViaOpensslRandHex32
   JWT_REFRESH_SECRET_KEY=OutraChaveSecretaDePeloMenos64CaracteresAleatorios
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7

   # Provedor de IA (Google Gemini)
   GOOGLE_API_KEY=AIzaSySuaChaveRealDoGoogleGeminiFlashAqui
   LLM_PROVIDER=gemini
   LLM_MODEL_NAME=gemini-3.1-flash-lite

   # Gateway de Pagamentos Asaas (MODO PRODUÇÃO)
   ASAAS_API_KEY=$aact_SuaChaveRealDeProducaoDoAsaasAqui
   ASAAS_ENVIRONMENT=production
   ASAAS_WEBHOOK_SECRET_TOKEN=TokenAleatorioParaValidarWebhookAsaas

   # Frontend e CORS (URL pública do frontend, usada como build-arg e para o CORS)
   NEXT_PUBLIC_API_URL=https://tutorinteligente.com.br
   CORS_ORIGINS=https://tutorinteligente.com.br,https://www.tutorinteligente.com.br
   ```

   > [!IMPORTANT]
   > Os nomes acima devem corresponder exatamente aos definidos em `backend/app/core/config.py`. Em particular: a chave do Gemini é `GOOGLE_API_KEY` (não `GEMINI_API_KEY`) e o token do webhook é `ASAAS_WEBHOOK_SECRET_TOKEN` (não `ASAAS_WEBHOOK_SECRET`). O arquivo `docker-compose.prod.yml` referencia os serviços como `database` e `redis` (use esses nomes em `DATABASE_URL` e `REDIS_URL`, não `db`/`postgres`/`backend`). Como o frontend é servido pelo mesmo Nginx, `NEXT_PUBLIC_API_URL` pode ficar vazio — o cliente browser detecta automaticamente a própria origem em HTTPS.

---

### Fase F: Subida dos Containers e Inicialização dos Dados1. **Subir a Stack Docker de Produção:**
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

   > [!IMPORTANT]
   > Como `NEXT_PUBLIC_API_URL` é inlinada no bundle em tempo de **build** (e não em runtime), na AWS ela será lida do `.env` no momento do build. Se precisar alterá-la depois, rode `docker compose -f docker-compose.prod.yml up -d --build frontend` para reconstruir a imagem. Com o Nginx servindo frontend e API no mesmo domínio, recomendamos deixar `NEXT_PUBLIC_API_URL` vazio — o cliente detecta a própria origem automaticamente.

   Verifique se os 4 containers estão saudáveis:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   ```

2. **Executar Migrações do Banco de Dados (Alembic):**
   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
   ```

3. **Sincronizar Acervo dos 11 Volumes Iezzi (Aulas KaTeX e Baterias):**
   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend python -m scripts.seed_content
   ```

4. **Sincronizar 315 Itens Calibrados TRI 3PL:**
   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend python -m scripts.seed_exercises
   ```

5. **Semear Credenciais Iniciais de Administrador/Professor:**
   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend python -m app.db.seed
   ```
   *Isto criará o acesso mestre inicial:*
   - **Login Docente:** `professor@tutorinteligente.com.br` / `SenhaSegura123!` (solicitar troca de senha no primeiro login).
   - **Login Administrador:** `admin@tutorinteligente.com.br` / `SenhaSegura123!`.

---

### Fase G: Proxy Reverso Nginx e Certificado SSL Gratuito (HTTPS)

1. **Instalar Nginx e Certbot no Host:**
   ```bash
   sudo apt install -y nginx certbot python3-certbot-nginx
   ```

2. **Configurar o Nginx com o Arquivo do Projeto:**
   ```bash
   sudo cp /home/ubuntu/tutor-inteligente/infra/nginx/tutor.conf /etc/nginx/sites-available/tutor
   # Substitui 'seu-dominio.com.br' pelo domínio real do cliente:
   sudo sed -i 's/seu-dominio.com.br/tutorinteligente.com.br/g' /etc/nginx/sites-available/tutor
   sudo ln -s /etc/nginx/sites-available/tutor /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. **Emitir Certificado SSL Let's Encrypt com Renovação Automática:**
   ```bash
   sudo certbot --nginx -d tutorinteligente.com.br -d www.tutorinteligente.com.br
   ```
   - Informe seu e-mail de suporte.
   - Aceite os termos de serviço (Y).
   - O Certbot configurará a criptografia HTTPS automaticamente e ativará o redirecionamento automático de HTTP para HTTPS.
   - A renovação já fica agendada no `systemd` / `cron` sem necessidade de intervenção humana.

---

### Fase H: Configuração de Backups Automatizados no S3

1. **Criar o Bucket no Amazon S3:**
   - No console da AWS, vá para **S3 > Create bucket**.
   - Nome: `tutor-inteligente-backups-producao` (nomes de bucket são globais).
   - Mantenha **Block all public access** ativado (100% privado).

2. **Configurar a AWS CLI na EC2:**
   ```bash
   sudo apt install -y awscli
   aws configure
   ```
   Insira a `Access Key ID` e `Secret Access Key` do usuário `deploy-tutor` criado na Fase A.

3. **Testar e Agendar o Script de Backup:**
   ```bash
   chmod +x /home/ubuntu/tutor-inteligente/infra/scripts/backup.sh
   # Teste manual imediato:
   AWS_S3_BACKUP_BUCKET="s3://tutor-inteligente-backups-producao" /home/ubuntu/tutor-inteligente/infra/scripts/backup.sh
   ```
   Verifique no console do S3 se o arquivo `.sql.gz` foi criado.
   Em seguida, adicione no crontab para rodar diariamente às 03:00 da manhã:
   ```bash
   crontab -e
   ```
   Adicione a linha:
   ```cron
   0 3 * * * AWS_S3_BACKUP_BUCKET="s3://tutor-inteligente-backups-producao" /home/ubuntu/tutor-inteligente/infra/scripts/backup.sh >> /var/log/tutor_backup.log 2>&1
   ```

---

### Fase I: Conexão da Pipeline de CI/CD (GitHub Actions)

Para que qualquer commit ou melhoria futura suba para a AWS automaticamente com `git push`:

1. No seu repositório no GitHub, acesse **Settings > Secrets and variables > Actions**.
2. Clique em **New repository secret** e cadastre as 3 chaves:
   - `EC2_HOST`: O IP Elástico da EC2 (ex: `54.232.120.45`).
   - `EC2_USER`: `ubuntu`.
   - `EC2_SSH_KEY`: O conteúdo textual completo do arquivo `tutor-key.pem` (incluindo `-----BEGIN RSA PRIVATE KEY-----` e `-----END RSA PRIVATE KEY-----`).
3. Faça um teste fazendo um push na branch `main`:
   - Acompanhe na aba **Actions** do GitHub.
   - O workflow `.github/workflows/deploy-aws.yml` fará o login via SSH na EC2, rodará o git pull, rebuildará os containers e aplicará migrações em menos de 2 minutos.

---

### Fase J: Ativação do Gateway Asaas em Produção

1. Acesse o painel do Asaas com a conta real da instituição/cliente ([asaas.com](https://www.asaas.com)).
2. Vá em **Configurações da Conta > Integrações > Gerar nova Chave de API**.
3. Copie a chave de produção e atualize no `.env` da EC2 (`ASAAS_API_KEY`).
4. Na mesma tela de Integrações no Asaas, clique em **Webhooks > Adicionar Webhook**:
   - **URL do Webhook:** `https://tutorinteligente.com.br/api/v1/pagamentos/webhook`
   - **E-mail para alertas de falha:** contato@tutorinteligente.com.br
   - **Eventos:** Marque `PAYMENT_RECEIVED`, `PAYMENT_CONFIRMED` e `PAYMENT_REFUNDED`.
   - **Token de Autenticação:** Digite o mesmo valor definido em `ASAAS_WEBHOOK_SECRET` no `.env`.
   - Salve o webhook.

---

## 4. Checklist de Homologação Final e Roteiro de Teste com o Cliente

Antes de entregar formalmente o sistema, realize o seguinte teste de ponta a ponta junto com o cliente:

### Roteiro 1: Experiência do Estudante (End-to-End)
- [ ] Acessar `https://tutorinteligente.com.br` e verificar o cadeado verde de SSL (HTTPS).
- [ ] Criar uma nova conta de estudante informando dados reais (CPF validado matematicamente por Módulo 11).
- [ ] Fazer a prova adaptativa de proficiência CAT inicial.
- [ ] Abrir uma aula (ex: Função Afim no Volume 1) e ler os blocos KaTeX.
- [ ] Resolver um exercício: errar na primeira chance, ler a dica pedagógica socrática da IA e acertar na segunda chance (+0.5 pontos).
- [ ] Gerar um PIX de teste de R$ 1,00 para desbloqueio de um capítulo. Pagar com o app bancário e constatar que a liberação ocorre instantaneamente na tela via Webhook.
- [ ] Baixar o Boletim em PDF com o polígono de proficiência.

### Roteiro 2: Painel de Gestão Docente
- [ ] Fazer login com `professor@tutorinteligente.com.br` e acessar o `/teacher`.
- [ ] Visualizar os 4 cards de KPI atualizados com a compra recém-efetuada.
- [ ] Abrir a tela de **Gestão de Alunos**, localizar o estudante de teste e abrir seu **Dossiê**.
- [ ] Clicar em **Baixar Boletim (PDF)** diretamente pelo painel do professor.
- [ ] Acessar a **Curadoria KaTeX**, editar um texto de aula, visualizar o preview em tempo real e salvar.
- [ ] Clicar no botão **Modo Visão do Aluno** e verificar a visualização idêntica à do estudante.
- [ ] Ir para a aba **Financeiro**, localizar o pagamento de R$ 1,00 e clicar em **Estornar (CDC)**. Confirmar no duplo modal e verificar que o valor é estornado no Asaas e a matrícula é revogada.

---

## 5. Termo de Entrega Técnica e Orientações ao Cliente

Ao finalizar os passos acima, envie a seguinte mensagem formal ao cliente contratante:

> **Prezado(a) [Nome do Cliente],**  
>   
> É com grande satisfação que comunicamos a conclusão e publicação em produção da plataforma **Tutor Inteligente**.  
>   
> **1. Dados de Acesso:**  
> - **Endereço Oficial:** `https://tutorinteligente.com.br`  
> - **Painel Docente & Administrativo:** `https://tutorinteligente.com.br/teacher`  
> - **Usuário Mestre:** `admin@tutorinteligente.com.br`  
> - **Senha Provisória:** `SenhaSegura123!` *(por segurança, altere-a no primeiro acesso)*  
>   
> **2. Infraestrutura e Segurança:**  
> - Ambiente configurado em nuvem dedicada na AWS (EC2 + S3).  
> - Certificado de Segurança SSL (HTTPS) com renovação perpétua automatizada.  
> - Rotina diária de backups do banco de dados agendada para as 03:00 da manhã no Amazon S3.  
> - Gateway de Pagamentos Asaas integrado com conciliação instantânea de PIX e Cartão de Crédito.  
>   
> **3. Acervo Pedagógico Integrado:**  
> - 11 Volumes da Coleção Fundamentos de Matemática Elementar (Gelson Iezzi).  
> - 63 Aulas interativas em 4 blocos instrucionais com fórmulas em KaTeX.  
> - 315 Questões calibradas pela Teoria de Resposta ao Item (TRI 3PL) e motor adaptativo CAT.  
> - Tutor Socrático com IA Gemini Flash integrado para mediação de dúvidas.  
>   
> Ficamos à disposição para o suporte técnico e desejamos excelente trabalho pedagógico com seus estudantes!
