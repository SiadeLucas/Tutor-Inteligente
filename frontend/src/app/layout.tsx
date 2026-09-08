import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "katex/dist/katex.min.css";
import { ConcurrentSessionModal } from "@/components/session/ConcurrentSessionModal";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Tutor Inteligente — Plataforma EAD de Matemática",
  description: "Plataforma EAD de Matemática do Ensino Médio com IA Socrática orientada pela coleção Gelson Iezzi.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={inter.variable}>
      <body className="font-sans antialiased selection:bg-[#FFF3E0] selection:text-[#E65100]">
        {children}
        <ConcurrentSessionModal />
      </body>
    </html>
  );
}
