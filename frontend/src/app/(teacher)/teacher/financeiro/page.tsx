"use client";

import React, { useEffect, useState } from "react";
import {
  DollarSign,
  TrendingUp,
  Receipt,
  RotateCcw,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Clock,
  CreditCard,
  QrCode,
  ShieldAlert,
  X,
  RefreshCw,
} from "lucide-react";
import { api } from "@/lib/api";

interface TransacaoItem {
  id: string;
  matricula_id?: string | null;
  usuario_id: string;
  aluno_nome: string;
  aluno_email: string;
  valor_bruto: number;
  taxa_gateway: number;
  valor_liquido: number;
  status: string;
  metodo: string;
  gateway_transacao_id: string;
  pago_em?: string | null;
  criado_em: string;
}

interface ExtratoResponse {
  saldo_total_bruto: number;
  saldo_total_liquido: number;
  taxas_totais_asaas: number;
  total_transacoes: number;
  total_reembolsado: number;
  transacoes: TransacaoItem[];
}

export default function FinanceiroPage() {
  const [extrato, setExtrato] = useState<ExtratoResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Modal de Estorno
  const [selectedTx, setSelectedTx] = useState<TransacaoItem | null>(null);
  const [estornando, setEstornando] = useState(false);
  const [feedback, setFeedback] = useState<{ tipo: "sucesso" | "erro"; msg: string } | null>(null);

  const carregarExtrato = async () => {
    setLoading(true);
    try {
      const res = await api.get<ExtratoResponse>("/api/v1/teacher/financeiro/extrato");
      setExtrato(res);
    } catch (err) {
      console.error("Erro ao carregar extrato:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarExtrato();
  }, []);

  const confirmarEstorno = async () => {
    if (!selectedTx || !selectedTx.matricula_id) return;
    setEstornando(true);
    setFeedback(null);
    try {
      const resp = await api.post<{ sucesso: boolean; mensagem: string }>(
        `/api/v1/teacher/matriculas/${selectedTx.matricula_id}/estorno`
      );
      setFeedback({ tipo: "sucesso", msg: resp.mensagem });
      setSelectedTx(null);
      await carregarExtrato();
    } catch (err: any) {
      setFeedback({
        tipo: "erro",
        msg: err?.message || "Não foi possível efetuar o estorno administrativo.",
      });
    } finally {
      setEstornando(false);
    }
  };

  // Verifica se a transação está dentro dos 7 dias do CDC
  const isDentroDos7Dias = (criadoEm: string) => {
    const dataTx = new Date(criadoEm).getTime();
    const agora = new Date().getTime();
    const seteDiasMs = 7 * 24 * 60 * 60 * 1000;
    return agora - dataTx <= seteDiasMs;
  };

  return (
    <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      {/* Topo */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Gestão Financeira & Extrato Contábil
          </h1>
          <p className="text-slate-600 dark:text-ink-muted text-sm mt-0.5">
            Monitoramento de faturamento, conciliação do gateway Asaas e estorno legal (CDC 7 dias).
          </p>
        </div>
        <button
          onClick={carregarExtrato}
          disabled={loading}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white dark:bg-surface-card border border-line text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition-colors shadow-2xs self-start sm:self-auto cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-subject-500" : ""}`} />
          <span>Atualizar Extrato</span>
        </button>
      </div>

      {feedback && (
        <div
          className={`mb-6 p-4 rounded-xl border flex items-center justify-between text-sm animate-fadeIn ${
            feedback.tipo === "sucesso"
              ? "bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300"
              : "bg-rose-50 text-rose-800 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300"
          }`}
        >
          <div className="flex items-center gap-2.5">
            {feedback.tipo === "sucesso" ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-rose-600" />
            )}
            <span>{feedback.msg}</span>
          </div>
          <button onClick={() => setFeedback(null)} className="text-xs opacity-70 hover:opacity-100">
            Fechar
          </button>
        </div>
      )}

      {/* Grid de Cards de Saldo */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-8">
        <div className="bg-white dark:bg-surface-card border border-line rounded-2xl p-5 shadow-xs">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Total Faturado Bruto
          </span>
          <div className="text-2xl font-black text-slate-900 dark:text-white mt-1">
            {loading
              ? "--"
              : (extrato?.saldo_total_bruto ?? 0).toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
          </div>
          <span className="text-[11px] text-slate-400">Total acumulado de entradas</span>
        </div>

        <div className="bg-white dark:bg-surface-card border border-line rounded-2xl p-5 shadow-xs">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Taxas Gateway Asaas
          </span>
          <div className="text-2xl font-black text-rose-600 dark:text-rose-400 mt-1">
            {loading
              ? "--"
              : (extrato?.taxas_totais_asaas ?? 0).toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
          </div>
          <span className="text-[11px] text-slate-400">Tarifas de PIX e Cartão</span>
        </div>

        <div className="bg-white dark:bg-surface-card border border-line rounded-2xl p-5 shadow-xs">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Saldo Líquido Real
          </span>
          <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1">
            {loading
              ? "--"
              : (extrato?.saldo_total_liquido ?? 0).toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
          </div>
          <span className="text-[11px] text-slate-400">Disponível para repasse</span>
        </div>

        <div className="bg-white dark:bg-surface-card border border-line rounded-2xl p-5 shadow-xs">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Total Estornado (CDC)
          </span>
          <div className="text-2xl font-black text-amber-600 dark:text-amber-400 mt-1">
            {loading
              ? "--"
              : (extrato?.total_reembolsado ?? 0).toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
          </div>
          <span className="text-[11px] text-slate-400">Reembolsos homologados</span>
        </div>
      </div>

      {/* Tabela de Transações */}
      <div className="bg-white dark:bg-surface-card border border-line rounded-2xl shadow-xs overflow-hidden">
        <div className="p-4 border-b border-line flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Receipt className="w-4 h-4 text-subject-500" />
            <span>Extrato Analítico de Transações</span>
          </h3>
          <span className="text-xs text-slate-400 font-medium">
            {extrato?.transacoes.length || 0} registros
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-surface-elevated border-b border-line text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Data / Hora</th>
                <th className="py-3 px-4">Estudante</th>
                <th className="py-3 px-4 text-center">Método</th>
                <th className="py-3 px-4 text-right">Valor Bruto</th>
                <th className="py-3 px-4 text-right">Taxa Asaas</th>
                <th className="py-3 px-4 text-right">Líquido</th>
                <th className="py-3 px-4 text-center">Status</th>
                <th className="py-3 px-4 text-right">Ação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-line text-slate-700 dark:text-slate-300 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">
                    Carregando extrato contábil...
                  </td>
                </tr>
              ) : !extrato || extrato.transacoes.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">
                    Nenhuma transação registrada até o momento.
                  </td>
                </tr>
              ) : (
                extrato.transacoes.map((tx) => {
                  const dentro7Dias = isDentroDos7Dias(tx.criado_em);
                  const podeEstornar =
                    tx.status === "paid" && tx.matricula_id && dentro7Dias;

                  return (
                    <tr
                      key={tx.id}
                      className="hover:bg-slate-50/70 dark:hover:bg-surface-elevated/40 transition-colors"
                    >
                      <td className="py-3 px-4 font-mono text-slate-500">
                        {new Date(tx.criado_em).toLocaleDateString("pt-BR")}{" "}
                        {new Date(tx.criado_em).toLocaleTimeString("pt-BR", {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </td>

                      <td className="py-3 px-4">
                        <div className="font-bold text-slate-900 dark:text-white">
                          {tx.aluno_nome}
                        </div>
                        <div className="text-[11px] text-slate-400">{tx.aluno_email}</div>
                      </td>

                      <td className="py-3 px-4 text-center">
                        <span
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold ${
                            tx.metodo === "pix"
                              ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                              : "bg-purple-50 text-purple-700 dark:bg-purple-950/40 dark:text-purple-300"
                          }`}
                        >
                          {tx.metodo === "pix" ? (
                            <QrCode className="w-3 h-3" />
                          ) : (
                            <CreditCard className="w-3 h-3" />
                          )}
                          <span>{tx.metodo.toUpperCase()}</span>
                        </span>
                      </td>

                      <td className="py-3 px-4 text-right font-semibold text-slate-900 dark:text-white">
                        {tx.valor_bruto.toLocaleString("pt-BR", {
                          style: "currency",
                          currency: "BRL",
                        })}
                      </td>

                      <td className="py-3 px-4 text-right text-rose-500 font-mono">
                        -
                        {tx.taxa_gateway.toLocaleString("pt-BR", {
                          style: "currency",
                          currency: "BRL",
                        })}
                      </td>

                      <td className="py-3 px-4 text-right font-bold text-emerald-600 dark:text-emerald-400">
                        {tx.valor_liquido.toLocaleString("pt-BR", {
                          style: "currency",
                          currency: "BRL",
                        })}
                      </td>

                      <td className="py-3 px-4 text-center">
                        <span
                          className={`inline-block px-2 py-0.5 rounded-full text-[11px] font-bold ${
                            tx.status === "paid"
                              ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300"
                              : tx.status === "refunded"
                              ? "bg-rose-100 text-rose-800 dark:bg-rose-950/50 dark:text-rose-300"
                              : "bg-amber-100 text-amber-800 dark:bg-amber-950/50 dark:text-amber-300"
                          }`}
                        >
                          {tx.status === "paid"
                            ? "Pago"
                            : tx.status === "refunded"
                            ? "Estornado"
                            : "Aguardando"}
                        </span>
                      </td>

                      <td className="py-3 px-4 text-right">
                        {podeEstornar ? (
                          <button
                            onClick={() => setSelectedTx(tx)}
                            className="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-rose-50 hover:bg-rose-100 text-rose-700 dark:bg-rose-950/40 dark:hover:bg-rose-900/50 dark:text-rose-300 border border-rose-200 dark:border-rose-900/40 transition-colors cursor-pointer"
                          >
                            Estornar (CDC)
                          </button>
                        ) : tx.status === "refunded" ? (
                          <span className="text-[11px] text-slate-400 italic">Reembolsado</span>
                        ) : (
                          <span className="text-[11px] text-slate-400">—</span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Duplo de Confirmação de Estorno Administrativo */}
      {selectedTx && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-surface-card border border-line rounded-3xl w-full max-w-md shadow-2xl p-6">
            <div className="flex items-center gap-3 text-rose-600 mb-4">
              <div className="w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-950/50 flex items-center justify-center flex-shrink-0">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Confirmar Estorno Administrativo?
                </h3>
                <span className="text-xs text-rose-600 dark:text-rose-400 font-semibold">
                  Garantia Legal CDC — 7 dias
                </span>
              </div>
            </div>

            <div className="bg-slate-50 dark:bg-surface-elevated rounded-xl p-3.5 text-xs text-slate-700 dark:text-slate-300 space-y-1.5 mb-5 border border-line">
              <div>
                <strong>Aluno:</strong> {selectedTx.aluno_nome} ({selectedTx.aluno_email})
              </div>
              <div>
                <strong>Valor a Reembolsar:</strong>{" "}
                {selectedTx.valor_bruto.toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
              </div>
              <div>
                <strong>ID Transação:</strong>{" "}
                <span className="font-mono">{selectedTx.gateway_transacao_id}</span>
              </div>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Ao confirmar, a plataforma comunicará a devolução integral ao Asaas e revogará
              imediatamente o acesso do estudante ao conteúdo adquirido. Esta operação é irreversível.
            </p>

            <div className="flex items-center justify-end gap-3">
              <button
                onClick={() => setSelectedTx(null)}
                disabled={estornando}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-surface-elevated transition-colors cursor-pointer"
              >
                Cancelar
              </button>
              <button
                onClick={confirmarEstorno}
                disabled={estornando}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-600 hover:bg-rose-700 text-white transition-colors shadow-xs cursor-pointer disabled:opacity-50 flex items-center gap-2"
              >
                <RotateCcw className={`w-3.5 h-3.5 ${estornando ? "animate-spin" : ""}`} />
                <span>{estornando ? "Estornando..." : "Sim, Efetuar Estorno"}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
