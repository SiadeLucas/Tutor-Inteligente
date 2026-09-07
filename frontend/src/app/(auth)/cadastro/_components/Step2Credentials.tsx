"use client";

import { useState } from "react";
import { AlertCircle, ArrowLeft, ArrowRight, Check, Lock, Mail, Phone, ShieldCheck, X } from "lucide-react";

import { useOnboarding } from "@/contexts/OnboardingContext";
import { api, extrairMensagemErro } from "@/lib/api";
import { apenasDigitos, forcaSenha, mascaraCPF, mascaraTelefone } from "@/lib/formatters";
import { ValidacaoEtapaResponse } from "@/types/onboarding";

const inputCls =
  "w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all";

const CORES_FORCA = ["bg-slate-200 dark:bg-[#3d2f1f]", "bg-rose-500", "bg-amber-500", "bg-lime-500", "bg-green-600"];
const ROTULOS_FORCA = ["", "Fraca", "Razoável", "Boa", "Forte"];

export default function Step2Credentials({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const { form, setCampo, setResponsavel, ehMenorIdade, salvandoRascunho } = useOnboarding();
  const [erro, setErro] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);

  const menor = ehMenorIdade();
  const forca = forcaSenha(form.senha);
  const responsavel = form.dados_responsavel ?? { nome_completo: "", cpf: "", telefone: "", email: "" };

  const validarLocalmente = (): string | null => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) return "Informe um e-mail válido.";
    if (form.senha.length < 8) return "A senha deve conter no mínimo 8 caracteres.";
    if (form.senha !== form.confirmacao_senha) return "As senhas não coincidem.";
    if (apenasDigitos(form.telefone).length < 10) return "Informe um telefone/WhatsApp válido com DDD.";

    if (menor) {
      if (!responsavel.nome_completo || responsavel.nome_completo.trim().length < 3) {
        return "Informe o nome completo do responsável legal.";
      }
      if (apenasDigitos(responsavel.cpf).length !== 11) return "Informe o CPF do responsável legal.";
      if (apenasDigitos(responsavel.telefone).length < 10) {
        return "Informe o telefone do responsável legal.";
      }
    }
    return null;
  };

  const handleAvancar = async () => {
    setErro(null);
    const erroLocal = validarLocalmente();
    if (erroLocal) {
      setErro(erroLocal);
      return;
    }

    setCarregando(true);
    try {
      await api.post<ValidacaoEtapaResponse>("/api/v1/onboarding/validar-etapa-2", {
        email: form.email.trim(),
        senha: form.senha,
        confirmacao_senha: form.confirmacao_senha,
        telefone: form.telefone,
        dados_responsavel: menor
          ? {
              nome_completo: responsavel.nome_completo,
              cpf: responsavel.cpf,
              telefone: responsavel.telefone,
              email: responsavel.email?.trim() ? responsavel.email.trim() : undefined,
            }
          : undefined,
      });
      onNext();
    } catch (err: any) {
      setErro(extrairMensagemErro(err, "Não foi possível validar seus dados. Tente novamente."));
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">Contato & Credenciais</h2>
        <p className="text-xs text-slate-500 dark:text-[#A89F91] mt-1">
          Como você acessará a plataforma e como poderemos falar com você.
        </p>
      </div>

      {erro && (
        <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 text-rose-800 dark:text-rose-300 text-xs flex items-start gap-2.5 leading-relaxed">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
          <span>{erro}</span>
        </div>
      )}

      <div>
        <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          E-mail
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Mail className="w-4 h-4" />
          </div>
          <input
            type="email"
            value={form.email}
            onChange={(e) => setCampo("email", e.target.value)}
            placeholder="aluno@exemplo.com"
            className={inputCls}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Senha
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type="password"
              value={form.senha}
              onChange={(e) => setCampo("senha", e.target.value)}
              placeholder="Mínimo 8 caracteres"
              className={inputCls}
            />
          </div>
        </div>
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Confirmar senha
            </label>
            {form.confirmacao_senha.length > 0 && (
              <span
                className={`text-[11px] font-semibold flex items-center gap-1 ${
                  form.senha === form.confirmacao_senha
                    ? "text-emerald-600 dark:text-emerald-400"
                    : "text-rose-600 dark:text-rose-400"
                }`}
              >
                {form.senha === form.confirmacao_senha ? (
                  <>
                    <Check className="w-3 h-3" />
                    <span>Senhas coincidem</span>
                  </>
                ) : (
                  <>
                    <X className="w-3 h-3" />
                    <span>Não coincidem</span>
                  </>
                )}
              </span>
            )}
          </div>
          <input
            type="password"
            value={form.confirmacao_senha}
            onChange={(e) => setCampo("confirmacao_senha", e.target.value)}
            placeholder="Repita a senha"
            className={`w-full px-3.5 py-2.5 bg-white dark:bg-[#1a1408] border rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 transition-all ${
              form.confirmacao_senha.length > 0
                ? form.senha === form.confirmacao_senha
                  ? "border-emerald-500 focus:ring-emerald-500/20 focus:border-emerald-500"
                  : "border-rose-400 focus:ring-rose-400/20 focus:border-rose-500"
                : "border-slate-300 dark:border-[#3d2f1f] focus:ring-[#F57C00]/20 focus:border-[#F57C00]"
            }`}
          />
        </div>
      </div>

      {/* Indicador de força da senha */}
      <div className="flex items-center gap-2">
        <div className="flex-1 flex gap-1">
          {[1, 2, 3, 4].map((nivel) => (
            <div
              key={nivel}
              className={`h-1 flex-1 rounded-full ${
                forca >= nivel ? CORES_FORCA[forca] : "bg-slate-200 dark:bg-[#3d2f1f]"
              }`}
            />
          ))}
        </div>
        <span className="text-[10px] font-semibold text-slate-500 dark:text-[#A89F91] w-14 text-right">
          {ROTULOS_FORCA[forca]}
        </span>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          Telefone / WhatsApp
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Phone className="w-4 h-4" />
          </div>
          <input
            type="text"
            inputMode="numeric"
            value={form.telefone}
            onChange={(e) => setCampo("telefone", mascaraTelefone(e.target.value))}
            placeholder="(00) 00000-0000"
            className={inputCls}
          />
        </div>
      </div>

      {/* Bloco condicional: responsável legal para menores de 18 anos (RN-ONB-005) */}
      {menor && (
        <div className="border border-[#FFB74D]/40 bg-[#FFF3E0]/60 dark:bg-[#2b1f10]/60 rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-[#E65100] dark:text-[#FFB74D]" />
            <p className="text-xs font-bold text-[#E65100] dark:text-[#FFB74D]">
              Responsável legal (obrigatório para menores de 18 anos)
            </p>
          </div>
          <input
            type="text"
            value={responsavel.nome_completo}
            onChange={(e) => setResponsavel({ nome_completo: e.target.value })}
            placeholder="Nome completo do responsável"
            className="w-full px-3.5 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input
              type="text"
              inputMode="numeric"
              value={responsavel.cpf}
              onChange={(e) => setResponsavel({ cpf: mascaraCPF(e.target.value) })}
              placeholder="CPF do responsável"
              className="w-full px-3.5 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
            />
            <input
              type="text"
              inputMode="numeric"
              value={responsavel.telefone}
              onChange={(e) => setResponsavel({ telefone: mascaraTelefone(e.target.value) })}
              placeholder="Telefone do responsável"
              className="w-full px-3.5 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
            />
          </div>
          <input
            type="email"
            value={responsavel.email ?? ""}
            onChange={(e) => setResponsavel({ email: e.target.value })}
            placeholder="E-mail do responsável (opcional)"
            className="w-full px-3.5 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
          />
        </div>
      )}

      <div className="pt-2 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onBack}
            className="py-3 px-4 rounded-xl border border-slate-300 dark:border-[#3d2f1f] text-slate-600 dark:text-slate-300 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-[#1a1408] transition-colors flex items-center gap-2 cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Voltar</span>
          </button>
          <span className="text-[11px] text-slate-400 dark:text-slate-500">
            {salvandoRascunho ? "Salvando rascunho..." : "Rascunho salvo"}
          </span>
        </div>
        <button
          type="button"
          onClick={handleAvancar}
          disabled={carregando}
          className="py-3 px-5 rounded-xl bg-[#F57C00] hover:bg-[#EF6C00] text-white font-semibold text-sm shadow-sm transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {carregando ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <span>Continuar</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
