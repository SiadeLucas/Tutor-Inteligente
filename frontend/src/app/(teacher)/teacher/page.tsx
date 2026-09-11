"use client";

import React from "react";
import { GraduationCap, ShieldCheck, Activity, Users, BookMarked } from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";

export default function TeacherDashboardPage() {
  // Mantém a presença do professor ativa via Redis
  useHeartbeat();

  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">

      {/* Main Content */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 sm:p-8 shadow-sm mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200 mb-4">
            <ShieldCheck className="w-4 h-4 text-subject-600" />
            <span>Etapa 03: Autenticação de Docente Concluída</span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-2">
            Painel do Professor
          </h2>
          <p className="text-slate-600 dark:text-ink-muted text-sm leading-relaxed max-w-3xl">
            Acesso autorizado com perfil de <strong>Professor/Administrador</strong>. As regras de autenticação, expiração e auditoria foram confirmadas com sucesso.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 flex items-center justify-center mb-4">
                <Users className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Acompanhamento de Alunos
              </h3>
              <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
                Métricas agregadas por região, instituição e faixas de proficiência TRI serão implementadas na <strong>Etapa 10</strong>.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-line text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              Painel Avançado
            </div>
          </div>

          <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4 border border-emerald-100 dark:border-emerald-800/30">
                <Activity className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Sessão Segura Ativa
              </h3>
              <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
                O heartbeat mantém a sessão do docente sincronizada com o Redis, bloqueando logins concorrentes indevidos.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-line text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>Conectado</span>
            </div>
          </div>

          <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4 border border-blue-100 dark:border-blue-800/30">
                <BookMarked className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Curadoria de Conteúdo
              </h3>
              <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
                Revisão de itens paramétricos, validação simbólica via SymPy e supervisão dos 11 volumes didáticos.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-line text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              Planejamento
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
