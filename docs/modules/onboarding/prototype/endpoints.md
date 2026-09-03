---
title: Onboarding - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Endpoints da API FastAPI

Implementação das rotas de validação passo a passo em tempo real, consulta de CEP e finalização atômica do cadastro (`app/modules/onboarding/router.py`).

---

## Código Fonte (`backend/app/modules/onboarding/router.py`)

```python
import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.database import get_db
from app.models.user import Usuario
from app.core.validators import CPFValidator
from app.modules.onboarding.schemas import (
    Etapa1Request,
    Etapa2Request,
    FinalizarCadastroRequest,
    CadastroConcluidoResponse
)
from app.modules.onboarding.onboarding_service import OnboardingService

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding & Cadastro"])


# ============================================================================
# 1. Validação em Tempo Real da Etapa 1 (Anti-Duplicidade)
# ============================================================================

@router.post("/validar-etapa-1", status_code=status.HTTP_200_OK)
async def validar_etapa_1(
    payload: Etapa1Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Valida formato, algoritmo do CPF e verifica se e-mail ou CPF
    já estão em uso antes de permitir que o estudante avance para a Etapa 2.
    """
    if not CPFValidator.validar(payload.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O CPF informado é matematicamente inválido."
        )

    stmt = select(Usuario).where(
        or_(
            Usuario.email == payload.email.lower(),
            Usuario.cpf == payload.cpf
        )
    )
    res = await db.execute(stmt)
    usuario = res.scalar_one_or_none()

    if usuario:
        if usuario.cpf == payload.cpf:
            raise HTTPException(status_code=409, detail="Este CPF já está cadastrado na plataforma.")
        else:
            raise HTTPException(status_code=409, detail="Este endereço de e-mail já está cadastrado.")

    return {"valido": True, "mensagem": "Credenciais disponíveis para cadastro."}


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
# 3. Finalização Atômica do Cadastro
# ============================================================================

@router.post("/finalizar-cadastro", response_model=CadastroConcluidoResponse)
async def finalizar_cadastro(
    payload: FinalizarCadastroRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Submissão atômica de todas as etapas do Wizard:
    1. Grava o estudante na tabela usuarios.
    2. Registra a primeira sessão autorizada.
    3. Inicializa a sessão da Prova Adaptativa Diagnóstica (CAT).
    4. Devolve tokens e redireciona direto para a avaliação.
    """
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Desconhecido")

    resultado = await OnboardingService.finalizar_cadastro(
        db=db,
        payload=payload,
        ip_cliente=ip_cliente,
        user_agent=user_agent
    )

    return resultado
```
