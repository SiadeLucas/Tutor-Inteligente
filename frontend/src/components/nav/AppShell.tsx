"use client";

/**
 * AppShell — casca única de navegação (RN-INT-007 revisada).
 *
 * Desktop (>=1024px): SideNav fixa 256px + conteúdo deslocado.
 * Mobile/tablet: GlobalHeader compacto fixo no topo + BottomNav na base.
 * Focus-mode (/exercicios, /onboarding/cat): sem navegação primária
 * (docs: "Tela dedicada e focada (sem sidebar)").
 */

import React from "react";
import { usePathname } from "next/navigation";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { SideNav } from "@/components/nav/SideNav";
import { BottomNav } from "@/components/nav/BottomNav";
import { useCurrentUser } from "@/hooks/useCurrentUser";

/** Rotas em modo foco: sem SideNav nem BottomNav (mantêm apenas o header). */
const FOCUS_MODE_ROUTES = ["/exercicios", "/onboarding/cat"];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "/";
  const isFocusMode = FOCUS_MODE_ROUTES.some((r) => pathname.startsWith(r));
  const { user } = useCurrentUser();

  return (
    <div className="min-h-screen">
      <SideNav />
      {!isFocusMode && <BottomNav />}

      <div className="lg:pl-64">
        <GlobalHeader userRole="student" userName={user?.nome_completo || "Aluno"} />
        <div className={isFocusMode ? "" : "pb-safe-bottom"}>{children}</div>
      </div>
    </div>
  );
}
