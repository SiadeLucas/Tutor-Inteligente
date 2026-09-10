"use client";

import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { TimelineThetaItem } from "@/types/progress";

interface TimelineThetaProps {
  timeline: TimelineThetaItem[];
  thetaAtual: number;
}

export function TimelineTheta({ timeline, thetaAtual }: TimelineThetaProps) {
  // Se houver poucos dados históricos, garante visualização com ponto atual
  const dadosGrafico =
    timeline && timeline.length > 0
      ? timeline.map((item, index) => ({
          idx: index + 1,
          data: item.data || `Registro ${index + 1}`,
          theta: Number(item.theta_estimado.toFixed(2)),
          origem: item.origem_ajuste,
        }))
      : [
          {
            idx: 1,
            data: "Entrada",
            theta: Number(thetaAtual.toFixed(2)),
            origem: "Diagnóstico",
          },
        ];

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h3 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
            Evolução Temporal da Proficiência (&theta;)
          </h3>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
            Série histórica da calibração psicométrica contínua na Teoria de Resposta ao Item
          </p>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#F57C00]" />
            <span className="text-slate-600 dark:text-slate-300">Proficiência (&theta;)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-4 h-0.5 border-t border-dashed border-emerald-500" />
            <span className="text-emerald-600 dark:text-emerald-400 font-semibold">Meta Avançado (+1.0)</span>
          </div>
        </div>
      </div>

      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={dadosGrafico}
            margin={{ top: 15, right: 20, left: -10, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:stroke-slate-800" />
            <XAxis
              dataKey="data"
              tick={{ fill: "#64748b", fontSize: 10 }}
              interval="preserveStartEnd"
            />
            <YAxis
              domain={[-3.0, 3.0]}
              ticks={[-3, -2, -1, -0.5, 0, 1, 2, 3]}
              tick={{ fill: "#64748b", fontSize: 10 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const item = payload[0].payload;
                  return (
                    <div className="bg-slate-900 text-white text-xs p-3 rounded-xl shadow-xl border border-slate-700 space-y-1">
                      <p className="font-bold text-amber-400">{item.data}</p>
                      <p>
                        Proficiência (&theta;):{" "}
                        <span className="font-mono font-bold">
                          {item.theta >= 0 ? `+${item.theta}` : item.theta}
                        </span>
                      </p>
                      <p className="text-slate-400 text-[10px]">
                        Origem: {item.origem.replace(/_/g, " ")}
                      </p>
                    </div>
                  );
                }
                return null;
              }}
            />
            {/* Linha de referência da meta do nível Avançado (RN-PRG-014) */}
            <ReferenceLine
              y={1.0}
              stroke="#10b981"
              strokeDasharray="4 4"
              strokeWidth={1.5}
              label={{
                value: "Nível Avançado (+1.0)",
                fill: "#10b981",
                fontSize: 10,
                position: "insideTopRight",
              }}
            />
            {/* Linha de referência do nível Intermediário */}
            <ReferenceLine
              y={-0.5}
              stroke="#f59e0b"
              strokeDasharray="3 3"
              strokeWidth={1}
              label={{
                value: "Intermediário (-0.5)",
                fill: "#f59e0b",
                fontSize: 9,
                position: "insideBottomRight",
              }}
            />
            <Line
              type="monotone"
              dataKey="theta"
              stroke="#F57C00"
              strokeWidth={2.5}
              dot={{ r: 4, fill: "#F57C00" }}
              activeDot={{ r: 6, fill: "#E65100" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
