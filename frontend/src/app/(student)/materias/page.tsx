"use client";

/**
 * /materias — Árvore de Habilidades (Fase 3: "Caderno de Foco").
 *
 * Design system revisado (RN-INT-001/007):
 * - Header tipográfico flat (sem banner-card): uma única superfície por tela.
 * - Mastery strip por volume: células na cor canônica do heatmap (RN-PRG-012)
 *   — leitura de domínio de um relance, sem abrir nada.
 * - Capítulos como linhas com hairlines (fim do card-in-card).
 * - Stats com tabular-nums (números não "tremer" ao atualizar).
 * - Toda a cor via tokens (subject/ink/surface/line) — laranja = Matemática,
 *   mas a página é agnóstica de disciplina.
 *
 * Lógica de dados preservada: skill-tree, pendências CAT/Reforço, filtro por
 * grande área, expansão de volumes (Volume 1 aberto por padrão).
 */

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  Clock,
  AlertCircle,
  Sparkles,
  Layers,
  Compass,
  Grid,
  TrendingUp,
  PenLine,
  Inbox,
  ClipboardList,
  ChevronDown,
  Sigma,
  Lock,
} from "lucide-react";
import { ItemCaixaReforco } from "@/types/exercise";
import { useHeartbeat } from "@/hooks/useHeartbeat";
import { VolumeComCapitulos, SkillTreeNode } from "@/types/content";
import { CheckoutModal } from "@/components/payment/CheckoutModal";
import { TipoProduto } from "@/types/payment";
import { api, extrairMensagemErro } from "@/lib/api";

const GRANDES_AREAS = [
  { key: "todas", label: "Todas as Áreas", icon: Layers },
  { key: "algebra_funcoes", label: "Álgebra e Funções", icon: TrendingUp },
  { key: "geometria", label: "Geometria e Trigonometria", icon: Compass },
  { key: "algebra_linear", label: "Álgebra Linear", icon: Grid },
  { key: "aplicada", label: "Matemática Aplicada", icon: Sparkles },
];

/** Cores canônicas do heatmap (RN-PRG-012) — semânticas, não tematizadas. */
function heatmapClasses(cor: string): { cell: string; label: string } {
  switch (cor) {
    case "green":
      return { cell: "bg-emerald-500", label: "Domínio consolidado" };
    case "yellow":
      return { cell: "bg-amber-400", label: "Domínio em progresso" };
    case "red":
      return { cell: "bg-rose-500", label: "Precisa de reforço" };
    default:
      return { cell: "bg-slate-200 dark:bg-slate-700", label: "Não iniciado" };
  }
}

export default function MateriasPage() {
  useHeartbeat();

  const [volumes, setVolumes] = useState<VolumeComCapitulos[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedArea, setSelectedArea] = useState<string>("todas");
  const [expandedVolumes, setExpandedVolumes] = useState<Record<string, boolean>>({});
  const [reforcoPendentes, setReforcoPendentes] = useState(0);
  const [catPendente, setCatPendente] = useState(false);

  // Modal de Checkout In-App (Etapa 9)
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [checkoutData, setCheckoutData] = useState<{
    tipoProduto: TipoProduto;
    referenciaId?: string;
    titulo: string;
    preco: number;
  }>({
    tipoProduto: "capitulo_50min",
    titulo: "",
    preco: 9.90,
  });

  const abrirCheckoutCapitulo = (cap: SkillTreeNode) => {
    setCheckoutData({
      tipoProduto: "capitulo_50min",
      referenciaId: cap.id,
      titulo: `Capítulo ${cap.numero_capitulo}: ${cap.titulo}`,
      preco: 9.90,
    });
    setCheckoutOpen(true);
  };

  const abrirCheckoutVolume = (vol: VolumeComCapitulos) => {
    setCheckoutData({
      tipoProduto: "volume_iezzi",
      referenciaId: vol.id,
      titulo: `Volume ${vol.numero_volume}: ${vol.titulo}`,
      preco: 49.90,
    });
    setCheckoutOpen(true);
  };

  const abrirCheckoutPasseGlobal = () => {
    setCheckoutData({
      tipoProduto: "passe_global",
      referenciaId: undefined,
      titulo: "Passe Global Ilimitado (11 Volumes + Tutoria IA)",
      preco: 199.00,
    });
    setCheckoutOpen(true);
  };

  const loadSkillTree = async () => {
    try {
      setLoading(true);
      const data: VolumeComCapitulos[] = await api.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica"
      );
      setVolumes(data);
      if (data.length > 0 && Object.keys(expandedVolumes).length === 0) {
        setExpandedVolumes({ [data[0].id]: true });
      }
    } catch (err: any) {
      setError(extrairMensagemErro(err, "Não foi possível carregar a árvore de conteúdos."));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    async function loadPendencias() {
      try {
        const caixa: ItemCaixaReforco[] = await api.get("/api/v1/exercicios/caixa-reforco");
        setReforcoPendentes(caixa.length);
      } catch {
        setReforcoPendentes(0);
      }
      try {
        const historico = await api.get("/api/v1/exercicios/cat/historico");
        setCatPendente(historico.length === 0);
      } catch {
        setCatPendente(false);
      }
    }
    loadPendencias();
  }, []);

  useEffect(() => {
    loadSkillTree();
  }, []);

  const toggleVolume = (volId: string) => {
    setExpandedVolumes((prev) => ({ ...prev, [volId]: !prev[volId] }));
  };

  const filteredVolumes = useMemo(() => {
    if (selectedArea === "todas") return volumes;
    return volumes.filter((v) => v.grande_area === selectedArea);
  }, [volumes, selectedArea]);

  const totalCapitulosGeral = useMemo(() => {
    return volumes.reduce((acc, v) => acc + (v.capitulos?.length || 0), 0);
  }, [volumes]);

  const progressoGeral = useMemo(() => {
    const todos = volumes.flatMap((v) => v.capitulos || []);
    if (todos.length === 0) return 0;
    const concluidos = todos.filter((c) => c.status_dominio === "mastered").length;
    return Math.round((concluidos / todos.length) * 100);
  }, [volumes]);

  return (
    <div className="text-slate-900 dark:text-slate-100">
      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {/* ── Header tipográfico flat (sem banner-card) ─────────────────── */}
        <header className="mb-6">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-widest text-subject-600 dark:text-subject-400">
            <Sigma className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Matemática · Coleção Gelson Iezzi</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight mt-1.5">
            Árvore de Habilidades
          </h1>
          <p className="text-sm text-slate-500 dark:text-ink-muted mt-1.5 leading-relaxed max-w-xl">
            Sessões focadas de <strong className="font-semibold text-slate-700 dark:text-slate-300">50 minutos</strong> com
            tutoria socrática. A cor de cada célula mostra seu domínio — passe o mouse para detalhes.
          </p>

          {/* Stats inline, tabular-nums */}
          <div className="flex items-baseline gap-5 mt-4 tabular-nums">
            <div>
              <span className="text-xl font-extrabold text-subject-600 dark:text-subject-400">{volumes.length}</span>
              <span className="text-xs text-ink-faint ml-1.5">volumes</span>
            </div>
            <div>
              <span className="text-xl font-extrabold">{totalCapitulosGeral}</span>
              <span className="text-xs text-ink-faint ml-1.5">capítulos</span>
            </div>
            <div>
              <span className="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">{progressoGeral}%</span>
              <span className="text-xs text-ink-faint ml-1.5">domínio</span>
            </div>
          </div>

          {/* Filtro por Grande Área */}
          <div className="flex items-center gap-2 mt-5 -mx-4 px-4 overflow-x-auto scrollbar-none sm:mx-0 sm:px-0">
            {GRANDES_AREAS.map((area) => {
              const Icon = area.icon;
              const isSelected = selectedArea === area.key;
              return (
                <button
                  key={area.key}
                  onClick={() => setSelectedArea(area.key)}
                  aria-pressed={isSelected}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${
                    isSelected
                      ? "bg-subject-500 text-white"
                      : "bg-surface-elevated text-ink-muted hover:text-ink-text border border-transparent hover:border-line"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>{area.label}</span>
                </button>
              );
            })}
          </div>
        </header>

        {/* ── Callouts (CAT pendente / Reforço) ─────────────────────────── */}
        {!loading && catPendente && (
          <Link
            href="/onboarding/cat"
            className="mb-3 flex items-center justify-between gap-4 px-4 py-3.5 rounded-xl bg-subject-wash border border-subject-200 dark:border-transparent group"
          >
            <div className="flex items-center gap-3 min-w-0">
              <ClipboardList className="w-5 h-5 text-subject-600 dark:text-subject-400 flex-shrink-0" aria-hidden="true" />
              <div className="min-w-0">
                <p className="text-sm font-bold text-ink-text leading-tight">Prova Diagnóstica pendente</p>
                <p className="text-xs text-ink-muted mt-0.5 truncate">
                  Calibre sua trilha: 12 a 20 questões adaptativas.
                </p>
              </div>
            </div>
            <span className="text-xs font-bold text-subject-700 dark:text-subject-400 flex-shrink-0 group-hover:underline">
              Iniciar
            </span>
          </Link>
        )}
        {!loading && reforcoPendentes > 0 && (
          <Link
            href="/reforco"
            className="mb-3 flex items-center justify-between gap-4 px-4 py-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 group"
          >
            <div className="flex items-center gap-3 min-w-0">
              <Inbox className="w-5 h-5 text-rose-600 dark:text-rose-400 flex-shrink-0" aria-hidden="true" />
              <div className="min-w-0">
                <p className="text-sm font-bold text-ink-text leading-tight">Caixa de Reforço</p>
                <p className="text-xs text-ink-muted mt-0.5 truncate">
                  {reforcoPendentes === 1 ? "1 item aguardando revisão" : `${reforcoPendentes} itens aguardando revisão`}
                </p>
              </div>
            </div>
            <span className="text-xs font-bold text-rose-600 dark:text-rose-400 flex-shrink-0 group-hover:underline">
              Revisar
            </span>
          </Link>
        )}

        {/* ── Estados de carga/erro ─────────────────────────────────────── */}
        {loading && (
          <div className="space-y-3 mt-6" aria-busy="true" aria-label="Carregando árvore de habilidades">
            {[1, 2, 3].map((n) => (
              <div key={n} className="h-20 rounded-xl bg-surface-card border border-line animate-pulse" />
            ))}
          </div>
        )}
        {error && (
          <div
            role="alert"
            className="mt-6 p-4 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 text-rose-700 dark:text-rose-300 flex items-center gap-3"
          >
            <AlertCircle className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}
        {!loading && !error && filteredVolumes.length === 0 && (
          <div className="mt-6 p-8 rounded-xl bg-surface-card border border-line text-center">
            <p className="text-sm font-semibold text-ink-text">Nenhum volume nesta área</p>
            <p className="text-xs text-ink-faint mt-1">Tente outro filtro de grande área.</p>
          </div>
        )}

        {/* ── Banner Promocional Passe Global (se houver conteúdos bloqueados) ── */}
        {!loading && !error && volumes.some((v) => (v.capitulos || []).some((c) => !c.desbloqueado)) && (
          <div className="mb-4 p-4 rounded-xl bg-gradient-to-r from-amber-500/10 via-subject-500/10 to-emerald-500/10 border border-subject-200/60 dark:border-subject-800/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-subject-500 text-white flex items-center justify-center font-black shrink-0 shadow-sm">
                <Sparkles className="w-5 h-5 text-amber-200" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                  Passe Global Ilimitado
                  <span className="text-[10px] font-extrabold uppercase px-1.5 py-0.5 bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 rounded">
                    11 Volumes
                  </span>
                </h3>
                <p className="text-xs text-ink-muted mt-0.5">
                  Acesso irrestrito a todos os 11 volumes didáticos, exercícios e ao Tutor IA Especialista por 12 meses.
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={abrirCheckoutPasseGlobal}
              className="w-full sm:w-auto px-4 py-2 rounded-lg bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs shadow-sm transition-all shrink-0 cursor-pointer flex items-center justify-center gap-1.5"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Desbloquear Tudo por R$ 199,00</span>
            </button>
          </div>
        )}

        {/* ── Lista de Volumes: mastery strip + linhas ──────────────────── */}
        {!loading && !error && (
          <div className="space-y-3">
            {filteredVolumes.map((vol) => {
              const isExpanded = !!expandedVolumes[vol.id];
              const caps = vol.capitulos || [];
              const totalCaps = caps.length;
              const dominioVolume =
                totalCaps > 0
                  ? Math.round((caps.filter((c) => c.status_dominio === "mastered").length / totalCaps) * 100)
                  : 0;

              return (
                <section
                  key={vol.id}
                  className="bg-surface-card border border-line rounded-xl overflow-hidden"
                >
                  {/* Cabeçalho do volume */}
                  <button
                    onClick={() => toggleVolume(vol.id)}
                    aria-expanded={isExpanded}
                    className="w-full px-4 sm:px-5 pt-4 pb-3.5 text-left hover:bg-surface-elevated/60 transition-colors"
                  >
                    <div className="flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3 min-w-0">
                        <span
                          className="flex items-center justify-center w-9 h-9 rounded-lg bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-400 font-extrabold text-sm flex-shrink-0 tabular-nums"
                          aria-hidden="true"
                        >
                          {String(vol.numero_volume).padStart(2, "0")}
                        </span>
                        <div className="min-w-0">
                          <h2 className="font-bold text-sm sm:text-base leading-snug truncate">
                            {vol.titulo}
                          </h2>
                          <p className="text-[11px] text-ink-faint mt-0.5 tabular-nums">
                            {totalCaps} {totalCaps === 1 ? "capítulo" : "capítulos"} · {totalCaps * 50} min ·{" "}
                            <span className="font-semibold text-emerald-600 dark:text-emerald-400">{dominioVolume}%</span>
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        {caps.some((c) => !c.desbloqueado) && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              abrirCheckoutVolume(vol);
                            }}
                            className="inline-flex items-center gap-1 text-[11px] font-semibold text-subject-600 dark:text-subject-400 bg-subject-50 dark:bg-subject-wash px-2 sm:px-2.5 py-1 rounded-lg border border-subject-200/60 dark:border-subject-wash-strong hover:bg-subject-500 hover:text-white transition-colors cursor-pointer"
                          >
                            <Lock className="w-3 h-3" />
                            <span className="hidden sm:inline">Comprar Volume (R$ 49,90)</span>
                            <span className="sm:hidden">Volume R$ 49,90</span>
                          </button>
                        )}
                        <ChevronDown
                          className={`w-4 h-4 text-ink-faint flex-shrink-0 transition-transform ${isExpanded ? "" : "-rotate-90"}`}
                          aria-hidden="true"
                        />
                      </div>
                    </div>

                    {/* Mastery strip: uma célula por capítulo (RN-PRG-012) */}
                    {totalCaps > 0 && (
                      <div className="flex gap-[3px] mt-3" aria-hidden="true">
                        {caps.map((cap) => (
                          <span
                            key={cap.id}
                            className={`h-1.5 flex-1 rounded-full ${heatmapClasses(cap.cor_heatmap).cell}`}
                          />
                        ))}
                      </div>
                    )}
                  </button>

                  {/* Capítulos expandidos: linhas com hairline, não cards */}
                  {isExpanded && (
                    <ul className="border-t border-line">
                      {caps.map((cap: SkillTreeNode) => {
                        const semConteudo = cap.tem_conteudo === false;
                        const travado = !cap.desbloqueado || semConteudo;
                        const hm = heatmapClasses(cap.cor_heatmap);

                        return (
                          <li key={cap.id} className="border-b border-line last:border-b-0">
                            <div className="px-4 sm:px-5 py-3 flex items-center gap-3">
                              {/* Dot de domínio */}
                              <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${hm.cell}`} title={hm.label} />

                              {/* Conteúdo principal da linha */}
                              {semConteudo ? (
                                <>
                                  <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2">
                                      <span className="text-[11px] font-semibold text-ink-faint tabular-nums">
                                        Cap. {cap.numero_capitulo}
                                      </span>
                                      <span className="text-[10px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded bg-slate-100 dark:bg-surface-elevated text-ink-faint">
                                        Em breve
                                      </span>
                                    </div>
                                    <p className="text-sm text-ink-muted truncate mt-0.5">{cap.titulo}</p>
                                  </div>
                                  <Clock className="w-4 h-4 text-ink-faint flex-shrink-0" aria-hidden="true" />
                                </>
                              ) : !cap.desbloqueado ? (
                                <>
                                  <button
                                    type="button"
                                    onClick={() => abrirCheckoutCapitulo(cap)}
                                    className="flex-1 min-w-0 text-left group/row"
                                  >
                                    <div className="flex items-center gap-2">
                                      <span className="text-[11px] font-semibold text-ink-faint tabular-nums">
                                        Cap. {cap.numero_capitulo}
                                      </span>
                                      <span className="inline-flex items-center gap-1 text-[10px] font-bold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-200/50 dark:border-amber-800/40">
                                        <Lock className="w-3 h-3" /> Bloqueado
                                      </span>
                                    </div>
                                    <p className="text-sm font-semibold text-ink-muted group-hover/row:text-subject-600 dark:group-hover/row:text-subject-400 transition-colors truncate mt-0.5">
                                      {cap.titulo}
                                    </p>
                                  </button>

                                  <div className="flex items-center gap-2 flex-shrink-0">
                                    <span className="hidden sm:flex items-center gap-1 text-[11px] text-ink-faint tabular-nums mr-1">
                                      <Clock className="w-3 h-3" aria-hidden="true" />
                                      {cap.tempo_estimado_min}min
                                    </span>
                                    <button
                                      type="button"
                                      onClick={() => abrirCheckoutCapitulo(cap)}
                                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-subject-50 dark:bg-subject-wash text-subject-700 dark:text-subject-300 hover:bg-subject-500 hover:text-white text-xs font-semibold border border-subject-200/60 dark:border-subject-wash-strong transition-all cursor-pointer"
                                    >
                                      <Lock className="w-3.5 h-3.5" />
                                      <span>Desbloquear R$ 9,90</span>
                                    </button>
                                  </div>
                                </>
                              ) : (
                                <>
                                  <Link href={`/aula/${cap.id}`} className="flex-1 min-w-0 group/row">
                                    <div className="flex items-center gap-2">
                                      <span className="text-[11px] font-semibold text-ink-faint tabular-nums">
                                        Cap. {cap.numero_capitulo}
                                      </span>
                                      {cap.pre_requisito_pendente && (
                                        <span className="inline-flex items-center gap-1 text-[10px] font-medium text-ink-faint">
                                          <Lock className="w-3 h-3" aria-hidden="true" />
                                          sugerido anterior
                                        </span>
                                      )}
                                    </div>
                                    <p className="text-sm font-semibold text-ink-text group-hover/row:text-subject-600 dark:group-hover/row:text-subject-400 transition-colors truncate mt-0.5">
                                      {cap.titulo}
                                    </p>
                                  </Link>

                                  {/* Ações à direita */}
                                  <div className="flex items-center gap-1.5 flex-shrink-0">
                                    <span className="hidden sm:flex items-center gap-1 text-[11px] text-ink-faint tabular-nums mr-1">
                                      <Clock className="w-3 h-3" aria-hidden="true" />
                                      {cap.tempo_estimado_min}min
                                    </span>
                                    <Link
                                      href={`/exercicios/${cap.id}`}
                                      title="Exercícios do capítulo"
                                      aria-label={`Exercícios do capítulo ${cap.numero_capitulo}`}
                                      className="w-9 h-9 rounded-lg flex items-center justify-center transition-colors bg-subject-wash text-subject-700 dark:text-subject-400 hover:bg-subject-500 hover:text-white"
                                    >
                                      <PenLine className="w-4 h-4" aria-hidden="true" />
                                    </Link>
                                    <Link
                                      href={`/aula/${cap.id}`}
                                      title="Abrir aula"
                                      aria-label={`Abrir aula do capítulo ${cap.numero_capitulo}`}
                                      className="w-9 h-9 rounded-lg flex items-center justify-center transition-colors bg-surface-elevated text-ink-muted hover:text-subject-600 dark:hover:text-subject-400"
                                    >
                                      <PlayIcon />
                                    </Link>
                                  </div>
                                </>
                              )}
                            </div>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </section>
              );
            })}
          </div>
        )}

        {/* Modal Global de Checkout In-App (Etapa 9) */}
        <CheckoutModal
          isOpen={checkoutOpen}
          onClose={() => setCheckoutOpen(false)}
          tipoProduto={checkoutData.tipoProduto}
          referenciaId={checkoutData.referenciaId}
          tituloProduto={checkoutData.titulo}
          precoPadrao={checkoutData.preco}
          onPaymentSuccess={() => {
            loadSkillTree();
          }}
        />
      </main>
    </div>
  );
}

/** Ícone de play em SVG inline (Lucide PlayCircle). */
function PlayIcon() {
  return (
    <svg
      className="w-4 h-4"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="10" />
      <polygon points="10 8 16 12 10 16 10 8" />
    </svg>
  );
}
