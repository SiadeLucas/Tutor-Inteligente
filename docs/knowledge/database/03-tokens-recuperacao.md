---
title: Tabela 03 - tokens_recuperacao_senha
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/autenticacao/business-rules/regras-recuperacao.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 03: `tokens_recuperacao_senha`

Gerencia os tokens temporários de segurança utilizados no fluxo de **Link Mágico** para recuperação de acesso por e-mail.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE tokens_recuperacao_senha (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,       -- Hash SHA-256 do token enviado por e-mail
    expira_em TIMESTAMPTZ NOT NULL,                -- Validade estrita de 15 minutos
    utilizado BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tokens_recuperacao ON tokens_recuperacao_senha(token_hash);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Usuário solicitante |
| `token_hash` | VARCHAR(255) | Não | Hash criptográfico do token de URL | Uso único |
| `expira_em` | TIMESTAMPTZ | Não | Data/hora limite de validade | NOW() + INTERVAL '15 minutes' (RN-AUT-017) |
| `utilizado` | BOOLEAN | Não | Flag de consumo do token | Invalida reutilização (RN-AUT-018) |
