"use client";

import React, { useMemo } from "react";
import katex from "katex";

interface KaTeXRendererProps {
  content: string;
  className?: string;
}

/**
 * Renderiza textos matemáticos mistos contendo markdown e equações LaTeX.
 * Suporta delimitação de bloco ($$...$$) e inline ($...$).
 */
export function KaTeXRenderer({ content, className = "" }: KaTeXRendererProps) {
  // Processa o conteúdo convertendo blocos e inline em elementos HTML estilizados
  const renderedHtml = useMemo(() => {
    if (!content) return "";

    // 1. Processar blocos de display math ($$...$$)
    let processed = content.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
      try {
        const rendered = katex.renderToString(formula.trim(), {
          displayMode: true,
          throwOnError: false,
        });
        return `<div class="katex-display-wrapper my-4 overflow-x-auto py-2 text-center">${rendered}</div>`;
      } catch (e) {
        return `<pre class="text-red-500 font-mono text-xs">${formula}</pre>`;
      }
    });

    // 2. Processar inline math ($...$)
    processed = processed.replace(/\$([^\$\n]+?)\$/g, (match, formula) => {
      try {
        const rendered = katex.renderToString(formula.trim(), {
          displayMode: false,
          throwOnError: false,
        });
        return `<span class="katex-inline-wrapper px-1">${rendered}</span>`;
      } catch (e) {
        return `<code class="text-red-500 font-mono text-xs">${formula}</code>`;
      }
    });

    // 3. Processar formatação Markdown básica (Alertas, Títulos, Listas, Negrito)
    const lines = processed.split("\n");
    const formattedLines: string[] = [];
    let inAlert = false;
    let alertType = "";
    let alertContent: string[] = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Alertas padrão GitHub / Docs: > [!WARNING], > [!TIP], > [!IMPORTANT]
      const alertMatch = line.match(/^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/i);
      if (alertMatch) {
        inAlert = true;
        alertType = alertMatch[1].toUpperCase();
        alertContent = [];
        continue;
      }

      if (inAlert) {
        if (line.startsWith(">")) {
          alertContent.push(line.replace(/^>\s?/, ""));
          continue;
        } else {
          // Fechar alerta anterior
          formattedLines.push(renderAlertBox(alertType, alertContent.join("<br/>")));
          inAlert = false;
        }
      }

      // Títulos
      if (line.startsWith("### ")) {
        formattedLines.push(`<h3 class="text-lg font-bold text-slate-900 dark:text-white mt-6 mb-2 tracking-tight">${line.slice(4)}</h3>`);
      } else if (line.startsWith("## ")) {
        formattedLines.push(`<h2 class="text-xl font-bold text-slate-900 dark:text-white mt-7 mb-3 tracking-tight border-b border-slate-100 dark:border-line pb-1.5">${line.slice(3)}</h2>`);
      } else if (line.startsWith("# ")) {
        formattedLines.push(`<h1 class="text-2xl font-extrabold text-slate-900 dark:text-white mt-4 mb-4 tracking-tight">${line.slice(2)}</h1>`);
      } else if (line.startsWith("---")) {
        formattedLines.push(`<hr class="my-6 border-slate-200 dark:border-line" />`);
      } else if (line.startsWith("- ")) {
        const itemText = line.slice(2).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedLines.push(`<li class="ml-4 list-disc text-slate-700 dark:text-slate-300 my-1">${itemText}</li>`);
      } else if (line.trim() === "") {
        formattedLines.push(`<div class="h-2"></div>`);
      } else {
        const pText = line.replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-900 dark:text-white">$1</strong>');
        formattedLines.push(`<p class="text-slate-700 dark:text-slate-300 leading-relaxed my-2">${pText}</p>`);
      }
    }

    if (inAlert) {
      formattedLines.push(renderAlertBox(alertType, alertContent.join("<br/>")));
    }

    return formattedLines.join("\n");
  }, [content]);

  return (
    <div
      className={`katex-article-content prose max-w-none text-slate-800 dark:text-slate-200 ${className}`}
      dangerouslySetInnerHTML={{ __html: renderedHtml }}
    />
  );
}

function renderAlertBox(type: string, innerHtml: string): string {
  // RN-INT-004: ícones vetoriais (Material/Lucide) — nunca emoji, pois a
  // renderização varia por SO e quebra a consistência visual.
  const svgWrap = (paths: string) =>
    `<svg class="w-3.5 h-3.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;

  const ICON_LIGHTBULB = svgWrap(
    '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5"/>'
  );
  const ICON_WARNING = svgWrap(
    '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 20h16a2 2 0 0 0 1.73-2Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>'
  );
  const ICON_PIN = svgWrap(
    '<line x1="12" x2="12" y1="17" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/>'
  );

  let borderColor = "border-subject-500";
  let bgColor = "bg-subject-100 dark:bg-subject-wash";
  let textColor = "text-subject-700 dark:text-subject-300";
  let icon = ICON_LIGHTBULB;
  let label = "Dica Pedagógica";

  if (type === "WARNING") {
    borderColor = "border-amber-500";
    bgColor = "bg-amber-50 dark:bg-amber-950/30";
    textColor = "text-amber-800 dark:text-amber-300";
    icon = ICON_WARNING;
    label = "Atenção & Pegadinha";
  } else if (type === "IMPORTANT") {
    borderColor = "border-sky-500";
    bgColor = "bg-sky-50 dark:bg-sky-950/30";
    textColor = "text-sky-800 dark:text-sky-300";
    icon = ICON_PIN;
    label = "Conceito Fundamental";
  }

  return `
    <div class="my-5 p-4 rounded-xl border-l-4 ${borderColor} ${bgColor} shadow-xs">
      <div class="flex items-center gap-2 font-bold text-xs uppercase tracking-wider ${textColor} mb-1">
        <span>${icon}</span>
        <span>${label}</span>
      </div>
      <div class="text-sm ${textColor} leading-relaxed">
        ${innerHtml}
      </div>
    </div>
  `;
}
