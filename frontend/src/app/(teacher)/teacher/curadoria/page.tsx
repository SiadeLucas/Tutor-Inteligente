"use client";

import React, { useEffect, useState } from "react";
import {
  BookOpenCheck,
  Save,
  CheckCircle2,
  AlertCircle,
  Video,
  Eye,
  Columns,
  RefreshCw,
  Code2,
  Sparkles,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";
import { KaTeXRenderer } from "@/components/math/KaTeXRenderer";

interface CapituloItem {
  capitulo_id: string;
  numero_capitulo: number;
  titulo: string;
  tempo_estimado_min: number;
  tem_aula: boolean;
  publicado: boolean;
  atualizado_em?: string;
}

interface VolumeItem {
  volume_id: string;
  numero_volume: number;
  titulo: string;
  grande_area: string;
  total_capitulos: number;
  capitulos: CapituloItem[];
}

interface AulaDetalhe {
  capitulo_id: string;
  capitulo_titulo: string;
  numero_capitulo: number;
  volume_titulo: string;
  numero_volume: number;
  bloco1_teoria_katex: string;
  bloco2_exemplos_katex: string;
  bloco3_dicas_ia: string;
  video_url?: string | null;
  publicado: boolean;
  atualizado_em?: string;
}

export default function CuradoriaPage() {
  const [volumes, setVolumes] = useState<VolumeItem[]>([]);
  const [loadingVolumes, setLoadingVolumes] = useState(true);

  const [selectedVolumeId, setSelectedVolumeId] = useState<string>("");
  const [selectedCapituloId, setSelectedCapituloId] = useState<string>("");

  const [aula, setAula] = useState<AulaDetalhe | null>(null);
  const [loadingAula, setLoadingAula] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [mensagemSucesso, setMensagemSucesso] = useState<string | null>(null);
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);

  // Aba ativa de edição: 1 = Teoria, 2 = Exemplos, 3 = Dicas IA
  const [blocoAtivo, setBlocoAtivo] = useState<1 | 2 | 3>(1);

  // Conteúdo em edição
  const [bloco1, setBloco1] = useState("");
  const [bloco2, setBloco2] = useState("");
  const [bloco3, setBloco3] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [publicado, setPublicado] = useState(true);

  // Carrega volumes ao iniciar
  useEffect(() => {
    async function carregarVolumes() {
      setLoadingVolumes(true);
      try {
        const res = await api.get<VolumeItem[]>("/api/v1/teacher/curadoria/volumes");
        setVolumes(res);
        if (res.length > 0) {
          setSelectedVolumeId(res[0].volume_id);
          if (res[0].capitulos.length > 0) {
            setSelectedCapituloId(res[0].capitulos[0].capitulo_id);
          }
        }
      } catch (err) {
        console.error("Erro ao carregar volumes:", err);
      } finally {
        setLoadingVolumes(false);
      }
    }
    carregarVolumes();
  }, []);

  // Ao mudar capítulo selecionado, carrega aula
  useEffect(() => {
    if (!selectedCapituloId) return;

    async function carregarAula() {
      setLoadingAula(true);
      setMensagemSucesso(null);
      setMensagemErro(null);
      try {
        const res = await api.get<AulaDetalhe>(`/api/v1/teacher/curadoria/aulas/${selectedCapituloId}`);
        setAula(res);
        setBloco1(res.bloco1_teoria_katex || "");
        setBloco2(res.bloco2_exemplos_katex || "");
        setBloco3(res.bloco3_dicas_ia || "");
        setVideoUrl(res.video_url || "");
        setPublicado(res.publicado);
      } catch (err) {
        console.error("Erro ao carregar aula:", err);
      } finally {
        setLoadingAula(false);
      }
    }
    carregarAula();
  }, [selectedCapituloId]);

  // Volume selecionado no dropdown
  const volumeAtual = volumes.find((v) => v.volume_id === selectedVolumeId);

  // Salvar aula
  const handleSalvar = async () => {
    if (!selectedCapituloId) return;
    setSalvando(true);
    setMensagemSucesso(null);
    setMensagemErro(null);

    try {
      const payload = {
        bloco1_teoria_katex: bloco1,
        bloco2_exemplos_katex: bloco2,
        bloco3_dicas_ia: bloco3,
        video_url: videoUrl.trim() || null,
        publicado: publicado,
      };

      const res = await api.put<AulaDetalhe>(
        `/api/v1/teacher/curadoria/aulas/${selectedCapituloId}`,
        payload
      );
      setAula(res);
      setMensagemSucesso("Conteúdo da aula e fórmulas KaTeX salvos com sucesso!");
      setTimeout(() => setMensagemSucesso(null), 4000);
    } catch (err: any) {
      setMensagemErro(err?.message || "Erro ao salvar alterações da aula.");
    } finally {
      setSalvando(false);
    }
  };

  // Atalhos rápidos de inserção de código KaTeX
  const inserirKaTeX = (texto: string) => {
    if (blocoAtivo === 1) setBloco1((prev) => prev + texto);
    else if (blocoAtivo === 2) setBloco2((prev) => prev + texto);
    else if (blocoAtivo === 3) setBloco3((prev) => prev + texto);
  };

  const getConteudoAtivo = () => {
    if (blocoAtivo === 1) return bloco1;
    if (blocoAtivo === 2) return bloco2;
    return bloco3;
  };

  const setConteudoAtivo = (val: string) => {
    if (blocoAtivo === 1) setBloco1(val);
    else if (blocoAtivo === 2) setBloco2(val);
    else setBloco3(val);
  };

  return (
    <main className="flex-1 flex flex-col h-[calc(100vh-3.5rem-41px)] overflow-hidden">
      {/* Barra de Controle Superior: Seletores de Volume / Capítulo e Salvar */}
      <div className="bg-white dark:bg-surface-card border-b border-line px-4 sm:px-6 py-2.5 flex flex-wrap items-center justify-between gap-3 flex-shrink-0">
        <div className="flex flex-wrap items-center gap-3">
          {/* Seletor Volume */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Volume:</span>
            <select
              value={selectedVolumeId}
              onChange={(e) => {
                const volId = e.target.value;
                setSelectedVolumeId(volId);
                const vol = volumes.find((v) => v.volume_id === volId);
                if (vol && vol.capitulos.length > 0) {
                  setSelectedCapituloId(vol.capitulos[0].capitulo_id);
                }
              }}
              aria-label="Selecionar volume didático"
              className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-line bg-slate-50 dark:bg-surface-elevated text-slate-900 dark:text-white max-w-[220px] truncate"
            >
              {volumes.map((v) => (
                <option key={v.volume_id} value={v.volume_id}>
                  Vol. {v.numero_volume} — {v.titulo}
                </option>
              ))}
            </select>
          </div>

          {/* Seletor Capítulo */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Capítulo:</span>
            <select
              value={selectedCapituloId}
              onChange={(e) => setSelectedCapituloId(e.target.value)}
              aria-label="Selecionar capítulo"
              className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-line bg-slate-50 dark:bg-surface-elevated text-slate-900 dark:text-white max-w-[260px] truncate"
            >
              {volumeAtual?.capitulos.map((c) => (
                <option key={c.capitulo_id} value={c.capitulo_id}>
                  Cap. {c.numero_capitulo}: {c.titulo} {c.publicado ? "✓" : "(Rascunho)"}
                </option>
              ))}
            </select>
          </div>

          {/* Status de Publicação */}
          <label className="flex items-center gap-2 text-xs font-semibold cursor-pointer pl-2 border-l border-line text-slate-700 dark:text-slate-300">
            <input
              type="checkbox"
              checked={publicado}
              onChange={(e) => setPublicado(e.target.checked)}
              className="rounded border-slate-300 text-subject-600 focus:ring-subject-500"
            />
            <span>Publicado para Estudantes</span>
          </label>
        </div>

        {/* Botão de Salvar */}
        <div className="flex items-center gap-3">
          {mensagemSucesso && (
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5 animate-fadeIn">
              <CheckCircle2 className="w-4 h-4" />
              <span>{mensagemSucesso}</span>
            </span>
          )}
          {mensagemErro && (
            <span className="text-xs font-bold text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
              <AlertCircle className="w-4 h-4" />
              <span>{mensagemErro}</span>
            </span>
          )}

          <button
            onClick={handleSalvar}
            disabled={salvando || loadingAula}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-bold bg-subject-500 hover:bg-subject-600 text-white transition-colors shadow-xs cursor-pointer disabled:opacity-50"
          >
            <Save className={`w-3.5 h-3.5 ${salvando ? "animate-spin" : ""}`} />
            <span>{salvando ? "Salvando..." : "Salvar Alterações"}</span>
          </button>
        </div>
      </div>

      {/* Toolbar KaTeX & Abas de Bloco */}
      <div className="bg-slate-50 dark:bg-surface-elevated/60 border-b border-line px-4 sm:px-6 py-2 flex flex-wrap items-center justify-between gap-3 flex-shrink-0">
        {/* Abas de Bloco */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setBlocoAtivo(1)}
            className={`px-3 py-1 rounded-md text-xs font-bold transition-colors cursor-pointer ${
              blocoAtivo === 1
                ? "bg-white dark:bg-surface-card text-subject-600 dark:text-subject-400 shadow-2xs border border-line"
                : "text-slate-500 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            Bloco 1: Teoria Fundamental
          </button>
          <button
            onClick={() => setBlocoAtivo(2)}
            className={`px-3 py-1 rounded-md text-xs font-bold transition-colors cursor-pointer ${
              blocoAtivo === 2
                ? "bg-white dark:bg-surface-card text-subject-600 dark:text-subject-400 shadow-2xs border border-line"
                : "text-slate-500 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            Bloco 2: Exemplos Práticos
          </button>
          <button
            onClick={() => setBlocoAtivo(3)}
            className={`px-3 py-1 rounded-md text-xs font-bold transition-colors cursor-pointer ${
              blocoAtivo === 3
                ? "bg-white dark:bg-surface-card text-subject-600 dark:text-subject-400 shadow-2xs border border-line"
                : "text-slate-500 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            Bloco 3: Dicas Socráticas da IA
          </button>
        </div>

        {/* Toolbar de Fórmulas Rápidas */}
        <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-none">
          <span className="text-[11px] font-bold text-slate-400 uppercase mr-1">Inserir KaTeX:</span>
          <button
            onClick={() => inserirKaTeX(" $x$ ")}
            className="px-2 py-0.5 rounded text-xs font-mono bg-white dark:bg-surface-card border border-line hover:border-subject-300 text-slate-700 dark:text-slate-300 cursor-pointer shadow-2xs"
            title="Expressão em linha"
          >
            $inline$
          </button>
          <button
            onClick={() => inserirKaTeX("\n$$\n f(x) = \\dots \n$$\n")}
            className="px-2 py-0.5 rounded text-xs font-mono bg-white dark:bg-surface-card border border-line hover:border-subject-300 text-slate-700 dark:text-slate-300 cursor-pointer shadow-2xs"
            title="Equação em bloco"
          >
            $$display$$
          </button>
          <button
            onClick={() => inserirKaTeX("\\frac{a}{b}")}
            className="px-2 py-0.5 rounded text-xs font-mono bg-white dark:bg-surface-card border border-line hover:border-subject-300 text-slate-700 dark:text-slate-300 cursor-pointer shadow-2xs"
            title="Fração"
          >
            \frac
          </button>
          <button
            onClick={() => inserirKaTeX("\\sqrt{x}")}
            className="px-2 py-0.5 rounded text-xs font-mono bg-white dark:bg-surface-card border border-line hover:border-subject-300 text-slate-700 dark:text-slate-300 cursor-pointer shadow-2xs"
            title="Raiz Quadrada"
          >
            \sqrt
          </button>
          <button
            onClick={() => inserirKaTeX("\\sum_{i=1}^{n}")}
            className="px-2 py-0.5 rounded text-xs font-mono bg-white dark:bg-surface-card border border-line hover:border-subject-300 text-slate-700 dark:text-slate-300 cursor-pointer shadow-2xs"
            title="Somatório"
          >
            \sum
          </button>
          <button
            onClick={() => inserirKaTeX("\n> [!TIP]\n> Dica importante aqui.\n")}
            className="px-2 py-0.5 rounded text-xs font-sans bg-amber-50 dark:bg-amber-950/40 border border-amber-200 text-amber-800 dark:text-amber-300 cursor-pointer"
            title="Alerta Pedagógico"
          >
            [!TIP]
          </button>
        </div>
      </div>

      {/* Editor Split-Screen (65% / 35% ou 50% / 50%) */}
      <div className="flex-1 flex flex-col md:flex-row h-full overflow-hidden">
        {/* Painel Esquerdo: Entrada de Texto / Editor */}
        <div className="w-full md:w-1/2 h-full flex flex-col border-r border-line bg-slate-50/30 dark:bg-surface-card/40">
          <div className="p-3 border-b border-line bg-white dark:bg-surface-card flex items-center justify-between text-xs font-semibold text-slate-500">
            <span className="flex items-center gap-1.5">
              <Code2 className="w-4 h-4 text-slate-400" />
              <span>Editor de Código (Markdown + LaTeX)</span>
            </span>
            <span>{getConteudoAtivo().length} caracteres</span>
          </div>

          <textarea
            value={getConteudoAtivo()}
            onChange={(e) => setConteudoAtivo(e.target.value)}
            placeholder="Digite o conteúdo da aula em Markdown e fórmulas em KaTeX..."
            className="flex-1 w-full p-4 font-mono text-xs sm:text-sm leading-relaxed bg-transparent resize-none focus:outline-hidden text-slate-900 dark:text-slate-100"
          />

          {/* Campo de URL de Vídeo no rodapé do editor */}
          <div className="p-3 border-t border-line bg-white dark:bg-surface-card flex items-center gap-2">
            <Video className="w-4 h-4 text-slate-400 flex-shrink-0" />
            <input
              type="text"
              placeholder="URL da Videoaula complementar (ex: YouTube, Vimeo)..."
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              className="flex-1 text-xs px-3 py-1.5 rounded-lg border border-line bg-slate-50 dark:bg-surface-elevated text-slate-900 dark:text-white focus:outline-hidden"
            />
          </div>
        </div>

        {/* Painel Direito: Preview KaTeX em Tempo Real */}
        <div className="w-full md:w-1/2 h-full flex flex-col bg-white dark:bg-surface-card overflow-hidden">
          <div className="p-3 border-b border-line flex items-center justify-between text-xs font-semibold text-slate-500 bg-slate-50/50 dark:bg-surface-elevated/40">
            <span className="flex items-center gap-1.5">
              <Eye className="w-4 h-4 text-subject-500" />
              <span className="font-bold text-slate-800 dark:text-slate-200">
                Visualização do Aluno em Tempo Real
              </span>
            </span>
            <span className="text-[11px] text-slate-400">Renderização KaTeX</span>
          </div>

          <div className="flex-1 p-6 overflow-y-auto">
            {getConteudoAtivo().trim() ? (
              <KaTeXRenderer
                content={getConteudoAtivo()}
                className="text-sm sm:text-base leading-relaxed"
              />
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                Digite ou selecione fórmulas no editor à esquerda para visualizar o resultado aqui.
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
