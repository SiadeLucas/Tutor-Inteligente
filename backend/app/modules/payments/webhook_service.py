"""
Serviço de Processamento de Webhooks Asaas (Idempotência e Segurança Timing-Safe).
Conforme especificações em docs-site/docs/implementation/etapa-09-pagamento.md (Seção 9.3).
"""
import secrets
import logging
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.payment import TransacaoFinanceira, MatriculaPagamento

logger = logging.getLogger("app.modules.payments.webhook_service")


def validar_token(token_recebido: Optional[str], token_esperado: Optional[str]) -> bool:
    """
    Usa secrets.compare_digest para evitar ataques de análise de tempo (timing attacks)
    na verificação do token secreto de webhook do gateway Asaas.
    """
    if not token_recebido or not token_esperado:
        # Se nenhuma chave configurada em dev, permite token padrão dev se idêntico
        return False
    return secrets.compare_digest(str(token_recebido).strip().encode(), str(token_esperado).strip().encode())


async def processar_webhook_asaas(db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa eventos de pagamento do Asaas garantindo estrita idempotência.
    Eventos suportados: PAYMENT_RECEIVED, PAYMENT_CONFIRMED, PAYMENT_REFUNDED.
    """
    event_type = payload.get("event")
    payment_data = payload.get("payment", {})
    payment_id = payment_data.get("id")

    if not payment_id:
        return {"status": "ignored", "reason": "no_payment_id"}

    # 1. Idempotência: busca transação existente
    stmt = select(TransacaoFinanceira).where(
        TransacaoFinanceira.gateway_transacao_id == payment_id
    )
    result = await db.execute(stmt)
    transacao = result.scalar_one_or_none()

    # Se pagamento recebido ou confirmado
    if event_type in ("PAYMENT_RECEIVED", "PAYMENT_CONFIRMED"):
        if transacao and transacao.status_transacao == "paid":
            logger.info(f"Webhook idempotente: cobrança {payment_id} já foi processada anteriormente.")
            return {"status": "already_processed", "idempotent": True, "transacao_id": str(transacao.id)}

        agora = datetime.now(timezone.utc)
        expiracao_365_dias = agora + timedelta(days=365)

        if transacao:
            transacao.status_transacao = "paid"
            transacao.pago_em = agora
            transacao.gateway_payload = payload
            if "netValue" in payment_data:
                valor_bruto = transacao.valor_bruto
                valor_liquido = Decimal(str(payment_data["netValue"]))
                transacao.valor_liquido = valor_liquido
                transacao.taxa_gateway = max(Decimal("0.00"), valor_bruto - valor_liquido)

            # Ativa ou renova a matrícula associada por 365 dias
            if transacao.matricula_id:
                mat_res = await db.execute(
                    select(MatriculaPagamento).where(MatriculaPagamento.id == transacao.matricula_id)
                )
                matricula = mat_res.scalar_one_or_none()
                if matricula:
                    matricula.status = "active"
                    matricula.data_inicio = agora
                    matricula.data_expiracao = expiracao_365_dias
                    matricula.transacao_gateway_id = payment_id

            await db.commit()
            return {"status": "success", "action": "payment_confirmed", "transacao_id": str(transacao.id)}

        else:
            # Transação ainda não existia no banco local
            logger.warning(f"Cobrança {payment_id} não encontrada localmente. Ignorando ou registrando.")
            return {"status": "not_found", "payment_id": payment_id}

    # Eventos informativos sem efeito financeiro: resposta uniforme (sempre com 'status')
    # NOTA: PAYMENT_REFUNDED NÃO está aqui — precisa cair no handler de estorno abaixo,
    # para revogar a matrícula quando o reembolso é iniciado direto no painel do Asaas.
    elif event_type in (
        "PAYMENT_CREATED",
        "PAYMENT_UPDATED",
        "PAYMENT_OVERDUE",
        "PAYMENT_DELETED",
        "PAYMENT_RECEIVE_IN_CASH",
    ):
        return {"status": "ignored", "event": event_type}

    # Se estorno / reembolso
    elif event_type in ("PAYMENT_REFUNDED", "PAYMENT_CHARGEBACK"):
        if transacao:
            transacao.status_transacao = "refunded"
            transacao.gateway_payload = payload
            if transacao.matricula_id:
                mat_res = await db.execute(
                    select(MatriculaPagamento).where(MatriculaPagamento.id == transacao.matricula_id)
                )
                matricula = mat_res.scalar_one_or_none()
                if matricula:
                    matricula.status = "canceled"
            await db.commit()
            return {"status": "success", "action": "payment_refunded", "transacao_id": str(transacao.id)}

    return {"status": "ignored", "event": event_type, "payment_id": payment_id}
