"""
Gerenciamento de conexão com o Redis assíncrono.
"""
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings

_redis_pool: Optional[aioredis.ConnectionPool] = None


def get_redis_pool() -> aioredis.ConnectionPool:
    """Retorna o pool singleton de conexões Redis."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=50
        )
    return _redis_pool


def get_redis() -> aioredis.Redis:
    """Retorna cliente Redis assíncrono conectado ao pool."""
    pool = get_redis_pool()
    return aioredis.Redis(connection_pool=pool)


async def close_redis() -> None:
    """Fecha o pool de conexões Redis no encerramento da aplicação."""
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.disconnect()
        _redis_pool = None
