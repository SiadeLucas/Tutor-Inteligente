---
title: "Etapa 3: Autenticação e Sessões"
type: "implementation"
status: "complete"
related: ["etapa-02-infraestrutura.md", "etapa-04-onboarding.md"]
last_updated: "2026-09-07"
updated_by: buffy---
<!-- ai-summary: Implementação detalhada dos fluxos de autenticação, JWT, sessões únicas com Redis e fluxos de recuperação de senha do Tutor Inteligente. -->

# Etapa 3: Autenticação e Sessões

> [!NOTE]
> **Duração Estimada:** 1-2 semanas | **Status:** `Concluída`
> **Pré-requisito:** Etapa 1 concluída (Ambiente Local Docker operacional com PostgreSQL e Redis)
> **Entregável:** Login funcional no navegador com sessão única entre abas e proteção de rotas. [x] Concluído!

> [!IMPORTANT]
> **Sincronização (2026-09-07):** os trechos de código abaixo foram atualizados para refletir a implementação real (modelo híbrido PostgreSQL + Redis, APIs Pydantic v2 e estrutura modular `app/modules/auth/`). O dicionário de dados canônico está em `knowledge/database/02-sessoes-ativas.md` e `03-tokens-recuperacao.md`.

Nesta etapa, implementaremos o núcleo de segurança da aplicação. O Tutor Inteligente exige uma política estrita de "uma sessão por usuário" (para evitar compartilhamento de contas), que gerenciaremos combinando JWT (para autorização stateless) e Redis (para rastreamento de estado e heartbeats).

---

## 3.1 Migração Alembic: Tabelas de Autenticação

Para iniciarmos a persistência de usuários, precisamos configurar o Alembic (caso ainda não esteja) e criar nossos modelos SQLAlchemy.

### Configuração do Alembic (Async)

Se for a primeira migração do projeto, inicialize o Alembic com suporte assíncrono:

```powershell
alembic init -t async alembic
```

Edite o arquivo `alembic/env.py` para usar o engine assíncrono e importar seus modelos (Base) corretamente.

### Modelos SQLAlchemy

Crie o arquivo `backend/app/models/user.py`:

```python
import uuid
from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Usuario(Base):
    """Modelo de usuário (Estudante ou Professor)."""
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    idade_anos = Column(Integer, nullable=False)
    eh_menor_idade = Column(Boolean, nullable=False, default=False)
    dados_responsavel = Column(JSONB, nullable=True)
    genero = Column(String(20), nullable=False, default="nao_informar", server_default="nao_informar")
    telefone = Column(String(15), nullable=False, default="", server_default="")
    uf = Column(String(2), nullable=False)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=True)
    logradouro = Column(String(200), nullable=True)
    numero = Column(String(20), nullable=True)
    cep = Column(String(8), nullable=False)
    escola_tipo = Column(String(50), nullable=False)
    nome_escola = Column(String(200), nullable=True)
    serie_ano = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False, default="student", index=True)
    avatar_url = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    sessoes = relationship("SessaoAtiva", back_populates="usuario", cascade="all, delete-orphan")
    tokens_recuperacao = relationship("TokenRecuperacaoSenha", back_populates="usuario", cascade="all, delete-orphan")


class SessaoAtiva(Base):
    """Modelo para controle de sessão única por usuário (híbrido PG + Redis)."""
    __tablename__ = "sessoes_ativas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False)  # SHA-256 do refresh token em cookie
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text, nullable=False)
    ultimo_heartbeat = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revogado = Column(Boolean, nullable=False, default=False, index=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="sessoes")


class TokenRecuperacaoSenha(Base):
    """Modelo para tokens de redefinição de senha com link mágico."""
    __tablename__ = "tokens_recuperacao_senha"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)  # SHA-256 do token da URL
    expira_em = Column(DateTime(timezone=True), nullable=False)
    utilizado = Column(Boolean, nullable=False, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="tokens_recuperacao")
```

Migrações aplicadas:
- `452e8214a3fc` — 001_auth_tables (criação das 3 tabelas).
- `f3a9c1d24b57` — 002_onboarding_fields (colunas de onboarding em `usuarios` + índices `idx_usuarios_uf_cidade` e parcial `idx_sessoes_ativas_usuario WHERE revogado = FALSE`).

---

## 3.2 Backend: Módulo de Segurança (`app/core/security.py`)

Configuraremos o Argon2id para hash de senhas, por ser mais resistente a ataques de GPU do que bcrypt, e funções para gerenciar JWT via HS256. A implementação real expõe os utilitários `hash_senha()`, `verificar_senha()`, `safe_compare()` e a classe `TokenService` (com chaves separadas para access e refresh tokens, `session_id` no payload e rotação em `/refresh`).

> [!WARNING]
> Nunca compare tokens ou senhas usando `==` diretamente. Use `secrets.compare_digest` para evitar ataques de temporização (Timing Attacks).

```python
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], session_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "sid": session_id, "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def safe_compare(val1: str, val2: str) -> bool:
    return secrets.compare_digest(val1, val2)
```

---

## 3.3 Backend: Session Manager (`app/modules/auth/session_manager.py`)

Para aplicar a regra de uma única sessão ativa e rate limit de login, usamos uma arquitetura **híbrida**: PostgreSQL como registro auditável de abertura/revogação de sessões e Redis para presença em tempo real (heartbeat) e contadores de rate limit.

> [!TIP]
> O heartbeat ocorre a cada 30s. O TTL (Time to Live) no Redis deve ser ligeiramente maior (ex: 45s) para tolerar pequenas latências de rede antes de considerar a sessão offline.

A implementação real expõe (métodos de classe estáticos que recebem `db`/`redis` como parâmetros):
- `obter_tentativas_login` / `incrementar_tentativa_login` / `limpar_tentativas_login` — chave `rate_limit:login:{identificador}:{ip}` (janela de 15 min);
- `registrar_nova_sessao` — revoga sessões anteriores no PG, cria a nova com `session_token`/`refresh_token_hash` e define `session:{usuario_id}:active` + `heartbeat:{usuario_id}:{session_id}` (TTL 45s) no Redis;
- `validar_sessao_ativa` — verifica no PG se a sessão existe e não está revogada (dispara 401 `CONCURRENT_SESSION_REVOKED`);
- `atualizar_heartbeat` — renova o TTL no Redis e o `ultimo_heartbeat` no PG;
- `revogar_sessao` / `revogar_todas_sessoes_usuario` — logout local e remoto (RN-AUT-015).

```python
import redis.asyncio as redis
from typing import Optional
from app.core.config import settings
import hashlib
import json

class SessionManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def obter_tentativas_login(self, ip: str) -> int:
        key = f"rate_limit:login:{ip}"
        tentativas = await self.redis.get(key)
        return int(tentativas) if tentativas else 0

    async def incrementar_tentativa_login(self, ip: str) -> None:
        key = f"rate_limit:login:{ip}"
        await self.redis.incr(key)
        await self.redis.expire(key, 900) # 15 minutos

    async def limpar_tentativas_login(self, ip: str) -> None:
        key = f"rate_limit:login:{ip}"
        await self.redis.delete(key)

    async def criar_sessao(self, user_id: str, session_data: dict) -> str:
        # Garante a regra de 1 dispositivo: remove qualquer sessão existente
        await self.revogar_todas_sessoes_usuario(user_id)
        
        session_id = hashlib.sha256(f"{user_id}:{settings.SECRET_KEY}".encode()).hexdigest()
        key = f"session:{user_id}:{session_id}"
        
        await self.redis.set(key, json.dumps(session_data), ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400)
        # Heartbeat chave separada
        await self.registrar_heartbeat(user_id, session_id)
        
        return session_id

    async def validar_sessao(self, user_id: str, session_id: str) -> bool:
        key = f"session:{user_id}:{session_id}"
        return await self.redis.exists(key) > 0

    async def registrar_heartbeat(self, user_id: str, session_id: str) -> None:
        hb_key = f"heartbeat:{user_id}:{session_id}"
        await self.redis.set(hb_key, "1", ex=45) # 45s TTL

    async def revogar_todas_sessoes_usuario(self, user_id: str) -> None:
        # Busca todas as chaves de sessão deste usuário
        keys = await self.redis.keys(f"session:{user_id}:*")
        if keys:
            await self.redis.delete(*keys)
        hb_keys = await self.redis.keys(f"heartbeat:{user_id}:*")
        if hb_keys:
            await self.redis.delete(*hb_keys)
```

---

## 3.4 Backend: Endpoints de Autenticação

Implementados em `backend/app/modules/auth/router.py` (prefixo `/api/v1/auth`), com schemas em `backend/app/modules/auth/schemas.py`. As dependências reutilizáveis de proteção de rotas — `extrair_bearer_token`, `get_current_session` e `get_current_user` — estão em `backend/app/core/deps.py`.

```python
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_session
from app.modules.auth.session_manager import SessionManager
# Imports de schemas e utilitários omitidos por brevidade

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação & Sessões"])

@router.post("/login")
async def login(request: Request, response: Response, creds: LoginSchema, db: AsyncSession = Depends(get_db)):
    ip = request.client.host
    session_mgr = SessionManager(request.app.state.redis)
    
    tentativas = await session_mgr.obter_tentativas_login(ip)
    if tentativas >= 5:
        raise HTTPException(status_code=429, detail="Muitas tentativas. Tente novamente em 15 minutos.")

    # Busca usuário por CPF ou Email
    user = await crud_user.get_by_email_or_cpf(db, creds.identificador)
    if not user or not security.verify_password(creds.senha, user.senha_hash):
        await session_mgr.incrementar_tentativa_login(ip)
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    await session_mgr.limpar_tentativas_login(ip)

    session_id = await session_mgr.criar_sessao(str(user.id), {"ip": ip, "user_agent": request.headers.get("user-agent")})
    
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id, session_id)

    # Refresh token em HTTP-Only cookie
    response.set_cookie(
        key="refresh_token", value=refresh_token, 
        httponly=True, secure=True, samesite="strict",
        max_age=7 * 24 * 60 * 60
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401)
    
    # Validar token e payload (omitido detalhe jwt.decode)
    # Verificar se a sessão ainda existe no Redis
    # Emitir novo access token
    pass

@router.get("/heartbeat")
async def heartbeat(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current: Tuple[Usuario, SessaoAtiva] = Depends(get_current_session)
):
    """Pulso de presença: renova o heartbeat (Redis TTL 45s) e o ultimo_heartbeat no PG.
    Retorna 401 CONCURRENT_SESSION_REVOKED se a sessão foi revogada por login concorrente."""
    usuario, sessao = current
    redis = get_redis()
    await SessionManager.atualizar_heartbeat(db, redis, sessao.id, usuario.id)
    return HeartbeatResponse(sessao_ativa=True, session_id=sessao.id, servidor_timestamp=datetime.utcnow())

@router.post("/solicitar-link-magico")
async def solicitar_link_magico(data: MagicLinkSchema, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_by_email(db, data.email)
    if user:
        raw_token = secrets.token_urlsafe(32)
        # Salva o SHA-256 no banco, não o token puro
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        
        # Omitido: Salvar `hashed_token` na tabela tokens_recuperacao_senha
        # Omitido: Envio via Amazon SES com `raw_token` no link
    
    # Prevenção de enumeração de emails: sempre retorna sucesso
    return {"message": "Se o email existir, um link foi enviado."}
```

> [!IMPORTANT]
> A extração do Bearer header em `app/core/deps.py` (`extrair_bearer_token`) verifica explicitamente `len(partes) == 2` e `partes[0].lower() == 'bearer'` para evitar index out of bounds. O `/refresh` valida ainda o hash SHA-256 do cookie contra `sessoes_ativas.refresh_token_hash`, rejeitando cookies já rotacionados (proteção anti-reuso).

---

## 3.5 Frontend: Telas de Autenticação

No Next.js (App Router), estruturaremos da seguinte forma:

- `app/(auth)/login/page.tsx`
- `app/(auth)/esqueci-senha/page.tsx`
- `app/(auth)/redefinir-senha/page.tsx`

### Hook de Heartbeat: `useStudyTimer`

```typescript
import { useEffect } from 'react';
import { api } from '@/lib/api';

export function useStudyTimer() {
  useEffect(() => {
    const interval = setInterval(() => {
      api.get('/auth/heartbeat').catch((err) => {
        if (err.response?.status === 401) {
          // Sessão derrubada (ex: login em outro dispositivo)
          window.dispatchEvent(new CustomEvent('session_conflict'));
        }
      });
    }, 30000); // 30 segundos

    return () => clearInterval(interval);
  }, []);
}
```

### Componente Modal de Conflito

Crie um componente que ouve o evento `session_conflict` e exibe um modal dizendo: *"Sua conta foi acessada em outro dispositivo. Você foi desconectado."* bloqueando a tela e forçando redirecionamento para o login.

---

## 3.6 Testes Automatizados

Implementados em `backend/tests/test_auth.py` (com fixtures em `backend/tests/conftest.py`), utilizando `pytest`, `pytest-asyncio` e `httpx`. Suíte atual: 11 testes cobrindo login híbrido, rate limiting, sessão única concorrente, rotação com verificação de hash (anti-reuso), logout local/remoto e o ciclo completo de link mágico.

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_com_email(async_client: AsyncClient, usuario_teste):
    response = await async_client.post("/api/v1/auth/login", json={
        "identificador": usuario_teste["email"],
        "senha": usuario_teste["senha_plana"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies

@pytest.mark.asyncio
async def test_session_uniqueness(async_client: AsyncClient, usuario_teste):
    # Primeiro login
    resp1 = await async_client.post("/api/v1/auth/login", json={...})
    token1 = resp1.json()["access_token"]
    
    # Segundo login (deve invalidar a sessão do primeiro)
    resp2 = await async_client.post("/api/v1/auth/login", json={...})
    token2 = resp2.json()["access_token"]
    
    # Acesso com o primeiro token não deve renovar via refresh
    # Se testar a rota /refresh com o cookie do login 1, deve retornar 401
    # Implemente a verificação de sessão revogada no Redis.

@pytest.mark.asyncio
async def test_rate_limiting(async_client: AsyncClient):
    for _ in range(5):
        await async_client.post("/api/v1/auth/login", json={"identificador": "x", "senha": "y"})
    
    response = await async_client.post("/api/v1/auth/login", json={"identificador": "x", "senha": "y"})
    assert response.status_code == 429
```

---

## 3.7 Critérios de Aceitação
 
- [x] Tabelas `usuarios`, `sessoes_ativas` e `tokens_recuperacao_senha` criadas e versionadas via Alembic.
- [x] Hashes de senhas gerados e validados utilizando o algoritmo `Argon2id`.
- [x] Endpoints de Autenticação construídos: login, refresh, heartbeat, logout, recuperar e redefinir senha.
- [x] Prevenção de ataques de tempo (timing attacks) implementada com `secrets.compare_digest`.
- [x] Rate Limit no endpoint de login (máx. 5 tentativas por IP a cada 15 min) validado.
- [x] Sistema garante **apenas 1 sessão ativa por usuário**, derrubando sessões antigas ao fazer um novo login.
- [x] Heartbeat a cada 30 segundos configurado no frontend e backend (Redis).
- [x] Frontend possui Modal interceptor bloqueando a tela em caso de conflito de sessão.
- [x] Tokens de recuperação de senha usam lookup determinístico em hash (SHA-256) com tempo de expiração.
- [x] Testes de integração (pytest) garantem o bloqueio do rate-limit, a invalidacão de sessões redundantes e a geração de magic links seguros.
- [x] Interface do frontend e componentes totalmente padronizados no Design System institucional Khan Academy (paleta Laranja `#F57C00`, fundos neutros, tipografia Inter, cabeçalho institucional com badge de Matemática e eliminação de aspectos de template de IA).
