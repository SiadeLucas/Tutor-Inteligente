/**
 * Tipos TypeScript para Conteúdo Didático, Skill Tree e Aulas KaTeX.
 */

export interface Disciplina {
  id: string;
  slug: string;
  nome: string;
  nivel_ensino: string;
  icone: string;
  cor_tema: string;
  ordem: number;
  ativo: boolean;
}

export interface SkillTreeNode {
  id: string;
  volume_id: string;
  numero_capitulo: number;
  titulo: string;
  tempo_estimado_min: number;
  ordem: number;
  status_dominio: "mastered" | "in_progress" | "struggling" | "not_started";
  cor_heatmap: "green" | "yellow" | "red" | "grey";
  percentual_acerto: number;
  desbloqueado: boolean;
}

export interface VolumeComCapitulos {
  id: string;
  numero_volume: number;
  titulo: string;
  grande_area: "algebra_funcoes" | "geometria" | "algebra_linear" | "aplicada";
  ordem_exibicao: number;
  capitulos: SkillTreeNode[];
}

export interface AulaCompleta {
  id: string;
  capitulo_id: string;
  bloco1_teoria_katex: string;
  bloco2_exemplos_katex: string;
  bloco3_dicas_ia: string;
  video_url?: string | null;
  publicado: boolean;
  atualizado_em: string;
  capitulo_titulo?: string;
  numero_capitulo?: number;
  volume_id?: string;
  numero_volume?: number;
  volume_titulo?: string;
}

export interface ConcluirAulaResponse {
  sucesso: boolean;
  concluida: boolean;
  mensagem: string;
  percentual_atingido: number;
  proximo_capitulo_id?: string | null;
}

// Bateria de Fixação server-side (gabarito só chega após submissão)
export interface QuestaoFixacao {
  numero: number;
  enunciado_katex: string;
  alternativas: string[];
}

export interface BateriaFixacao {
  capitulo_id: string;
  questoes: QuestaoFixacao[];
  percentual_minimo: number;
}

export interface SubmeterFixacaoResponse {
  sucesso: boolean;
  percentual_acertos: number;
  percentual_minimo: number;
  concluida: boolean;
  mensagem: string;
  gabarito: Record<string, number>;
  proximo_capitulo_id?: string | null;
}

// Chunk RAG citado pelo tutor (preparação para Etapa 6)
export interface ChunkRAG {
  trecho: string;
  pagina?: number | null;
  teorema_ou_topico?: string | null;
  score_similaridade: number;
}

export interface ChatAulaResponse {
  resposta_katex: string;
  chunks_utilizados: ChunkRAG[];
  nivel_ajuda_socratico: 1 | 2 | 3;
}
