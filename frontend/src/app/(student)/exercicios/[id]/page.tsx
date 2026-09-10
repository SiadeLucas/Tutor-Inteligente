"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, RotateCcw, Award } from "lucide-react";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { api, extrairMensagemErro } from "@/lib/api";
import { ItemExercicio, SubmissaoResult } from "@/types/exercise";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";

export default function ExerciciosCapituloPage() {
  useHeartbeat();
  const params = useParams();
  const router = useRouter();
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

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8">
        {/* Barra Superior de Navegação e Progresso */}
        <div className="flex items-center justify-between mb-6">
          <Link
            href="/materias"
            className="flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Voltar para Matérias
          </Link>

          {!loading && itens.length > 0 && !concluido && (
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Progresso: {indiceAtual + 1} / {itens.length}
              </span>
              <div className="w-32 h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#F57C00] transition-all duration-300"
                  style={{ width: `${((indiceAtual + 1) / itens.length) * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>

        {/* Conteúdo Central */}
        {loading ? (
          <div className="p-12 text-center text-slate-400">
            <div className="inline-block w-8 h-8 border-4 border-[#F57C00] border-t-transparent rounded-full animate-spin mb-4" />
            <p>Carregando exercícios de fixação...</p>
          </div>
        ) : error ? (
          <div className="p-6 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-2xl text-rose-700 dark:text-rose-300 text-center">
            {error}
          </div>
        ) : itens.length === 0 ? (
          <div className="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
            <p className="text-slate-500">Nenhum exercício cadastrado para este capítulo ainda.</p>
            <Link
              href="/materias"
              className="mt-4 inline-block px-5 py-2 rounded-xl bg-[#F57C00] text-white font-semibold text-xs"
            >
              Voltar ao Catálogo
            </Link>
          </div>
        ) : concluido ? (
          /* Tela de Conclusão da Bateria */
          <div className="bg-white dark:bg-slate-900 rounded-2xl p-8 border border-slate-200 dark:border-slate-800 text-center max-w-lg mx-auto shadow-sm">
            <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <Award className="w-8 h-8" />
            </div>
            <h2 className="text-2xl font-black text-slate-900 dark:text-white mb-2">
              Bateria de Fixação Concluída!
            </h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
              Você completou todos os exercícios recomendados para este capítulo.
            </p>

            <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl mb-6 grid grid-cols-2 gap-4 text-center">
              <div>
                <span className="text-xs text-slate-400 block uppercase">Pontuação Final</span>
                <span className="text-xl font-black text-[#F57C00]">
                  {totalPontos.toFixed(1)} / {maxPontosPossivel.toFixed(1)}
                </span>
              </div>
              <div>
                <span className="text-xs text-slate-400 block uppercase">Aproveitamento</span>
                <span className="text-xl font-black text-emerald-600 dark:text-emerald-400">
                  {aproveitamento}%
                </span>
              </div>
            </div>

            <div className="flex gap-3 justify-center">
              <Link
                href="/materias"
                className="px-6 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-sm shadow-sm transition-all"
              >
                Continuar Estudando
              </Link>
              <Link
                href="/reforco"
                className="px-6 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold text-sm transition-all"
              >
                Ver Caixa de Reforço
              </Link>
            </div>
          </div>
        ) : (
          /* Card do Exercício Ativo */
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
