"use client";

/**
 * ExerciseCard — superfície da questão em focus mode (Fase 5).
 *
 * Flat, sem card-in-card: enunciado grande (KaTeX), alternativas com chip
 * de letra, CTA único full-width na base (>= 48px, RN-INT-009).
 * Lógica preservada: tentativas 1|2, pista socrática na 1ª chance,
 * pontuação, resolução completa e Questão Gêmea.
 */

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

  const isGemea = item.tipo_origem === "gemea_ia";

  return (
    <div className="w-full">
      {/* ── Meta da questão (fora do card: flat) ── */}
      <div className="flex items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2">
          {numeroExercicio && (
            <span
              aria-current="step"
              className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-subject-500 text-white font-black text-sm tabular-nums"
            >
              {numeroExercicio}
            </span>
          )}
          {isGemea && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-violet-100 dark:bg-violet-950/40 text-violet-700 dark:text-violet-300 text-[11px] font-bold">
              <Sparkles className="w-3 h-3" aria-hidden="true" />
              Questão Gêmea
            </span>
          )}
        </div>
        <span className="text-[11px] font-semibold text-ink-faint tabular-nums">
          Tentativa {tentativaNumero}/2
        </span>
      </div>

      {/* ── Enunciado: protagonista absoluto ── */}
      <div className="mb-8">
        <KaTeXRenderer content={item.enunciado_katex} className="text-base sm:text-lg leading-relaxed" />
      </div>

      {/* ── Entrada: Múltipla Escolha vs Input Numérico ── */}
      {!isFinalizado && !resultado?.permite_segunda_chance && (
        <div className="mb-6">
          {item.tipo_item === "multiple_choice" ? (
            <fieldset className="space-y-2.5">
              <legend className="sr-only">Alternativas da questão</legend>
              {(item.alternativas || []).map((alt) => {
                const selecionada = respostaSelecionada === alt.letra;
                return (
                  <button
                    key={alt.letra}
                    type="button"
                    disabled={carregando || disabled}
                    aria-pressed={selecionada}
                    onClick={() => setRespostaSelecionada(alt.letra)}
                    className={`w-full text-left px-4 py-3.5 rounded-xl border transition-colors flex items-start gap-3.5 ${
                      selecionada
                        ? "border-subject-500 bg-subject-wash"
                        : "border-line bg-surface-card hover:border-line-strong hover:bg-surface-elevated/60"
                    }`}
                  >
                    <span
                      className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 transition-colors ${
                        selecionada
                          ? "bg-subject-500 text-white"
                          : "bg-surface-elevated text-ink-muted"
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
            </fieldset>
          ) : (
            <div className="space-y-3">
              <label
                htmlFor="resposta-numerica"
                className="block text-xs font-semibold uppercase tracking-wider text-ink-faint"
              >
                Digite sua resposta numérica ou algébrica:
              </label>
              <input
                id="resposta-numerica"
                type="text"
                inputMode="text"
                autoComplete="off"
                value={respostaSelecionada}
                onChange={(e) => setRespostaSelecionada(e.target.value)}
                placeholder="Exemplo: 5 ou x^2 - 4"
                disabled={carregando || disabled}
                className="w-full px-4 py-3.5 rounded-xl border border-line-strong bg-surface-card text-ink-text font-mono text-lg focus:ring-2 focus:ring-subject-300 focus:border-subject-500 outline-none transition-colors"
              />
              {respostaSelecionada.trim() && (
                <div className="px-4 py-3 bg-surface-elevated rounded-xl border border-line">
                  <span className="text-[10px] font-bold uppercase tracking-widest text-ink-faint block mb-1">
                    Pré-visualização
                  </span>
                  <KaTeXRenderer content={`$${respostaSelecionada}$`} />
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── Feedback: 1ª tentativa errada (pista + 2ª chance) ── */}
      {resultado && resultado.permite_segunda_chance && !resultado.acertou && (
        <div className="p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 mb-6">
          <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 font-bold text-sm mb-2">
            <AlertCircle className="w-5 h-5 text-amber-600" aria-hidden="true" />
            1ª tentativa incorreta — não desanime!
          </div>

          {resultado.pista_socratica_ia && (
            <div className="mt-3 p-4 rounded-xl bg-surface-card border border-amber-200/60 dark:border-amber-900/40">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 mb-1">
                <HelpCircle className="w-3.5 h-3.5" aria-hidden="true" />
                Pista Socrática do Tutor IA
              </div>
              <KaTeXRenderer
                content={resultado.pista_socratica_ia}
                className="text-sm text-ink-text"
              />
            </div>
          )}

          <div className="mt-4 flex justify-end">
            <button
              onClick={handleTentarSegundaChance}
              className="inline-flex items-center gap-2 px-5 py-2.5 min-h-[48px] rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
              Tentar 2ª chance (vale 0,5 ponto)
            </button>
          </div>
        </div>
      )}

      {/* ── CTA único na base (enquanto responde) ── */}
      {!isFinalizado && !resultado?.permite_segunda_chance && (
        <button
          onClick={handleSubmit}
          disabled={!respostaSelecionada.trim() || carregando || disabled}
          className="w-full inline-flex items-center justify-center gap-2 px-6 min-h-[52px] rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {carregando ? (
            "Corrigindo..."
          ) : (
            <>
              Confirmar Resposta
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </>
          )}
        </button>
      )}

      {/* ── Feedback: conclusão do exercício ── */}
      {isFinalizado && (
        <div className="space-y-5">
          {resultado.acertou ? (
            <div className="flex items-center gap-3">
              <span className="flex items-center justify-center w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-950/40 text-emerald-600 shrink-0">
                <CheckCircle2 className="w-5 h-5" aria-hidden="true" />
              </span>
              <div>
                <h4 className="font-bold text-sm text-ink-text">
                  {tentativaNumero === 1 ? "Acerto na 1ª tentativa!" : "Acerto na 2ª tentativa."}
                </h4>
                <p className="text-xs text-ink-muted tabular-nums">
                  +{resultado.pontuacao_obtida.toFixed(1).replace(".", ",")} ponto
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <span className="flex items-center justify-center w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-950/40 text-rose-600 shrink-0">
                <XCircle className="w-5 h-5" aria-hidden="true" />
              </span>
              <div>
                <h4 className="font-bold text-sm text-ink-text">Tentativas esgotadas (0,0 pontos).</h4>
                <p className="text-xs text-ink-muted">
                  Gabarito:{" "}
                  <strong>Alternativa {resultado.resposta_correta || "Indisponível"}</strong>. Esta questão
                  foi arquivada na sua <strong>Caixa de Reforço</strong>.
                </p>
              </div>
            </div>
          )}

          {/* Resolução completa KaTeX */}
          {resultado.resolucao_completa_katex && (
            <div className="p-5 rounded-2xl bg-surface-elevated border border-line">
              <h5 className="font-bold text-[10px] uppercase tracking-widest text-ink-faint mb-3">
                Resolução passo a passo
              </h5>
              <KaTeXRenderer
                content={resultado.resolucao_completa_katex}
                className="text-sm text-ink-text"
              />
            </div>
          )}

          {/* Ações finais: gêmea à esquerda, próxima à direita */}
          <div className="flex items-center justify-between gap-3 pt-1">
            {resultado.pode_gerar_gemea && onGerarGemea ? (
              <button
                onClick={handleAcionarGemea}
                disabled={gerandoGemea}
                className="inline-flex items-center gap-2 px-4 min-h-[48px] rounded-xl border border-violet-300 dark:border-violet-800 hover:bg-violet-50 dark:hover:bg-violet-950/30 text-violet-700 dark:text-violet-300 font-semibold text-xs transition-colors"
              >
                <Sparkles className="w-4 h-4" aria-hidden="true" />
                {gerandoGemea ? "Gerando..." : "Questão Gêmea"}
              </button>
            ) : (
              <div />
            )}

            {onProximo && (
              <button
                onClick={onProximo}
                className="inline-flex items-center gap-2 px-6 min-h-[52px] rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm transition-colors"
              >
                Próxima Questão
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
