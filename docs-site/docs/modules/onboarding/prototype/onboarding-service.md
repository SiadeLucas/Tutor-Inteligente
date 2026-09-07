---
title: Onboarding - Serviço de Cadastro Atômico
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 3. Serviço de Cadastro Atômico

Implementação do serviço que consolida a **gravação atômica na tabela `usuarios`**, emissão dos tokens de autenticação e abertura da **sessão única ativa** (mesma infraestrutura da Etapa 3).

> [!IMPORTANT]
> A sessão da Prova Adaptativa Diagnóstica (CAT) **não é criada aqui**. O wizard de cadastro tem 3 etapas; a sessão CAT é instanciada no primeiro acesso do aluno a uma matéria (motor CAT da Etapa 7).

---

## Código Fonte (`backend/app/modules/onboarding/onboarding_service.py`)

```python
import hashlib
from uuid import uuid4
from datetime import date
from uuid import UUID
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.models.user import Usuario
from app.core.security import hash_senha, TokenService
from app.core.validators import CPFValidator
from app.modules.auth.session_manager import SessionManager
from app.modules.onboarding.schemas import (
    FinalizarCadastroRequest,
    CadastroConcluidoResponse
)


class ResultadoCadastro(BaseModel):
    """Resultado interno: o refresh_token é injetado em cookie HTTP-Only pelo router
    e NUNCA retornado no corpo da resposta (padrão do módulo de autenticação)."""
    usuario_id: UUID
    nome_completo: str
    access_token: str
    refresh_token: str
    sessao_id: UUID


class OnboardingService:
    """Orquestrador da finalização de cadastro do wizard de 3 etapas."""

    @staticmethod
    async def finalizar_cadastro(
        db: AsyncSession,
        payload: FinalizarCadastroRequest,
        ip_cliente: str,
        user_agent: str
    ) -> ResultadoCadastro:
        """
        Executa todas as validações de integridade de forma atômica:
        revalida CPF/e-mail, calcula menoridade, grava o usuário e abre a sessão.
        """
        # 1. Validação matemática estrita do CPF (Módulo 11)
        if not CPFValidator.validar(payload.etapa1.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O CPF informado é matematicamente inválido."
            )

        # 2. Checagem de unicidade no banco (E-mail da Etapa 2 e CPF da Etapa 1)
        stmt_existente = select(Usuario).where(
            or_(
                Usuario.email == payload.etapa2.email.lower(),
                Usuario.cpf == payload.etapa1.cpf
            )
        )
        res_existente = await db.execute(stmt_existente)
        usuario_duplicado = res_existente.scalar_one_or_none()

        if usuario_duplicado:
            if usuario_duplicado.cpf == payload.etapa1.cpf:
                detalhe = "Já existe uma conta cadastrada com este CPF."
            else:
                detalhe = "Já existe uma conta cadastrada com este endereço de e-mail."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detalhe)

        # 3. Cálculo formal de idade e menoridade civil (bissextos inclusos no cálculo)
        hoje = date.today()
        nasc = payload.etapa1.data_nascimento
        if nasc >= hoje:
            raise HTTPException(status_code=400, detail="A data de nascimento deve ser uma data passada.")
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        eh_menor = (idade < 18)

        if eh_menor and not payload.etapa2.dados_responsavel:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estudantes menores de 18 anos exigem obrigatoriamente os dados do responsável legal."
            )

        dados_resp = payload.etapa2.dados_responsavel.model_dump() if payload.etapa2.dados_responsavel else None

        # 4. Criação atômica do usuário com senha hasheada (Argon2id)
        novo_usuario = Usuario(
            id=uuid4(),
            cpf=payload.etapa1.cpf,
            email=payload.etapa2.email.lower(),
            senha_hash=hash_senha(payload.etapa2.senha),
            nome_completo=payload.etapa1.nome_completo,
            data_nascimento=nasc,
            idade_anos=idade,
            eh_menor_idade=eh_menor,
            dados_responsavel=dados_resp,
            genero=payload.etapa1.genero,
            telefone=payload.etapa2.telefone,
            uf=payload.etapa3.uf.upper(),
            cidade=payload.etapa3.cidade,
            bairro=payload.etapa3.bairro,
            logradouro=payload.etapa3.logradouro,
            numero=payload.etapa3.numero,
            cep=payload.etapa3.cep,
            escola_tipo=payload.etapa3.escola_tipo,
            nome_escola=payload.etapa3.nome_escola,
            serie_ano=payload.etapa3.serie_ano,
            role="student",
            avatar_url=payload.etapa1.foto_perfil,
            ativo=True
        )
        db.add(novo_usuario)
        await db.flush()

        # 5. Criação da sessão única ativa (revoga sessões anteriores, grava no PG + Redis)
        sessao = await SessionManager.registrar_nova_sessao(
            db=db,
            redis=None,  # o router injeta o cliente Redis real
            usuario_id=novo_usuario.id,
            ip_address=ip_cliente,
            user_agent=user_agent,
            refresh_token_hash="pendente"
        )

        # 6. Emissão dos tokens JWT e persistência do hash SHA-256 do refresh token
        access_token = TokenService.criar_access_token(
            usuario_id=novo_usuario.id,
            role=novo_usuario.role,
            session_id=sessao.id
        )
        refresh_token = TokenService.criar_refresh_token(
            usuario_id=novo_usuario.id,
            session_id=sessao.id
        )
        sessao.refresh_token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

        await db.commit()
        await db.refresh(novo_usuario)

        return ResultadoCadastro(
            usuario_id=novo_usuario.id,
            nome_completo=novo_usuario.nome_completo,
            access_token=access_token,
            refresh_token=refresh_token,
            sessao_id=sessao.id
        )
```

---

## Notas de Implementação

| Aspecto | Decisão |
|:---|:---|
| **Unicidade CPF/E-mail** | Revalidada dentro da transação final (além das validações por etapa), retornando `409 Conflict`. |
| **E-mail** | Normalizado para minúsculas antes da persistência (`payload.etapa2.email.lower()`), garantindo consistência com o login híbrido da Etapa 3. |
| **UF** | Normalizada para maiúsculas (`uf.upper()`), garantindo o padrão do dicionário de dados. |
| **Rascunho Redis** | Após o commit bem-sucedido, o router deleta `onboarding_draft:{X-Draft-Session-ID}`. |
| **Menoridade** | `dados_responsavel` só é gravado como JSONB se o aluno for menor de idade; caso contrário permanece `NULL`. |
| **Prova CAT** | Fora do escopo do cadastro: nenhuma tabela da Etapa 7 é tocada nesta transação. |
