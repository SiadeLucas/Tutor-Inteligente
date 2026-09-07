/**
 * Formatadores e máscaras de input do Tutor Inteligente.
 * Bloqueiam letras conforme critérios de aceitação da Etapa 4.
 */

export function apenasDigitos(valor: string): string {
  return valor.replace(/\D/g, "");
}

/** Máscara de CPF: 000.000.000-00 */
export function mascaraCPF(valor: string): string {
  const d = apenasDigitos(valor).slice(0, 11);
  if (d.length <= 3) return d;
  if (d.length <= 6) return `${d.slice(0, 3)}.${d.slice(3)}`;
  if (d.length <= 9) return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6)}`;
  return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6, 9)}-${d.slice(9)}`;
}

/** Máscara de CEP: 00000-000 */
export function mascaraCEP(valor: string): string {
  const d = apenasDigitos(valor).slice(0, 8);
  if (d.length <= 5) return d;
  return `${d.slice(0, 5)}-${d.slice(5)}`;
}

/** Máscara de Telefone/WhatsApp: (00) 00000-0000 */
export function mascaraTelefone(valor: string): string {
  const d = apenasDigitos(valor).slice(0, 11);
  if (d.length === 0) return "";
  if (d.length <= 2) return `(${d}`;
  if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
  if (d.length <= 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
}

/** Idade exata em anos completos (mesma regra do backend: RN-ONB-004). */
export function calcularIdade(dataNascimentoISO: string): number | null {
  if (!dataNascimentoISO) return null;
  const nasc = new Date(dataNascimentoISO + "T00:00:00");
  if (Number.isNaN(nasc.getTime())) return null;
  const hoje = new Date();
  if (nasc > hoje) return null;
  const jaFezAniversario =
    hoje.getMonth() > nasc.getMonth() ||
    (hoje.getMonth() === nasc.getMonth() && hoje.getDate() >= nasc.getDate());
  return hoje.getFullYear() - nasc.getFullYear() - (jaFezAniversario ? 0 : 1);
}

/** Checklist de requisitos de senha exibida em tempo real no cadastro. */
export interface RequisitoSenha {
  rotulo: string;
  cumprido: boolean;
  obrigatorio: boolean;
}

/**
 * Espelho das regras de força da senha. Apenas "Mínimo 8 caracteres" é
 * obrigatório (regra do backend: `senha.min_length=8`); os demais itens
 * são recomendações que elevam o indicador de força.
 */
export function requisitosSenha(senha: string): RequisitoSenha[] {
  return [
    { rotulo: "Mínimo 8 caracteres", cumprido: senha.length >= 8, obrigatorio: true },
    { rotulo: "Letra maiúscula e minúscula", cumprido: /[a-z]/.test(senha) && /[A-Z]/.test(senha), obrigatorio: false },
    { rotulo: "Ao menos um número", cumprido: /\d/.test(senha), obrigatorio: false },
    { rotulo: "Ao menos um símbolo", cumprido: /[^A-Za-z0-9]/.test(senha), obrigatorio: false },
  ];
}

/**
 * Validação dos dígitos verificadores do CPF (Módulo 11).
 * Espelho fiel do backend: backend/app/core/validators.py (CPFValidator.validar).
 */
export function validarCPF(valor: string): boolean {
  const d = apenasDigitos(valor);
  if (d.length !== 11) return false;
  if (d === d[0].repeat(11)) return false; // sequências repetidas (ex: 111.111.111-11)

  const soma1 = d.slice(0, 9).split("").reduce((acc, dig, i) => acc + Number(dig) * (10 - i), 0);
  const resto1 = (soma1 * 10) % 11;
  const dv1 = resto1 === 10 ? 0 : resto1;
  if (Number(d[9]) !== dv1) return false;

  const soma2 = d.slice(0, 10).split("").reduce((acc, dig, i) => acc + Number(dig) * (11 - i), 0);
  const resto2 = (soma2 * 10) % 11;
  const dv2 = resto2 === 10 ? 0 : resto2;
  return Number(d[10]) === dv2;
}

/** Indicador de força da senha (0 a 4). */
export function forcaSenha(senha: string): number {
  if (!senha) return 0;
  let forca = 0;
  if (senha.length >= 8) forca++;
  if (/[a-z]/.test(senha) && /[A-Z]/.test(senha)) forca++;
  if (/\d/.test(senha)) forca++;
  if (/[^A-Za-z0-9]/.test(senha)) forca++;
  return forca;
}
