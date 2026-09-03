---
title: Autenticação - Schemas e DTOs
type: module
status: draft
related:
  - modules/autenticacao/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs (Pydantic v2 & TypeScript)

Contratos tipados para autenticação híbrida, gerenciamento de tokens e recuperação de senha.

---

## 1. Modelos Backend em Python (`app/modules/auth/schemas.py`)

```python
from __future__ import annotations
import re
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator


# ============================================================================
# 1. Login Híbrido (E-mail ou CPF)
# ============================================================================

class LoginRequest(BaseModel):
    identificador: str = Field(
        ..., 
        description="E-mail válido ou CPF (formatado 000.000.000-00 ou 11 dígitos numéricos)"
    )
    senha: str = Field(..., min_length=8, description="Senha do usuário")

    @field_validator("identificador")
    @classmethod
    def normalizar_identificador(cls, valor: str) -> str:
        valor_limpo = valor.strip()
        # Se for numérico (com ou sem pontuação de CPF), extrai apenas dígitos
        apenas_digitos = re.sub(r"\D", "", valor_limpo)
        if len(apenas_digitos) == 11 and "@" not in valor_limpo:
            return apenas_digitos  # Normaliza para 11 dígitos para busca no banco
        return valor_limpo.lower()  # Normaliza e-mail para minúsculas


class UsuarioAuthResponse(BaseModel):
    id: UUID
    nome_completo: str
    email: EmailStr
    cpf: str
    role: Literal["student", "teacher"]
    avatar_url: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in_seconds: int = Field(900, description="15 minutos (900 segundos)")
    session_id: UUID
    usuario: UsuarioAuthResponse


# ============================================================================
# 2. Heartbeat e Desconexão Concorrente
# ============================================================================

class HeartbeatResponse(BaseModel):
    sessao_ativa: bool = True
    session_id: UUID
    servidor_timestamp: datetime


class ConcurrentSessionRevokedResponse(BaseModel):
    detail: Literal["CONCURRENT_SESSION_REVOKED"] = "CONCURRENT_SESSION_REVOKED"
    mensagem: str = "Sua conta foi conectada em outro dispositivo. Se não foi você, redefina sua senha imediatamente."
    horario_desconexao: str
    novo_ip_origem: Optional[str] = None


# ============================================================================
# 3. Recuperação de Senha por Link Mágico
# ============================================================================

class SolicitarLinkMagicoRequest(BaseModel):
    identificador: str = Field(..., description="E-mail ou CPF cadastrado")


class SolicitarLinkMagicoResponse(BaseModel):
    mensagem: str = "Se o identificador constar em nossa base, um link de redefinição válido por 15 minutos foi enviado."


class RedefinirSenhaRequest(BaseModel):
    token: str = Field(..., description="Token criptográfico de uso único recebido no link mágico")
    nova_senha: str = Field(..., min_length=8, description="Nova senha com no mínimo 8 caracteres")
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/auth.ts`)

```typescript
export type UserRole = "student" | "teacher";

export interface UsuarioAuth {
  id: string;
  nome_completo: string;
  email: string;
  cpf: string;
  role: UserRole;
  avatar_url?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  expires_in_seconds: number;
  session_id: string;
  usuario: UsuarioAuth;
}

export interface ConcurrentSessionError {
  detail: "CONCURRENT_SESSION_REVOKED";
  mensagem: string;
  horario_desconexao: string;
  novo_ip_origem?: string;
}
```
