"use client";

import React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  Users,
  BookOpenCheck,
  CreditCard,
  Eye,
  ExternalLink,
} from "lucide-react";

export function TeacherNavBar() {
  const pathname = usePathname();
  const router = useRouter();

  const links = [
    {
      href: "/teacher",
      label: "Visão Geral",
      icon: LayoutDashboard,
      active: pathname === "/teacher",
    },
    {
      href: "/teacher/alunos",
      label: "Gestão de Alunos",
      icon: Users,
      active: pathname.startsWith("/teacher/alunos"),
    },
    {
      href: "/teacher/curadoria",
      label: "Curadoria KaTeX",
      icon: BookOpenCheck,
      active: pathname.startsWith("/teacher/curadoria"),
    },
    {
      href: "/teacher/financeiro",
      label: "Financeiro & Extrato",
      icon: CreditCard,
      active: pathname.startsWith("/teacher/financeiro"),
    },
  ];

  const handleEntrarModoAluno = () => {
    // Redireciona para o catálogo de matérias com flag de visualização docente
    router.push("/materias?view=student");
  };

  return (
    <div className="bg-white dark:bg-surface-card border-b border-line px-4 sm:px-6">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 py-2.5">
        {/* Links de navegação */}
        <nav className="flex items-center gap-1 sm:gap-2 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0 scrollbar-none">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
                  link.active
                    ? "bg-subject-50 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200 dark:border-subject-800/60 shadow-xs"
                    : "text-slate-600 dark:text-ink-muted hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-surface-elevated"
                }`}
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Botão de Modo Visão do Aluno */}
        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <button
            onClick={handleEntrarModoAluno}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-surface-elevated dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-line transition-all shadow-2xs cursor-pointer group"
            title="Navegar pela plataforma simulando a experiência do estudante"
          >
            <Eye className="w-3.5 h-3.5 text-subject-600 group-hover:scale-110 transition-transform" />
            <span>Modo Visão do Aluno</span>
            <ExternalLink className="w-3 h-3 text-slate-400 opacity-60" />
          </button>
        </div>
      </div>
    </div>
  );
}
