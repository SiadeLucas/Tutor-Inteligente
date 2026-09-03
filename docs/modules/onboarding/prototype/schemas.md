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
# 1. Etapa 1: Credenciais Básicas
# ============================================================================

class Etapa1Request(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=200)
    email: EmailStr
    cpf: str = Field(..., description="CPF válido com ou sem pontuação")
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")
    confirmacao_senha: str

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return digitos

    @model_validator(mode="after")
    def verificar_senhas_iguais(self):
        if self.senha != self.confirmacao_senha:
            raise ValueError("A senha e a confirmação de senha não coincidem.")
        return self


# ============================================================================
# 2. Etapa 2: Dados Pessoais e Menoridade Civil
# ============================================================================

class DadosResponsavelSchema(BaseModel):
    nome_completo: str = Field(..., min_length=3)
    cpf: str = Field(..., description="CPF do responsável legal")
    telefone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr


class Etapa2Request(BaseModel):
    data_nascimento: date
    dados_responsavel: Optional[DadosResponsavelSchema] = None

    @model_validator(mode="after")
    def validar_menoridade(self):
        hoje = date.today()
        # Cálculo exato de idade
        idade = hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
        if idade < 18 and not self.dados_responsavel:
            raise ValueError("Estudantes menores de 18 anos exigem o preenchimento dos dados do responsável legal.")
        return self


# ============================================================================
# 3. Etapa 3: Localização e Escola
# ============================================================================

class Etapa3Request(BaseModel):
    cep: str = Field(..., description="CEP com 8 dígitos numéricos")
    cidade: str
    uf: str = Field(..., min_length=2, max_length=2)
    escola_tipo: Literal["publica", "privada", "outro"]
    nome_escola: Optional[str] = None

    @field_validator("cep")
    @classmethod
    def limpar_cep(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 8:
            raise ValueError("O CEP deve conter exatamente 8 dígitos numéricos.")
        return digitos


# ============================================================================
# 4. Etapa 4: Escolaridade e Submissão Unificada
# ============================================================================

class FinalizarCadastroRequest(BaseModel):
    etapa1: Etapa1Request
    etapa2: Etapa2Request
    etapa3: Etapa3Request
    disciplina_id: UUID = Field(..., description="Disciplina de entrada (Matemática no lançamento)")
    serie_ano: Literal["1_ano", "2_ano", "3_ano"] = Field(..., description="Série do Ensino Médio")


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
  // Etapa 1
  nome_completo: string;
  email: string;
  cpf: string;
  senha: string;
  confirmacao_senha: string;
  // Etapa 2
  data_nascimento: string;
  dados_responsavel?: DadosResponsavel;
  // Etapa 3
  cep: string;
  cidade: string;
  uf: string;
  escola_tipo: "publica" | "privada" | "outro";
  nome_escola?: string;
  // Etapa 4
  disciplina_id: string;
  serie_ano: "1_ano" | "2_ano" | "3_ano";
}
```
