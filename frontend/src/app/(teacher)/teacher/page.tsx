"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Users,
  Activity,
  DollarSign,
  TrendingUp,
  School,
  MapPin,
  Sparkles,
  ArrowRight,
  RefreshCw,
  AlertCircle,
  PieChart as PieIcon,
  BarChart3,
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  AreaChart,
  Area,
} from "recharts";
import { api } from "@/lib/api";
import { useHeartbeat } from "@/hooks/useHeartbeat";

interface DistribuicaoItem {
  label: string;
  valor: number;
  percentual: number;
}

interface FaturamentoItem {
  mes: string;
  faturamento_bruto: number;
  faturamento_liquido: number;
  transacoes: number;
}

interface AnalyticsData {
  total_faturado_bruto: number;
  total_faturado_liquido: number;
  total_alunos: number;
  alunos_ativos: number;
  theta_medio_global: number;
  distribuicao_escola: DistribuicaoItem[];
  distribuicao_uf: DistribuicaoItem[];
  distribuicao_tri: {
    basico: number;
    intermediario: number;
    avancado: number;
  };
  faturamento_mensal: FaturamentoItem[];
  metodos_pagamento: {
    pix: number;
    credit_card: number;
  };
}

const CORES_DONUT = ["#F57C00", "#0284C7", "#10B981", "#8B5CF6", "#64748B"];

export default function TeacherDashboardPage() {
  useHeartbeat();

  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const carregarDados = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get<AnalyticsData>("/api/v1/teacher/analytics");
      setData(resp);
    } catch (err: any) {
      setError(err?.message || "Falha ao carregar indicadores analíticos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  const triData = data
    ? [
        { faixa: "Básico (θ < -0.5)", quantidade: data.distribuicao_tri.basico, fill: "#EF4444" },
        { faixa: "Intermediário (-0.5 a +1.0)", quantidade: data.distribuicao_tri.intermediario, fill: "#F59E0B" },
        { faixa: "Avançado (θ > +1.0)", quantidade: data.distribuicao_tri.avancado, fill: "#10B981" },
      ]
    : [];

  return (
    <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      {/* Header do Dashboard */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Dashboard Docente & Analytics
          </h1>
          <p className="text-slate-600 dark:text-ink-muted text-sm mt-1">
            Métricas de desempenho pedagógico, perfil demográfico dos alunos e consolidação financeira.
          </p>
        </div>
        <button
          onClick={carregarDados}
          disabled={loading}
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-white dark:bg-surface-card border border-line text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-surface-elevated transition-colors shadow-2xs self-start sm:self-auto cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-subject-500" : ""}`} />
          <span>Atualizar Indicadores</span>
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 text-rose-800 dark:text-rose-300 flex items-center gap-3 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-600" />
          <span>{error}</span>
        </div>
      )}

      {/* Grid de 4 KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-8">
        {/* KPI 1: Alunos Cadastrados */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              Total de Estudantes
            </span>
            <div className="w-8 h-8 rounded-lg bg-subject-100 dark:bg-subject-wash text-subject-600 dark:text-subject-400 flex items-center justify-center">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              {loading ? "--" : data?.total_alunos ?? 0}
            </div>
            <div className="text-xs text-slate-500 dark:text-ink-muted mt-1">
              {loading ? "Calculando..." : `${data?.alunos_ativos ?? 0} alunos ativos no mês`}
            </div>
          </div>
        </div>

        {/* KPI 2: Alunos Ativos */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              Engajamento Ativo
            </span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center border border-emerald-200/50">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
              <span>{loading ? "--" : data?.alunos_ativos ?? 0}</span>
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <div className="text-xs text-emerald-600 dark:text-emerald-400 font-medium mt-1">
              Presença e matrícula regular
            </div>
          </div>
        </div>

        {/* KPI 3: Faturamento Líquido */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              Receita Líquida
            </span>
            <div className="w-8 h-8 rounded-lg bg-sky-50 dark:bg-sky-950/40 text-sky-600 dark:text-sky-400 flex items-center justify-center border border-sky-200/50">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              {loading
                ? "--"
                : (data?.total_faturado_liquido ?? 0).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}
            </div>
            <div className="text-xs text-slate-500 dark:text-ink-muted mt-1">
              Bruto:{" "}
              {(data?.total_faturado_bruto ?? 0).toLocaleString("pt-BR", {
                style: "currency",
                currency: "BRL",
              })}
            </div>
          </div>
        </div>

        {/* KPI 4: Theta Médio TRI */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              Proficiência Média (θ)
            </span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 flex items-center justify-center border border-indigo-200/50">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              {loading
                ? "--"
                : `${(data?.theta_medio_global ?? 0) >= 0 ? "+" : ""}${(
                    data?.theta_medio_global ?? 0
                  ).toFixed(2)}`}
            </div>
            <div className="text-xs text-indigo-600 dark:text-indigo-400 font-medium mt-1">
              Escala TRI (-3.0 a +3.0)
            </div>
          </div>
        </div>
      </div>

      {/* Seção de Gráficos Analíticos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gráfico 1: Demografia Escolar */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 sm:p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <School className="w-5 h-5 text-subject-500" />
              <h3 className="font-bold text-slate-900 dark:text-white text-base">
                Distribuição por Rede de Ensino
              </h3>
            </div>
            <span className="text-xs text-slate-400">RN-PRF-005</span>
          </div>

          <div className="h-64 w-full">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Carregando dados demográficos...
              </div>
            ) : data?.distribuicao_escola && data.distribuicao_escola.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.distribuicao_escola}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={85}
                    paddingAngle={4}
                    dataKey="valor"
                    nameKey="label"
                  >
                    {data.distribuicao_escola.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={CORES_DONUT[index % CORES_DONUT.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value: any, name: any, item: any) => [
                      `${value} alunos (${item.payload.percentual}%)`,
                      name,
                    ]}
                  />
                  <Legend verticalAlign="bottom" height={36} iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Nenhum dado demográfico disponível.
              </div>
            )}
          </div>
        </div>

        {/* Gráfico 2: Distribuição TRI CAT */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 sm:p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-500" />
              <h3 className="font-bold text-slate-900 dark:text-white text-base">
                Faixas de Proficiência TRI (CAT)
              </h3>
            </div>
            <span className="text-xs text-slate-400">RN-PRF-004</span>
          </div>

          <div className="h-64 w-full">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Calculando faixas psicométricas...
              </div>
            ) : triData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={triData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis dataKey="faixa" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(val: any) => [`${val} estudantes`, "Total"]} />
                  <Bar dataKey="quantidade" radius={[6, 6, 0, 0]}>
                    {triData.map((entry, index) => (
                      <Cell key={`bar-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Nenhuma avaliação diagnóstica registrada.
              </div>
            )}
          </div>
        </div>

        {/* Gráfico 3: Alunos por Estado (UF) */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 sm:p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-sky-500" />
              <h3 className="font-bold text-slate-900 dark:text-white text-base">
                Top Estados por Número de Alunos
              </h3>
            </div>
            <span className="text-xs text-slate-400">RN-PRF-003</span>
          </div>

          <div className="h-64 w-full">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Carregando distribuição geográfica...
              </div>
            ) : data?.distribuicao_uf && data.distribuicao_uf.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={data.distribuicao_uf}
                  layout="vertical"
                  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} horizontal={false} />
                  <XAxis type="number" allowDecimals={false} tick={{ fontSize: 11 }} />
                  <YAxis type="category" dataKey="label" width={30} tick={{ fontSize: 12, fontWeight: "bold" }} />
                  <Tooltip formatter={(val: any) => [`${val} alunos`, "Estudantes"]} />
                  <Bar dataKey="valor" fill="#0284C7" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Nenhum dado geográfico disponível.
              </div>
            )}
          </div>
        </div>

        {/* Gráfico 4: Evolução do Faturamento Mensal */}
        <div className="bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-5 sm:p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-emerald-500" />
              <h3 className="font-bold text-slate-900 dark:text-white text-base">
                Evolução do Faturamento Mensal
              </h3>
            </div>
            <span className="text-xs text-slate-400">RN-PRF-016</span>
          </div>

          <div className="h-64 w-full">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Carregando histórico de vendas...
              </div>
            ) : data?.faturamento_mensal && data.faturamento_mensal.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={data.faturamento_mensal}
                  margin={{ top: 10, right: 10, left: -10, bottom: 0 }}
                >
                  <defs>
                    <linearGradient id="colorLiquido" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#10B981" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis dataKey="mes" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip
                    formatter={(val: any) => [
                      Number(val).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }),
                      "Líquido",
                    ]}
                  />
                  <Area
                    type="monotone"
                    dataKey="faturamento_liquido"
                    stroke="#10B981"
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#colorLiquido)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Nenhuma transação financeira concluída no período.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Ações Rápidas de Navegação */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Link
          href="/teacher/alunos"
          className="group bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-xs hover:border-subject-400 dark:hover:border-subject-700 transition-all flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-700 dark:text-subject-300 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
              <Users className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-slate-900 dark:text-white text-base mb-1">
              Gestão de Estudantes
            </h4>
            <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
              Consulte a ficha pedagógica completa, histórico de proficiência TRI e emita o Boletim Oficial em PDF.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-line flex items-center justify-between text-xs font-semibold text-subject-600 dark:text-subject-400">
            <span>Acessar Alunos</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link
          href="/teacher/curadoria"
          className="group bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-xs hover:border-blue-400 dark:hover:border-blue-700 transition-all flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform border border-blue-100 dark:border-blue-800/30">
              <PieIcon className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-slate-900 dark:text-white text-base mb-1">
              Central de Curadoria KaTeX
            </h4>
            <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
              Editor split-screen em tempo real dos 11 volumes didáticos, videoaulas e 4 blocos instrucionais.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-line flex items-center justify-between text-xs font-semibold text-blue-600 dark:text-blue-400">
            <span>Editar Conteúdo</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link
          href="/teacher/financeiro"
          className="group bg-white dark:bg-surface-card border border-slate-200/90 dark:border-line rounded-2xl p-6 shadow-xs hover:border-emerald-400 dark:hover:border-emerald-700 transition-all flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform border border-emerald-100 dark:border-emerald-800/30">
              <DollarSign className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-slate-900 dark:text-white text-base mb-1">
              Extrato Financeiro & Estorno
            </h4>
            <p className="text-xs text-slate-500 dark:text-ink-muted leading-relaxed">
              Auditoria de vendas, taxas retidas do Asaas e estorno administrativo dentro do prazo legal de 7 dias (CDC).
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-line flex items-center justify-between text-xs font-semibold text-emerald-600 dark:text-emerald-400">
            <span>Ver Transações</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>
      </div>
    </main>
  );
}
