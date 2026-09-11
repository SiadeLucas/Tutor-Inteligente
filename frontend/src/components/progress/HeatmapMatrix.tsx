"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HeatmapVolumeResponse, VolumeResumoItem, HeatmapCapituloItem } from "@/types/progress";
import { BookOpen, CheckCircle2, ChevronRight, HelpCircle } from "lucide-react";

interface HeatmapMatrixProps {
  volumes: VolumeResumoItem[];
  selectedVolume: HeatmapVolumeResponse | null;
  selectedVolumeId: string;
  onSelectVolume: (volumeId: string) => void;
  isLoadingVolume?: boolean;
}

export function HeatmapMatrix({
  volumes,
  selectedVolume,
  selectedVolumeId,
  onSelectVolume,
  isLoadingVolume = false,
}: HeatmapMatrixProps) {
  const [hoveredCap, setHoveredCap] = useState<HeatmapCapituloItem | null>(null);

  const getCorClasses = (statusCor: string) => {
    switch (statusCor) {
      case "verde":
        return "bg-emerald-500 hover:bg-emerald-600 text-white border-emerald-600 ring-emerald-300";
      case "amarelo":
        return "bg-amber-400 hover:bg-amber-500 text-slate-950 border-amber-500 ring-amber-300";
      case "vermelho":
        return "bg-rose-500 hover:bg-rose-600 text-white border-rose-600 ring-rose-300";
      case "cinza":
      default:
        return "bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700 ring-slate-400";
    }
  };

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col space-y-6">
      {/* Cabeçalho da Seção */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            Matriz de Domínio dos 11 Volumes (Gelson Iezzi)
          </h3>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
            Mapeamento visual do estado de maestria em cada capítulo do currículo
          </p>
        </div>

        {/* Legenda das 4 Cores Canônicas (RN-PRG-012) */}
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-md bg-slate-200 dark:bg-slate-700 border border-slate-300 dark:border-slate-600" />
            <span className="text-slate-500 dark:text-slate-400">&lt; 3 itens</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-md bg-rose-500 border border-rose-600" />
            <span className="text-slate-600 dark:text-slate-300">&lt; 50%</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-md bg-amber-400 border border-amber-500" />
            <span className="text-slate-600 dark:text-slate-300">50–74%</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-md bg-emerald-500 border border-emerald-600" />
            <span className="text-slate-600 dark:text-slate-300">&ge; 75%</span>
          </div>
        </div>
      </div>

      {/* Barra de Seleção de Volumes em Abas/Pílulas */}
      <div className="w-full overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-slate-200 dark:scrollbar-thumb-slate-800">
        <div className="flex items-center gap-2 min-w-max">
          {volumes.map((vol) => {
            const isSelected = vol.volume_id === selectedVolumeId;
            return (
              <button
                key={vol.volume_id}
                onClick={() => onSelectVolume(vol.volume_id)}
                className={`flex flex-col items-start px-3.5 py-2 rounded-xl text-left transition-all border ${
                  isSelected
                    ? "bg-subject-100 dark:bg-subject-wash-strong border-subject-500 text-subject-700 dark:text-subject-300 shadow-sm ring-1 ring-subject-300"
                    : "bg-slate-50 dark:bg-slate-800/60 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                }`}
              >
                <div className="flex items-center justify-between w-full gap-2">
                  <span className="font-bold text-xs">Vol. {vol.numero_volume}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-white/70 dark:bg-slate-900/70">
                    {vol.completude_percentual}%
                  </span>
                </div>
                <span className="text-[11px] truncate max-w-[130px] opacity-90 mt-0.5">
                  {vol.titulo_volume}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Grid de Capítulos do Volume Ativo */}
      <div className="min-h-[220px] relative">
        {isLoadingVolume ? (
          <div className="flex items-center justify-center h-48 text-slate-400 text-sm">
            Carregando capítulos do volume...
          </div>
        ) : selectedVolume ? (
          <div>
            {/* Cabeçalho do Volume Selecionado */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-subject-600" />
                <span className="font-bold text-sm text-slate-900 dark:text-white">
                  Volume {selectedVolume.numero_volume}: {selectedVolume.titulo_volume}
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                  ({selectedVolume.capitulos.length} capítulos)
                </span>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">Completude:</span>
                  <div className="w-28 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-subject-500 rounded-full transition-all duration-500"
                      style={{ width: `${selectedVolume.completude_volume_percentual}%` }}
                    />
                  </div>
                  <span className="text-xs font-mono font-bold text-subject-700 dark:text-subject-300">
                    {selectedVolume.completude_volume_percentual}%
                  </span>
                </div>
              </div>
            </div>

            {/* Matriz dos Capítulos */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {selectedVolume.capitulos.map((cap) => (
                <Link
                  key={cap.capitulo_id}
                  href={`/aula/${cap.capitulo_id}`}
                  onMouseEnter={() => setHoveredCap(cap)}
                  onMouseLeave={() => setHoveredCap(null)}
                  className={`group relative p-3 rounded-xl border transition-all duration-200 flex flex-col justify-between min-h-[90px] shadow-sm hover:scale-[1.02] hover:shadow-md ${getCorClasses(
                    cap.status_cor
                  )}`}
                >
                  <div className="flex items-start justify-between w-full gap-1">
                    <span className="font-mono text-xs font-bold opacity-80">
                      Cap. {cap.numero_capitulo}
                    </span>
                    {cap.aula_concluida && (
                      <CheckCircle2 className="w-3.5 h-3.5 flex-shrink-0" />
                    )}
                  </div>

                  <p className="text-xs font-semibold line-clamp-2 my-1.5 leading-snug">
                    {cap.titulo}
                  </p>

                  <div className="flex items-center justify-between text-[10px] font-mono opacity-90 pt-1 border-t border-current/20">
                    <span>{cap.total_exercicios_respondidos} itens</span>
                    <span className="font-bold">
                      {cap.total_exercicios_respondidos >= 3
                        ? `${cap.taxa_acertos_ponderada}%`
                        : "Neutro"}
                    </span>
                  </div>
                </Link>
              ))}
            </div>

            {/* Banner de Detalhes do Capítulo Selecionado/Hover */}
            {hoveredCap && (
              <div className="mt-4 p-3 bg-amber-50 dark:bg-amber-950/40 border border-amber-200/80 dark:border-amber-800/60 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                <div>
                  <span className="font-bold text-amber-900 dark:text-amber-200 mr-2">
                    Capítulo {hoveredCap.numero_capitulo}: {hoveredCap.titulo}
                  </span>
                  <span className="text-slate-600 dark:text-slate-300">
                    Taxa ponderada: <b>{hoveredCap.taxa_acertos_ponderada}%</b> ({hoveredCap.total_exercicios_respondidos} questões submetidas)
                  </span>
                </div>
                <Link
                  href={`/aula/${hoveredCap.capitulo_id}`}
                  className="flex items-center gap-1 font-semibold text-subject-700 dark:text-subject-300 hover:underline"
                >
                  Acessar Aula & Exercícios <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            )}
          </div>
        ) : (
          <div className="flex items-center justify-center h-48 text-slate-400 text-sm">
            Nenhum volume selecionado.
          </div>
        )}
      </div>
    </div>
  );
}
