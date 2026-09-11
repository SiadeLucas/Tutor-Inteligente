/**
 * Tipos de compras e cobranças do usuário (Etapa 9).
 * Consumidos pela página /cobranca (fatura + histórico) e pelo painel de produtos.
 */

import { MatriculaProduto } from "./payment";

/** Status canônico da transação financeira (status_transacao no backend). */
export type StatusTransacao = "paid" | "waiting_payment" | "refunded";

/** Status canônico da matrícula comercial (matriculas_pagamentos.status). */
export type StatusMatricula = "active" | "past_due" | "canceled";

/** Um produto adquirido (capítulo, volume ou passe global) com vigência. */
export type ProdutoAdquirido = MatriculaProduto;

/** Histórico simplificado de transações do usuário. */
export interface TransacaoResumo {
  id: string;
  gateway_transacao_id: string;
  metodo: "pix" | "credit_card" | "upgrade_gratis";
  status_transacao: StatusTransacao;
  valor_bruto: number;
  taxa_gateway: number;
  valor_liquido: number;
  pago_em: string | null;
  criado_em: string;
}
