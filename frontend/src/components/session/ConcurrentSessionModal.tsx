"use client";

import React, { useState, useEffect } from "react";
import { AlertTriangle, LogIn, ShieldAlert } from "lucide-react";
import { setAccessToken } from "@/lib/api";

export function ConcurrentSessionModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [details, setDetails] = useState<any>(null);

  useEffect(() => {
    const handleConflict = (event: any) => {
      setDetails(event.detail);
      setIsOpen(true);
      // Limpa token de acesso local para impedir requisições subsequentes
      setAccessToken(null);
    };

    window.addEventListener("session_conflict", handleConflict);
    return () => window.removeEventListener("session_conflict", handleConflict);
  }, []);

  if (!isOpen) return null;

  const handleRedirect = () => {
    window.location.href = "/login?sessao_revogada=true";
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-white dark:bg-surface-bg border border-slate-200 dark:border-line rounded-2xl shadow-xl max-w-md w-full p-6 text-center">
        <div className="mx-auto w-14 h-14 bg-subject-100 dark:bg-subject-wash text-subject-600 rounded-full flex items-center justify-center mb-4 ring-8 ring-subject-200 dark:ring-subject-wash-strong">
          <ShieldAlert className="w-7 h-7" />
        </div>

        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
          Sessão Conectada em Outro Aparelho
        </h3>

        <p className="text-sm text-slate-600 dark:text-ink-muted mb-5 leading-relaxed">
          {details?.mensagem ||
            "Sua conta foi acessada em outro dispositivo. Para garantir a segurança dos seus dados pedagógicos e avaliações, apenas uma conexão simultânea é permitida."}
        </p>

        <div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 rounded-xl p-3 mb-6 text-xs text-amber-800 dark:text-amber-300 flex items-center gap-2 text-left">
          <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <span>Se você não reconhece esta atividade, recomendamos redefinir sua senha imediatamente.</span>
        </div>

        <button
          onClick={handleRedirect}
          className="w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-medium text-sm shadow-sm transition-colors cursor-pointer"
        >
          <LogIn className="w-4 h-4" />
          Fazer Login Novamente
        </button>
      </div>
    </div>
  );
}
