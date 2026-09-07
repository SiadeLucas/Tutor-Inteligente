"""
Modelos ORM para Usuários, Sessões Ativas e Recuperação de Senha.
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    """Modelo de usuário (Estudante ou Professor)."""
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    idade_anos = Column(Integer, nullable=False)
    eh_menor_idade = Column(Boolean, nullable=False, default=False)
    dados_responsavel = Column(JSONB, nullable=True)
    genero = Column(String(20), nullable=False, default="nao_informar", server_default="nao_informar")
    telefone = Column(String(15), nullable=False, default="", server_default="")
    uf = Column(String(2), nullable=False)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=True)
    logradouro = Column(String(200), nullable=True)
    numero = Column(String(20), nullable=True)
    cep = Column(String(8), nullable=False)
    escola_tipo = Column(String(50), nullable=False)
    nome_escola = Column(String(200), nullable=True)
    serie_ano = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False, default="student", index=True)
    avatar_url = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    sessoes = relationship("SessaoAtiva", back_populates="usuario", cascade="all, delete-orphan")
    tokens_recuperacao = relationship("TokenRecuperacaoSenha", back_populates="usuario", cascade="all, delete-orphan")


class SessaoAtiva(Base):
    """Modelo para controle de sessão única por usuário."""
    __tablename__ = "sessoes_ativas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text, nullable=False)
    ultimo_heartbeat = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revogado = Column(Boolean, nullable=False, default=False, index=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="sessoes")


class TokenRecuperacaoSenha(Base):
    """Modelo para tokens de redefinição de senha com link mágico."""
    __tablename__ = "tokens_recuperacao_senha"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expira_em = Column(DateTime(timezone=True), nullable=False)
    utilizado = Column(Boolean, nullable=False, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="tokens_recuperacao")
