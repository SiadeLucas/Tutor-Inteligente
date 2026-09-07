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
      setErro(err.data?.detail || "Erro ao solicitar redefinição de senha.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600 shadow-xl shadow-indigo-500/25 mb-4 text-white">
            <KeyRound className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Recuperar Acesso</h1>
          <p className="text-sm text-indigo-200/80 mt-1">Enviaremos um link mágico para redefinir sua senha</p>
        </div>

        <div className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
          {sucesso ? (
            <div className="text-center space-y-4">
              <div className="mx-auto w-12 h-12 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-white">Link Solicitado</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                {sucesso.mensagem}
              </p>

              {sucesso.link_dev && (
                <div className="mt-4 p-3 bg-indigo-950/80 border border-indigo-500/40 rounded-xl text-left">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400 block mb-1">
                    Atalho de Desenvolvimento Local:
                  </span>
                  <a
                    href={sucesso.link_dev}
                    className="text-xs text-indigo-300 underline break-all hover:text-indigo-200"
                  >
                    {sucesso.link_dev}
                  </a>
                </div>
              )}

              <div className="pt-4">
                <Link
                  href="/login"
                  className="w-full py-3 px-4 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium text-sm transition-colors inline-flex items-center justify-center gap-2"
                >
                  <ArrowLeft className="w-4 h-4" />
                  Voltar para o Login
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              {erro && (
                <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-400" />
                  <span>{erro}</span>
                </div>
              )}

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  E-mail ou CPF cadastrado
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={identificador}
                    onChange={(e) => setIdentificador(e.target.value)}
                    placeholder="exemplo@email.com ou apenas números do CPF"
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={carregando}
                className="w-full py-3.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm shadow-lg shadow-indigo-600/30 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {carregando ? (
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <span>Enviar Link de Recuperação</span>
                )}
              </button>

              <div className="text-center pt-2">
                <Link
                  href="/login"
                  className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors inline-flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  Voltar para tela de login
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
