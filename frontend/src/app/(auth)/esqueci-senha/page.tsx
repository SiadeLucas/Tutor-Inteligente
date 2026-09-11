"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ArrowLeft, KeyRound, Mail, CheckCircle2, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";

export default function EsqueciSenhaPage() {
  const [identificador, setIdentificador] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [sucesso, setSucesso] = useState<{ mensagem: string; link_dev?: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro(null);
    setCarregando(true);

    try {
      const data = await api.post("/api/v1/auth/solicitar-link-magico", {
        identificador,
      });
      setSucesso(data);
    } catch (err: any) {
      setErro(err.data?.detail || "Erro ao solicitar recuperação de senha.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-md">
        {/* Cabeçalho Institucional */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-subject-500 text-white shadow-sm mb-3">
            <KeyRound className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Recuperar Acesso
          </h1>
          <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
            Enviaremos um link mágico para redefinir sua senha com segurança
          </p>
        </div>

        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-7 sm:p-9 shadow-sm">
          {sucesso ? (
            <div className="text-center space-y-4">
              <div className="mx-auto w-12 h-12 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 rounded-full flex items-center justify-center border border-emerald-200 dark:border-emerald-800/40">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Link de Recuperação Gerado
              </h3>
              <p className="text-xs text-slate-600 dark:text-ink-muted leading-relaxed">
                {sucesso.mensagem}
              </p>

              {sucesso.link_dev && (
                <div className="mt-4 p-3.5 bg-slate-50 dark:bg-surface-bg border border-slate-200 dark:border-line rounded-xl text-left">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 block mb-1">
                    Atalho de Desenvolvimento Local:
                  </span>
                  <a
                    href={sucesso.link_dev}
                    className="text-xs text-subject-700 dark:text-subject-300 underline break-all hover:text-subject-600"
                  >
                    {sucesso.link_dev}
                  </a>
                </div>
              )}

              <div className="pt-3">
                <Link
                  href="/login"
                  className="w-full py-2.5 px-4 rounded-xl border border-slate-200 dark:border-line hover:bg-slate-50 dark:hover:bg-surface-bg text-slate-700 dark:text-slate-200 font-semibold text-xs transition-colors inline-flex items-center justify-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Voltar para o Login</span>
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {erro && (
                <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 text-rose-800 dark:text-rose-300 text-xs flex items-start gap-2.5 leading-relaxed">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
                  <span>{erro}</span>
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                  E-mail ou CPF cadastrado
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    autoComplete="email"
                    value={identificador}
                    onChange={(e) => setIdentificador(e.target.value)}
                    placeholder="exemplo@email.com ou 000.000.000-00"
                    className="w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
                  />
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={carregando}
                  className="w-full py-3 px-4 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  {carregando ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <span>Enviar Link de Recuperação</span>
                  )}
                </button>
              </div>

              <div className="text-center pt-2">
                <Link
                  href="/login"
                  className="text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 transition-colors inline-flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Voltar para tela de login</span>
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
