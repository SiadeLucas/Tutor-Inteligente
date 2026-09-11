import Link from "next/link";
import { BookOpen, Cpu, Award, ArrowRight, ShieldCheck, CheckCircle2, Sigma } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col">
      {/* Header Institucional */}
      <header className="border-b border-slate-200 dark:border-line bg-white dark:bg-surface-bg sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-subject-500 flex items-center justify-center text-white font-black text-sm shadow-sm">
              TI
            </div>
            <div>
              <span className="font-bold text-base tracking-tight block leading-tight">
                Tutor Inteligente
              </span>
              <span className="text-[11px] text-slate-500 dark:text-ink-muted block">
                Matemática do Ensino Médio
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200">
              <Sigma className="w-3.5 h-3.5" />
              <span>Coleção Gelson Iezzi</span>
            </div>

            <Link
              href="/cadastro"
              className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-surface-elevated transition-colors"
            >
              Criar Conta
            </Link>

            <Link
              href="/login"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-subject-500 hover:bg-subject-600 text-white text-xs font-semibold shadow-sm transition-colors cursor-pointer"
            >
              <span>Acessar Plataforma</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="max-w-5xl mx-auto px-4 sm:px-6 pt-16 pb-12 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200 mb-6">
            <ShieldCheck className="w-4 h-4 text-subject-600" />
            <span>Educação com Rigor Matemático e Pedagogia Socrática</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight max-w-3xl mx-auto">
            Aprenda Matemática do Ensino Médio com Clareza e Profundidade
          </h1>

          <p className="mt-5 text-base sm:text-lg text-slate-600 dark:text-ink-muted max-w-2xl mx-auto leading-relaxed">
            Uma plataforma de aprendizagem completa estruturada nos 11 volumes da coleção <em>Fundamentos de Matemática Elementar</em> de Gelson Iezzi, com tutoria de IA Socrática e avaliação adaptativa por Teoria da Resposta ao Item.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              href="/cadastro"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors cursor-pointer"
            >
              <span>Começar Gratuitamente</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl border border-slate-300 dark:border-line hover:bg-slate-100 dark:hover:bg-surface-elevated text-slate-700 dark:text-slate-200 font-semibold text-sm transition-colors"
            >
              Entrar na Conta
            </Link>

            <a
              href="#pilares"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3.5 rounded-xl text-slate-600 dark:text-ink-muted hover:text-slate-900 dark:hover:text-white text-sm font-medium transition-colors"
            >
              Metodologia
            </a>
          </div>
        </section>

        {/* Pilares Didáticos */}
        <section id="pilares" className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 flex items-center justify-center mb-4">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                11 Volumes do Iezzi
              </h3>
              <p className="text-xs text-slate-600 dark:text-ink-muted leading-relaxed">
                Currículo completo de Álgebra, Trigonometria, Geometria, Análise Combinatória e Cálculo, sem simplificações artificiais.
              </p>
            </div>

            <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-600 flex items-center justify-center mb-4 border border-subject-200">
                <Cpu className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                Mediação Socrática
              </h3>
              <p className="text-xs text-slate-600 dark:text-ink-muted leading-relaxed">
                O Tutor IA guia o raciocínio em 3 estágios com perguntas conceituais e contra-exemplos, sem jamais entregar a resposta pronta.
              </p>
            </div>

            <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4 border border-emerald-100 dark:border-emerald-800/30">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                Modelo TRI (CAT)
              </h3>
              <p className="text-xs text-slate-600 dark:text-ink-muted leading-relaxed">
                Calibração psicométrica que mede a proficiência real (θ), discriminando chute e guiando o estudante na sua zona de desenvolvimento proximal.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-line bg-white dark:bg-surface-bg py-8 text-center text-xs text-slate-500 dark:text-ink-muted">
        <div className="max-w-6xl mx-auto px-4">
          <p>Tutor Inteligente — Plataforma EAD de Matemática do Ensino Médio.</p>
          <p className="mt-1 text-[11px] text-slate-400 dark:text-slate-600">
            Ambiente seguro com sessão única por aluno e proteção de dados.
          </p>
        </div>
      </footer>
    </div>
  );
}
