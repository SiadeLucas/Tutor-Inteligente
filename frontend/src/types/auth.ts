export type UserRole = "student" | "teacher" | "admin";

export interface UsuarioAuth {
  id: string;
  nome_completo: string;
  email: string;
  cpf: string;
  role: UserRole;
  avatar_url?: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  expires_in_seconds: number;
  session_id: string;
  usuario: UsuarioAuth;
}

/** Perfil completo para a tela /perfil (RN-INT §2.6). */
export interface MeResponse extends UsuarioAuth {
  telefone: string;
  uf: string;
  cidade: string;
  serie_ano: string;
  escola_tipo: string;
  nome_escola?: string | null;
  data_nascimento?: string | null;
  genero: string;
  eh_menor_idade: boolean;
  dados_responsavel?: {
    nome?: string;
    cpf?: string;
    telefone?: string;
    email?: string;
  } | null;
  criado_em: string;
}

export interface AtualizarPerfilRequest {
  telefone?: string;
  avatar_url?: string;
}

export interface AlterarSenhaRequest {
  senha_atual: string;
  nova_senha: string;
}

export interface ConcurrentSessionError {
  detail: "CONCURRENT_SESSION_REVOKED";
  mensagem: string;
  horario_desconexao: string;
  novo_ip_origem?: string;
}

export interface VerificarTokenResponse {
  valido: boolean;
  email_mascarado?: string | null;
  mensagem: string;
}
