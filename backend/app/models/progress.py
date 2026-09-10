"""
Modelos ORM para Progresso do Estudante: Heatmap de Domínio (Tabela 15),
Histórico de Theta TRI (Tabela 16) e Horas de Estudo Diárias (Tabela 17),
conforme docs-site/docs/knowledge/database/.
"""
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Numeric,
    Date,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class HeatmapDominio(Base):
    """Tabela 15: heatmap_dominio - Estado visual do domínio por estudante/capítulo."""
    __tablename__ = "heatmap_dominio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=False, index=True)
    total_questoes_respondidas = Column(Integer, nullable=False, default=0)
    taxa_acertos_ponderada = Column(Numeric(5, 2), nullable=False, default=0.00)
    # RN-PRG-012: 'cinza' (<3 itens) | 'vermelho' (<50%) | 'amarelo' (<75%) | 'verde' (>=75%)
    status_cor = Column(String(20), nullable=False, default="cinza", index=True)
    aula_concluida = Column(Boolean, nullable=False, default=False)
    ultima_interacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("usuario_id", "capitulo_id", name="uk_heatmap_usuario_capitulo"),
        Index("idx_heatmap_usuario", "usuario_id"),
        Index("idx_heatmap_usuario_cor", "usuario_id", "status_cor"),
    )

    # Relacionamentos
    usuario = relationship("Usuario")
    capitulo = relationship("Capitulo")


class HistoricoTheta(Base):
    """Tabela 16: historico_theta - Série temporal psicométrica contínua (theta TRI)."""
    __tablename__ = "historico_theta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    disciplina_id = Column(UUID(as_uuid=True), ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    volume_id = Column(UUID(as_uuid=True), ForeignKey("volumes_didaticos.id", ondelete="SET NULL"), nullable=True, index=True)
    # grande_area: os 4 slugs canônicos ('algebra_funcoes' | 'geometria' |
    # 'algebra_linear' | 'aplicada') OU o agregado 'geral' (theta global da prova CAT).
    grande_area = Column(String(50), nullable=False)
    theta_estimado = Column(Numeric(6, 3), nullable=False)  # Escala contínua de -3.000 a +3.000
    erro_padrao_se = Column(Numeric(6, 3), nullable=False)
    origem_ajuste = Column(String(40), nullable=False)  # 'onboarding_cat' | 'marco_cat' | 'micro_ajuste_exercicio'
    registrado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_historico_theta_usuario_disciplina", "usuario_id", "disciplina_id", "registrado_em"),
    )

    # Relacionamentos
    usuario = relationship("Usuario")
    disciplina = relationship("Disciplina")
    volume = relationship("VolumeDidatico")


class HorasEstudoDiarias(Base):
    """Tabela 17: horas_estudo_diarias - Tempo líquido ativo por dia (RN-PRG-003)."""
    __tablename__ = "horas_estudo_diarias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    data_registro = Column(Date, nullable=False)
    segundos_ativos = Column(Integer, nullable=False, default=0)
    aulas_concluidas = Column(Integer, nullable=False, default=0)
    exercicios_submetidos = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("usuario_id", "data_registro", name="uk_horas_usuario_data"),
        Index("idx_horas_estudo_usuario", "usuario_id", "data_registro"),
    )

    # Relacionamentos
    usuario = relationship("Usuario")

