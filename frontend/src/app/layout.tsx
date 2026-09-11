import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "katex/dist/katex.min.css";
import { ConcurrentSessionModal } from "@/components/session/ConcurrentSessionModal";
import { DisciplineThemeProvider } from "@/components/theme/DisciplineThemeProvider";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Tutor Inteligente — Plataforma EAD de Matemática",
  description: "Plataforma EAD de Matemática do Ensino Médio com IA Socrática orientada pela coleção Gelson Iezzi.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover", // respeita safe-areas em iOS com notch (BottomNav)
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#fcf9f7" },
    { media: "(prefers-color-scheme: dark)", color: "#0d0907" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={inter.variable}>
      <body className="font-sans antialiased selection:bg-subject-200 selection:text-subject-900">
        <DisciplineThemeProvider>{children}</DisciplineThemeProvider>
        <ConcurrentSessionModal />
      </body>
    </html>
  );
}
