"""
Modelos ORM para o Módulo de Exercícios e Motor Psicométrico CAT.
Conforme especificações em docs-site/docs/knowledge/database/ (Tabelas 11 a 14).
"""
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Numeric,
    ForeignKey,
    DateTime,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ItemExercicio(Base):
    """
    Tabela 11: itens_exercicios
    Banco de itens avaliativos calibrados pela Teoria da Resposta ao Item (TRI).
    """
    __tablename__ = "itens_exercicios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=False)
    tipo_origem = Column(String(30), nullable=False, default="iezzi_original")  # 'iezzi_original' | 'gemea_ia'
    tipo_item = Column(String(30), nullable=False, default="multiple_choice")  # 'multiple_choice' | 'numeric_input'
    item_matriz_id = Column(UUID(as_uuid=True), ForeignKey("itens_exercicios.id", ondelete="SET NULL"), nullable=True)
    enunciado_katex = Column(Text, nullable=False)
    alternativas = Column(JSONB, nullable=False, default=list)  # [{"letra": "A", "texto": "...", "correta": false}]
    resposta_correta = Column(String(50), nullable=False)  # 'A', 'B', etc. ou valor numérico/algébrico
    resolucao_passo_a_passo = Column(Text, nullable=False)
    parametro_a = Column(Numeric(6, 3), nullable=False, default=1.000)  # Discriminação (típico 0.5 a 2.5)
    parametro_b = Column(Numeric(6, 3), nullable=False, default=0.000)  # Dificuldade (-3.0 a +3.0)
    parametro_c = Column(Numeric(6, 3), nullable=False, default=0.200)  # Chute (0.20 para 5 opções)
    metadados_sympy = Column(JSONB, nullable=True)  # Expressão simbólica, raízes, tolerância
    validado_sympy = Column(Boolean, nullable=False, default=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    capitulo = relationship("Capitulo", backref="itens_exercicios")
    item_matriz = relationship("ItemExercicio", remote_side=[id], backref="questoes_gemeas")

    __table_args__ = (
        Index("idx_itens_capitulo", "capitulo_id", "ativo"),
        Index("idx_itens_matriz", "item_matriz_id"),
    )


class TentativaExercicio(Base):
    """
    Tabela 12: tentativas_exercicios
    Registra todas as respostas submetidas, suportando pontuação ponderada (1.0 vs 0.5 vs 0.0).
    """
    __tablename__ = "tentativas_exercicios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("itens_exercicios.id", ondelete="CASCADE"), nullable=False)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=False)
    tentativa_numero = Column(Integer, nullable=False)  # 1 ou 2
    resposta_enviada = Column(String(150), nullable=False)
    acertou = Column(Boolean, nullable=False)
    pontuacao_obtida = Column(Numeric(3, 1), nullable=False)  # 1.0 (1ª) | 0.5 (2ª com dica) | 0.0 (erro)
    usou_dica_ia = Column(Boolean, nullable=False, default=False)
    tempo_resposta_segundos = Column(Integer, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", backref="tentativas_exercicios")
    item = relationship("ItemExercicio", backref="tentativas")
    capitulo = relationship("Capitulo", backref="tentativas_exercicios")

    __table_args__ = (
        Index("idx_tentativas_usuario_capitulo", "usuario_id", "capitulo_id"),
        Index("idx_tentativas_item", "item_id"),
    )


class CaixaReforco(Base):
    """
    Tabela 13: caixa_reforco
    Armazena os itens nos quais o estudante cometeu erro duplo (esgotou 2 tentativas).
    """
    __tablename__ = "caixa_reforco"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("itens_exercicios.id", ondelete="CASCADE"), nullable=False)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=False)
    total_erros = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default="pendente")  # 'pendente' | 'superado'
    arquivado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    superado_em = Column(DateTime(timezone=True), nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", backref="itens_caixa_reforco")
    item = relationship("ItemExercicio", backref="registros_caixa_reforco")
    capitulo = relationship("Capitulo", backref="itens_caixa_reforco")

    __table_args__ = (
        Index("idx_caixa_reforco_pendente", "usuario_id", "status"),
        Index("idx_caixa_reforco_capitulo", "usuario_id", "capitulo_id"),
    )


class ProvaCat(Base):
    """
    Tabela 14: provas_cat
    Registra as sessões formais de Teste Adaptativo Computadorizado (CAT).
    """
    __tablename__ = "provas_cat"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    disciplina_id = Column(UUID(as_uuid=True), ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False)
    tipo_prova = Column(String(30), nullable=False)  # 'onboarding_diagnostico' | 'marco_periodico'
    theta_geral = Column(Numeric(6, 3), nullable=False, default=0.000)
    erro_padrao_se = Column(Numeric(6, 3), nullable=False, default=1.000)
    scores_grandes_areas = Column(JSONB, nullable=False, default=dict)
    total_itens_aplicados = Column(Integer, nullable=False, default=0)
    itens_respondidos_ids = Column(JSONB, nullable=False, default=list)  # Lista de UUID strings
    respostas_detalhadas = Column(JSONB, nullable=False, default=list)  # Histórico detalhado para reestimação Bayesiana
    iniciado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finalizado_em = Column(DateTime(timezone=True), nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", backref="provas_cat")
    disciplina = relationship("Disciplina", backref="provas_cat")

    __table_args__ = (
        Index("idx_provas_cat_usuario_disciplina", "usuario_id", "disciplina_id"),
    )
