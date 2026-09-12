"use client";

import React, { useEffect, useState, useTransition } from "react";
import {
  Users,
  Search,
  Filter,
  FileText,
  Download,
  X,
  Clock,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  ShieldAlert,
  GraduationCap,
  Calendar,
  Phone,
  Mail,
  UserCheck,
} from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
} from "recharts";
import { api, getAccessToken, getApiBaseUrl } from "@/lib/api";

interface AlunoResumo {
  id: string;
  nome_completo: string;
  cpf_mascarado: string;
  email: string;
  uf: string;
  cidade: string;
  escola_tipo: string;
  serie_ano: string;
  eh_menor_idade: boolean;
  theta_atual: number;
  faixa_tri: string;
  total_exercicios: number;
  status_matricula: string;
  criado_em: string;
}

interface AlunosPaginados {
  total: number;
  page: number;
  limit: number;
  total_paginas: number;
  items: AlunoResumo[];
}

interface TentativaAuditoria {
  id: string;
  item_id: string;
  enunciado_resumo: string;
  tipo_resolucao: string;
  acertou: boolean;
  pontuacao: number;
  tempo_resposta_segundos: number;
  criado_em: string;
}

interface AlunoDossie {
  id: string;
  nome_completo: string;
  cpf_mascarado: string;
  email: string;
  idade_anos: number;
  eh_menor_idade: boolean;
  dados_responsavel?: {
    nome?: string;
    cpf?: string;
    telefone?: string;
    email?: string;
  } | null;
  uf: string;
  cidade: string;
  bairro?: string;
  escola_tipo: string;
  nome_escola?: string;
  serie_ano: string;
  criado_em: string;
  theta_atual: number;
  erro_padrao: number;
  faixa_tri: string;
  historico_theta: { data: string; theta: number; fonte: string }[];
  radar_areas: { area: string; dominio: number }[];
  horas_liquidas_total: number;
  dias_estudo_total: number;
  total_exercicios_resolvidos: number;
  taxa_acerto_exercicios: number;
  status_matricula: string;
  matricula_expira_em?: string;
  ultimas_tentativas: TentativaAuditoria[];
}

export default function GestaoAlunosPage() {
  const [alunos, setAlunos] = useState<AlunoResumo[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  // Filtros
  const [search, setSearch] = useState("");
  const [filtroEscola, setFiltroEscola] = useState("");
  const [filtroUf, setFiltroUf] = useState("");

  // Modal de Dossiê
  const [selectedAlunoId, setSelectedAlunoId] = useState<string | null>(null);
  const [dossie, setDossie] = useState<AlunoDossie | null>(null);
  const [loadingDossie, setLoadingDossie] = useState(false);
  const [baixandoPdf, setBaixandoPdf] = useState(false);

  const carregarAlunos = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.set("page", String(page));
      params.set("limit", "15");
      if (search.trim()) params.set("search", search.trim());
      if (filtroEscola) params.set("escola_tipo", filtroEscola);
      if (filtroUf) params.set("uf", filtroUf);

      const res = await api.get<AlunosPaginados>(`/api/v1/teacher/alunos?${params.toString()}`);
      setAlunos(res.items);
      setTotal(res.total);
      setTotalPages(res.total_paginas);
    } catch (err) {
      console.error("Falha ao listar alunos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      carregarAlunos();
    }, 300);
    return () => clearTimeout(timer);
  }, [search, filtroEscola, filtroUf, page]);

  const abrirDossie = async (alunoId: string) => {
    setSelectedAlunoId(alunoId);
    setLoadingDossie(true);
    setDossie(null);
    try {
      const resp = await api.get<AlunoDossie>(`/api/v1/teacher/alunos/${alunoId}`);
      setDossie(resp);
    } catch (err) {
      console.error("Erro ao carregar dossiê:", err);
    } finally {
      setLoadingDossie(false);
    }
  };

  const fecharDossie = () => {
    setSelectedAlunoId(null);
    setDossie(null);
  };

  const baixarBoletimPdf = async () => {
    if (!selectedAlunoId) return;
    setBaixandoPdf(true);
    try {
      const token = getAccessToken();
      const apiUrl = getApiBaseUrl();
      const response = await fetch(`${apiUrl}/api/v1/teacher/alunos/${selectedAlunoId}/boletim`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error("Erro ao gerar PDF");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Boletim_${dossie?.nome_completo.replace(/\s+/g, "_") || "Aluno"}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Não foi possível gerar o boletim em PDF.");
    } finally {
      setBaixandoPdf(false);
    }
  };

  const formatarSerie = (serie: string) => {
    const mapas: Record<string, string> = {
      "1_ano": "1º Ano EM",
      "2_ano": "2º Ano EM",
      "3_ano": "3º Ano EM",
      "cursinho": "Pré-Vestibular",
      "todos": "Geral / Todos",
    };
    return mapas[serie] || serie;
  };

  return (
    <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      {/* Topo da página */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Gestão & Acompanhamento de Alunos
          </h1>
          <p className="text-slate-600 dark:text-ink-muted text-sm mt-0.5">
            Dossiê pedagógico individual, histórico psicométrico TRI e emissão de boletins oficiais.
          </p>
        </div>
        <div className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-subject-50 dark:bg-subject-wash text-subject-700 dark:text-subject-300 border border-subject-200 dark:border-subject-800/40 self-start sm:self-auto">
          {total} alunos matriculados
        </div>
      </div>

      {/* Barra de Filtros e Busca */}
      <div className="bg-white dark:bg-surface-card border border-line rounded-2xl p-4 mb-6 shadow-xs flex flex-col md:flex-row items-center gap-3">
        {/* Input de busca debounced */}
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar por nome, e-mail ou CPF..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="w-full pl-10 pr-4 py-2 text-sm rounded-xl border border-slate-200 dark:border-line bg-slate-50 dark:bg-surface-elevated focus:outline-hidden focus:ring-2 focus:ring-subject-500 text-slate-900 dark:text-white placeholder-slate-400"
          />
        </div>

        {/* Filtro Escola */}
        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={filtroEscola}
            onChange={(e) => {
              setFiltroEscola(e.target.value);
              setPage(1);
            }}
            aria-label="Filtrar por rede escolar"
            className="px-3 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-line bg-slate-50 dark:bg-surface-elevated text-slate-700 dark:text-slate-200 focus:outline-hidden"
          >
            <option value="">Todas as Redes</option>
            <option value="publica">Escola Pública</option>
            <option value="privada">Escola Privada</option>
            <option value="militar">Colégio Militar</option>
            <option value="federal">Instituto Federal / ETEC</option>
            <option value="outro">Outra</option>
          </select>

          {/* Filtro UF */}
          <select
            value={filtroUf}
            onChange={(e) => {
              setFiltroUf(e.target.value);
              setPage(1);
            }}
            aria-label="Filtrar por Unidade Federativa (UF)"
            className="px-3 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-line bg-slate-50 dark:bg-surface-elevated text-slate-700 dark:text-slate-200 focus:outline-hidden"
          >
            <option value="">Todas as UFs</option>
            {["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "DF", "GO"].map((uf) => (
              <option key={uf} value={uf}>
                {uf}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabela de Estudantes */}
      <div className="bg-white dark:bg-surface-card border border-line rounded-2xl shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-surface-elevated border-b border-line text-xs font-bold text-slate-500 dark:text-ink-muted uppercase tracking-wider">
              <tr>
                <th className="py-3.5 px-4">Estudante / CPF</th>
                <th className="py-3.5 px-4">Localização</th>
                <th className="py-3.5 px-4">Rede / Série</th>
                <th className="py-3.5 px-4 text-center">Proficiência (θ)</th>
                <th className="py-3.5 px-4 text-center">Exercícios</th>
                <th className="py-3.5 px-4 text-center">Matrícula</th>
                <th className="py-3.5 px-4 text-right">Ação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-line text-slate-700 dark:text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-xs text-slate-400">
                    Carregando listagem de estudantes...
                  </td>
                </tr>
              ) : alunos.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-xs text-slate-400">
                    Nenhum aluno encontrado com os filtros selecionados.
                  </td>
                </tr>
              ) : (
                alunos.map((a) => (
                  <tr key={a.id} className="hover:bg-slate-50/70 dark:hover:bg-surface-elevated/40 transition-colors">
                    <td className="py-3 px-4">
                      <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                        <span>{a.nome_completo}</span>
                        {a.eh_menor_idade && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300 border border-amber-200">
                            Menor
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-slate-400 font-mono mt-0.5">
                        {a.cpf_mascarado} • {a.email}
                      </div>
                    </td>

                    <td className="py-3 px-4 text-xs">
                      <div className="font-medium text-slate-800 dark:text-slate-200">{a.cidade}</div>
                      <div className="text-slate-400">{a.uf}</div>
                    </td>

                    <td className="py-3 px-4 text-xs">
                      <div className="capitalize font-medium text-slate-800 dark:text-slate-200">
                        {a.escola_tipo}
                      </div>
                      <div className="text-slate-400">{formatarSerie(a.serie_ano)}</div>
                    </td>

                    <td className="py-3 px-4 text-center">
                      <span
                        className={`inline-block px-2 py-1 rounded-md text-xs font-bold font-mono ${
                          a.theta_atual < -0.5
                            ? "bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
                            : a.theta_atual <= 1.0
                            ? "bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300"
                            : "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                        }`}
                      >
                        {a.theta_atual >= 0 ? `+${a.theta_atual.toFixed(2)}` : a.theta_atual.toFixed(2)}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-center text-xs font-semibold">
                      {a.total_exercicios}
                    </td>

                    <td className="py-3 px-4 text-center">
                      <span
                        className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
                          a.status_matricula === "active"
                            ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300"
                            : a.status_matricula === "canceled"
                            ? "bg-rose-100 text-rose-800 dark:bg-rose-950/50 dark:text-rose-300"
                            : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400"
                        }`}
                      >
                        {a.status_matricula === "active"
                          ? "Ativa"
                          : a.status_matricula === "canceled"
                          ? "Cancelada"
                          : "Sem plano"}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => abrirDossie(a.id)}
                        className="px-3 py-1.5 rounded-lg text-xs font-bold bg-subject-50 hover:bg-subject-100 dark:bg-subject-wash dark:hover:bg-subject-900/40 text-subject-700 dark:text-subject-300 border border-subject-200 dark:border-subject-800/40 transition-colors shadow-2xs cursor-pointer"
                      >
                        Ver Dossiê
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Paginação */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-line bg-slate-50/50 dark:bg-surface-card">
            <span className="text-xs text-slate-500">
              Página {page} de {totalPages} ({total} alunos)
            </span>
            <div className="flex items-center gap-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="p-1.5 rounded-lg border border-line text-slate-600 disabled:opacity-30 cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                className="p-1.5 rounded-lg border border-line text-slate-600 disabled:opacity-30 cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modal / Gaveta de Dossiê do Estudante */}
      {selectedAlunoId && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white dark:bg-surface-card border border-line rounded-3xl w-full max-w-3xl shadow-2xl overflow-hidden my-8">
            {/* Header do Modal */}
            <div className="flex items-center justify-between p-6 border-b border-line bg-slate-50 dark:bg-surface-elevated">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-subject-100 dark:bg-subject-wash text-subject-600 dark:text-subject-400 flex items-center justify-center font-black">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                    {loadingDossie ? "Carregando Ficha..." : dossie?.nome_completo}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-ink-muted">
                    Dossiê Pedagógico & Auditoria de Atividades
                  </p>
                </div>
              </div>
              <button
                onClick={fecharDossie}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 dark:hover:bg-surface-elevated transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {loadingDossie ? (
              <div className="p-12 text-center text-sm text-slate-400">
                Compilando dados psicométricos e histórico de estudos...
              </div>
            ) : dossie ? (
              <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto">
                {/* Seção Alerta de Menor de Idade (RN-PRF-006) */}
                {dossie.eh_menor_idade && dossie.dados_responsavel && (
                  <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40">
                    <div className="flex items-center gap-2 text-xs font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider mb-2">
                      <ShieldAlert className="w-4 h-4" />
                      <span>Estudante Menor de 18 Anos — Contato dos Pais/Responsáveis</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-amber-900 dark:text-amber-200">
                      <div>
                        <strong>Nome:</strong> {dossie.dados_responsavel.nome || "Não informado"}
                      </div>
                      <div>
                        <strong>CPF:</strong> {dossie.dados_responsavel.cpf || "Não informado"}
                      </div>
                      <div className="flex items-center gap-1.5">
                        <Phone className="w-3.5 h-3.5 text-amber-600" />
                        <span>{dossie.dados_responsavel.telefone || "Telefone não informado"}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <Mail className="w-3.5 h-3.5 text-amber-600" />
                        <span>{dossie.dados_responsavel.email || "E-mail não informado"}</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Grid de Indicadores Centrais */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3.5 rounded-xl border border-line bg-slate-50/60 dark:bg-surface-elevated/40">
                    <span className="text-[11px] font-bold text-slate-400 uppercase">Theta TRI (θ)</span>
                    <div className="text-xl font-black text-slate-900 dark:text-white mt-1">
                      {dossie.theta_atual >= 0 ? `+${dossie.theta_atual}` : dossie.theta_atual}
                    </div>
                    <span className="text-[10px] text-slate-500 font-medium capitalize">
                      {dossie.faixa_tri}
                    </span>
                  </div>

                  <div className="p-3.5 rounded-xl border border-line bg-slate-50/60 dark:bg-surface-elevated/40">
                    <span className="text-[11px] font-bold text-slate-400 uppercase">Horas Líquidas</span>
                    <div className="text-xl font-black text-slate-900 dark:text-white mt-1">
                      {dossie.horas_liquidas_total}h
                    </div>
                    <span className="text-[10px] text-slate-500 font-medium">
                      {dossie.dias_estudo_total} dias de estudo
                    </span>
                  </div>

                  <div className="p-3.5 rounded-xl border border-line bg-slate-50/60 dark:bg-surface-elevated/40">
                    <span className="text-[11px] font-bold text-slate-400 uppercase">Taxa de Acerto</span>
                    <div className="text-xl font-black text-slate-900 dark:text-white mt-1">
                      {dossie.taxa_acerto_exercicios}%
                    </div>
                    <span className="text-[10px] text-slate-500 font-medium">
                      {dossie.total_exercicios_resolvidos} exercícios
                    </span>
                  </div>

                  <div className="p-3.5 rounded-xl border border-line bg-slate-50/60 dark:bg-surface-elevated/40">
                    <span className="text-[11px] font-bold text-slate-400 uppercase">Matrícula</span>
                    <div className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-1 capitalize">
                      {dossie.status_matricula === "active" ? "Ativa (365d)" : "Inativa"}
                    </div>
                    <span className="text-[10px] text-slate-500">
                      {dossie.matricula_expira_em
                        ? new Date(dossie.matricula_expira_em).toLocaleDateString("pt-BR")
                        : "Sem vigência"}
                    </span>
                  </div>
                </div>

                {/* Gráfico Radar de Áreas */}
                <div className="border border-line rounded-2xl p-4 bg-white dark:bg-surface-card">
                  <h4 className="font-bold text-sm text-slate-900 dark:text-white mb-2">
                    Polígono de Domínio por Grande Área
                  </h4>
                  <div className="h-56 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart data={dossie.radar_areas}>
                        <PolarGrid strokeOpacity={0.2} />
                        <PolarAngleAxis dataKey="area" tick={{ fontSize: 10, fill: "#64748B" }} />
                        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 9 }} />
                        <Radar
                          name="Domínio (%)"
                          dataKey="dominio"
                          stroke="#F57C00"
                          fill="#F57C00"
                          fillOpacity={0.4}
                        />
                        <Tooltip />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Trilha de Auditoria de Tentativas (RN-PRF-010) */}
                <div className="border border-line rounded-2xl p-4 bg-white dark:bg-surface-card">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                      <Clock className="w-4 h-4 text-subject-500" />
                      <span>Trilha de Auditoria de Exercícios Recentes</span>
                    </h4>
                    <span className="text-[11px] text-slate-400">RN-PRF-010</span>
                  </div>

                  <div className="divide-y divide-slate-100 dark:divide-line text-xs max-h-48 overflow-y-auto">
                    {dossie.ultimas_tentativas.length === 0 ? (
                      <div className="py-4 text-center text-slate-400">
                        Nenhuma tentativa registrada até o momento.
                      </div>
                    ) : (
                      dossie.ultimas_tentativas.map((t) => (
                        <div key={t.id} className="py-2.5 flex items-center justify-between gap-3">
                          <div className="flex items-center gap-2 min-w-0">
                            {t.acertou ? (
                              <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                            ) : (
                              <XCircle className="w-4 h-4 text-rose-500 flex-shrink-0" />
                            )}
                            <span className="truncate text-slate-700 dark:text-slate-300 max-w-sm">
                              {t.enunciado_resumo}
                            </span>
                          </div>
                          <div className="flex items-center gap-3 text-slate-400 flex-shrink-0 font-mono text-[11px]">
                            <span>{t.tempo_resposta_segundos}s</span>
                            <span>{new Date(t.criado_em).toLocaleDateString("pt-BR")}</span>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Rodapé com botão de emissão de Boletim PDF */}
                <div className="pt-2 flex items-center justify-between gap-4 border-t border-line">
                  <span className="text-xs text-slate-500">
                    Boletim oficial vetorial gerado sob demanda para envio formal aos responsáveis.
                  </span>
                  <button
                    onClick={baixarBoletimPdf}
                    disabled={baixandoPdf}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-subject-500 hover:bg-subject-600 text-white transition-colors shadow-xs cursor-pointer disabled:opacity-50"
                  >
                    <Download className={`w-3.5 h-3.5 ${baixandoPdf ? "animate-bounce" : ""}`} />
                    <span>{baixandoPdf ? "Gerando PDF..." : "Baixar Boletim (PDF)"}</span>
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </main>
  );
}
