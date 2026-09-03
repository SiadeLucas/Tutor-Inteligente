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
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
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

    # Se o valor for R$ 0,00 (já pagou capítulos suficientes para cobrir o volume)
    if valor_a_cobrar <= 0.00:
        raise HTTPException(
            status_code=400, 
            detail="Você já possui créditos suficientes para este volume. O upgrade é imediato!"
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
# 3. Polling de Status do PIX em Tempo Real (A cada 3 segundos no Modal)
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

    stmt = select(TransacaoFinanceira).where(
        TransacaoFinanceira.gateway_payload["id"].astext == cobranca_id
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
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
```
