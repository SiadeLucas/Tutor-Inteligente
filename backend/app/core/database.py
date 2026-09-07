"""
Configuração do banco de dados assíncrono com SQLAlchemy 2.0.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# Engine assíncrono para conexão com o PostgreSQL (asyncpg)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base declarativa compartilhada para todos os modelos ORM
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Injetor de dependência assíncrona de sessão do banco para rotas do FastAPI."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
