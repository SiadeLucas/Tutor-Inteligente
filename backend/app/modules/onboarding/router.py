"""
Endpoints do Onboarding: validação em tempo real das 3 etapas, rascunho no
Redis, proxy ViaCEP e finalização atômica do cadastro.
Prefixo: /api/v1/onboarding
"""
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.redis import get_redis
from app.core.validators import CPFValidator
from app.models.user import Usuario
from app.modules.onboarding.onboarding_service import DRAFT_TTL_SEGUNDOS, OnboardingService
from app.modules.onboarding.schemas import (
    CadastroConcluidoResponse,
    Etapa1Request,
    Etapa2Request,
    Etapa3Request,
    FinalizarCadastroRequest,
)

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding & Cadastro"])


# ============================================================================
# 1. Validação em Tempo Real da Etapa 1 (Dados Pessoais e CPF)
# ============================================================================

@router.post("/validar-etapa-1", status_code=status.HTTP_200_OK)
async def validar_etapa_1(payload: Etapa1Request, db: AsyncSession = Depends(get_db)):
    """
    Valida o algoritmo matemático do CPF e verifica duplicidade no banco
    antes de liberar a passagem para a Etapa 2. Retorna a idade calculada
    para acionar o bloco do responsável legal.
    """
    if not CPFValidator.validar(payload.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O CPF informado é matematicamente inválido."
        )

    if payload.data_nascimento >= datetime.now().date():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de nascimento deve ser uma data no passado."
        )

    if payload.idade_anos < 6 or payload.idade_anos > 120:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de nascimento inválida. O estudante deve ter entre 6 e 120 anos."
        )

    stmt = select(Usuario).where(Usuario.cpf == payload.cpf)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este CPF já está cadastrado na plataforma.")

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
async def validar_etapa_2(payload: Etapa2Request, db: AsyncSession = Depends(get_db)):
    """
    Valida disponibilidade do e-mail (normalizado em minúsculas) e a
    matematica do CPF do responsável legal, quando presente.
    """
    stmt = select(Usuario).where(Usuario.email == payload.email.lower())
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este endereço de e-mail já está cadastrado.")

    if payload.dados_responsavel:
        if not CPFValidator.validar(payload.dados_responsavel.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O CPF do responsável legal é matematicamente inválido."
            )

    return {"valido": True, "mensagem": "Contato e credenciais válidos."}


# ============================================================================
# 3. Validação da Etapa 3 (Acadêmico e Endereço)
# ============================================================================

@router.post("/validar-etapa-3", status_code=status.HTTP_200_OK)
async def validar_etapa_3(payload: Etapa3Request):
    """Valida o preenchimento dos dados escolares e de endereço."""
    return {"valido": True, "mensagem": "Dados escolares e endereço validados com sucesso."}


# ============================================================================
# 4. Persistência Progressiva de Rascunho (Redis, TTL 48h)
# ============================================================================

@router.post("/salvar-rascunho", status_code=status.HTTP_200_OK)
async def salvar_rascunho(
    payload: dict,
    draft_session_id: str = Header(..., alias="X-Draft-Session-ID"),
):
    """
    Persiste dados parciais das etapas intermediárias no Redis com TTL de
    48 horas, permitindo que o aluno retome o wizard de onde parou.
    """
    redis = get_redis()
    await OnboardingService.salvar_rascunho(redis, draft_session_id, payload)

    return {
        "status": "rascunho_salvo",
        "draft_session_id": draft_session_id,
        "expira_em_segundos": DRAFT_TTL_SEGUNDOS,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/rascunho")
async def obter_rascunho(
    draft_session_id: str = Header(..., alias="X-Draft-Session-ID"),
):
    """
    Recupera os dados parciais preenchidos pelo estudante a partir do Redis.
    Retorna objeto vazio se não houver rascunho (ou se expirou).
    """
    redis = get_redis()
    dados = await OnboardingService.obter_rascunho(redis, draft_session_id)

    return {
        "draft_session_id": draft_session_id,
        "dados_parciais": dados
    }


# ============================================================================
# 5. Consulta Automática de CEP (ViaCEP com timeout de 4s)
# ============================================================================

@router.get("/cep/{cep}")
async def consultar_cep(cep: str):
    """
    Autocompleta cidade, estado, bairro e logradouro a partir do CEP.
    Timeout curto (4s): em caso de instabilidade externa, responde 503 e o
    frontend libera o preenchimento manual dos campos.
    """
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O CEP deve possuir 8 dígitos numéricos.")

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resposta = await client.get(url)
            dados = resposta.json()
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de consulta de CEP temporariamente indisponível. Preencha o endereço manualmente."
        )

    if dados.get("erro"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CEP não localizado nos Correios.")

    return {
        "cep": cep_limpo,
        "cidade": dados.get("localidade"),
        "uf": dados.get("uf"),
        "bairro": dados.get("bairro"),
        "logradouro": dados.get("logradouro")
    }


# ============================================================================
# 6. Finalização Atômica do Cadastro (3 etapas, sem CAT)
# ============================================================================

@router.post("/finalizar-cadastro", response_model=CadastroConcluidoResponse, status_code=status.HTTP_201_CREATED)
async def finalizar_cadastro(
    payload: FinalizarCadastroRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    draft_session_id: str = Header(None, alias="X-Draft-Session-ID"),
):
    """
    Submissão atômica de todas as etapas do wizard:
    1. Revalida CPF (Módulo 11), unicidade e menoridade.
    2. Grava o estudante na tabela usuarios (e-mail minúsculas, UF maiúsculas).
    3. Registra a primeira sessão única ativa com hash SHA-256 do refresh token.
    4. Devolve o access token e injeta o refresh token em cookie HTTP-Only.
    A sessão da Prova CAT só é criada no primeiro acesso a uma matéria (Etapa 7).
    """
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Desconhecido")
    redis = get_redis()

    resultado = await OnboardingService.finalizar_cadastro(
        db=db,
        redis=redis,
        payload=payload,
        ip_cliente=ip_cliente,
        user_agent=user_agent,
        draft_session_id=draft_session_id,
    )

    # Refresh token exclusivamente em cookie HTTP-Only (mesmo padrão da autenticação)
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
