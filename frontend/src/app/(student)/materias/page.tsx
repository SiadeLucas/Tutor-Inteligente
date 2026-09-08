"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  BookOpen,
  ChevronDown,
  ChevronRight,
  Clock,
  AlertCircle,
  PlayCircle,
  Sparkles,
  Layers,
  Compass,
  Grid,
  TrendingUp,
} from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { api, extrairMensagemErro } from "@/lib/api";
import { VolumeComCapitulos, SkillTreeNode } from "@/types/content";

const GRANDES_AREAS = [
  { key: "todas", label: "Todas as Áreas", icon: Layers },
  { key: "algebra_funcoes", label: "Álgebra e Funções", icon: TrendingUp },
  { key: "geometria", label: "Geometria e Trigonometria", icon: Compass },
  { key: "algebra_linear", label: "Álgebra Linear", icon: Grid },
  { key: "aplicada", label: "Matemática Aplicada", icon: Sparkles },
];

export default function MateriasPage() {
  useHeartbeat();

  const [volumes, setVolumes] = useState<VolumeComCapitulos[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedArea, setSelectedArea] = useState<string>("todas");
  const [expandedVolumes, setExpandedVolumes] = useState<Record<string, boolean>>({});

  useEffect(() => {
    async function loadSkillTree() {
      try {
        setLoading(true);
        // api.get injeta o Bearer token e trata refresh silencioso automaticamente
        const data: VolumeComCapitulos[] = await api.get(
          "/api/v1/conteudo/skill-tree?disciplina_slug=matematica"
        );
        setVolumes(data);

        // Expandir o Volume 1 por padrão
        if (data.length > 0) {
          setExpandedVolumes({ [data[0].id]: true });
        }
      } catch (err: any) {
        setError(extrairMensagemErro(err, "Não foi possível carregar a árvore de conteúdos."));
      } finally {
        setLoading(false);
      }
    }

    loadSkillTree();
  }, []);

  const toggleVolume = (volId: string) => {
    setExpandedVolumes((prev) => ({
      ...prev,
      [volId]: !prev[volId],
    }));
  };

  const filteredVolumes = useMemo(() => {
    if (selectedArea === "todas") return volumes;
    return volumes.filter((v) => v.grande_area === selectedArea);
  }, [volumes, selectedArea]);

  const totalCapitulosGeral = useMemo(() => {
    return volumes.reduce((acc, v) => acc + (v.capitulos?.length || 0), 0);
  }, [volumes]);

  const progressoGeral = useMemo(() => {
    const todos = volumes.flatMap((v) => v.capitulos || []);
    if (todos.length === 0) return 0;
    const concluidos = todos.filter((c) => c.status_dominio === "mastered").length;
    return Math.round((concluidos / todos.length) * 100);
  }, [volumes]);

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#1a1408] text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader userRole="student" userName="Aluno" showDisciplineBadge={true} />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        {/* Banner Curricular */}
        <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 sm:p-8 shadow-sm mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] border border-[#FFB74D]/30 mb-3">
                <BookOpen className="w-4 h-4 text-[#F57C00]" />
                <span>Coleção Gelson Iezzi — 11 Volumes</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                Árvore de Habilidades de Matemática 📐
              </h1>
              <p className="text-slate-600 dark:text-[#A89F91] text-sm mt-1.5 max-w-3xl leading-relaxed">
                Navegue pela progressão clássica de <strong>Fundamentos de Matemática Elementar</strong>. Cada capítulo
                foi dimensionado para sessões focadas de <strong>50 minutos</strong> com auxílio de inteligência artificial socrática.
              </p>
            </div>

            {/* Estatísticas Rápidas */}
            <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-slate-100 dark:border-[#382b1c] pt-4 md:pt-0 md:pl-6">
              <div className="text-center">
                <div className="text-2xl font-black text-[#F57C00]">{volumes.length}</div>
                <div className="text-xs text-slate-500 dark:text-[#A89F91]">Volumes</div>
              </div>
              <div className="h-8 w-px bg-slate-200 dark:bg-[#382b1c]" />
              <div className="text-center">
                <div className="text-2xl font-black text-slate-800 dark:text-slate-200">{totalCapitulosGeral}</div>
                <div className="text-xs text-slate-500 dark:text-[#A89F91]">Capítulos</div>
              </div>
              <div className="h-8 w-px bg-slate-200 dark:bg-[#382b1c]" />
              <div className="text-center">
                <div className="text-2xl font-black text-emerald-600">{progressoGeral}%</div>
                <div className="text-xs text-slate-500 dark:text-[#A89F91]">Domínio</div>
              </div>
            </div>
          </div>

          {/* Filtro por Grandes Áreas */}
          <div className="flex items-center gap-2 mt-6 overflow-x-auto pb-1 scrollbar-none border-t border-slate-100 dark:border-[#382b1c] pt-4">
            {GRANDES_AREAS.map((area) => {
              const Icon = area.icon;
              const isSelected = selectedArea === area.key;
              return (
                <button
                  key={area.key}
                  onClick={() => setSelectedArea(area.key)}
                  className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                    isSelected
                      ? "bg-[#F57C00] text-white shadow-sm shadow-orange-500/20"
                      : "bg-slate-100 dark:bg-[#1a1408] text-slate-600 dark:text-[#A89F91] hover:bg-slate-200 dark:hover:bg-[#332514]"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{area.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Estado de Carregamento */}
        {loading && (
          <div className="space-y-4">
            {[1, 2, 3].map((n) => (
              <div
                key={n}
                className="h-24 bg-white dark:bg-[#261d11] rounded-2xl border border-slate-200/80 dark:border-[#3d2f1f] animate-pulse"
              />
            ))}
          </div>
        )}

        {/* Estado de Erro */}
        {error && (
          <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/40 text-red-700 dark:text-red-400 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Lista de Volumes e Capítulos (Accordion) */}
        {!loading && !error && (
          <div className="space-y-5">
            {filteredVolumes.map((vol) => {
              const isExpanded = !!expandedVolumes[vol.id];
              const totalCaps = vol.capitulos?.length || 0;
              const dominioVolume = totalCaps > 0
                ? Math.round((vol.capitulos!.filter((c) => c.status_dominio === "mastered").length / totalCaps) * 100)
                : 0;

              return (
                <div
                  key={vol.id}
                  className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl overflow-hidden shadow-xs transition-all"
                >
                  {/* Cabeçalho do Volume (Clicável) */}
                  <button
                    onClick={() => toggleVolume(vol.id)}
                    className="w-full px-6 py-5 flex items-center justify-between text-left hover:bg-slate-50/70 dark:hover:bg-[#2e2315] transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-11 h-11 rounded-xl bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] font-extrabold text-sm flex items-center justify-center border border-[#FFB74D]/30 flex-shrink-0">
                        {String(vol.numero_volume).padStart(2, "0")}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h2 className="font-bold text-slate-900 dark:text-white text-base">
                            Vol. {vol.numero_volume}: {vol.titulo}
                          </h2>
                        </div>
                        <p className="text-xs text-slate-500 dark:text-[#A89F91] mt-0.5">
                          {totalCaps} {totalCaps === 1 ? "capítulo" : "capítulos"} • Duração estimada: {totalCaps * 50} min
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="hidden sm:inline-flex text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 dark:bg-[#1a1408] text-slate-600 dark:text-[#A89F91]">
                        {vol.grande_area.replace("_", " ").toUpperCase()}
                      </span>
                      {isExpanded ? (
                        <ChevronDown className="w-5 h-5 text-slate-400" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-slate-400" />
                      )}
                    </div>
                  </button>

                  {/* Lista Expandida de Capítulos */}
                  {isExpanded && (
                    <div className="border-t border-slate-100 dark:border-[#382b1c] px-6 py-4 bg-slate-50/50 dark:bg-[#20180e]">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {vol.capitulos?.map((cap: SkillTreeNode) => {
                          const statusColor = getStatusColor(cap.cor_heatmap);
                          const travado = !cap.desbloqueado;

                          return (
                            <Link
                              key={cap.id}
                              href={`/aula/${cap.id}`}
                              className={`group p-4 rounded-xl bg-white dark:bg-[#261d11] border ${
                                travado
                                  ? "border-slate-200/60 dark:border-[#2e2315] opacity-70"
                                  : "border-slate-200/80 dark:border-[#3d2f1f] hover:border-[#F57C00] dark:hover:border-[#FFB74D] hover:shadow-sm"
                              } transition-all flex items-start justify-between`}
                            >
                              <div className="flex items-start gap-3">
                                <div
                                  className={`w-3 h-3 rounded-full mt-1.5 flex-shrink-0 ${statusColor.bg} border ${statusColor.border}`}
                                />
                                <div>
                                  <div className="text-xs font-semibold text-slate-400 dark:text-slate-500">
                                    Capítulo {cap.numero_capitulo}
                                  </div>
                                  <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm group-hover:text-[#F57C00] transition-colors leading-snug mt-0.5">
                                    {cap.titulo}
                                  </h3>
                                  <div className="flex items-center gap-2 mt-2 text-[11px] text-slate-500 dark:text-[#A89F91]">
                                    <Clock className="w-3.5 h-3.5" />
                                    <span>{cap.tempo_estimado_min} min</span>
                                    {cap.percentual_acerto > 0 && (
                                      <span className="font-semibold">{Math.round(cap.percentual_acerto)}%</span>
                                    )}
                                  </div>
                                </div>
                              </div>

                              <div className="text-slate-300 dark:text-slate-600 group-hover:text-[#F57C00] transition-colors mt-1">
                                <PlayCircle className="w-5 h-5" />
                              </div>
                            </Link>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}

function getStatusColor(heatmap: string) {
  switch (heatmap) {
    case "green":
      return { bg: "bg-emerald-500", border: "border-emerald-600" };
    case "yellow":
      return { bg: "bg-amber-400", border: "border-amber-500" };
    case "red":
      return { bg: "bg-rose-500", border: "border-rose-600" };
    default:
      return { bg: "bg-slate-300 dark:bg-slate-600", border: "border-slate-400 dark:border-slate-500" };
  }
}
