import Link from "next/link";
import { BookOpen, Cpu, Award, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#1a1408] text-slate-900 dark:text-slate-100 flex flex-col">
      {/* Header Institucional */}
      <header className="border-b border-slate-200 dark:border-[#382b1c] bg-white dark:bg-[#1a1408] sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#F57C00] flex items-center justify-center text-white font-black text-sm shadow-sm">
              TI
            </div>
            <div>
              <span className="font-bold text-base tracking-tight block leading-tight">
                Tutor Inteligente
              </span>
              <span className="text-[11px] text-slate-500 dark:text-[#A89F91] block">
                Matemática do Ensino Médio
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] border border-[#FFB74D]/40">
              <span>📐</span>
              <span>Coleção Gelson Iezzi</span>
            </div>

            <Link
              href="/login"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#F57C00] hover:bg-[#EF6C00] text-white text-xs font-semibold shadow-sm transition-colors cursor-pointer"
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
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] border border-[#FFB74D]/30 mb-6">
            <ShieldCheck className="w-4 h-4 text-[#F57C00]" />
            <span>Educação com Rigor Matemático e Pedagogia Socrática</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight max-w-3xl mx-auto">
            Aprenda Matemática do Ensino Médio com Clareza e Profundidade
          </h1>

          <p className="mt-5 text-base sm:text-lg text-slate-600 dark:text-[#A89F91] max-w-2xl mx-auto leading-relaxed">
            Uma plataforma de aprendizagem completa estruturada nos 11 volumes da coleção <em>Fundamentos de Matemática Elementar</em> de Gelson Iezzi, com tutoria de IA Socrática e avaliação adaptativa por Teoria da Resposta ao Item.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              href="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-[#F57C00] hover:bg-[#EF6C00] text-white font-semibold text-sm shadow-sm transition-colors cursor-pointer"
            >
              <span>Entrar com Login ou CPF</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <a
              href="#pilares"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl border border-slate-300 dark:border-[#3d2f1f] hover:bg-slate-100 dark:hover:bg-[#261d11] text-slate-700 dark:text-slate-200 font-semibold text-sm transition-colors"
            >
              Conhecer a Metodologia
            </a>
          </div>
        </section>

        {/* Pilares Didáticos */}
        <section id="pilares" className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] flex items-center justify-center mb-4">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                11 Volumes do Iezzi
              </h3>
              <p className="text-xs text-slate-600 dark:text-[#A89F91] leading-relaxed">
                Currículo completo de Álgebra, Trigonometria, Geometria, Análise Combinatória e Cálculo, sem simplificações artificiais.
              </p>
            </div>

            <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-[#F57C00] flex items-center justify-center mb-4 border border-amber-100 dark:border-amber-800/30">
                <Cpu className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                Mediação Socrática
              </h3>
              <p className="text-xs text-slate-600 dark:text-[#A89F91] leading-relaxed">
                O Tutor IA guia o raciocínio em 3 estágios com perguntas conceituais e contra-exemplos, sem jamais entregar a resposta pronta.
              </p>
            </div>

            <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-6 sm:p-7 shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4 border border-emerald-100 dark:border-emerald-800/30">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-2">
                Modelo TRI (CAT)
              </h3>
              <p className="text-xs text-slate-600 dark:text-[#A89F91] leading-relaxed">
                Calibração psicométrica que mede a proficiência real (θ), discriminando chute e guiando o estudante na sua zona de desenvolvimento proximal.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-[#382b1c] bg-white dark:bg-[#1a1408] py-8 text-center text-xs text-slate-500 dark:text-[#A89F91]">
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
