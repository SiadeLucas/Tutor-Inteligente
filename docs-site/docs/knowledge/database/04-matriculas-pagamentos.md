---
title: Tabela 04 - matriculas_pagamentos
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/pagamento/business-rules/regras-produtos.md
  - modules/pagamento/business-rules/regras-vigencia.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 04: `matriculas_pagamentos`

Controla o direito comercial de acesso aos conteúdos da plataforma, registrando os produtos adquiridos e a vigência de 12 meses (365 dias).

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE matriculas_pagamentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo_produto VARCHAR(30) NOT NULL,             -- 'capitulo_50min' | 'volume_iezzi' | 'passe_global'
    referencia_produto_id UUID,                    -- capitulo_id OU volume_id (NULL se passe_global)
    data_inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_expiracao TIMESTAMPTZ NOT NULL,           -- data_inicio + 365 dias (RN-PAG-006)
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- 'active' | 'past_due' | 'canceled'
    valor_pago DECIMAL(10, 2) NOT NULL,            -- Valor efetivamente cobrado
    metodo_pagamento VARCHAR(20) NOT NULL,         -- 'pix' | 'credit_card'
    transacao_gateway_id VARCHAR(100),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_matriculas_usuario_status 
ON matriculas_pagamentos(usuario_id, status);

CREATE INDEX idx_matriculas_produto 
ON matriculas_pagamentos(tipo_produto, referencia_produto_id);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador da matrícula | UUID v4 |
| `usuario_id` | UUID | Não | Chave estrangeira para `usuarios(id)` | Aluno comprador |
| `tipo_produto` | VARCHAR(30) | Não | Escopo do produto adquirido | RN-PAG-001 |
| `referencia_produto_id` | UUID | Sim | ID do capítulo ou volume didático | NULL se `passe_global` |
| `data_inicio` | TIMESTAMPTZ | Não | Momento da ativação da matrícula | NOW() |
| `data_expiracao` | TIMESTAMPTZ | Não | Prazo final de acesso | 365 dias corridos (RN-PAG-006) |
| `status` | VARCHAR(20) | Não | Situação contratual do acesso | `active`, `past_due`, `canceled` |
| `valor_pago` | DECIMAL(10,2) | Não | Preço final pago (usado no abatimento) | RN-PAG-005 |
| `metodo_pagamento` | VARCHAR(20) | Não | Meio utilizado para liquidação | `pix` ou `credit_card` |
| `transacao_gateway_id` | VARCHAR(100) | Sim | ID da cobrança ou autorização no Asaas | Conciliação contábil |
| `criado_em` | TIMESTAMPTZ | Não | Carimbo temporal do registro | Auditoria |

