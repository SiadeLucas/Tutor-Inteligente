"""
Tutor Inteligente — Ponto de Entrada da API FastAPI
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.redis import close_redis
from app.modules.auth.router import router as auth_router
from app.modules.onboarding.router import router as onboarding_router
from app.modules.content.router import router as content_router
from app.modules.exercises.router import router as exercises_router
from app.modules.progress.router import router as progress_router
from app.modules.payments.router import router as payments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização da aplicação
    yield
    # Finalização de recursos assíncronos
    await close_redis()


app = FastAPI(
    title="Tutor Inteligente API",
    description="API da plataforma EAD de Matemática do Ensino Médio com IA Socrática",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rotas de módulos
app.include_router(auth_router)
app.include_router(onboarding_router)
app.include_router(content_router)
app.include_router(exercises_router)
app.include_router(progress_router)
app.include_router(payments_router)




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
