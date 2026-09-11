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
} from "recharts";

interface CatRadarChartProps {
  scores: Record<string, number>;
  thetaFinal: number;
  classificacao?: string;
}

const LABELS_AREAS: Record<string, string> = {
  algebra_funcoes: "Álgebra & Funções",
  geometria: "Geometria",
  combinatoria_probabilidade: "Combinatória & Probabilidade",
  matematica_financeira: "Matemática Financeira",
  algebra_linear: "Álgebra Linear & Matrizes",
  aplicada: "Matemática Aplicada",
};

export function CatRadarChart({
  scores,
  thetaFinal,
  classificacao = "Intermediário",
}: CatRadarChartProps) {
  // RN-INT-001: cor da disciplina vem do tema (fonte da verdade no banco)
  const { palette } = useDisciplineTheme();
  const subjectColor = palette?.scale[500] ?? "#F57C00";

  // Converte a escala theta (-3 a +3) para uma pontuação percentual pedagógica (0 a 100)
  // formula: pontuacao = ((theta + 3) / 6) * 100
  const data = Object.entries(scores).map(([areaKey, thetaVal]) => {
    const pontuacao = Math.round(((Math.min(Math.max(thetaVal, -3), 3) + 3) / 6) * 100);
    return {
      area: LABELS_AREAS[areaKey] || areaKey,
      theta: Number(thetaVal.toFixed(2)),
      pontuacao: pontuacao,
    };
  });

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col items-center">
      <div className="text-center mb-4">
        <span className="inline-block px-3 py-1 bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 font-semibold text-xs rounded-full uppercase tracking-wider mb-2">
          Classificação: {classificacao} (θ = {thetaFinal.toFixed(2)})
        </span>
        <h3 className="text-xl font-bold text-slate-900 dark:text-white">
          Polígono Diagnóstico de Competências
        </h3>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Nível relativo estimado pelo modelo psicométrico TRI em cada Grande Área
        </p>
      </div>

      <div className="w-full h-80 max-w-md">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
            <PolarGrid stroke="#e2e8f0" className="dark:stroke-slate-700" />
            <PolarAngleAxis
              dataKey="area"
              tick={{ fill: "#64748b", fontSize: 11, fontWeight: 500 }}
            />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 100]}
              tick={{ fill: "#94a3b8", fontSize: 10 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const item = payload[0].payload;
                  return (
                    <div className="bg-slate-900 text-white text-xs p-3 rounded-xl shadow-lg border border-slate-700">
                      <p className="font-bold text-amber-400">{item.area}</p>
                      <p className="mt-1">Proficiência (θ): <span className="font-mono">{item.theta}</span></p>
                      <p>Domínio Relativo: <span className="font-mono">{item.pontuacao}%</span></p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Radar
              name="Proficiência"
              dataKey="pontuacao"
              stroke={subjectColor}
              fill={subjectColor}
              fillOpacity={0.45}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-3 w-full max-w-md mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 text-xs">
        {data.map((item) => (
          <div
            key={item.area}
            className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/50"
          >
            <span className="text-slate-600 dark:text-slate-400 font-medium truncate max-w-[130px]">
              {item.area}
            </span>
            <span className="font-mono font-bold text-amber-600 dark:text-amber-400">
              θ {item.theta >= 0 ? `+${item.theta}` : item.theta}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
