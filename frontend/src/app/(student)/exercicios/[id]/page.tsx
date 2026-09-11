"use client";

/**
 * /exercicios/[id] — Focus mode (Fase 5: "Caderno de Foco").
 *
 * Tela dedicada e focada (protótipo RN-INT §2.4): uma questão por vez,
 * sem navegação primária (AppShell focus-mode), sem cards dentro de cards.
 * A questão É a página: coluna única ~42rem, CTA único na base.
 *
 * Lógica preservada: submissão com tentativas (1|2), pontuação por acerto,
 * Questão Gêmea inserida após a atual, conclusão com aproveitamento.
 */

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, Award, Inbox, TrendingUp } from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { api, extrairMensagemErro } from "@/lib/api";
import { ItemExercicio, SubmissaoResult } from "@/types/exercise";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";

export default function ExerciciosCapituloPage() {
  useHeartbeat();
  const params = useParams();
  const capituloId = params.id as string;

  const [itens, setItens] = useState<ItemExercicio[]>([]);
  const [indiceAtual, setIndiceAtual] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pontuacoes, setPontuacoes] = useState<number[]>([]);
  const [concluido, setConcluido] = useState<boolean>(false);

  useEffect(() => {
    async function carregarExercicios() {
      if (!capituloId) return;
      try {
        setLoading(true);
        const data: ItemExercicio[] = await api.get(`/api/v1/exercicios/capitulo/${capituloId}`);
        setItens(data);
      } catch (err: any) {
        setError(extrairMensagemErro(err, "Não foi possível carregar a lista de exercícios."));
      } finally {
        setLoading(false);
      }
    }
    carregarExercicios();
  }, [capituloId]);

  const handleSubmeter = async (
    itemId: string,
    tentativaNumero: 1 | 2,
    tipoItem: "multiple_choice" | "numeric_input",
    resposta: string,
    tempoSegundos: number
  ): Promise<SubmissaoResult> => {
    const res: SubmissaoResult = await api.post("/api/v1/exercicios/submeter", {
      item_id: itemId,
      capitulo_id: capituloId,
      tentativa_numero: tentativaNumero,
      tipo_item: tipoItem,
      resposta_enviada: resposta,
      tempo_resposta_segundos: tempoSegundos,
    });

    if (res.acertou || (!res.acertou && !res.permite_segunda_chance)) {
      setPontuacoes((prev) => [...prev, res.pontuacao_obtida]);
    }

    return res;
  };

  const handleGerarGemea = async (itemMatrizId: string) => {
    try {
      const novaGemea: ItemExercicio = await api.post(
        `/api/v1/exercicios/gerar-gemea/${itemMatrizId}`
      );
      // Insere a nova questão gêmea imediatamente após a questão atual
      setItens((prev) => {
        const copia = [...prev];
        copia.splice(indiceAtual + 1, 0, novaGemea);
        return copia;
      });
      // Avança para a questão gêmea
      setIndiceAtual((prev) => prev + 1);
    } catch (err: any) {
      alert(extrairMensagemErro(err, "Falha ao gerar Questão Gêmea."));
    }
  };

  const handleProximo = () => {
    if (indiceAtual + 1 < itens.length) {
      setIndiceAtual((prev) => prev + 1);
    } else {
      setConcluido(true);
    }
  };

  const totalPontos = pontuacoes.reduce((acc, p) => acc + p, 0);
  const maxPontosPossivel = pontuacoes.length * 1.0;
  const aproveitamento = maxPontosPossivel > 0 ? Math.round((totalPontos / maxPontosPossivel) * 100) : 0;

  const pctProgresso = itens.length > 0 ? (indiceAtual / itens.length) * 100 : 0;

  return (
    <div className="min-h-screen flex flex-col text-slate-900 dark:text-slate-100">
      {/* ── Faixa de progresso da bateria (abaixo do GlobalHeader) ── */}
      {!loading && !error && itens.length > 0 && !concluido && (
        <div className="sticky top-14 z-20 border-b border-line bg-surface-bg/95 backdrop-blur supports-[backdrop-filter]:bg-surface-bg/90">
          <div className="max-w-2xl mx-auto px-4 sm:px-6 py-2.5 flex items-center gap-4">
            <Link
              href="/materias"
              aria-label="Sair da bateria e voltar para Matérias"
              className="p-1.5 -ml-1.5 rounded-lg text-ink-faint hover:text-ink-text hover:bg-surface-elevated transition-colors flex-shrink-0"
            >
              <ArrowLeft className="w-4 h-4" aria-hidden="true" />
            </Link>
            <div className="flex-1">
              <div className="flex items-center justify-between text-[11px] font-bold mb-1.5">
                <span className="uppercase tracking-widest text-ink-faint">
                  Questão {indiceAtual + 1} de {itens.length}
                </span>
                <span className="text-ink-faint tabular-nums">
                  {totalPontos.toFixed(1).replace(".", ",")} pts
                </span>
              </div>
              <div className="h-1 rounded-full bg-line overflow-hidden">
                <div
                  className="h-full bg-subject-500 transition-[width] duration-300 ease-out"
                  style={{ width: `${pctProgresso}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Palco central: a questão é a página ── */}
      <main className="flex-1 w-full max-w-2xl mx-auto px-4 sm:px-6 py-6 sm:py-10">
        {loading && (
          <div className="space-y-5" aria-busy="true" aria-label="Carregando exercícios">
            <div className="h-6 w-40 rounded-full bg-surface-elevated animate-pulse" />
            <div className="space-y-3">
              {[100, 92, 96, 78].map((w, i) => (
                <div
                  key={i}
                  className="h-4 rounded-full bg-surface-elevated animate-pulse"
                  style={{ width: `${w}%` }}
                />
              ))}
            </div>
            <div className="pt-4 space-y-2.5">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-14 rounded-xl bg-surface-card border border-line animate-pulse" />
              ))}
            </div>
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="rounded-2xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 p-6 text-center"
          >
            <p className="text-sm font-medium text-rose-700 dark:text-rose-300">{error}</p>
            <Link
              href="/materias"
              className="mt-4 inline-flex items-center gap-2 text-xs font-bold text-ink-muted hover:text-ink-text underline"
            >
              <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
              Voltar para Matérias
            </Link>
          </div>
        )}

        {concluido && (
          /* ── Conclusão: hero flat, número como protagonista ── */
          <div className="max-w-md mx-auto text-center pt-8 sm:pt-16">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-subject-wash text-subject-600 dark:text-subject-400 mb-5">
              <Award className="w-8 h-8" aria-hidden="true" />
            </div>
            <h2 className="text-2xl font-extrabold tracking-tight">Bateria concluída</h2>
            <p className="text-sm text-ink-muted mt-2">
              Você respondeu {pontuacoes.length} {pontuacoes.length === 1 ? "questão" : "questões"} deste capítulo.
            </p>

            <div className="mt-8 flex items-end justify-center gap-8 tabular-nums">
              <div>
                <span className="block text-5xl font-black text-subject-600 dark:text-subject-400 leading-none">
                  {aproveitamento}
                  <span className="text-2xl align-top">%</span>
                </span>
                <span className="block text-[11px] font-bold uppercase tracking-widest text-ink-faint mt-2">
                  Aproveitamento
                </span>
              </div>
              <div className="pb-1 text-left">
                <span className="block text-xl font-extrabold leading-none">
                  {totalPontos.toFixed(1).replace(".", ",")}
                </span>
                <span className="block text-[11px] text-ink-faint mt-1">
                  de {maxPontosPossivel.toFixed(1).replace(".", ",")} pontos
                </span>
              </div>
            </div>

            <div
              className={`mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold border ${
                aproveitamento >= 60
                  ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-900/40"
                  : "bg-amber-50 dark:bg-amber-950/30 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-900/40"
              }`}
            >
              <TrendingUp className="w-3.5 h-3.5" aria-hidden="true" />
              {aproveitamento >= 60
                ? "Capítulo validado para a árvore de habilidades"
                : "Abaixo de 60% — itens foram para a Caixa de Reforço"}
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
              <Link
                href="/materias"
                className="inline-flex items-center justify-center gap-2 px-6 min-h-[48px] rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm transition-colors"
              >
                Continuar Estudando
              </Link>
              <Link
                href="/reforco"
                className="inline-flex items-center justify-center gap-2 px-6 min-h-[48px] rounded-xl border border-line hover:bg-surface-elevated text-ink-muted font-semibold text-sm transition-colors"
              >
                <Inbox className="w-4 h-4" aria-hidden="true" />
                Ver Caixa de Reforço
              </Link>
            </div>
          </div>
        )}

        {!loading && !error && !concluido && itens.length > 0 && (
          <ExerciseCard
            key={itens[indiceAtual].id}
            item={itens[indiceAtual]}
            numeroExercicio={indiceAtual + 1}
            totalExercicios={itens.length}
            onSubmeter={handleSubmeter}
            onGerarGemea={handleGerarGemea}
            onProximo={handleProximo}
          />
        )}
      </main>
    </div>
  );
}
