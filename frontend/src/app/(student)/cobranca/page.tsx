"use client";

/**
 * /cobranca — Assinatura e Compras (Etapa 9).
 *
 * Fatura ativa (Passe Global ou volume adquirido) + histórico de compras
 * (capítulos avulsos que alimentam o abatimento RN-PAG-005 na compra do volume).
 *
 * Fonte de dados: GET /api/v1/pagamentos/meus-produtos (matrículas ativas).
 * Design system: header tipográfico flat + linhas com hairline (Fase 3).
 */

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  AlertCircle,
  CheckCircle2,
  Clock,
  CreditCard,
  Inbox,
  Lock,
  QrCode,
  Sparkles,
} from "lucide-react";
import { ProdutoAdquirido } from "@/types/billing";
import { api, extrairMensagemErro } from "@/lib/api";

const LABEL_PRODUTO: Record<string, string> = {
  passe_global: "Passe Global Ilimitado",
  volume_iezzi: "Volume Didático",
  capitulo_50min: "Capítulo Avulso (50 min)",
};

const LABEL_METODO: Record<string, string> = {
  pix: "PIX",
  credit_card: "Cartão de Crédito",
  upgrade_gratis: "Abatimento (Upgrade 100%)",
  sistema_admin: "Concessão administrativa",
};

function diasRestantes(dataExpiracao: string): number {
  return Math.max(0, Math.ceil((new Date(dataExpiracao).getTime() - Date.now()) / 86_400_000));
}

function statusMatriculaColor(status: string): string {
  switch (status) {
    case "active":
      return "text-emerald-600 dark:text-emerald-400";
    case "past_due":
      return "text-amber-600 dark:text-amber-400";
    default:
      return "text-ink-faint";
  }
}

export default function CobrancaPage() {
  const [produtos, setProdutos] = useState<ProdutoAdquirido[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        setLoading(true);
        const data = await api.get<ProdutoAdquirido[]>("/api/v1/pagamentos/meus-produtos");
        if (mounted) setProdutos(Array.isArray(data) ? data : []);
      } catch (err) {
        if (mounted) setError(extrairMensagemErro(err, "Não foi possível carregar suas compras."));
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  const passe = produtos.find((p) => p.tipo_produto === "passe_global");
  const volumes = produtos.filter((p) => p.tipo_produto === "volume_iezzi");
  const capitulos = produtos.filter((p) => p.tipo_produto === "capitulo_50min");
  const temAlgumAcesso = produtos.length > 0;

  return (
    <div className="text-slate-900 dark:text-slate-100">
      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {/* ── Header tipográfico flat ───────────────────────────────────── */}
        <header className="mb-6">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-widest text-subject-600 dark:text-subject-400">
            <CreditCard className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Assinatura e Compras</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight mt-1.5">Suas Compras</h1>
          <p className="text-sm text-slate-500 dark:text-ink-muted mt-1.5 leading-relaxed max-w-xl">
            Todos os produtos adquiridos dão <strong className="font-semibold text-slate-700 dark:text-slate-300">365 dias</strong> de
            acesso. Capítulos avulsos são integralmente abatidos na compra do volume completo.
          </p>
        </header>

        {/* ── Estados de carga/erro ─────────────────────────────────────── */}
        {loading && (
          <div className="space-y-3" aria-busy="true" aria-label="Carregando compras">
            {[1, 2, 3].map((n) => (
              <div key={n} className="h-16 rounded-xl bg-surface-card border border-line animate-pulse" />
            ))}
          </div>
        )}
        {error && (
          <div
            role="alert"
            className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 text-rose-700 dark:text-rose-300 flex items-center gap-3"
          >
            <AlertCircle className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {/* ── Fatura ativa: Passe Global ────────────────────────────────── */}
        {!loading && !error && passe && (
          <section
            aria-label="Assinatura ativa"
            className="mb-4 p-5 rounded-xl bg-gradient-to-r from-amber-500/10 via-subject-500/10 to-emerald-500/10 border border-subject-200/60 dark:border-subject-800/40"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 min-w-0">
                <div className="w-10 h-10 rounded-lg bg-subject-500 text-white flex items-center justify-center shrink-0 shadow-sm">
                  <Sparkles className="w-5 h-5 text-amber-200" aria-hidden="true" />
                </div>
                <div className="min-w-0">
                  <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    {passe.titulo_produto}
                    <span className="text-[10px] font-extrabold uppercase px-1.5 py-0.5 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 rounded">
                      Ativo
                    </span>
                  </h2>
                  <p className="text-xs text-ink-muted mt-1 leading-relaxed">
                    Acesso irrestrito a todos os 11 volumes, exercícios e Tutor IA Especialista.
                  </p>
                </div>
              </div>
              <div className="text-right shrink-0 tabular-nums">
                <div className="text-lg font-extrabold text-emerald-600 dark:text-emerald-400">
                  {diasRestantes(passe.data_expiracao)}d
                </div>
                <div className="text-[10px] text-ink-faint uppercase font-semibold">restantes</div>
              </div>
            </div>
          </section>
        )}

        {/* ── CTA de compra quando não há nada adquirido ────────────────── */}
        {!loading && !error && !temAlgumAcesso && (
          <section
            aria-label="Sem compras"
            className="mb-4 p-6 rounded-xl bg-surface-card border border-line text-center"
          >
            <Inbox className="w-10 h-10 text-ink-faint mx-auto mb-3" aria-hidden="true" />
            <h2 className="text-sm font-bold text-ink-text">Nenhuma compra encontrada</h2>
            <p className="text-xs text-ink-muted mt-1 mb-4 leading-relaxed max-w-xs mx-auto">
              Desbloqueie capítulos avulsos por R$ 9,90, volumes completos por R$ 49,90 ou todo o
              acervo com o Passe Global por R$ 199,00.
            </p>
            <Link
              href="/materias"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-subject-500 hover:bg-subject-600 text-white text-xs font-bold shadow-sm transition-colors"
            >
              <Lock className="w-3.5 h-3.5" aria-hidden="true" />
              Ver catálogo de aulas
            </Link>
          </section>
        )}

        {/* ── Lista de produtos adquiridos ──────────────────────────────── */}
        {!loading && !error && produtos.length > 0 && (
          <div className="space-y-3">
            {/* Volumes completos */}
            {volumes.length > 0 && (
              <ProductSection
                titulo="Volumes Completos"
                icone={<CheckCircle2 className="w-4 h-4" aria-hidden="true" />}
                itens={volumes}
              />
            )}

            {/* Capítulos avulsos (abatíveis no upgrade) */}
            {capitulos.length > 0 && (
              <ProductSection
                titulo="Capítulos Avulsos"
                subtitulo="Valor integralmente abatido na compra do volume correspondente (RN-PAG-005)."
                icone={<Clock className="w-4 h-4" aria-hidden="true" />}
                itens={capitulos}
              />
            )}
          </div>
        )}

        {/* ── Footer informativo ────────────────────────────────────────── */}
        {!loading && !error && temAlgumAcesso && (
          <p className="mt-6 flex items-center justify-center gap-2 text-[11px] text-ink-faint">
            <QrCode className="w-3.5 h-3.5" aria-hidden="true" />
            <span>
              Pagamentos processados via PIX e Cartão de Crédito pelo gateway Asaas. Dúvidas?
              Consulte os{" "}
              <Link href="/materias" className="underline hover:text-subject-600">
                conteúdos liberados
              </Link>
              .
            </span>
          </p>
        )}
      </main>
    </div>
  );
}

/** Grupo de produtos com o mesmo tipo (hairline rows, sem card-in-card). */
function ProductSection({
  titulo,
  subtitulo,
  icone,
  itens,
}: {
  titulo: string;
  subtitulo?: string;
  icone: React.ReactNode;
  itens: ProdutoAdquirido[];
}) {
  return (
    <section className="bg-surface-card border border-line rounded-xl overflow-hidden">
      <div className="px-4 sm:px-5 pt-4 pb-3 border-b border-line">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <span className="text-subject-600 dark:text-subject-400">{icone}</span>
          {titulo}
          <span className="text-[10px] font-bold uppercase tabular-nums px-1.5 py-0.5 bg-surface-elevated text-ink-faint rounded">
            {itens.length}
          </span>
        </h2>
        {subtitulo && <p className="text-[11px] text-ink-muted mt-1">{subtitulo}</p>}
      </div>
      <ul>
        {itens.map((item) => (
          <li key={item.id} className="px-4 sm:px-5 py-3 border-b border-line last:border-b-0">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <p className="text-sm font-semibold text-ink-text truncate">{item.titulo_produto}</p>
                <p className="text-[11px] text-ink-faint mt-0.5 tabular-nums">
                  R$ {(item.valor_pago ?? 0).toFixed(2)}
                </p>
              </div>
              <div className="text-right shrink-0 tabular-nums">
                <div className={`text-sm font-bold ${statusMatriculaColor(item.status)}`}>
                  {item.dias_restantes}d
                </div>
                <div className="text-[10px] text-ink-faint uppercase font-semibold">restantes</div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
