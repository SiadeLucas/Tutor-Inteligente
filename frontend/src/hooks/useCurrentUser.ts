"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { UsuarioAuth, MeResponse } from "@/types/auth";

export function useCurrentUser() {
  const [user, setUser] = useState<UsuarioAuth | null>(() => {
    if (typeof window === "undefined") return null;
    try {
      const cached = sessionStorage.getItem("ti_user");
      return cached ? JSON.parse(cached) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState<boolean>(!user);

  useEffect(() => {
    let alive = true;
    async function fetchUser() {
      try {
        const data = await api.get<MeResponse>("/api/v1/auth/me");
        if (alive) {
          setUser(data);
          try {
            sessionStorage.setItem("ti_user", JSON.stringify(data));
          } catch {
            // sessionStorage desabilitado ou cheio
          }
        }
      } catch {
        // Usuário não autenticado ou offline
      } finally {
        if (alive) setLoading(false);
      }
    }
    fetchUser();
    return () => {
      alive = false;
    };
  }, []);

  return { user, loading };
}
