---
title: Pagamento - Serviço de Webhook e Idempotência
type: module
status: draft
related:
  - modules/pagamento/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Serviço de Webhook de PIX Instantâneo e Idempotência

Implementação do processamento assíncrono de notificações de pagamento do gateway (Padrão Asaas / MercadoPago), com verificação de assinatura, prevenção de transações duplicadas e ativação imediata de vigência de 12 meses.

---

## Código Fonte (`backend/app/modules/payment/webhook_service.py`)

```python
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

import secrets
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.modules.payment.schemas import GatewayWebhookPayload


class WebhookService:
    """Processador resiliente de notificações de pagamento."""

    @staticmethod
    async def processar_notificacao_gateway(
        db: AsyncSession,
        payload: GatewayWebhookPayload,
        token_recebido: str,
        token_esperado: str
    ) -> Dict[str, Any]:
        """
        Valida segurança, garante idempotência estrita e ativa a matrícula por 365 dias.
        """
        # 1. Validação em tempo constante contra timing attack
        if not secrets.compare_digest(token_recebido, token_esperado):
            raise PermissionError("Assinatura de webhook inválida ou não autorizada.")

        # Só processa eventos de pagamento concluído
        if payload.event not in ("PAYMENT_RECEIVED", "PAYMENT_CONFIRMED"):
            return {"status": "ignorado", "evento": payload.event}

        payment_data = payload.payment
        gateway_cobranca_id = payment_data.id  # Ex: 'pay_982347109283'

        # 2. Garantia de Idempotência: Checa se a transação já foi processada anteriormente
        stmt_transacao_existente = select(TransacaoFinanceira).where(
            TransacaoFinanceira.gateway_payload["id"].astext == gateway_cobranca_id
        )
        result_transacao = await db.execute(stmt_transacao_existente)
        if result_transacao.scalar_one_or_none():
            # Notificação duplicada reenviada pelo gateway: retorna 200 OK sem reprocessar
            return {"status": "ja_processado", "cobranca_id": gateway_cobranca_id}

        # 3. Decodifica o externalReference: "usuario_id:tipo_produto:referencia_produto_id"
        partes = payment_data.externalReference.split(":")
        if len(partes) != 3:
            raise ValueError("Formato de externalReference inválido.")

        usuario_id = UUID(partes[0])
        tipo_produto = partes[1]
        referencia_produto_id = UUID(partes[2])

        # 4. Ativação ou Renovação da Matrícula por 365 dias (12 meses)
        agora = datetime.utcnow()
        data_expiracao_calculada = agora + timedelta(days=365)

        # Verifica se já existia matrícula anterior para renovação
        stmt_matricula = select(MatriculaPagamento).where(
            and_(
                MatriculaPagamento.usuario_id == usuario_id,
                MatriculaPagamento.tipo_produto == tipo_produto,
                MatriculaPagamento.referencia_produto_id == referencia_produto_id
            )
        )
        result_matricula = await db.execute(stmt_matricula)
        matricula = result_matricula.scalar_one_or_none()

        if matricula:
            # Renovação de vigência por mais 12 meses
            matricula.status = "active"
            matricula.data_expiracao = data_expiracao_calculada
            matricula.valor_pago = payment_data.value
            matricula.data_inicio = agora
        else:
            # Nova matrícula ativada
            matricula = MatriculaPagamento(
                id=uuid4(),
                usuario_id=usuario_id,
                tipo_produto=tipo_produto,
                referencia_produto_id=referencia_produto_id,
                status="active",
                data_inicio=agora,
                data_expiracao=data_expiracao_calculada,
                valor_pago=payment_data.value
            )
            db.add(matricula)

        await db.flush()

        # 5. Registro Contábil Auditável na tabela transacoes_financeiras
        taxa_gateway = round(payment_data.value - payment_data.netValue, 2)
        transacao = TransacaoFinanceira(
            id=uuid4(),
            matricula_id=matricula.id,
            usuario_id=usuario_id,
            valor_bruto=payment_data.value,
            taxa_gateway=taxa_gateway,
            valor_liquido=payment_data.netValue,
            metodo="pix" if payment_data.billingType == "PIX" else "credit_card",
            status_transacao="paid",
            gateway_payload=payment_data.dict(),
            pago_em=payment_data.confirmedDate or agora
        )
        db.add(transacao)

        await db.commit()

        return {
            "status": "sucesso",
            "matricula_id": str(matricula.id),
            "vigencia_ate": data_expiracao_calculada.isoformat(),
            "valor_liquido": payment_data.netValue
        }
```
