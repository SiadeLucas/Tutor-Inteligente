---
title: Pagamento - 3. Gateway e Checkout
type: module
status: draft
related:
  - modules/pagamento/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 3. Métodos de Pagamento e Segurança

### 3.1 Checkout Transparente Instantâneo

#### RN-PAG-011: PIX Dinâmico com Webhook Instantâneo
- A cobrança por PIX gera um QR Code e código Copia e Cola exclusivos por transação com expiração configurada para 30 minutos.
- A confirmação de pagamento via webhook bancário deve liberar o acesso do estudante em até 5 segundos.

#### RN-PAG-012: Cartão de Crédito com Parcelamento
- Suporte às principais bandeiras (Visa, Mastercard, Elo, Hipercard, Amex).
- Parcelamento em até 12 vezes para volumes completos e planos anuais.

#### RN-PAG-013: Eliminação de Métodos Lentos no MVP
- Boletos bancários não são ofertados no fluxo principal para evitar fricção e cancelamento por abandono de pagamento.

#### RN-PAG-014: Segurança e Conformidade PCI-DSS
- Dados sensíveis de cartão de crédito nunca trafegam nem são armazenados nos servidores do Tutor Inteligente, sendo tokenizados diretamente no gateway de pagamento.

#### RN-PAG-015: Idempotência de Transações
- Todo webhook e requisição de compra utiliza chaves de idempotência para evitar cobranças duplicadas em caso de instabilidade de rede.
