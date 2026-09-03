---
title: Tabela 05 - transacoes_financeiras
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/pagamento/business-rules/regras-gateway.md
  - modules/painel-professor/business-rules/regras-financeiro.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 05: `transacoes_financeiras`

Extrato contábil e financeiro auditável de todas as cobranças emitidas, taxas de intermediação de gateway e conciliação de faturamento do professor.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE transacoes_financeiras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    matricula_id UUID REFERENCES matriculas_pagamentos(id) ON DELETE SET NULL,
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    valor_bruto DECIMAL(10, 2) NOT NULL,
    taxa_gateway DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    valor_liquido DECIMAL(10, 2) NOT NULL,          -- valor_bruto - taxa_gateway
    metodo VARCHAR(20) NOT NULL,                    -- 'pix' | 'credit_card'
    status_transacao VARCHAR(30) NOT NULL,          -- 'paid' | 'waiting_payment' | 'refunded'
    gateway_payload JSONB,                          -- Retorno do webhook (endToEndId, txid)
    pago_em TIMESTAMPTZ,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transacoes_usuario ON transacoes_financeiras(usuario_id);
CREATE INDEX idx_transacoes_status ON transacoes_financeiras(status_transacao);
CREATE INDEX idx_transacoes_data ON transacoes_financeiras(criado_em);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador da transação financeira | UUID v4 |
| `matricula_id` | UUID | Sim | Matrícula gerada por este pagamento | Set Null em estorno |
| `valor_bruto` | DECIMAL(10,2) | Não | Valor nominal pago pelo estudante | Em R$ |
| `taxa_gateway` | DECIMAL(10,2) | Não | Taxa cobrada pelo Asaas/MercadoPago | R$ 0,99 no PIX |
| `valor_liquido` | DECIMAL(10,2) | Não | Valor líquido repassado ao professor | Base do extrato |
| `metodo` | VARCHAR(20) | Não | Meio de pagamento (`pix` ou `credit_card`) | RN-PAG-008 |
| `gateway_payload` | JSONB | Sim | JSON bruto retornado pelo gateway | Auditoria e conciliação |
