---
title: Pagamento - Endpoints da API FastAPI
type: module
status: draft
related:
  - modules/pagamento/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Endpoints da API FastAPI

Implementação das rotas de checkout de produtos (PIX e Cartão), cálculo de upgrade proporcional e listener de webhooks (`app/modules/payment/router.py`).

---

## Código Fonte (`backend/app/modules/payment/router.py`)

```python
from uuid import UUID, uuid4
from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.config import settings
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.modules.auth.dependencies import get_current_user
from app.modules.payment.schemas import (
    CheckoutPixRequest,
    PixQrCodeResponse,
    CheckoutCartaoRequest,
    CheckoutCartaoResponse,
    UpgradeCalculationResponse,
    GatewayWebhookPayload
)
from app.modules.payment.upgrade_service import UpgradeService
from app.modules.payment.webhook_service import WebhookService

router = APIRouter(prefix="/api/v1/pagamentos", tags=["Pagamentos & Checkout"])


# ============================================================================
# 1. Consulta de Abatimento Proporcional para Upgrade
# ============================================================================

@router.get("/calcular-upgrade/{volume_id}", response_model=UpgradeCalculationResponse)
async def consultar_upgrade(
    volume_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Calcula dinamicamente a dedução de 100% dos capítulos já pagos pelo estudante
    para exibição na tela de confirmação de upgrade do volume.
    """
    try:
        resultado = await UpgradeService.calcular_upgrade_volume(
            db=db,
            usuario_id=current_user.id,
            volume_id=volume_id
        )
        return resultado
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


# ============================================================================
# 2. Emissão de PIX Dinâmico com QR Code
# ============================================================================

@router.post("/checkout/pix", response_model=PixQrCodeResponse)
async def criar_checkout_pix(
    payload: CheckoutPixRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Emite cobrança PIX no gateway Asaas/MercadoPago com expiração estrita de 15 minutos.
    Retorna imagem do QR Code em Base64 e a chave alfanumérica Copia e Cola.
    """
    # Se for compra de volume, verifica se tem direito a desconto de upgrade
    valor_a_cobrar = 49.90  # Valor base do volume
    if payload.tipo_produto == "volume_iezzi":
        upgrade_info = await UpgradeService.calcular_upgrade_volume(
            db, current_user.id, payload.referencia_produto_id
        )
        valor_a_cobrar = upgrade_info.valor_final_com_abatimento

    # Se o valor for R$ 0,00 (já pagou capítulos suficientes para cobrir o volume por upgrade integral)
    if valor_a_cobrar <= 0.00:
        nova_matricula = MatriculaPagamento(
            id=uuid4(),
            usuario_id=current_user.id,
            tipo_produto="volume_iezzi",
            referencia_produto_id=payload.referencia_produto_id,
            data_inicio=datetime.utcnow(),
            data_expiracao=datetime.utcnow() + timedelta(days=365),
            status="active",
            valor_pago=0.00,
            metodo_pagamento="upgrade_credito"
        )
        db.add(nova_matricula)
        await db.commit()
        return PixQrCodeResponse(
            cobranca_id=f"upgrade_concluido_{nova_matricula.id}",
            qr_code_base64="",
            copia_cola="UPGRADE_CONCLUIDO_COM_SUCESSO",
            valor=0.00,
            expira_em_segundos=0,
            expira_em_timestamp=datetime.utcnow()
        )

    # externalReference: identificador seguro para reconciliação no webhook
    ext_ref = f"{current_user.id}:{payload.tipo_produto}:{payload.referencia_produto_id}"

    # Chamada fictícia ao SDK do Asaas (exemplo de retorno formatado)
    expiracao = datetime.utcnow() + timedelta(minutes=15)
    
    return PixQrCodeResponse(
        cobranca_id="pay_asaas_873216892",
        qr_code_base64="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
        copia_cola="00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000520400005303986540549.905802BR5913Tutor Inteligente6009Sao Paulo62070503***6304E2CA",
        valor=valor_a_cobrar,
        expira_em_segundos=900,
        expira_em_timestamp=expiracao
    )


# ============================================================================
# 3. Checkout com Cartão de Crédito (até 12x)
# ============================================================================

@router.post("/checkout/cartao", response_model=CheckoutCartaoResponse)
async def criar_checkout_cartao(
    payload: CheckoutCartaoRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Processa pagamento transparente via Cartão de Crédito tokenizado pelo SDK frontend.
    Concede acesso e ativa a matrícula de 365 dias instantaneamente em caso de aprovação.
    """
    from uuid import uuid4
    from app.models.payment import MatriculaPagamento, TransacaoFinanceira

    # Calcula abatimento se for upgrade de volume
    valor_final = 49.90 if payload.tipo_produto == "volume_iezzi" else 9.90
    if payload.tipo_produto == "volume_iezzi":
        upgrade_info = await UpgradeService.calcular_upgrade_volume(
            db, current_user.id, payload.referencia_produto_id
        )
        valor_final = upgrade_info.valor_final_com_abatimento

    # Simula chamada autorizada ao gateway com token PCI-DSS
    # Em produção: gateway_client.charges.create(...)
    transacao_id = f"tx_card_{uuid4().hex[:12]}"
    
    # Cria a matrícula imediatamente
    matricula = MatriculaPagamento(
        id=uuid4(),
        usuario_id=current_user.id,
        tipo_produto=payload.tipo_produto,
        referencia_produto_id=payload.referencia_produto_id,
        data_inicio=datetime.utcnow(),
        data_expiracao=datetime.utcnow() + timedelta(days=365),
        status="active",
        valor_pago=valor_final,
        metodo_pagamento="credit_card",
        transacao_gateway_id=transacao_id
    )
    db.add(matricula)

    # Registra a transação contábil
    transacao = TransacaoFinanceira(
        id=uuid4(),
        matricula_id=matricula.id,
        usuario_id=current_user.id,
        valor_bruto=valor_final,
        taxa_gateway=round(valor_final * 0.0399, 2), # Exemplo taxa 3.99%
        valor_liquido=round(valor_final * 0.9601, 2),
        status_transacao="paid",
        pago_em=datetime.utcnow()
    )
    db.add(transacao)
    await db.commit()

    return CheckoutCartaoResponse(
        sucesso=True,
        transacao_id=transacao_id,
        mensagem="Pagamento com cartão aprovado! Acesso liberado por 12 meses.",
        matricula_id=matricula.id,
        vigencia_ate=matricula.data_expiracao
    )


# ============================================================================
# 4. Polling de Status do PIX em Tempo Real (A cada 3 segundos no Modal)
# ============================================================================

@router.get("/status/{cobranca_id}")
async def consultar_status_pix(
    cobranca_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Rota de alta frequência consultada pelo modal do aluno a cada 3 segundos.
    Retorna pago=True assim que o webhook do gateway confirmar o recebimento,
    permitindo o redirecionamento imediato para a aula desbloqueada.
    """
    from app.models.payment import TransacaoFinanceira
    from sqlalchemy import select

    # Validação IDOR estrita: a cobrança deve pertencer ao estudante autenticado
    stmt = select(TransacaoFinanceira).where(
        and_(
            TransacaoFinanceira.gateway_payload["id"].astext == cobranca_id,
            TransacaoFinanceira.usuario_id == current_user.id
        )
    )
    result = await db.execute(stmt)
    tx = result.scalar_one_or_none()

    if tx and tx.status_transacao == "paid":
        return {
            "pago": True,
            "status": "paid",
            "mensagem": "Pagamento confirmado instantaneamente via PIX!",
            "liberado_em": tx.pago_em
        }

    return {
        "pago": False,
        "status": "waiting_payment",
        "mensagem": "Aguardando confirmação bancária..."
    }


# ============================================================================
# 4. Webhook de Confirmação Instantânea do Gateway
# ============================================================================

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def receber_webhook_gateway(
    payload: GatewayWebhookPayload,
    asaas_access_token: str = Header(..., alias="asaas-access-token"),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint público que recebe os eventos assíncronos do gateway.
    Valida token, garante idempotência e ativa a matrícula de 12 meses imediatamente.
    """
    try:
        resultado = await WebhookService.processar_notificacao_gateway(
            db=db,
            payload=payload,
            token_recebido=asaas_access_token,
            token_esperado=settings.ASAAS_WEBHOOK_SECRET_TOKEN
        )
        return {"status": "ok", "resultado": resultado}
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de webhook inválido.")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha interna ao processar notificação de pagamento."
        )


# ============================================================================
# 5. Consulta de Matrículas e Produtos Ativos do Aluno
# ============================================================================

@router.get("/meus-produtos")
async def listar_meus_produtos(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RN-PAG-006 / RN-PAG-007: Retorna todos os produtos e volumes com vigência ativa (365 dias)
    adquiridos pelo estudante autenticado para controle de acesso na Skill Tree.
    """
    stmt = (
        select(MatriculaPagamento)
        .where(
            and_(
                MatriculaPagamento.usuario_id == current_user.id,
                MatriculaPagamento.status == "active",
                MatriculaPagamento.data_expiracao > datetime.utcnow()
            )
        )
        .order_by(MatriculaPagamento.data_expiracao.desc())
    )
    result = await db.execute(stmt)
    matriculas = result.scalars().all()

    return [
        {
            "matricula_id": str(m.id),
            "tipo_produto": m.tipo_produto,
            "referencia_produto_id": str(m.referencia_produto_id) if m.referencia_produto_id else None,
            "data_inicio": m.data_inicio.isoformat(),
            "data_expiracao": m.data_expiracao.isoformat(),
            "dias_restantes": max(0, (m.data_expiracao - datetime.utcnow()).days),
            "valor_pago": float(m.valor_pago)
        }
        for m in matriculas
    ]
```
