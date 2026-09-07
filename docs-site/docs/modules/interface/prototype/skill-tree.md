---
title: Interface - Árvore de Habilidades Visual (Skill Tree)
type: module
status: draft
related:
  - modules/interface/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Árvore de Habilidades Visual (`SkillTree.tsx`)

Componente interativo em **React e Tailwind CSS** que renderiza o mapa de competências dos **11 volumes da coleção Gelson Iezzi** em formato de árvore de habilidades (*Skill Tree*), com conexões em SVG e regras estritas de bloqueio comercial (*Zero Degustação*).

---

## Código Fonte (`frontend/src/components/tree/SkillTree.tsx`)

```tsx
"use client";

import React from "react";
import { Lock, CheckCircle2, PlayCircle, BookOpen } from "lucide-react";

export interface NodeVolume {
  id: string;
  numero: number;
  titulo: string;
  grande_area: string;
  status: "bloqueado" | "liberado" | "concluido";
  taxa_dominio_percentual: number;
  capitulos_concluidos: number;
  capitulos_total: number;
  preco_volume: number;
}

interface SkillTreeProps {
  volumes: NodeVolume[];
  onSelectVolume: (volume: NodeVolume) => void;
  onOpenCheckout: (volume: NodeVolume) => void;
}

export const SkillTree: React.FC<SkillTreeProps> = ({
  volumes,
  onSelectVolume,
  onOpenCheckout,
}) => {
  return (
    <div className="relative w-full max-w-5xl mx-auto py-12 px-4 flex flex-col items-center gap-12">
      {/* Camada de Linhas Conectoras em SVG de Fundo */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none stroke-neutral-300 dark:stroke-neutral-700 stroke-2 stroke-dashed">
        <line x1="50%" y1="60" x2="50%" y2="100%" />
      </svg>

      {volumes.map((vol, index) => {
        const isBloqueado = vol.status === "bloqueado";
        const isConcluido = vol.status === "concluido";

        return (
          <div
            key={vol.id}
            className={`relative z-10 w-full max-w-md p-5 rounded-2xl border transition-all duration-300 backdrop-blur-md ${
              isBloqueado
                ? "bg-neutral-100/80 dark:bg-neutral-900/80 border-neutral-300 dark:border-neutral-800 opacity-90"
                : isConcluido
                ? "bg-amber-50/90 dark:bg-amber-950/40 border-amber-400 dark:border-amber-600 shadow-lg shadow-amber-500/10"
                : "bg-white/95 dark:bg-neutral-900/95 border-orange-500 shadow-xl shadow-orange-500/15 hover:-translate-y-1"
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <div
                  className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg ${
                    isBloqueado
                      ? "bg-neutral-200 dark:bg-neutral-800 text-neutral-500"
                      : isConcluido
                      ? "bg-emerald-500 text-white"
                      : "bg-orange-500 text-white shadow-md shadow-orange-500/30"
                  }`}
                >
                  {isConcluido ? (
                    <CheckCircle2 className="w-6 h-6 text-white" />
                  ) : isBloqueado ? (
                    <Lock className="w-5 h-5 text-neutral-500" />
                  ) : (
                    vol.numero
                  )}
                </div>

                <div>
                  <span className="text-xs font-semibold tracking-wider uppercase text-orange-600 dark:text-orange-400">
                    Volume {vol.numero} • {vol.grande_area}
                  </span>
                  <h3 className="font-bold text-lg text-neutral-900 dark:text-neutral-50">
                    {vol.titulo}
                  </h3>
                </div>
              </div>

              {/* Tag de Domínio ou Preço */}
              <div>
                {isBloqueado ? (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300">
                    R$ {vol.preco_volume.toFixed(2)}
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-orange-100 dark:bg-orange-950/60 text-orange-700 dark:text-orange-300">
                    {vol.taxa_dominio_percentual.toFixed(0)}% Domínio
                  </span>
                )}
              </div>
            </div>

            {/* Barra de Progresso do Volume */}
            {!isBloqueado && (
              <div className="mt-4">
                <div className="flex justify-between text-xs text-neutral-500 dark:text-neutral-400 mb-1">
                  <span>Capítulos Concluídos</span>
                  <span>
                    {vol.capitulos_concluidos} de {vol.capitulos_total}
                  </span>
                </div>
                <div className="w-full h-2 bg-neutral-200 dark:bg-neutral-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-orange-500 rounded-full transition-all duration-500"
                    style={{
                      width: `${(vol.capitulos_concluidos / vol.capitulos_total) * 100}%`,
                    }}
                  />
                </div>
              </div>
            )}

            {/* Botão de Ação Direta */}
            <div className="mt-5 flex gap-2">
              {isBloqueado ? (
                <button
                  onClick={() => onOpenCheckout(vol)}
                  className="w-full py-2.5 px-4 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-sm transition-colors flex items-center justify-center gap-2 shadow-sm"
                >
                  <Lock className="w-4 h-4" /> Desbloquear Volume
                </button>
              ) : (
                <button
                  onClick={() => onSelectVolume(vol)}
                  className="w-full py-2.5 px-4 rounded-xl bg-neutral-900 hover:bg-black dark:bg-neutral-800 dark:hover:bg-neutral-700 text-white font-semibold text-sm transition-colors flex items-center justify-center gap-2"
                >
                  <PlayCircle className="w-4 h-4 text-orange-400" /> Acessar Capítulos
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
```
