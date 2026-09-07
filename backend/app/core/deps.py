"""
Dependências FastAPI compartilhadas para proteção de rotas autenticadas.
Encapsula a extração do Bearer, a decodificação do JWT de acesso e a
validação da sessão única ativa (regra de 1 dispositivo por usuário).

Referências:
- docs-site/docs/implementation/etapa-03-autenticacao.md (seção get_current_user)
- docs-site/docs/modules/autenticacao/business-rules/regras-sessao.md (RN-AUT-011 a RN-AUT-014)
"""
from typing import Tuple
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import TokenService
from app.models.user import Usuario, SessaoAtiva
from app.modules.auth.session_manager import SessionManager


def extrair_bearer_token(request: Request) -> str:
    """Extrai e valida o cabeçalho Authorization no formato Bearer."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho de autorização não fornecido."
        )

    partes = auth_header.strip().split(" ")
    if len(partes) != 2 or partes[0].lower() != "bearer" or not partes[1].strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de token Bearer malformado."
        )

    return partes[1].strip()


async def get_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Tuple[Usuario, SessaoAtiva]:
    """
    Retorna o usuário autenticado e sua sessão ativa.
    Dispara 401 (com detail=CONCURRENT_SESSION_REVOKED) caso a sessão
    tenha sido revogada por login concorrente em outro dispositivo.
    """
    token = extrair_bearer_token(request)

    try:
        payload = TokenService.decodificar_token(token)
        usuario_id = UUID(payload["sub"])
        session_id = UUID(payload["session_id"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso inválido ou expirado."
        )

    sessao = await SessionManager.validar_sessao_ativa(db, session_id, usuario_id)

    usuario = await db.get(Usuario, usuario_id)
    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo ou não encontrado."
        )

    return usuario, sessao


async def get_current_user(
    current: Tuple[Usuario, SessaoAtiva] = Depends(get_current_session)
) -> Usuario:
    """Dependência de conveniência para rotas que precisam apenas do usuário."""
    return current[0]
