"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AlertCircle, ArrowLeft, CheckCircle2, GraduationCap, MapPin } from "lucide-react";

import { useOnboarding } from "@/contexts/OnboardingContext";
import { api, extrairMensagemErro, setAccessToken } from "@/lib/api";
import { apenasDigitos, mascaraCEP } from "@/lib/formatters";
import { EscolaTipo, ViaCepResponse } from "@/types/onboarding";

const inputCls =
  "w-full px-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all";

const OPCOES_SERIE = [
  { valor: "6_ano", rotulo: "6º Ano — Fundamental" },
  { valor: "7_ano", rotulo: "7º Ano — Fundamental" },
  { valor: "8_ano", rotulo: "8º Ano — Fundamental" },
  { valor: "9_ano", rotulo: "9º Ano — Fundamental" },
  { valor: "1_ano", rotulo: "1º Ano — Ensino Médio" },
  { valor: "2_ano", rotulo: "2º Ano — Ensino Médio" },
  { valor: "3_ano", rotulo: "3º Ano — Ensino Médio" },
  { valor: "pre_vestibular", rotulo: "Pré-Vestibular / Outro" },
];

const UFS = [
  "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
  "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
];

export default function Step3Academic({ onBack }: { onBack: () => void }) {
  const { form, setCampo, finalizarCadastro, salvandoRascunho } = useOnboarding();
  const router = useRouter();
  const [erro, setErro] = useState<string | null>(null);
  const [avisoCep, setAvisoCep] = useState<string | null>(null);
  const [buscandoCep, setBuscandoCep] = useState(false);
  const [carregando, setCarregando] = useState(false);

  const consultarCep = async (cepMascarado: string) => {
    const cep = apenasDigitos(cepMascarado);
    if (cep.length !== 8) return;

    setBuscandoCep(true);
    setAvisoCep(null);
    try {
      const resposta = await api.get<ViaCepResponse>(`/api/v1/onboarding/cep/${cep}`);
      if (resposta.uf) setCampo("uf", resposta.uf);
      if (resposta.cidade) setCampo("cidade", resposta.cidade);
      if (resposta.bairro) setCampo("bairro", resposta.bairro);
      if (resposta.logradouro) setCampo("logradouro", resposta.logradouro);
    } catch (err: any) {
      // ViaCEP indisponível ou CEP inexistente: libera preenchimento manual (RN-ONB-006)
      setAvisoCep(
        err.status === 404
          ? "CEP não encontrado. Preencha o endereço manualmente."
          : "Consulta de CEP indisponível. Preencha o endereço manualmente."
      );
    } finally {
      setBuscandoCep(false);
    }
  };

  const validarLocalmente = (): string | null => {
    if (apenasDigitos(form.cep).length !== 8) return "Informe um CEP válido com 8 dígitos.";
    if (!form.uf || form.uf.length !== 2) return "Selecione a UF.";
    if (!form.cidade || form.cidade.trim().length < 2) return "Informe a cidade.";
    if (!form.escola_tipo) return "Selecione a rede de ensino.";
    if (!form.serie_ano) return "Selecione sua série/ano atual.";
    return null;
  };

  const handleFinalizar = async () => {
    setErro(null);
    const erroLocal = validarLocalmente();
    if (erroLocal) {
      setErro(erroLocal);
      return;
    }

    setCarregando(true);
    try {
      const resposta = await finalizarCadastro();
      setAccessToken(resposta.access_token);
      router.push("/materias");
    } catch (err: any) {
      setErro(extrairMensagemErro(err, "Não foi possível concluir o cadastro. Tente novamente."));
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">Acadêmico & Endereço</h2>
        <p className="text-xs text-slate-500 dark:text-ink-muted mt-1">
          Onde você estuda e onde podemos te encontrar.
        </p>
      </div>

      {erro && (
        <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 text-rose-800 dark:text-rose-300 text-xs flex items-start gap-2.5 leading-relaxed">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
          <span>{erro}</span>
        </div>
      )}
      {avisoCep && (
        <div className="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 text-amber-800 dark:text-amber-300 text-xs flex items-start gap-2.5 leading-relaxed">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
          <span>{avisoCep}</span>
        </div>
      )}

      <div>
        <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          CEP {buscandoCep && <span className="font-normal text-slate-400">(consultando...)</span>}
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <MapPin className="w-4 h-4" />
          </div>
          <input
            type="text"
            inputMode="numeric"
            value={form.cep}
            onChange={(e) => setCampo("cep", mascaraCEP(e.target.value))}
            onBlur={(e) => void consultarCep(e.target.value)}
            placeholder="00000-000"
            className="w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">UF</label>
          <select
            value={form.uf}
            onChange={(e) => setCampo("uf", e.target.value)}
            className={inputCls}
          >
            <option value="">—</option>
            {UFS.map((uf) => (
              <option key={uf} value={uf}>{uf}</option>
            ))}
          </select>
        </div>
        <div className="col-span-1 sm:col-span-2">
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Cidade</label>
          <input
            type="text"
            value={form.cidade}
            onChange={(e) => setCampo("cidade", e.target.value)}
            placeholder="Cidade"
            className={inputCls}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Bairro</label>
          <input
            type="text"
            value={form.bairro ?? ""}
            onChange={(e) => setCampo("bairro", e.target.value)}
            placeholder="Opcional"
            className={inputCls}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Logradouro
          </label>
          <input
            type="text"
            value={form.logradouro ?? ""}
            onChange={(e) => setCampo("logradouro", e.target.value)}
            placeholder="Rua, avenida..."
            className={inputCls}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Número</label>
          <input
            type="text"
            value={form.numero ?? ""}
            onChange={(e) => setCampo("numero", e.target.value)}
            placeholder="Opcional"
            className={inputCls}
          />
        </div>
      </div>

      <div className="pt-1 border-t border-slate-100 dark:border-line" />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Rede de ensino
          </label>
          <select
            value={form.escola_tipo}
            onChange={(e) => setCampo("escola_tipo", e.target.value as EscolaTipo)}
            className={inputCls}
          >
            <option value="publica">Pública</option>
            <option value="privada">Privada</option>
            <option value="outro">Outro</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Instituição de ensino
          </label>
          <input
            type="text"
            value={form.nome_escola ?? ""}
            onChange={(e) => setCampo("nome_escola", e.target.value)}
            placeholder="Nome da escola (opcional)"
            className={inputCls}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
          Série / Ano atual
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <GraduationCap className="w-4 h-4" />
          </div>
          <select
            value={form.serie_ano}
            onChange={(e) => setCampo("serie_ano", e.target.value)}
            className="w-full pl-10 pr-3.5 py-2.5 bg-white dark:bg-surface-bg border border-slate-300 dark:border-line rounded-xl text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-subject-300 focus:border-subject-500 transition-all"
          >
            <option value="">Selecione...</option>
            {OPCOES_SERIE.map((opcao) => (
              <option key={opcao.valor} value={opcao.valor}>{opcao.rotulo}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="pt-2 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onBack}
            disabled={carregando}
            className="py-3 px-4 rounded-xl border border-slate-300 dark:border-line text-slate-600 dark:text-slate-300 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-surface-bg transition-colors flex items-center gap-2 disabled:opacity-50 cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Voltar</span>
          </button>
          <span className="text-[11px] text-slate-400 dark:text-slate-500">
            {salvandoRascunho ? "Salvando rascunho..." : "Rascunho salvo"}
          </span>
        </div>
        <button
          type="button"
          onClick={handleFinalizar}
          disabled={carregando}
          className="py-3 px-5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-semibold text-sm shadow-sm transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {carregando ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <CheckCircle2 className="w-4 h-4" />
              <span>Concluir cadastro</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
