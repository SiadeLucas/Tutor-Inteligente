"""
Schemas Pydantic v2 para Autenticação, Tokens e Sessões.
"""
from __future__ import annotations
import re
from uuid import UUID
from datetime import datetime, date
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class LoginRequest(BaseModel):
    """Requisição de login com identificador híbrido (E-mail ou CPF) e senha."""
    identificador: str = Field(
        ...,
        description="E-mail válido ou CPF (formatado 000.000.000-00 ou 11 dígitos numéricos)"
    )
    senha: str = Field(..., min_length=8, description="Senha do usuário (mínimo 8 caracteres)")

    @field_validator("identificador")
    @classmethod
    def normalizar_identificador(cls, valor: str) -> str:
        valor_limpo = valor.strip()
        apenas_digitos = re.sub(r"\D", "", valor_limpo)
        if len(apenas_digitos) == 11 and "@" not in valor_limpo:
            return apenas_digitos
        return valor_limpo.lower()


class UsuarioAuthResponse(BaseModel):
    """Dados cadastrais públicos do usuário retornados após login bem-sucedido."""
    id: UUID
    nome_completo: str
    email: EmailStr
    cpf: str
    role: Literal["student", "teacher"]
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MeResponse(UsuarioAuthResponse):
    """Perfil completo para a tela /perfil (RN-INT §2.6)."""
    telefone: str = ""
    uf: str
    cidade: str
    serie_ano: str
    escola_tipo: str
    nome_escola: Optional[str] = None
    data_nascimento: Optional[date] = None
    genero: str = "nao_informato"
    eh_menor_idade: bool = False
    dados_responsavel: Optional[dict] = None
    criado_em: datetime


class LoginResponse(BaseModel):
    """Resposta com Access Token e identificador de sessão ativa."""
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in_seconds: int = Field(900, description="15 minutos (900 segundos)")
    session_id: UUID
    usuario: UsuarioAuthResponse


class HeartbeatResponse(BaseModel):
    """Resposta do pulso de presença do estudante."""
    sessao_ativa: bool = True
    session_id: UUID
    servidor_timestamp: datetime


class ConcurrentSessionRevokedResponse(BaseModel):
    """Payload de erro emitido quando a sessão foi revogada por login concorrente."""
    detail: Literal["CONCURRENT_SESSION_REVOKED"] = "CONCURRENT_SESSION_REVOKED"
    mensagem: str = "Sua conta foi conectada em outro dispositivo. Se não foi você, redefina sua senha imediatamente."
    horario_desconexao: str
    novo_ip_origem: Optional[str] = None


class SolicitarLinkMagicoRequest(BaseModel):
    """Requisição para emissão de link mágico de recuperação de senha."""
    identificador: str = Field(..., description="E-mail ou CPF cadastrado na plataforma")


class SolicitarLinkMagicoResponse(BaseModel):
    """Confirmação de solicitação com mensagem anti-enumeração de contas."""
    mensagem: str = "Se o identificador constar em nossa base, um link de redefinição válido por 15 minutos foi enviado."
    expira_em_minutos: int = 15
    link_dev: Optional[str] = Field(None, description="URL gerada apenas em ambiente de desenvolvimento local")


class VerificarTokenResponse(BaseModel):
    """Verificação prévia da validade do token para liberação do formulário."""
    valido: bool
    email_mascarado: Optional[str] = None
    mensagem: str


class RedefinirSenhaRequest(BaseModel):
    """Requisição final de redefinição de senha com token criptográfico de uso único."""
    token: str = Field(..., description="Token criptográfico de uso único recebido no link mágico")
class AtualizarPerfilRequest(BaseModel):
    """Atualização de dados cadastrais editáveis (RN-INT §2.6)."""
    telefone: Optional[str] = Field(None, min_length=10, max_length=11, description="Somente dígitos, DDD + número")
    avatar_url: Optional[str] = Field(None, max_length=500)


class AlterarSenhaRequest(BaseModel):
    """Troca de senha autenticada (RN-AUT §regras-credenciais)."""
    senha_atual: str = Field(..., min_length=1)
    nova_senha: str = Field(..., min_length=8, description="Nova senha com no mínimo 8 caracteres")
    confirmacao_senha: Optional[str] = Field(None, min_length=8, description="Confirmação idêntica da nova senha")
