"""
Bateria de Testes Automatizados — Painel do Professor (Etapa 10).
Valida:
1. Bloqueio de acesso para aluno comum (HTTP 403 Forbidden).
2. Acesso liberado para professor e administrador (HTTP 200 OK).
3. Dashboard Analytics agregado com faixas TRI, faturamento e demografia.
4. Listagem paginada de estudantes e busca textual com filtros.
5. Dossiê individual com radar, métricas e auditoria de tentativas.
6. Emissão e download de Boletim Docente em PDF.
7. Central de Curadoria KaTeX: listagem de volumes e edição de aula com preview/salvamento.
8. Extrato contábil e processamento de estorno CDC dentro dos 7 dias.
"""
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select, delete, update

from app.core.security import hash_senha
from app.models.user import Usuario, SessaoAtiva, TokenRecuperacaoSenha
from app.models.content import Disciplina, VolumeDidatico, Capitulo, Aula
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.models.progress import HistoricoTheta, HorasEstudoDiarias
from app.models.exercise import ItemExercicio, TentativaExercicio


async def autenticar(async_client: AsyncClient, creds: dict) -> dict:
    """Helper para autenticar usuário e retornar headers Authorization Bearer."""
    res = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": creds["email"],
            "senha": creds["senha_plana"],
        },
    )
    assert res.status_code == 200, f"Falha no login: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def professor_teste(db_session):
    """Cria e retorna um usuário docente de teste isolado."""
    email_prof = "prof_unitario@tutorinteligente.com.br"
    cpf_prof = "88877766655"
    senha_plana = "SenhaProf123@"

    stmt_busca = select(Usuario).where(Usuario.email == email_prof)
    existente = (await db_session.execute(stmt_busca)).scalar_one_or_none()
    if existente:
        await db_session.execute(
            update(Aula).where(Aula.atualizado_por == existente.id).values(atualizado_por=None)
        )
        await db_session.execute(delete(SessaoAtiva).where(SessaoAtiva.usuario_id == existente.id))
        await db_session.delete(existente)
        await db_session.commit()

    professor = Usuario(
        cpf=cpf_prof,
        email=email_prof,
        senha_hash=hash_senha(senha_plana),
        nome_completo="Professor Teste Unitário",
        data_nascimento=date(1980, 8, 20),
        idade_anos=44,
        eh_menor_idade=False,
        uf="SP",
        cidade="São Paulo",
        cep="01310000",
        escola_tipo="outro",
        serie_ano="todos",
        role="teacher",
        ativo=True,
    )
    db_session.add(professor)
    await db_session.commit()
    await db_session.refresh(professor)

    yield {
        "id": professor.id,
        "email": email_prof,
        "cpf": cpf_prof,
        "senha_plana": senha_plana,
        "role": "teacher",
        "usuario_obj": professor,
    }

    await db_session.execute(
        update(Aula).where(Aula.atualizado_por == professor.id).values(atualizado_por=None)
    )
    await db_session.execute(delete(SessaoAtiva).where(SessaoAtiva.usuario_id == professor.id))
    await db_session.execute(delete(Usuario).where(Usuario.id == professor.id))
    await db_session.commit()


@pytest.mark.asyncio
async def test_controle_de_acesso_rotas_professor(
    async_client: AsyncClient,
    usuario_teste: dict,
    professor_teste: dict,
):
    """Garante que estudantes recebam HTTP 403 e professores recebam HTTP 200."""
    headers_aluno = await autenticar(async_client, usuario_teste)
    headers_prof = await autenticar(async_client, professor_teste)

    # 1. Aluno comum tenta acessar /api/v1/teacher/analytics -> 403 Forbidden
    res_aluno = await async_client.get("/api/v1/teacher/analytics", headers=headers_aluno)
    assert res_aluno.status_code == 403
    assert "Acesso restrito" in res_aluno.json()["detail"]

    # 2. Professor acessa /api/v1/teacher/analytics -> 200 OK
    res_prof = await async_client.get("/api/v1/teacher/analytics", headers=headers_prof)
    assert res_prof.status_code == 200
    dados = res_prof.json()
    assert "total_alunos" in dados
    assert "distribuicao_tri" in dados
    assert "faturamento_mensal" in dados


@pytest.mark.asyncio
async def test_analytics_consolidado_demografia_e_tri(
    async_client: AsyncClient,
    professor_teste: dict,
    usuario_teste: dict,
    db_session,
):
    """Valida o cálculo agregado de indicadores, métricas TRI e demografia."""
    headers_prof = await autenticar(async_client, professor_teste)

    # Obtém disciplina para vincular HistoricoTheta
    disc_res = await db_session.execute(select(Disciplina).limit(1))
    disciplina = disc_res.scalar_one()

    # Cria histórico theta para o aluno de teste
    hist = HistoricoTheta(
        usuario_id=usuario_teste["id"],
        disciplina_id=disciplina.id,
        grande_area="geral",
        theta_estimado=0.85,
        erro_padrao_se=0.25,
        origem_ajuste="onboarding_cat"
    )
    db_session.add(hist)
    await db_session.commit()

    res = await async_client.get("/api/v1/teacher/analytics", headers=headers_prof)
    assert res.status_code == 200
    dados = res.json()

    assert dados["total_alunos"] >= 1
    assert "basico" in dados["distribuicao_tri"]
    assert "intermediario" in dados["distribuicao_tri"]
    assert "avancado" in dados["distribuicao_tri"]
    assert len(dados["distribuicao_escola"]) >= 1


@pytest.mark.asyncio
async def test_listar_alunos_paginado_com_busca(
    async_client: AsyncClient,
    professor_teste: dict,
    usuario_teste: dict,
):
    """Valida a listagem paginada de estudantes com filtro de busca debounced."""
    headers_prof = await autenticar(async_client, professor_teste)

    # Busca pelo nome do aluno de teste
    res = await async_client.get(
        "/api/v1/teacher/alunos",
        params={"search": "Aluno Teste Unitário", "page": 1, "limit": 10},
        headers=headers_prof,
    )
    assert res.status_code == 200
    dados = res.json()
    assert dados["total"] >= 1
    aluno_encontrado = next((a for a in dados["items"] if a["id"] == str(usuario_teste["id"])), None)
    assert aluno_encontrado is not None
    assert aluno_encontrado["nome_completo"] == "Aluno Teste Unitário"
    assert "cpf_mascarado" in aluno_encontrado


@pytest.mark.asyncio
async def test_obter_dossie_e_boletim_pdf_do_aluno(
    async_client: AsyncClient,
    professor_teste: dict,
    usuario_teste: dict,
    db_session,
):
    """Valida o dossiê individual completo e a geração do PDF do Boletim."""
    headers_prof = await autenticar(async_client, professor_teste)

    # 1. Dossiê individual
    res_dossie = await async_client.get(
        f"/api/v1/teacher/alunos/{usuario_teste['id']}",
        headers=headers_prof,
    )
    assert res_dossie.status_code == 200
    dossie = res_dossie.json()
    assert dossie["id"] == str(usuario_teste["id"])
    assert dossie["eh_menor_idade"] is True
    assert dossie["dados_responsavel"] is not None
    assert "radar_areas" in dossie
    assert "historico_theta" in dossie

    # 2. Download do Boletim em PDF
    res_pdf = await async_client.get(
        f"/api/v1/teacher/alunos/{usuario_teste['id']}/boletim",
        headers=headers_prof,
    )
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    assert len(res_pdf.content) > 1000  # Arquivo PDF gerado


@pytest.mark.asyncio
async def test_curadoria_volumes_e_atualizacao_katex(
    async_client: AsyncClient,
    professor_teste: dict,
    db_session,
):
    """Valida a árvore de volumes didáticos e a edição split-screen de aula KaTeX."""
    headers_prof = await autenticar(async_client, professor_teste)

    # 1. Listar volumes
    res_vols = await async_client.get("/api/v1/teacher/curadoria/volumes", headers=headers_prof)
    assert res_vols.status_code == 200
    volumes = res_vols.json()
    assert len(volumes) >= 1
    primeiro_vol = volumes[0]
    assert len(primeiro_vol["capitulos"]) >= 1
    cap_id = primeiro_vol["capitulos"][0]["capitulo_id"]

    # 2. Obter conteúdo da aula
    res_aula = await async_client.get(f"/api/v1/teacher/curadoria/aulas/{cap_id}", headers=headers_prof)
    assert res_aula.status_code == 200
    aula_dados = res_aula.json()
    assert "bloco1_teoria_katex" in aula_dados

    # 3. Atualizar conteúdo KaTeX da aula e garantir restauração do conteúdo original
    novo_payload = {
        "bloco1_teoria_katex": "## Teoria Curada pelo Professor\n\nFórmula atualizada: $$ E = mc^2 $$ e $$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$$",
        "bloco2_exemplos_katex": "## Exemplo Prático Docente\n\nResolução analítica de equação linear.",
        "bloco3_dicas_ia": "> [!IMPORTANT]\n> Cuidado com o domínio da função.",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "publicado": True
    }
    try:
        res_update = await async_client.put(
            f"/api/v1/teacher/curadoria/aulas/{cap_id}",
            json=novo_payload,
            headers=headers_prof,
        )
        assert res_update.status_code == 200
        atualizado = res_update.json()
        assert "Teoria Curada pelo Professor" in atualizado["bloco1_teoria_katex"]
        assert atualizado["video_url"] == novo_payload["video_url"]
        assert atualizado["publicado"] is True
    finally:
        # Restaura o conteúdo canônico original da aula para evitar poluição do banco de dados
        payload_original = {
            "bloco1_teoria_katex": aula_dados.get("bloco1_teoria_katex"),
            "bloco2_exemplos_katex": aula_dados.get("bloco2_exemplos_katex"),
            "bloco3_dicas_ia": aula_dados.get("bloco3_dicas_ia"),
            "video_url": aula_dados.get("video_url"),
            "publicado": aula_dados.get("publicado", True),
        }
        await async_client.put(
            f"/api/v1/teacher/curadoria/aulas/{cap_id}",
            json=payload_original,
            headers=headers_prof,
        )


@pytest.mark.asyncio
async def test_extrato_financeiro_e_estorno_cdc(
    async_client: AsyncClient,
    professor_teste: dict,
    usuario_teste: dict,
    db_session,
):
    """Valida a auditoria financeira e o estorno administrativo de matrícula dentro dos 7 dias."""
    headers_prof = await autenticar(async_client, professor_teste)

    # 1. Cria Matrícula e Transação paga de teste
    agora = datetime.now(timezone.utc)
    matricula = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=uuid4(),
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("9.90"),
        metodo_pagamento="pix",
        transacao_gateway_id="sim_cobranca_teste_docente"
    )
    db_session.add(matricula)
    await db_session.flush()

    transacao = TransacaoFinanceira(
        matricula_id=matricula.id,
        usuario_id=usuario_teste["id"],
        gateway_transacao_id="sim_cobranca_teste_docente",
        valor_bruto=Decimal("9.90"),
        taxa_gateway=Decimal("0.99"),
        valor_liquido=Decimal("8.91"),
        status_transacao="paid",
        metodo="pix",
        pago_em=agora,
        criado_em=agora,
    )
    db_session.add(transacao)
    await db_session.commit()

    # 2. Consultar extrato financeiro
    res_extrato = await async_client.get("/api/v1/teacher/financeiro/extrato", headers=headers_prof)
    assert res_extrato.status_code == 200
    extrato = res_extrato.json()
    assert extrato["saldo_total_bruto"] >= 9.90
    assert len(extrato["transacoes"]) >= 1

    # 3. Solicitar estorno CDC (dentro dos 7 dias)
    res_estorno = await async_client.post(
        f"/api/v1/teacher/matriculas/{matricula.id}/estorno",
        headers=headers_prof,
    )
    assert res_estorno.status_code == 200
    estorno_dados = res_estorno.json()
    assert estorno_dados["sucesso"] is True
    assert estorno_dados["novo_status"] == "canceled"

    # Confere no banco se o status da matrícula e da transação foram atualizados
    await db_session.refresh(matricula)
    await db_session.refresh(transacao)
    assert matricula.status == "canceled"
    assert transacao.status_transacao == "refunded"
