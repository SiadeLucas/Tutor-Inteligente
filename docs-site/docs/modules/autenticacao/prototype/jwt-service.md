---
title: Autenticação - Tokens JWT e Silent Refresh
type: module
status: draft
related:
  - modules/autenticacao/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Serviço de Tokens JWT e Silent Refresh

Implementação dos tokens criptográficos com par assimétrico de validade (15 min para Access Token e 7 dias para Refresh Token com rotação automática).

---

## 1. Serviço Backend em Python (`backend/app/core/security.py`)

```python
import jwt
from uuid import UUID
from datetime import datetime, timedelta
from typing import Dict, Any
from passlib.context import CryptContext

from app.core.config import settings

# Hashing de senhas com Argon2id / bcrypt
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hash)


class TokenService:
    """Gerador e validador de tokens JWT."""

    ACCESS_TOKEN_EXPIRE_MINUTES = 15      # 15 minutos
    REFRESH_TOKEN_EXPIRE_DAYS = 7         # 7 dias

    @classmethod
    def criar_access_token(cls, usuario_id: UUID, role: str, session_id: UUID) -> str:
        """Emite token de curta duração para autorização de requisições."""
        expiracao = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(usuario_id),
            "role": role,
            "session_id": str(session_id),
            "exp": expiracao,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    @classmethod
    def criar_refresh_token(cls, usuario_id: UUID, session_id: UUID) -> str:
        """Emite token de longa duração trafegado exclusivamente em cookie seguro."""
        expiracao = datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(usuario_id),
            "session_id": str(session_id),
            "exp": expiracao,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, algorithm="HS256")

    @classmethod
    def decodificar_token(cls, token: str, is_refresh: bool = False) -> Dict[str, Any]:
        """Decodifica e valida assinatura e expiração."""
        secret = settings.JWT_REFRESH_SECRET_KEY if is_refresh else settings.JWT_SECRET_KEY
        return jwt.decode(token, secret, algorithms=["HS256"])

    @classmethod
    def gerar_token_aleatorio(cls, bytes_len: int = 32) -> str:
        """Gera um token criptograficamente seguro e URL-safe para links mágicos."""
        import secrets
        return secrets.token_urlsafe(bytes_len)
```

---

## 2. Interceptor HTTP de Silent Refresh no Frontend (`frontend/src/lib/api.ts`)

```typescript
import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true, // Garante o envio do cookie HTTP-Only com Refresh Token
});

let isRefreshing = false;
let failedQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token!);
    }
  });
  failedQueue = [];
};

// Interceptor de Resposta: renova silenciosamente no erro 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Se o erro for de sessão concorrente revogada, NÃO tenta refresh
    if (error.response?.data?.detail === "CONCURRENT_SESSION_REVOKED") {
      return Promise.reject(error);
    }

    // Se for 401 por token expirado e ainda não tentou refresh nesta requisição
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Chama endpoint silencioso de refresh (lê cookie HTTP-Only)
        const { data } = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/refresh`,
          {},
          { withCredentials: true }
        );

        const newAccessToken = data.access_token;
        api.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

        processQueue(null, newAccessToken);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        // Refresh Token também expirou: redireciona suave para login
        window.location.href = "/login?sessao_expirada=true";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);
```
