"use client";

import { useState } from "react";
import { AlertCircle, ArrowRight, CheckCircle2, User } from "lucide-react";

import { useOnboarding } from "@/contexts/OnboardingContext";
import { api, extrairMensagemErro } from "@/lib/api";
import { apenasDigitos, mascaraCPF, validarCPF } from "@/lib/formatters";
import { Genero, ValidacaoEtapaResponse } from "@/types/onboarding";

const inputCls =
  "w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all";

export default function Step1Identity({ onNext }: { onNext: () => void }) {
  const { form, setCampo, calcularIdadeAluno, salvandoRascunho } = useOnboarding();
  const [erro, setErro] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [cpfInvalido, setCpfInvalido] = useState(false);

  const idade = calcularIdadeAluno();

  const validarLocalmente = (): string | null => {
    if (form.nome_completo.trim().length < 3) return "Informe seu nome completo.";
    if (apenasDigitos(form.cpf).length !== 11) return "Informe o CPF completo (11 dígitos).";
    if (!form.data_nascimento) return "Informe sua data de nascimento.";
    const nascimento = new Date(form.data_nascimento + "T00:00:00");
    if (Number.isNaN(nascimento.getTime()) || nascimento >= new Date()) {
      return "A data de nascimento deve ser uma data no passado.";
    }
    if (nascimento.getFullYear() < 1900) {
      return "Data de nascimento inválida (ano mínimo permitido: 1900).";
    }
    const idadeCalculada = calcularIdadeAluno();
    if (idadeCalculada !== null && (idadeCalculada < 6 || idadeCalculada > 120)) {
      return "Idade inválida. O estudante deve ter entre 6 e 120 anos.";
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
      await api.post<ValidacaoEtapaResponse>("/api/v1/onboarding/validar-etapa-1", {
        nome_completo: form.nome_completo,
        cpf: form.cpf,
        data_nascimento: form.data_nascimento,
        genero: form.genero,
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
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">Dados Pessoais</h2>
        <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
          Sua identificação civil na plataforma.
          {idade !== null && (
            <span className="ml-1 font-semibold text-subject-700 dark:text-subject-300">
              ({idade} anos{idade < 18 ? " — dados do responsável serão solicitados na próxima etapa" : ""})
            </span>
          )}
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
          Nome completo
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <User className="w-4 h-4" />
          </div>
          <input
            type="text"
            value={form.nome_completo}
            onChange={(e) => setCampo("nome_completo", e.target.value)}
            placeholder="Nome civil completo"
            className={inputCls}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          CPF
        </label>
        <input
          type="text"
          inputMode="numeric"
          value={form.cpf}
          onChange={(e) => {
            setCampo("cpf", mascaraCPF(e.target.value));
            if (cpfInvalido) setCpfInvalido(false);
          }}
          onBlur={() => {
            const digitos = apenasDigitos(form.cpf);
            setCpfInvalido(digitos.length === 11 && !validarCPF(form.cpf));
          }}
          placeholder="000.000.000-00"
          className={`w-full px-3.5 py-2.5 bg-white dark:bg-surface-bg border rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 transition-all ${
            cpfInvalido
              ? "border-rose-400 focus:ring-rose-400/20 focus:border-rose-500"
              : "border-slate-300 dark:border-line focus:ring-subject-300 focus:border-subject-500"
          }`}
        />
        {cpfInvalido && (
          <p className="mt-1 text-[11px] text-rose-600 dark:text-rose-400 flex items-center gap-1">
            <AlertCircle className="w-3 h-3 shrink-0" />
            Dígitos verificadores do CPF inválidos. Confira os números digitados.
          </p>
        )}
        {!cpfInvalido && apenasDigitos(form.cpf).length === 11 && validarCPF(form.cpf) && (
          <p className="mt-1 text-[11px] text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3 shrink-0" />
            CPF válido.
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Data de nascimento
          </label>
          <input
            type="date"
            value={form.data_nascimento}
            min="1900-01-01"
            max={new Date().toISOString().slice(0, 10)}
            onChange={(e) => setCampo("data_nascimento", e.target.value)}
            className="w-full px-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Gênero
          </label>
          <select
            value={form.genero}
            onChange={(e) => setCampo("genero", e.target.value as Genero)}
            className="w-full px-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
          >
            <option value="masculino">Masculino</option>
            <option value="feminino">Feminino</option>
            <option value="outro">Outro</option>
            <option value="nao_informar">Prefiro não informar</option>
          </select>
        </div>
      </div>

      <div className="pt-2 flex items-center justify-between gap-3">
        <span className="text-[11px] text-slate-400 dark:text-slate-500">
          {salvandoRascunho ? "Salvando rascunho..." : "Rascunho salvo automaticamente"}
        </span>
        <button
          type="button"
          onClick={handleAvancar}
          disabled={carregando}
          className="py-3 px-5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
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
