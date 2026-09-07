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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-white dark:bg-slate-900 border border-amber-300 dark:border-amber-600/50 rounded-2xl shadow-2xl max-w-md w-full p-6 text-center">
        <div className="mx-auto w-14 h-14 bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 rounded-full flex items-center justify-center mb-4 ring-8 ring-amber-50 dark:ring-amber-950/30">
          <ShieldAlert className="w-8 h-8" />
        </div>

        <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
          Sessão Conectada em Outro Dispositivo
        </h3>

        <p className="text-sm text-slate-600 dark:text-slate-300 mb-6 leading-relaxed">
          {details?.mensagem ||
            "Sua conta foi conectada em outro dispositivo. Por questões de segurança, cada estudante pode ter apenas uma sessão ativa por vez."}
        </p>

        <div className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-3 mb-6 text-xs text-slate-500 dark:text-slate-400 flex items-center justify-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
          <span>Se você não reconhece esta atividade, redefina sua senha imediatamente.</span>
        </div>

        <button
          onClick={handleRedirect}
          className="w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-medium shadow-lg shadow-indigo-600/20 transition-colors"
        >
          <LogIn className="w-4 h-4" />
          Fazer Login Novamente
        </button>
      </div>
    </div>
  );
}
