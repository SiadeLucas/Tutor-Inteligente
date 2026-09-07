"""
Schemas Pydantic v2 do Onboarding (wizard de 3 etapas).
Especificação canônica: docs-site/docs/modules/onboarding/prototype/schemas.md
"""
from __future__ import annotations

import re
from datetime import date
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# ============================================================================
# 1. Etapa 1: Dados Pessoais
# ============================================================================

class Etapa1Request(BaseModel):
    """Dados de identificação civil do aluno (inclui gênero e foto opcional)."""
    nome_completo: str = Field(..., min_length=3, max_length=200, description="Nome completo do aluno")
    cpf: str = Field(..., description="CPF válido do aluno com ou sem pontuação")
    data_nascimento: date = Field(..., description="Data de nascimento para cálculo de idade")
    genero: Literal["masculino", "feminino", "outro", "nao_informar"] = "nao_informar"
    foto_perfil: Optional[str] = Field(None, description="URL ou Base64 da foto do perfil (máx 5MB)")

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return digitos

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: date) -> date:
        hoje = date.today()
        if v >= hoje:
            raise ValueError("A data de nascimento deve ser uma data no passado.")
        idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
        if idade < 6:
            raise ValueError("O estudante deve ter no mínimo 6 anos de idade.")
        if idade > 120:
            raise ValueError("Data de nascimento inválida. A idade máxima permitida é de 120 anos.")
        return v

    @property
    def idade_anos(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def eh_menor_idade(self) -> bool:
        return self.idade_anos < 18


# ============================================================================
# 2. Etapa 2: Contato, Credenciais e Responsável Legal
# ============================================================================

class DadosResponsavelSchema(BaseModel):
    """Bloco condicional obrigatório para menores de 18 anos (RN-ONB-005)."""
    nome_completo: str = Field(..., min_length=3, description="Nome do responsável legal")
    cpf: str = Field(..., description="CPF do responsável legal")
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone/WhatsApp do responsável")
    email: Optional[EmailStr] = Field(None, description="E-mail do responsável legal (opcional)")

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf_resp(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF do responsável deve conter exatamente 11 dígitos numéricos.")
        return digitos


class Etapa2Request(BaseModel):
    """Contato e credenciais de acesso (telefone/WhatsApp obrigatório)."""
    email: EmailStr = Field(..., description="E-mail principal para login (armazenado em minúsculas)")
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")
    confirmacao_senha: str = Field(..., description="Confirmação idêntica da senha")
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone/WhatsApp do aluno (obrigatório)")
    dados_responsavel: Optional[DadosResponsavelSchema] = None

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        return v.strip().lower()

    @model_validator(mode="after")
    def verificar_senhas_iguais(self):
        if self.senha != self.confirmacao_senha:
            raise ValueError("A senha e a confirmação de senha não coincidem.")
        return self


# ============================================================================
# 3. Etapa 3: Acadêmico e Endereço
# ============================================================================

class Etapa3Request(BaseModel):
    """Endereço (auto-preenchido pelo ViaCEP) e dados escolares."""
    cep: str = Field(..., description="CEP com 8 dígitos numéricos")
    uf: str = Field(..., min_length=2, max_length=2, description="Unidade federativa (ex: SP)")
    cidade: str = Field(..., min_length=2, description="Município de residência")
    bairro: Optional[str] = None
    logradouro: Optional[str] = Field(None, description="Auto-preenchido pelo ViaCEP, editável")
    numero: Optional[str] = Field(None, description="Número do endereço (preenchimento manual)")
    escola_tipo: Literal["publica", "privada", "outro"]
    nome_escola: Optional[str] = Field(None, description="Nome da instituição de ensino")
    serie_ano: str = Field(..., min_length=1, description="Série dinâmica (ex: 1_ano, 2_ano, 3_ano, 9_ano, pre_vestibular)")

    @field_validator("cep")
    @classmethod
    def limpar_cep(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 8:
            raise ValueError("O CEP deve conter exatamente 8 dígitos numéricos.")
        return digitos

    @field_validator("uf")
    @classmethod
    def normalizar_uf(cls, v: str) -> str:
        return v.strip().upper()


# ============================================================================
# 4. Submissão Unificada (Atômica)
# ============================================================================

class FinalizarCadastroRequest(BaseModel):
    """Consolidação atômica das 3 etapas do wizard (sem inicialização de CAT)."""
    etapa1: Etapa1Request
    etapa2: Etapa2Request
    etapa3: Etapa3Request

    @model_validator(mode="before")
    @classmethod
    def suportar_payload_plano_ou_aninhado(cls, data: Any) -> Any:
        if isinstance(data, dict) and "etapa1" not in data and "cpf" in data:
            return {
                "etapa1": {
                    "nome_completo": data.get("nome_completo"),
                    "cpf": data.get("cpf"),
                    "data_nascimento": data.get("data_nascimento"),
                    "genero": data.get("genero", "nao_informar"),
                    "foto_perfil": data.get("foto_perfil"),
                },
                "etapa2": {
                    "email": data.get("email"),
                    "senha": data.get("senha"),
                    "confirmacao_senha": data.get("confirmacao_senha"),
                    "telefone": data.get("telefone"),
                    "dados_responsavel": data.get("dados_responsavel"),
                },
                "etapa3": {
                    "cep": data.get("cep"),
                    "uf": data.get("uf"),
                    "cidade": data.get("cidade"),
                    "bairro": data.get("bairro"),
                    "logradouro": data.get("logradouro"),
                    "numero": data.get("numero"),
                    "escola_tipo": data.get("escola_tipo"),
                    "nome_escola": data.get("nome_escola"),
                    "serie_ano": data.get("serie_ano"),
                },
            }
        return data

    @model_validator(mode="after")
    def validar_responsavel_se_menor(self):
        if self.etapa1.eh_menor_idade and not self.etapa2.dados_responsavel:
            raise ValueError(
                "Estudantes menores de 18 anos exigem obrigatoriamente os dados do responsável legal na Etapa 2."
            )
        return self


class CadastroConcluidoResponse(BaseModel):
    """
    Resposta pública do cadastro concluído.
    O refresh token NUNCA retorna no corpo: é injetado em cookie HTTP-Only (padrão da Etapa 3).
    """
    usuario_id: UUID
    nome_completo: str
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in_seconds: int = Field(900, description="15 minutos (900 segundos)")
    sessao_id: UUID
    mensagem: str = "Cadastro realizado com sucesso! Redirecionando para o dashboard de matérias."
