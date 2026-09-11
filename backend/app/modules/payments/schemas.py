"""
Schemas Pydantic para Checkout e Pagamentos (Asaas).
"""
from uuid import UUID
from decimal import Decimal
from typing import Optional, Literal, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CalcularUpgradeResponse(BaseModel):
    """Resposta do cálculo de abatimento proporcional de volume (RN-PAG-005)."""
    volume_id: UUID
    preco_original: float
    total_abatimento: float
    valor_final: float
    capitulos_abatidos_count: int
    gratis_por_upgrade: bool


class CheckoutPixRequest(BaseModel):
    """Solicitação de checkout via PIX."""
    tipo_produto: Literal["capitulo_50min", "volume_iezzi", "passe_global"]
    referencia_produto_id: Optional[UUID] = None


class CheckoutPixResponse(BaseModel):
    """Retorno do checkout PIX com QR Code e Copia e Cola."""
    cobranca_id: str
    valor: float
    pix_copia_e_cola: str
    pix_qrcode_base64: str
    expira_em: datetime
    gratis_por_upgrade: bool = False
    matricula_id: Optional[UUID] = None


class DadosCartaoCredito(BaseModel):
    """Dados de cartão de crédito para tokenização / cobrança direta."""
    nome_titular: str
    numero_cartao: str
    mes_expiracao: str
    ano_expiracao: str
    cvv: str


class CheckoutCartaoRequest(BaseModel):
    """Solicitação de checkout via Cartão de Crédito."""
    tipo_produto: Literal["capitulo_50min", "volume_iezzi", "passe_global"]
    referencia_produto_id: Optional[UUID] = None
    cartao: DadosCartaoCredito
    parcelas: int = Field(default=1, ge=1, le=12)


class CheckoutCartaoResponse(BaseModel):
    """Retorno do checkout de Cartão."""
    cobranca_id: str
    status: str
    valor: float
    pago: bool
    matricula_id: Optional[UUID] = None
    gratis_por_upgrade: bool = False


class StatusCobrancaResponse(BaseModel):
    """Status de cobrança para polling leve de 3s no frontend."""
    cobranca_id: str
    status: str
    pago: bool
    matricula_id: Optional[UUID] = None


class MatriculaProdutoResponse(BaseModel):
    """Detalhes de matrícula ativa do usuário."""
    id: UUID
    tipo_produto: str
    referencia_produto_id: Optional[UUID] = None
    titulo_produto: str
    data_inicio: datetime
    data_expiracao: datetime
    dias_restantes: int
    status: str
    valor_pago: float

    model_config = ConfigDict(from_attributes=True)


class SimularPagamentoRequest(BaseModel):
    """Payload para testar confirmação de pagamento em ambiente local/dev."""
    cobranca_id: str
