"""
Modelos ORM para Matrículas e Transações Financeiras (Asaas / Checkout).
Conforme especificações em docs-site/docs/knowledge/database/04-matriculas-pagamentos.md e 05-transacoes-financeiras.md.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class MatriculaPagamento(Base):
    """
    Tabela 04: matriculas_pagamentos
    Controla o direito comercial de acesso aos conteúdos da plataforma (vigência de 365 dias).
    """
    __tablename__ = "matriculas_pagamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_produto = Column(String(30), nullable=False)  # 'capitulo_50min' | 'volume_iezzi' | 'passe_global'
    referencia_produto_id = Column(UUID(as_uuid=True), nullable=True)  # capitulo_id OU volume_id (NULL se passe_global)
    data_inicio = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # 'active' | 'past_due' | 'canceled'
    valor_pago = Column(Numeric(10, 2), nullable=False)
    metodo_pagamento = Column(String(20), nullable=False)  # 'pix' | 'credit_card' | 'upgrade_gratis'
    transacao_gateway_id = Column(String(100), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_matriculas_usuario_status", "usuario_id", "status"),
        Index("idx_matriculas_produto", "tipo_produto", "referencia_produto_id"),
    )

    # Relacionamentos
    usuario = relationship("Usuario")
    transacoes = relationship("TransacaoFinanceira", back_populates="matricula")


class TransacaoFinanceira(Base):
    """
    Tabela 05: transacoes_financeiras
    Extrato contábil e financeiro auditável de cobranças, taxas e repasses.
    """
    __tablename__ = "transacoes_financeiras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula_id = Column(UUID(as_uuid=True), ForeignKey("matriculas_pagamentos.id", ondelete="SET NULL"), nullable=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    gateway_transacao_id = Column(String(100), nullable=False, unique=True, index=True)
    valor_bruto = Column(Numeric(10, 2), nullable=False)
    taxa_gateway = Column(Numeric(10, 2), nullable=False, default=0.00)
    valor_liquido = Column(Numeric(10, 2), nullable=False)  # valor_bruto - taxa_gateway
    status_transacao = Column(String(30), nullable=False, default="waiting_payment", index=True)  # 'paid' | 'waiting_payment' | 'refunded'
    metodo = Column(String(20), nullable=False)  # 'pix' | 'credit_card'
    gateway_payload = Column(JSONB, nullable=True)
    pago_em = Column(DateTime(timezone=True), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_transacoes_data", "criado_em"),
    )

    # Relacionamentos
    matricula = relationship("MatriculaPagamento", back_populates="transacoes")
    usuario = relationship("Usuario")

    @property
    def status(self) -> str:
        return self.status_transacao

    @status.setter
    def status(self, val: str):
        self.status_transacao = val
