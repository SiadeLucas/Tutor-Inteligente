"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, LogOut, ShieldCheck, Activity, User } from "lucide-react";
import { api, clearAuth } from "@/lib/api";
import { useHeartbeat } from "@/hooks/useHeartbeat";

export default function MateriasPage() {
  const router = useRouter();
  const [carregandoLogout, setCarregandoLogout] = useState(false);

  // Ativa o heartbeat de sessão única a cada 30 segundos
  useHeartbeat();

  const handleLogout = async () => {
    setCarregandoLogout(true);
    try {
      await api.post("/api/v1/auth/logout");
    } catch {
      // Mesmo com erro de rede, limpa credenciais locais
    } finally {
      clearAuth();
      router.push("/login");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
            TI
          </div>
          <div>
            <h1 className="font-bold text-white text-lg leading-tight">Tutor Inteligente</h1>
            <p className="text-xs text-slate-400">Ambiente do Aluno</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Sessão Ativa (Heartbeat 30s)
          </div>

          <button
            onClick={handleLogout}
            disabled={carregandoLogout}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-medium bg-slate-800 hover:bg-rose-950/40 hover:text-rose-400 hover:border-rose-800/60 border border-slate-700 text-slate-300 transition-all cursor-pointer"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>{carregandoLogout ? "Saindo..." : "Sair"}</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-6 md:p-10">
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-4">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            Etapa 03: Autenticação Validada com Sucesso
          </div>

          <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
            Bem-vindo ao Painel de Matérias! 🎓
          </h2>
          <p className="text-slate-400 text-sm leading-relaxed mb-6">
            Você efetuou login com sucesso no perfil de <strong>Aluno</strong>. Seu token de acesso (JWT) e cookie de refresh estão ativos, e o monitoramento em segundo plano contra sessões simultâneas está funcionando via Redis.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
              <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm mb-1">
                <BookOpen className="w-4 h-4" />
                Matérias
              </div>
              <p className="text-xs text-slate-400">
                O catálogo didático de Matemática do Ensino Médio será implementado na <strong>Etapa 05</strong>.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm mb-1">
                <Activity className="w-4 h-4" />
                Sessão Única
              </div>
              <p className="text-xs text-slate-400">
                Abra uma aba anônima e faça login com este mesmo usuário para testar o modal de derrubada imediata!
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
              <div className="flex items-center gap-2 text-cyan-400 font-semibold text-sm mb-1">
                <User className="w-4 h-4" />
                Onboarding
              </div>
              <p className="text-xs text-slate-400">
                O fluxo de questionário inicial do aluno está previsto para a <strong>Etapa 04</strong>.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
