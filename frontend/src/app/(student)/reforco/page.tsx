"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Inbox,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  ArrowLeft,
  CheckCircle,
} from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { api, extrairMensagemErro } from "@/lib/api";
import { ItemCaixaReforco, ItemExercicio, SubmissaoResult } from "@/types/exercise";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";

export default function CaixaReforcoPage() {
  useHeartbeat();

  const [itens, setItens] = useState<ItemCaixaReforco[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // RN-EXE-011: sessão de treino de reforço ilimitado com Questões Gêmeas inline
  const [gemeaAtual, setGemeaAtual] = useState<ItemExercicio | null>(null);
  const [gerandoGemea, setGerandoGemea] = useState<string | null>(null);

  async function carregarReforco() {
    try {
      setLoading(true);
      const data: ItemCaixaReforco[] = await api.get("/api/v1/exercicios/caixa-reforco");
      setItens(data);
    } catch (err: any) {
      setError(extrairMensagemErro(err, "Não foi possível carregar a Caixa de Reforço."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    carregarReforco();
  }, []);

  const handlePraticarGemea = async (itemMatrizId: string) => {
    try {
      setGerandoGemea(itemMatrizId);
      const nova: ItemExercicio = await api.post(
        `/api/v1/exercicios/gerar-gemea/${itemMatrizId}`
      );
      setGemeaAtual(nova);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err: any) {
      alert(extrairMensagemErro(err, "Falha ao gerar Questão Gêmea."));
    } finally {
      setGerandoGemea(null);
    }
  };

  const handleSubmeterGemea = async (
    itemId: string,
    tentativaNumero: 1 | 2,
    tipoItem: "multiple_choice" | "numeric_input",
    resposta: string,
    tempoSegundos: number
  ): Promise<SubmissaoResult> => {
    // RN-EXE-008: o servidor é autoritativo no número de tentativas.
    const res: SubmissaoResult = await api.post("/api/v1/exercicios/submeter", {
      item_id: itemId,
      capitulo_id: gemeaAtual?.capitulo_id,
      tentativa_numero: tentativaNumero,
      tipo_item: tipoItem,
      resposta_enviada: resposta,
      tempo_resposta_segundos: tempoSegundos,
    });
    return res;
  };

  const handleGerarGemeaEncadeada = async (itemMatrizId: string) => {
    // Prática ilimitada: a gêmea pode gerar outra variação da mesma estrutura
    await handlePraticarGemea(itemMatrizId);
  };

  const handleFecharPratica = () => {
    // Recarrega a lista: se a gêmea foi acertada, o backend marcou o item como 'superado'
    setGemeaAtual(null);
    carregarReforco();
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col">

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8">
        {/* Cabeçalho */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <Link
              href="/materias"
              className="flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors mb-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Voltar ao Catálogo
            </Link>
            <h1 className="text-2xl font-black text-slate-900 dark:text-white flex items-center gap-2.5">
              <Inbox className="w-7 h-7 text-subject-600" />
              Caixa de Reforço
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
              Exercícios onde você encontrou desafios. Pratique Questões Gêmeas para superar suas dúvidas.
            </p>
          </div>

          <div className="text-right">
            <span className="text-2xl font-black text-subject-600 font-mono">
              {itens.length}
            </span>
            <span className="text-xs text-slate-400 block uppercase tracking-wider">
              {itens.length === 1 ? "Item Pendente" : "Itens Pendentes"}
            </span>
          </div>
        </div>

        {/* Sessão de Prática Ativa: Questão Gêmea inline (RN-EXE-011) */}
        {gemeaAtual && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500 dark:text-ink-muted flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-600" />
                Treino de Reforço — Questão Gêmea
              </h2>
              <button
                onClick={handleFecharPratica}
                className="text-xs font-semibold text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors px-3 py-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-surface-elevated"
              >
                Encerrar treino e atualizar caixa
              </button>
            </div>
            <ExerciseCard
              key={gemeaAtual.id}
              item={gemeaAtual}
              onSubmeter={handleSubmeterGemea}
              onGerarGemea={handleGerarGemeaEncadeada}
              onProximo={handleFecharPratica}
            />
          </div>
        )}

        {/* Lista de Itens */}
        {loading ? (
          <div className="p-16 text-center text-slate-400">
            <div className="inline-block w-8 h-8 border-4 border-subject-500 border-t-transparent rounded-full animate-spin mb-4" />
            <p>Consultando sua Caixa de Reforço...</p>
          </div>
        ) : error ? (
          <div className="p-6 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-2xl text-rose-700 dark:text-rose-300 text-center">
            {error}
          </div>
        ) : itens.length === 0 ? (
          /* Estado Vazio: Nenhuma pendência */
          <div className="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs max-w-md mx-auto">
            <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">
              Sua Caixa de Reforço está vazia!
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
              Você não possui exercícios pendentes de revisão. Continue seus estudos nos próximos tópicos.
            </p>
            <Link
              href="/materias"
              className="px-6 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm shadow-sm transition-all inline-block"
            >
              Explorar Novas Aulas
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {itens.map((item, idx) => (
              <div
                key={item.id}
                className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-xs transition-all hover:border-slate-300 dark:hover:border-slate-700"
              >
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 font-bold text-xs rounded-md uppercase tracking-wider">
                      Item #{idx + 1}
                    </span>
                    <span className="flex items-center gap-1 text-xs text-amber-600 dark:text-amber-400 font-medium">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      {item.total_erros === 1 ? "1 erro duplo" : `${item.total_erros} erros acumulados`}
                    </span>
                  </div>

                  <span className="text-xs text-slate-400 font-mono">
                    {new Date(item.arquivado_em).toLocaleDateString("pt-BR")}
                  </span>
                </div>

                <div className="my-3 pl-1">
                  <KaTeXRenderer content={item.enunciado_katex} className="text-sm text-slate-800 dark:text-slate-200" />
                </div>

                <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-3">
                  <button
                    onClick={() => handlePraticarGemea(item.item_id)}
                    disabled={gerandoGemea === item.item_id}
                    className="px-4 py-2 rounded-xl border border-purple-300 dark:border-purple-800 hover:bg-purple-50 dark:hover:bg-purple-950/30 text-purple-700 dark:text-purple-300 font-bold text-xs flex items-center gap-2 transition-all disabled:opacity-50"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    {gerandoGemea === item.item_id ? "Gerando..." : "Praticar Questão Gêmea agora"}
                  </button>
                  <Link
                    href={`/exercicios/${item.capitulo_id}`}
                    className="px-4 py-2 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs flex items-center gap-2 shadow-xs transition-all"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    Praticar no Capítulo
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
