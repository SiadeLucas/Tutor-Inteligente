"use client";

import { AppShell } from "@/components/nav/AppShell";
import { TeacherSimulationBanner } from "@/components/teacher/TeacherSimulationBanner";

export default function StudentLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <TeacherSimulationBanner />
      <AppShell>{children}</AppShell>
    </>
  );
}
