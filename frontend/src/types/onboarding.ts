/**
 * Tipos do Onboarding (wizard de cadastro em 3 etapas).
 * Espelho dos schemas Pydantic: backend/app/modules/onboarding/schemas.py
 * Referência: docs-site/docs/modules/onboarding/prototype/schemas.md
 */

export type Genero = "masculino" | "feminino" | "outro" | "nao_informar";
export type EscolaTipo = "publica" | "privada" | "outro";

export interface DadosResponsavel {
  nome_completo: string;
  cpf: string;
  telefone: string;
  email?: string;
}

export interface OnboardingFormState {
  // Etapa 1: Dados Pessoais
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  genero: Genero;
  foto_perfil?: string;

  // Etapa 2: Contato e Credenciais
  email: string;
  senha: string;
  confirmacao_senha: string;
  telefone: string;
  dados_responsavel?: DadosResponsavel;

  // Etapa 3: Acadêmico e Endereço
  cep: string;
  uf: string;
  cidade: string;
  bairro?: string;
  logradouro?: string;
  numero?: string;
  escola_tipo: EscolaTipo;
  nome_escola?: string;
  serie_ano: string;
}

export const ONBOARDING_FORM_INICIAL: OnboardingFormState = {
  nome_completo: "",
  cpf: "",
  data_nascimento: "",
  genero: "nao_informar",
  email: "",
  senha: "",
  confirmacao_senha: "",
  telefone: "",
  cep: "",
  uf: "",
  cidade: "",
  bairro: "",
  logradouro: "",
  numero: "",
  escola_tipo: "publica",
  nome_escola: "",
  serie_ano: "",
};

// ---------------------------------------------------------------------------
// Respostas da API (/api/v1/onboarding)
// ---------------------------------------------------------------------------

export interface ValidacaoEtapaResponse {
  valido: boolean;
  idade_anos?: number;
  eh_menor_idade?: boolean;
  mensagem: string;
}

export interface DraftSessionResponse {
  draft_session_id: string;
  dados_parciais: Partial<OnboardingFormState>;
  expira_em_segundos?: number;
  timestamp?: string;
}

export interface ViaCepResponse {
  cep: string;
  cidade: string | null;
  uf: string | null;
  bairro: string | null;
  logradouro: string | null;
}

export interface CadastroConcluidoResponse {
  usuario_id: string;
  nome_completo: string;
  access_token: string;
  token_type: "bearer";
  expires_in_seconds: number;
  sessao_id: string;
  mensagem: string;
}
