---
title: Onboarding - Schemas e DTOs do Wizard
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs do Wizard (Pydantic v2 & TypeScript)

Contratos tipados para cada etapa do formulário de cadastro, validação condicional de menoridade civil e submissão atômica unificada.

---

## 1. Modelos Backend em Python (`app/modules/onboarding/schemas.py`)

```python
from __future__ import annotations
import re
from uuid import UUID
from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


# ============================================================================
# 1. Etapa 1: Dados Pessoais
# ============================================================================

class Etapa1Request(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=200, description="Nome completo do aluno")
    cpf: str = Field(..., description="CPF válido do aluno com ou sem pontuação")
    data_nascimento: date = Field(..., description="Data de nascimento para cálculo de idade")
    genero: Optional[Literal["masculino", "feminino", "outro", "nao_informar"]] = "nao_informar"
    foto_perfil: Optional[str] = Field(None, description="URL ou Base64 da foto do perfil (máx 5MB)")

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return digitos

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
# 2. Etapa 2: Contato, Endereço e Credenciais de Acesso
# ============================================================================

class DadosResponsavelSchema(BaseModel):
    nome_completo: str = Field(..., min_length=3, description="Nome do responsável legal")
    cpf: str = Field(..., description="CPF do responsável legal")
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone/WhatsApp do responsável")
    email: EmailStr = Field(..., description="E-mail do responsável legal")

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf_resp(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF do responsável deve conter exatamente 11 dígitos numéricos.")
        return digitos


class Etapa2Request(BaseModel):
    email: EmailStr = Field(..., description="E-mail principal para login e comunicações")
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")
    confirmacao_senha: str = Field(...)
    telefone: str = Field(..., min_length=10, max_length=15, description="WhatsApp do aluno")
    cep: str = Field(..., description="CEP com 8 dígitos numéricos")
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: str = Field(...)
    uf: str = Field(..., min_length=2, max_length=2)
    dados_responsavel: Optional[DadosResponsavelSchema] = None

    @field_validator("cep")
    @classmethod
    def limpar_cep(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 8:
            raise ValueError("O CEP deve conter exatamente 8 dígitos numéricos.")
        return digitos

    @model_validator(mode="after")
    def verificar_senhas_iguais(self):
        if self.senha != self.confirmacao_senha:
            raise ValueError("A senha e a confirmação de senha não coincidem.")
        return self


# ============================================================================
# 3. Etapa 3: Dados Acadêmicos e Escolaridade
# ============================================================================

class Etapa3Request(BaseModel):
    nivel_ensino_id: Optional[UUID] = Field(None, description="Identificador do nível de ensino")
    escola_tipo: Literal["publica", "privada", "outro"]
    nome_escola: Optional[str] = Field(None, description="Nome da instituição de ensino")
    serie_ano: str = Field(..., description="Série cadastrada de forma dinâmica (ex: 1_ano, 2_ano, 3_ano, 9_ano, pre_vestibular)")


# ============================================================================
# 4. Submissão Unificada
# ============================================================================

class FinalizarCadastroRequest(BaseModel):
    etapa1: Etapa1Request
    etapa2: Etapa2Request
    etapa3: Etapa3Request
    disciplina_id: UUID = Field(..., description="Disciplina de entrada (Matemática no lançamento)")

    @model_validator(mode="after")
    def validar_responsavel_se_menor(self):
        if self.etapa1.eh_menor_idade and not self.etapa2.dados_responsavel:
            raise ValueError("Estudantes menores de 18 anos exigem obrigatoriamente os dados do responsável legal na Etapa 2.")
        return self


class CadastroConcluidoResponse(BaseModel):
    usuario_id: UUID
    nome_completo: str
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    sessao_id: UUID
    sessao_cat_id: UUID = Field(..., description="ID da sessão da Prova Adaptativa Diagnóstica já inicializada")
    mensagem: str = "Cadastro realizado com sucesso! Redirecionando para a Prova Diagnóstica."
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/onboarding.ts`)

```typescript
export interface DadosResponsavel {
  nome_completo: string;
  cpf: string;
  telefone: string;
  email: string;
}

export interface OnboardingFormState {
  // Etapa 1: Dados Pessoais
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  genero?: "masculino" | "feminino" | "outro" | "nao_informar";
  foto_perfil?: string;

  // Etapa 2: Contato, Endereço e Credenciais
  email: string;
  senha: string;
  confirmacao_senha: string;
  telefone: string;
  cep: string;
  logradouro?: string;
  numero?: string;
  complemento?: string;
  bairro?: string;
  cidade: string;
  uf: string;
  dados_responsavel?: DadosResponsavel;

  // Etapa 3: Acadêmico
  nivel_ensino_id?: string;
  escola_tipo: "publica" | "privada" | "outro";
  nome_escola?: string;
  serie_ano: string; // Dinâmico (ex: "1_ano", "2_ano", "3_ano", "pre_vestibular")

  // Contexto da Disciplina
  disciplina_id: string;
}
```
