"""
Bateria de Testes Automatizados — Módulo de Progresso & Analytics (Etapa 8).
Valida:
1. Obtenção de indicadores gerais, 4 eixos canônicos do Radar e Linha do Tempo.
2. UPSERT cumulativo no endpoint POST /api/v1/progresso/tempo-estudo (Tabela 17).
3. Matriz de capítulos do Heatmap e transição de cores (cinza, vermelho, amarelo, verde).
4. Consulta do Hub de Ação nos Top 3 Tópicos Críticos (RN-PRG-016).
5. Geração e streaming do Boletim Escolar em PDF via ReportLab (RN-PRG-017 / RN-PRG-018).
6. Micro-ajuste estocástico de proficiência (TRI 3PL) e registro na tabela historico_theta.
"""
import pytest
import uuid
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy import select, and_

from app.models.content import VolumeDidatico, Capitulo, Disciplina
from app.models.progress import HistoricoTheta, HeatmapDominio, HorasEstudoDiarias
from app.models.exercise import ItemExercicio, TentativaExercicio
from app.modules.progress.theta_updater import ThetaUpdaterService
from app.modules.progress.pdf_generator import BoletimPDFGenerator


async def autenticar(async_client: AsyncClient, usuario_teste: dict) -> dict:
    """Helper para autenticar o usuário e retornar o header Bearer."""
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
async def test_obter_progresso_geral(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    # Inserir um registro inicial em historico_theta para o usuário
    stmt_disc = select(Disciplina).limit(1)
    disc = (await db_session.execute(stmt_disc)).scalars().first()
    assert disc is not None

    reg_theta = HistoricoTheta(
        id=uuid.uuid4(),
        usuario_id=usuario_teste["id"],
        disciplina_id=disc.id,
        volume_id=None,
        grande_area="algebra_funcoes",
        theta_estimado=Decimal("0.750"),
        erro_padrao_se=Decimal("0.250"),
        origem_ajuste="onboarding_cat",
    )
    db_session.add(reg_theta)
    await db_session.commit()

    res = await async_client.get("/api/v1/progresso/geral", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert "theta_atual" in data
    assert "classificacao_nivel" in data
    assert data["classificacao_nivel"] in ["Básico", "Intermediário", "Avançado"]
    assert "radar_areas" in data
    assert len(data["radar_areas"]) == 4

    slugs_esperados = {"algebra_funcoes", "geometria", "algebra_linear", "aplicada"}
    slugs_recebidos = {a["slug_area"] for a in data["radar_areas"]}
    assert slugs_esperados == slugs_recebidos


@pytest.mark.asyncio
async def test_tempo_estudo_upsert(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    # 1. Enviar primeiro lote de 120 segundos
    res1 = await async_client.post(
        "/api/v1/progresso/tempo-estudo",
        headers=headers,
        json={"segundos_ativos": 120},
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["sucesso"] is True
    assert data1["segundos_adicionados"] == 120

    # 2. Enviar segundo lote de 180 segundos no mesmo dia (deve somar no UPSERT)
    res2 = await async_client.post(
        "/api/v1/progresso/tempo-estudo",
        headers=headers,
        json={"segundos_ativos": 180},
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["sucesso"] is True
    assert data2["segundos_adicionados"] == 180

    # 3. Consulta no banco direto
    stmt = select(HorasEstudoDiarias).where(
        HorasEstudoDiarias.usuario_id == usuario_teste["id"]
    )
    registro = (await db_session.execute(stmt)).scalars().first()
    assert registro is not None
    assert registro.segundos_ativos >= 300  # 120 + 180 = 300 segundos acumulados


@pytest.mark.asyncio
async def test_heatmap_volume_e_transicoes_de_cor(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    # Busca um volume
    stmt_vol = select(VolumeDidatico).limit(1)
    volume = (await db_session.execute(stmt_vol)).scalars().first()
    assert volume is not None

    # Consulta endpoint heatmap
    res = await async_client.get(f"/api/v1/progresso/heatmap/{volume.id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["volume_id"] == str(volume.id)
    assert "capitulos" in data
    assert len(data["capitulos"]) > 0

    # Validação da regra canônica de cores (RN-PRG-012 / Tabela 15):
    # - Cinza: menos de 3 itens
    # - Vermelho: < 50%
    # - Amarelo: 50% a 74.99%
    # - Verde: >= 75%
    # Busca um item real existente para satisfazer a chave estrangeira de tentativas
    stmt_item = select(ItemExercicio).limit(1)
    real_item = (await db_session.execute(stmt_item)).scalars().first()
    assert real_item is not None
    cap_id = real_item.capitulo_id

    # Caso 1: 2 tentativas (mesmo com 100% de acerto, deve ser cinza)
    t1 = TentativaExercicio(
        usuario_id=usuario_teste["id"],
        item_id=real_item.id,
        capitulo_id=cap_id,
        tentativa_numero=1,
        resposta_enviada="A",
        acertou=True,
        pontuacao_obtida=Decimal("1.0"),
        usou_dica_ia=False,
        tempo_resposta_segundos=30,
    )
    t2 = TentativaExercicio(
        usuario_id=usuario_teste["id"],
        item_id=real_item.id,
        capitulo_id=cap_id,
        tentativa_numero=2,
        resposta_enviada="B",
        acertou=True,
        pontuacao_obtida=Decimal("1.0"),
        usou_dica_ia=False,
        tempo_resposta_segundos=25,
    )
    db_session.add_all([t1, t2])
    await db_session.commit()

    await ThetaUpdaterService._atualizar_no_heatmap(db_session, usuario_teste["id"], cap_id)
    await db_session.commit()

    stmt_hm = select(HeatmapDominio).where(
        and_(
            HeatmapDominio.usuario_id == usuario_teste["id"],
            HeatmapDominio.capitulo_id == cap_id,
        )
    )
    hm_node = (await db_session.execute(stmt_hm)).scalar_one()
    assert hm_node.status_cor == "cinza"

    # Caso 2: adiciona 3º item com acerto (3/3 = 100% -> verde)
    t3 = TentativaExercicio(
        usuario_id=usuario_teste["id"],
        item_id=real_item.id,
        capitulo_id=cap_id,
        tentativa_numero=1,
        resposta_enviada="C",
        acertou=True,
        pontuacao_obtida=Decimal("1.0"),
        usou_dica_ia=False,
        tempo_resposta_segundos=20,
    )
    db_session.add(t3)
    await db_session.commit()

    await ThetaUpdaterService._atualizar_no_heatmap(db_session, usuario_teste["id"], cap_id)
    await db_session.commit()

    hm_node = (await db_session.execute(stmt_hm)).scalar_one()
    assert hm_node.status_cor == "verde"
    assert hm_node.total_questoes_respondidas == 3
    assert float(hm_node.taxa_acertos_ponderada) == 100.0


@pytest.mark.asyncio
async def test_top_3_criticos_endpoint(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    res = await async_client.get("/api/v1/progresso/top-criticos", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "top_criticos" in data
    assert "tem_pendencias_criticas" in data
    assert isinstance(data["top_criticos"], list)
    assert len(data["top_criticos"]) <= 3


@pytest.mark.asyncio
async def test_boletim_pdf_download(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    headers = await autenticar(async_client, usuario_teste)

    res = await async_client.get("/api/v1/progresso/boletim-pdf", headers=headers)
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in res.headers.get("content-disposition", "")
    assert res.content.startswith(b"%PDF-")


@pytest.mark.asyncio
async def test_micro_ajuste_estocastico_tri(
    db_session,
    usuario_teste: dict,
):
    stmt_item = select(ItemExercicio).limit(1)
    item = (await db_session.execute(stmt_item)).scalars().first()
    assert item is not None

    stmt_disc = select(Disciplina.id).limit(1)
    disc_id = (await db_session.execute(stmt_disc)).scalar_one()

    novo_theta = await ThetaUpdaterService.processar_micro_ajuste_exercicio(
        db=db_session,
        usuario_id=usuario_teste["id"],
        disciplina_id=disc_id,
        volume_id=None,
        capitulo_id=item.capitulo_id,
        item=item,
        pontuacao_ponderada=1.0,
        total_questoes_respondidas_aluno=5,
        grande_area="algebra_funcoes",
    )
    await db_session.commit()

    assert isinstance(novo_theta, float)
    assert -3.0 <= novo_theta <= 3.0

    # Verifica registro na tabela historico_theta
    stmt_hist = (
        select(HistoricoTheta)
        .where(
            and_(
                HistoricoTheta.usuario_id == usuario_teste["id"],
                HistoricoTheta.origem_ajuste == "micro_ajuste_exercicio",
            )
        )
        .order_by(HistoricoTheta.registrado_em.desc())
        .limit(1)
    )
    hist_rec = (await db_session.execute(stmt_hist)).scalar_one_or_none()
    assert hist_rec is not None
    assert float(hist_rec.theta_estimado) == novo_theta
