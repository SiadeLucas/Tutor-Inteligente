---
title: Painel do Professor - Editor Split-Screen KaTeX
type: module
status: draft
related:
  - modules/painel-professor/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Editor Split-Screen KaTeX (`CuratorEditor.tsx`)

Componente de curadoria visual para o professor editar conteúdos didáticos com **Markdown à esquerda (50%)** e **preview KaTeX em tempo real à direita (50%)**, com barra de ferramentas para fórmulas rápidas.

---

## Código Fonte (`frontend/src/components/teacher/CuratorEditor.tsx`)

```tsx
"use client";

import React, { useState } from "react";
import { Save, Eye, Code2, Sparkles, CheckCircle2 } from "lucide-react";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";

interface CuratorEditorProps {
  initialContent: string;
  capituloTitulo: string;
  onSave: (newContent: string) => Promise<void>;
}

export const CuratorEditor: React.FC<CuratorEditorProps> = ({
  initialContent,
  capituloTitulo,
  onSave,
}) => {
  const [content, setContent] = useState(initialContent);
  const [isSaving, setIsSaving] = useState(false);
  const [showToast, setShowToast] = useState(false);

  const inserirSnippet = (snippet: string) => {
    setContent((prev) => prev + snippet);
  };

  const handleSalvar = async () => {
    setIsSaving(true);
    try {
      await onSave(content);
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-neutral-100 dark:bg-neutral-950">
      {/* Barra de Ações Superior */}
      <header className="h-14 bg-white dark:bg-neutral-900 border-b border-neutral-200 dark:border-neutral-800 px-6 flex items-center justify-between">
        <div>
          <span className="text-[10px] uppercase font-bold text-orange-600 tracking-wider">
            Curadoria Pedagógica
          </span>
          <h2 className="text-sm font-bold text-neutral-800 dark:text-neutral-100">
            {capituloTitulo}
          </h2>
        </div>

        {/* Barra de Ferramentas de Snippets Matemáticos */}
        <div className="hidden md:flex items-center gap-1.5 bg-neutral-100 dark:bg-neutral-800 p-1 rounded-xl">
          {[
            { label: "Fração", snippet: " \\frac{a}{b} " },
            { label: "Raiz", snippet: " \\sqrt{x} " },
            { label: "Delta", snippet: " \\Delta = b^2 - 4ac " },
            { label: "Função", snippet: " f(x) = ax^2 + bx + c " },
          ].map((btn, i) => (
            <button
              key={i}
              onClick={() => inserirSnippet(btn.snippet)}
              className="px-2.5 py-1 rounded-lg text-xs font-mono font-medium hover:bg-white dark:hover:bg-neutral-700 transition-colors text-neutral-700 dark:text-neutral-300"
            >
              {btn.label}
            </button>
          ))}
        </div>

        <button
          onClick={handleSalvar}
          disabled={isSaving}
          className="px-4 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-xs transition-colors flex items-center gap-2 shadow-sm"
        >
          <Save className="w-3.5 h-3.5" />
          {isSaving ? "Salvando..." : "Salvar Alterações"}
        </button>
      </header>

      {/* Editor Split-Screen (50% Código / 50% Preview KaTeX) */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-neutral-200 dark:divide-neutral-800 overflow-hidden">
        {/* Lado Esquerdo: Textarea com Markdown e LaTeX */}
        <div className="flex flex-col h-full bg-white dark:bg-neutral-900">
          <div className="px-4 py-2 bg-neutral-50 dark:bg-neutral-800/50 border-b border-neutral-200 dark:border-neutral-800 text-[11px] font-semibold text-neutral-500 flex items-center gap-1.5">
            <Code2 className="w-3.5 h-3.5 text-orange-500" /> Editor Markdown & KaTeX
          </div>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="flex-1 p-6 font-mono text-xs leading-relaxed bg-transparent resize-none outline-none text-neutral-800 dark:text-neutral-200"
            placeholder="Escreva a teoria usando $...$ para equações em linha ou $$...$$ para destaque centralizado..."
          />
        </div>

        {/* Lado Direito: Preview Renderizado em Tempo Real */}
        <div className="flex flex-col h-full bg-neutral-50/50 dark:bg-neutral-900/50 overflow-y-auto">
          <div className="px-4 py-2 bg-neutral-50 dark:bg-neutral-800/50 border-b border-neutral-200 dark:border-neutral-800 text-[11px] font-semibold text-neutral-500 flex items-center gap-1.5">
            <Eye className="w-3.5 h-3.5 text-emerald-500" /> Pré-visualização do Aluno
          </div>
          <div className="p-8 max-w-2xl mx-auto w-full">
            <KaTeXRenderer content={content} />
          </div>
        </div>
      </div>

      {/* Toast Notificação de Salvo com Sucesso */}
      {showToast && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-2.5 rounded-xl bg-neutral-900 text-white text-xs font-semibold shadow-2xl animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          Conteúdo didático atualizado com sucesso!
        </div>
      )}
    </div>
  );
};
```
