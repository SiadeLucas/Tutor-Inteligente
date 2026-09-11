"""
Bateria de Testes Automatizados — Módulo de Exercícios e Motor CAT (Etapa 7).
Valida:
1. Submissão com lógica de 2ª chance (1.0 vs 0.5 vs 0.0) e geração de pista socrática.
2. Entrada automática na Caixa de Reforço em caso de erro duplo.
3. Geração de Questões Gêmeas determinísticas a partir de item matriz.
4. Sessão da Prova Adaptativa CAT (inicialização, submissão cega e encerramento).
5. Bateria de fixação por capítulo e consulta da Caixa de Reforço.
"""
import pytest
import pytest_asyncio
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient
from sqlalchemy import select
from app.models.exercise import ItemExercicio, ProvaCat, CaixaReforco
from app.models.content import Capitulo, Disciplina
from app.models.payment import MatriculaPagamento


@pytest_asyncio.fixture(autouse=True)
async def matricular_usuario_teste(usuario_teste, db_session):
    """Concede Passe Global para usuario_teste para permitir testes de exercícios de capítulos."""
    mat = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="passe_global",
        referencia_produto_id=None,
        data_inicio=datetime.now(timezone.utc),
        data_expiracao=datetime.now(timezone.utc) + timedelta(days=365),
        status="active",
        valor_pago=Decimal("199.00"),
        metodo_pagamento="pix",
        transacao_gateway_id="fixture_passe_global_exe",
    )
    db_session.add(mat)
    await db_session.commit()


async def autenticar(async_client: AsyncClient, usuario_teste: dict) -> dict:
    """Helper para efetuar login do usuário de teste."""
    res = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario_teste["email"],
            "senha": usuario_teste["senha_plana"],
        },
    )
    assert res.status_code == 200, f"Falha no login: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_submissao_primeira_tentativa_correta(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    # Busca um item de múltipla escolha
    stmt = select(ItemExercicio).where(ItemExercicio.tipo_item == "multiple_choice")
    item = (await db_session.execute(stmt)).scalars().first()
    assert item is not None

    res = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item.id),
            "capitulo_id": str(item.capitulo_id),
            "tentativa_numero": 1,
            "tipo_item": "multiple_choice",
            "resposta_enviada": item.resposta_correta,
            "tempo_resposta_segundos": 45,
        },
    )

    assert res.status_code == 200
    data = res.json()
    assert data["acertou"] is True
    assert data["pontuacao_obtida"] == 1.0
    assert data["permite_segunda_chance"] is False
    assert data["resolucao_completa_katex"] is not None


@pytest.mark.asyncio
async def test_submissao_segunda_chance_e_erro_duplo(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    stmt = select(ItemExercicio).where(ItemExercicio.tipo_item == "multiple_choice")
    item = (await db_session.execute(stmt)).scalars().first()
    assert item is not None

    resposta_errada = "E" if item.resposta_correta != "E" else "D"

    # 1ª tentativa errada: deve liberar 2ª chance com pista socrática
    res1 = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item.id),
            "capitulo_id": str(item.capitulo_id),
            "tentativa_numero": 1,
            "tipo_item": "multiple_choice",
            "resposta_enviada": resposta_errada,
            "tempo_resposta_segundos": 30,
        },
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["acertou"] is False
    assert data1["pontuacao_obtida"] == 0.0
    assert data1["permite_segunda_chance"] is True
    assert data1["pista_socratica_ia"] is not None

    # 2ª tentativa correta: deve pontuar 0.5
    res2_acerto = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item.id),
            "capitulo_id": str(item.capitulo_id),
            "tentativa_numero": 2,
            "tipo_item": "multiple_choice",
            "resposta_enviada": item.resposta_correta,
            "tempo_resposta_segundos": 25,
        },
    )
    assert res2_acerto.status_code == 200
    data2 = res2_acerto.json()
    assert data2["acertou"] is True
    assert data2["pontuacao_obtida"] == 0.5

    # Anti-fraude (RN-EXE-008): o número de tentativas é contado no SERVIDOR.
    # Reenviar o mesmo item como "tentativa 2" após esgotar as chances deve conflitar.
    res_extra = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item.id),
            "capitulo_id": str(item.capitulo_id),
            "tentativa_numero": 2,
            "tipo_item": "multiple_choice",
            "resposta_enviada": resposta_errada,
            "tempo_resposta_segundos": 20,
        },
    )
    assert res_extra.status_code == 409

    # Erro duplo real (item novo): 1ª errada + 2ª errada -> 0.0 e pode gerar gêmea
    stmt_item2 = select(ItemExercicio).where(
        ItemExercicio.tipo_item == "multiple_choice",
        ItemExercicio.id != item.id,
    )
    item2 = (await db_session.execute(stmt_item2)).scalars().first()
    assert item2 is not None

    res_1_erro = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item2.id),
            "capitulo_id": str(item2.capitulo_id),
            "tentativa_numero": 1,
            "tipo_item": "multiple_choice",
            "resposta_enviada": resposta_errada,
            "tempo_resposta_segundos": 20,
        },
    )
    assert res_1_erro.status_code == 200

    res_2_erro = await async_client.post(
        "/api/v1/exercicios/submeter",
        headers=headers,
        json={
            "item_id": str(item2.id),
            "capitulo_id": str(item2.capitulo_id),
            "tentativa_numero": 2,
            "tipo_item": "multiple_choice",
            "resposta_enviada": resposta_errada,
            "tempo_resposta_segundos": 20,
        },
    )
    assert res_2_erro.status_code == 200
    data_erro = res_2_erro.json()
    assert data_erro["acertou"] is False
    assert data_erro["pontuacao_obtida"] == 0.0
    assert data_erro["pode_gerar_gemea"] is True

    # Verifica se foi arquivado na Caixa de Reforço
    res_cr = await async_client.get("/api/v1/exercicios/caixa-reforco", headers=headers)
    assert res_cr.status_code == 200
    cr_itens = res_cr.json()
    assert len(cr_itens) > 0
    assert any(i["item_id"] == str(item2.id) for i in cr_itens)


@pytest.mark.asyncio
async def test_gerar_questao_gemea(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    stmt = select(ItemExercicio).where(ItemExercicio.tipo_origem == "iezzi_original")
    item_matriz = (await db_session.execute(stmt)).scalars().first()
    assert item_matriz is not None

    res = await async_client.post(
        f"/api/v1/exercicios/gerar-gemea/{item_matriz.id}",
        headers=headers,
    )
    assert res.status_code == 200
    gemea = res.json()
    assert gemea["tipo_origem"] == "gemea_ia"
    assert gemea["item_matriz_id"] == str(item_matriz.id)
    assert len(gemea["alternativas"]) == 5
    assert gemea["validado_sympy"] is True


@pytest.mark.asyncio
async def test_fluxo_cat_adaptativo(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    stmt_disc = select(Disciplina).where(Disciplina.slug == "matematica")
    disc = (await db_session.execute(stmt_disc)).scalars().first()
    assert disc is not None

    # 1. Iniciar Sessão CAT
    res_ini = await async_client.post(
        "/api/v1/exercicios/cat/iniciar",
        headers=headers,
        json={
            "disciplina_id": str(disc.id),
            "tipo_prova": "onboarding_diagnostico",
        },
    )
    assert res_ini.status_code == 200
    dados_ini = res_ini.json()
    sessao_id = dados_ini["sessao_cat_id"]
    primeiro_item = dados_ini["primeiro_item"]
    assert primeiro_item["id"] is not None

    # 2. Submeter resposta da 1ª questão
    res_sub = await async_client.post(
        "/api/v1/exercicios/cat/submeter",
        headers=headers,
        json={
            "sessao_cat_id": sessao_id,
            "item_id": primeiro_item["id"],
            "resposta_enviada": "A",
            "tempo_resposta_segundos": 45,
        },
    )
    assert res_sub.status_code == 200
    status_cat = res_sub.json()
    assert status_cat["sessao_id"] == sessao_id
    assert status_cat["theta_final"] is not None
    assert status_cat["erro_padrao"] is not None
    assert "Questão" in status_cat["indicador_progresso"]


@pytest.mark.asyncio
async def test_obter_bateria_capitulo(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    stmt_item = select(ItemExercicio)
    item = (await db_session.execute(stmt_item)).scalars().first()
    assert item is not None

    res = await async_client.get(
        f"/api/v1/exercicios/capitulo/{item.capitulo_id}",
        headers=headers,
    )
    assert res.status_code == 200
    itens = res.json()
    assert len(itens) > 0
    # Verifica que gabarito (campo correta) está oculto
    for it in itens:
        for alt in it["alternativas"]:
            assert alt["correta"] is None
