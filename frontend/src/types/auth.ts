export type UserRole = "student" | "teacher";

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
