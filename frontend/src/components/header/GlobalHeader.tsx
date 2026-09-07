"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { BookOpen, LogOut, Sparkles, User, ShieldCheck } from "lucide-react";
import { api, clearAuth } from "@/lib/api";

interface GlobalHeaderProps {
  userRole?: "student" | "teacher" | "admin";
  userName?: string;
  showDisciplineBadge?: boolean;
}

export function GlobalHeader({
  userRole = "student",
  userName = "Aluno",
  showDisciplineBadge = true,
}: GlobalHeaderProps) {
  const router = useRouter();
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await api.post("/api/v1/auth/logout");
    } catch {
      // Ignora erro de rede para assegurar limpeza local
    } finally {
      clearAuth();
      router.push("/login");
    }
  };

  return (
    <header className="w-full bg-white dark:bg-[#1a1408] border-b border-slate-200 dark:border-[#382b1c] sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Lado Esquerdo: Logo institucional e Disciplina */}
        <div className="flex items-center gap-4 sm:gap-6">
          <Link href={userRole === "teacher" ? "/teacher" : "/materias"} className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-[#F57C00] flex items-center justify-center text-white font-bold shadow-sm group-hover:bg-[#EF6C00] transition-colors">
              <span className="text-sm tracking-tight font-black">TI</span>
            </div>
            <div className="hidden sm:block">
              <span className="text-base font-bold text-slate-900 dark:text-slate-100 tracking-tight leading-none block">
                Tutor Inteligente
              </span>
              <span className="text-[11px] text-slate-500 dark:text-[#A89F91] leading-none block mt-0.5">
                {userRole === "teacher" ? "Painel do Docente" : "Ensino Médio • Iezzi"}
              </span>
            </div>
          </Link>

          {/* RN-INT-019: Seletor Global de Disciplina (Badge Elegante no Lançamento) */}
          {showDisciplineBadge && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] border border-[#FFB74D]/40">
              <span>📐</span>
              <span className="font-medium">Matemática (Ensino Médio)</span>
            </div>
          )}
        </div>

        {/* Lado Direito: Status de Presença (Heartbeat), Perfil e Logout */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* Indicador de Heartbeat Ativo */}
          <div
            title="Sessão única monitorada via Redis (Heartbeat 30s)"
            className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Presença Ativa</span>
          </div>

          {/* Identificação de Perfil */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-[#382b1c]">
            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-[#2a1f12] border border-slate-200 dark:border-[#3d2f1f] flex items-center justify-center text-slate-600 dark:text-[#FFCC80]">
              <User className="w-4 h-4" />
            </div>
            <div className="hidden lg:block text-left">
              <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block leading-tight">
                {userName}
              </span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 uppercase tracking-wider block">
                {userRole === "teacher" ? "Professor" : "Estudante"}
              </span>
            </div>
          </div>

          {/* Botão de Logout */}
          <button
            onClick={handleLogout}
            disabled={loggingOut}
            title="Encerrar sessão"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 border border-slate-200 dark:border-[#382b1c] transition-colors cursor-pointer"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{loggingOut ? "Saindo..." : "Sair"}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
