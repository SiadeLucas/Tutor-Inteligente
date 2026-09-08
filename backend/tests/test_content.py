"""
Bateria de Testes Automatizados — Módulo de Conteúdo Didático (Etapa 5).
Valida rotas de catálogo, Skill Tree dos 11 volumes, visualização de aulas KaTeX,
fixação server-side com persistência no heatmap_dominio (RN-PRG-012) e
consolidação de tempo de estudo em horas_estudo_diarias (RN-PRG-003).

Todos os endpoints exigem autenticação (Bearer token via get_current_user).
"""
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models.progress import HeatmapDominio, HorasEstudoDiarias


async def autenticar(async_client: AsyncClient, usuario_teste: dict) -> dict:
    """Realiza login e retorna o header Authorization pronto para uso."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario_teste["email"],
            "senha": usuario_teste["senha_plana"],
        },
    )
    assert response.status_code == 200, f"Login falhou: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def obter_cap1_id(async_client: AsyncClient, headers: dict) -> str:
    """Helper: retorna o id do primeiro capítulo do Volume 1."""
    tree_res = await async_client.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica",
        headers=headers,
    )
    assert tree_res.status_code == 200
    return tree_res.json()[0]["capitulos"][0]["id"]


# ============================================================================
# Proteção por autenticação
# ============================================================================

@pytest.mark.asyncio
async def test_endpoints_exigem_autenticacao(async_client: AsyncClient):
    """Todos os endpoints de conteúdo devem rejeitar requisições sem Bearer token (401)."""
    res_tree = await async_client.get("/api/v1/conteudo/skill-tree")
    assert res_tree.status_code == 401

    res_disc = await async_client.get("/api/v1/conteudo/disciplinas")
    assert res_disc.status_code == 401

    res_aula = await async_client.get("/api/v1/conteudo/aulas/00000000-0000-0000-0000-000000000000")
    assert res_aula.status_code == 401


# ============================================================================
# Catálogo e Skill Tree
# ============================================================================

@pytest.mark.asyncio
async def test_listar_disciplinas(async_client: AsyncClient, usuario_teste):
    """Verifica se a disciplina Matemática é retornada como ativa."""
    headers = await autenticar(async_client, usuario_teste)
    response = await async_client.get("/api/v1/conteudo/disciplinas", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    slugs = [d["slug"] for d in data]
    assert "matematica" in slugs
    mat = next(d for d in data if d["slug"] == "matematica")
    assert mat["nome"] == "Matemática"
    assert mat["nivel_ensino"] == "ensino_medio"
    assert mat["ativo"] is True


@pytest.mark.asyncio
async def test_listar_volumes_matematica(async_client: AsyncClient, usuario_teste):
    """Verifica se os 11 volumes do Iezzi estão vinculados à Matemática."""
    headers = await autenticar(async_client, usuario_teste)
    disc_res = await async_client.get("/api/v1/conteudo/disciplinas", headers=headers)
    disciplina_id = disc_res.json()[0]["id"]

    response = await async_client.get(
        f"/api/v1/conteudo/volumes/{disciplina_id}", headers=headers
    )
    assert response.status_code == 200
    volumes = response.json()
    assert len(volumes) == 11

    numeros = [v["numero_volume"] for v in volumes]
    assert sorted(numeros) == list(range(1, 12))

    vol1 = next(v for v in volumes if v["numero_volume"] == 1)
    assert "Conjuntos e Funções" in vol1["titulo"]
    assert vol1["grande_area"] == "algebra_funcoes"
    assert vol1["total_capitulos"] == 8


@pytest.mark.asyncio
async def test_obter_skill_tree_completa(async_client: AsyncClient, usuario_teste):
    """Verifica a recuperação agregada da Skill Tree para a interface do aluno."""
    headers = await autenticar(async_client, usuario_teste)
    response = await async_client.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica", headers=headers
    )
    assert response.status_code == 200
    tree = response.json()
    assert len(tree) == 11

    total_capitulos = sum(len(vol["capitulos"]) for vol in tree)
    assert total_capitulos >= 60

    primeiro_cap = tree[0]["capitulos"][0]
    assert primeiro_cap["tempo_estimado_min"] == 50
    assert primeiro_cap["status_dominio"] in ["mastered", "in_progress", "struggling", "not_started"]
    assert primeiro_cap["cor_heatmap"] in ["green", "yellow", "red", "grey"]


# ============================================================================
# Aula em 4 Blocos KaTeX
# ============================================================================

@pytest.mark.asyncio
async def test_obter_aula_katex(async_client: AsyncClient, usuario_teste):
    """Verifica se a aula estruturada em 4 blocos com KaTeX é retornada para o Cap. 1."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    response = await async_client.get(f"/api/v1/conteudo/aulas/{cap1_id}", headers=headers)
    assert response.status_code == 200
    aula = response.json()

    assert "bloco1_teoria_katex" in aula
    assert "bloco2_exemplos_katex" in aula
    assert "bloco3_dicas_ia" in aula
    assert "$" in aula["bloco1_teoria_katex"]  # Contém equações KaTeX
    assert aula["capitulo_titulo"] == "Noções de Lógica e Proposições"
    assert aula["numero_volume"] == 1


# ============================================================================
# Fixação Server-Side + Heatmap (RN-PRG-012) + Horas de Estudo (RN-PRG-003)
# ============================================================================

@pytest.mark.asyncio
async def test_fixacao_server_side_fluxo_completo(
    async_client: AsyncClient, usuario_teste, db_session
):
    """
    Fluxo completo: busca bateria (sem gabarito), submete respostas suficientes,
    valida persistência em heatmap_dominio e horas_estudo_diarias.
    """
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # 1. Bateria não deve expor o gabarito
    res_bateria = await async_client.get(
        f"/api/v1/conteudo/aulas/{cap1_id}/fixacao", headers=headers
    )
    assert res_bateria.status_code == 200
    bateria = res_bateria.json()
    assert len(bateria["questoes"]) >= 3
    for questao in bateria["questoes"]:
        assert "indice_correto" not in questao
        assert "correta" not in questao

    # 2. Submeter todas as respostas corretas (gabarito conhecido do seed)
    respostas_corretas = {1: 1, 2: 1, 3: 3}
    res_ok = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/fixacao",
        json={"respostas": respostas_corretas, "segundos_estudo": 1200},
        headers=headers,
    )
    assert res_ok.status_code == 200
    data_ok = res_ok.json()
    assert data_ok["concluida"] is True
    assert data_ok["percentual_acertos"] == 100.0
    assert data_ok["proximo_capitulo_id"] is not None
    # Gabarito agora é revelado após a submissão
    assert data_ok["gabarito"] == {"1": 1, "2": 1, "3": 3}

    # 3. Heatmap persistido com RN-PRG-012 (100% >= 75% => 'verde')
    hm = (
        await db_session.execute(
            select(HeatmapDominio).where(
                HeatmapDominio.usuario_id == usuario_teste["id"],
                HeatmapDominio.capitulo_id == cap1_id,
            )
        )
    ).scalar_one_or_none()
    assert hm is not None
    assert hm.aula_concluida is True
    assert hm.status_cor == "verde"
    assert float(hm.taxa_acertos_ponderada) == 100.0

    # 4. Horas de estudo consolidadas (RN-PRG-003)
    hs = (
        await db_session.execute(
            select(HorasEstudoDiarias).where(
                HorasEstudoDiarias.usuario_id == usuario_teste["id"],
            )
        )
    ).scalar_one_or_none()
    assert hs is not None
    assert hs.segundos_ativos == 1200
    assert hs.exercicios_submetidos == 3
    assert hs.aulas_concluidas == 1

    # 5. Skill Tree agora reflete o domínio real (verde/mastered)
    tree_res = await async_client.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica", headers=headers
    )
    cap1_node = tree_res.json()[0]["capitulos"][0]
    assert cap1_node["status_dominio"] == "mastered"
    assert cap1_node["cor_heatmap"] == "green"


@pytest.mark.asyncio
async def test_fixacao_reprovacao_abaixo_60(async_client: AsyncClient, usuario_teste, db_session):
    """Valida RN-CNT-010: submissão com <60% não conclui a aula e marca 'vermelho'."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # 1 acerto em 3 questões = 33.3% (< 50% => vermelho)
    res_fail = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/fixacao",
        json={"respostas": {1: 0, 2: 0, 3: 0}, "segundos_estudo": 300},
        headers=headers,
    )
    assert res_fail.status_code == 200
    data_fail = res_fail.json()
    assert data_fail["concluida"] is False
    assert data_fail["percentual_acertos"] < 60.0

    hm = (
        await db_session.execute(
            select(HeatmapDominio).where(
                HeatmapDominio.usuario_id == usuario_teste["id"],
                HeatmapDominio.capitulo_id == cap1_id,
            )
        )
    ).scalar_one_or_none()
    assert hm is not None
    assert hm.aula_concluida is False
    assert hm.status_cor == "vermelho"


@pytest.mark.asyncio
async def test_concluir_aula_trava_60_porcento(async_client: AsyncClient, usuario_teste, db_session):
    """Valida a rota legada de conclusão manual: bloqueia <60% e persiste heatmap quando aprovada."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # Tentativa com 50% de acerto -> deve reprovar a conclusão
    res_fail = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/concluir",
        json={"percentual_acertos": 50.0},
        headers=headers,
    )
    assert res_fail.status_code == 200
    data_fail = res_fail.json()
    assert data_fail["concluida"] is False
    assert data_fail["sucesso"] is False

    # Tentativa com 75% de acerto -> deve aprovar e indicar próximo capítulo
    res_ok = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/concluir",
        json={"percentual_acertos": 75.0},
        headers=headers,
    )
    assert res_ok.status_code == 200
    data_ok = res_ok.json()
    assert data_ok["concluida"] is True
    assert data_ok["sucesso"] is True
    assert data_ok["proximo_capitulo_id"] is not None

    # Conclusão persistida no heatmap
    hm = (
        await db_session.execute(
            select(HeatmapDominio).where(
                HeatmapDominio.usuario_id == usuario_teste["id"],
                HeatmapDominio.capitulo_id == cap1_id,
            )
        )
    ).scalar_one_or_none()
    assert hm is not None
    assert hm.aula_concluida is True
    assert float(hm.taxa_acertos_ponderada) == 75.0
    # 75% >= 75% => verde pela RN-PRG-012 (limiar de domínio)
    assert hm.status_cor == "verde"


# ============================================================================
# Placeholders Socráticos (Etapa 6)
# ============================================================================

@pytest.mark.asyncio
async def test_placeholders_socratica_e_pista(async_client: AsyncClient, usuario_teste):
    """Testa endpoints interativos da aula (chat socrático e pista rápida)."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # Chat
    chat_payload = {
        "capitulo_id": cap1_id,
        "mensagem": "Não entendi a negação da condicional",
        "trecho_selecionado": r"p \to q",
    }
    chat_res = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/chat", json=chat_payload, headers=headers
    )
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "resposta_katex" in chat_data
    assert isinstance(chat_data["chunks_utilizados"], list)
    assert chat_data["nivel_ajuda_socratico"] in (1, 2, 3)

    # Pista
    pista_payload = {"capitulo_id": cap1_id, "contexto_exercicio": "Questão de lógica"}
    pista_res = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/pista", json=pista_payload, headers=headers
    )
    assert pista_res.status_code == 200
    pista_data = pista_res.json()
    assert "pista_socratica_katex" in pista_data
