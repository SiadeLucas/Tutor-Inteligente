/**
 * Tipos e DTOs TypeScript do Módulo de Progresso & Analytics.
 * Em conformidade com docs-site/docs/modules/progresso/prototype/schemas.md.
 */

export type StatusCorHeatmap = "cinza" | "vermelho" | "amarelo" | "verde";

export interface RadarAreaItem {
  area: string;
  slug_area: string;
  score_entrada_cat: number;
  score_atual: number;
}

export interface TimelineThetaItem {
  data: string;
  theta_estimado: number;
  origem_ajuste: string;
}

export interface ProgressoGeralResponse {
  usuario_id: string;
  theta_atual: number;
  erro_padrao_se: number;
  classificacao_nivel: "Básico" | "Intermediário" | "Avançado";
  completude_global_percentual: number;
  horas_estudo_liquidas_total: number;
  aulas_concluidas_count: number;
  streak_dias_consecutivos: number;
  radar_areas: RadarAreaItem[];
  timeline: TimelineThetaItem[];
}

export interface HeatmapCapituloItem {
  capitulo_id: string;
  numero_capitulo: number;
  titulo: string;
  taxa_acertos_ponderada: number;
  status_cor: StatusCorHeatmap;
  total_exercicios_respondidos: number;
  aula_concluida: boolean;
}

export interface HeatmapVolumeResponse {
  volume_id: string;
  numero_volume: number;
  titulo_volume: string;
  grande_area: string;
  completude_volume_percentual: number;
  capitulos: HeatmapCapituloItem[];
}

export interface VolumeResumoItem {
  volume_id: string;
  numero_volume: number;
  titulo_volume: string;
  grande_area: string;
  completude_percentual: number;
  total_capitulos: number;
  capitulos_concluidos: number;
}

export interface TopCriticoItem {
  capitulo_id: string;
  titulo_capitulo: string;
  numero_volume: number;
  titulo_volume: string;
  taxa_acerto_ponderada: number;
  total_erros_na_caixa_reforco: number;
  acao_revisar_teoria_url: string;
  acao_praticar_reforco_url: string;
}

export interface HubAcaoTop3Response {
  top_criticos: TopCriticoItem[];
  tem_pendencias_criticas: boolean;
}
