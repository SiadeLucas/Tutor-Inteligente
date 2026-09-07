"use client";

import React from "react";
import { BookOpen, ShieldCheck, Activity, User, Sparkles, Award } from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { GlobalHeader } from "@/components/header/GlobalHeader";

export default function MateriasPage() {
  // Mantém a sessão única ativa via Redis com heartbeat a cada 30 segundos
  useHeartbeat();

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#1a1408] text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader userRole="student" userName="Aluno" showDisciplineBadge={true} />

      {/* Main Content */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        {/* Banner de Boas-Vindas */}
        <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 sm:p-8 shadow-sm mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] border border-[#FFB74D]/30 mb-4">
            <ShieldCheck className="w-4 h-4 text-[#F57C00]" />
            <span>Etapa 03: Autenticação Validada com Sucesso</span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-2">
            Painel do Estudante 🎓
          </h2>
          <p className="text-slate-600 dark:text-[#A89F91] text-sm leading-relaxed max-w-3xl">
            Sua sessão está devidamente autenticada. O token JWT e o cookie seguro estão ativos no navegador, e a infraestrutura do Redis monitora a unicidade do seu dispositivo em tempo real.
          </p>
        </div>

        {/* Grade de Cards Modulares do Ecossistema */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] flex items-center justify-center mb-4">
                <BookOpen className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Coleção Gelson Iezzi
              </h3>
              <p className="text-xs text-slate-500 dark:text-[#A89F91] leading-relaxed">
                Os 11 volumes de Fundamentos de Matemática Elementar e a Skill Tree de áreas serão estruturados na <strong>Etapa 05</strong>.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-[#382b1c] text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              Próximas Etapas
            </div>
          </div>

          <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4 border border-emerald-100 dark:border-emerald-800/30">
                <Activity className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Sessão Única em Execução
              </h3>
              <p className="text-xs text-slate-500 dark:text-[#A89F91] leading-relaxed">
                O heartbeat silencioso de 30s mantém sua presença confirmada. Caso faça login em outra janela ou dispositivo, a sessão anterior será notificada.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-[#382b1c] text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>Operando Normalmente</span>
            </div>
          </div>

          <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-[#F57C00] flex items-center justify-center mb-4 border border-amber-100 dark:border-amber-800/30">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1.5">
                Onboarding & CAT
              </h3>
              <p className="text-xs text-slate-500 dark:text-[#A89F91] leading-relaxed">
                O questionário de metas e a Prova Adaptativa de Nivelamento baseada em Teoria da Resposta ao Item serão implementados na <strong>Etapa 04</strong>.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-[#382b1c] text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              Planejamento
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
