"use client";

import React, { useState, useMemo } from "react";
import {
  Play,
  Video,
  ChevronUp,
  ExternalLink,
  Sparkles,
  AlertCircle,
  Tv,
} from "lucide-react";

interface AulaVideoPlayerProps {
  videoUrl?: string | null;
  titulo?: string;
  capituloNumero?: number;
  className?: string;
  defaultWatching?: boolean;
}

type VideoType =
  | { type: "youtube"; embedUrl: string; rawUrl: string }
  | { type: "vimeo"; embedUrl: string; rawUrl: string }
  | { type: "direct"; streamUrl: string; rawUrl: string }
  | { type: "external"; rawUrl: string }
  | null;

/**
 * Normaliza e identifica o tipo e URL de incorporação para reprodução segura.
 */
function parseVideoSource(rawUrl?: string | null): VideoType {
  if (!rawUrl || typeof rawUrl !== "string") return null;
  const trimmed = rawUrl.trim();
  if (!trimmed) return null;

  try {
    // 1. YouTube
    const ytMatch =
      trimmed.match(
        /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/i
      );
    if (ytMatch && ytMatch[1]) {
      const videoId = ytMatch[1];
      // Extrair tempo inicial se existir (ex: t=120s ou t=120 ou start=120)
      let startSeconds = "";
      const timeMatch = trimmed.match(/[?&](?:t|start)=([0-9]+)s?/i);
      if (timeMatch && timeMatch[1]) {
        startSeconds = `&start=${timeMatch[1]}`;
      }

      return {
        type: "youtube",
        embedUrl: `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&enablejsapi=1${startSeconds}`,
        rawUrl: trimmed,
      };
    }

    // 2. Vimeo
    const vimeoMatch = trimmed.match(
      /(?:vimeo\.com\/(?:channels\/(?:\w+\/)?|groups\/[^\/]*\/videos\/|album\/(?:\d+\/)?video\/|video\/|)(\d+))/i
    );
    if (vimeoMatch && vimeoMatch[1]) {
      return {
        type: "vimeo",
        embedUrl: `https://player.vimeo.com/video/${vimeoMatch[1]}?autoplay=1&title=0&byline=0`,
        rawUrl: trimmed,
      };
    }

    // 3. Arquivo de vídeo direto (MP4, WebM, OGG ou S3)
    const directMatch = trimmed.match(/\.(mp4|webm|ogg)(?:[?#].*)?$/i);
    if (directMatch || trimmed.includes("amazonaws.com") || trimmed.includes("cloudfront.net")) {
      return {
        type: "direct",
        streamUrl: trimmed,
        rawUrl: trimmed,
      };
    }

    // 4. URL externa genérica
    if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
      return {
        type: "external",
        rawUrl: trimmed,
      };
    }
  } catch (err) {
    console.error("Erro ao analisar URL de vídeo:", err);
  }

  return null;
}

export function AulaVideoPlayer({
  videoUrl,
  titulo,
  capituloNumero,
  className = "",
  defaultWatching = false,
}: AulaVideoPlayerProps) {
  const [isWatching, setIsWatching] = useState<boolean>(defaultWatching);

  const parsedSource = useMemo(() => parseVideoSource(videoUrl), [videoUrl]);

  if (!parsedSource) {
    return null;
  }

  return (
    <div
      className={`rounded-2xl border border-line overflow-hidden transition-all duration-200 bg-surface-card ${className}`}
    >
      {/* ── MODO 1: Sob Demanda (Capa com Botão para Assistir) ── */}
      {!isWatching ? (
        <div className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gradient-to-r from-subject-wash/80 via-surface-card to-surface-card">
          <div className="flex items-start sm:items-center gap-3.5">
            <div className="w-12 h-12 rounded-xl bg-subject-500 text-white flex items-center justify-center flex-shrink-0 shadow-md shadow-subject-500/20 group">
              <Video className="w-6 h-6" aria-hidden="true" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-subject-100 dark:bg-subject-wash-strong text-subject-700 dark:text-subject-400">
                  <Tv className="w-3 h-3" aria-hidden="true" />
                  Videoaula Explicativa
                </span>
                {capituloNumero && (
                  <span className="text-[11px] font-bold text-ink-muted">
                    Capítulo {capituloNumero}
                  </span>
                )}
              </div>
              <h3 className="font-extrabold text-sm sm:text-base text-ink-text leading-snug">
                {titulo ? `Vídeo: ${titulo}` : "Assista à explicação em vídeo desta aula"}
              </h3>
              <p className="text-xs text-ink-muted mt-0.5">
                Reforce os conceitos matemáticos com a aula audiovisual complementar.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-center">
            {parsedSource.type === "external" ? (
              <a
                href={parsedSource.rawUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs shadow-sm transition-all"
              >
                <ExternalLink className="w-4 h-4" aria-hidden="true" />
                <span>Abrir Vídeo Externo</span>
              </a>
            ) : (
              <button
                type="button"
                onClick={() => setIsWatching(true)}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-extrabold text-xs shadow-md shadow-subject-500/25 active:scale-98 transition-all cursor-pointer"
              >
                <Play className="w-4 h-4 fill-white" aria-hidden="true" />
                <span>Assistir Videoaula</span>
              </button>
            )}
          </div>
        </div>
      ) : (
        /* ── MODO 2: Player Ativo em Reprodução ── */
        <div className="flex flex-col bg-slate-950 text-white">
          {/* Barra de Controles Superior do Player */}
          <div className="px-4 py-2.5 bg-slate-900 border-b border-slate-800 flex items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse flex-shrink-0" />
              <span className="font-bold text-slate-200 truncate">
                {titulo || "Videoaula do Capítulo"}
              </span>
            </div>

            <div className="flex items-center gap-2 flex-shrink-0">
              <a
                href={parsedSource.rawUrl}
                target="_blank"
                rel="noopener noreferrer"
                title="Abrir no site original em nova aba"
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                aria-label="Abrir no site original"
              >
                <ExternalLink className="w-3.5 h-3.5" aria-hidden="true" />
              </a>

              <button
                type="button"
                onClick={() => setIsWatching(false)}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-[11px] font-bold transition-colors cursor-pointer"
                title="Ocultar player e retornar para o modo de leitura de fórmulas"
              >
                <ChevronUp className="w-3.5 h-3.5" aria-hidden="true" />
                <span>Ocultar Vídeo</span>
              </button>
            </div>
          </div>

          {/* Área de Visualização com Aspect Ratio 16:9 */}
          <div className="relative w-full aspect-video bg-black">
            {parsedSource.type === "youtube" && (
              <iframe
                src={parsedSource.embedUrl}
                title={titulo || "Videoaula da disciplina"}
                className="w-full h-full border-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
              />
            )}

            {parsedSource.type === "vimeo" && (
              <iframe
                src={parsedSource.embedUrl}
                title={titulo || "Videoaula da disciplina"}
                className="w-full h-full border-0"
                allow="autoplay; fullscreen; picture-in-picture"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
              />
            )}

            {parsedSource.type === "direct" && (
              <video
                src={parsedSource.streamUrl}
                controls
                autoPlay
                playsInline
                className="w-full h-full object-contain"
              >
                Seu navegador não suporta reprodução de vídeos HTML5.
              </video>
            )}

            {parsedSource.type === "external" && (
              <div className="w-full h-full flex flex-col items-center justify-center p-6 text-center bg-slate-900">
                <AlertCircle className="w-8 h-8 text-amber-400 mb-2" />
                <p className="text-sm text-slate-300 mb-3 max-w-md">
                  Este vídeo está hospedado em uma plataforma externa e não suporta incorporação direta.
                </p>
                <a
                  href={parsedSource.rawUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-subject-500 hover:bg-subject-600 text-white font-bold text-xs transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>Assistir no Provedor Externo</span>
                </a>
              </div>
            )}
          </div>

          {/* Barra de auxílio caso o navegador/adblocker bloqueie embeds */}
          <div className="px-3.5 py-1.5 bg-slate-900/90 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
            <span>Problemas com a exibição?</span>
            <a
              href={parsedSource.rawUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 font-semibold text-subject-400 hover:text-subject-300 hover:underline"
            >
              <span>Abrir no site oficial</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
