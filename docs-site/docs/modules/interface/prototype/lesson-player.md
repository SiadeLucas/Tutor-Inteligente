---
title: Interface - Player de Aula em Split-Screen (65% / 35%)
type: module
status: draft
related:
  - modules/interface/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 3. Player de Aula em Split-Screen (`LessonPlayer.tsx`)

Componente central da experiência de aprendizagem de 50 minutos: **Leitor KaTeX à esquerda (65%)** e **Chat Socrático com IA em tempo real à direita (35%)**, com cronômetro ativo e suporte a *Bottom Sheet* no mobile.

---

## Código Fonte (`frontend/src/components/lesson/LessonPlayer.tsx`)

```tsx
"use client";

import React, { useState } from "react";
import { Clock, Send, Sparkles, BookOpen, CheckSquare, MessageSquare } from "lucide-react";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";

interface AulaData {
  id: string;
  capitulo_titulo: string;
  volume_numero: number;
  bloco1_teoria: string;
  bloco2_exemplos: string;
  bloco3_dicas: string;
}

export const LessonPlayer: React.FC<{ aula: AulaData }> = ({ aula }) => {
  const [blocoAtivo, setBlocoAtivo] = useState<"teoria" | "exemplos" | "dicas" | "fixacao">("teoria");
  const [duvidaInput, setDuvidaInput] = useState("");
  const [mensagensChat, setMensagensChat] = useState([
    {
      papel: "assistant",
      texto: `Olá! Sou o Tutor Especialista do Volume ${aula.volume_numero}. Estou aqui para tirar suas dúvidas conceituais sem dar respostas prontas. Em que posso ajudar?`,
    },
  ]);
  const [tempoRestanteSegundos, setTempoRestanteSegundos] = useState(50 * 60);

  const enviarDuvida = () => {
    if (!duvidaInput.trim()) return;
    const novaMsg = { papel: "user", texto: duvidaInput };
    setMensagensChat((prev) => [...prev, novaMsg]);
    setDuvidaInput("");

    // Resposta simulada socrática em KaTeX
    setTimeout(() => {
      setMensagensChat((prev) => [
        ...prev,
        {
          papel: "assistant",
          texto:
            "Observe atentamente os coeficientes na equação geral $ax^2 + bx + c = 0$. Qual é o valor do discriminante $\\Delta$?",
        },
      ]);
    }, 600);
  };

  return (
    <div className="flex flex-col h-screen bg-neutral-50 dark:bg-neutral-950">
      {/* Topo: Barra da Sessão de 50 Minutos */}
      <header className="h-14 border-b border-neutral-200 dark:border-neutral-800 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md px-6 flex items-center justify-between z-20">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold px-2 py-0.5 rounded bg-orange-100 dark:bg-orange-950 text-orange-600 dark:text-orange-400">
            Vol. {aula.volume_numero}
          </span>
          <h1 className="font-semibold text-sm text-neutral-800 dark:text-neutral-200 truncate max-w-md">
            {aula.capitulo_titulo}
          </h1>
        </div>

        {/* Cronômetro de Estudo Ativo */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 font-mono text-xs font-semibold">
          <Clock className="w-3.5 h-3.5 text-orange-500 animate-pulse" />
          <span>
            {Math.floor(tempoRestanteSegundos / 60)}:
            {(tempoRestanteSegundos % 60).toString().padStart(2, "0")} restantes
          </span>
        </div>
      </header>

      {/* Corpo Split-Screen (65% Leitor / 35% Chat) */}
      <div className="flex-1 flex overflow-hidden">
        {/* Painel Esquerdo: Leitor KaTeX em 4 Blocos (65%) */}
        <main className="w-full lg:w-[65%] h-full flex flex-col border-r border-neutral-200 dark:border-neutral-800 overflow-y-auto">
          {/* Navegação de Abas dos 4 Blocos */}
          <div className="sticky top-0 z-10 bg-white/95 dark:bg-neutral-900/95 backdrop-blur-sm border-b border-neutral-200 dark:border-neutral-800 px-6 py-2.5 flex gap-2">
            {[
              { key: "teoria", label: "1. Teoria (10m)", icon: BookOpen },
              { key: "exemplos", label: "2. Exemplos (15m)", icon: Sparkles },
              { key: "dicas", label: "3. Dicas IA (10m)", icon: MessageSquare },
              { key: "fixacao", label: "4. Fixação (15m)", icon: CheckSquare },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setBlocoAtivo(tab.key as any)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                  blocoAtivo === tab.key
                    ? "bg-orange-500 text-white shadow-sm"
                    : "text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800"
                }`}
              >
                <tab.icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Área de Leitura com Renderização KaTeX */}
          <div className="p-8 max-w-3xl mx-auto w-full">
            {blocoAtivo === "teoria" && <KaTeXRenderer content={aula.bloco1_teoria} />}
            {blocoAtivo === "exemplos" && <KaTeXRenderer content={aula.bloco2_exemplos} />}
            {blocoAtivo === "dicas" && <KaTeXRenderer content={aula.bloco3_dicas} />}
            {blocoAtivo === "fixacao" && (
              <div className="text-center py-12">
                <CheckSquare className="w-12 h-12 text-orange-500 mx-auto mb-3" />
                <h3 className="text-lg font-bold">Bateria de Fixação (3 a 5 exercícios)</h3>
                <p className="text-sm text-neutral-500 max-w-sm mx-auto mt-1 mb-6">
                  Para concluir este capítulo e liberar o próximo nó da Skill Tree, responda a bateria.
                </p>
                <button className="px-6 py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-sm transition-colors">
                  Iniciar Bateria Agora
                </button>
              </div>
            )}
          </div>
        </main>

        {/* Painel Direito: Chat Socrático Fixo (35% no Desktop) */}
        <aside className="hidden lg:flex w-[35%] h-full flex-col bg-white dark:bg-neutral-900">
          <div className="p-4 border-b border-neutral-200 dark:border-neutral-800 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span className="font-semibold text-sm">Tutor Socrático • Vol. {aula.volume_numero}</span>
          </div>

          {/* Histórico de Mensagens */}
          <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
            {mensagensChat.map((m, idx) => (
              <div
                key={idx}
                className={`p-3.5 rounded-2xl text-xs max-w-[85%] leading-relaxed ${
                  m.papel === "user"
                    ? "bg-orange-500 text-white self-end rounded-br-none"
                    : "bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 self-start rounded-bl-none border border-neutral-200 dark:border-neutral-700"
                }`}
              >
                <KaTeXRenderer content={m.texto} />
              </div>
            ))}
          </div>

          {/* Campo de Envio de Dúvida */}
          <div className="p-3 border-t border-neutral-200 dark:border-neutral-800 flex gap-2">
            <input
              type="text"
              value={duvidaInput}
              onChange={(e) => setDuvidaInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && enviarDuvida()}
              placeholder="Tire uma dúvida sobre este tópico..."
              className="flex-1 px-3.5 py-2 text-xs rounded-xl bg-neutral-100 dark:bg-neutral-800 border-none focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <button
              onClick={enviarDuvida}
              className="p-2 rounded-xl bg-orange-500 text-white hover:bg-orange-600 transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
};
```
