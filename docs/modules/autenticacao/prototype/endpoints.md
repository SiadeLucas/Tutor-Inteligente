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
    # 1. Verificação de Rate Limiting (RN-AUT-019: máx 5 tentativas por 15 min)
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    chave_rate_limit = f"login_attempts:{payload.identificador}:{ip_cliente}"
    
    # Simulação de verificação no Redis (ou SessionManager)
    tentativas_falhas = await SessionManager.obter_tentativas_login(chave_rate_limit)
    if tentativas_falhas >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas inválidas consecutivas. Conta temporariamente bloqueada por 15 minutos."
        )

    # 2. Busca usuário por e-mail ou CPF
    stmt = select(Usuario).where(
        or_(
            Usuario.email == payload.identificador,
            Usuario.cpf == payload.identificador
        )
    )
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()

    if not usuario or not verificar_senha(payload.senha, usuario.senha_hash):
        await SessionManager.incrementar_tentativa_login(chave_rate_limit, ttl_segundos=900)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique seu e-mail/CPF e senha."
        )

    # Limpa histórico de tentativas em caso de sucesso
    await SessionManager.limpar_tentativas_login(chave_rate_limit)

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
# 4. Logout e Logout Remoto
# ============================================================================

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Encerra a sessão ativa no dispositivo atual e limpa o cookie."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = TokenService.decodificar_token(token)
            session_id = UUID(payload["session_id"])
            await SessionManager.revogar_sessao(db, session_id)
        except Exception:
            pass

    response.delete_cookie("refresh_token")
    return {"mensagem": "Logout realizado com sucesso."}


@router.post("/logout-remoto")
async def logout_remoto(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    RN-AUT-015: Invalida TODAS as sessões ativas do estudante em todos os dispositivos,
    forçando novo login geral.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Não autenticado.")

    token = auth_header.split(" ")[1]
    payload = TokenService.decodificar_token(token)
    usuario_id = UUID(payload["sub"])

    # Revoga todas as sessões ativas do usuário
    stmt = (
        update(SessaoAtiva)
        .where(and_(SessaoAtiva.usuario_id == usuario_id, SessaoAtiva.revogado == False))
        .values(revogado=True)
    )
    await db.execute(stmt)
    await db.commit()

    response.delete_cookie("refresh_token")
    return {"mensagem": "Todas as sessões ativas foram desconectadas com sucesso."}


# ============================================================================
# 5. Recuperação por Link Mágico (RN-AUT-016 a RN-AUT-018)
# ============================================================================

@router.post("/solicitar-link-magico", response_model=SolicitarLinkMagicoResponse)
async def solicitar_link_magico(
    payload: SolicitarLinkMagicoRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Gera token assinado de uso único com expiração de 15 minutos e envia por e-mail.
    Retorna sempre sucesso para evitar enumeração de contas (RN-AUT-020).
    """
    stmt = select(Usuario).where(Usuario.email == payload.email)
    usuario = (await db.execute(stmt)).scalar_one_or_none()

    if usuario and usuario.ativo:
        token_raw = TokenService.gerar_token_aleatorio(32)
        token_hash = hash_senha(token_raw)
        expira_em = datetime.utcnow() + timedelta(minutes=15)

        # Registra na tabela tokens_recuperacao_senha
        novo_token = TokenRecuperacaoSenha(
            id=uuid4(),
            usuario_id=usuario.id,
            token_hash=token_hash,
            expira_em=expira_em,
            utilizado=False
        )
        db.add(novo_token)
        await db.commit()

        # Envia e-mail assíncrono com o link direto (simulado no protótipo)
        # link = f"https://app.tutorinteligente.com.br/redefinir-senha?token={token_raw}"

    return SolicitarLinkMagicoResponse(
        mensagem="Se o e-mail informado estiver cadastrado, um link mágico de recuperação foi enviado.",
        expira_em_minutos=15
    )


@router.post("/redefinir-senha")
async def redefinir_senha(
    payload: RedefinirSenhaRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Valida token temporário, atualiza a senha para o novo hash Argon2id
    e invalida TODAS as sessões antigas do usuário (RN-AUT-018).
    """
    if payload.nova_senha != payload.confirmacao_senha:
        raise HTTPException(status_code=400, detail="A nova senha e a confirmação não coincidem.")

    if len(payload.nova_senha) < 8:
        raise HTTPException(status_code=400, detail="A senha deve conter no mínimo 8 caracteres.")

    # Busca token não utilizado e não expirado
    stmt_token = select(TokenRecuperacaoSenha).where(
        and_(
            TokenRecuperacaoSenha.utilizado == False,
            TokenRecuperacaoSenha.expira_em > datetime.utcnow()
        )
    )
    tokens_candidatos = (await db.execute(stmt_token)).scalars().all()
    token_valido = None
    for t in tokens_candidatos:
        if verificar_senha(payload.token, t.token_hash):
            token_valido = t
            break

    if not token_valido:
        raise HTTPException(status_code=400, detail="Token de recuperação expirado ou inválido.")

    # Atualiza a senha do usuário
    usuario = await db.get(Usuario, token_valido.usuario_id)
    usuario.senha_hash = hash_senha(payload.nova_senha)
    usuario.atualizado_em = datetime.utcnow()

    # Marca token como utilizado
    token_valido.utilizado = True

    # Invalida todas as sessões ativas do usuário imediatamente
    stmt_revogar = (
        update(SessaoAtiva)
        .where(SessaoAtiva.usuario_id == usuario.id)
        .values(revogado=True)
    )
    await db.execute(stmt_revogar)
    await db.commit()

    return {"mensagem": "Senha alterada com sucesso! Faça login novamente com a nova credencial."}
```
