"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Clock, ArrowRight, ShieldCheck, Award, Sparkles } from "lucide-react";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { api, extrairMensagemErro } from "@/lib/api";
import {
  ItemExercicio,
  IniciarCatResponse,
  CatStatusResponse,
} from "@/types/exercise";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";
import { CatRadarChart } from "@/components/exercises/CatRadarChart";

export default function ProvaCatPage() {
  useHeartbeat();
  const router = useRouter();

  const [sessaoId, setSessaoId] = useState<string | null>(null);
  const [itemAtual, setItemAtual] = useState<ItemExercicio | null>(null);
  const [respostaSelecionada, setRespostaSelecionada] = useState<string>("");
  const [indicadorProgresso, setIndicadorProgresso] = useState<string>("Iniciando avaliação...");
  const [loading, setLoading] = useState<boolean>(true);
  const [submetendo, setSubmetendo] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [resultadoFinal, setResultadoFinal] = useState<CatStatusResponse | null>(null);

  // Cronômetro da questão atual
  const [segundosGastos, setSegundosGastos] = useState<number>(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSegundosGastos((s) => s + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [itemAtual?.id]);

  // Inicializa a sessão CAT no mount
  useEffect(() => {
    async function iniciarCat() {
      try {
        setLoading(true);
        // Primeiro recupera o ID da disciplina de matemática
        const disciplinas: any[] = await api.get("/api/v1/conteudo/disciplinas");
        const mat = disciplinas.find((d) => d.slug === "matematica") || disciplinas[0];

        if (!mat) {
          throw new Error("Disciplina de Matemática não localizada.");
        }

        const res: IniciarCatResponse = await api.post("/api/v1/exercicios/cat/iniciar", {
          disciplina_id: mat.id,
          tipo_prova: "onboarding_diagnostico",
        });

        setSessaoId(res.sessao_cat_id);
        setItemAtual(res.primeiro_item);
        setIndicadorProgresso(res.indicador_progresso);
      } catch (err: any) {
        setError(extrairMensagemErro(err, "Não foi possível iniciar a prova diagnóstica CAT."));
      } finally {
        setLoading(false);
      }
    }
    iniciarCat();
  }, []);

  const handleSubmeter = async () => {
    if (!sessaoId || !itemAtual || !respostaSelecionada.trim() || submetendo) return;

    try {
      setSubmetendo(true);
      const res: CatStatusResponse = await api.post("/api/v1/exercicios/cat/submeter", {
        sessao_cat_id: sessaoId,
        item_id: itemAtual.id,
        resposta_enviada: respostaSelecionada.trim(),
        tempo_resposta_segundos: Math.max(1, segundosGastos),
      });

      if (res.finalizado) {
        setResultadoFinal(res);
      } else if (res.proximo_item) {
        setItemAtual(res.proximo_item);
        setIndicadorProgresso(res.indicador_progresso);
        setRespostaSelecionada("");
        setSegundosGastos(0);
      }
    } catch (err: any) {
      alert(extrairMensagemErro(err, "Falha ao submeter resposta no teste adaptativo."));
    } finally {
      setSubmetendo(false);
    }
  };

  const formatarTempo = (segundos: number) => {
    const m = Math.floor(segundos / 60);
    const s = segundos % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader />

      <main className="flex-1 max-w-3xl w-full mx-auto px-4 py-8">
        {loading ? (
          <div className="p-16 text-center text-slate-400">
            <div className="inline-block w-8 h-8 border-4 border-[#F57C00] border-t-transparent rounded-full animate-spin mb-4" />
            <p className="font-semibold text-sm">Calibrando seu teste adaptativo...</p>
          </div>
        ) : error ? (
          <div className="p-8 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-2xl text-center text-rose-700 dark:text-rose-300">
            {error}
          </div>
        ) : resultadoFinal ? (
          /* Tela de Dossiê Diagnóstico CAT com Gráfico Radar */
          <div className="space-y-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-amber-100 dark:bg-amber-950/60 text-[#F57C00] rounded-full flex items-center justify-center mx-auto mb-3 shadow-xs">
                <Sparkles className="w-8 h-8" />
              </div>
              <h2 className="text-2xl font-black text-slate-900 dark:text-white">
                Avaliação Diagnóstica Concluída!
              </h2>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                O motor psicométrico convergiu sua proficiência estimada ($\theta$) com precisão Bayesiana.
              </p>
            </div>

            {/* Radar Chart Component */}
            {resultadoFinal.scores_grandes_areas && (
              <CatRadarChart
                scores={resultadoFinal.scores_grandes_areas}
                thetaFinal={resultadoFinal.theta_final ?? 0.0}
                classificacao={resultadoFinal.classificacao ?? "Intermediário"}
              />
            )}

            {/* Resumo Estatístico */}
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-xs text-slate-400 uppercase block">Escore θ Geral</span>
                <span className="text-lg font-mono font-bold text-[#F57C00]">
                  {resultadoFinal.theta_final !== undefined && resultadoFinal.theta_final !== null
                    ? (resultadoFinal.theta_final >= 0 ? `+${resultadoFinal.theta_final.toFixed(2)}` : resultadoFinal.theta_final.toFixed(2))
                    : "0.00"}
                </span>
              </div>
              <div className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-xs text-slate-400 uppercase block">Erro Padrão (SE)</span>
                <span className="text-lg font-mono font-bold text-slate-700 dark:text-slate-300">
                  ±{resultadoFinal.erro_padrao?.toFixed(2) ?? "0.30"}
                </span>
              </div>
              <div className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-xs text-slate-400 uppercase block">Itens Resolvidos</span>
                <span className="text-lg font-mono font-bold text-slate-700 dark:text-slate-300">
                  {resultadoFinal.total_questoes_respondidas ?? 12}
                </span>
              </div>
            </div>

            {/* Botão de Avanço */}
            <div className="text-center pt-2">
              <button
                onClick={() => router.push(resultadoFinal.redirecionar_url || "/materias")}
                className="px-8 py-3 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-sm shadow-md hover:shadow-lg transition-all inline-flex items-center gap-2"
              >
                Acessar Trilha Personalizada
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        ) : itemAtual ? (
          /* Ambiente de Prova Adaptativa (Submissão Cega) */
          <div className="bg-white dark:bg-slate-900 rounded-2xl p-7 border border-slate-200 dark:border-slate-800 shadow-sm">
            {/* Header da Prova CAT */}
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4 mb-5">
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-lg uppercase tracking-wider">
                  {indicadorProgresso}
                </span>
                <span className="flex items-center gap-1 text-xs text-slate-400">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                  Ambiente Calibrado
                </span>
              </div>

              <div className="flex items-center gap-1.5 text-xs font-mono font-semibold text-slate-500 bg-slate-50 dark:bg-slate-800/60 px-3 py-1 rounded-lg">
                <Clock className="w-3.5 h-3.5 text-[#F57C00]" />
                {formatarTempo(segundosGastos)}
              </div>
            </div>

            {/* Enunciado */}
            <div className="mb-6">
              <KaTeXRenderer content={itemAtual.enunciado_katex} className="text-base leading-relaxed" />
            </div>

            {/* Alternativas ou Input Numérico */}
            <div className="mb-6">
              {itemAtual.tipo_item === "multiple_choice" ? (
                <div className="space-y-3">
                  {(itemAtual.alternativas || []).map((alt) => {
                    const selecionada = respostaSelecionada === alt.letra;
                    return (
                      <button
                        key={alt.letra}
                        type="button"
                        disabled={submetendo}
                        onClick={() => setRespostaSelecionada(alt.letra)}
                        className={`w-full text-left p-4 rounded-xl border transition-all flex items-start gap-3.5 ${
                          selecionada
                            ? "border-[#F57C00] bg-orange-50/50 dark:bg-orange-950/20 shadow-xs"
                            : "border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900"
                        }`}
                      >
                        <span
                          className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 transition-colors ${
                            selecionada
                              ? "bg-[#F57C00] text-white"
                              : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
                          }`}
                        >
                          {alt.letra}
                        </span>
                        <div className="pt-0.5 flex-1">
                          <KaTeXRenderer content={alt.texto_katex} />
                        </div>
                      </button>
                    );
                  })}
                </div>
              ) : (
                <div className="space-y-3">
                  <input
                    type="text"
                    value={respostaSelecionada}
                    onChange={(e) => setRespostaSelecionada(e.target.value)}
                    placeholder="Digite sua resposta"
                    disabled={submetendo}
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 font-mono text-base focus:ring-2 focus:ring-[#F57C00] outline-none"
                  />
                  {respostaSelecionada.trim() && (
                    <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
                      <KaTeXRenderer content={`$${respostaSelecionada}$`} />
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Botão de Envio Cego */}
            <div className="flex justify-end pt-2">
              <button
                onClick={handleSubmeter}
                disabled={!respostaSelecionada.trim() || submetendo}
                className="px-7 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-sm shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {submetendo ? "Calculando..." : "Próxima Questão"}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
}
