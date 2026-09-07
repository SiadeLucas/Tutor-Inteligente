---
title: Painel do Professor - Modo Visão do Aluno
type: module
status: draft
related:
  - modules/painel-professor/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Modo Visão do Aluno (`StudentPreviewBar.tsx`)

Recurso que permite ao professor testar a experiência de navegação da **Skill Tree**, dos conteúdos em KaTeX e do chat com IA como se fosse um aluno real, sem necessidade de deslogar ou criar contas secundárias.

---

## Código Fonte (`frontend/src/components/teacher/StudentPreviewBar.tsx`)

```tsx
"use client";

import React, { createContext, useContext, useState } from "react";
import { Eye, ArrowLeft, ShieldAlert } from "lucide-react";
import { useRouter } from "next/navigation";

interface StudentPreviewContextType {
  isStudentPreview: boolean;
  ativarModoAluno: () => void;
  desativarModoAluno: () => void;
}

const StudentPreviewContext = createContext<StudentPreviewContextType>({
  isStudentPreview: false,
  ativarModoAluno: () => {},
  desativarModoAluno: () => {},
});

export const StudentPreviewProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isStudentPreview, setIsStudentPreview] = useState(false);
  const router = useRouter();

  const ativarModoAluno = () => {
    setIsStudentPreview(true);
    router.push("/app/skill-tree");
  };

  const desativarModoAluno = () => {
    setIsStudentPreview(false);
    router.push("/teacher/dashboard");
  };

  return (
    <StudentPreviewContext.Provider value={{ isStudentPreview, ativarModoAluno, desativarModoAluno }}>
      {isStudentPreview && (
        <div className="sticky top-0 z-50 h-10 bg-amber-500 text-neutral-950 font-medium text-xs px-4 flex items-center justify-between shadow-md">
          <div className="flex items-center gap-2">
            <Eye className="w-4 h-4 text-neutral-950" />
            <span>
              <b>Modo Visão do Aluno Ativo:</b> Você está navegando na Skill Tree e nas aulas com a visão de um estudante.
            </span>
          </div>

          <button
            onClick={desativarModoAluno}
            className="px-3 py-1 rounded-lg bg-neutral-950 text-white hover:bg-neutral-800 transition-colors flex items-center gap-1.5 text-[11px] font-semibold"
          >
            <ArrowLeft className="w-3 h-3" /> Voltar ao Painel Docente
          </button>
        </div>
      )}
      {children}
    </StudentPreviewContext.Provider>
  );
};

export const useStudentPreview = () => useContext(StudentPreviewContext);
```
