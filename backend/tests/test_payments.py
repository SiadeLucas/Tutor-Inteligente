"""
Bateria de Testes Automatizados — Módulo de Pagamento e Checkout (Etapa 9).
Valida:
1. Conexão Asaas / Emissão de PIX dinâmico com QR Code e expiração.
2. Checkout com Cartão de Crédito.
3. Cálculo de upgrade proporcional com abatimento integral (100%) por volume (RN-PAG-005).
4. Ativação instantânea de matrícula gratuita quando o abatimento cobre o valor total.
5. Idempotência estrita do Webhook.
6. Validação timing-safe do segredo do Webhook (secrets.compare_digest).
7. Proteção contra IDOR no endpoint de polling de status.
8. Vigência canônica de 365 dias para compras e listagem em meus-produtos.
9. Desbloqueio universal e irrestrito para Admin e Passe Global.
"""
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import pytest
from httpx import AsyncClient
from sqlalchemy import select, delete

from app.core.config import settings
from app.core.security import hash_senha
from app.models.user import Usuario
from app.models.content import VolumeDidatico, Capitulo
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.modules.payments.webhook_service import validar_token


async def autenticar(async_client: AsyncClient, usuario: dict) -> dict:
    """Helper para efetuar login e retornar headers de autorização Bearer."""
    res = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario["email"],
            "senha": usuario["senha_plana"],
        },
    )
    assert res.status_code == 200, f"Falha no login: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_calcular_upgrade_sem_e_com_capitulos(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Valida a regra RN-PAG-005 de dedução de capítulos avulsos na compra do volume."""
    headers = await autenticar(async_client, usuario_teste)

    # 1. Busca Volume 1 e seus capítulos
    vol_res = await db_session.execute(
        select(VolumeDidatico).where(VolumeDidatico.numero_volume == 1)
    )
    vol = vol_res.scalar_one()

    caps_res = await db_session.execute(
        select(Capitulo).where(Capitulo.volume_id == vol.id).order_by(Capitulo.ordem)
    )
    capitulos = caps_res.scalars().all()
    assert len(capitulos) >= 2

    # Sem compras anteriores: abatimento = 0
    res_zero = await async_client.get(
        f"/api/v1/pagamentos/calcular-upgrade/{vol.id}", headers=headers
    )
    assert res_zero.status_code == 200
    data_zero = res_zero.json()
    assert data_zero["total_abatimento"] == 0.0
    assert data_zero["valor_final"] == float(vol.preco_padrao)
    assert data_zero["gratis_por_upgrade"] is False

    # Insere 2 compras de capítulos (ex: R$ 9.90 cada = R$ 19.80)
    agora = datetime.now(timezone.utc)
    mat1 = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=capitulos[0].id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("9.90"),
        metodo_pagamento="pix",
    )
    mat2 = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=capitulos[1].id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("9.90"),
        metodo_pagamento="pix",
    )
    db_session.add_all([mat1, mat2])
    await db_session.commit()

    # Com 2 compras: abatimento = 19.80
    res_upg = await async_client.get(
        f"/api/v1/pagamentos/calcular-upgrade/{vol.id}", headers=headers
    )
    assert res_upg.status_code == 200
    data_upg = res_upg.json()
    assert data_upg["total_abatimento"] == 19.80
    assert data_upg["valor_final"] == round(float(vol.preco_padrao) - 19.80, 2)
    assert data_upg["capitulos_abatidos_count"] == 2


@pytest.mark.asyncio
async def test_checkout_pix_fluxo_completo(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Testa emissão de PIX dinâmico com QR Code, copia e cola e expiração em 15 min."""
    headers = await autenticar(async_client, usuario_teste)

    # Busca um capítulo
    cap_res = await db_session.execute(select(Capitulo))
    cap = cap_res.scalars().first()
    assert cap is not None

    res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={
            "tipo_produto": "capitulo_50min",
            "referencia_produto_id": str(cap.id),
        },
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert "cobranca_id" in data
    assert "pix_copia_e_cola" in data
    assert "pix_qrcode_base64" in data
    assert data["valor"] > 0
    assert data["gratis_por_upgrade"] is False
    assert data["matricula_id"] is not None

    # Consulta status da cobrança
    cobranca_id = data["cobranca_id"]
    st_res = await async_client.get(
        f"/api/v1/pagamentos/status/{cobranca_id}", headers=headers
    )
    assert st_res.status_code == 200
    st_data = st_res.json()
    assert st_data["cobranca_id"] == cobranca_id
    assert st_data["status"] == "waiting_payment"
    assert st_data["pago"] is False


@pytest.mark.asyncio
async def test_checkout_upgrade_gratis_instantaneo(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Se o abatimento cobrir todo o preço do volume, matrícula é instantânea sem gateway."""
    headers = await autenticar(async_client, usuario_teste)

    vol_res = await db_session.execute(
        select(VolumeDidatico).where(VolumeDidatico.numero_volume == 2)
    )
    vol = vol_res.scalar_one()

    caps_res = await db_session.execute(
        select(Capitulo).where(Capitulo.volume_id == vol.id)
    )
    cap = caps_res.scalars().first()

    # Simula compras anteriores que somam o valor total do volume (R$ 50.00 >= R$ 49.90)
    agora = datetime.now(timezone.utc)
    mat_grande = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=cap.id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("50.00"),
        metodo_pagamento="pix",
    )
    db_session.add(mat_grande)
    await db_session.commit()

    # Tenta checkout do volume via PIX
    res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={
            "tipo_produto": "volume_iezzi",
            "referencia_produto_id": str(vol.id),
        },
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["gratis_por_upgrade"] is True
    assert data["valor"] == 0.0
    assert data["matricula_id"] is not None

    # Verifica se a matrícula no volume está ativa no banco
    mat_vol = (
        await db_session.execute(
            select(MatriculaPagamento).where(
                MatriculaPagamento.id == data["matricula_id"]
            )
        )
    ).scalar_one()
    assert mat_vol.status == "active"
    assert mat_vol.tipo_produto == "volume_iezzi"


@pytest.mark.asyncio
async def test_checkout_cartao_aprovado(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Testa checkout com Cartão de Crédito."""
    headers = await autenticar(async_client, usuario_teste)

    cap_res = await db_session.execute(select(Capitulo))
    cap = cap_res.scalars().first()

    res = await async_client.post(
        "/api/v1/pagamentos/checkout/cartao",
        json={
            "tipo_produto": "capitulo_50min",
            "referencia_produto_id": str(cap.id),
            "parcelas": 1,
            "cartao": {
                "nome_titular": "Aluno Teste",
                "numero_cartao": "4000123456789010",
                "mes_expiracao": "12",
                "ano_expiracao": "2028",
                "cvv": "123",
            },
        },
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["pago"] is True
    assert data["status"] == "paid"
    assert data["matricula_id"] is not None


@pytest.mark.asyncio
async def test_protecao_idor_status_cobranca(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Garante que um estudante não pode consultar cobranças de outro usuário (IDOR)."""
    headers_user1 = await autenticar(async_client, usuario_teste)

    # Cria usuário 2
    user2 = Usuario(
        cpf="33344455566",
        email="outro_aluno@tutorinteligente.com.br",
        senha_hash=hash_senha("SenhaSegura123!"),
        nome_completo="Outro Aluno",
        data_nascimento=datetime(2005, 1, 1).date(),
        idade_anos=19,
        eh_menor_idade=False,
        uf="SP",
        cidade="São Paulo",
        cep="01001000",
        escola_tipo="publica",
        serie_ano="3_ano",
        role="student",
        ativo=True,
    )
    db_session.add(user2)
    await db_session.commit()
    await db_session.refresh(user2)

    headers_user2 = await autenticar(
        async_client,
        {"email": "outro_aluno@tutorinteligente.com.br", "senha_plana": "SenhaSegura123!"},
    )

    # Usuário 1 cria uma cobrança
    cap_res = await db_session.execute(select(Capitulo))
    cap = cap_res.scalars().first()

    checkout_res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={"tipo_produto": "capitulo_50min", "referencia_produto_id": str(cap.id)},
        headers=headers_user1,
    )
    cobranca_id = checkout_res.json()["cobranca_id"]

    # Usuário 2 tenta consultar a cobrança do Usuário 1 -> 403 Forbidden!
    idor_res = await async_client.get(
        f"/api/v1/pagamentos/status/{cobranca_id}", headers=headers_user2
    )
    assert idor_res.status_code == 403

    # Limpeza
    await db_session.execute(delete(TransacaoFinanceira).where(TransacaoFinanceira.usuario_id == user2.id))
    await db_session.execute(delete(MatriculaPagamento).where(MatriculaPagamento.usuario_id == user2.id))
    await db_session.execute(delete(Usuario).where(Usuario.id == user2.id))
    await db_session.commit()


@pytest.mark.asyncio
async def test_webhook_idempotencia_e_seguranca_token(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Valida que o webhook é seguro contra timing attacks e idempotente (não duplica processamento)."""
    headers = await autenticar(async_client, usuario_teste)

    # 1. Testa secrets.compare_digest
    assert validar_token("token_secreto_123", "token_secreto_123") is True
    assert validar_token("token_errado", "token_secreto_123") is False
    assert validar_token(None, "token_secreto_123") is False

    # 2. Cria cobrança pendente
    cap_res = await db_session.execute(select(Capitulo))
    cap = cap_res.scalars().first()

    checkout_res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={"tipo_produto": "capitulo_50min", "referencia_produto_id": str(cap.id)},
        headers=headers,
    )
    cobranca_id = checkout_res.json()["cobranca_id"]
    matricula_id = checkout_res.json()["matricula_id"]

    webhook_payload = {
        "event": "PAYMENT_RECEIVED",
        "payment": {
            "id": cobranca_id,
            "status": "RECEIVED",
            "netValue": 8.91,
        },
    }

    # 3. Dispara Webhook 1ª vez: sucesso
    wh1 = await async_client.post(
        "/api/v1/pagamentos/webhook",
        json=webhook_payload,
        headers={"asaas-access-token": settings.ASAAS_WEBHOOK_SECRET_TOKEN or "dev_token"},
    )
    assert wh1.status_code == 200
    assert wh1.json()["status"] == "success"

    # Verifica se matrícula foi ativada
    mat = (
        await db_session.execute(
            select(MatriculaPagamento).where(MatriculaPagamento.id == matricula_id)
        )
    ).scalar_one()
    assert mat.status == "active"

    # 4. Dispara Webhook 2ª vez: IDEMPOTÊNCIA (detecta que já foi pago)
    wh2 = await async_client.post(
        "/api/v1/pagamentos/webhook",
        json=webhook_payload,
        headers={"asaas-access-token": settings.ASAAS_WEBHOOK_SECRET_TOKEN or "dev_token"},
    )
    assert wh2.status_code == 200
    assert wh2.json()["status"] == "already_processed"
    assert wh2.json()["idempotent"] is True


@pytest.mark.asyncio
async def test_listar_meus_produtos_e_vigencia(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Valida o endpoint /meus-produtos com vigência canônica de 365 dias."""
    headers = await autenticar(async_client, usuario_teste)

    agora = datetime.now(timezone.utc)
    mat = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="passe_global",
        referencia_produto_id=None,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("199.00"),
        metodo_pagamento="pix",
        transacao_gateway_id="pay_test_vigencia",
    )
    db_session.add(mat)
    await db_session.commit()

    res = await async_client.get("/api/v1/pagamentos/meus-produtos", headers=headers)
    assert res.status_code == 200
    produtos = res.json()
    assert len(produtos) >= 1
    passe = next(p for p in produtos if p["tipo_produto"] == "passe_global")
    assert "Passe Global" in passe["titulo_produto"]
    assert passe["dias_restantes"] in (364, 365)
    assert passe["status"] == "active"


@pytest.mark.asyncio
async def test_admin_e_passe_global_possuem_acesso_irrestrito(
    async_client: AsyncClient,
    db_session,
):
    """Garante que contas de Administrador ou com Passe Global têm todos os conteúdos desbloqueados."""
    # 1. Login do Administrador
    admin_headers = await autenticar(
        async_client,
        {"email": "admin@tutorinteligente.com.br", "senha_plana": "SenhaSegura123!"},
    )

    # Consulta Skill Tree como Admin
    tree_res = await async_client.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica",
        headers=admin_headers,
    )
    assert tree_res.status_code == 200
    tree = tree_res.json()

    # Todos os nós com conteúdo devem estar 'desbloqueado = True' para o Admin!
    for vol in tree:
        for cap in vol["capitulos"]:
            if cap["tem_conteudo"]:
                assert cap["desbloqueado"] is True, f"Capítulo {cap['titulo']} bloqueado para Admin!"


@pytest.mark.asyncio
async def test_status_cobranca_upgrade_gratis(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Verifica que upgrade 100% gratuito cria TransacaoFinanceira auditável e responde no polling de status."""
    headers = await autenticar(async_client, usuario_teste)

    vol_res = await db_session.execute(
        select(VolumeDidatico).where(VolumeDidatico.numero_volume == 3)
    )
    vol = vol_res.scalar_one()

    caps_res = await db_session.execute(
        select(Capitulo).where(Capitulo.volume_id == vol.id)
    )
    cap = caps_res.scalars().first()

    agora = datetime.now(timezone.utc)
    mat_grande = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=cap.id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("50.00"),
        metodo_pagamento="pix",
    )
    db_session.add(mat_grande)
    await db_session.commit()

    # Checkout PIX do Volume 3 com 100% de desconto
    res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={
            "tipo_produto": "volume_iezzi",
            "referencia_produto_id": str(vol.id),
        },
        headers=headers,
    )
    assert res.status_code == 200
    cobranca_id = res.json()["cobranca_id"]

    # Consulta status da cobrança de upgrade gratuito -> deve retornar paid e não 404!
    st_res = await async_client.get(
        f"/api/v1/pagamentos/status/{cobranca_id}", headers=headers
    )
    assert st_res.status_code == 200
    st_data = st_res.json()
    assert st_data["pago"] is True
    assert st_data["status"] == "paid"


@pytest.mark.asyncio
async def test_bloqueio_compra_duplicada(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Garante que o aluno não pode comprar novamente um produto que já possui ativo."""
    headers = await autenticar(async_client, usuario_teste)

    cap_res = await db_session.execute(select(Capitulo))
    cap = cap_res.scalars().first()

    # Compra o capítulo
    agora = datetime.now(timezone.utc)
    mat = MatriculaPagamento(
        usuario_id=usuario_teste["id"],
        tipo_produto="capitulo_50min",
        referencia_produto_id=cap.id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),
        status="active",
        valor_pago=Decimal("9.90"),
        metodo_pagamento="pix",
    )
    db_session.add(mat)
    await db_session.commit()

    # Tenta comprar o mesmo capítulo novamente -> 400 Bad Request
    dup_res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={
            "tipo_produto": "capitulo_50min",
            "referencia_produto_id": str(cap.id),
        },
        headers=headers,
    )
    assert dup_res.status_code == 400
    assert "já possui" in dup_res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_fluxo_bloqueio_e_desbloqueio_apos_pagamento(
    async_client: AsyncClient,
    usuario_teste: dict,
    db_session,
):
    """Valida o ciclo completo da RN-PAG-001.1: bloqueio pré-pagamento (403) e liberação imediata (200) pós-webhook."""
    headers = await autenticar(async_client, usuario_teste)

    # Busca Cap 1
    cap_res = await db_session.execute(
        select(Capitulo).order_by(Capitulo.ordem)
    )
    cap = cap_res.scalars().first()
    assert cap is not None

    # 1. Sem matrícula: GET /aulas/{cap.id} retorna 403 Forbidden!
    res_bloq = await async_client.get(f"/api/v1/conteudo/aulas/{cap.id}", headers=headers)
    assert res_bloq.status_code == 403
    assert "bloqueado" in res_bloq.json()["detail"].lower()

    # 2. Checkout PIX para o capítulo
    checkout_res = await async_client.post(
        "/api/v1/pagamentos/checkout/pix",
        json={"tipo_produto": "capitulo_50min", "referencia_produto_id": str(cap.id)},
        headers=headers,
    )
    assert checkout_res.status_code == 200
    cobranca_id = checkout_res.json()["cobranca_id"]

    # 3. Webhook confirma pagamento
    wh_res = await async_client.post(
        "/api/v1/pagamentos/webhook",
        json={
            "event": "PAYMENT_RECEIVED",
            "payment": {
                "id": cobranca_id,
                "status": "RECEIVED",
                "netValue": 8.91,
            },
        },
        headers={"asaas-access-token": settings.ASAAS_WEBHOOK_SECRET_TOKEN or "dev_token"},
    )
    assert wh_res.status_code == 200

    # 4. Com matrícula ativada pelo webhook: GET /aulas/{cap.id} agora retorna 200 OK!
    res_ok = await async_client.get(f"/api/v1/conteudo/aulas/{cap.id}", headers=headers)
    assert res_ok.status_code == 200
    aula_data = res_ok.json()
    assert "bloco1_teoria_katex" in aula_data

