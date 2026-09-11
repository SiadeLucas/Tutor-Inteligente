"use client";

import { GlobalHeader } from "@/components/header/GlobalHeader";

export default function TeacherLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader userRole="teacher" userName="Professor" showDisciplineBadge={false} />
      {children}
    </div>
  );
}
