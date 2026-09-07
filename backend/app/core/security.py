"""
Módulo de segurança, criptografia com Argon2id e serviços de token JWT.
"""
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from uuid import UUID

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Contexto criptográfico priorizando Argon2id com fallback seguro para bcrypt
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str) -> str:
    """Gera hash seguro da senha plana utilizando Argon2id."""
    return pwd_context.hash(senha)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Verifica a correspondência da senha contra o hash armazenado."""
    return pwd_context.verify(senha_pura, senha_hash)


def safe_compare(val1: str, val2: str) -> bool:
    """Comparação em tempo constante para mitigar ataques de temporização (Timing Attacks)."""
    return secrets.compare_digest(val1, val2)


class TokenService:
    """Serviço de emissão, decodificação e validação de tokens JWT e tokens aleatórios."""

    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # 15 min
    REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS      # 7 dias
    ALGORITHM = settings.JWT_ALGORITHM                                  # HS256

    @classmethod
    def criar_access_token(cls, usuario_id: UUID, role: str, session_id: UUID) -> str:
        """
        Emite token de curta duração (15 min) para autorização de requisições.
        Contém o identificador do usuário, perfil (role) e session_id ativo.
        """
        expiracao = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(usuario_id),
            "role": role,
            "session_id": str(session_id),
            "exp": expiracao,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def criar_refresh_token(cls, usuario_id: UUID, session_id: UUID) -> str:
        """
        Emite token de longa duração (7 dias) trafegado exclusivamente em cookie seguro HTTP-Only.
        """
        expiracao = datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(usuario_id),
            "session_id": str(session_id),
            "exp": expiracao,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decodificar_token(cls, token: str, is_refresh: bool = False) -> Dict[str, Any]:
        """Decodifica e valida a assinatura criptográfica e a expiração do token JWT."""
        secret = settings.JWT_REFRESH_SECRET_KEY if is_refresh else settings.JWT_SECRET_KEY
        return jwt.decode(token, secret, algorithms=[cls.ALGORITHM])

    @classmethod
    def gerar_token_aleatorio(cls, bytes_len: int = 32) -> str:
        """Gera token criptograficamente seguro e URL-safe para links mágicos."""
        return secrets.token_urlsafe(bytes_len)
