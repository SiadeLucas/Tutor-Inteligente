"use client";

import React from "react";
import { useDisciplineTheme } from "@/components/theme/DisciplineThemeProvider";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";
import { RadarAreaItem } from "@/types/progress";

interface ProgressRadarChartProps {
  radarAreas: RadarAreaItem[];
  thetaAtual: number;
  classificacao: string;
}

export function ProgressRadarChart({
  radarAreas,
  thetaAtual,
  classificacao,
}: ProgressRadarChartProps) {
  // RN-INT-001: cor da disciplina vem do tema (fonte da verdade no banco)
  const { palette } = useDisciplineTheme();
  const subjectColor = palette?.scale[500] ?? "#F57C00";

  // Converte a escala psicométrica (-3.0 a +3.0) em pontuação percentual pedagógica (0 a 100)
  const data = radarAreas.map((item) => {
    const pontuacaoEntrada = Math.round(
      ((Math.min(Math.max(item.score_entrada_cat, -3), 3) + 3) / 6) * 100
    );
    const pontuacaoAtual = Math.round(
      ((Math.min(Math.max(item.score_atual, -3), 3) + 3) / 6) * 100
    );

    return {
      area: item.area,
      slug: item.slug_area,
      entrada: pontuacaoEntrada,
      atual: pontuacaoAtual,
      thetaEntrada: item.score_entrada_cat,
      thetaAtual: item.score_atual,
    };
  });

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col items-center">
      <div className="text-center mb-3">
        <div className="flex items-center justify-center gap-2 mb-1.5">
          <span className="inline-block px-3 py-1 bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 font-semibold text-xs rounded-full uppercase tracking-wider">
            Nível: {classificacao} (&theta; = {thetaAtual >= 0 ? `+${thetaAtual.toFixed(2)}` : thetaAtual.toFixed(2)})
          </span>
        </div>
        <h3 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
          Gráfico Radar Multiaxial
        </h3>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
          Comparativo entre o Diagnóstico Inicial (CAT) e a Proficiência Atual
        </p>
      </div>

      <div className="w-full h-80 max-w-md">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="72%" data={data}>
            <PolarGrid stroke="#cbd5e1" className="dark:stroke-slate-700" />
            <PolarAngleAxis
              dataKey="area"
              tick={{ fill: "#64748b", fontSize: 11, fontWeight: 600 }}
            />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 100]}
              tick={{ fill: "#94a3b8", fontSize: 9 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const item = payload[0].payload;
                  return (
                    <div className="bg-slate-900 text-white text-xs p-3 rounded-xl shadow-xl border border-slate-700 space-y-1">
                      <p className="font-bold text-amber-400 text-sm">{item.area}</p>
                      <div className="flex items-center justify-between gap-4">
                        <span className="text-slate-400">Diagnóstico Inicial:</span>
                        <span className="font-mono font-semibold">
                          &theta; {item.thetaEntrada >= 0 ? `+${item.thetaEntrada.toFixed(2)}` : item.thetaEntrada.toFixed(2)} ({item.entrada}%)
                        </span>
                      </div>
                      <div className="flex items-center justify-between gap-4">
                        <span className="text-amber-300">Proficiência Atual:</span>
                        <span className="font-mono font-bold text-amber-400">
                          &theta; {item.thetaAtual >= 0 ? `+${item.thetaAtual.toFixed(2)}` : item.thetaAtual.toFixed(2)} ({item.atual}%)
                        </span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: 12, paddingTop: 8 }}
              formatter={(value) => <span className="text-slate-600 dark:text-slate-300">{value}</span>}
            />
            <Radar
              name="Diagnóstico Entrada"
              dataKey="entrada"
              stroke="#94a3b8"
              strokeDasharray="4 4"
              fill="#94a3b8"
              fillOpacity={0.2}
            />
            <Radar
              name="Proficiência Atual"
              dataKey="atual"
              stroke={subjectColor}
              strokeWidth={2}
              fill={subjectColor}
              fillOpacity={0.45}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-2.5 w-full max-w-md mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
        {data.map((item) => {
          const delta = item.thetaAtual - item.thetaEntrada;
          const deltaColor = delta >= 0 ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400";
          return (
            <div
              key={item.slug}
              className="flex items-center justify-between p-2 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800"
            >
              <span className="text-slate-600 dark:text-slate-400 font-medium truncate max-w-[110px]" title={item.area}>
                {item.area}
              </span>
              <div className="text-right font-mono">
                <span className="font-bold text-amber-600 dark:text-amber-400">
                  {item.thetaAtual >= 0 ? `+${item.thetaAtual.toFixed(2)}` : item.thetaAtual.toFixed(2)}
                </span>
                <span className={`text-[10px] ml-1.5 font-bold ${deltaColor}`}>
                  ({delta >= 0 ? `+${delta.toFixed(2)}` : delta.toFixed(2)})
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
