"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, EyeOff, LogIn, Lock, User, AlertCircle, ShieldAlert, BookOpen, ArrowBigUpDash, Sigma } from "lucide-react";
import { api, extrairMensagemErro, setAccessToken } from "@/lib/api";
import { LoginResponse } from "@/types/auth";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [identificador, setIdentificador] = useState("");
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [capsLockAtivo, setCapsLockAtivo] = useState(false);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);

  useEffect(() => {
    if (searchParams.get("sessao_revogada") === "true") {
      setAviso("Você foi desconectado porque sua conta foi acessada em outro aparelho.");
    } else if (searchParams.get("sessao_expirada") === "true") {
      setAviso("Sua sessão expirou por inatividade. Faça login novamente.");
    } else if (searchParams.get("redefinido") === "true") {
      setAviso("Senha alterada com sucesso! Faça login com suas novas credenciais.");
    }
  }, [searchParams]);

  // Formatação amigável de CPF durante a digitação
  const handleIdentificadorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    const apenasDigitos = val.replace(/\D/g, "");

    if (apenasDigitos.length > 0 && !val.includes("@") && apenasDigitos.length <= 11) {
      let formatado = apenasDigitos;
      if (apenasDigitos.length > 9) {
        formatado = `${apenasDigitos.slice(0, 3)}.${apenasDigitos.slice(3, 6)}.${apenasDigitos.slice(6, 9)}-${apenasDigitos.slice(9, 11)}`;
      } else if (apenasDigitos.length > 6) {
        formatado = `${apenasDigitos.slice(0, 3)}.${apenasDigitos.slice(3, 6)}.${apenasDigitos.slice(6)}`;
      } else if (apenasDigitos.length > 3) {
        formatado = `${apenasDigitos.slice(0, 3)}.${apenasDigitos.slice(3)}`;
      }
      setIdentificador(formatado);
    } else {
      setIdentificador(val);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro(null);
    setCarregando(true);

    try {
      const data = await api.post<LoginResponse>("/api/v1/auth/login", {
        identificador,
        senha,
      });

      setAccessToken(data.access_token);

      if (data.usuario.role === "teacher") {
        router.push("/teacher");
      } else {
        router.push("/materias");
      }
    } catch (err: any) {
      setErro(extrairMensagemErro(err, "Falha ao realizar login. Verifique suas credenciais."));
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-7 sm:p-9 shadow-sm">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
          Acesse sua conta
        </h2>
        <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
          Informe seu e-mail institucional ou CPF cadastrado
        </p>
      </div>

      {aviso && (
        <div className="mb-5 p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 text-amber-800 dark:text-amber-300 text-xs flex items-start gap-2.5 leading-relaxed">
          <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
          <span>{aviso}</span>
        </div>
      )}

      {erro && (
        <div className="mb-5 p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 text-rose-800 dark:text-rose-300 text-xs flex items-start gap-2.5 leading-relaxed">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
          <span>{erro}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            E-mail ou CPF
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <User className="w-4 h-4" />
            </div>
            <input
              type="text"
              required
              value={identificador}
              onChange={handleIdentificadorChange}
              placeholder="aluno@exemplo.com ou 000.000.000-00"
              className="w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
            />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Senha
            </label>
            <Link
              href="/esqueci-senha"
              className="text-xs font-medium text-subject-700 dark:text-subject-300 hover:underline"
            >
              Esqueceu a senha?
            </Link>
          </div>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type={mostrarSenha ? "text" : "password"}
              required
              autoComplete="current-password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              onKeyUp={(e) => setCapsLockAtivo(e.getModifierState("CapsLock"))}
              onBlur={() => setCapsLockAtivo(false)}
              placeholder="Digite sua senha"
              className="w-full pl-10 pr-11 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
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

        <div className="pt-2">
          <button
            type="submit"
            disabled={carregando}
            className="w-full py-3 px-4 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {carregando ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Entrar na Plataforma</span>
              </>
            )}
          </button>
        </div>
      </form>

      <div className="mt-6 pt-5 border-t border-slate-100 dark:border-line text-center">
        <p className="text-xs text-slate-500 dark:text-ink-muted">
          Ainda não tem uma conta?{" "}
          <Link
            href="/cadastro"
            className="font-semibold text-subject-700 dark:text-subject-300 hover:underline"
          >
            Cadastre-se gratuitamente
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-surface-bg dark:bg-surface-bg text-slate-900 dark:text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-md">
        {/* Cabeçalho Institucional */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-subject-500 text-white shadow-sm mb-3">
            <span className="text-xl font-black tracking-tight">TI</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Tutor Inteligente
          </h1>
          <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
            Matemática do Ensino Médio • Fundamentos com Rigor e IA Socrática
          </p>
          <div className="mt-2.5 inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200">
            <Sigma className="w-3.5 h-3.5" />
            <span>Orientado pela Coleção Gelson Iezzi</span>
          </div>
        </div>

        <Suspense
          fallback={
            <div className="bg-white dark:bg-surface-card border border-slate-200 dark:border-line rounded-2xl p-8 text-center text-slate-500">
              <div className="w-6 h-6 border-2 border-subject-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
              Carregando formulário...
            </div>
          }
        >
          <LoginForm />
        </Suspense>

        {/* Rodapé informativo discreto */}
        <p className="text-center text-xs text-slate-400 dark:text-slate-500 mt-6 leading-relaxed">
          Plataforma com controle estrito de sessão única (1 dispositivo simultâneo) e proteção criptográfica de dados.
        </p>
      </div>
    </div>
  );
}
