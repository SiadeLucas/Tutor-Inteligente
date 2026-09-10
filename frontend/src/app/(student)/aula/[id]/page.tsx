"use client";

import React, { useState, useEffect, useRef } from "react";
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
} from "lucide-react";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { useStudyTimer } from "@/hooks/useStudyTimer";
import { GlobalHeader } from "@/components/header/GlobalHeader";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";
import { api, extrairMensagemErro } from "@/lib/api";
import {
  AulaCompleta,
  BateriaFixacao,
  SubmeterFixacaoResponse,
  ChatAulaResponse,
} from "@/types/content";

type TabType = "teoria" | "exemplos" | "dicas" | "fixacao";

interface MensagemChatLocal {
  id: string;
  autor: "aluno" | "tutor";
  texto: string;
  timestamp: string;
  chunks?: ChatAulaResponse["chunks_utilizados"];
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
      texto: "Olá! Sou seu Tutor Socrático. Estou acompanhando sua leitura nesta aula. Se tiver qualquer dúvida conceitual ou travar em um passo matemático, me pergunte!",
      timestamp: "Agora",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [estagioSocratico, setEstagioSocratico] = useState<1 | 2 | 3>(1);
  const [trechoSelecionado, setTrechoSelecionado] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

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

  const mudarAba = (tab: TabType) => {
    setActiveTab(tab);
    setAbasVisitadas((prev) => ({ ...prev, [tab]: true }));
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
          texto: "Neste momento estou organizando meus cadernos de anotações do Iezzi. Que tal reler a definição no Bloco 1 acima?",
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
          texto: `💡 **Pista Cirúrgica:**\n${data.pista_socratica_katex}\n\n*${data.dica_pegadinha || ""}*`,
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
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#1a1408] text-slate-900 dark:text-slate-100 flex flex-col">
      <GlobalHeader userRole="student" userName="Aluno" showDisciplineBadge={true} />

      {/* Subheader da Aula */}
      <div className="bg-white dark:bg-[#261d11] border-b border-slate-200/90 dark:border-[#3d2f1f] sticky top-14 z-30 px-4 sm:px-6 lg:px-8 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/materias"
              className="p-1.5 rounded-lg text-slate-500 hover:text-[#F57C00] hover:bg-slate-100 dark:hover:bg-[#332514] transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <div className="text-[11px] font-semibold text-[#F57C00] uppercase tracking-wider">
                Vol. {aula?.numero_volume || "1"}: {aula?.volume_titulo || "Fundamentos"} • Cap. {aula?.numero_capitulo || "1"}
              </div>
              <h1 className="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white truncate max-w-md sm:max-w-xl">
                {aula?.capitulo_titulo || "Carregando aula..."}
              </h1>
            </div>
          </div>

          {/* Cronômetro Compacto no Topo */}
          <div className="flex items-center gap-2 bg-[#FFF3E0] dark:bg-[#2b1f10] border border-[#FFB74D]/30 px-3 py-1.5 rounded-xl">
            <Clock className={`w-4 h-4 text-[#F57C00] ${timer.isActive ? "" : "opacity-40"}`} />
            <span className="font-mono font-bold text-xs text-[#E65100] dark:text-[#FFB74D]">
              {timer.formattedTime} / 50:00
            </span>
            <button
              onClick={timer.isActive ? timer.pause : timer.resume}
              className="p-1 rounded text-[#E65100] dark:text-[#FFB74D] hover:bg-[#FFE0B2] dark:hover:bg-[#3a2813] transition-colors ml-1"
              title={timer.isActive ? "Pausar cronômetro" : "Retomar cronômetro"}
            >
              {timer.isActive ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            </button>
          </div>
        </div>
      </div>

      {/* Split-Screen Principal */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading && (
          <div className="h-96 rounded-2xl bg-white dark:bg-[#261d11] border border-slate-200 dark:border-[#3d2f1f] animate-pulse flex items-center justify-center text-slate-400">
            Carregando material instrucional do Iezzi...
          </div>
        )}

        {error && (
          <div className="p-8 rounded-2xl bg-white dark:bg-[#261d11] border border-red-200 dark:border-red-900/40 text-center max-w-lg mx-auto my-12">
            <AlertTriangle className="w-10 h-10 text-red-500 mx-auto mb-3" />
            <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-2">Material não disponível</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">{error}</p>
            <Link
              href="/materias"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#F57C00] text-white font-bold text-sm shadow-sm"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Voltar à Árvore de Habilidades</span>
            </Link>
          </div>
        )}

        {!loading && !error && aula && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* PAINEL ESQUERDO (65% - 8 colunas de 12 em telas grandes) */}
            <div className="lg:col-span-8 bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl shadow-xs overflow-hidden flex flex-col">
              {/* Abas Pedagógicas dos 4 Blocos (com indicador de progresso) */}
              <div className="flex border-b border-slate-200 dark:border-[#382b1c] bg-slate-50/50 dark:bg-[#20180e] overflow-x-auto">
                {(
                  [
                    { key: "teoria", label: "1. Teoria & Formalismo", icon: BookOpen },
                    { key: "exemplos", label: "2. Exemplos Passo a Passo", icon: Sparkles },
                    { key: "dicas", label: "3. Dicas & Pegadinhas", icon: Lightbulb },
                    { key: "fixacao", label: "4. Fixação", icon: CheckCircle2 },
                  ] as const
                ).map((tab) => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.key;
                  return (
                    <button
                      key={tab.key}
                      onClick={() => mudarAba(tab.key)}
                      className={`px-5 py-3.5 text-xs sm:text-sm font-bold whitespace-nowrap border-b-2 transition-all flex items-center gap-2 ${
                        isActive
                          ? "border-[#F57C00] text-[#F57C00] bg-white dark:bg-[#261d11]"
                          : "border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white"
                      }`}
                    >
                      {abasVisitadas[tab.key] && !isActive ? (
                        <Check className="w-3.5 h-3.5 text-emerald-500" />
                      ) : (
                        <Icon className={`w-4 h-4 ${isActive ? "" : "opacity-60"}`} />
                      )}
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Conteúdo da Aba Ativa */}
              <div className="p-6 sm:p-8 min-h-[500px]">
                {activeTab === "teoria" && (
                  <div>
                    <KaTeXRenderer content={aula.bloco1_teoria_katex} />
                    <div className="mt-6 p-3 rounded-xl bg-orange-50/60 dark:bg-[#20180e] border border-orange-100 dark:border-[#382b1c] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                      <div className="flex items-center gap-2 text-slate-600 dark:text-slate-300">
                        <Sparkles className="w-4 h-4 text-[#F57C00] flex-shrink-0" />
                        <span>Ficou com dúvida neste passo? Selecione o texto e tire sua dúvida com o Tutor IA.</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => {
                          const selection = window.getSelection()?.toString().trim();
                          setTrechoSelecionado(selection || aula.capitulo_titulo || null);
                        }}
                        className="px-3 py-1.5 rounded-lg bg-[#FFF3E0] dark:bg-[#332514] text-[#E65100] dark:text-[#FFB74D] font-bold text-[11px] border border-[#FFB74D]/30 hover:bg-[#FFE0B2] transition-colors whitespace-nowrap"
                      >
                        Explicar este passo (IA)
                      </button>
                    </div>
                    <div className="mt-6 pt-6 border-t border-slate-100 dark:border-[#382b1c] flex justify-end">
                      <button
                        onClick={() => mudarAba("exemplos")}
                        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-xs shadow-sm transition-all"
                      >
                        <span>Avançar para Exemplos</span>
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}

                {activeTab === "exemplos" && (
                  <div>
                    <KaTeXRenderer content={aula.bloco2_exemplos_katex} />
                    <div className="mt-8 pt-6 border-t border-slate-100 dark:border-[#382b1c] flex justify-between">
                      <button
                        onClick={() => mudarAba("teoria")}
                        className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-[#A89F91] hover:bg-slate-100 dark:hover:bg-[#332514]"
                      >
                        Voltar à Teoria
                      </button>
                      <button
                        onClick={() => mudarAba("dicas")}
                        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-bold text-xs shadow-sm transition-all"
                      >
                        <span>Ver Dicas do Tutor</span>
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}

                {activeTab === "dicas" && (
                  <div>
                    <KaTeXRenderer content={aula.bloco3_dicas_ia} />
                    <div className="mt-8 pt-6 border-t border-slate-100 dark:border-[#382b1c] flex justify-between">
                      <button
                        onClick={() => mudarAba("exemplos")}
                        className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-[#A89F91] hover:bg-slate-100 dark:hover:bg-[#332514]"
                      >
                        Voltar aos Exemplos
                      </button>
                      <button
                        onClick={() => mudarAba("fixacao")}
                        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition-all"
                      >
                        <span>Ir para a Fixação</span>
                        <CheckCircle2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}

                {activeTab === "fixacao" && (
                  <div className="space-y-6">
                    <div className="p-4 rounded-xl bg-slate-50 dark:bg-[#20180e] border border-slate-200/80 dark:border-[#3d2f1f]">
                      <h3 className="font-bold text-slate-900 dark:text-white text-sm mb-1">
                        Bateria de Fixação do Iezzi
                      </h3>
                      <p className="text-xs text-slate-500 dark:text-[#A89F91]">
                        Responda as questões abaixo para validar a conclusão da aula. É necessário mínimo de{" "}
                        <strong>{bateria?.percentual_minimo ?? 60}% de acerto</strong>. A correção é feita no servidor.
                      </p>
                    </div>

                    {!bateria && (
                      <div className="p-5 rounded-xl border border-amber-300 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200 text-sm">
                        Bateria de fixação ainda não disponível para este capítulo. Use o botão
                        <strong> "Concluir Aula"</strong> abaixo para registrar sua conclusão manualmente.
                      </div>
                    )}

                    {/* Questões vindas do servidor (sem gabarito) */}
                    {bateria?.questoes.map((q) => {
                      const gabaritoQ = resultadoFixacao?.gabarito
                        ? resultadoFixacao.gabarito[String(q.numero)]
                        : undefined;
                      const acertou = gabaritoQ !== undefined && respostas[q.numero] === gabaritoQ;

                      return (
                        <div
                          key={q.numero}
                          className={`p-5 rounded-xl border bg-white dark:bg-[#261d11] ${
                            resultadoFixacao
                              ? acertou
                                ? "border-emerald-300 dark:border-emerald-800"
                                : "border-rose-300 dark:border-rose-800"
                              : "border-slate-200/80 dark:border-[#3d2f1f]"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1.5">
                            <div className="text-xs font-bold text-[#F57C00]">
                              Questão {String(q.numero).padStart(2, "0")} • Coleção Iezzi
                            </div>
                            {resultadoFixacao && (
                              acertou ? (
                                <Check className="w-4 h-4 text-emerald-600" />
                              ) : (
                                <XCircle className="w-4 h-4 text-rose-500" />
                              )
                            )}
                          </div>
                          <div className="text-sm text-slate-800 dark:text-slate-200 mb-4">
                            <KaTeXRenderer content={q.enunciado_katex} />
                          </div>
                          <div className="space-y-2">
                            {q.alternativas.map((alt, idx) => {
                              const isCorreta = resultadoFixacao && gabaritoQ === idx;
                              const isEscolhidaErrada =
                                resultadoFixacao && respostas[q.numero] === idx && !acertou;

                              return (
                                <button
                                  key={idx}
                                  onClick={() =>
                                    !resultadoFixacao &&
                                    setRespostas((prev) => ({ ...prev, [q.numero]: idx }))
                                  }
                                  disabled={!!resultadoFixacao}
                                  className={`w-full p-3 rounded-xl text-left text-xs sm:text-sm font-medium border transition-all flex items-center justify-between ${
                                    isCorreta
                                      ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-300"
                                      : isEscolhidaErrada
                                      ? "border-rose-400 bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-300"
                                      : respostas[q.numero] === idx
                                      ? "border-[#F57C00] bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D]"
                                      : "border-slate-200/70 dark:border-[#3d2f1f] hover:bg-slate-50 dark:hover:bg-[#20180e]"
                                  }`}
                                >
                                  <KaTeXRenderer content={alt} />
                                  {respostas[q.numero] === idx && !resultadoFixacao && (
                                    <Check className="w-4 h-4 text-[#F57C00] flex-shrink-0 ml-2" />
                                  )}
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}

                    {/* Feedback de Conclusão */}
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
                            <ShieldCheck className="w-5 h-5 text-emerald-600" />
                          ) : (
                            <AlertTriangle className="w-5 h-5 text-amber-600" />
                          )}
                          <span>
                            {resultadoFixacao.concluida
                              ? "Aula Concluída!"
                              : "Atenção Pedagógica"}{" "}
                            — {resultadoFixacao.percentual_acertos.toFixed(1)}%
                          </span>
                        </div>
                        <p className="text-xs leading-relaxed">{resultadoFixacao.mensagem}</p>
                        {resultadoFixacao.concluida && resultadoFixacao.proximo_capitulo_id && (
                          <Link
                            href={`/aula/${resultadoFixacao.proximo_capitulo_id}`}
                            className="inline-flex items-center gap-1.5 mt-3 text-xs font-bold text-emerald-700 dark:text-emerald-300 underline"
                          >
                            <span>Ir para o próximo capítulo</span>
                            <ChevronRight className="w-3.5 h-3.5" />
                          </Link>
                        )}
                      </div>
                    )}

                    {/* Botões de Ação */}
                    <div className="pt-4 flex items-center justify-between">
                      <button
                        onClick={() => mudarAba("dicas")}
                        className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-[#A89F91] hover:bg-slate-100 dark:hover:bg-[#332514]"
                      >
                        Voltar às Dicas
                      </button>

                      {bateria && !resultadoFixacao ? (
                        <button
                          onClick={handleSubmeterFixacao}
                          disabled={submetendo || !todasRespondidas}
                          title={todasRespondidas ? undefined : "Responda todas as questões antes de enviar"}
                          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-extrabold text-sm shadow-md shadow-orange-500/20 disabled:opacity-50 transition-all"
                        >
                          <CheckCircle2 className="w-4 h-4" />
                          <span>{submetendo ? "Corrigindo..." : "Enviar Respostas"}</span>
                        </button>
                      ) : (
                        !resultadoFixacao && (
                          <button
                            onClick={async () => {
                              try {
                                setSubmetendo(true);
                                const data = await api.post(
                                  `/api/v1/conteudo/aulas/${capituloId}/concluir`,
                                  { percentual_acertos: 100.0 }
                                );
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
                            disabled={submetendo}
                            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white font-extrabold text-sm shadow-md shadow-orange-500/20 disabled:opacity-50 transition-all"
                          >
                            <CheckCircle2 className="w-4 h-4" />
                            <span>{submetendo ? "Validando..." : "Concluir Aula (60%+)"}</span>
                          </button>
                        )
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* PAINEL DIREITO (35% - 4 colunas de 12 em telas grandes) - CHAT SOCRÁTICO */}
            <div className="lg:col-span-4 bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl shadow-xs flex flex-col h-[650px] sticky top-28">
              {/* Header do Chat */}
              <div className="p-4 border-b border-slate-200 dark:border-[#382b1c] bg-slate-50/70 dark:bg-[#20180e] flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#F57C00] flex items-center justify-center font-bold text-xs border border-[#FFB74D]/30">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-xs sm:text-sm text-slate-900 dark:text-white">Tutor Socrático IA</h3>
                    <p className="text-[10px] text-emerald-600 font-semibold">
                      Online • Base Iezzi Vol. {aula?.numero_volume || "1"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold border transition-colors ${
                      estagioSocratico === 1
                        ? "bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800"
                        : estagioSocratico === 2
                        ? "bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800"
                        : "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800"
                    }`}
                    title="Nível pedagógico socrático ativo"
                  >
                    {estagioSocratico === 1
                      ? "1. Reflexão"
                      : estagioSocratico === 2
                      ? "2. Pista"
                      : "3. Passo Guiado"}
                  </span>
                  <button
                    onClick={handlePedirPista}
                    disabled={chatLoading}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#FFF3E0] dark:bg-[#2b1f10] text-[#E65100] dark:text-[#FFB74D] text-[11px] font-bold border border-[#FFB74D]/30 hover:bg-[#FFE0B2] transition-colors disabled:opacity-50"
                    title="Pede uma pista matemática cirúrgica"
                  >
                    <Lightbulb className="w-3.5 h-3.5" />
                    <span>Pista</span>
                  </button>
                </div>
              </div>

              {/* Mensagens */}
              <div className="flex-1 p-4 overflow-y-auto space-y-3.5 scrollbar-thin">
                {chatMessages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex flex-col ${msg.autor === "aluno" ? "items-end" : "items-start"}`}
                  >
                    <div
                      className={`max-w-[88%] rounded-2xl p-3 text-xs leading-relaxed ${
                        msg.autor === "aluno"
                          ? "bg-[#F57C00] text-white rounded-tr-xs"
                          : "bg-slate-100 dark:bg-[#20180e] text-slate-800 dark:text-slate-200 rounded-tl-xs border border-slate-200/60 dark:border-[#382b1c]"
                      }`}
                    >
                      <KaTeXRenderer content={msg.texto} />

                      {/* Citações da base Iezzi (RAG) */}
                      {msg.chunks && msg.chunks.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-slate-200/70 dark:border-[#382b1c] space-y-1">
                          {msg.chunks.map((chunk, i) => (
                            <div
                              key={i}
                              className="flex items-start gap-1.5 text-[10px] text-slate-500 dark:text-[#A89F91] italic"
                            >
                              <Quote className="w-3 h-3 mt-0.5 flex-shrink-0" />
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
                    <span className="text-[9px] text-slate-400 mt-1 px-1">{msg.timestamp}</span>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 p-2 italic">
                    <Sparkles className="w-3.5 h-3.5 animate-spin text-[#F57C00]" />
                    <span>O tutor está consultando os teoremas...</span>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Input de Mensagem com Foco de Trecho */}
              <form
                onSubmit={handleSendMessage}
                className="p-3 border-t border-slate-200 dark:border-[#382b1c] bg-white dark:bg-[#261d11]"
              >
                {trechoSelecionado && (
                  <div className="mb-2 px-2.5 py-1.5 rounded-lg bg-[#FFF3E0] dark:bg-[#332514] border border-[#FFB74D]/40 flex items-center justify-between text-[11px] text-[#E65100] dark:text-[#FFB74D]">
                    <div className="flex items-center gap-1.5 truncate max-w-[85%]">
                      <Sparkles className="w-3 h-3 flex-shrink-0" />
                      <span className="truncate">Foco selecionado: <strong>{trechoSelecionado}</strong></span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setTrechoSelecionado(null)}
                      className="text-xs font-bold hover:text-red-500 px-1"
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
                    className="flex-1 px-3.5 py-2 text-xs rounded-xl border border-slate-200 dark:border-[#3d2f1f] bg-slate-50 dark:bg-[#1a1408] text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#F57C00]/40"
                  />
                  <button
                    type="submit"
                    disabled={!chatInput.trim() || chatLoading}
                    className="p-2 rounded-xl bg-[#F57C00] hover:bg-[#E65100] text-white disabled:opacity-40 transition-colors"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
