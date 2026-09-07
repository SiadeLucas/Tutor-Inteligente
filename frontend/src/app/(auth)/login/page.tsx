"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, EyeOff, LogIn, Lock, User, AlertCircle, ShieldAlert } from "lucide-react";
import { api, setAccessToken } from "@/lib/api";
import { LoginResponse } from "@/types/auth";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [identificador, setIdentificador] = useState("");
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
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
      setErro(err.data?.detail || "Falha ao realizar login. Verifique suas credenciais.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
      <h2 className="text-xl font-semibold text-white mb-6">Acesse sua conta</h2>

      {aviso && (
        <div className="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 shrink-0 mt-0.5 text-amber-400" />
          <span>{aviso}</span>
        </div>
      )}

      {erro && (
        <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-400" />
          <span>{erro}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1.5">
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
              placeholder="seu.email@exemplo.com ou CPF"
              className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="block text-xs font-medium text-slate-300">
              Senha
            </label>
            <Link
              href="/esqueci-senha"
              className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
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
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="Sua senha secreta"
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

        <button
          type="submit"
          disabled={carregando}
          className="w-full py-3.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm shadow-lg shadow-indigo-600/30 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {carregando ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <LogIn className="w-4 h-4" />
              <span>Entrar na Plataforma</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Cabeçalho / Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600 shadow-xl shadow-indigo-500/25 mb-4 text-white">
            <LogIn className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Tutor Inteligente</h1>
          <p className="text-sm text-indigo-200/80 mt-1">Plataforma EAD de Matemática com IA Socrática</p>
        </div>

        <Suspense fallback={
          <div className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center text-slate-300">
            <div className="w-8 h-8 border-3 border-indigo-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            Carregando...
          </div>
        }>
          <LoginForm />
        </Suspense>

        {/* Rodapé informativo */}
        <p className="text-center text-xs text-slate-400 mt-6">
          Protegido com sessão única e criptografia ponta a ponta.
        </p>
      </div>
    </div>
  );
}
