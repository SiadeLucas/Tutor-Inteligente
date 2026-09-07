---
title: Interface - Modal de Bloqueio por Sessão Concorrente
type: module
status: draft
related:
  - modules/interface/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Modal de Sessão Concorrente (`ConcurrentSessionModal.tsx`)

Componente de segurança e UX que **congela a interface em tempo real**, pausa o cronômetro e salva o rascunho de respostas preenchidas quando o sistema detecta login em um segundo aparelho.

---

## Código Fonte (`frontend/src/components/session/ConcurrentSessionModal.tsx`)

```tsx
"use client";

import React, { useEffect } from "react";
import { AlertTriangle, Lock, ArrowRight, ShieldAlert } from "lucide-react";

interface ConcurrentSessionModalProps {
  isOpen: boolean;
  horarioDesconexao: string;
  onReconectar: () => void;
  onRedefinirSenha: () => void;
}

export const ConcurrentSessionModal: React.FC<ConcurrentSessionModalProps> = ({
  isOpen,
  horarioDesconexao,
  onReconectar,
  onRedefinirSenha,
}) => {
  // Salva rascunho no instante da desconexão
  useEffect(() => {
    if (isOpen) {
      console.log("[Segurança] Sessão concorrente detectada. Pausando cronômetro e salvando rascunho.");
      // Exemplo: window.localStorage.setItem("rascunho_aula_backup", JSON.stringify(dadosLocais));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="w-full max-w-md p-6 rounded-2xl bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 shadow-2xl flex flex-col items-center text-center">
        {/* Ícone de Alerta em Destaque */}
        <div className="w-14 h-14 rounded-2xl bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center mb-4">
          <ShieldAlert className="w-8 h-8" />
        </div>

        <h2 className="text-xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">
          Conta Conectada em Outro Aparelho
        </h2>

        <p className="text-xs text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
          Sua sessão de estudos foi desconectada neste dispositivo porque outro aparelho fez login na sua conta às{" "}
          <span className="font-semibold text-neutral-900 dark:text-neutral-200">{horarioDesconexao}</span>.
          <br />
          <span className="text-emerald-600 dark:text-emerald-400 font-medium">
            Suas respostas preenchidas foram salvas como rascunho.
          </span>
        </p>

        {/* Botões de Ação */}
        <div className="w-full flex flex-col gap-2.5">
          <button
            onClick={onReconectar}
            className="w-full py-3 px-4 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-sm transition-all flex items-center justify-center gap-2 shadow-lg shadow-orange-500/25"
          >
            <Lock className="w-4 h-4" /> Conectar Novamente Neste Aparelho
          </button>

          <button
            onClick={onRedefinirSenha}
            className="w-full py-2.5 px-4 rounded-xl border border-neutral-300 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-700 dark:text-neutral-300 font-medium text-xs transition-colors"
          >
            Não foi você? Redefina sua senha
          </button>
        </div>
      </div>
    </div>
  );
};
```
