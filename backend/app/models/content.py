"""
Modelos ORM para Conteúdo Didático: Disciplinas, Volumes Didáticos, Capítulos, Aulas e Documentos RAG.
Conforme especificações em docs-site/docs/knowledge/database/ (Tabelas 06 a 10).
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
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base


class Disciplina(Base):
    """Tabela 06: disciplinas - Suporte a múltiplas disciplinas e níveis de ensino."""
    __tablename__ = "disciplinas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    nivel_ensino = Column(String(50), nullable=False)  # 'ensino_medio' | 'fundamental' | 'superior'
    icone = Column(String(50), nullable=False, default="school")
    cor_tema = Column(String(20), nullable=False, default="#F57C00")
    ordem = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    volumes = relationship("VolumeDidatico", back_populates="disciplina", cascade="all, delete-orphan", order_by="VolumeDidatico.ordem_exibicao")


class VolumeDidatico(Base):
    """Tabela 07: volumes_didaticos - 11 volumes canônicos da coleção Iezzi."""
    __tablename__ = "volumes_didaticos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    disciplina_id = Column(UUID(as_uuid=True), ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    nome_colecao = Column(String(150), nullable=False)  # 'Fundamentos de Matemática Elementar - Gelson Iezzi'
    numero_volume = Column(Integer, nullable=False)      # 1 a 11
    titulo = Column(String(150), nullable=False)        # Ex: 'Conjuntos e Funções'
    grande_area = Column(String(50), nullable=False)    # 'algebra_funcoes' | 'geometria' | 'algebra_linear' | 'aplicada'
    ordem_exibicao = Column(Integer, nullable=False)
    preco_padrao = Column(Numeric(10, 2), nullable=False, default=49.90)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("disciplina_id", "numero_volume", name="uk_volume_disciplina_numero"),
        Index("idx_volumes_disciplina", "disciplina_id", "ordem_exibicao"),
    )

    # Relacionamentos
    disciplina = relationship("Disciplina", back_populates="volumes")
    capitulos = relationship("Capitulo", back_populates="volume", cascade="all, delete-orphan", order_by="Capitulo.ordem")
    documentos_rag = relationship("DocumentoVetorialRAG", back_populates="volume", cascade="all, delete-orphan")


class Capitulo(Base):
    """Tabela 08: capitulos - Unidades pedagógicas de 50 minutos."""
    __tablename__ = "capitulos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volume_id = Column(UUID(as_uuid=True), ForeignKey("volumes_didaticos.id", ondelete="CASCADE"), nullable=False, index=True)
    numero_capitulo = Column(Integer, nullable=False)
    titulo = Column(String(200), nullable=False)
    tempo_estimado_min = Column(Integer, nullable=False, default=50)
    preco_avulso = Column(Numeric(10, 2), nullable=False, default=9.90)
    pre_requisitos_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, default=list)
    ordem = Column(Integer, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_capitulos_volume", "volume_id", "ordem"),
    )

    # Relacionamentos
    volume = relationship("VolumeDidatico", back_populates="capitulos")
    aula = relationship("Aula", back_populates="capitulo", uselist=False, cascade="all, delete-orphan")


class Aula(Base):
    """Tabela 09: aulas - Material instrucional em 4 blocos com fórmulas KaTeX."""
    __tablename__ = "aulas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), unique=True, nullable=False)
    bloco1_teoria_katex = Column(Text, nullable=False)
    bloco2_exemplos_katex = Column(Text, nullable=False)
    bloco3_dicas_ia = Column(Text, nullable=False)
    video_url = Column(Text, nullable=True)
    publicado = Column(Boolean, nullable=False, default=True)
    atualizado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    capitulo = relationship("Capitulo", back_populates="aula")
    curador = relationship("Usuario")


class DocumentoVetorialRAG(Base):
    """Tabela 10: documentos_vetoriais_rag - Base vetorial 768d para busca semântica."""
    __tablename__ = "documentos_vetoriais_rag"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volume_id = Column(UUID(as_uuid=True), ForeignKey("volumes_didaticos.id", ondelete="CASCADE"), nullable=False, index=True)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=True, index=True)
    trecho_conteudo = Column(Text, nullable=False)
    metadados = Column(JSONB, nullable=False, default=dict)
    embedding = Column(Vector(768), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_rag_volume", "volume_id"),
    )

    # Relacionamentos
    volume = relationship("VolumeDidatico", back_populates="documentos_rag")
    capitulo = relationship("Capitulo")
