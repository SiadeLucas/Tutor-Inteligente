"""
Endpoints REST FastAPI para Pagamento, Upgrade e Checkout Asaas.
Conforme especificações em docs-site/docs/implementation/etapa-09-pagamento.md (Seção 9.4).
"""
import uuid
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import Usuario
from app.models.content import Capitulo, VolumeDidatico
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.modules.payments.schemas import (
    CalcularUpgradeResponse,
    CheckoutPixRequest,
    CheckoutPixResponse,
    CheckoutCartaoRequest,
    CheckoutCartaoResponse,
    StatusCobrancaResponse,
    MatriculaProdutoResponse,
    SimularPagamentoRequest,
)
from app.modules.payments.upgrade_calculator import calcular_abatimento_volume
from app.modules.payments.asaas_service import asaas_service
from app.modules.payments.webhook_service import validar_token, processar_webhook_asaas

router = APIRouter(prefix="/api/v1/pagamentos", tags=["Pagamento e Checkout"])

PRECO_PASSE_GLOBAL = Decimal("199.00")
PRECO_PADRAO_CAPITULO = Decimal("9.90")
PRECO_PADRAO_VOLUME = Decimal("49.90")


async def _ativar_matricula_upgrade_gratis(
    db: AsyncSession,
    usuario: Usuario,
    tipo_produto: str,
    referencia_produto_id: UUID,
) -> MatriculaPagamento:
    """
    Ativa instantaneamente uma matrícula quando o abatimento de capítulos avulsos
    cobre 100% do preço do volume (RN-PAG-005), sem passar pelo gateway Asaas.
    Cria a TransacaoFinanceira auditável (R$ 0,00, status 'paid') correspondente.
    """
    agora = datetime.now(timezone.utc)
    cobranca_id_free = f"upg_free_{referencia_produto_id.hex[:12]}"
    matricula = MatriculaPagamento(
        usuario_id=usuario.id,
        tipo_produto=tipo_produto,
        referencia_produto_id=referencia_produto_id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(days=365),  # RN-PAG-006: 365 dias de acesso
        status="active",
        valor_pago=Decimal("0.00"),
        metodo_pagamento="upgrade_gratis",
        transacao_gateway_id=cobranca_id_free,
    )
    db.add(matricula)
    await db.flush()

    transacao_free = TransacaoFinanceira(
        matricula_id=matricula.id,
        usuario_id=usuario.id,
        gateway_transacao_id=cobranca_id_free,
        valor_bruto=Decimal("0.00"),
        taxa_gateway=Decimal("0.00"),
        valor_liquido=Decimal("0.00"),
        status_transacao="paid",
        metodo="upgrade_gratis",
        gateway_payload={"tipo": "upgrade_gratis_100", "volume_id": str(referencia_produto_id)},
        pago_em=agora,
    )
    db.add(transacao_free)
    await db.commit()
    await db.refresh(matricula)
    return matricula


async def _verificar_compra_duplicada(
    db: AsyncSession,
    usuario_id: UUID,
    tipo_produto: str,
    referencia_produto_id: Optional[UUID],
) -> None:
    """Impede cobranças duplicadas para produtos já ativos na conta do aluno."""
    agora = datetime.now(timezone.utc)
    # Se já tem Passe Global ativo, não precisa comprar nada mais
    res_pg = await db.execute(
        select(MatriculaPagamento.id).where(
            and_(
                MatriculaPagamento.usuario_id == usuario_id,
                MatriculaPagamento.tipo_produto == "passe_global",
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > agora,
            )
        )
    )
    if res_pg.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já possui um Passe Global ativo com acesso ilimitado a todos os conteúdos.",
        )

    if tipo_produto == "passe_global":
        return

    if tipo_produto == "volume_iezzi":
        res_vol = await db.execute(
            select(MatriculaPagamento.id).where(
                and_(
                    MatriculaPagamento.usuario_id == usuario_id,
                    MatriculaPagamento.tipo_produto == "volume_iezzi",
                    MatriculaPagamento.referencia_produto_id == referencia_produto_id,
                    MatriculaPagamento.status == "active",
                    MatriculaPagamento.data_expiracao > agora,
                )
            )
        )
        if res_vol.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já possui uma matrícula ativa para este volume didático.",
            )

    elif tipo_produto == "capitulo_50min":
        res_cap = await db.execute(
            select(MatriculaPagamento.id).where(
                and_(
                    MatriculaPagamento.usuario_id == usuario_id,
                    MatriculaPagamento.tipo_produto == "capitulo_50min",
                    MatriculaPagamento.referencia_produto_id == referencia_produto_id,
                    MatriculaPagamento.status == "active",
                    MatriculaPagamento.data_expiracao > agora,
                )
            )
        )
        if res_cap.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já possui uma matrícula ativa para este capítulo.",
            )
        cap_res = await db.execute(select(Capitulo.volume_id).where(Capitulo.id == referencia_produto_id))
        vol_id = cap_res.scalar_one_or_none()
        if vol_id:
            res_vol = await db.execute(
                select(MatriculaPagamento.id).where(
                    and_(
                        MatriculaPagamento.usuario_id == usuario_id,
                        MatriculaPagamento.tipo_produto == "volume_iezzi",
                        MatriculaPagamento.referencia_produto_id == vol_id,
                        MatriculaPagamento.status == "active",
                        MatriculaPagamento.data_expiracao > agora,
                    )
                )
            )
            if res_vol.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Você já possui acesso a este capítulo através do volume didático adquirido.",
                )


# ============================================================================
# 1. GET /api/v1/pagamentos/calcular-upgrade/{volume_id}
# ============================================================================
@router.get(
    "/calcular-upgrade/{volume_id}",
    response_model=CalcularUpgradeResponse,
    summary="Calcular abatimento proporcional para aquisição de volume",
)
async def calcular_upgrade(
    volume_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    RN-PAG-005: 100% do valor gasto em capítulos avulsos do volume_id
    é abatido do preço total do volume didático no checkout.
    """
    calc = await calcular_abatimento_volume(db, usuario.id, volume_id)
    if not calc.get("volume_encontrado"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume didático não encontrado.",
        )

    return CalcularUpgradeResponse(
        volume_id=volume_id,
        preco_original=float(calc["preco_original"]),
        total_abatimento=float(calc["total_abatimento"]),
        valor_final=float(calc["valor_final"]),
        capitulos_abatidos_count=calc["capitulos_abatidos_count"],
        gratis_por_upgrade=calc["gratis_por_upgrade"],
    )


# ============================================================================
# 2. POST /api/v1/pagamentos/checkout/pix
# ============================================================================
@router.post(
    "/checkout/pix",
    response_model=CheckoutPixResponse,
    summary="Iniciar checkout com emissão de PIX dinâmico (Asaas)",
)
async def checkout_pix(
    dados: CheckoutPixRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Gera cobrança PIX no gateway Asaas com QR Code e Copia e Cola (expiração de 15 min).
    Se o upgrade abater 100% do valor (R$ 0,00), ativa a matrícula imediatamente.
    """
    agora = datetime.now(timezone.utc)
    expiracao_365 = agora + timedelta(days=365)

    # Impede compras redundantes/duplicadas caso já tenha acesso ativo
    await _verificar_compra_duplicada(db, usuario.id, dados.tipo_produto, dados.referencia_produto_id)

    # 1. Determina valor e descrição do produto
    descricao = ""
    valor_a_cobrar = Decimal("0.00")

    if dados.tipo_produto == "volume_iezzi":
        if not dados.referencia_produto_id:
            raise HTTPException(status_code=400, detail="referencia_produto_id é obrigatório para volume.")
        calc = await calcular_abatimento_volume(db, usuario.id, dados.referencia_produto_id)
        if not calc.get("volume_encontrado"):
            raise HTTPException(status_code=404, detail="Volume não encontrado.")

        vol_res = await db.execute(select(VolumeDidatico).where(VolumeDidatico.id == dados.referencia_produto_id))
        vol = vol_res.scalar_one()
        descricao = f"Volume {vol.numero_volume}: {vol.titulo}"

        # Se upgrade zerou o saldo
        if calc["gratis_por_upgrade"]:
            matricula = await _ativar_matricula_upgrade_gratis(
                db, usuario, "volume_iezzi", dados.referencia_produto_id
            )
            return CheckoutPixResponse(
                cobranca_id=matricula.transacao_gateway_id or "",
                valor=0.0,
                pix_copia_e_cola="",
                pix_qrcode_base64="",
                expira_em=matricula.data_expiracao,
                gratis_por_upgrade=True,
                matricula_id=matricula.id,
            )

        valor_a_cobrar = calc["valor_final"]

    elif dados.tipo_produto == "capitulo_50min":
        if not dados.referencia_produto_id:
            raise HTTPException(status_code=400, detail="referencia_produto_id é obrigatório para capítulo.")
        cap_res = await db.execute(select(Capitulo).where(Capitulo.id == dados.referencia_produto_id))
        cap = cap_res.scalar_one_or_none()
        if not cap:
            raise HTTPException(status_code=404, detail="Capítulo não encontrado.")
        descricao = f"Capítulo {cap.numero_capitulo}: {cap.titulo}"
        valor_a_cobrar = Decimal(str(cap.preco_avulso or PRECO_PADRAO_CAPITULO))

    elif dados.tipo_produto == "passe_global":
        descricao = "Passe Global Ilimitado (11 Volumes + IA Especialista)"
        valor_a_cobrar = PRECO_PASSE_GLOBAL

    # 2. Cria registro de matrícula pendente
    # Vigência de 365 dias (RN-PAG-006) começa a contar da ATIVAÇÃO (webhook),
    # não da emissão da cobrança. Enquanto pendente, expira em 30 min (janela do PIX).
    matricula = MatriculaPagamento(
        usuario_id=usuario.id,
        tipo_produto=dados.tipo_produto,
        referencia_produto_id=dados.referencia_produto_id,
        data_inicio=agora,
        data_expiracao=agora + timedelta(minutes=30),
        status="past_due",  # Torna-se 'active' por 365 dias quando confirmado pelo webhook
        valor_pago=valor_a_cobrar,
        metodo_pagamento="pix",
    )
    db.add(matricula)
    await db.flush()

    # 3. Emite PIX no Asaas
    pix_data = await asaas_service.criar_cobranca_pix(
        usuario=usuario,
        valor=valor_a_cobrar,
        descricao=descricao,
        referencia_id=str(matricula.id),
        expiracao_minutos=15,
    )

    matricula.transacao_gateway_id = pix_data["gateway_transacao_id"]

    # 4. Registra a transação financeira contábil
    transacao = TransacaoFinanceira(
        matricula_id=matricula.id,
        usuario_id=usuario.id,
        gateway_transacao_id=pix_data["gateway_transacao_id"],
        valor_bruto=valor_a_cobrar,
        taxa_gateway=Decimal("0.99"),  # Taxa média PIX Asaas
        valor_liquido=valor_a_cobrar - Decimal("0.99"),
        status_transacao="waiting_payment",
        metodo="pix",
        gateway_payload=pix_data.get("raw_payload"),
    )
    db.add(transacao)
    await db.commit()

    return CheckoutPixResponse(
        cobranca_id=pix_data["gateway_transacao_id"],
        valor=float(valor_a_cobrar),
        pix_copia_e_cola=pix_data["pix_copia_e_cola"],
        pix_qrcode_base64=pix_data["pix_qrcode_base64"],
        expira_em=pix_data["expira_em"],
        gratis_por_upgrade=False,
        matricula_id=matricula.id,
    )


# ============================================================================
# 3. POST /api/v1/pagamentos/checkout/cartao
# ============================================================================
@router.post(
    "/checkout/cartao",
    response_model=CheckoutCartaoResponse,
    summary="Processar checkout com Cartão de Crédito",
)
async def checkout_cartao(
    dados: CheckoutCartaoRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Processa compra transparente por Cartão de Crédito com parcelamento em até 12x.
    """
    agora = datetime.now(timezone.utc)
    expiracao_365 = agora + timedelta(days=365)
    descricao = ""
    valor_a_cobrar = Decimal("0.00")

    # Impede compras redundantes/duplicadas caso já tenha acesso ativo
    await _verificar_compra_duplicada(db, usuario.id, dados.tipo_produto, dados.referencia_produto_id)

    if dados.tipo_produto == "volume_iezzi":
        if not dados.referencia_produto_id:
            raise HTTPException(status_code=400, detail="referencia_produto_id é obrigatório para volume.")
        calc = await calcular_abatimento_volume(db, usuario.id, dados.referencia_produto_id)
        if not calc.get("volume_encontrado"):
            raise HTTPException(status_code=404, detail="Volume não encontrado.")

        vol_res = await db.execute(select(VolumeDidatico).where(VolumeDidatico.id == dados.referencia_produto_id))
        vol = vol_res.scalar_one()
        descricao = f"Volume {vol.numero_volume}: {vol.titulo}"

        if calc["gratis_por_upgrade"]:
            matricula = await _ativar_matricula_upgrade_gratis(
                db, usuario, "volume_iezzi", dados.referencia_produto_id
            )
            return CheckoutCartaoResponse(
                cobranca_id=matricula.transacao_gateway_id or "",
                status="paid",
                valor=0.0,
                pago=True,
                matricula_id=matricula.id,
                gratis_por_upgrade=True,
            )
        valor_a_cobrar = calc["valor_final"]

    elif dados.tipo_produto == "capitulo_50min":
        if not dados.referencia_produto_id:
            raise HTTPException(status_code=400, detail="referencia_produto_id é obrigatório.")
        cap_res = await db.execute(select(Capitulo).where(Capitulo.id == dados.referencia_produto_id))
        cap = cap_res.scalar_one_or_none()
        if not cap:
            raise HTTPException(status_code=404, detail="Capítulo não encontrado.")
        descricao = f"Capítulo {cap.numero_capitulo}: {cap.titulo}"
        valor_a_cobrar = Decimal(str(cap.preco_avulso or PRECO_PADRAO_CAPITULO))

    elif dados.tipo_produto == "passe_global":
        descricao = "Passe Global Ilimitado"
        valor_a_cobrar = PRECO_PASSE_GLOBAL

    # Processa no gateway Asaas
    cc_res = await asaas_service.criar_cobranca_cartao(
        usuario=usuario,
        valor=valor_a_cobrar,
        descricao=descricao,
        referencia_id=f"cartao_{uuid.uuid4().hex[:10]}",
        cartao_dados=dados.cartao.model_dump(),
        parcelas=dados.parcelas,
    )

    foi_aprovado = cc_res.get("status") == "paid"
    matricula_status = "active" if foi_aprovado else "past_due"

    matricula = MatriculaPagamento(
        usuario_id=usuario.id,
        tipo_produto=dados.tipo_produto,
        referencia_produto_id=dados.referencia_produto_id,
        data_inicio=agora,
        data_expiracao=expiracao_365,
        status=matricula_status,
        valor_pago=valor_a_cobrar,
        metodo_pagamento="credit_card",
        transacao_gateway_id=cc_res["gateway_transacao_id"],
    )
    db.add(matricula)
    await db.flush()

    transacao = TransacaoFinanceira(
        matricula_id=matricula.id,
        usuario_id=usuario.id,
        gateway_transacao_id=cc_res["gateway_transacao_id"],
        valor_bruto=valor_a_cobrar,
        taxa_gateway=cc_res.get("taxa_gateway", Decimal("2.00")),
        valor_liquido=valor_a_cobrar - cc_res.get("taxa_gateway", Decimal("2.00")),
        status_transacao="paid" if foi_aprovado else "waiting_payment",
        metodo="credit_card",
        gateway_payload=cc_res.get("raw_payload"),
        pago_em=agora if foi_aprovado else None,
    )
    db.add(transacao)
    await db.commit()

    return CheckoutCartaoResponse(
        cobranca_id=cc_res["gateway_transacao_id"],
        status=transacao.status_transacao,
        valor=float(valor_a_cobrar),
        pago=foi_aprovado,
        matricula_id=matricula.id,
        gratis_por_upgrade=False,
    )


# ============================================================================
# 4. GET /api/v1/pagamentos/status/{cobranca_id}
# ============================================================================
@router.get(
    "/status/{cobranca_id}",
    response_model=StatusCobrancaResponse,
    summary="Polling de status de cobrança (com proteção IDOR)",
)
async def consultar_status_cobranca(
    cobranca_id: str,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Usado para polling a cada 3s no frontend durante exibição do QR Code PIX.
    IDOR Check: Valida se a cobrança pertence estritamente ao usuário autenticado (ou Admin).
    """
    stmt = select(TransacaoFinanceira).where(
        TransacaoFinanceira.gateway_transacao_id == cobranca_id
    )
    res = await db.execute(stmt)
    transacao = res.scalar_one_or_none()

    if not transacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cobrança não encontrada.",
        )

    # Proteção IDOR estrita
    if transacao.usuario_id != usuario.id and usuario.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Você não tem permissão para consultar esta transação.",
        )

    esta_pago = transacao.status_transacao == "paid"

    return StatusCobrancaResponse(
        cobranca_id=cobranca_id,
        status=transacao.status_transacao,
        pago=esta_pago,
        matricula_id=transacao.matricula_id,
    )


# ============================================================================
# 5. POST /api/v1/pagamentos/webhook
# ============================================================================
@router.post(
    "/webhook",
    summary="Webhook idempotente do Asaas com proteção contra timing attacks",
)
async def webhook_asaas(
    request: Request,
    db: AsyncSession = Depends(get_db),
    asaas_access_token: Optional[str] = Header(None, alias="asaas-access-token"),
):
    """
    Recebe eventos de liquidação financeira do Asaas.
    - Validação de timing-attack com secrets.compare_digest.
    - Idempotência: não ativa 2 vezes o mesmo pagamento.
    """
    token_esperado = settings.ASAAS_WEBHOOK_SECRET_TOKEN.strip()

    # Validação de segurança (deny-by-default)
    # Sem segredo configurado, apenas ambiente não-produtivo aceita o token de dev padrão.
    if not token_esperado:
        if settings.ENVIRONMENT.lower() == "production":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Webhook não configurado (ASAAS_WEBHOOK_SECRET_TOKEN ausente).",
            )
        token_esperado = "dev_token"

    if not validar_token(asaas_access_token, token_esperado):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de webhook inválido ou não fornecido.",
        )

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Payload JSON inválido.")

    resultado = await processar_webhook_asaas(db, payload)
    return resultado


# ============================================================================
# 6. GET /api/v1/pagamentos/meus-produtos
# ============================================================================
@router.get(
    "/meus-produtos",
    response_model=List[MatriculaProdutoResponse],
    summary="Listar matrículas ativas e produtos adquiridos pelo usuário",
)
async def listar_meus_produtos(
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Retorna as matrículas ativas do usuário com vigência e contagem de dias restantes.
    """
    agora = datetime.now(timezone.utc)
    stmt = (
        select(MatriculaPagamento)
        .where(
            and_(
                MatriculaPagamento.usuario_id == usuario.id,
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > agora,
            )
        )
        .order_by(MatriculaPagamento.data_expiracao.desc())
    )
    res = await db.execute(stmt)
    matriculas = res.scalars().all()

    produtos = []
    for m in matriculas:
        dias_restantes = max(0, (m.data_expiracao - agora).days)
        titulo = "Produto Desconhecido"

        if m.tipo_produto == "passe_global":
            titulo = "Passe Global Ilimitado (Todos os 11 Volumes)"
        elif m.tipo_produto == "volume_iezzi" and m.referencia_produto_id:
            vol_res = await db.execute(
                select(VolumeDidatico).where(VolumeDidatico.id == m.referencia_produto_id)
            )
            vol = vol_res.scalar_one_or_none()
            titulo = f"Volume {vol.numero_volume}: {vol.titulo}" if vol else "Volume Didático"
        elif m.tipo_produto == "capitulo_50min" and m.referencia_produto_id:
            cap_res = await db.execute(
                select(Capitulo).where(Capitulo.id == m.referencia_produto_id)
            )
            cap = cap_res.scalar_one_or_none()
            titulo = f"Capítulo {cap.numero_capitulo}: {cap.titulo}" if cap else "Capítulo 50min"

        produtos.append(
            MatriculaProdutoResponse(
                id=m.id,
                tipo_produto=m.tipo_produto,
                referencia_produto_id=m.referencia_produto_id,
                titulo_produto=titulo,
                data_inicio=m.data_inicio,
                data_expiracao=m.data_expiracao,
                dias_restantes=dias_restantes,
                status=m.status,
                valor_pago=float(m.valor_pago),
            )
        )

    return produtos


# ============================================================================
# 7. POST /api/v1/pagamentos/simular-pagamento (Ambiente de Testes / Dev)
# ============================================================================
@router.post(
    "/simular-pagamento",
    summary="Simular confirmação de pagamento para testes de frontend e polling",
)
async def simular_pagamento(
    dados: SimularPagamentoRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Permite confirmar instantaneamente uma cobrança pendente para facilitar
    a validação do polling e liberação automática no frontend.
    """
    # Segurança: apenas o dono da cobrança (ou Admin) pode simulá-la; só faz sentido
    # em ambiente de desenvolvimento (o frontend esconde o botão [Simular Baixa] em produção).
    stmt = select(TransacaoFinanceira).where(
        TransacaoFinanceira.gateway_transacao_id == dados.cobranca_id
    )
    res = await db.execute(stmt)
    tx = res.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cobrança não encontrada.")
    if tx.usuario_id != usuario.id and usuario.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cobrança não pertence a este usuário.")
    if settings.ENVIRONMENT.lower() == "production":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Simulação desabilitada em produção.")

    net_val = float(tx.valor_bruto - Decimal("0.99")) if tx else 9.00

    payload_webhook = {
        "event": "PAYMENT_RECEIVED",
        "payment": {
            "id": dados.cobranca_id,
            "status": "RECEIVED",
            "netValue": max(0.0, net_val),
        },
    }
    return await processar_webhook_asaas(db, payload_webhook)
