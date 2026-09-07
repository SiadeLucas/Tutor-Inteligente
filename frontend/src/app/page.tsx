export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 text-center bg-slate-950 text-slate-100">
      <div className="max-w-xl p-8 rounded-2xl border border-slate-800 bg-slate-900/60 shadow-2xl backdrop-blur-md">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-6">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Ambiente Local Operacional
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight mb-4 text-white">
          Tutor Inteligente
        </h1>
        <p className="text-slate-400 text-sm mb-6 leading-relaxed">
          Plataforma EAD de Matemática do Ensino Médio orientada pela coleção Gelson Iezzi, alimentada por IA Socrática e Teoria de Resposta ao Item (TRI).
        </p>
        <div className="grid grid-cols-2 gap-3 text-left text-xs text-slate-300">
          <div className="p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
            <span className="text-slate-500 block">Frontend</span>
            <span className="font-mono text-indigo-400">Next.js 14 App Router</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
            <span className="text-slate-500 block">Backend</span>
            <span className="font-mono text-emerald-400">FastAPI + Python 3.11</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
            <span className="text-slate-500 block">Banco de Dados</span>
            <span className="font-mono text-cyan-400">PostgreSQL 16 + pgvector</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
            <span className="text-slate-500 block">Cache & Sessões</span>
            <span className="font-mono text-rose-400">Redis 7 Alpine</span>
          </div>
        </div>
      </div>
    </main>
  );
}
