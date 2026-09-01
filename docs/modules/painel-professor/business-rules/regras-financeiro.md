---
title: Painel do Professor - 4. Gestão Financeira
type: module
status: draft
related:
  - modules/painel-professor/business-rules/index.md
last_updated: "2026-09-01"
updated_by: claude
---

# 4. Gestão Financeira e Controle de Acessos

### 4.1 Regras de Matrícula e Vigência

#### RN-PRF-016: Indicadores de Faturamento
- A aba financeira exibe: Receita Recorrente Mensal (MRR), Total Faturado no mês e no ano, e Distribuição por Método de Pagamento (PIX, Cartão e Boleto).

#### RN-PRF-017: Estados de Acesso do Estudante
- O acesso do aluno à plataforma é controlado pelos seguintes status:
  - `active`: Pagamento compensado ou bolsa ativa; acesso total liberado.
  - `past_due`: Pagamento pendente/em atraso; período de carência de 3 dias antes do bloqueio.
  - `canceled`: Assinatura encerrada; acesso bloqueado aos conteúdos pagos.
  - `scholarship`: Acesso gratuito concedido manualmente pelo professor.

#### RN-PRF-018: Concessão Manual de Bolsas de Estudo
- O professor pode cadastrar alunos bolsistas informando e-mail e CPF, liberando acesso integral com status `scholarship` sem exigência de cartão ou pagamento.

#### RN-PRF-019: Estorno e Cancelamento Manual
- O professor tem autonomia para cancelar uma matrícula e solicitar o estorno de transações diretamente pelo painel.

#### RN-PRF-020: Registro e Log de Transações
- Todo evento de pagamento, compensação de PIX ou alteração manual de acesso é auditado com timestamp, valor e ID do operador no extrato financeiro.
