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


@app.get("/", tags=["Infraestrutura"])
async def root():
    """Endpoint raiz com mensagem de boas-vindas."""
    return {
        "message": "Bem-vindo à API do Tutor Inteligente!",
        "docs": "/docs",
        "health": "/health"
    }
