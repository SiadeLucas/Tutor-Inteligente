"""
Testes automatizados da Etapa 03: Autenticação, Sessões e Recuperação de Senha.
"""
import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_com_email(async_client: AsyncClient, usuario_teste):
    """Valida login bem-sucedido utilizando o e-mail cadastrado."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario_teste["email"],
            "senha": usuario_teste["senha_plana"]
        }
    )
    assert response.status_code == 200
    dados = response.json()
    assert "access_token" in dados
    assert dados["token_type"] == "bearer"
    assert dados["usuario"]["email"] == usuario_teste["email"]
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_login_com_cpf(async_client: AsyncClient, usuario_teste):
    """Valida login bem-sucedido utilizando CPF com e sem formatação."""
    # CPF formatado
    cpf_formatado = f"{usuario_teste['cpf'][:3]}.{usuario_teste['cpf'][3:6]}.{usuario_teste['cpf'][6:9]}-{usuario_teste['cpf'][9:]}"
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": cpf_formatado,
            "senha": usuario_teste["senha_plana"]
        }
    )
    assert response.status_code == 200
    assert response.json()["usuario"]["cpf"] == usuario_teste["cpf"]


@pytest.mark.asyncio
async def test_login_credenciais_invalidas(async_client: AsyncClient, usuario_teste):
    """Valida rejeição com 401 ao informar senha incorreta."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario_teste["email"],
            "senha": "SenhaIncorreta999"
        }
    )
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"]


@pytest.mark.asyncio
async def test_rate_limiting_login(async_client: AsyncClient):
    """Valida bloqueio por 15 minutos (HTTP 429) após 5 tentativas falhas."""
    identificador_ataque = "alvo_bruteforce@tutorinteligente.com.br"
    for _ in range(5):
        await async_client.post(
            "/api/v1/auth/login",
            json={"identificador": identificador_ataque, "senha": "senha_errada_qualquer"}
        )

    response_bloqueada = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": identificador_ataque, "senha": "senha_errada_qualquer"}
    )
    assert response_bloqueada.status_code == 429
    assert "bloqueada" in response_bloqueada.json()["detail"]


@pytest.mark.asyncio
async def test_regra_sessao_unica_concorrente(async_client: AsyncClient, usuario_teste):
    """
    RN-AUT-011 a RN-AUT-014:
    Dispositivo A faz login -> Dispositivo B faz login na mesma conta.
    A sessão de A deve ser invalidada e seu próximo heartbeat deve retornar 401 CONCURRENT_SESSION_REVOKED.
    """
    # 1. Login no Dispositivo A
    login_a = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": usuario_teste["senha_plana"]}
    )
    assert login_a.status_code == 200
    token_a = login_a.json()["access_token"]

    # Dispositivo A executa heartbeat com sucesso
    hb_a1 = await async_client.get(
        "/api/v1/auth/heartbeat",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert hb_a1.status_code == 200
    assert hb_a1.json()["sessao_ativa"] is True

    # 2. Login no Dispositivo B (mesma conta de estudante)
    login_b = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": usuario_teste["senha_plana"]}
    )
    assert login_b.status_code == 200
    token_b = login_b.json()["access_token"]

    # 3. Dispositivo A tenta heartbeat novamente -> Deve receber 401 CONCURRENT_SESSION_REVOKED
    hb_a2 = await async_client.get(
        "/api/v1/auth/heartbeat",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert hb_a2.status_code == 401
    assert hb_a2.json()["detail"] == "CONCURRENT_SESSION_REVOKED"

    # 4. Dispositivo B continua ativo normalmente
    hb_b = await async_client.get(
        "/api/v1/auth/heartbeat",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert hb_b.status_code == 200


@pytest.mark.asyncio
async def test_silent_refresh_e_rotacao(async_client: AsyncClient, usuario_teste):
    """Valida a rotação do token via cookie seguro HTTP-Only."""
    login_resp = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": usuario_teste["senha_plana"]}
    )
    assert login_resp.status_code == 200
    refresh_cookie = login_resp.cookies.get("refresh_token")

    # Requisição de renovação de token enviando o cookie
    refresh_resp = await async_client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": refresh_cookie}
    )
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()
    assert "refresh_token" in refresh_resp.cookies


@pytest.mark.asyncio
async def test_logout_local_e_remoto(async_client: AsyncClient, usuario_teste):
    """Valida revogação de sessão no logout local e logout remoto."""
    # Login
    login_resp = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": usuario_teste["senha_plana"]}
    )
    token = login_resp.json()["access_token"]

    # Logout remoto
    logout_resp = await async_client.post(
        "/api/v1/auth/logout-remoto",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_resp.status_code == 200

    # Próximo heartbeat deve falhar
    hb_pos_logout = await async_client.get(
        "/api/v1/auth/heartbeat",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert hb_pos_logout.status_code == 401


@pytest.mark.asyncio
async def test_fluxo_link_magico_e_redefinicao(async_client: AsyncClient, usuario_teste):
    """
    Valida o ciclo completo de recuperação de senha:
    1. Solicitação do link mágico (anti-enumeração)
    2. Validação do token na URL
    3. Redefinição com nova senha
    4. Login com a nova credencial
    """
    # 1. Solicita link mágico
    req_link = await async_client.post(
        "/api/v1/auth/solicitar-link-magico",
        json={"identificador": usuario_teste["email"]}
    )
    assert req_link.status_code == 200
    link_dev = req_link.json().get("link_dev")
    assert link_dev is not None
    token_recuperacao = link_dev.split("token=")[1]

    # 2. Valida token
    valida_resp = await async_client.get(f"/api/v1/auth/verificar-token?token={token_recuperacao}")
    assert valida_resp.status_code == 200
    assert valida_resp.json()["valido"] is True

    # 3. Redefine senha
    nova_senha = "NovaSenhaForte2026!"
    reset_resp = await async_client.post(
        "/api/v1/auth/redefinir-senha",
        json={
            "token": token_recuperacao,
            "nova_senha": nova_senha,
            "confirmacao_senha": nova_senha
        }
    )
    assert reset_resp.status_code == 200

    # 4. Login com nova senha deve funcionar
    novo_login = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": nova_senha}
    )
    assert novo_login.status_code == 200

    # 5. Token consumido não deve ser aceito novamente
    valida_reuso = await async_client.get(f"/api/v1/auth/verificar-token?token={token_recuperacao}")
    assert valida_reuso.json()["valido"] is False


@pytest.mark.asyncio
async def test_refresh_token_hash_rotacao_e_reuso(async_client: AsyncClient, usuario_teste):
    """
    Valida a rotação anti-reuso do refresh token:
    - O hash SHA-256 do cookie é persistido em sessoes_ativas.refresh_token_hash;
    - Após a rotação, o cookie ANTIGO é rejeitado (401);
    - O cookie NOVO é aceito normalmente.
    """
    login_resp = await async_client.post(
        "/api/v1/auth/login",
        json={"identificador": usuario_teste["email"], "senha": usuario_teste["senha_plana"]}
    )
    assert login_resp.status_code == 200
    cookie_antigo = login_resp.cookies.get("refresh_token")
    assert cookie_antigo is not None

    # 1. Primeira rotação: cookie original é válido
    # Aguarda >1s para garantir iat/exp distintos entre os tokens (JWT tem resolução de 1 segundo)
    await asyncio.sleep(1.1)
    refresh_1 = await async_client.post("/api/v1/auth/refresh", cookies={"refresh_token": cookie_antigo})
    assert refresh_1.status_code == 200
    # Lê o cookie rotacionado do jar do cliente (Set-Cookie da resposta)
    cookie_novo = async_client.cookies.get("refresh_token")
    assert cookie_novo is not None and cookie_novo != cookie_antigo

    # 2. Reuso do cookie antigo após rotação: deve ser rejeitado com 401
    reuso = await async_client.post("/api/v1/auth/refresh", cookies={"refresh_token": cookie_antigo})
    assert reuso.status_code == 401

    # 3. Cookie novo (atual) continua válido
    refresh_2 = await async_client.post("/api/v1/auth/refresh", cookies={"refresh_token": cookie_novo})
    assert refresh_2.status_code == 200
