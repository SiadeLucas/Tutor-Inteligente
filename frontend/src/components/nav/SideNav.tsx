"use client";

/**
 * SideNav — navegação lateral fixa para desktop >= 1024px (RN-INT-007).
 *
 * Marca + identidade da disciplina (nome/ícone vindos do banco via
 * DisciplineThemeProvider) + navegação + sessão na base.
 * No mobile/tablet quem assume é a BottomNav + GlobalHeader compacto.
 */

import React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { BookOpen, Dumbbell, TrendingUp, LogOut } from "lucide-react";
import { api, clearAuth } from "@/lib/api";
import { useDisciplineTheme } from "@/components/theme/DisciplineThemeProvider";

const NAV_ITEMS = [
  { href: "/materias", label: "Matérias", icon: BookOpen, match: (p: string) => p.startsWith("/materias") || p.startsWith("/aula") },
  { href: "/reforco", label: "Praticar", icon: Dumbbell, match: (p: string) => p.startsWith("/reforco") || p.startsWith("/exercicios") },
  { href: "/progresso", label: "Progresso", icon: TrendingUp, match: (p: string) => p.startsWith("/progresso") },
] as const;

export function SideNav() {
  const pathname = usePathname() || "/";
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
    <aside
      className="fixed inset-y-0 left-0 z-40 hidden lg:flex w-64 flex-col border-r border-line bg-surface-card"
      aria-label="Navegação lateral"
    >
      {/* Marca */}
      <Link href="/materias" className="flex items-center gap-3 px-5 h-16 border-b border-line">
        <span className="flex items-center justify-center w-9 h-9 rounded-xl bg-subject-500 text-white font-black text-sm shadow-sm">
          TI
        </span>
        <span className="leading-tight">
          <span className="block text-sm font-bold text-ink-text tracking-tight">Tutor Inteligente</span>
          <span className="block text-[10px] font-medium uppercase tracking-widest text-ink-faint">
            Ensino Médio
          </span>
        </span>
      </Link>

      {/* Navegação primária */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const active = item.match(pathname);
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={active ? "page" : undefined}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
                active
                  ? "bg-subject-wash text-subject-700 dark:text-subject-400"
                  : "text-ink-muted hover:bg-surface-elevated hover:text-ink-text"
              }`}
            >
              <Icon className="w-5 h-5" aria-hidden="true" />
              {item.label}
              {active && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-subject-500" aria-hidden="true" />}
            </Link>
          );
        })}
      </nav>

      {/* Identidade da disciplina + sessão */}
      <div className="px-3 py-4 border-t border-line space-y-1">
        <div className="flex items-center gap-3 px-3 py-2 rounded-xl bg-surface-elevated">
          <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-subject-wash text-subject-600 dark:text-subject-400">
            <BookOpen className="w-4 h-4" aria-hidden="true" />
          </span>
          <span className="text-xs">
            <span className="block font-bold text-ink-text leading-tight">{nomeDisciplina}</span>
            <span className="block text-ink-faint leading-tight">Disciplina ativa</span>
          </span>
        </div>
        <button
          onClick={handleLogout}
          disabled={loggingOut}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold text-ink-muted hover:bg-rose-50 dark:hover:bg-rose-950/30 hover:text-rose-600 transition-colors cursor-pointer"
        >
          <LogOut className="w-5 h-5" aria-hidden="true" />
          {loggingOut ? "Saindo..." : "Sair"}
        </button>
      </div>
    </aside>
  );
}
