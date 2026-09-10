/**
 * Tipos TypeScript para o Módulo de Exercícios e Motor CAT.
 * Sincronizado com os Schemas Pydantic v2 do Backend.
 */

export type LetraAlternativa = "A" | "B" | "C" | "D" | "E";

export interface Alternativa {
  letra: LetraAlternativa;
  texto_katex: string;
  correta?: boolean;
}

export interface ItemExercicio {
  id: string;
  capitulo_id: string;
  tipo_origem: "iezzi_original" | "gemea_ia";
  tipo_item: "multiple_choice" | "numeric_input";
  item_matriz_id?: string | null;
  enunciado_katex: string;
  alternativas?: Alternativa[];
  parametro_a: number;
  parametro_b: number;
  parametro_c: number;
  validado_sympy: boolean;
  criado_em?: string;
}

export interface SubmissaoRequest {
  item_id: string;
  capitulo_id: string;
  tentativa_numero: 1 | 2;
  tipo_item: "multiple_choice" | "numeric_input";
  resposta_enviada: string;
  tempo_resposta_segundos: number;
}

export interface SubmissaoResult {
  acertou: boolean;
  pontuacao_obtida: 1.0 | 0.5 | 0.0;
  permite_segunda_chance: boolean;
  pista_socratica_ia?: string | null;
  resolucao_completa_katex?: string | null;
  pode_gerar_gemea: boolean;
  resposta_correta?: string | null;
}

export interface IniciarCatRequest {
  disciplina_id: string;
  tipo_prova: "onboarding_diagnostico" | "marco_periodico";
}

export interface IniciarCatResponse {
  sessao_cat_id: string;
  indicador_progresso: string;
  total_itens_estimado: string;
  primeiro_item: ItemExercicio;
}

export interface SubmeterCatRequest {
  sessao_cat_id: string;
  item_id: string;
  resposta_enviada: string;
  tempo_resposta_segundos: number;
}

export interface CatStatusResponse {
  sessao_id: string;
  finalizado: boolean;
  indicador_progresso: string;
  proximo_item?: ItemExercicio | null;
  theta_final?: number | null;
  erro_padrao?: number | null;
  classificacao?: "Básico" | "Intermediário" | "Avançado" | string | null;
  total_questoes_respondidas?: number | null;
  scores_grandes_areas?: Record<string, number> | null;
  redirecionar_url?: string | null;
  mensagem?: string | null;
}

export interface ItemCaixaReforco {
  id: string;
  item_id: string;
  capitulo_id: string;
  enunciado_katex: string;
  total_erros: number;
  status: "pendente" | "superado";
  arquivado_em: string;
  superado_em?: string | null;
}
