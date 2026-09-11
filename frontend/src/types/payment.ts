export type TipoProduto = "capitulo_50min" | "volume_iezzi" | "passe_global";

/** Alias para fluxos de compra de volume completo / passe global (com abatimento RN-PAG-005). */
export type TipoProdutoPasse = Extract<TipoProduto, "volume_iezzi" | "passe_global">;

/** Alias para fluxos de compra de capítulo avulso (R$ 9,90). */
export type TipoProdutoCapitulo = Extract<TipoProduto, "capitulo_50min">;

export interface CalcularUpgradeResponse {
  volume_id: string;
  preco_original: number;
  total_abatimento: number;
  valor_final: number;
  capitulos_abatidos_count: number;
  gratis_por_upgrade: boolean;
}

export interface CheckoutPixResponse {
  cobranca_id: string;
  valor: number;
  pix_copia_e_cola: string;
  pix_qrcode_base64: string;
  expira_em: string;
  gratis_por_upgrade: boolean;
  matricula_id?: string;
}

export interface CheckoutCartaoResponse {
  cobranca_id: string;
  status: string;
  valor: number;
  pago: boolean;
  matricula_id?: string;
  gratis_por_upgrade: boolean;
}

export interface StatusCobrancaResponse {
  cobranca_id: string;
  status: string;
  pago: boolean;
  matricula_id?: string;
}

export interface MatriculaProduto {
  id: string;
  tipo_produto: string;
  referencia_produto_id?: string | null;
  titulo_produto: string;
  data_inicio: string;
  data_expiracao: string;
  dias_restantes: number;
  status: string;
  valor_pago: number;
}
