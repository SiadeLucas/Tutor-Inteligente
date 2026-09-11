"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  TrendingUp,
  Clock,
  CheckCircle2,
  Flame,
  FileDown,
  ArrowLeft,
  Award,
  Loader2,
} from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { api, getAccessToken, extrairMensagemErro } from "@/lib/api";
import {
  ProgressoGeralResponse,
  VolumeResumoItem,
  HeatmapVolumeResponse,
  HubAcaoTop3Response,
} from "@/types/progress";
import { ProgressRadarChart } from "@/components/progress/ProgressRadarChart";
import { TimelineTheta } from "@/components/progress/TimelineTheta";
import { HeatmapMatrix } from "@/components/progress/HeatmapMatrix";
import { TopCriticosHub } from "@/components/progress/TopCriticosHub";

export default function ProgressoPage() {
  useHeartbeat();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progresso, setProgresso] = useState<ProgressoGeralResponse | null>(null);
  const [volumes, setVolumes] = useState<VolumeResumoItem[]>([]);
  const [topCriticos, setTopCriticos] = useState<HubAcaoTop3Response | null>(null);
  const [selectedVolumeId, setSelectedVolumeId] = useState<string>("");
  const [selectedVolume, setSelectedVolume] = useState<HeatmapVolumeResponse | null>(null);
  const [loadingVolume, setLoadingVolume] = useState(false);
  const [baixandoPdf, setBaixandoPdf] = useState(false);

  // Carregar dados gerais do progresso
  useEffect(() => {
    async function carregarProgresso() {
      try {
        setLoading(true);
        setError(null);

        const [resGeral, resVolumes, resCriticos] = await Promise.all([
          api.get<ProgressoGeralResponse>("/api/v1/progresso/geral"),
          api.get<VolumeResumoItem[]>("/api/v1/progresso/volumes"),
          api.get<HubAcaoTop3Response>("/api/v1/progresso/top-criticos"),
        ]);

        setProgresso(resGeral);
        setVolumes(resVolumes);
        setTopCriticos(resCriticos);

        if (resVolumes && resVolumes.length > 0) {
          const primeiroVolId = resVolumes[0].volume_id;
          setSelectedVolumeId(primeiroVolId);
          await carregarHeatmapVolume(primeiroVolId);
        }
      } catch (err: any) {
        setError(extrairMensagemErro(err, "Não foi possível carregar os dados de progresso."));
      } finally {
        setLoading(false);
      }
    }

    carregarProgresso();
  }, []);

  // Carregar heatmap de um volume específico
  const carregarHeatmapVolume = async (volumeId: string) => {
    try {
      setLoadingVolume(true);
      const resHeatmap = await api.get<HeatmapVolumeResponse>(
        `/api/v1/progresso/heatmap/${volumeId}`
      );
      setSelectedVolume(resHeatmap);
    } catch (err: any) {
      console.error("Erro ao carregar heatmap do volume:", err);
    } finally {
      setLoadingVolume(false);
    }
  };

  const handleSelectVolume = (volumeId: string) => {
    setSelectedVolumeId(volumeId);
    carregarHeatmapVolume(volumeId);
  };

  // Download do Boletim Escolar em PDF
  const handleBaixarBoletim = async () => {
    try {
      setBaixandoPdf(true);
      const token = getAccessToken();
      const res = await fetch("/api/v1/progresso/boletim-pdf", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("Falha ao gerar o arquivo PDF.");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `Boletim_Proficiencia_${new Date().toISOString().split("T")[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert("Erro ao baixar o boletim escolar em PDF. Tente novamente.");
    } finally {
      setBaixandoPdf(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">
        <div className="flex-1 flex flex-col items-center justify-center p-6 space-y-4">
          <Loader2 className="w-8 h-8 animate-spin text-subject-600" />
          <p className="text-sm text-slate-500">Compilando analytics e histórico psicométrico...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Barra Superior de Ações & Navegação */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/80 dark:border-slate-800">
          <div className="flex items-center gap-3">
            <Link
              href="/materias"
              className="p-2 rounded-xl text-slate-500 hover:text-subject-600 hover:bg-white dark:hover:bg-slate-800 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 transition-colors shadow-sm"
              title="Voltar para Matérias"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-bold text-subject-600 uppercase tracking-wider">
                  Painel de Analytics & Evolução
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                Meu Progresso de Aprendizagem
              </h1>
            </div>
          </div>

          {/* Botão de Ação Primária: Baixar Boletim em PDF (RN-PRG-018) */}
          <button
            onClick={handleBaixarBoletim}
            disabled={baixandoPdf}
            className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-bold text-sm bg-subject-500 hover:bg-subject-600 text-white shadow-md hover:shadow-lg transition-all active:scale-[0.98] disabled:opacity-60"
          >
            {baixandoPdf ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Gerando PDF...</span>
              </>
            ) : (
              <>
                <FileDown className="w-4 h-4" />
                <span>Baixar Boletim em PDF</span>
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300 text-sm">
            {error}
          </div>
        )}

        {/* Resumo Executivo das 4 Métricas Tridimensionais */}
        {progresso && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Card 1: Theta TRI & Nível de Maestria */}
            <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Proficiência Geral (TRI &theta;)
                </span>
                <span className="p-2 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-600">
                  <TrendingUp className="w-4 h-4" />
                </span>
              </div>
              <div className="mt-3">
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl sm:text-3xl font-mono font-black text-slate-900 dark:text-white">
                    {progresso.theta_atual >= 0 ? `+${progresso.theta_atual.toFixed(2)}` : progresso.theta_atual.toFixed(2)}
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    &plusmn;{progresso.erro_padrao_se.toFixed(2)} SE
                  </span>
                </div>
                <div className="mt-2 flex items-center gap-1.5">
                  <Award className="w-3.5 h-3.5 text-subject-600" />
                  <span className="text-xs font-bold text-subject-700 dark:text-subject-300">
                    Nível {progresso.classificacao_nivel}
                  </span>
                </div>
              </div>
            </div>

            {/* Card 2: Tempo Líquido Ativo */}
            <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Tempo Líquido Ativo
                </span>
                <span className="p-2 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400">
                  <Clock className="w-4 h-4" />
                </span>
              </div>
              <div className="mt-3">
                <div className="flex items-baseline gap-1.5">
                  <span className="text-2xl sm:text-3xl font-mono font-black text-slate-900 dark:text-white">
                    {progresso.horas_estudo_liquidas_total.toFixed(1)}
                  </span>
                  <span className="text-sm font-semibold text-slate-500">horas</span>
                </div>
                <p className="mt-2 text-[11px] text-slate-400">
                  Excluindo inatividades superiores a 3 min
                </p>
              </div>
            </div>

            {/* Card 3: Completude Curricular Global */}
            <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Completude Curricular
                </span>
                <span className="p-2 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400">
                  <CheckCircle2 className="w-4 h-4" />
                </span>
              </div>
              <div className="mt-3">
                <div className="flex items-baseline gap-1.5">
                  <span className="text-2xl sm:text-3xl font-mono font-black text-slate-900 dark:text-white">
                    {progresso.completude_global_percentual.toFixed(1)}%
                  </span>
                  <span className="text-xs font-medium text-slate-400">
                    ({progresso.aulas_concluidas_count} capítulos)
                  </span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                    style={{ width: `${progresso.completude_global_percentual}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Card 4: Sequência Ativa (Streak) */}
            <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Sequência Ativa (Streak)
                </span>
                <span className="p-2 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-600 dark:text-subject-400">
                  <Flame className="w-4 h-4" />
                </span>
              </div>
              <div className="mt-3">
                <div className="flex items-baseline gap-1.5">
                  <span className="text-2xl sm:text-3xl font-mono font-black text-slate-900 dark:text-white">
                    {progresso.streak_dias_consecutivos}
                  </span>
                  <span className="text-sm font-semibold text-slate-500">
                    {progresso.streak_dias_consecutivos === 1 ? "dia ativo" : "dias ativos"}
                  </span>
                </div>
                <p className="mt-2 text-[11px] text-subject-600 dark:text-subject-400 font-medium">
                  {progresso.streak_dias_consecutivos > 0
                    ? "Mantenha o foco diário de 50 minutos!"
                    : "Comece uma aula hoje para iniciar seu streak!"}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Gráficos Principais: Radar Multiaxial e Linha do Tempo lado a lado */}
        {progresso && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ProgressRadarChart
              radarAreas={progresso.radar_areas}
              thetaAtual={progresso.theta_atual}
              classificacao={progresso.classificacao_nivel}
            />

            <TimelineTheta
              timeline={progresso.timeline}
              thetaAtual={progresso.theta_atual}
            />
          </div>
        )}

        {/* Hub de Ação: Top 3 Gargalos Críticos de Aprendizagem */}
        {topCriticos && (
          <TopCriticosHub
            topCriticos={topCriticos.top_criticos}
            temPendencias={topCriticos.tem_pendencias_criticas}
          />
        )}

        {/* Matriz Interativa do Heatmap de Domínio dos 11 Volumes */}
        <HeatmapMatrix
          volumes={volumes}
          selectedVolume={selectedVolume}
          selectedVolumeId={selectedVolumeId}
          onSelectVolume={handleSelectVolume}
          isLoadingVolume={loadingVolume}
        />
      </main>
    </div>
  );
}
