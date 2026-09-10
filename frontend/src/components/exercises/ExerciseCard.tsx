"use client";

import React, { useState } from "react";
import { ItemExercicio, SubmissaoResult } from "@/types/exercise";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";
import {
  CheckCircle2,
  AlertCircle,
  XCircle,
  HelpCircle,
  Sparkles,
  ArrowRight,
  RotateCcw,
} from "lucide-react";

interface ExerciseCardProps {
  item: ItemExercicio;
  numeroExercicio?: number;
  totalExercicios?: number;
  onSubmeter: (
    itemId: string,
    tentativaNumero: 1 | 2,
    tipoItem: "multiple_choice" | "numeric_input",
    resposta: string,
    tempoSegundos: number
  ) => Promise<SubmissaoResult>;
  onGerarGemea?: (itemMatrizId: string) => Promise<void>;
  onProximo?: () => void;
  disabled?: boolean;
}

export function ExerciseCard({
  item,
  numeroExercicio,
  totalExercicios,
  onSubmeter,
  onGerarGemea,
  onProximo,
  disabled = false,
}: ExerciseCardProps) {
  const [respostaSelecionada, setRespostaSelecionada] = useState<string>("");
  const [tentativaNumero, setTentativaNumero] = useState<1 | 2>(1);
  const [carregando, setCarregando] = useState(false);
  const [resultado, setResultado] = useState<SubmissaoResult | null>(null);
  const [tempoInicio] = useState<number>(Date.now());
  const [gerandoGemea, setGerandoGemea] = useState(false);

  const handleSubmit = async () => {
    if (!respostaSelecionada.trim() || carregando || disabled) return;

    setCarregando(true);
    const tempoGasto = Math.max(1, Math.round((Date.now() - tempoInicio) / 1000));

    try {
      const res = await onSubmeter(
        item.id,
        tentativaNumero,
        item.tipo_item,
        respostaSelecionada,
        tempoGasto
      );
      setResultado(res);
    } catch (err) {
      console.error("Erro na submissão do exercício:", err);
    } finally {
      setCarregando(false);
    }
  };

  const handleTentarSegundaChance = () => {
    setTentativaNumero(2);
    setResultado(null);
    setRespostaSelecionada("");
  };

  const handleAcionarGemea = async () => {
    if (!onGerarGemea) return;
    setGerandoGemea(true);
    try {
      await onGerarGemea(item.id);
    } finally {
      setGerandoGemea(false);
    }
  };

  const isFinalizado =
    resultado !== null &&
    (resultado.acertou || (!resultado.acertou && !resultado.permite_segunda_chance));

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm transition-all">
      {/* Header do Exercício */}
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4 mb-5">
        <div className="flex items-center gap-2">
          {numeroExercicio && (
            <span className="px-2.5 py-1 bg-orange-100 dark:bg-orange-950/60 text-[#F57C00] font-bold text-xs rounded-lg uppercase tracking-wider">
              Questão {numeroExercicio} {totalExercicios ? `de ${totalExercicios}` : ""}
            </span>
          )}
          {item.tipo_origem === "gemea_ia" && (
            <span className="flex items-center gap-1 px-2.5 py-1 bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 font-semibold text-xs rounded-lg">
              <Sparkles className="w-3.5 h-3.5" />
              Questão Gêmea
            </span>
          )}
        </div>
        <div className="text-xs text-slate-400 font-mono">
          Tentativa {tentativaNumero} de 2
        </div>
      </div>

      {/* Enunciado Formatado KaTeX */}
      <div className="mb-6">
        <KaTeXRenderer content={item.enunciado_katex} className="text-base leading-relaxed" />
      </div>

      {/* Bloco de Entrada: Múltipla Escolha vs Input Numérico */}
      {!isFinalizado && !resultado?.permite_segunda_chance && (
        <div className="mb-6">
          {item.tipo_item === "multiple_choice" ? (
            <div className="space-y-3">
              {(item.alternativas || []).map((alt) => {
                const selecionada = respostaSelecionada === alt.letra;
                return (
                  <button
                    key={alt.letra}
                    type="button"
                    disabled={carregando || disabled}
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
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500">
                Digite sua resposta numérica ou algébrica:
              </label>
              <input
                type="text"
                value={respostaSelecionada}
                onChange={(e) => setRespostaSelecionada(e.target.value)}
                placeholder="Exemplo: 5 ou x^2 - 4"
                disabled={carregando || disabled}
                className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white font-mono text-base focus:ring-2 focus:ring-[#F57C00] focus:border-transparent outline-none transition-all"
              />
              {respostaSelecionada.trim() && (
                <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
                  <span className="text-slate-400 block mb-1">Pré-visualização Matemática:</span>
                  <KaTeXRenderer content={`$${respostaSelecionada}$`} />
                </div>
              )}
            </div>
          )}

          {/* Botão de Envio */}
          <div className="mt-5 flex justify-end">
            <button
              onClick={handleSubmit}
              disabled={!respostaSelecionada.trim() || carregando || disabled}
              className="px-6 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-sm shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {carregando ? (
                <>Enviando...</>
              ) : (
                <>
                  Confirmar Resposta
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Estado de Feedback: 1ª Tentativa Errada (Pista Socrática e 2ª Chance) */}
      {resultado && resultado.permite_segunda_chance && !resultado.acertou && (
        <div className="p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 mb-5">
          <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 font-bold text-sm mb-2">
            <AlertCircle className="w-5 h-5 text-amber-600" />
            1ª Tentativa Incorreta — Não desanime!
          </div>

          {resultado.pista_socratica_ia && (
            <div className="mt-3 p-4 rounded-xl bg-white dark:bg-slate-900/80 border border-amber-200/60 dark:border-amber-900/40">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 mb-1">
                <HelpCircle className="w-3.5 h-3.5" />
                Pista Socrática do Tutor IA
              </div>
              <KaTeXRenderer content={resultado.pista_socratica_ia} className="text-sm text-slate-700 dark:text-slate-300" />
            </div>
          )}

          <div className="mt-4 flex justify-end">
            <button
              onClick={handleTentarSegundaChance}
              className="px-5 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs flex items-center gap-2 transition-colors shadow-xs"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Tentar 2ª Chance (Vale 0.5 ponto)
            </button>
          </div>
        </div>
      )}

      {/* Estado de Feedback: Conclusão do Exercício */}
      {isFinalizado && (
        <div className="space-y-4">
          {resultado.acertou ? (
            <div className="p-4 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/60 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0" />
                <div>
                  <h4 className="font-bold text-emerald-900 dark:text-emerald-200 text-sm">
                    {tentativaNumero === 1 ? "Excelente! Acerto na 1ª tentativa." : "Muito bem! Acerto na 2ª tentativa."}
                  </h4>
                  <p className="text-xs text-emerald-700 dark:text-emerald-400">
                    Pontuação obtida nesta questão: <strong>{resultado.pontuacao_obtida.toFixed(1)} ponto</strong>
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <XCircle className="w-6 h-6 text-rose-600 shrink-0" />
                <div>
                  <h4 className="font-bold text-rose-900 dark:text-rose-200 text-sm">
                    Tentativas esgotadas (0.0 pontos).
                  </h4>
                  <p className="text-xs text-rose-700 dark:text-rose-400">
                    Gabarito: <strong>Alternativa {resultado.resposta_correta || "Indisponível"}</strong>. Esta questão foi arquivada na sua <strong>Caixa de Reforço</strong>.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Resolução Completa KaTeX */}
          {resultado.resolucao_completa_katex && (
            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800">
              <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
                Resolução Passo a Passo
              </h5>
              <KaTeXRenderer content={resultado.resolucao_completa_katex} className="text-sm text-slate-700 dark:text-slate-300" />
            </div>
          )}

          {/* Botões de Ação Final */}
          <div className="flex items-center justify-between pt-2">
            {resultado.pode_gerar_gemea && onGerarGemea ? (
              <button
                onClick={handleAcionarGemea}
                disabled={gerandoGemea}
                className="px-4 py-2.5 rounded-xl border border-purple-300 dark:border-purple-800 hover:bg-purple-50 dark:hover:bg-purple-950/30 text-purple-700 dark:text-purple-300 font-semibold text-xs flex items-center gap-2 transition-all shadow-xs"
              >
                <Sparkles className="w-4 h-4 text-purple-600" />
                {gerandoGemea ? "Gerando Questão Gêmea..." : "Tentar Questão Gêmea similar agora"}
              </button>
            ) : <div />}

            {onProximo && (
              <button
                onClick={onProximo}
                className="px-6 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-sm flex items-center gap-2 shadow-sm transition-all"
              >
                Próxima Questão
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
