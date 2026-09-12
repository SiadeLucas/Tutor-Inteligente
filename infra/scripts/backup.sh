#!/bin/bash
# ==============================================================================
# Tutor Inteligente — Rotina de Backup Automatizado do PostgreSQL para AWS S3
# Agendamento recomendado no crontab:
# 0 3 * * * /home/ubuntu/tutor-inteligente/infra/scripts/backup.sh >> /var/log/tutor_backup.log 2>&1
# ==============================================================================
set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILENAME="tutor_db_${TIMESTAMP}.sql.gz"
BACKUP_DIR="/tmp/tutor_backups"
S3_BUCKET="${AWS_S3_BACKUP_BUCKET:-s3://tutor-inteligente-backups}"
CONTAINER_NAME="${DB_CONTAINER:-tutor-db-prod}"
DB_USER="${POSTGRES_USER:-tutor_admin}"
DB_NAME="${POSTGRES_DB:-tutor_inteligente}"

mkdir -p "$BACKUP_DIR"

echo "========================================================"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Iniciando rotina de backup..."

# 1. Extrai o dump diretamente do container Postgres em execução
echo "📦 Gerando dump binário compactado via pg_dump..."
docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_DIR/$BACKUP_FILENAME"

# 2. Upload para o bucket S3 seguro (Standard-Infrequent Access para economia)
echo "☁️ Fazendo upload do backup para o bucket $S3_BUCKET..."
aws s3 cp "$BACKUP_DIR/$BACKUP_FILENAME" "$S3_BUCKET/$BACKUP_FILENAME" --storage-class STANDARD_IA

# 3. Limpeza local de segurança
echo "🧹 Removendo arquivo temporário local..."
rm -f "$BACKUP_DIR/$BACKUP_FILENAME"

echo "✅ Backup realizado com sucesso em $S3_BUCKET/$BACKUP_FILENAME"
echo "========================================================"
