#!/usr/bin/env bash
# ==============================================================================
# Tutor Inteligente — Bootstrap da Instância EC2 (Ubuntu 22.04/24.04 LTS)
# Executar UMA VEZ dentro da instância, como usuário com sudo (ex.: ubuntu):
#   bash infra/scripts/bootstrap-ec2.sh
#
# O que faz:
#   1. Instala Docker Engine + Plugin Compose (via repositório oficial)
#   2. Adiciona o usuário ao grupo docker (sem sudo para docker)
#   3. Configura UFW para permitir apenas SSH(22) e HTTP(80)
#   4. Clona/atualiza o repositório em /home/ubuntu/tutor-inteligente
#   5. Prepara o .env de produção a partir do template (se ainda não existir)
#   6. Sobe a stack completa (migrações + seeds rodam no 1º up / no workflow)
# ==============================================================================
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/SiadeLucas/Tutor-Inteligente.git}"
APP_DIR="${APP_DIR:-$HOME/tutor-inteligente}"

echo "==> [1/6] Instalando Docker Engine + Compose plugin..."
if command -v docker >/dev/null 2>&1; then
  echo "    Docker já instalado: $(docker --version)"
else
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  echo "    Instalado: $(sudo docker --version)"
fi

echo "==> [2/6] Configurando grupo docker para o usuário $(whoami)..."
if id -nG "$(whoami)" | grep -qw docker; then
  echo "    Usuário já pertence ao grupo docker."
else
  sudo usermod -aG docker "$(whoami)"
  echo "    Adicionado ao grupo docker (efetivo em novo login; usando newgrp abaixo)."
fi

echo "==> [3/6] Configurando firewall UFW (SSH 22 + HTTP 80)..."
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow OpenSSH >/dev/null 2>&1 || true
  sudo ufw allow 80/tcp  >/dev/null 2>&1 || true
  sudo ufw --force enable >/dev/null 2>&1 || true
  echo "    UFW ativo. Lembre-se: o Security Group da EC2 também precisa liberar 22 e 80."
else
  echo "    UFW ausente — seguindo apenas com o Security Group da EC2."
fi

echo "==> [4/6] Clonando repositório em $APP_DIR..."
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" fetch origin
  git -C "$APP_DIR" reset --hard origin/main
  echo "    Repositório atualizado para origin/main."
else
  git clone "$REPO_URL" "$APP_DIR"
fi

echo "==> [5/6] Preparando .env de produção..."
cd "$APP_DIR"
if [ -f .env ]; then
  echo "    .env já existe — mantendo o atual (revise manualmente se necessário)."
else
  cp infra/scripts/env.production.example .env
  echo "    .env criado a partir do template."
  echo ""
  echo "    ⚠️  AÇÃO OBRIGATÓRIA ANTES DE SUBIR:"
  echo "       nano $APP_DIR/.env"
  echo "       - Troque todos os TROQUE_* por segredos fortes (openssl rand -base64 32)"
  echo "       - Cole a GOOGLE_API_KEY real"
  echo "       - Substitua SEU_IP_ELASTICO pelo IP público da instância"
  echo ""
  read -r -p "Deseja editar o .env agora? [s/N] " resp
  if [ "${resp:-n}" = "s" ] || [ "${resp:-n}" = "S" ]; then
    "${EDITOR:-nano}" .env
  fi
fi

echo "==> [6/6] Subindo stack de produção (build inicial ~3-5 min)..."
sudo docker compose -f docker-compose.prod.yml build
sudo docker compose -f docker-compose.prod.yml up -d --remove-orphans
sleep 20
sudo docker compose -f docker-compose.prod.yml ps

PUBLIC_IP=$(curl -fsSL --max-time 5 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "SEU_IP")
echo ""
echo "✅ Bootstrap concluído!"
echo "   Frontend : http://$PUBLIC_IP"
echo "   API docs : http://$PUBLIC_IP/docs"
echo "   Health   : http://$PUBLIC_IP/api/health  (via nginx) ou http://$PUBLIC_IP:8000 bloqueado — use o nginx"
echo ""
echo "   Próximos passos:"
echo "   1. Configure os secrets no GitHub: EC2_HOST, EC2_USER, EC2_SSH_KEY"
echo "   2. Faça push em main para ativar o deploy contínuo"
