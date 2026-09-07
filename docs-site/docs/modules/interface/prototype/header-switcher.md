---
title: Interface - Seletor Global de Disciplinas e Header
type: module
status: draft
related:
  - modules/interface/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 5. Seletor Global de Disciplinas e Header (`DisciplineSwitcher.tsx`)

Componente da barra de navegação superior com suporte a **Seletor Global de Matéria** (preparado para escalabilidade de Múltiplas Disciplinas) e menu de usuário.

---

## Código Fonte (`frontend/src/components/header/DisciplineSwitcher.tsx`)

```tsx
"use client";

import React, { useState } from "react";
import { ChevronDown, Check, Compass, LogOut, User } from "lucide-react";

export interface DisciplinaOption {
  id: string;
  slug: string;
  nome: string;
  nivel: string;
  ativa: boolean;
}

interface DisciplineSwitcherProps {
  disciplinasDisponiveis: DisciplinaOption[];
  disciplinaAtual: DisciplinaOption;
  onSelectDisciplina: (disc: DisciplinaOption) => void;
}

export const DisciplineSwitcher: React.FC<DisciplineSwitcherProps> = ({
  disciplinasDisponiveis,
  disciplinaAtual,
  onSelectDisciplina,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  // Se houver apenas 1 disciplina ativa (Lançamento: apenas Matemática), não abre dropdown
  const hasMultipleDisciplinas = disciplinasDisponiveis.filter((d) => d.ativa).length > 1;

  return (
    <div className="relative">
      <button
        onClick={() => hasMultipleDisciplinas && setIsOpen(!isOpen)}
        disabled={!hasMultipleDisciplinas}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all ${
          hasMultipleDisciplinas
            ? "bg-white dark:bg-neutral-800 border-neutral-300 dark:border-neutral-700 hover:border-orange-500 cursor-pointer shadow-sm"
            : "bg-orange-50 dark:bg-orange-950/40 border-orange-200 dark:border-orange-800/60 text-orange-700 dark:text-orange-300 cursor-default"
        }`}
      >
        <span className="text-base leading-none">📐</span>
        <span className="font-bold">{disciplinaAtual.nome}</span>
        <span className="text-[10px] px-1.5 py-0.5 rounded bg-orange-100 dark:bg-orange-900 text-orange-700 dark:text-orange-300 font-medium">
          {disciplinaAtual.nivel}
        </span>
        {hasMultipleDisciplinas && (
          <ChevronDown className="w-3.5 h-3.5 text-neutral-400" />
        )}
      </button>

      {/* Menu Suspenso de Disciplinas (Expansão Futura) */}
      {isOpen && hasMultipleDisciplinas && (
        <div className="absolute left-0 mt-2 w-56 rounded-2xl bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 shadow-xl p-2 z-50 animate-fade-in">
          <div className="text-[10px] font-bold uppercase tracking-wider text-neutral-400 px-2.5 py-1 mb-1">
            Disciplinas Disponíveis
          </div>
          {disciplinasDisponiveis
            .filter((d) => d.ativa)
            .map((d) => (
              <button
                key={d.id}
                onClick={() => {
                  onSelectDisciplina(d);
                  setIsOpen(false);
                }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
                  d.id === disciplinaAtual.id
                    ? "bg-orange-500 text-white font-semibold"
                    : "hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-700 dark:text-neutral-300"
                }`}
              >
                <span>{d.nome}</span>
                {d.id === disciplinaAtual.id && <Check className="w-4 h-4" />}
              </button>
            ))}
        </div>
      )}
    </div>
  );
};
```
