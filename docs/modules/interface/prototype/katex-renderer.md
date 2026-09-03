---
title: Interface - Renderizador KaTeX Seguro (React)
type: module
status: draft
related:
  - modules/interface/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Renderizador KaTeX Seguro (`KaTeXRenderer.tsx`)

Componente React otimizado para o **Next.js 14 (App Router)** que processa textos mistos contendo Markdown e fórmulas matemáticas KaTeX em linha (`$...$`) e em bloco centralizado (`$$...$$`), imune a falhas de hidratação SSR.

---

## Código Fonte (`frontend/src/components/math/KaTeXRenderer.tsx`)

```tsx
"use client";

import React, { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

interface KaTeXRendererProps {
  content: string;
  className?: string;
}

export const KaTeXRenderer: React.FC<KaTeXRendererProps> = ({ content, className = "" }) => {
  // Processa e compila os delimitadores matemáticos de forma segura
  const htmlContent = useMemo(() => {
    if (!content) return "";

    try {
      // 1. Processa blocos centralizados de fórmulas ($$...$$)
      let parsed = content.replace(/\$\$([\s\S]*?)\$\$/g, (_, equation) => {
        try {
          return katex.renderToString(equation.trim(), {
            displayMode: true,
            throwOnError: false,
            strict: false,
          });
        } catch {
          return `<span class="katex-error text-red-500 font-mono">$$${equation}$$</span>`;
        }
      });

      // 2. Processa expressões em linha ($...$)
      parsed = parsed.replace(/\$([^\$\n]+?)\$/g, (_, equation) => {
        try {
          return katex.renderToString(equation.trim(), {
            displayMode: false,
            throwOnError: false,
            strict: false,
          });
        } catch {
          return `<span class="katex-error text-red-500 font-mono">$${equation}$</span>`;
        }
      });

      return parsed;
    } catch (err) {
      console.error("Erro no parsing do KaTeX:", err);
      return content;
    }
  }, [content]);

  return (
    <div
      className={`prose prose-orange max-w-none text-neutral-800 dark:text-neutral-100 leading-relaxed font-sans ${className}`}
      dangerouslySetInnerHTML={{ __html: htmlContent }}
    />
  );
};
```
