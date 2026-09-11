"use client";

import { useState } from "react";
import Link from "next/link";
import { BookOpen } from "lucide-react";

import { OnboardingProvider } from "@/contexts/OnboardingContext";
import ProgressBar from "./_components/ProgressBar";
import Step1Identity from "./_components/Step1Identity";
import Step2Credentials from "./_components/Step2Credentials";
import Step3Academic from "./_components/Step3Academic";

function CadastroContent() {
  const [currentStep, setCurrentStep] = useState(1);

  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-2xl">
        {/* Cabeçalho Institucional */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-subject-500 text-white shadow-sm mb-3">
            <span className="text-xl font-black tracking-tight">TI</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Crie sua Conta no Tutor Inteligente
          </h1>
          <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
            Matemática do Ensino Médio • Fundamentos com Rigor e IA Socrática
          </p>
          <div className="mt-2.5 inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Orientado pela Coleção Gelson Iezzi</span>
          </div>
        </div>

        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 sm:p-9 shadow-sm">
          <ProgressBar currentStep={currentStep} totalSteps={3} />

          <div className="mt-8">
            {currentStep === 1 && <Step1Identity onNext={() => setCurrentStep(2)} />}
            {currentStep === 2 && (
              <Step2Credentials onNext={() => setCurrentStep(3)} onBack={() => setCurrentStep(1)} />
            )}
            {currentStep === 3 && <Step3Academic onBack={() => setCurrentStep(2)} />}
          </div>
        </div>

        <p className="text-center text-xs text-slate-400 dark:text-slate-500 mt-6 leading-relaxed">
          Já tem uma conta?{" "}
          <Link href="/login" className="font-medium text-subject-700 dark:text-subject-300 hover:underline">
            Faça login
          </Link>
          <br />
          Seu progresso é salvo automaticamente e pode ser retomado em até 48 horas.
        </p>
      </div>
    </div>
  );
}

export default function CadastroPage() {
  return (
    <OnboardingProvider>
      <CadastroContent />
    </OnboardingProvider>
  );
}
