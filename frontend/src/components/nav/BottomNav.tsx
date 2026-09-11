"use client";

/**
 * BottomNav — navegação primária mobile-first (RN-INT-007 revisada).
 *
 * No mobile o hamburger é onde apps de educação morrem: a navegação primária
 * vive em uma tab bar fixa na base, dentro da zona do polegar, com touch
 * targets >= 48px (RN-INT-009). Tablet/desktop usam a SideNav.
 *
 * Cores: 100% tokens (subject/ink/surface/line) — RN-INT-001 revisada.
 */

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Dumbbell, TrendingUp, User } from "lucide-react";

const NAV_ITEMS = [
  { href: "/materias", label: "Matérias", icon: BookOpen, match: (p: string) => p.startsWith("/materias") || p.startsWith("/aula") },
  { href: "/reforco", label: "Praticar", icon: Dumbbell, match: (p: string) => p.startsWith("/reforco") || p.startsWith("/exercicios") },
  { href: "/progresso", label: "Progresso", icon: TrendingUp, match: (p: string) => p.startsWith("/progresso") },
  { href: "/perfil", label: "Perfil", icon: User, match: (p: string) => p.startsWith("/perfil") },
] as const;

export function BottomNav() {
  const pathname = usePathname() || "/";

  return (
    <nav
      aria-label="Navegação principal"
      className="fixed inset-x-0 bottom-0 z-40 lg:hidden border-t border-line bg-surface-card/95 backdrop-blur supports-[backdrop-filter]:bg-surface-card/85"
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
    >
      <div className="mx-auto max-w-md grid grid-cols-4">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const active = item.match(pathname);
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={active ? "page" : undefined}
              className={`flex flex-col items-center justify-center gap-0.5 min-h-[56px] pt-1.5 pb-2 text-[10px] font-semibold transition-colors ${
                active ? "text-subject-600 dark:text-subject-400" : "text-ink-faint hover:text-ink-muted"
              }`}
            >
              <span
                className={`flex items-center justify-center w-11 h-7 rounded-full transition-colors ${
                  active ? "bg-subject-wash" : ""
                }`}
              >
                <Icon className="w-5 h-5" strokeWidth={active ? 2.4 : 2} aria-hidden="true" />
              </span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
