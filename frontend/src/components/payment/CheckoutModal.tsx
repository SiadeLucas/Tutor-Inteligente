"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  X,
  QrCode,
  CreditCard,
  CheckCircle2,
  Copy,
  Check,
  Clock,
  Sparkles,
  ShieldCheck,
  ArrowRight,
  AlertCircle,
  Loader2,
} from "lucide-react";
import { api, extrairMensagemErro } from "@/lib/api";
import {
  TipoProduto,
  CalcularUpgradeResponse,
  CheckoutPixResponse,
  CheckoutCartaoResponse,
  StatusCobrancaResponse,
} from "@/types/payment";

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  tipoProduto: TipoProduto;
  referenciaId?: string;
  tituloProduto: string;
  precoPadrao: number;
  onPaymentSuccess?: () => void;
}

export function CheckoutModal({
  isOpen,
  onClose,
  tipoProduto,
  referenciaId,
  tituloProduto,
  precoPadrao,
  onPaymentSuccess,
}: CheckoutModalProps) {
  const [activeTab, setActiveTab] = useState<"pix" | "cartao">("pix");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  // Upgrade info
  const [upgradeInfo, setUpgradeInfo] = useState<CalcularUpgradeResponse | null>(null);

  // PIX state
  const [pixData, setPixData] = useState<CheckoutPixResponse | null>(null);
  const [copiado, setCopiado] = useState(false);
  const [segundosRestantes, setSegundosRestantes] = useState(15 * 60);

  // Cartão state
  const [nomeTitular, setNomeTitular] = useState("");
  const [numeroCartao, setNumeroCartao] = useState("");
  const [mesExp, setMesExp] = useState("");
  const [anoExp, setAnoExp] = useState("");
  const [cvv, setCvv] = useState("");
  const [parcelas, setParcelas] = useState(1);

  // Sucesso
  const [pagamentoConfirmado, setPagamentoConfirmado] = useState(false);

  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // 1. Carrega dados de upgrade caso seja Volume Didático
  useEffect(() => {
    if (!isOpen) {
      resetState();
      return;
    }

    if (tipoProduto === "volume_iezzi" && referenciaId) {
      api
        .get<CalcularUpgradeResponse>(`/api/v1/pagamentos/calcular-upgrade/${referenciaId}`)
        .then((res) => {
          setUpgradeInfo(res);
        })
        .catch(() => {
          // segue com valor padrão
        });
    }
  }, [isOpen, tipoProduto, referenciaId]);

  // 2. Timer regressivo de 15 minutos para PIX
  useEffect(() => {
    if (pixData && !pagamentoConfirmado) {
      timerRef.current = setInterval(() => {
        setSegundosRestantes((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current!);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [pixData, pagamentoConfirmado]);

  // 3. Polling a cada 3 segundos para confirmação instantânea
  useEffect(() => {
    if (pixData?.cobranca_id && !pagamentoConfirmado) {
      pollingRef.current = setInterval(async () => {
        try {
          const res = await api.get<StatusCobrancaResponse>(
            `/api/v1/pagamentos/status/${pixData.cobranca_id}`
          );
          if (res.pago) {
            handleSucesso();
          }
        } catch {
          // ignore erros transitórios de rede
        }
      }, 3000);
    }

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [pixData, pagamentoConfirmado]);

  const resetState = () => {
    setPixData(null);
    setUpgradeInfo(null);
    setPagamentoConfirmado(false);
    setLoading(false);
    setErro(null);
    setCopiado(false);
    setSegundosRestantes(15 * 60);
    if (pollingRef.current) clearInterval(pollingRef.current);
    if (timerRef.current) clearInterval(timerRef.current);
  };

  const handleSucesso = () => {
    setPagamentoConfirmado(true);
    if (pollingRef.current) clearInterval(pollingRef.current);
    if (timerRef.current) clearInterval(timerRef.current);
    setTimeout(() => {
      if (onPaymentSuccess) onPaymentSuccess();
      onClose();
    }, 2500);
  };

  const handleGerarPix = async () => {
    setLoading(true);
    setErro(null);
    try {
      const res = await api.post<CheckoutPixResponse>("/api/v1/pagamentos/checkout/pix", {
        tipo_produto: tipoProduto,
        referencia_produto_id: referenciaId || null,
      });

      if (res.gratis_por_upgrade) {
        handleSucesso();
      } else {
        setPixData(res);
      }
    } catch (err: any) {
      setErro(extrairMensagemErro(err, "Falha ao gerar cobrança PIX. Tente novamente."));
    } finally {
      setLoading(false);
    }
  };

  const handlePagarCartao = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);
    try {
      const res = await api.post<CheckoutCartaoResponse>("/api/v1/pagamentos/checkout/cartao", {
        tipo_produto: tipoProduto,
        referencia_produto_id: referenciaId || null,
        parcelas,
        cartao: {
          nome_titular: nomeTitular,
          numero_cartao: numeroCartao.replace(/\D/g, ""),
          mes_expiracao: mesExp,
          ano_expiracao: anoExp,
          cvv: cvv,
        },
      });

      if (res.pago || res.gratis_por_upgrade) {
        handleSucesso();
      } else {
        setErro("Pagamento não autorizado pela operadora do cartão.");
      }
    } catch (err: any) {
      setErro(extrairMensagemErro(err, "Falha ao processar cartão de crédito."));
    } finally {
      setLoading(false);
    }
  };

  const copiarPix = () => {
    if (pixData?.pix_copia_e_cola) {
      navigator.clipboard.writeText(pixData.pix_copia_e_cola);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 2000);
    }
  };

  // Simulação manual de pagamento (atalho de teste local)
  const simularPagamentoDev = async () => {
    if (!pixData?.cobranca_id) return;
    try {
      await api.post("/api/v1/pagamentos/simular-pagamento", {
        cobranca_id: pixData.cobranca_id,
      });
      handleSucesso();
    } catch (e) {
      console.error(e);
    }
  };

  if (!isOpen) return null;

  const valorFinal = upgradeInfo ? upgradeInfo.valor_final : precoPadrao;
  const temDesconto = upgradeInfo && upgradeInfo.total_abatimento > 0;
  const minutos = Math.floor(segundosRestantes / 60);
  const segundos = segundosRestantes % 60;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-white dark:bg-surface-bg border border-slate-200 dark:border-line rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-line flex items-center justify-between bg-slate-50/50 dark:bg-surface-elevated/40">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-subject-500">
              Desbloqueio de Conteúdo
            </span>
            <h3 className="text-base font-bold text-slate-900 dark:text-white line-clamp-1">
              {tituloProduto}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-ink-muted hover:text-slate-900 dark:hover:text-white p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-surface-elevated transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Banner de Upgrade se houver abatimento */}
        {temDesconto && (
          <div className="bg-emerald-50 dark:bg-emerald-950/40 border-b border-emerald-200 dark:border-emerald-800/40 px-6 py-3 flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div className="text-xs text-emerald-900 dark:text-emerald-200">
              <span className="font-bold">Abatimento Integral de 100%!</span> Você já investiu R${" "}
              {upgradeInfo.total_abatimento.toFixed(2)} em capítulos deste volume. Esse valor foi
              totalmente descontado do total.
            </div>
          </div>
        )}

        {/* Resumo de Preço */}
        <div className="px-6 pt-4 pb-2 flex items-baseline justify-between">
          <span className="text-sm text-ink-muted">Valor do investimento (12 meses):</span>
          <div className="text-right">
            {temDesconto && (
              <span className="text-xs line-through text-ink-faint mr-2">
                R$ {upgradeInfo.preco_original.toFixed(2)}
              </span>
            )}
            <span className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
              R$ {valorFinal.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Estado: Pagamento Confirmado com Sucesso */}
        {pagamentoConfirmado ? (
          <div className="p-8 text-center flex flex-col items-center justify-center animate-in zoom-in-95 duration-300">
            <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 rounded-full flex items-center justify-center mb-4 ring-8 ring-emerald-50 dark:ring-emerald-950/40">
              <CheckCircle2 className="w-10 h-10 animate-bounce" />
            </div>
            <h4 className="text-lg font-bold text-slate-900 dark:text-white mb-1">
              Pagamento Confirmado!
            </h4>
            <p className="text-sm text-ink-muted max-w-xs mb-3">
              Seu acesso foi liberado com sucesso por 365 dias. Redirecionando para a aula...
            </p>
            <div className="flex items-center gap-2 text-xs font-medium text-emerald-600 dark:text-emerald-400">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Abrindo conteúdo liberado...</span>
            </div>
          </div>
        ) : (
          <>
            {/* Abas PIX / Cartão */}
            <div className="px-6 pt-2">
              <div className="flex rounded-xl bg-slate-100 dark:bg-surface-elevated p-1 border border-line">
                <button
                  type="button"
                  onClick={() => setActiveTab("pix")}
                  className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-semibold rounded-lg transition-all ${
                    activeTab === "pix"
                      ? "bg-white dark:bg-surface-card text-slate-900 dark:text-white shadow-sm"
                      : "text-ink-muted hover:text-slate-900 dark:hover:text-white"
                  }`}
                >
                  <QrCode className="w-4 h-4 text-emerald-500" />
                  PIX Dinâmico (Instantâneo)
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("cartao")}
                  className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-semibold rounded-lg transition-all ${
                    activeTab === "cartao"
                      ? "bg-white dark:bg-surface-card text-slate-900 dark:text-white shadow-sm"
                      : "text-ink-muted hover:text-slate-900 dark:hover:text-white"
                  }`}
                >
                  <CreditCard className="w-4 h-4 text-subject-500" />
                  Cartão de Crédito
                </button>
              </div>
            </div>

            {/* Mensagem de Erro */}
            {erro && (
              <div className="mx-6 mt-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/40 rounded-xl p-3 flex items-center gap-2 text-xs text-rose-700 dark:text-rose-300">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{erro}</span>
              </div>
            )}

            {/* Conteúdo das Abas */}
            <div className="p-6">
              {activeTab === "pix" ? (
                <div className="space-y-4">
                  {!pixData ? (
                    <div className="text-center py-4">
                      <p className="text-xs text-ink-muted mb-4 leading-relaxed">
                        Ao clicar em gerar PIX, criaremos um QR Code exclusivo com baixa
                        instantânea em 3 a 5 segundos diretamente pelo seu banco.
                      </p>
                      <button
                        onClick={handleGerarPix}
                        disabled={loading}
                        className="w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm shadow-sm transition-colors cursor-pointer disabled:opacity-50"
                      >
                        {loading ? (
                          <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            Gerando QR Code...
                          </>
                        ) : (
                          <>
                            <QrCode className="w-4 h-4" />
                            Gerar Chave e QR Code PIX
                          </>
                        )}
                      </button>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center text-center">
                      {/* Contador Regressivo */}
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/40 px-3 py-1 rounded-full mb-3">
                        <Clock className="w-3.5 h-3.5" />
                        <span>
                          Expira em {String(minutos).padStart(2, "0")}:
                          {String(segundos).padStart(2, "0")}
                        </span>
                      </div>

                      {/* Imagem do QR Code */}
                      <div className="w-44 h-44 border border-line rounded-xl p-2 bg-white flex items-center justify-center shadow-inner mb-3">
                        {pixData.pix_qrcode_base64 ? (
                          <img
                            src={pixData.pix_qrcode_base64}
                            alt="QR Code PIX"
                            className="w-full h-full object-contain"
                          />
                        ) : (
                          <QrCode className="w-20 h-20 text-slate-400" />
                        )}
                      </div>

                      {/* Caixa Copia e Cola */}
                      <div className="w-full mb-3">
                        <label className="text-[11px] font-semibold text-ink-muted block text-left mb-1">
                          Código PIX Copia e Cola:
                        </label>
                        <div className="flex items-center gap-2">
                          <input
                            type="text"
                            readOnly
                            value={pixData.pix_copia_e_cola}
                            className="flex-1 text-xs bg-slate-50 dark:bg-surface-elevated border border-line rounded-lg px-3 py-2 text-ink-muted font-mono truncate select-all"
                          />
                          <button
                            onClick={copiarPix}
                            className="px-3 py-2 rounded-lg bg-subject-500 hover:bg-subject-600 text-white font-medium text-xs flex items-center gap-1.5 transition-colors shrink-0"
                          >
                            {copiado ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                            {copiado ? "Copiado!" : "Copiar"}
                          </button>
                        </div>
                      </div>

                      {/* Status de Polling */}
                      <div className="flex items-center justify-between w-full pt-2 border-t border-line text-[11px] text-ink-muted">
                        <div className="flex items-center gap-1.5">
                          <Loader2 className="w-3 h-3 animate-spin text-emerald-600" />
                          <span>Aguardando pagamento no banco...</span>
                        </div>
                        {/* Botão para testes locais rápidos */}
                        <button
                          onClick={simularPagamentoDev}
                          className="text-[10px] text-subject-500 hover:underline font-medium"
                          title="Simula pagamento imediatamente sem app de banco"
                        >
                          [Simular Baixa]
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                /* Formulário Cartão */
                <form onSubmit={handlePagarCartao} className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-ink-muted block mb-1">
                      Nome Impresso no Cartão
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: LUCAS L SIADE"
                      value={nomeTitular}
                      onChange={(e) => setNomeTitular(e.target.value.toUpperCase())}
                      className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-ink-muted block mb-1">
                      Número do Cartão
                    </label>
                    <input
                      type="text"
                      required
                      maxLength={19}
                      placeholder="0000 0000 0000 0000"
                      value={numeroCartao}
                      onChange={(e) => setNumeroCartao(e.target.value)}
                      className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white"
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="text-xs font-semibold text-ink-muted block mb-1">Mês</label>
                      <input
                        type="text"
                        required
                        maxLength={2}
                        placeholder="MM"
                        value={mesExp}
                        onChange={(e) => setMesExp(e.target.value)}
                        className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white text-center"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-ink-muted block mb-1">Ano</label>
                      <input
                        type="text"
                        required
                        maxLength={4}
                        placeholder="AAAA"
                        value={anoExp}
                        onChange={(e) => setAnoExp(e.target.value)}
                        className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white text-center"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-ink-muted block mb-1">CVV</label>
                      <input
                        type="password"
                        required
                        maxLength={4}
                        placeholder="123"
                        value={cvv}
                        onChange={(e) => setCvv(e.target.value)}
                        className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white text-center"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-ink-muted block mb-1">
                      Parcelamento
                    </label>
                    <select
                      value={parcelas}
                      onChange={(e) => setParcelas(Number(e.target.value))}
                      className="w-full text-xs px-3 py-2 rounded-xl bg-slate-50 dark:bg-surface-elevated border border-line text-slate-900 dark:text-white"
                    >
                      <option value={1}>1x de R$ {valorFinal.toFixed(2)} (à vista)</option>
                      {valorFinal >= 30 && (
                        <>
                          <option value={2}>2x de R$ {(valorFinal / 2).toFixed(2)} sem juros</option>
                          <option value={3}>3x de R$ {(valorFinal / 3).toFixed(2)} sem juros</option>
                        </>
                      )}
                      {valorFinal >= 60 && (
                        <>
                          <option value={6}>6x de R$ {(valorFinal / 6).toFixed(2)} sem juros</option>
                          <option value={12}>12x de R$ {(valorFinal / 12).toFixed(2)} sem juros</option>
                        </>
                      )}
                    </select>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full mt-2 inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors cursor-pointer disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processando Cartão...
                      </>
                    ) : (
                      <>
                        <ShieldCheck className="w-4 h-4" />
                        Confirmar Pagamento de R$ {valorFinal.toFixed(2)}
                      </>
                    )}
                  </button>
                </form>
              )}
            </div>

            {/* Footer de Segurança */}
            <div className="px-6 py-3 border-t border-line bg-slate-50/50 dark:bg-surface-elevated/20 flex items-center justify-center gap-2 text-[11px] text-ink-faint">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
              <span>Pagamento Seguro processado via Gateway Asaas (Criptografia de Ponta a Ponta)</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
