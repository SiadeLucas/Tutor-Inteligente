---
title: Pagamento - Schemas e DTOs
type: module
status: draft
related:
  - modules/pagamento/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs (Pydantic v2 & TypeScript)

Contratos tipados para checkout in-app, emissão de PIX dinâmico, cálculo de upgrade proporcional e eventos de webhook do gateway.

---

## 1. Modelos Backend em Python (`app/modules/payment/schemas.py`)

```python
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# 1. Requisições e Respostas de Checkout
# ============================================================================

class CheckoutPixRequest(BaseModel):
    tipo_produto: Literal["capitulo_50min", "volume_iezzi", "passe_global"]
    referencia_produto_id: UUID = Field(
        ..., 
        description="ID do capítulo ou volume didático que o estudante deseja adquirir"
    )


class PixQrCodeResponse(BaseModel):
    cobranca_id: str = Field(..., description="ID da cobrança gerada no gateway (Asaas/MercadoPago)")
    qr_code_base64: str = Field(..., description="Imagem do QR Code em Base64 para renderização direta")
    copia_cola: str = Field(..., description="Chave alfanumérica Copia e Cola do PIX")
    valor: float = Field(..., description="Valor nominal a ser pago em R$")
    expira_em_segundos: int = Field(900, description="Tempo limite de 15 minutos (900s)")
    expira_em_timestamp: datetime


class CheckoutCartaoRequest(BaseModel):
    tipo_produto: Literal["capitulo_50min", "volume_iezzi", "passe_global"]
    referencia_produto_id: UUID
    token_cartao: str = Field(..., description="Token seguro gerado client-side pelo SDK do gateway")
    parcelas: int = Field(1, ge=1, le=12, description="Número de parcelas (1 a 12x)")


class CheckoutCartaoResponse(BaseModel):
    sucesso: bool
    matricula_id: UUID
    status_transacao: Literal["paid", "waiting_payment", "refused"]
    mensagem: str


# ============================================================================
# 2. Cálculo Dinâmico de Abatimento Proporcional (Upgrade)
# ============================================================================

class UpgradeCalculationResponse(BaseModel):
    volume_id: UUID
    titulo_volume: str
    preco_tabela_volume: float = Field(..., description="Preço de tabela (ex: R$ 49,90)")
    total_ja_investido_capitulos: float = Field(..., description="Soma dos valores pagos em capítulos deste volume")
    capitulos_adquiridos_count: int
    capitulos_adquiridos_ids: List[UUID]
    valor_final_com_abatimento: float = Field(
        ..., 
        description="Preço final = max(0, preco_tabela - total_ja_investido)"
    )
    desconto_obtido: float


# ============================================================================
# 3. Payload do Webhook do Gateway (Padrão Asaas / MercadoPago)
# ============================================================================

class WebhookPaymentData(BaseModel):
    id: str
    customer: str
    value: float
    netValue: float
    billingType: Literal["PIX", "CREDIT_CARD"]
    status: str
    externalReference: str = Field(
        ..., 
        description="ID interno no formato: usuario_id:tipo_produto:referencia_produto_id"
    )
    confirmedDate: Optional[datetime] = None


class GatewayWebhookPayload(BaseModel):
    event: Literal["PAYMENT_RECEIVED", "PAYMENT_CONFIRMED", "PAYMENT_REFUNDED"]
    payment: WebhookPaymentData
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/payment.ts`)

```typescript
export type TipoProduto = "capitulo_50min" | "volume_iezzi" | "passe_global";

export interface PixQrCodeData {
  cobranca_id: string;
  qr_code_base64: string;
  copia_cola: string;
  valor: number;
  expira_em_segundos: number;
  expira_em_timestamp: string;
}

export interface UpgradeCalculation {
  volume_id: string;
  titulo_volume: string;
  preco_tabela_volume: number;
  total_ja_investido_capitulos: number;
  capitulos_adquiridos_count: number;
  capitulos_adquiridos_ids: string[];
  valor_final_com_abatimento: number;
  desconto_obtido: number;
}
```
