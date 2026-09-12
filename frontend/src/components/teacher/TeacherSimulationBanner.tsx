"use client";

import React, { Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Eye, ArrowLeft } from "lucide-react";

function BannerContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const isSimulation = searchParams.get("view") === "student";

  if (!isSimulation) return null;

  return (
    <aside
      aria-label="Barra de Simulação Docente"
      className="bg-amber-500 text-slate-950 px-4 py-2 text-xs font-bold flex items-center justify-between shadow-md sticky top-0 z-50 animate-fadeIn"
    >
      <div className="flex items-center gap-2">
        <Eye className="w-4 h-4" />
        <span>Modo Visão do Aluno ativo: Você está navegando pela plataforma com visão simulada de estudante.</span>
      </div>
      <button
        onClick={() => router.push("/teacher")}
        className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-slate-950 text-white hover:bg-slate-850 transition-colors shadow-2xs cursor-pointer ml-3 flex-shrink-0"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Voltar ao Painel Docente</span>
      </button>
    </aside>
  );
}

export function TeacherSimulationBanner() {
  return (
    <Suspense fallback={null}>
      <BannerContent />
    </Suspense>
  );
}
