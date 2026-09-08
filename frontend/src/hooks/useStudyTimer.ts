"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface UseStudyTimerReturn {
  seconds: number;
  minutes: number;
  formattedTime: string;
  isActive: boolean;
  pause: () => void;
  resume: () => void;
  reset: () => void;
}

/**
 * Hook para cronometrar o tempo líquido de estudo ativo em uma aula de 50 min.
 * Pausa automaticamente em caso de inatividade (60s sem interação) ou perda de foco da aba.
 */
export function useStudyTimer(inactivityTimeoutSeconds = 60): UseStudyTimerReturn {
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(true);
  const lastActivityRef = useRef<number>(Date.now());

  const resetActivity = useCallback(() => {
    lastActivityRef.current = Date.now();
    if (!isActive) {
      setIsActive(true);
    }
  }, [isActive]);

  // Monitorar interações do usuário (teclado, mouse, scroll)
  useEffect(() => {
    const handleUserActivity = () => {
      lastActivityRef.current = Date.now();
    };

    const handleVisibilityChange = () => {
      if (document.hidden) {
        setIsActive(false);
      } else {
        lastActivityRef.current = Date.now();
        setIsActive(true);
      }
    };

    window.addEventListener("mousemove", handleUserActivity, { passive: true });
    window.addEventListener("keydown", handleUserActivity, { passive: true });
    window.addEventListener("scroll", handleUserActivity, { passive: true });
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      window.removeEventListener("mousemove", handleUserActivity);
      window.removeEventListener("keydown", handleUserActivity);
      window.removeEventListener("scroll", handleUserActivity);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  // Intervalo de contagem de 1 segundo
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isActive) {
      interval = setInterval(() => {
        const timeSinceActivity = (Date.now() - lastActivityRef.current) / 1000;
        if (timeSinceActivity > inactivityTimeoutSeconds) {
          setIsActive(false);
        } else {
          setSeconds((prev) => prev + 1);
        }
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, inactivityTimeoutSeconds]);

  const pause = useCallback(() => setIsActive(false), []);
  const resume = useCallback(() => {
    lastActivityRef.current = Date.now();
    setIsActive(true);
  }, []);
  const reset = useCallback(() => setSeconds(0), []);

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
  };
}
