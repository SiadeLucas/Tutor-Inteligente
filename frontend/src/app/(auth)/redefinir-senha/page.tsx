"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Lock, Eye, EyeOff, AlertCircle, ShieldCheck, ArrowRight } from "lucide-react";
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
    <div className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
      {verificando ? (
        <div className="text-center py-10">
          <div className="w-8 h-8 border-3 border-indigo-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-slate-300">Validando autenticidade do link...</p>
        </div>
      ) : !tokenValido ? (
        <div className="text-center space-y-4">
          <div className="mx-auto w-12 h-12 bg-rose-500/20 text-rose-400 rounded-full flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-white">Link Indisponível</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            {mensagemErroToken || "Este link mágico expirou ou já foi utilizado para alterar a senha."}
          </p>
          <div className="pt-4">
            <Link
              href="/esqueci-senha"
              className="w-full py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-colors inline-flex items-center justify-center gap-2"
            >
              Solicitar Novo Link
            </Link>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-5">
          {emailMascarado && (
            <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-xs text-indigo-300 flex items-center justify-between">
              <span>Conta vinculada:</span>
              <strong className="font-mono text-white">{emailMascarado}</strong>
            </div>
          )}

          {erroForm && (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-400" />
              <span>{erroForm}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
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
                value={novaSenha}
                onChange={(e) => setNovaSenha(e.target.value)}
                placeholder="Mínimo 8 caracteres"
                className="w-full pl-10 pr-11 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
              <button
                type="button"
                onClick={() => setMostrarSenha(!mostrarSenha)}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-white transition-colors"
              >
                {mostrarSenha ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
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
                value={confirmacaoSenha}
                onChange={(e) => setConfirmacaoSenha(e.target.value)}
                placeholder="Repita a senha idêntica"
                className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={salvando}
            className="w-full py-3.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm shadow-lg shadow-indigo-600/30 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {salvando ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <span>Atualizar Senha</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
}

export default function RedefinirSenhaPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600 shadow-xl shadow-indigo-500/25 mb-4 text-white">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Criar Nova Senha</h1>
          <p className="text-sm text-indigo-200/80 mt-1">Defina uma credencial forte e exclusiva</p>
        </div>

        <Suspense fallback={
          <div className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center text-slate-300">
            <div className="w-8 h-8 border-3 border-indigo-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            Carregando...
          </div>
        }>
          <RedefinirSenhaForm />
        </Suspense>
      </div>
    </div>
  );
}
