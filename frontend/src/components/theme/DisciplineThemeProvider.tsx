"use client";

/**
 * DisciplineThemeProvider — RN-INT-001 revisada
 *
 * Responsabilidade única: transformar `disciplinas.cor_tema` (fonte da verdade
 * no banco) em CSS custom properties na <html>, visíveis a todo o app.
 *
 * - Busca a disciplina ativa em GET /conteudo/disciplinas/{slug} (backend).
 * - Deriva toda a escala via OKLCH (lib/color.ts) — zero hex no código.
 * - Aplica também os neutros estruturais (bg/card/text/border), levemente
 *   matizados pelo hue da disciplina (0.4–1.2% de croma).
 * - Fallback offline: se o backend não responder, usa Matemática (#F57C00)
 *   para não quebrar o desenvolvimento local.
 */

import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { buildPalette, neutralPalette, hexToOklch, hexToRgb } from "@/lib/color";

export type ThemeMode = "light" | "dark" | "system";

export interface DisciplinaAtiva {
  slug: string;
  nome: string;
  icone: string;
  cor_tema: string;
}

interface DisciplineThemeContextValue {
  disciplina: DisciplinaAtiva | null;
  /** Escala derivada 50–900, útil para gráficos (Recharts) e SVGs. */
  palette: ReturnType<typeof buildPalette> | null;
  loading: boolean;
  /** Modo de tema escolhido pelo usuário (RN-INT-005 — tela /perfil). */
  theme: ThemeMode;
  setTheme: (mode: ThemeMode) => void;
}

const DisciplineThemeContext = createContext<DisciplineThemeContextValue>({
  disciplina: null,
  palette: null,
  loading: true,
  theme: "system",
  setTheme: () => {},
});

const THEME_STORAGE_KEY = "ti-theme";

function lerTemaInicial(): ThemeMode {
  if (typeof window === "undefined") return "system";
  const salvo = window.localStorage.getItem(THEME_STORAGE_KEY);
  return salvo === "dark" || salvo === "light" || salvo === "system" ? salvo : "system";
}

/** Hue de fallback (laranja #F57C00 ≈ 60° em OKLCH) para modo offline. */
const FALLBACK_HUE = 60;
const FALLBACK_BASE = "#F57C00";

export function DisciplineThemeProvider({
  children,
  slug = "matematica",
}: {
  children: React.ReactNode;
  slug?: string;
}) {
  const [disciplina, setDisciplina] = useState<DisciplinaAtiva | null>(null);
  const [loading, setLoading] = useState(true);
  const [theme, setThemeState] = useState<ThemeMode>(lerTemaInicial);

  const setTheme = React.useCallback((mode: ThemeMode) => {
    setThemeState(mode);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(THEME_STORAGE_KEY, mode);
    }
  }, []);

  useEffect(() => {
    let alive = true;
    async function load() {
      try {
        const data = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/conteudo/disciplinas/${slug}`
        ).then((r) => {
          if (!r.ok) throw new Error(String(r.status));
          return r.json();
        });
        if (alive) setDisciplina(data);
      } catch {
        if (alive) setDisciplina({ slug, nome: "Matemática", icone: "calculate", cor_tema: FALLBACK_BASE });
      } finally {
        if (alive) setLoading(false);
      }
    }
    load();
    return () => {
      alive = false;
    };
  }, [slug]);

  const palette = useMemo(() => {
    const base = disciplina?.cor_tema || FALLBACK_BASE;
    const hue = hexToOklch(base).h;
    const dark = neutralPalette(hue, true);
    const light = neutralPalette(hue, false);
    return { subject: buildPalette(base), dark, light, hue };
  }, [disciplina]);

  useEffect(() => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;
    const s = palette.subject.scale;
    const { dark, light } = palette;

    // Escala da disciplina (idêntica em light e dark — contraste garantido)
    root.style.setProperty("--subject-50", s[50]);
    root.style.setProperty("--subject-100", s[100]);
    root.style.setProperty("--subject-200", s[200]);
    root.style.setProperty("--subject-300", s[300]);
    root.style.setProperty("--subject-400", s[400]);
    root.style.setProperty("--subject-500", s[500]);
    root.style.setProperty("--subject-600", s[600]);
    root.style.setProperty("--subject-700", s[700]);
    root.style.setProperty("--subject-800", s[800]);
    root.style.setProperty("--subject-900", s[900]);
    root.style.setProperty("--subject-base", palette.subject.base);

    // Wash: tinta da disciplina com alfa pré-computado (Tailwind v3 ignora
    // modificadores /N sobre vars de cor pura, então o alfa vai no valor).
    const wash = (alpha: number) => {
      const { r, g, b } = hexToRgb(palette.subject.scale[500]);
      return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    };
    root.style.setProperty("--subject-wash", wash(0.08));
    root.style.setProperty("--subject-wash-strong", wash(0.16));

    // Estruturais light (default :root)
    root.style.setProperty("--surface-bg", light.bg);
    root.style.setProperty("--surface-card", light.card);
    root.style.setProperty("--surface-elevated", light.elevated);
    root.style.setProperty("--ink-text", light.text);
    root.style.setProperty("--ink-muted", light.textMuted);
    root.style.setProperty("--ink-faint", light.textFaint);
    root.style.setProperty("--line-border", light.border);
    root.style.setProperty("--line-strong", light.borderStrong);

    // Escolhe dark ou light conforme o modo do usuário (RN-INT-005):
    // "system" segue prefers-color-scheme; light/dark são escolhas explícitas.
    const prefereDark =
      theme === "dark" ||
      (theme === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);
    applyMode(root, palette, prefereDark ? "dark" : "light");
  }, [palette, theme]);

  // Em "system", acompanha mudanças ao vivo da preferência do SO.
  useEffect(() => {
    if (theme !== "system" || typeof window === "undefined") return;
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => {
      applyMode(document.documentElement, palette, mq.matches ? "dark" : "light");
    };
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, [theme, palette, disciplina]);

  const value = useMemo(
    () => ({ disciplina, palette: palette.subject, loading, theme, setTheme }),
    [disciplina, palette, loading, theme, setTheme]
  );

  return <DisciplineThemeContext.Provider value={value}>{children}</DisciplineThemeContext.Provider>;
}

function applyMode(
  root: HTMLElement,
  palette: { dark: ReturnType<typeof neutralPalette>; light: ReturnType<typeof neutralPalette> },
  theme: "dark" | "light"
) {
  const structural = theme === "dark" ? palette.dark : palette.light;
  root.style.setProperty("--surface-bg", structural.bg);
  root.style.setProperty("--surface-card", structural.card);
  root.style.setProperty("--surface-elevated", structural.elevated);
  root.style.setProperty("--ink-text", structural.text);
  root.style.setProperty("--ink-muted", structural.textMuted);
  root.style.setProperty("--ink-faint", structural.textFaint);
  root.style.setProperty("--line-border", structural.border);
  root.style.setProperty("--line-strong", structural.borderStrong);
  if (theme === "dark") {
    root.classList.add("dark");
  } else {
    root.classList.remove("dark");
  }
}

export function useDisciplineTheme() {
  return useContext(DisciplineThemeContext);
}
