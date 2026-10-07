"use client";

import React from "react";
import { X, TrendingUp, AlertTriangle } from "lucide-react";

// ── Tipos ─────────────────────────────────────────────────────────────────────

interface CatRecomendacaoModalProps {
  /** Mapa de scores brutos (theta, escala –3 a +3) por chave de área */
  scores: Record<string, number>;
  /** Callback para fechar o modal */
  onFechar: () => void;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Mapa de chave → nome exibido (deve ser idêntico ao de CatRadarChart) */
const LABELS_AREAS: Record<string, string> = {
  algebra_funcoes: "Álgebra e Funções",
  geometria: "Geometria e Trigonometria",
  combinatoria_probabilidade: "Combinatória e Probabilidade",
  matematica_financeira: "Matemática Financeira e Estatística",
  algebra_linear: "Álgebra Linear e Sequências",
  aplicada: "Matemática Aplicada e Estatística",
};

/** Converte theta (–3 a +3) para percentual pedagógico (0 a 100) */
function thetaParaPorcentagem(theta: number): number {
  return Math.round(((Math.min(Math.max(theta, -3), 3) + 3) / 6) * 100);
}

type Faixa = "fraca" | "mediana" | "boa";

function classificarFaixa(porcentagem: number): Faixa {
  if (porcentagem < 50) return "fraca";
  if (porcentagem <= 70) return "mediana";
  return "boa";
}

// ── Lógica de mensagem ────────────────────────────────────────────────────────

interface AreaClassificada {
  chave: string;
  nome: string;
  porcentagem: number;
  faixa: Faixa;
}

function gerarMensagem(areas: AreaClassificada[]): {
  titulo: string;
  paragrafos: string[];
  icone: "alerta" | "dica";
} {
  const fracas = areas.filter((a) => a.faixa === "fraca");
  const medianas = areas.filter((a) => a.faixa === "mediana");

  // Ordena por pior desempenho primeiro (para prioridade na mensagem)
  const fracasOrdenadas = [...fracas].sort((a, b) => a.porcentagem - b.porcentagem);
  const medianasOrdenadas = [...medianas].sort((a, b) => a.porcentagem - b.porcentagem);

  // ── Cenário 1: sem áreas problemáticas ──────────────────────────────────────
  if (fracas.length === 0 && medianas.length === 0) {
    return {
      titulo: "Excelente desempenho diagnóstico! 🎉",
      paragrafos: [
        "Você demonstrou domínio sólido em todas as grandes áreas da Matemática nesta avaliação diagnóstica.",
        "Continue explorando os conteúdos avançados da plataforma para aprofundar ainda mais seus conhecimentos.",
      ],
      icone: "dica",
    };
  }

  // ── Cenário 2: apenas medianas, sem fracas ───────────────────────────────────
  if (fracas.length === 0) {
    const nomesMedianas = medianasOrdenadas.map((a) => `"${a.nome}"`).join(", ");
    return {
      titulo: "Desempenho razoável — há espaço para crescer!",
      paragrafos: [
        `Conforme seu desempenho na Prova Diagnóstica, você apresentou resultado intermediário em ${nomesMedianas}.`,
        "Apesar do desempenho razoável, para aprimorar seus conhecimentos e alcançar um nível mais avançado, é importante que você busque assinar e praticar os conteúdos dessas áreas.",
      ],
      icone: "dica",
    };
  }

  // ── Cenário 3: apenas fracas, sem medianas ───────────────────────────────────
  if (medianas.length === 0) {
    const nomesFracas = fracasOrdenadas.map((a) => `"${a.nome}"`).join(", ");
    if (fracas.length === 1) {
      return {
        titulo: "Atenção: área que exige prioridade!",
        paragrafos: [
          `Conforme seu desempenho na Prova Diagnóstica, recomendamos que você priorize assinar aulas de ${nomesFracas}.`,
          "Fortalecer essa área é fundamental para avançar com segurança nos demais conteúdos da plataforma.",
        ],
        icone: "alerta",
      };
    }
    return {
      titulo: "Atenção: áreas que exigem prioridade!",
      paragrafos: [
        `Conforme seu desempenho na Prova Diagnóstica, recomendamos que você priorize assinar aulas das seguintes áreas: ${nomesFracas}.`,
        "Essas são as áreas em que seu desempenho ficou abaixo de 50%. Dedicar atenção a elas trará uma evolução significativa no seu aproveitamento geral.",
      ],
      icone: "alerta",
    };
  }

  // ── Cenário 4: fracas E medianas ─────────────────────────────────────────────
  const nomePrioridade = fracasOrdenadas[0].nome;
  const outrasFracas = fracasOrdenadas.slice(1).map((a) => `"${a.nome}"`);
  const nomesMedianas = medianasOrdenadas.map((a) => `"${a.nome}"`).join(", ");

  const paragrafos: string[] = [];

  // Parágrafo sobre a prioridade máxima (pior área fraca)
  paragrafos.push(
    `Conforme seu desempenho na Prova Diagnóstica, recomendamos que você priorize, acima de tudo, assinar aulas de "${nomePrioridade}" — área em que seu resultado foi o mais baixo e exige atenção imediata.`
  );

  // Se há outras fracas além da pior
  if (outrasFracas.length > 0) {
    paragrafos.push(
      `Além disso, ${outrasFracas.join(", ")} ${outrasFracas.length === 1 ? "também apresentou resultado" : "também apresentaram resultados"} abaixo de 50% e ${outrasFracas.length === 1 ? "deve ser trabalhada" : "devem ser trabalhadas"} logo em seguida.`
    );
  }

  // Parágrafo sobre as medianas
  paragrafos.push(
    `É importante também que você assine conteúdos de ${nomesMedianas}, ${medianasOrdenadas.length === 1 ? "área em que" : "áreas em que"} seu desempenho foi razoável (entre 50% e 70%). Aprimorar esses conhecimentos complementará sua evolução de forma equilibrada.`
  );

  return {
    titulo: "Resultado diagnóstico: áreas para priorizar",
    icone: "alerta",
    paragrafos,
  };
}

// ── Componente ────────────────────────────────────────────────────────────────

export function CatRecomendacaoModal({ scores, onFechar }: CatRecomendacaoModalProps) {
  // Processa cada área recebida
  const areas: AreaClassificada[] = Object.entries(scores).map(([chave, theta]) => {
    const porcentagem = thetaParaPorcentagem(theta);
    return {
      chave,
      nome: LABELS_AREAS[chave] ?? chave,
      porcentagem,
      faixa: classificarFaixa(porcentagem),
    };
  });

  const { titulo, paragrafos, icone } = gerarMensagem(areas);
  const isAlerta = icone === "alerta";

  return (
    /* Overlay */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-titulo-recomendacao"
    >
      {/* Painel do modal */}
      <div className="relative w-full max-w-lg bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden">

        {/* Faixa superior colorida */}
        <div
          className={`h-1.5 w-full ${isAlerta ? "bg-amber-400" : "bg-emerald-400"}`}
          aria-hidden="true"
        />

        {/* Botão de fechar */}
        <button
          onClick={onFechar}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          aria-label="Fechar recomendação"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Conteúdo */}
        <div className="p-6 pt-5">
          {/* Ícone + Título */}
          <div className="flex items-start gap-3 mb-4">
            <div
              className={`shrink-0 w-10 h-10 rounded-xl flex items-center justify-center ${
                isAlerta
                  ? "bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400"
                  : "bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400"
              }`}
            >
              {isAlerta ? (
                <AlertTriangle className="w-5 h-5" />
              ) : (
                <TrendingUp className="w-5 h-5" />
              )}
            </div>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-widest text-slate-400 dark:text-slate-500 mb-0.5">
                Recomendação Personalizada
              </p>
              <h2
                id="modal-titulo-recomendacao"
                className="text-base font-bold text-slate-900 dark:text-white leading-snug"
              >
                {titulo}
              </h2>
            </div>
          </div>

          {/* Parágrafos da mensagem */}
          <div className="space-y-3 text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {paragrafos.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
          </div>

          {/* Legenda de referência das faixas */}
          <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-wrap gap-3 text-[11px] text-slate-500 dark:text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-400 shrink-0" />
              Abaixo de 50% — prioridade alta
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shrink-0" />
              50% a 70% — aprimoramento recomendado
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shrink-0" />
              Acima de 70% — bom desempenho
            </span>
          </div>
        </div>

        {/* Botão de fechar na base */}
        <div className="px-6 pb-5">
          <button
            onClick={onFechar}
            className="w-full py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm transition-colors shadow-sm"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
}
