"""
Testes automatizados da Etapa 04: Onboarding e Cadastro (wizard de 3 etapas).
Referências: docs-site/docs/implementation/etapa-04-onboarding.md (seção 4.6)
"""
import hashlib
import re
import uuid as uuid_module

import pytest
from httpx import AsyncClient
from sqlalchemy import delete, select

from app.models.user import SessaoAtiva, TokenRecuperacaoSenha, Usuario


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gerar_cpf_valido(seed: str) -> str:
    """Gera um CPF matematicamente válido (Módulo 11) a partir de 9 dígitos base."""
    base = re.sub(r"\D", "", seed)[:9].ljust(9, "0")

    def digito(digs: str) -> str:
        soma = sum(int(d) * (len(digs) + 1 - i) for i, d in enumerate(digs))
        resto = (soma * 10) % 11
        return "0" if resto in (10, 11) else str(resto)

    cpf = base + digito(base)
    return cpf + digito(cpf)


def prefixo_unico() -> str:
    return uuid_module.uuid4().hex[:10]


def payload_completo(menor: bool = False, com_responsavel: bool = True) -> dict:
    """Payload final do wizard com dados únicos por execução."""
    p = prefixo_unico()
    payload = {
        "etapa1": {
            "nome_completo": f"Aluno Onboarding {p}",
            "cpf": gerar_cpf_valido(p + "123456"),
            "data_nascimento": "2012-05-10" if menor else "2000-05-20",
            "genero": "masculino",
        },
        "etapa2": {
            "email": f"aluno_{p}@onboarding-teste.com.br",
            "senha": "SenhaForte123@",
            "confirmacao_senha": "SenhaForte123@",
            "telefone": "(11) 98765-4321",
        },
        "etapa3": {
            "cep": "01310100",
            "uf": "sp",
            "cidade": "São Paulo",
            "bairro": "Bela Vista",
            "logradouro": "Avenida Paulista",
            "numero": "1000",
            "escola_tipo": "publica",
            "nome_escola": "E.E. Teste",
            "serie_ano": "3_ano",
        },
    }
    if menor and com_responsavel:
        payload["etapa2"]["dados_responsavel"] = {
            "nome_completo": f"Responsável Legal {p}",
            "cpf": gerar_cpf_valido(p + "987654"),
            "telefone": "11987654321",
            "email": None,
        }
    return payload


async def limpar_usuario(db_session, email: str, cpf: str) -> None:
    """Remove o usuário de teste e registros dependentes."""
    stmt = select(Usuario).where((Usuario.email == email) | (Usuario.cpf == cpf))
    usuario = (await db_session.execute(stmt)).scalar_one_or_none()
    if usuario:
        await db_session.execute(delete(SessaoAtiva).where(SessaoAtiva.usuario_id == usuario.id))
        await db_session.execute(delete(TokenRecuperacaoSenha).where(TokenRecuperacaoSenha.usuario_id == usuario.id))
        await db_session.delete(usuario)
        await db_session.commit()


# ---------------------------------------------------------------------------
# Etapa 1: CPF e dados pessoais
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_validar_etapa_1_cpf_invalido(async_client: AsyncClient):
    """CPF matematicamente inválido (dígito verificador errado) deve retornar 400."""
    response = await async_client.post(
        "/api/v1/onboarding/validar-etapa-1",
        json={
            "nome_completo": "Aluno Teste",
            "cpf": "529.982.247-24",
            "data_nascimento": "2000-05-20",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_validar_etapa_1_cpf_duplicado(async_client: AsyncClient, db_session, usuario_teste):
    """CPF já cadastrado deve retornar 409 Conflict (RN-ONB-002)."""
    try:
        response = await async_client.post(
            "/api/v1/onboarding/validar-etapa-1",
            json={
                "nome_completo": "Duplicado Teste",
                "cpf": usuario_teste["cpf"],
                "data_nascimento": "2000-05-20",
            },
        )
        assert response.status_code == 409
    finally:
        await limpar_usuario(db_session, usuario_teste["email"], usuario_teste["cpf"])


@pytest.mark.asyncio
async def test_validar_etapa_1_calcula_menoridade(async_client: AsyncClient):
    """Etapa 1 válida deve retornar idade e flag de menoridade calculadas."""
    response = await async_client.post(
        "/api/v1/onboarding/validar-etapa-1",
        json={
            "nome_completo": "Aluno Menor Teste",
            "cpf": gerar_cpf_valido(prefixo_unico() + "111222"),
            "data_nascimento": "2012-05-10",
        },
    )
    assert response.status_code == 200
    dados = response.json()
    assert dados["valido"] is True
    assert dados["eh_menor_idade"] is True
    assert dados["idade_anos"] < 18


@pytest.mark.asyncio
async def test_validar_etapa_1_data_nascimento_ano_1500_rejeitada(async_client: AsyncClient):
    """Data de nascimento de 1500 (>120 anos) deve ser rejeitada com 422."""
    response = await async_client.post(
        "/api/v1/onboarding/validar-etapa-1",
        json={
            "nome_completo": "Aluno Matusalem",
            "cpf": gerar_cpf_valido(prefixo_unico() + "333444"),
            "data_nascimento": "1500-01-01",
        },
    )
    assert response.status_code == 422
    assert "120" in response.text


@pytest.mark.asyncio
async def test_validar_etapa_1_idade_minima_rejeitada(async_client: AsyncClient):
    """Estudante com menos de 6 anos deve ser rejeitado com 422."""
    response = await async_client.post(
        "/api/v1/onboarding/validar-etapa-1",
        json={
            "nome_completo": "Bebe Teste",
            "cpf": gerar_cpf_valido(prefixo_unico() + "555666"),
            "data_nascimento": "2024-01-01",
        },
    )
    assert response.status_code == 422
    assert "6" in response.text


# ---------------------------------------------------------------------------
# Etapa 2: e-mail, telefone e responsável
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_validar_etapa_2_email_duplicado(async_client: AsyncClient, db_session, usuario_teste):
    """E-mail já cadastrado deve retornar 409 Conflict (RN-ONB-003)."""
    try:
        response = await async_client.post(
            "/api/v1/onboarding/validar-etapa-2",
            json={
                "email": usuario_teste["email"].upper(),  # normalização case-insensitive
                "senha": "SenhaForte123@",
                "confirmacao_senha": "SenhaForte123@",
                "telefone": "11987654321",
            },
        )
        assert response.status_code == 409
    finally:
        await limpar_usuario(db_session, usuario_teste["email"], usuario_teste["cpf"])


@pytest.mark.asyncio
async def test_telefone_obrigatorio(async_client: AsyncClient):
    """Telefone com menos de 10 dígitos deve ser rejeitado pela validação da Etapa 2."""
    response = await async_client.post(
        "/api/v1/onboarding/validar-etapa-2",
        json={
            "email": f"{prefixo_unico()}@onboarding-teste.com.br",
            "senha": "SenhaForte123@",
            "confirmacao_senha": "SenhaForte123@",
            "telefone": "119",
        },
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Finalização atômica do cadastro
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_minor_requires_responsavel(async_client: AsyncClient, db_session):
    """Menor de 18 anos sem dados do responsável deve retornar 400 (RN-ONB-005)."""
    payload = payload_completo(menor=True, com_responsavel=False)
    email = payload["etapa2"]["email"]
    cpf = payload["etapa1"]["cpf"]
    try:
        response = await async_client.post("/api/v1/onboarding/finalizar-cadastro", json=payload)
        # 422: o model_validator do schema bloqueia antes da rota (defesa em profundidade:
        # o serviço também recusaria com 400 se o bloco fosse injetado sem validação)
        assert response.status_code == 422
        assert "respons" in response.text
    finally:
        await limpar_usuario(db_session, email, cpf)


@pytest.mark.asyncio
async def test_duplicate_cpf_rejection(async_client: AsyncClient, db_session, usuario_teste):
    """Finalização com CPF existente deve retornar 409 detalhado."""
    payload = payload_completo()
    payload["etapa1"]["cpf"] = usuario_teste["cpf"]
    try:
        response = await async_client.post("/api/v1/onboarding/finalizar-cadastro", json=payload)
        assert response.status_code == 409
        assert "CPF" in response.json()["detail"]
    finally:
        await limpar_usuario(db_session, usuario_teste["email"], usuario_teste["cpf"])


@pytest.mark.asyncio
async def test_complete_registration_flow(async_client: AsyncClient, db_session):
    """
    Fluxo completo: payload final válido cria o usuário no PostgreSQL
    (incl. genero/telefone/logradouro/numero), abre sessão única com hash
    SHA-256 do refresh token, emite JWT e cookie HTTP-Only, e permite login.
    """
    payload = payload_completo()
    email = payload["etapa2"]["email"]
    cpf = payload["etapa1"]["cpf"]
    try:
        response = await async_client.post(
            "/api/v1/onboarding/finalizar-cadastro",
            json=payload,
            headers={"X-Draft-Session-ID": prefixo_unico()},
        )
        assert response.status_code == 201, response.text
        dados = response.json()

        assert dados["token_type"] == "bearer"
        assert "access_token" in dados
        assert "refresh_token" not in dados  # cookie HTTP-Only, nunca no corpo
        assert "refresh_token" in response.cookies

        # Persistência com os novos campos do dicionário de dados
        usuario = (await db_session.execute(select(Usuario).where(Usuario.cpf == cpf))).scalar_one()
        assert usuario.email == email.lower()
        assert usuario.genero == "masculino"
        assert usuario.telefone == "11987654321"
        assert usuario.logradouro == "Avenida Paulista"
        assert usuario.numero == "1000"
        assert usuario.uf == "SP"
        assert usuario.idade_anos >= 18
        assert usuario.eh_menor_idade is False

        # Hash SHA-256 do refresh token persistido na sessão única
        cookie = response.cookies.get("refresh_token")
        sessao = (
            await db_session.execute(
                select(SessaoAtiva).where(SessaoAtiva.usuario_id == usuario.id)
            )
        ).scalar_one()
        assert sessao.refresh_token_hash == hashlib.sha256(cookie.encode("utf-8")).hexdigest()

        # Login imediato com as credenciais criadas (e-mail em minúsculas)
        login = await async_client.post(
            "/api/v1/auth/login",
            json={"identificador": email.upper(), "senha": "SenhaForte123@"},
        )
        assert login.status_code == 200
        assert login.json()["usuario"]["email"] == email.lower()
    finally:
        await limpar_usuario(db_session, email, cpf)


@pytest.mark.asyncio
async def test_minor_completo_com_responsavel(async_client: AsyncClient, db_session):
    """Menor de idade com responsável legal é persistido como JSONB (RN-ONB-005)."""
    payload = payload_completo(menor=True, com_responsavel=True)
    email = payload["etapa2"]["email"]
    cpf = payload["etapa1"]["cpf"]
    try:
        response = await async_client.post("/api/v1/onboarding/finalizar-cadastro", json=payload)
        assert response.status_code == 201, response.text

        usuario = (await db_session.execute(select(Usuario).where(Usuario.cpf == cpf))).scalar_one()
        assert usuario.eh_menor_idade is True
        assert usuario.dados_responsavel is not None
        assert usuario.dados_responsavel["nome_completo"].startswith("Responsável Legal")
        assert usuario.dados_responsavel["email"] is None
    finally:
        await limpar_usuario(db_session, email, cpf)


@pytest.mark.asyncio
async def test_finalizar_cadastro_suporta_payload_plano(async_client: AsyncClient, db_session):
    """Verifica que o endpoint aceita payload desaninhado (plano) com resiliência total."""
    p = prefixo_unico()
    email = f"plano_{p}@onboarding-teste.com.br"
    cpf = gerar_cpf_valido(p + "777888")
    payload_plano = {
        "nome_completo": f"Aluno Plano {p}",
        "cpf": cpf,
        "data_nascimento": "1998-07-15",
        "genero": "feminino",
        "email": email,
        "senha": "SenhaForte123@",
        "confirmacao_senha": "SenhaForte123@",
        "telefone": "11999998888",
        "cep": "01310100",
        "uf": "sp",
        "cidade": "São Paulo",
        "bairro": "Bela Vista",
        "logradouro": "Av. Paulista",
        "numero": "500",
        "escola_tipo": "privada",
        "serie_ano": "3_ano",
    }
    try:
        response = await async_client.post("/api/v1/onboarding/finalizar-cadastro", json=payload_plano)
        assert response.status_code == 201, response.text
        dados = response.json()
        assert "access_token" in dados
    finally:
        await limpar_usuario(db_session, email, cpf)


# ---------------------------------------------------------------------------
# Rascunho no Redis (TTL 48h)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_draft_save_and_recovery(async_client: AsyncClient):
    """Rascunho salvo é recuperado intacto via header X-Draft-Session-ID."""
    draft_id = prefixo_unico()
    dados_parciais = {
        "etapa1": {"nome_completo": "Aluno Rascunho", "cpf": gerar_cpf_valido("123456789")},
        "etapa_atual": 2,
    }

    salvar = await async_client.post(
        "/api/v1/onboarding/salvar-rascunho",
        json=dados_parciais,
        headers={"X-Draft-Session-ID": draft_id},
    )
    assert salvar.status_code == 200
    assert salvar.json()["expira_em_segundos"] == 172800  # TTL 48h

    recuperacao = await async_client.get(
        "/api/v1/onboarding/rascunho",
        headers={"X-Draft-Session-ID": draft_id},
    )
    assert recuperacao.status_code == 200
    assert recuperacao.json()["dados_parciais"] == dados_parciais


@pytest.mark.asyncio
async def test_draft_inexistente_retorna_vazio(async_client: AsyncClient):
    """Rascunho inexistente (ou expirado) retorna objeto vazio, sem erro."""
    recuperacao = await async_client.get(
        "/api/v1/onboarding/rascunho",
        headers={"X-Draft-Session-ID": f"inexistente_{prefixo_unico()}"},
    )
    assert recuperacao.status_code == 200
    assert recuperacao.json()["dados_parciais"] == {}


@pytest.mark.asyncio
async def test_draft_header_obrigatorio(async_client: AsyncClient):
    """Header X-Draft-Session-ID ausente deve gerar erro de validação (422)."""
    response = await async_client.get("/api/v1/onboarding/rascunho")
    assert response.status_code == 422
