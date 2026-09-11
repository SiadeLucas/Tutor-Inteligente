"use client";

/**
 * /aula/[id] — Superfície de leitura (Fase 4: "Caderno de Foco").
 *
 * Layout revisado (RN-INT-007/008/009):
 * - Subheader sticky com breadcrumb + cronômetro + barra de progresso de leitura.
 * - Abas como segmented control; em mobile, tab bar inferior própria (âncoras).
 * - Leitura em medida única (~65ch) com tipografia sustentada.
 * - Chat socrático: slide-over em mobile (FAB), docked 35% em desktop.
 *
 * Lógica preservada integralmente:
 * - useStudyTimer com auto-sync (RN-PRG-003) — nunca enviar tempo na submissão.
 * - Estágios socráticos 1→2→3, pista cirúrgica, seleção de trecho (RAG).
 * - Bateria de fixação server-side: gabarito só vem após submissão (RN-CNT-010).
 */

import React, { useState, useEffect, useRef, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  ArrowLeft,
  BookOpen,
  Clock,
  CheckCircle2,
  Sparkles,
  AlertTriangle,
  Lightbulb,
  Check,
  ChevronRight,
  ShieldCheck,
  Quote,
  XCircle,
  Send,
  Pause,
  Play,
  MessageCircle,
  X,
} from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { useStudyTimer } from "@/hooks/useStudyTimer";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";
import { api, extrairMensagemErro } from "@/lib/api";
import {
  AulaCompleta,
  BateriaFixacao,
  SubmeterFixacaoResponse,
  ChatAulaResponse,
} from "@/types/content";

type TabType = "teoria" | "exemplos" | "dicas" | "fixacao";

const TABS: { key: TabType; label: string; short: string; icon: typeof BookOpen }[] = [
  { key: "teoria", label: "Teoria", short: "Teoria", icon: BookOpen },
  { key: "exemplos", label: "Exemplos", short: "Exemplos", icon: Sparkles },
  { key: "dicas", label: "Dicas", short: "Dicas", icon: Lightbulb },
  { key: "fixacao", label: "Fixação", short: "Fixação", icon: CheckCircle2 },
];

interface MensagemChatLocal {
  id: string;
  autor: "aluno" | "tutor";
  texto: string;
  timestamp: string;
  chunks?: ChatAulaResponse["chunks_utilizados"];
}

/** Chat socrático (usado docked no desktop e dentro do slide-over no mobile). */
function SocraticChat({
  aula,
  chatMessages,
  chatLoading,
  chatInput,
  setChatInput,
  handleSendMessage,
  handlePedirPista,
  estagioSocratico,
  trechoSelecionado,
  setTrechoSelecionado,
  chatEndRef,
  onClose,
}: {
  aula: AulaCompleta | null;
  chatMessages: MensagemChatLocal[];
  chatLoading: boolean;
  chatInput: string;
  setChatInput: (v: string) => void;
  handleSendMessage: (e?: React.FormEvent) => void;
  handlePedirPista: () => void;
  estagioSocratico: 1 | 2 | 3;
  trechoSelecionado: string | null;
  setTrechoSelecionado: (v: string | null) => void;
  chatEndRef: React.RefObject<HTMLDivElement>;
  onClose?: () => void;
}) {
  const estagioMeta = {
    1: { label: "1 · Reflexão", cls: "bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800" },
    2: { label: "2 · Pista", cls: "bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800" },
    3: { label: "3 · Passo guiado", cls: "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800" },
  }[estagioSocratico];

  return (
    <div className="flex flex-col h-full bg-surface-card">
      {/* Header */}
      <div className="px-4 py-3 border-b border-line flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-2.5">
          <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-subject-wash text-subject-600 dark:text-subject-400">
            <Sparkles className="w-4 h-4" aria-hidden="true" />
          </span>
          <div>
            <h3 className="font-bold text-xs sm:text-sm text-ink-text leading-tight">Tutor Socrático</h3>
            <p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true" />
              Base Iezzi Vol. {aula?.numero_volume || "1"}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5">
          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${estagioMeta.cls}`} title="Nível pedagógico socrático ativo">
            {estagioMeta.label}
          </span>
          <button
            onClick={handlePedirPista}
            disabled={chatLoading}
            className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-subject-wash text-subject-700 dark:text-subject-400 text-[11px] font-bold hover:bg-subject-100 dark:hover:bg-subject-wash-strong transition-colors disabled:opacity-50"
            title="Pede uma pista matemática cirúrgica"
          >
            <Lightbulb className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Pista</span>
          </button>
          {onClose && (
            <button
              onClick={onClose}
              aria-label="Fechar chat"
              className="p-2 -mr-2 rounded-lg text-ink-faint hover:text-ink-text hover:bg-surface-elevated transition-colors"
            >
              <X className="w-4 h-4" aria-hidden="true" />
            </button>
          )}
        </div>
      </div>

      {/* Mensagens */}
      <div className="flex-1 px-4 py-4 overflow-y-auto space-y-3.5">
        {chatMessages.map((msg) => (
          <div key={msg.id} className={`flex flex-col ${msg.autor === "aluno" ? "items-end" : "items-start"}`}>
            <div
              className={`max-w-[88%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed ${
                msg.autor === "aluno"
                  ? "bg-subject-500 text-white rounded-br-[4px]"
                  : "bg-surface-elevated text-ink-text rounded-bl-[4px] border border-line"
              }`}
            >
              <KaTeXRenderer content={msg.texto} />

              {/* Citações da base Iezzi (RAG) */}
              {msg.chunks && msg.chunks.length > 0 && (
                <div className="mt-2 pt-2 border-t border-line/70 space-y-1">
                  {msg.chunks.map((chunk, i) => (
                    <div key={i} className="flex items-start gap-1.5 text-[10px] text-ink-muted italic">
                      <Quote className="w-3 h-3 mt-0.5 flex-shrink-0" aria-hidden="true" />
                      <span>
                        {chunk.teorema_ou_topico}
                        {chunk.pagina ? ` — Vol. ${aula?.numero_volume || 1}, p. ${chunk.pagina}` : ""}
                        {" "}(relevância {(chunk.score_similaridade * 100).toFixed(0)}%)
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <span className="text-[9px] text-ink-faint mt-1 px-1">{msg.timestamp}</span>
          </div>
        ))}
        {chatLoading && (
          <div className="flex items-center gap-1.5 text-xs text-ink-faint p-2 italic">
            <Sparkles className="w-3.5 h-3.5 animate-spin text-subject-600" aria-hidden="true" />
            <span>O tutor está consultando os teoremas...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input com foco de trecho */}
      <form onSubmit={handleSendMessage} className="px-3 py-3 border-t border-line flex-shrink-0">
        {trechoSelecionado && (
          <div className="mb-2 px-2.5 py-1.5 rounded-lg bg-subject-wash border border-subject-200 flex items-center justify-between text-[11px] text-subject-700 dark:text-subject-400">
            <div className="flex items-center gap-1.5 truncate max-w-[85%]">
              <Sparkles className="w-3 h-3 flex-shrink-0" aria-hidden="true" />
              <span className="truncate">
                Foco: <strong>{trechoSelecionado}</strong>
              </span>
            </div>
            <button
              type="button"
              onClick={() => setTrechoSelecionado(null)}
              className="text-xs font-bold hover:text-rose-500 px-1"
              title="Remover foco"
            >
              ✕
            </button>
          </div>
        )}
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Tire uma dúvida sobre fórmulas ou passos..."
            className="flex-1 px-3.5 py-2.5 text-xs rounded-xl border border-line bg-surface-bg text-ink-text focus:outline-none focus:ring-2 focus:ring-subject-300"
          />
          <button
            type="submit"
            disabled={!chatInput.trim() || chatLoading}
            aria-label="Enviar mensagem"
            className="p-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white disabled:opacity-40 transition-colors"
          >
            <Send className="w-4 h-4" aria-hidden="true" />
          </button>
        </div>
      </form>
    </div>
  );
}

export default function AulaPage() {
  useHeartbeat();
  const params = useParams();
  const capituloId = params?.id as string;

  const [aula, setAula] = useState<AulaCompleta | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>("teoria");
  const [abasVisitadas, setAbasVisitadas] = useState<Record<TabType, boolean>>({
    teoria: true,
    exemplos: false,
    dicas: false,
    fixacao: false,
  });

  // Cronômetro de Estudo (tempo líquido ativo, enviado ao servidor na submissão)
  const timer = useStudyTimer(60);

  // Chat Socrático Local
  const [chatMessages, setChatMessages] = useState<MensagemChatLocal[]>([
    {
      id: "1",
      autor: "tutor",
      texto:
        "Olá! Sou seu Tutor Socrático. Estou acompanhando sua leitura nesta aula. Se tiver qualquer dúvida conceitual ou travar em um passo matemático, me pergunte!",
      timestamp: "Agora",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [estagioSocratico, setEstagioSocratico] = useState<1 | 2 | 3>(1);
  const [trechoSelecionado, setTrechoSelecionado] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [chatAberto, setChatAberto] = useState(false);

  // Bateria de Fixação Server-Side
  const [bateria, setBateria] = useState<BateriaFixacao | null>(null);
  const [respostas, setRespostas] = useState<Record<number, number>>({});
  const [submetendo, setSubmetendo] = useState(false);
  const [resultadoFixacao, setResultadoFixacao] = useState<SubmeterFixacaoResponse | null>(null);

  // Rolar chat para o fim ao receber mensagens
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [chatMessages, chatLoading]);

  // Carregar conteúdo da aula + bateria de fixação
  useEffect(() => {
    async function loadAula() {
      if (!capituloId) return;
      try {
        setLoading(true);
        const data: AulaCompleta = await api.get(`/api/v1/conteudo/aulas/${capituloId}`);
        setAula(data);

        // Bateria server-side (pode não existir para todos os capítulos ainda)
        try {
          const bateriaData: BateriaFixacao = await api.get(
            `/api/v1/conteudo/aulas/${capituloId}/fixacao`
          );
          setBateria(bateriaData);
        } catch {
          setBateria(null);
        }
      } catch (err: any) {
        setError(extrairMensagemErro(err, "Aula ainda não disponibilizada para este capítulo."));
      } finally {
        setLoading(false);
      }
    }
    loadAula();
  }, [capituloId]);

  // Barra de progresso de leitura (topo da página)
  const [progressoPct, setProgressoPct] = useState(0);
  const progressoLeitura = useMemo(() => {
    if (typeof window === "undefined") return 0;
    const doc = document.documentElement;
    const total = doc.scrollHeight - window.innerHeight;
    return total > 0 ? Math.min(100, (window.scrollY / total) * 100) : 0;
  }, [activeTab, aula]);

  useEffect(() => {
    const onScroll = () => {
      const doc = document.documentElement;
      const total = doc.scrollHeight - window.innerHeight;
      setProgressoPct(total > 0 ? Math.min(100, (window.scrollY / total) * 100) : 0);
    };
    setProgressoPct(progressoLeitura);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [progressoLeitura]);

  const mudarAba = (tab: TabType) => {
    setActiveTab(tab);
    setAbasVisitadas((prev) => ({ ...prev, [tab]: true }));
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Enviar mensagem ao chat socrático
  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!chatInput.trim() || chatLoading) return;

    const userText = chatInput.trim();
    setChatInput("");
    const newMsgId = String(Date.now());

    setChatMessages((prev) => [
      ...prev,
      { id: newMsgId, autor: "aluno", texto: userText, timestamp: "Agora" },
    ]);

    const historicoRecente = chatMessages.slice(-6).map((m) => ({
      papel: m.autor === "aluno" ? "user" : "assistant",
      conteudo: m.texto,
    }));

    try {
      setChatLoading(true);
      const data: ChatAulaResponse = await api.post(
        `/api/v1/conteudo/aulas/${capituloId}/chat`,
        {
          capitulo_id: capituloId,
          mensagem: userText,
          trecho_selecionado: trechoSelecionado || undefined,
          historico_recente: historicoRecente,
        }
      );
      if (data.nivel_ajuda_socratico) {
        setEstagioSocratico(data.nivel_ajuda_socratico);
      }
      setChatMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 1),
          autor: "tutor",
          texto: data.resposta_katex,
          timestamp: "Agora",
          chunks: data.chunks_utilizados,
        },
      ]);
    } catch (err) {
      setChatMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 1),
          autor: "tutor",
          texto:
            "Neste momento estou organizando meus cadernos de anotações do Iezzi. Que tal reler a definição no Bloco 1 acima?",
          timestamp: "Agora",
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  // Pedir pista cirúrgica
  const handlePedirPista = async () => {
    try {
      setChatLoading(true);
      const data = await api.post<{ pista_socratica_katex: string; dica_pegadinha?: string }>(
        `/api/v1/conteudo/aulas/${capituloId}/pista`,
        { capitulo_id: capituloId }
      );
      setChatMessages((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          autor: "tutor",
          texto: `**Pista Cirúrgica:**\n${data.pista_socratica_katex}\n\n*${data.dica_pegadinha || ""}*`,
          timestamp: "Agora",
        },
      ]);
    } catch (e) {
      // ignore
    } finally {
      setChatLoading(false);
    }
  };

  // Submeter bateria de fixação (correção server-side + persistência de progresso)
  const handleSubmeterFixacao = async () => {
    if (!bateria || submetendo) return;
    try {
      setSubmetendo(true);
      const data: SubmeterFixacaoResponse = await api.post(
        `/api/v1/conteudo/aulas/${capituloId}/fixacao`,
        {
          respostas: respostas,
          // RN-PRG-003: o tempo líquido ativo é persistido EXCLUSIVAMENTE pelo
          // auto-sync do useStudyTimer (POST /progresso/tempo-estudo). Nunca
          // enviar segundos aqui: causaria contagem dupla na Tabela 17.
        }
      );
      setResultadoFixacao(data);
      timer.reset();
    } catch (err: any) {
      alert(extrairMensagemErro(err, "Erro ao enviar respostas da fixação."));
    } finally {
      setSubmetendo(false);
    }
  };

  const todasRespondidas = bateria
    ? bateria.questoes.every((q) => respostas[q.numero] !== undefined)
    : false;

  return (
    <div className="min-h-screen text-slate-900 dark:text-slate-100">
      {/* ── Barra de progresso de leitura (topo absoluto da página) ── */}
      <div
        className="fixed top-0 left-0 right-0 h-0.5 z-50 pointer-events-none"
        aria-hidden="true"
      >
        <div
          className="h-full bg-subject-500 transition-[width] duration-150 ease-out"
          style={{ width: `${progressoPct}%` }}
        />
      </div>

      {/* ── Subheader sticky (breadcrumb + timer + progresso de blocos) ── */}
      <div className="sticky top-14 z-30 border-b border-line bg-surface-card/95 backdrop-blur supports-[backdrop-filter]:bg-surface-card/90">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-2.5 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 min-w-0">
            <Link
              href="/materias"
              aria-label="Voltar para Árvore de Habilidades"
              className="p-1.5 -ml-1.5 rounded-lg text-ink-faint hover:text-ink-text hover:bg-surface-elevated transition-colors flex-shrink-0"
            >
              <ArrowLeft className="w-5 h-5" aria-hidden="true" />
            </Link>
            <div className="min-w-0">
              <p className="text-[10px] font-bold uppercase tracking-widest text-subject-600 dark:text-subject-400 truncate">
                Vol. {aula?.numero_volume || "1"} · {aula?.volume_titulo || "Fundamentos"} · Cap. {aula?.numero_capitulo || "1"}
              </p>
              <h1 className="font-bold text-sm truncate text-ink-text">
                {aula?.capitulo_titulo || "Carregando aula..."}
              </h1>
            </div>
          </div>

          {/* Cronômetro compacto */}
          <div className="flex items-center gap-1.5 bg-subject-wash border border-subject-200/70 px-2.5 py-1.5 rounded-lg flex-shrink-0">
            <Clock
              className={`w-3.5 h-3.5 text-subject-600 dark:text-subject-400 ${timer.isActive ? "" : "opacity-40"}`}
              aria-hidden="true"
            />
            <span className="font-mono font-bold text-[11px] text-subject-700 dark:text-subject-400 tabular-nums">
              {timer.formattedTime}
            </span>
            <button
              onClick={timer.isActive ? timer.pause : timer.resume}
              aria-label={timer.isActive ? "Pausar cronômetro" : "Retomar cronômetro"}
              className="p-1 rounded text-subject-700 dark:text-subject-400 hover:bg-subject-100 dark:hover:bg-subject-wash-strong transition-colors"
            >
              {timer.isActive ? <Pause className="w-3 h-3" aria-hidden="true" /> : <Play className="w-3 h-3" aria-hidden="true" />}
            </button>
          </div>
        </div>

        {/* Progresso de blocos visitados (4 dots) */}
        <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-2 flex items-center gap-1.5">
          {TABS.map((t) => (
            <span
              key={t.key}
              className={`h-1 flex-1 rounded-full transition-colors ${
                abasVisitadas[t.key] ? "bg-subject-400" : "bg-line"
              }`
              }
              aria-hidden="true"
            />
          ))}
        </div>
      </div>

      <main className="flex-1">
        {loading && (
          <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10" aria-busy="true">
            <div className="rounded-2xl border border-line bg-surface-card p-8 space-y-4">
              {[100, 92, 96, 85].map((w, i) => (
                <div
                  key={i}
                  className="h-4 rounded-full bg-surface-elevated animate-pulse"
                  style={{ width: `${w}%` }}
                />
              ))}
              <div className="h-32 rounded-xl bg-surface-elevated animate-pulse" />
              {[94, 88, 70].map((w, i) => (
                <div
                  key={`b${i}`}
                  className="h-4 rounded-full bg-surface-elevated animate-pulse"
                  style={{ width: `${w}%` }}
                />
              ))}
            </div>
          </div>
        )}

        {!loading && error && (
          <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
            <div className="rounded-2xl border border-line bg-surface-card p-10 text-center">
              <div className="w-16 h-16 rounded-2xl bg-subject-wash text-subject-600 flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-8 h-8" aria-hidden="true" />
              </div>
              <div className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 dark:bg-surface-elevated text-ink-muted border border-line mb-3">
                Conteúdo em Curadoria
              </div>
              <h2 className="text-xl font-extrabold mb-2 tracking-tight">Capítulo em Desenvolvimento</h2>
              <p className="text-sm text-ink-muted max-w-md mx-auto mb-6">
                {error} Este capítulo pertence ao acervo oficial da Coleção Gelson Iezzi. O material em 4 blocos
                pedagógicos está sendo preparado pela nossa equipe.
              </p>
              <Link
                href="/materias"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-sm transition-colors"
              >
                <ArrowLeft className="w-4 h-4" aria-hidden="true" />
                <span>Voltar para Árvore de Habilidades</span>
              </Link>
            </div>
          </div>
        )}

        {!loading && !error && aula && (
          <div className="max-w-5xl mx-auto px-4 sm:px-6 pt-4 pb-10">
            {/* Abas como segmented control (desktop+mobile topo) */}
            <div
              role="tablist"
              aria-label="Blocos pedagógicos da aula"
              className="sticky top-[7.75rem] z-20 mb-5 flex items-center gap-1 p-1 rounded-xl bg-surface-card border border-line overflow-x-auto scrollbar-none"
            >
              {TABS.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.key;
                return (
                  <button
                    key={tab.key}
                    role="tab"
                    aria-selected={isActive}
                    onClick={() => mudarAba(tab.key)}
                    className={`flex-1 min-w-[7.5rem] inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg text-xs font-bold whitespace-nowrap transition-colors ${
                      isActive
                        ? "bg-subject-500 text-white shadow-sm"
                        : "text-ink-muted hover:text-ink-text hover:bg-surface-elevated"
                    }`}
                  >
                    {abasVisitadas[tab.key] && !isActive ? (
                      <Check className="w-3.5 h-3.5 text-emerald-500" aria-hidden="true" /> 
                    ) : (
                      <Icon className="w-3.5 h-3.5" aria-hidden="true" />
                    )}
                    <span>{tab.short}</span>
                    {tab.key === "fixacao" && bateria && (
                      <span className="text-[9px] font-black opacity-80">{bateria.questoes.length}</span>
                    )}
                  </button>
                );
              })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* ── Superfície de leitura (65%) ── */}
              <article className="lg:col-span-8 rounded-2xl border border-line bg-surface-card">
                <div className="px-5 sm:px-8 py-6 sm:py-8 max-w-[65ch] min-h-[420px]">
                  {activeTab === "teoria" && (
                    <div>
                      <KaTeXRenderer content={aula.bloco1_teoria_katex} />
                      <div className="mt-8 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
                        <button
                          type="button"
                          onClick={() => {
                            const selection = window.getSelection()?.toString().trim();
                            setTrechoSelecionado(selection || aula.capitulo_titulo || null);
                            setChatAberto(true);
                          }}
                          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-subject-wash text-subject-700 dark:text-subject-400 font-bold text-xs border border-subject-200 hover:bg-subject-100 dark:hover:bg-subject-wash-strong transition-colors"
                        >
                          <Sparkles className="w-4 h-4" aria-hidden="true" />
                          <span>Explicar este passo (IA)</span>
                        </button>
                        <button
                          onClick={() => mudarAba("exemplos")}
                          className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs transition-colors"
                        >
                          <span>Avançar para Exemplos</span>
                          <ChevronRight className="w-4 h-4" aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  )}

                  {activeTab === "exemplos" && (
                    <div>
                      <KaTeXRenderer content={aula.bloco2_exemplos_katex} />
                      <div className="mt-8 flex justify-between gap-3">
                        <button
                          onClick={() => mudarAba("teoria")}
                          className="px-4 py-2 rounded-xl text-xs font-semibold text-ink-muted hover:bg-surface-elevated transition-colors"
                        >
                          Voltar à Teoria
                        </button>
                        <button
                          onClick={() => mudarAba("dicas")}
                          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs transition-colors"
                        >
                          <span>Ver Dicas do Tutor</span>
                          <ChevronRight className="w-4 h-4" aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  )}

                  {activeTab === "dicas" && (
                    <div>
                      <KaTeXRenderer content={aula.bloco3_dicas_ia} />
                      <div className="mt-8 flex justify-between gap-3">
                        <button
                          onClick={() => mudarAba("exemplos")}
                          className="px-4 py-2 rounded-xl text-xs font-semibold text-ink-muted hover:bg-surface-elevated transition-colors"
                        >
                          Voltar aos Exemplos
                        </button>
                        <button
                          onClick={() => mudarAba("fixacao")}
                          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition-colors"
                        >
                          <span>Ir para a Fixação</span>
                          <CheckCircle2 className="w-4 h-4" aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  )}

                  {activeTab === "fixacao" && (
                    <FixacaoBateria
                      bateria={bateria}
                      respostas={respostas}
                      setRespostas={setRespostas}
                      resultadoFixacao={resultadoFixacao}
                      submetendo={submetendo}
                      todasRespondidas={todasRespondidas}
                      capituloId={capituloId}
                      onSubmeter={handleSubmeterFixacao}
                      onVoltar={() => mudarAba("dicas")}
                      onConcluirManual={async () => {
                        try {
                          setSubmetendo(true);
                          const data = await api.post(`/api/v1/conteudo/aulas/${capituloId}/concluir`, {
                            percentual_acertos: 100.0,
                          });
                          setResultadoFixacao({
                            sucesso: data.sucesso,
                            percentual_acertos: data.percentual_atingido,
                            percentual_minimo: 60,
                            concluida: data.concluida,
                            mensagem: data.mensagem,
                            gabarito: {},
                            proximo_capitulo_id: data.proximo_capitulo_id,
                          });
                          timer.reset();
                        } catch (err: any) {
                          alert(extrairMensagemErro(err, "Erro ao concluir aula."));
                        } finally {
                          setSubmetendo(false);
                        }
                      }}
                      setResultadoFixacao={setResultadoFixacao}
                    />
                  )}
                </div>
              </article>

              {/* ── Chat docked (desktop ≥lg) ── */}
              <aside className="hidden lg:flex lg:col-span-4 flex-col rounded-2xl border border-line bg-surface-card overflow-hidden h-[min(720px,calc(100vh-11rem))] sticky top-[10.5rem]">
                <SocraticChat
                  aula={aula}
                  chatMessages={chatMessages}
                  chatLoading={chatLoading}
                  chatInput={chatInput}
                  setChatInput={setChatInput}
                  handleSendMessage={handleSendMessage}
                  handlePedirPista={handlePedirPista}
                  estagioSocratico={estagioSocratico}
                  trechoSelecionado={trechoSelecionado}
                  setTrechoSelecionado={setTrechoSelecionado}
                  chatEndRef={chatEndRef}
                />
              </aside>
            </div>
          </div>
        )}
      </main>

      {/* ── Chat mobile: FAB + slide-over ── */}
      {!loading && !error && aula && (
        <>
          <button
            onClick={() => setChatAberto(true)}
            aria-label="Abrir Tutor Socrático"
            className="lg:hidden fixed right-4 z-40 flex items-center justify-center w-14 h-14 rounded-full bg-subject-500 text-white shadow-lg shadow-subject-500/25 active:scale-95 transition-transform"
            style={{ bottom: "calc(4.25rem + env(safe-area-inset-bottom))" }}
          >
            <MessageCircle className="w-6 h-6" aria-hidden="true" />
          </button>

          {chatAberto && (
            <div className="lg:hidden fixed inset-0 z-50 flex" role="dialog" aria-modal="true" aria-label="Tutor Socrático">
              <button
                aria-label="Fechar chat"
                onClick={() => setChatAberto(false)}
                className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm"
              />
              <div
                className="relative ml-auto w-full max-w-md h-full bg-surface-card shadow-2xl flex flex-col animate-slide-in-right"
                style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
              >
                <SocraticChat
                  aula={aula}
                  chatMessages={chatMessages}
                  chatLoading={chatLoading}
                  chatInput={chatInput}
                  setChatInput={setChatInput}
                  handleSendMessage={handleSendMessage}
                  handlePedirPista={handlePedirPista}
                  estagioSocratico={estagioSocratico}
                  trechoSelecionado={trechoSelecionado}
                  setTrechoSelecionado={setTrechoSelecionado}
                  chatEndRef={chatEndRef}
                  onClose={() => setChatAberto(false)}
                />
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

/* ═══════════════════════════ Bateria de Fixação ═══════════════════════════ */

function FixacaoBateria({
  bateria,
  respostas,
  setRespostas,
  resultadoFixacao,
  submetendo,
  todasRespondidas,
  capituloId,
  onSubmeter,
  onVoltar,
  onConcluirManual,
  setResultadoFixacao,
}: {
  bateria: BateriaFixacao | null;
  respostas: Record<number, number>;
  setRespostas: React.Dispatch<React.SetStateAction<Record<number, number>>>;
  resultadoFixacao: SubmeterFixacaoResponse | null;
  submetendo: boolean;
  todasRespondidas: boolean;
  capituloId: string;
  onSubmeter: () => void;
  onVoltar: () => void;
  onConcluirManual: () => Promise<void>;
  setResultadoFixacao: React.Dispatch<React.SetStateAction<SubmeterFixacaoResponse | null>>;
}) {
  return (
    <div className="space-y-5">
      <div className="p-4 rounded-xl bg-surface-elevated border border-line">
        <h3 className="font-bold text-sm mb-1 text-ink-text">Bateria de Fixação do Iezzi</h3>
        <p className="text-xs text-ink-muted">
          Responda as questões para validar a conclusão. Mínimo de{" "}
          <strong>{bateria?.percentual_minimo ?? 60}% de acerto</strong>. A correção é feita no servidor.
        </p>
      </div>

      {!bateria && (
        <div className="p-5 rounded-xl border border-amber-300 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200 text-sm">
          Bateria de fixação ainda não disponível para este capítulo. Use o botão
          <strong> "Concluir Aula"</strong> abaixo para registrar sua conclusão manualmente.
        </div>
      )}

      {bateria?.questoes.map((q) => {
        const gabaritoQ = resultadoFixacao?.gabarito ? resultadoFixacao.gabarito[String(q.numero)] : undefined;
        const acertou = gabaritoQ !== undefined && respostas[q.numero] === gabaritoQ;

        return (
          <div
            key={q.numero}
            className={`p-5 rounded-xl border bg-surface-card ${
              resultadoFixacao
                ? acertou
                  ? "border-emerald-300 dark:border-emerald-800"
                  : "border-rose-300 dark:border-rose-800"
                : "border-line"
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <div className="text-xs font-bold text-subject-600 dark:text-subject-400">
                Questão {String(q.numero).padStart(2, "0")} · Coleção Iezzi
              </div>
              {resultadoFixacao &&
                (acertou ? (
                  <Check className="w-4 h-4 text-emerald-600" aria-hidden="true" />
                ) : (
                  <XCircle className="w-4 h-4 text-rose-500" aria-hidden="true" />
                ))}
            </div>
            <div className="text-sm mb-4 text-ink-text">
              <KaTeXRenderer content={q.enunciado_katex} />
            </div>
            <div className="space-y-2">
              {q.alternativas.map((alt, idx) => {
                const isCorreta = resultadoFixacao && gabaritoQ === idx;
                const isEscolhidaErrada = resultadoFixacao && respostas[q.numero] === idx && !acertou;

                return (
                  <button
                    key={idx}
                    onClick={() => !resultadoFixacao && setRespostas((prev) => ({ ...prev, [q.numero]: idx }))}
                    disabled={!!resultadoFixacao}
                    className={`w-full p-3 rounded-xl text-left text-xs sm:text-sm font-medium border transition-colors flex items-center justify-between ${
                      isCorreta
                        ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-300"
                        : isEscolhidaErrada
                        ? "border-rose-400 bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-300"
                        : respostas[q.numero] === idx
                        ? "border-subject-500 bg-subject-wash text-subject-700 dark:text-subject-400"
                        : "border-line hover:bg-surface-elevated"
                    }`}
                  >
                    <KaTeXRenderer content={alt} />
                    {respostas[q.numero] === idx && !resultadoFixacao && (
                      <Check className="w-4 h-4 text-subject-600 flex-shrink-0 ml-2" aria-hidden="true" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}

      {/* Feedback de conclusão */}
      {resultadoFixacao && (
        <div
          className={`p-5 rounded-xl border ${
            resultadoFixacao.concluida
              ? "bg-emerald-50 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200"
              : "bg-amber-50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200"
          }`}
        >
          <div className="flex items-center gap-2 font-bold text-sm mb-1">
            {resultadoFixacao.concluida ? (
              <ShieldCheck className="w-5 h-5 text-emerald-600" aria-hidden="true" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-amber-600" aria-hidden="true" />
            )}
            <span>
              {resultadoFixacao.concluida ? "Aula Concluída!" : "Atenção Pedagógica"} —{" "}
              {resultadoFixacao.percentual_acertos.toFixed(1)}%
            </span>
          </div>
          <p className="text-xs leading-relaxed">{resultadoFixacao.mensagem}</p>
          {resultadoFixacao.concluida && resultadoFixacao.proximo_capitulo_id && (
            <Link
              href={`/aula/${resultadoFixacao.proximo_capitulo_id}`}
              className="inline-flex items-center gap-1.5 mt-3 text-xs font-bold text-emerald-700 dark:text-emerald-300 underline"
            >
              <span>Ir para o próximo capítulo</span>
              <ChevronRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          )}
        </div>
      )}

      {/* Ações */}
      <div className="pt-2 flex items-center justify-between gap-3">
        <button
          onClick={onVoltar}
          className="px-4 py-2 rounded-xl text-xs font-semibold text-ink-muted hover:bg-surface-elevated transition-colors"
        >
          Voltar às Dicas
        </button>

        {bateria && !resultadoFixacao ? (
          <button
            onClick={onSubmeter}
            disabled={submetendo || !todasRespondidas}
            title={todasRespondidas ? undefined : "Responda todas as questões antes de enviar"}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-extrabold text-sm disabled:opacity-50 transition-colors min-h-[48px]"
          >
            <CheckCircle2 className="w-4 h-4" aria-hidden="true" />
            <span>{submetendo ? "Corrigindo..." : "Enviar Respostas"}</span>
          </button>
        ) : (
          !resultadoFixacao && (
            <button
              onClick={onConcluirManual}
              disabled={submetendo}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-extrabold text-sm disabled:opacity-50 transition-colors min-h-[48px]"
            >
              <CheckCircle2 className="w-4 h-4" aria-hidden="true" />
              <span>{submetendo ? "Validando..." : "Concluir Aula (60%+)"}</span>
            </button>
          )
        )}
      </div>
    </div>
  );
}
