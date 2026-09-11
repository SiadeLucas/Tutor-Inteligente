import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        /**
         * RN-INT-001 revisada — Discipline-Scoped Tokens
         *
         * Os valores das variáveis são injetados em runtime pelo
         * DisciplineThemeProvider a partir de `disciplinas.cor_tema` (banco).
         * Nenhum hex de disciplina deve aparecer em componentes.
         *
         * `subject-*`: identidade da matéria (laranja = Matemática hoje).
         * `ink-*`: texto estrutural (levemente matizado pelo hue da matéria).
         * `surface-*`: fundos (bg/card/elevated).
         * `line-*`: bordas e hairlines.
         */
        subject: {
          50: "var(--subject-50)",
          100: "var(--subject-100)",
          200: "var(--subject-200)",
          300: "var(--subject-300)",
          400: "var(--subject-400)",
          500: "var(--subject-500)",
          600: "var(--subject-600)",
          700: "var(--subject-700)",
          800: "var(--subject-800)",
          900: "var(--subject-900)",
          DEFAULT: "var(--subject-500)",
          wash: "var(--subject-wash)",
          "wash-strong": "var(--subject-wash-strong)",
        },
        ink: {
          text: "var(--ink-text)",
          muted: "var(--ink-muted)",
          faint: "var(--ink-faint)",
        },
        surface: {
          bg: "var(--surface-bg)",
          card: "var(--surface-card)",
          elevated: "var(--surface-elevated)",
        },
        line: {
          DEFAULT: "var(--line-border)",
          strong: "var(--line-strong)",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
