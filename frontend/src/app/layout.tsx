import type { Metadata } from "next";
import "./globals.css";
import { ConcurrentSessionModal } from "@/components/session/ConcurrentSessionModal";

export const metadata: Metadata = {
  title: "Tutor Inteligente — Plataforma EAD de Matemática",
  description: "Plataforma EAD de Matemática do Ensino Médio com IA Socrática",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>
        {children}
        <ConcurrentSessionModal />
      </body>
    </html>
  );
}
