"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2, ShieldAlert } from "lucide-react";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { TeacherNavBar } from "@/components/teacher/TeacherNavBar";
import { useCurrentUser } from "@/hooks/useCurrentUser";

/**
 * Layout da área docente — camada de defesa no cliente (Etapa 10.1.1).
 * A proteção canônica permanece no backend (require_teacher_role -> 403);
 * aqui apenas evitamos renderizar o painel para perfis não docentes.
 */
export default function TeacherLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const { user, loading } = useCurrentUser();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace("/login");
    } else if (user.role !== "teacher" && user.role !== "admin") {
      router.replace("/materias");
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen bg-surface-bg dark:bg-surface-bg flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-subject-500 animate-spin" />
      </div>
    );
  }

  if (user.role !== "teacher" && user.role !== "admin") {
    return (
      <div className="min-h-screen bg-surface-bg dark:bg-surface-bg flex items-center justify-center px-4">
        <div className="max-w-md text-center bg-white dark:bg-surface-card border border-line rounded-2xl p-8 shadow-sm">
          <ShieldAlert className="w-10 h-10 text-rose-500 mx-auto mb-4" />
          <h1 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
            Acesso restrito ao corpo docente
          </h1>
          <p className="text-sm text-slate-500 dark:text-ink-muted">
            Esta área é exclusiva para professores e administradores. Se você
            acredita que isso é um erro, faça login com suas credenciais
            institucionais.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader userRole="teacher" userName={user.nome_completo} showDisciplineBadge={false} />
      <TeacherNavBar />
      {children}
    </div>
  );
}
