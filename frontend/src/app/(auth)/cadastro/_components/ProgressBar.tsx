"use client";

interface ProgressBarProps {
  currentStep: number;
  totalSteps: number;
}

const LABELS = ["Dados Pessoais", "Contato & Credenciais", "Acadêmico & Endereço"];

export default function ProgressBar({ currentStep, totalSteps }: ProgressBarProps) {
  return (
    <div>
      <div className="flex items-center gap-2" aria-label={`Etapa ${currentStep} de ${totalSteps}`}>
        {Array.from({ length: totalSteps }, (_, indice) => {
          const numero = indice + 1;
          const concluida = numero < currentStep;
          const atual = numero === currentStep;
          return (
            <div key={numero} className="flex-1">
              <div
                className={`h-1.5 rounded-full transition-colors ${
                  concluida || atual ? "bg-[#F57C00]" : "bg-slate-200 dark:bg-[#3d2f1f]"
                }`}
              />
              <div className="mt-2 flex items-center gap-1.5">
                <span
                  className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-bold ${
                    concluida || atual
                      ? "bg-[#F57C00] text-white"
                      : "bg-slate-200 dark:bg-[#3d2f1f] text-slate-500 dark:text-[#A89F91]"
                  }`}
                >
                  {numero}
                </span>
                <span
                  className={`text-[11px] font-semibold hidden sm:block ${
                    atual
                      ? "text-[#E65100] dark:text-[#FFB74D]"
                      : "text-slate-500 dark:text-[#A89F91]"
                  }`}
                >
                  {LABELS[indice]}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
