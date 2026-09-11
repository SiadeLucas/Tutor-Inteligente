"use client";

/**
 * GlobalHeader — barra superior compacta (RN-INT-007 revisada).
 *
 * Mobile/tablet: fixa no topo (h-14), com marca compacta, badge da disciplina
 * (nome/ícone vindos do banco via DisciplineThemeProvider), presença e logout.
 * Desktop: permanece como barra fina sticky (a marca completa vive na SideNav).
 */

import React from "react";
import { useRouter } from "next/navigation";
import { LogOut, User, BookOpen } from "lucide-react";
import { api, clearAuth } from "@/lib/api";
import { useDisciplineTheme } from "@/components/theme/DisciplineThemeProvider";

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
  const { disciplina } = useDisciplineTheme();
  const [loggingOut, setLoggingOut] = React.useState(false);

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

  const nomeDisciplina = disciplina?.nome ?? "Matemática";

  return (
    <header className="sticky top-0 z-30 border-b border-line bg-surface-card/95 backdrop-blur supports-[backdrop-filter]:bg-surface-card/85">
      <div className="h-14 flex items-center justify-between gap-3 px-4 sm:px-6">
        {/* Marca compacta (a marca completa vive na SideNav em desktop) */}
        <div className="flex items-center gap-3 min-w-0">
          {userRole === "teacher" ? (
            <a href="/teacher" className="flex items-center gap-2.5 min-w-0">
              <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-subject-500 text-white font-black text-xs shadow-sm flex-shrink-0">
                TI
              </span>
              <span className="hidden sm:block text-sm font-bold text-ink-text tracking-tight truncate">
                Painel do Docente
              </span>
            </a>
          ) : (
            <a href="/materias" className="flex items-center gap-2.5 min-w-0">
              <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-subject-500 text-white font-black text-xs shadow-sm flex-shrink-0">
                TI
              </span>
              <span className="hidden sm:block text-sm font-bold text-ink-text tracking-tight truncate">
                Tutor Inteligente
              </span>
            </a>
          )}

          {/* RN-INT-019: badge da disciplina — nome/ícone do banco (cor só no tema) */}
          {showDisciplineBadge && (
            <span className="hidden sm:inline-flex items-center gap-1.5 pl-2.5 ml-1 border-l border-line text-xs font-semibold text-ink-muted">
              <BookOpen className="w-3.5 h-3.5 text-subject-600 dark:text-subject-400" aria-hidden="true" />
              <span className="truncate max-w-[160px]">{nomeDisciplina}</span>
            </span>
          )}
        </div>

        {/* Direita: presença, perfil, logout */}
        <div className="flex items-center gap-2 sm:gap-3">
          <span
            title="Sessão única monitorada via Redis (Heartbeat 30s)"
            className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true" />
            Presença Ativa
          </span>

          <span
            title={userName}
            className="flex items-center justify-center w-8 h-8 rounded-full bg-surface-elevated border border-line text-ink-muted"
          >
            <User className="w-4 h-4" aria-hidden="true" />
          </span>

          <button
            onClick={handleLogout}
            disabled={loggingOut}
            title="Encerrar sessão"
            aria-label="Encerrar sessão"
            className="inline-flex items-center justify-center w-9 h-9 rounded-lg text-ink-muted hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors cursor-pointer"
          >
            <LogOut className="w-4 h-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </header>
  );
}
