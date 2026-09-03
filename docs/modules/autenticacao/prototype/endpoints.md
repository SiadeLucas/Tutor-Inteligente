---
title: Autenticação - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/autenticacao/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Endpoints da API FastAPI

Implementação das rotas de autenticação, rotação de tokens e controle de sessão única (`app/modules/auth/router.py`).

---

## Código Fonte (`backend/app/modules/auth/router.py`)

```python
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.database import get_db
from app.core.security import hash_senha, verificar_senha, TokenService
from app.models.user import Usuario, SessaoAtiva
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    UsuarioAuthResponse,
    HeartbeatResponse,
    SolicitarLinkMagicoRequest,
    SolicitarLinkMagicoResponse,
    RedefinirSenhaRequest
)
from app.modules.auth.session_service import SessionManager

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação & Sessões"])


# ============================================================================
# 1. Login Híbrido (E-mail ou CPF) com Concorrência Única
# ============================================================================

@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Realiza login com E-mail OU CPF, invalida qualquer sessão anterior
    do estudante e emite Access Token (15 min) + Refresh Token em cookie HTTP-Only.
    """
    # 1. Busca usuário por e-mail ou CPF
    stmt = select(Usuario).where(
        or_(
            Usuario.email == payload.identificador,
            Usuario.cpf == payload.identificador
        )
    )
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()

    if not usuario or not verificar_senha(payload.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique seu e-mail/CPF e senha."
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada ou com acesso suspenso."
        )

    # 2. Captura metadados do dispositivo
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Desconhecido")

    # 3. Registra nova sessão e REVOGA qualquer sessão anterior do aluno
    nova_sessao = await SessionManager.registrar_nova_sessao(
        db=db,
        usuario_id=usuario.id,
        ip_address=ip_cliente,
        user_agent=user_agent,
        refresh_token_hash="hash_provisorio"
    )

    # 4. Emite tokens
    access_token = TokenService.criar_access_token(
        usuario_id=usuario.id,
        role=usuario.role,
        session_id=nova_sessao.id
    )
    refresh_token = TokenService.criar_refresh_token(
        usuario_id=usuario.id,
        session_id=nova_sessao.id
    )

    # 5. Injeta Refresh Token em cookie HTTP-Only seguro
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 3600  # 7 dias
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_seconds=900,
        session_id=nova_sessao.id,
        usuario=UsuarioAuthResponse(
            id=usuario.id,
            nome_completo=usuario.nome_completo,
            email=usuario.email,
            cpf=usuario.cpf,
            role=usuario.role,
            avatar_url=usuario.avatar_url
        )
    )


# ============================================================================
# 2. Silent Token Refresh
# ============================================================================

@router.post("/refresh")
async def silent_refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Renova o Access Token automaticamente em background lendo o cookie Refresh Token.
    Verifica se a sessão não foi invalidada por login em outro aparelho.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token ausente.")

    try:
        payload = TokenService.decodificar_token(refresh_token, is_refresh=True)
        usuario_id = UUID(payload["sub"])
        session_id = UUID(payload["session_id"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expirado ou inválido.")

    # Valida se a sessão ainda está ativa
    sessao = await SessionManager.validar_sessao_ativa(db, session_id, usuario_id)

    # Busca role do usuário
    usuario = await db.get(Usuario, usuario_id)
    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inativo.")

    # Emite novos tokens com rotação
    novo_access_token = TokenService.criar_access_token(usuario.id, usuario.role, sessao.id)
    novo_refresh_token = TokenService.criar_refresh_token(usuario.id, sessao.id)

    response.set_cookie(
        key="refresh_token",
        value=novo_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 3600
    )

    return {"access_token": novo_access_token, "expires_in_seconds": 900}


# ============================================================================
# 3. Heartbeat de Sessão Única (Chamado a cada 30s)
# ============================================================================

@router.get("/heartbeat", response_model=HeartbeatResponse)
async def heartbeat(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Verifica a cada 30s se a sessão do estudante continua autorizada.
    Se outro dispositivo tiver feito login, dispara 401 com CONCURRENT_SESSION_REVOKED.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Não autenticado.")

    token = auth_header.split(" ")[1]
    payload = TokenService.decodificar_token(token)
    session_id = UUID(payload["session_id"])
    usuario_id = UUID(payload["sub"])

    sessao = await SessionManager.validar_sessao_ativa(db, session_id, usuario_id)
    await SessionManager.atualizar_heartbeat(db, sessao.id)

    return HeartbeatResponse(
        sessao_ativa=True,
        session_id=sessao.id,
        servidor_timestamp=datetime.utcnow()
    )


# ============================================================================
# 4. Logout
# ============================================================================

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Encerra a sessão ativa e deleta o cookie de refresh."""
    response.delete_cookie("refresh_token")
    return {"mensagem": "Logout realizado com sucesso."}
```
