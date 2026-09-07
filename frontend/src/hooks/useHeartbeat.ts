"use client";

import { useEffect, useRef } from "react";
import { api, getAccessToken } from "@/lib/api";

interface UseHeartbeatOptions {
  onConcurrentSessionRevoked?: (data: any) => void;
  intervalMs?: number;
}

export function useHeartbeat({
  onConcurrentSessionRevoked,
  intervalMs = 30000,
}: UseHeartbeatOptions = {}) {
  const isRunningRef = useRef(false);

  useEffect(() => {
    // Escuta evento global disparado pelo interceptador de API
    const handleSessionConflict = (e: any) => {
      if (onConcurrentSessionRevoked) {
        onConcurrentSessionRevoked(e.detail);
      }
    };

    window.addEventListener("session_conflict", handleSessionConflict);

    // Dispara pulso de presença periódico
    const interval = setInterval(async () => {
      const token = getAccessToken();
      if (!token || isRunningRef.current) return;

      isRunningRef.current = true;
      try {
        await api.get("/api/v1/auth/heartbeat");
      } catch (err: any) {
        if (err.data?.detail === "CONCURRENT_SESSION_REVOKED") {
          if (onConcurrentSessionRevoked) {
            onConcurrentSessionRevoked(err.data);
          }
        }
      } finally {
        isRunningRef.current = false;
      }
    }, intervalMs);

    return () => {
      clearInterval(interval);
      window.removeEventListener("session_conflict", handleSessionConflict);
    };
  }, [onConcurrentSessionRevoked, intervalMs]);
}
