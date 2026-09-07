---
title: Painel do Professor - 4. Gestão Financeira
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 4. Gestão Financeira e Controle de Acessos

### 4.1 Regras de Matrícula e Vigência

#### RN-PRF-016: Indicadores de Faturamento
- A aba financeira exibe: Receita Recorrente Mensal (MRR), Total Faturado no mês e no ano, e Distribuição por Método de Pagamento (PIX e Cartão de Crédito).

#### RN-PRF-017: Estados de Acesso do Estudante
- O acesso do aluno à plataforma é controlado automaticamente pelos seguintes status:
  - `active`: Pagamento compensado via PIX ou Cartão; acesso total liberado pelo período de 12 meses.
  - `past_due`: Assinatura recorrente com pagamento pendente/em atraso; período de tolerância de 3 dias antes do bloqueio.
  - `canceled`: Assinatura cancelada ou prazo de 12 meses expirado; acesso aos conteúdos fechado.

#### RN-PRF-018: Acesso Estritamente Vinculado a Pagamento
- Não existe funcionalidade de liberação manual de acessos gratuitos ou concessão de bolsas pelo professor.
- A plataforma opera em modelo 100% comercial e automatizado: o desbloqueio de qualquer capítulo ou volume ocorre única e exclusivamente após a conciliação bancária do pagamento do estudante.

#### RN-PRF-019: Estorno e Cancelamento Administrativo
- O professor pode acionar o cancelamento de uma matrícula e solicitar o estorno formal de uma transação dentro da garantia legal de 7 dias (CDC) diretamente pela interface do painel.

#### RN-PRF-020: Registro e Log de Transações
- Todo evento de pagamento aprovado, compensação de PIX ou solicitação de estorno é auditado com timestamp, valor líquido e ID da transação no extrato financeiro.
