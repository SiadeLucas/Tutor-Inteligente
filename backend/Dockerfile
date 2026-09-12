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
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte
COPY . .

# Expor porta do Uvicorn
EXPOSE 8000

# Comando de inicialização (shell-form para expandir UVICORN_RELOAD em dev; prod = sem reload)
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 ${UVICORN_RELOAD:+--reload}
