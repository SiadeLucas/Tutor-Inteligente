---
title: Onboarding - Serviço de Cadastro Atômico e Inicialização CAT
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Serviço de Cadastro Atômico e Inicialização CAT

Implementação do serviço que consolida a **gravação atômica na tabela `usuarios`**, emissão dos tokens de autenticação e abertura da **sessão diagnóstica da Prova CAT**.

---

## Código Fonte (`backend/app/modules/onboarding/onboarding_service.py`)

```python
from uuid import UUID, uuid4
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.models.user import Usuario
from app.models.exercise import ProvaCat
from app.core.security import hash_senha, TokenService
from app.core.validators import CPFValidator
from app.modules.auth.session_service import SessionManager
from app.modules.onboarding.schemas import (
    FinalizarCadastroRequest,
    CadastroConcluidoResponse
)


class OnboardingService:
    """Orquestrador da finalização de cadastro e transição pedagógica."""

    @staticmethod
    async def finalizar_cadastro(
        db: AsyncSession,
        payload: FinalizarCadastroRequest,
        ip_cliente: str,
        user_agent: str
    ) -> CadastroConcluidoResponse:
        """
        Executa todas as validações de integridade de forma atômica
        e instancia a sessão de avaliação diagnóstica de entrada.
        """
        # 1. Validação matemática estrita do CPF
        if not CPFValidator.validar(payload.etapa1.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O CPF informado é matematicamente inválido."
            )

        # 2. Checagem de unicidade no banco de dados (E-mail e CPF)
        stmt_existente = select(Usuario).where(
            or_(
                Usuario.email == payload.etapa1.email.lower(),
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

        # 3. Cálculo formal de idade e menoridade civil
        hoje = date.today()
        nasc = payload.etapa2.data_nascimento
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        eh_menor = (idade < 18)

        dados_resp = None
        if eh_menor and payload.etapa2.dados_responsavel:
            dados_resp = payload.etapa2.dados_responsavel.dict()

        # 4. Criação atômica do usuário com senha hasheada
        novo_usuario = Usuario(
            id=uuid4(),
            cpf=payload.etapa1.cpf,
            email=payload.etapa1.email.lower(),
            senha_hash=hash_senha(payload.etapa1.senha),
            nome_completo=payload.etapa1.nome_completo,
            data_nascimento=nasc,
            idade_anos=idade,
            eh_menor_idade=eh_menor,
            dados_responsavel=dados_resp,
            cep=payload.etapa3.cep,
            cidade=payload.etapa3.cidade,
            uf=payload.etapa3.uf.upper(),
            escola_tipo=payload.etapa3.escola_tipo,
            nome_escola=payload.etapa3.nome_escola,
            serie_ano=payload.serie_ano,
            role="student",
            ativo=True
        )
        db.add(novo_usuario)
        await db.flush()

        # 5. Criação da sessão inicial autorizada no dispositivo do aluno
        sessao = await SessionManager.registrar_nova_sessao(
            db=db,
            usuario_id=novo_usuario.id,
            ip_address=ip_cliente,
            user_agent=user_agent,
            refresh_token_hash="hash_inicial"
        )

        # 6. Instancia a sessão da Prova Adaptativa Diagnóstica (CAT)
        sessao_cat = ProvaCat(
            id=uuid4(),
            usuario_id=novo_usuario.id,
            disciplina_id=payload.disciplina_id,
            tipo_prova="onboarding_diagnostico",
            theta_geral=0.000,
            erro_padrao_se=1.000,
            scores_grandes_areas={},
            total_itens_aplicados=0,
            itens_respondidos_ids=[]
        )
        db.add(sessao_cat)

        # 7. Emissão dos tokens JWT de autenticação
        access_token = TokenService.criar_access_token(
            usuario_id=novo_usuario.id,
            role=novo_usuario.role,
            session_id=sessao.id
        )

        await db.commit()

        return CadastroConcluidoResponse(
            usuario_id=novo_usuario.id,
            nome_completo=novo_usuario.nome_completo,
            access_token=access_token,
            sessao_id=sessao.id,
            sessao_cat_id=sessao_cat.id
        )
```
