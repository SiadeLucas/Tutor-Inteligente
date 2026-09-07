---
title: Onboarding - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 4. Endpoints da API FastAPI

Implementação das rotas de validação passo a passo em tempo real, consulta de CEP e finalização atômica do cadastro (`app/modules/onboarding/router.py`).

---

## Código Fonte (`backend/app/modules/onboarding/router.py`)

```python
import json
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.config import settings
from app.core.database import get_db
from app.core.redis import get_redis
from app.core.security import TokenService
from app.core.validators import CPFValidator
from app.models.user import Usuario
from app.modules.onboarding.schemas import (
    Etapa1Request,
    Etapa2Request,
    Etapa3Request,
    FinalizarCadastroRequest,
    CadastroConcluidoResponse
)
from app.modules.onboarding.onboarding_service import OnboardingService

DRAFT_TTL_SEGUNDOS = 48 * 3600  # 48 horas

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding & Cadastro"])


# ============================================================================
# 1. Validação em Tempo Real da Etapa 1 (Dados Pessoais e CPF)
# ============================================================================

@router.post("/validar-etapa-1", status_code=status.HTTP_200_OK)
async def validar_etapa_1(
    payload: Etapa1Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Valida algoritmo matemático do CPF e verifica duplicidade no banco
    antes de liberar a passagem para a Etapa 2.
    """
    if not CPFValidator.validar(payload.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O CPF informado é matematicamente inválido."
        )

    stmt = select(Usuario).where(Usuario.cpf == payload.cpf)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Este CPF já está cadastrado na plataforma.")

    return {
        "valido": True,
        "idade_anos": payload.idade_anos,
        "eh_menor_idade": payload.eh_menor_idade,
        "mensagem": "Dados pessoais válidos."
    }


# ============================================================================
# 2. Validação da Etapa 2 (Contato, Credenciais e Responsável)
# ============================================================================

@router.post("/validar-etapa-2", status_code=status.HTTP_200_OK)
async def validar_etapa_2(
    payload: Etapa2Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Valida disponibilidade de e-mail e dados obrigatórios do responsável
    se estudante menor de idade.
    """
    stmt = select(Usuario).where(Usuario.email == payload.email.lower())
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Este endereço de e-mail já está cadastrado.")

    if payload.dados_responsavel:
        if not CPFValidator.validar(payload.dados_responsavel.cpf):
            raise HTTPException(status_code=400, detail="O CPF do responsável legal é inválido.")

    return {"valido": True, "mensagem": "Contato e credenciais válidos."}


@router.post("/validar-etapa-3", status_code=status.HTTP_200_OK)
async def validar_etapa_3(payload: Etapa3Request):
    """Valida etapa acadêmica/endereço e formatação da série informada."""
    return {"valido": True, "mensagem": "Dados escolares e endereço validados com sucesso."}


# ============================================================================
# 4. Persistência Progressiva de Rascunho (Redis, TTL 48h)
# ============================================================================

@router.post("/salvar-rascunho", status_code=status.HTTP_200_OK)
async def salvar_rascunho(
    payload: dict,
    draft_session_id: str = Header(..., alias="X-Draft-Session-ID")
):
    """
    Persiste dados parciais das etapas intermediárias na sessão volátil
    (Redis com TTL de 48h) para retorno posterior do aluno.
    """
    redis = get_redis()
    await redis.setex(
        f"onboarding_draft:{draft_session_id}",
        DRAFT_TTL_SEGUNDOS,
        json.dumps(payload)
    )
    return {"status": "rascunho_salvo", "draft_session_id": draft_session_id, "timestamp": datetime.utcnow().isoformat()}


@router.get("/rascunho")
async def obter_rascunho(
    draft_session_id: str = Header(..., alias="X-Draft-Session-ID")
):
    """
    Recupera os dados parciais preenchidos pelo estudante a partir do Redis
    para permitir que continue o preenchimento do wizard de onde parou.
    """
    redis = get_redis()
    dados = await redis.get(f"onboarding_draft:{draft_session_id}")
    return {
        "draft_session_id": draft_session_id,
        "dados_parciais": json.loads(dados) if dados else {}
    }


# ============================================================================
# 2. Consulta Automática de CEP (ViaCEP com Timeout)
# ============================================================================

@router.get("/cep/{cep}")
async def consultar_cep(cep: str):
    """
    Autocompleta cidade, estado e logradouro a partir do CEP informado.
    """
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=400, detail="O CEP deve possuir 8 dígitos numéricos.")

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    async with httpx.AsyncClient(timeout=4.0) as client:
        try:
            resposta = await client.get(url)
            dados = resposta.json()
            if dados.get("erro"):
                raise HTTPException(status_code=404, detail="CEP não localizado nos Correios.")
            return {
                "cidade": dados.get("localidade"),
                "uf": dados.get("uf"),
                "bairro": dados.get("bairro"),
                "logradouro": dados.get("logradouro")
            }
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de consulta de CEP temporariamente indisponível.")


# ============================================================================
# 5. Finalização Atômica do Cadastro
# ============================================================================

@router.post("/finalizar-cadastro", response_model=CadastroConcluidoResponse)
async def finalizar_cadastro(
    payload: FinalizarCadastroRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Submissão atômica de todas as etapas do Wizard (3 etapas, sem CAT):
    1. Grava o estudante na tabela usuarios (com menoridade calculada).
    2. Registra a primeira sessão autorizada (SessionManager).
    3. Devolve o access token e injeta o refresh token em cookie HTTP-Only.
    A sessão da Prova CAT só é criada no primeiro acesso a uma matéria (Etapa 7).
    """
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Desconhecido")

    resultado = await OnboardingService.finalizar_cadastro(
        db=db,
        payload=payload,
        ip_cliente=ip_cliente,
        user_agent=user_agent
    )

    # Injeta o refresh token em cookie HTTP-Only (mesmo padrão do módulo de autenticação)
    eh_desenvolvimento = settings.ENVIRONMENT == "development"
    response.set_cookie(
        key="refresh_token",
        value=resultado.refresh_token,
        httponly=True,
        secure=not eh_desenvolvimento,
        samesite="lax" if eh_desenvolvimento else "strict",
        max_age=7 * 24 * 3600
    )

    return CadastroConcluidoResponse(
        usuario_id=resultado.usuario_id,
        nome_completo=resultado.nome_completo,
        access_token=resultado.access_token,
        sessao_id=resultado.sessao_id
    )
```
