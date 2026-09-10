"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { api, getAccessToken } from "@/lib/api";

interface UseStudyTimerOptions {
  inactivityTimeoutSeconds?: number;
  autoSyncIntervalSeconds?: number;
  enableAutoSync?: boolean;
}

interface UseStudyTimerReturn {
  seconds: number;
  minutes: number;
  formattedTime: string;
  isActive: boolean;
  pause: () => void;
  resume: () => void;
  reset: () => void;
  flushSync: () => Promise<void>;
}

/**
 * Hook para cronometrar o tempo líquido de estudo ativo (RN-PRG-003).
 * Pausa automaticamente após 3 minutos (180 segundos) cravados de ausência de interação
 * (mouse, teclado, scroll) ou ao ocultar a aba.
 * Sincroniza periodicamente com o endpoint POST /api/v1/progresso/tempo-estudo.
 */
export function useStudyTimer(
  optionsOrTimeout: UseStudyTimerOptions | number = {}
): UseStudyTimerReturn {
  const options =
    typeof optionsOrTimeout === "number"
      ? { inactivityTimeoutSeconds: optionsOrTimeout }
      : optionsOrTimeout;

  const {
    inactivityTimeoutSeconds = 180, // RN-PRG-003: 3 minutos cravados
    autoSyncIntervalSeconds = 30,   // Sincronização periódica a cada 30s (mesma cadência do heartbeat)
    enableAutoSync = true,
  } = options;

  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(true);
  const lastActivityRef = useRef<number>(Date.now());
  const unsyncedSecondsRef = useRef<number>(0);
  const isSyncingRef = useRef<boolean>(false);

  // Sincronizar lote de segundos não persistidos com a API.
  // RN-PRG-003 (arquitetura Etapa 8): este hook é o ÚNICO escritor do tempo
  // líquido ativo em horas_estudo_diarias.segundos_ativos, via UPSERT em
  // POST /api/v1/progresso/tempo-estudo. Nenhum outro endpoint grava tempo.
  const flushSync = useCallback(async () => {
    const toSync = unsyncedSecondsRef.current;
    if (toSync <= 0 || !enableAutoSync || isSyncingRef.current) return;

    const token = getAccessToken();
    if (!token) return;

    isSyncingRef.current = true;
    try {
      // keepalive garante que o lote final sobreviva ao fechamento/descarregamento da aba
      await api.post(
        "/api/v1/progresso/tempo-estudo",
        { segundos_ativos: toSync },
        { keepalive: true }
      );
      unsyncedSecondsRef.current = Math.max(0, unsyncedSecondsRef.current - toSync);
    } catch {
      // Mantém no buffer se houver falha de rede temporária
    } finally {
      isSyncingRef.current = false;
    }
  }, [enableAutoSync]);

  // Monitorar interações do usuário (teclado, mouse, scroll)
  useEffect(() => {
    const handleUserActivity = () => {
      lastActivityRef.current = Date.now();
      if (!isActive) {
        setIsActive(true);
      }
    };

    const handleVisibilityChange = () => {
      if (document.hidden) {
        setIsActive(false);
        flushSync();
      } else {
        lastActivityRef.current = Date.now();
        setIsActive(true);
      }
    };

    const handlePageUnload = () => {
      // Última chance de persistir o lote pendente antes de a aba morrer
      flushSync();
    };

    window.addEventListener("mousemove", handleUserActivity, { passive: true });
    window.addEventListener("keydown", handleUserActivity, { passive: true });
    window.addEventListener("scroll", handleUserActivity, { passive: true });
    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("pagehide", handlePageUnload);
    window.addEventListener("beforeunload", handlePageUnload);

    return () => {
      window.removeEventListener("mousemove", handleUserActivity);
      window.removeEventListener("keydown", handleUserActivity);
      window.removeEventListener("scroll", handleUserActivity);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("pagehide", handlePageUnload);
      window.removeEventListener("beforeunload", handlePageUnload);
      flushSync();
    };
  }, [isActive, flushSync]);

  // Intervalo de contagem de 1 segundo
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isActive) {
      interval = setInterval(() => {
        const secondsSinceActivity = (Date.now() - lastActivityRef.current) / 1000;
        if (secondsSinceActivity >= inactivityTimeoutSeconds) {
          setIsActive(false);
        } else {
          setSeconds((prev) => prev + 1);
          unsyncedSecondsRef.current += 1;

          // Se atingiu o intervalo de sincronização (ex: 60s), envia
          if (unsyncedSecondsRef.current >= autoSyncIntervalSeconds) {
            flushSync();
          }
        }
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, inactivityTimeoutSeconds, autoSyncIntervalSeconds, flushSync]);

  const pause = useCallback(() => {
    setIsActive(false);
    flushSync();
  }, [flushSync]);

  const resume = useCallback(() => {
    lastActivityRef.current = Date.now();
    setIsActive(true);
  }, []);

  // reset() zera apenas o CRONÔMETRO exibido (sessão local). O buffer de segundos
  // não sincronizados NÃO é descartado: ele continua drenando para o servidor nos
  // próximos ciclos de auto-sync, evitando perda de tempo ativo já estudado.
  const reset = useCallback(() => {
    setSeconds(0);
  }, []);

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  const formattedTime = `${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`;

  return {
    seconds,
    minutes,
    formattedTime,
    isActive,
    pause,
    resume,
    reset,
    flushSync,
  };
}
