---
title: Tabela 02 - sessoes_ativas
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/autenticacao/business-rules/regras-sessao.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 02: `sessoes_ativas`

Controla a regra de **1 único dispositivo conectado simultaneamente por estudante** (RN-AUT-011 a RN-AUT-015), operando em conjunto com uma arquitetura híbrida de alto desempenho:

1. **Camada Volátil (Redis 7 - `ti-redis`)**: Os heartbeats de 30 segundos (`useHeartbeat.ts`) atualizam a chave volátil `session:{usuario_id}:active` com TTL de 45 segundos. As validações em tempo real ocorrem no Redis em memória (sub-1ms), absorvendo a carga de milhares de conexões sem onerar o PostgreSQL.
2. **Camada de Persistência (PostgreSQL 16 - `sessoes_ativas`)**: Registra a abertura de sessão, dados de auditoria forense (IP e User-Agent) e a revogação de sessões legadas.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE sessoes_ativas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,    -- UUID v4 assinado
    refresh_token_hash VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,               -- Suporta IPv4 e IPv6
    user_agent TEXT NOT NULL,
    ultimo_heartbeat TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revogado BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índice parcial: busca em sub-1ms para sessões ativas do usuário
CREATE INDEX idx_sessoes_ativas_usuario 
ON sessoes_ativas(usuario_id) 
WHERE revogado = FALSE;
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador único da sessão | Gravado no payload do JWT |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Cascata na exclusão da conta |
| `session_token` | VARCHAR(255) | Não | Token de controle de sessão | Único universal |
| `refresh_token_hash` | VARCHAR(255) | Não | Hash do refresh token em cookie | Usado na validação do silent refresh |
| `ultimo_heartbeat` | TIMESTAMPTZ | Não | Estampa atualizada a cada 30 segundos | RN-AUT-012 |
| `revogado` | BOOLEAN | Não | Flag de revogação por concorrência | Se True, dispara erro 401 na API |
