/**
 * Cliente HTTP para a API FastAPI com suporte a envio de credenciais (cookies),
 * injeção automática de Bearer token e interceptação para Silent Refresh.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

let currentAccessToken: string | null = null;
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (err: any) => void;
}> = [];

export function setAccessToken(token: string | null) {
  currentAccessToken = token;
  if (typeof window !== "undefined") {
    if (token) {
      sessionStorage.setItem("ti_access_token", token);
    } else {
      sessionStorage.removeItem("ti_access_token");
    }
  }
}

export function clearAuth() {
  setAccessToken(null);
}

export function getAccessToken(): string | null {
  if (currentAccessToken) return currentAccessToken;
  if (typeof window !== "undefined") {
    currentAccessToken = sessionStorage.getItem("ti_access_token");
  }
  return currentAccessToken;
}

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token!);
    }
  });
  failedQueue = [];
};

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, data: any) {
    super(data?.detail || "Erro na requisição.");
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function request<T = any>(
  endpoint: string,
  options: RequestInit = {},
  isRetry = false
): Promise<T> {
  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;
  const token = getAccessToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token && !headers["Authorization"]) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers,
    credentials: "include", // Envia cookies HTTP-Only de Refresh Token
  };

  let response: Response;
  try {
    response = await fetch(url, config);
  } catch (netErr: any) {
    throw new ApiError(0, { detail: "Não foi possível conectar ao servidor." });
  }

  let data: any;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  } else {
    data = await response.text();
  }

  // Tratamento de sessão concorrente revogada
  if (response.status === 401 && data?.detail === "CONCURRENT_SESSION_REVOKED") {
    if (typeof window !== "undefined") {
      window.dispatchEvent(
        new CustomEvent("session_conflict", { detail: data })
      );
    }
    throw new ApiError(response.status, data);
  }

  // Silent Refresh em caso de token de acesso expirado
  if (response.status === 401 && !isRetry && !endpoint.includes("/auth/refresh") && !endpoint.includes("/auth/login")) {
    if (isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      }).then((newToken) => {
        return request<T>(endpoint, options, true);
      });
    }

    isRefreshing = true;

    try {
      const refreshRes = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });

      if (!refreshRes.ok) {
        throw new Error("Sessão expirada");
      }

      const refreshData = await refreshRes.json();
      const newAccessToken = refreshData.access_token;
      setAccessToken(newAccessToken);

      processQueue(null, newAccessToken);
      return request<T>(endpoint, options, true);
    } catch (refreshErr) {
      processQueue(refreshErr, null);
      setAccessToken(null);
      if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
        window.location.href = "/login?sessao_expirada=true";
      }
      throw new ApiError(response.status, data);
    } finally {
      isRefreshing = false;
    }
  }

  if (!response.ok) {
    throw new ApiError(response.status, data);
  }

  return data as T;
}

export const api = {
  get: <T = any>(endpoint: string, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: "GET" }),
  post: <T = any>(endpoint: string, body?: any, options?: RequestInit) =>
    request<T>(endpoint, {
      ...options,
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    }),
  put: <T = any>(endpoint: string, body?: any, options?: RequestInit) =>
    request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    }),
  delete: <T = any>(endpoint: string, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: "DELETE" }),
};

export function extrairMensagemErro(err: any, fallback = "Ocorreu um erro na requisição."): string {
  if (!err) return fallback;
  const detail = err?.data?.detail ?? err?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item: any) => {
        if (typeof item === "string") return item;
        const campo = item.loc ? item.loc.filter((p: any) => p !== "body").join(".") : "";
        const msg = item.msg || item.message || JSON.stringify(item);
        return campo ? `${campo}: ${msg}` : msg;
      })
      .join("; ");
  }
  if (detail && typeof detail === "object") {
    return detail.msg || detail.message || JSON.stringify(detail);
  }
  if (typeof err.message === "string") return err.message;
  return fallback;
}
