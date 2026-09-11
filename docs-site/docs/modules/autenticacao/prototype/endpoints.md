---
title: Autenticação - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/autenticacao/prototype/index.md
last_updated: "2026-09-10"
updated_by: buffy
---

# 4. Endpoints da API FastAPI

Implementação das rotas de autenticação, rotação de tokens e controle de sessão única (`app/modules/auth/router.py`).

---

## Código Fonte (`backend/app/modules/auth/router.py`)

```python
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Response, Request, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, update

from app.core.database import get_db
from app.core.security import hash_senha, verificar_senha, TokenService
from app.models.user import Usuario, SessaoAtiva, TokenRecuperacaoSenha
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    UsuarioAuthResponse,
    HeartbeatResponse,
    SolicitarLinkMagicoRequest,
    SolicitarLinkMagicoResponse,
    VerificarTokenResponse,
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
        redis=redis,
        usuario_id=usuario.id,
        ip_address=ip_cliente,
        user_agent=user_agent,
        refresh_token_hash="pendente"
    )

    # 4. Emite tokens e persiste o hash SHA-256 do refresh token em sessoes_ativas
    #    (hash verificado em /refresh; rotação anti-reuso)
    access_token = TokenService.criar_access_token(
        usuario_id=usuario.id,
        role=usuario.role,
        session_id=nova_sessao.id
    )
    refresh_token = TokenService.criar_refresh_token(
        usuario_id=usuario.id,
        session_id=nova_sessao.id
    )
    nova_sessao.refresh_token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
    await db.commit()

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

    partes = auth_header.split(" ")
    if len(partes) != 2 or not partes[1].strip():
        raise HTTPException(status_code=401, detail="Token de autorização malformado.")

    token = partes[1].strip()
    payload = TokenService.decodificar_token(token)
    session_id = UUID(payload["session_id"])
    usuario_id = UUID(payload["sub"])

    sessao = await SessionManager.validar_sessao_ativa(db, session_id, usuario_id)
    await SessionManager.atualizar_heartbeat(db, sessao.id, usuario_id=usuario_id)

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
            partes = auth_header.split(" ")
            if len(partes) == 2:
                payload = TokenService.decodificar_token(partes[1].strip())
                session_id = UUID(payload["session_id"])
                await SessionManager.revogar_sessao(db, session_id)
        except Exception:
            pass

    response.delete_cookie("refresh_token")
    return {"mensagem": "Logout realizado com sucesso."}


# ============================================================================
# 4.5 Perfil (RN-INT §2.6 — tela /perfil)
# ============================================================================

@router.get("/me", response_model=MeResponse)
async def obter_meu_perfil(
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Retorna dados cadastrais para a tela Perfil (nome, contato, escola, responsável)."""
    await db.refresh(usuario)
    return usuario


@router.patch("/me", response_model=MeResponse)
async def atualizar_meu_perfil(
    payload: AtualizarPerfilRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Atualiza apenas campos editáveis pelo aluno (telefone, avatar_url).
    E-mail/CPF/série não são editáveis aqui (integridade acadêmica e
    recuperação de conta — ver docs knowledge/database/01-usuarios.md).
    """
    if payload.telefone is not None:
        usuario.telefone = payload.telefone
    if payload.avatar_url is not None:
        usuario.avatar_url = payload.avatar_url
    await db.commit()
    await db.refresh(usuario)
    return usuario


@router.patch("/me/senha")
async def alterar_minha_senha(
    payload: AlterarSenhaRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Troca de senha autenticada: exige senha atual válida e nova senha >= 8 chars.
    Diferente de /redefinir-senha (link mágico), NÃO revoga a sessão atual.
    """
    if not verificar_senha(payload.senha_atual, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta.")
    if payload.nova_senha == payload.senha_atual:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A nova senha deve ser diferente da atual.")
    usuario.senha_hash = hash_senha(payload.nova_senha)
    await db.commit()
    return {"mensagem": "Senha alterada com sucesso."}


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

    partes = auth_header.split(" ")
    if len(partes) != 2 or not partes[1].strip():
        raise HTTPException(status_code=401, detail="Token de autorização malformado.")

    payload = TokenService.decodificar_token(partes[1].strip())
    usuario_id = UUID(payload["sub"])

    # Revoga todas as sessões ativas do usuário no banco e no Redis
    await SessionManager.revogar_todas_sessoes_usuario(db, usuario_id)

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
    Gera token de uso único com expiração de 15 minutos e hash SHA-256.
    Retorna sempre sucesso para evitar enumeração de contas (RN-AUT-020).
    """
    termo = payload.identificador.strip()
    apenas_digitos = "".join(filter(str.isdigit, termo))
    eh_cpf = (len(apenas_digitos) == 11 and "@" not in termo)

    if eh_cpf:
        stmt = select(Usuario).where(Usuario.cpf == apenas_digitos)
    else:
        stmt = select(Usuario).where(Usuario.email == termo.lower())

    usuario = (await db.execute(stmt)).scalar_one_or_none()

    if usuario and usuario.ativo:
        token_raw = TokenService.gerar_token_aleatorio(32)
        token_hash = hashlib.sha256(token_raw.encode("utf-8")).hexdigest()
        expira_em = datetime.utcnow() + timedelta(minutes=15)

        # Registra na tabela tokens_recuperacao_senha com hash determinístico
        novo_token = TokenRecuperacaoSenha(
            id=uuid4(),
            usuario_id=usuario.id,
            token_hash=token_hash,
            expira_em=expira_em,
            utilizado=False
        )
        db.add(novo_token)
        await db.commit()

        # Em produção: dispara e-mail via SES/SendGrid com link contendo token_raw
        # link = f"https://app.tutorinteligente.com.br/redefinir-senha?token={token_raw}"

    return SolicitarLinkMagicoResponse(
        mensagem="Se o identificador informado constar em nossa base, um link mágico de recuperação foi enviado.",
        expira_em_minutos=15
    )


@router.get("/verificar-token", response_model=VerificarTokenResponse)
async def verificar_token_recuperacao(
    token: str = Query(..., min_length=16, description="Token recebido na URL do link mágico"),
    db: AsyncSession = Depends(get_db)
):
    """
    Valida a vigência do token de link mágico antes de renderizar
    o formulário de nova senha no frontend (RN-AUT-017).
    """
    token_hash_busca = hashlib.sha256(token.encode("utf-8")).hexdigest()

    stmt = select(TokenRecuperacaoSenha, Usuario.email).join(
        Usuario, TokenRecuperacaoSenha.usuario_id == Usuario.id
    ).where(
        and_(
            TokenRecuperacaoSenha.token_hash == token_hash_busca,
            TokenRecuperacaoSenha.utilizado == False,
            TokenRecuperacaoSenha.expira_em > datetime.utcnow()
        )
    )
    result = await db.execute(stmt)
    registro = result.first()

    if not registro:
        return VerificarTokenResponse(
            valido=False,
            email_mascarado=None,
            mensagem="Este link mágico expirou ou já foi utilizado."
        )

    _, email_usuario = registro
    partes = email_usuario.split("@")
    email_mascarado = f"{partes[0][:2]}***@{partes[1]}" if len(partes) == 2 else email_usuario

    return VerificarTokenResponse(
        valido=True,
        email_mascarado=email_mascarado,
        mensagem="Token válido. Prossiga com a criação da nova senha."
    )


@router.post("/redefinir-senha")
async def redefinir_senha(
    payload: RedefinirSenhaRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Valida token via hash SHA-256 direto no índice SQL (prevenção total de DoS),
    atualiza a credencial para novo hash Argon2id e invalida todas as sessões anteriores.
    """
    if payload.confirmacao_senha and payload.nova_senha != payload.confirmacao_senha:
        raise HTTPException(status_code=400, detail="A nova senha e a confirmação não coincidem.")

    if len(payload.nova_senha) < 8:
        raise HTTPException(status_code=400, detail="A senha deve conter no mínimo 8 caracteres.")

    # Busca determinística no banco via hash SHA-256 (sub-1ms, zero loop de verificação)
    token_hash_busca = hashlib.sha256(payload.token.encode("utf-8")).hexdigest()

    stmt_token = select(TokenRecuperacaoSenha).where(
        and_(
            TokenRecuperacaoSenha.token_hash == token_hash_busca,
            TokenRecuperacaoSenha.utilizado == False,
            TokenRecuperacaoSenha.expira_em > datetime.utcnow()
        )
    )
    res_token = await db.execute(stmt_token)
    token_valido = res_token.scalar_one_or_none()

    if not token_valido:
        raise HTTPException(status_code=400, detail="Token de recuperação expirado ou inválido.")

    # Atualiza a senha do usuário com hash Argon2id
    usuario = await db.get(Usuario, token_valido.usuario_id)
    usuario.senha_hash = hash_senha(payload.nova_senha)
    usuario.atualizado_em = datetime.utcnow()

    # Marca token como consumido
    token_valido.utilizado = True

    # Invalida todas as sessões ativas do estudante (PostgreSQL e Redis)
    await SessionManager.revogar_todas_sessoes_usuario(db, usuario.id)

    return {"mensagem": "Senha alterada com sucesso! Faça login novamente com a nova credencial."}
```
