"use client";

import React from "react";
import Link from "next/link";
import { TopCriticoItem } from "@/types/progress";
import { AlertCircle, BookOpen, Flame, Sparkles, CheckCircle2 } from "lucide-react";

interface TopCriticosHubProps {
  topCriticos: TopCriticoItem[];
  temPendencias: boolean;
}

export function TopCriticosHub({ topCriticos, temPendencias }: TopCriticosHubProps) {
  if (!temPendencias || topCriticos.length === 0) {
    return (
      <div className="w-full bg-emerald-50 dark:bg-emerald-950/30 rounded-2xl p-6 border border-emerald-200 dark:border-emerald-800 shadow-sm flex items-center gap-4">
        <div className="w-12 h-12 rounded-2xl bg-emerald-100 dark:bg-emerald-900/60 flex items-center justify-center flex-shrink-0 text-emerald-600 dark:text-emerald-400">
          <CheckCircle2 className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-base font-bold text-emerald-900 dark:text-emerald-200">
            Nenhum gargalo crítico detectado!
          </h3>
          <p className="text-xs sm:text-sm text-emerald-700 dark:text-emerald-300 mt-0.5">
            Todos os capítulos praticados apresentam aproveitamento ponderado igual ou superior a 75%. Continue avançando nos próximos volumes!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-rose-100 dark:bg-rose-950/60 flex items-center justify-center text-rose-600 dark:text-rose-400">
            <AlertCircle className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">
              Hub de Ação — Top 3 Gargalos de Aprendizagem (RN-PRG-016)
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Capítulos com taxa de acerto ponderada abaixo de 75% sugeridos para intervenção imediata
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {topCriticos.map((item, idx) => (
          <div
            key={item.capitulo_id}
            className="p-4 rounded-xl border border-rose-200/80 dark:border-rose-900/40 bg-rose-50/40 dark:bg-rose-950/20 flex flex-col justify-between space-y-3"
          >
            <div>
              <div className="flex items-center justify-between gap-1 mb-1.5">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-900/60 text-rose-700 dark:text-rose-300">
                  Prioridade #{idx + 1}
                </span>
                <span className="text-xs font-mono font-bold text-rose-600 dark:text-rose-400">
                  {item.taxa_acerto_ponderada.toFixed(1)}% acerto
                </span>
              </div>

              <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 block">
                Vol. {item.numero_volume}: {item.titulo_volume}
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white mt-0.5 line-clamp-2">
                {item.titulo_capitulo}
              </h4>

              {item.total_erros_na_caixa_reforco > 0 && (
                <div className="flex items-center gap-1.5 mt-2 text-[11px] text-amber-700 dark:text-amber-300 font-medium">
                  <Flame className="w-3.5 h-3.5 text-amber-500" />
                  <span>{item.total_erros_na_caixa_reforco} erro(s) na Caixa de Reforço</span>
                </div>
              )}
            </div>

            {/* Hub de Ação com as 2 Alternativas Claras */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2 border-t border-rose-100 dark:border-rose-900/30">
              <Link
                href={item.acao_revisar_teoria_url}
                className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/60 transition-colors shadow-sm"
              >
                <BookOpen className="w-3.5 h-3.5 text-subject-600" />
                <span>Revisar Teoria</span>
              </Link>
              <Link
                href={item.acao_praticar_reforco_url}
                className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold bg-subject-500 hover:bg-subject-600 text-white transition-colors shadow-sm"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Praticar Reforço</span>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
