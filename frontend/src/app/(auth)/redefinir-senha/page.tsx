"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Lock, Eye, EyeOff, AlertCircle, ShieldCheck, ArrowRight, ArrowBigUpDash } from "lucide-react";
import { api } from "@/lib/api";
import { VerificarTokenResponse } from "@/types/auth";

function RedefinirSenhaForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";

  const [verificando, setVerificando] = useState(true);
  const [tokenValido, setTokenValido] = useState(false);
  const [emailMascarado, setEmailMascarado] = useState<string | null>(null);
  const [mensagemErroToken, setMensagemErroToken] = useState<string | null>(null);

  const [novaSenha, setNovaSenha] = useState("");
  const [confirmacaoSenha, setConfirmacaoSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [capsLockAtivo, setCapsLockAtivo] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setVerificando(false);
      setTokenValido(false);
      setMensagemErroToken("Nenhum token de recuperação foi fornecido.");
      return;
    }

    const verificar = async () => {
      try {
        const res = await api.get<VerificarTokenResponse>(
          `/api/v1/auth/verificar-token?token=${encodeURIComponent(token)}`
        );
        if (res.valido) {
          setTokenValido(true);
          setEmailMascarado(res.email_mascarado || null);
        } else {
          setTokenValido(false);
          setMensagemErroToken(res.mensagem || "Token expirado ou inválido.");
        }
      } catch (err: any) {
        setTokenValido(false);
        setMensagemErroToken("Não foi possível verificar o token de recuperação.");
      } finally {
        setVerificando(false);
      }
    };

    verificar();
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErroForm(null);

    if (novaSenha !== confirmacaoSenha) {
      setErroForm("A confirmação não coincide com a nova senha.");
      return;
    }

    if (novaSenha.length < 8) {
      setErroForm("A senha deve conter no mínimo 8 caracteres.");
      return;
    }

    setSalvando(true);
    try {
      await api.post("/api/v1/auth/redefinir-senha", {
        token,
        nova_senha: novaSenha,
        confirmacao_senha: confirmacaoSenha,
      });

      router.push("/login?redefinido=true");
    } catch (err: any) {
      setErroForm(err.data?.detail || "Erro ao atualizar senha. Tente novamente.");
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="bg-white dark:bg-[#261d11] border border-slate-200/90 dark:border-[#3d2f1f] rounded-2xl p-7 sm:p-9 shadow-sm">
      {verificando ? (
        <div className="text-center py-8">
          <div className="w-6 h-6 border-2 border-[#F57C00] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-xs text-slate-500 dark:text-[#A89F91]">Validando autenticidade do link...</p>
        </div>
      ) : !tokenValido ? (
        <div className="text-center space-y-4">
          <div className="mx-auto w-12 h-12 bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 rounded-full flex items-center justify-center border border-rose-200 dark:border-rose-800/40">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white">Link Indisponível</h3>
          <p className="text-xs text-slate-600 dark:text-[#A89F91] leading-relaxed">
            {mensagemErroToken || "Este link mágico expirou ou já foi utilizado para alterar a senha."}
          </p>
          <div className="pt-3">
            <Link
              href="/esqueci-senha"
              className="w-full py-2.5 px-4 rounded-xl bg-[#F57C00] hover:bg-[#EF6C00] text-white font-semibold text-xs transition-colors inline-flex items-center justify-center gap-2"
            >
              Solicitar Novo Link
            </Link>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {emailMascarado && (
            <div className="p-3 bg-[#FFF3E0] dark:bg-[#2b1f10] border border-[#FFB74D]/40 rounded-xl text-xs text-[#E65100] dark:text-[#FFB74D] flex items-center justify-between">
              <span>Conta vinculada:</span>
              <strong className="font-mono text-slate-900 dark:text-white">{emailMascarado}</strong>
            </div>
          )}

          {erroForm && (
            <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 text-rose-800 dark:text-rose-300 text-xs flex items-start gap-2.5 leading-relaxed">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
              <span>{erroForm}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Nova Senha (mín. 8 caracteres)
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type={mostrarSenha ? "text" : "password"}
                required
                minLength={8}
                autoComplete="new-password"
                value={novaSenha}
                onChange={(e) => setNovaSenha(e.target.value)}
                onKeyUp={(e) => setCapsLockAtivo(e.getModifierState("CapsLock"))}
                onBlur={() => setCapsLockAtivo(false)}
                placeholder="Mínimo 8 caracteres"
                className="w-full pl-10 pr-11 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
              />
              <button
                type="button"
                onClick={() => setMostrarSenha(!mostrarSenha)}
                aria-label={mostrarSenha ? "Ocultar senha" : "Mostrar senha"}
                aria-pressed={mostrarSenha}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors cursor-pointer"
              >
                {mostrarSenha ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {capsLockAtivo && (
              <p className="mt-1 text-[11px] font-medium text-amber-700 dark:text-amber-400 flex items-center gap-1">
                <ArrowBigUpDash className="w-3.5 h-3.5" />
                Caps Lock está ativado.
              </p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Confirme a Nova Senha
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type={mostrarSenha ? "text" : "password"}
                required
                minLength={8}
                autoComplete="new-password"
                value={confirmacaoSenha}
                onChange={(e) => setConfirmacaoSenha(e.target.value)}
                placeholder="Repita a nova senha idêntica"
                className="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-[#1a1408] border border-slate-300 dark:border-[#3d2f1f] rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#F57C00]/20 focus:border-[#F57C00] transition-all"
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={salvando}
              className="w-full py-3 px-4 rounded-xl bg-[#F57C00] hover:bg-[#EF6C00] text-white font-semibold text-sm shadow-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {salvando ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>Atualizar Senha</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default function RedefinirSenhaPage() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#1a1408] text-slate-900 dark:text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#F57C00] text-white shadow-sm mb-3">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Criar Nova Senha
          </h1>
          <p className="text-xs text-slate-500 dark:text-[#A89F91] mt-1">
            Defina uma nova credencial segura para a sua conta
          </p>
        </div>

        <Suspense
          fallback={
            <div className="bg-white dark:bg-[#261d11] border border-slate-200 dark:border-[#3d2f1f] rounded-2xl p-8 text-center text-slate-500">
              <div className="w-6 h-6 border-2 border-[#F57C00] border-t-transparent rounded-full animate-spin mx-auto mb-2" />
              Carregando...
            </div>
          }
        >
          <RedefinirSenhaForm />
        </Suspense>
      </div>
    </div>
  );
}
