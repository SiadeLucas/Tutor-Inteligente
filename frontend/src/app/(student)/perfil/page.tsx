"use client";

/**
 * /perfil — Perfil e Configurações (RN-INT §2.6 — Fase "Caderno de Foco").
 *
 * Layout flat com hairlines (sem card-in-card): seções separadas por
 * divisórias de 1px, hierarquia puramente tipográfica e uma única
 * superfície de leitura por seção.
 *
 * Seções:
 * - Identidade: avatar de iniciais (ou foto), nome, membro desde.
 * - Acesso: e-mail/CPF (somente leitura — integridade de recuperação de
 *   conta), telefone editável (PATCH /auth/me).
 * - Contexto acadêmico: escola/série (somente leitura, RN-ONB).
 * - Responsável legal: exibido apenas para menores (RN-ONB-005).
 * - Aparência: dark mode persistido (localStorage, RN-INT-005) + dark
 *   neutro (superfícies não herdam a cor da matéria).
 * - Segurança: alterar senha (PATCH /auth/me/senha), desconectar
 *   dispositivos (POST /auth/logout-remoto, RN-AUT-015).
 * - Diagnóstico: refazer prova CAT (POST /exercicios/cat/iniciar).
 */

import React from "react";
import { useRouter } from "next/navigation";
import {
  User, Lock, MonitorSmartphone, ClipboardList, Sun, Moon, Loader2,
  Check, AlertCircle, ShieldCheck, School, AtSign, Phone,
  ChevronRight, Eye, EyeOff, Users, LogOut,
} from "lucide-react";
import { api, extrairMensagemErro, clearAuth } from "@/lib/api";
import { MeResponse } from "@/types/auth";
import { useDisciplineTheme } from "@/components/theme/DisciplineThemeProvider";

/* ------------------------------------------------------------------ */
/* Helpers de formatação                                               */
/* ------------------------------------------------------------------ */

function formatarCpf(cpf: string): string {
  const d = cpf.replace(/\D/g, "").padStart(11, "?");
  return d.length === 11
    ? `${d.slice(0, 3)}.***.***-${d.slice(9)}`
    : "•••.•••.•••-••";
}

function formatarTelefone(t: string): string {
  const d = t.replace(/\D/g, "");
  if (d.length === 11) return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
  if (d.length === 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return t || "—";
}

function formatarData(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString("pt-BR", {
      day: "2-digit", month: "long", year: "numeric",
    });
  } catch {
    return iso;
  }
}

const ESCOLA_TIPO_LABEL: Record<string, string> = {
  publica: "Escola pública",
  privada: "Escola privada",
};

function slugId(titulo: string): string {
  return `perfil-${titulo
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")}`;
}

/* ------------------------------------------------------------------ */
/* Primitivas de layout (flat, hairline)                               */
/* ------------------------------------------------------------------ */

function Section({
  icon: Icon,
  title,
  description,
  children,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description?: string;
  children: React.ReactNode;
}) {
  const id = slugId(title);
  return (
    <section aria-labelledby={id} className="py-6 first:pt-2 sm:py-8">
      <div className="flex items-start gap-3">
        <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-subject-wash text-subject-600 dark:text-subject-400">
          <Icon className="h-[18px] w-[18px]" aria-hidden="true" />
        </div>
        <div className="min-w-0">
          <h2 id={id} className="text-base font-semibold tracking-tight text-ink-text">
            {title}
          </h2>
          {description && (
            <p className="mt-0.5 text-sm leading-relaxed text-ink-muted">{description}</p>
          )}
        </div>
      </div>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function FieldRow({
  label,
  value,
  mono = false,
  hint,
}: {
  label: string;
  value: React.ReactNode;
  mono?: boolean;
  hint?: string;
}) {
  return (
    <div className="flex flex-col gap-1 py-2.5 sm:flex-row sm:items-baseline sm:justify-between sm:gap-6">
      <span className="shrink-0 text-sm text-ink-muted sm:w-44">{label}</span>
      <span
        className={`text-sm font-medium text-ink-text sm:text-right ${mono ? "font-mono tracking-tight" : ""}`}
        title={hint}
      >
        {value}
      </span>
    </div>
  );
}

const inputBase =
  "w-full rounded-lg border border-line-border bg-surface-card px-3 py-2.5 text-sm text-ink-text placeholder:text-ink-faint focus:border-subject-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-subject-500/30";

function Button({
  variant = "primary",
  className = "",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "ghost" | "danger" }) {
  const styles = {
    primary:
      "bg-subject-500 text-white hover:bg-subject-600 focus-visible:ring-subject-500/40",
    ghost:
      "border border-line-strong bg-surface-card text-ink-text hover:bg-surface-elevated focus-visible:ring-subject-500/30",
    danger:
      "border border-rose-200 bg-rose-50 text-rose-700 hover:bg-rose-100 focus-visible:ring-rose-400/40 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300 dark:hover:bg-rose-950/70",
  }[variant];
  return (
    <button
      {...props}
      className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:cursor-not-allowed disabled:opacity-60 ${styles} ${className}`}
    />
  );
}

function Feedback({ kind, children }: { kind: "ok" | "error"; children: React.ReactNode }) {
  const styles = {
    ok: "border-emerald-200 bg-emerald-50 text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300",
    error: "border-rose-200 bg-rose-50 text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300",
  }[kind];
  const IconCmp = kind === "ok" ? Check : AlertCircle;
  return (
    <p
      role={kind === "error" ? "alert" : "status"}
      className={`flex items-start gap-2 rounded-lg border px-3 py-2.5 text-sm ${styles}`}
    >
      <IconCmp className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
      <span>{children}</span>
    </p>
  );
}

/* ------------------------------------------------------------------ */
/* Seções interativas                                                  */
/* ------------------------------------------------------------------ */

function TelefoneSection({
  perfil,
  onSaved,
}: {
  perfil: MeResponse;
  onSaved: (p: MeResponse) => void;
}) {
  const [valor, setValor] = React.useState(perfil.telefone || "");
  const [editando, setEditando] = React.useState(false);
  const [salvando, setSalvando] = React.useState(false);
  const [erro, setErro] = React.useState<string | null>(null);
  const [ok, setOk] = React.useState(false);

  React.useEffect(() => setValor(perfil.telefone || ""), [perfil.telefone]);

  const digitos = valor.replace(/\D/g, "");
  const valido = digitos.length === 10 || digitos.length === 11;

  async function salvar() {
    setErro(null);
    setOk(false);
    setSalvando(true);
    try {
      const atualizado = await api.patch<MeResponse>("/api/v1/auth/me", {
        telefone: digitos,
      });
      onSaved(atualizado);
      setOk(true);
      setEditando(false);
    } catch (err) {
      setErro(extrairMensagemErro(err, "Não foi possível salvar o telefone."));
    } finally {
      setSalvando(false);
    }
  }

  return (
    <>
      {!editando ? (
        <div className="flex items-center justify-between gap-4">
          <FieldRow label="Telefone" value={formatarTelefone(perfil.telefone)} />
          <button
            onClick={() => { setEditando(true); setOk(false); }}
            className="shrink-0 text-sm font-semibold text-subject-600 hover:underline dark:text-subject-400"
          >
            Editar
          </button>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          <div className="relative">
            <Phone className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" aria-hidden="true" />
            <input
              className={`${inputBase} pl-9`}
              inputMode="tel"
              placeholder="(11) 99999-9999"
              value={valor}
              onChange={(e) => setValor(e.target.value)}
              aria-label="Telefone com DDD"
            />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Button onClick={salvar} disabled={salvando || !valido}>
              {salvando && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
              Salvar telefone
            </Button>
            <Button variant="ghost" onClick={() => { setEditando(false); setValor(perfil.telefone || ""); setErro(null); }}>
              Cancelar
            </Button>
          </div>
          {erro && <Feedback kind="error">{erro}</Feedback>}
        </div>
      )}
      {ok && !editando && <div className="mt-2"><Feedback kind="ok">Telefone atualizado.</Feedback></div>}
    </>
  );
}

function SenhaSection() {
  const [atual, setAtual] = React.useState("");
  const [nova, setNova] = React.useState("");
  const [conf, setConf] = React.useState("");
  const [mostrar, setMostrar] = React.useState(false);
  const [salvando, setSalvando] = React.useState(false);
  const [erro, setErro] = React.useState<string | null>(null);
  const [ok, setOk] = React.useState(false);

  const senhasConferem = nova.length >= 8 && nova === conf;

  async function salvar() {
    setErro(null);
    setOk(false);
    setSalvando(true);
    try {
      await api.patch("/api/v1/auth/me/senha", {
        senha_atual: atual,
        nova_senha: nova,
        confirmacao_senha: conf,
      });
      setOk(true);
      setAtual(""); setNova(""); setConf("");
    } catch (err) {
      setErro(extrairMensagemErro(err, "Não foi possível alterar a senha."));
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form
      className="flex flex-col gap-3"
      onSubmit={(e) => { e.preventDefault(); if (senhasConferem) void salvar(); }}
    >
      <div className="relative">
        <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" aria-hidden="true" />
        <input
          type={mostrar ? "text" : "password"}
          className={`${inputBase} pl-9 pr-10`}
          placeholder="Senha atual"
          value={atual}
          onChange={(e) => setAtual(e.target.value)}
          autoComplete="current-password"
          aria-label="Senha atual"
          required
        />
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <div className="relative">
          <input
            type={mostrar ? "text" : "password"}
            className={inputBase}
            placeholder="Nova senha (mín. 8 caracteres)"
            value={nova}
            onChange={(e) => setNova(e.target.value)}
            autoComplete="new-password"
            aria-label="Nova senha"
            minLength={8}
            required
          />
        </div>
        <div className="relative">
          <input
            type={mostrar ? "text" : "password"}
            className={inputBase}
            placeholder="Confirmar nova senha"
            value={conf}
            onChange={(e) => setConf(e.target.value)}
            autoComplete="new-password"
            aria-label="Confirmar nova senha"
            minLength={8}
            required
          />
          <button
            type="button"
            onClick={() => setMostrar((m) => !m)}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 rounded p-1 text-ink-faint hover:text-ink-muted"
            aria-label={mostrar ? "Ocultar senhas" : "Mostrar senhas"}
          >
            {mostrar ? <EyeOff className="h-4 w-4" aria-hidden="true" /> : <Eye className="h-4 w-4" aria-hidden="true" />}
          </button>
        </div>
      </div>
      {nova.length > 0 && !senhasConferem && (
        <p className="text-xs text-ink-faint">
          {nova.length < 8 ? "A nova senha precisa de no mínimo 8 caracteres." : "As senhas não coincidem."}
        </p>
      )}
      <div>
        <Button type="submit" disabled={salvando || !senhasConferem || atual.length === 0}>
          {salvando && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
          Alterar senha
        </Button>
      </div>
      {erro && <Feedback kind="error">{erro}</Feedback>}
      {ok && <Feedback kind="ok">Senha alterada. Use a nova senha no próximo login.</Feedback>}
    </form>
  );
}

/* ------------------------------------------------------------------ */
/* Página                                                              */
/* ------------------------------------------------------------------ */

export default function PerfilPage() {
  const router = useRouter();
  const { disciplina, theme: tema, setTheme: aplicarTema } = useDisciplineTheme();
  const [perfil, setPerfil] = React.useState<MeResponse | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [erroCarga, setErroCarga] = React.useState<string | null>(null);
  const [iniciandoCat, setIniciandoCat] = React.useState(false);
  const [erroCat, setErroCat] = React.useState<string | null>(null);
  const [confirmandoRemoto, setConfirmandoRemoto] = React.useState(false);
  const [fazendoRemoto, setFazendoRemoto] = React.useState(false);
  const [erroRemoto, setErroRemoto] = React.useState<string | null>(null);
  const [fazendoLogoutLocal, setFazendoLogoutLocal] = React.useState(false);

  /* ------------------------- carregar perfil ------------------------ */
  const recarregar = React.useCallback(async () => {
    try {
      setLoading(true);
      setErroCarga(null);
      const data = await api.get<MeResponse>("/api/v1/auth/me");
      setPerfil(data);
    } catch (err) {
      setErroCarga(extrairMensagemErro(err, "Não foi possível carregar seu perfil."));
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => { void recarregar(); }, [recarregar]);

  /* ---------------------------- refazer CAT ------------------------- */
  async function refazerCat() {
    setErroCat(null);
    setIniciandoCat(true);
    try {
      const disciplinas = await api.get<Array<{ id: string; slug: string }>>(
        "/api/v1/conteudo/disciplinas"
      );
      const mat = disciplinas.find((d) => d.slug === "matematica") || disciplinas[0];
      if (!mat) throw new Error("Disciplina não localizada.");
      await api.post("/api/v1/exercicios/cat/iniciar", {
        disciplina_id: mat.id,
        tipo_prova: "onboarding_diagnostico",
      });
      router.push("/onboarding/cat");
    } catch (err) {
      setErroCat(extrairMensagemErro(err, "Não foi possível iniciar a prova de proficiência."));
      setIniciandoCat(false);
    }
  }

  /* ------------------------- logout local --------------------------- */
  async function logoutLocal() {
    setFazendoLogoutLocal(true);
    try {
      await api.post("/api/v1/auth/logout");
    } catch {
      // Ignora erro de rede para assegurar limpeza local
    } finally {
      clearAuth();
      router.push("/login");
    }
  }

  /* ------------------------ logout remoto --------------------------- */
  async function logoutRemoto() {
    setErroRemoto(null);
    setFazendoRemoto(true);
    try {
      await api.post("/api/v1/auth/logout-remoto");
    } catch (err) {
      console.warn("Aviso no logout remoto:", err);
    } finally {
      clearAuth();
      router.push("/login");
    }
  }

  /* --------------------------- estados ------------------------------ */
  if (loading) {
    return (
      <main className="mx-auto w-full max-w-3xl px-4 pb-safe-bottom sm:px-6">
        <div className="pt-8">
          <div className="h-4 w-24 animate-pulse rounded bg-surface-elevated" />
          <div className="mt-3 h-8 w-48 animate-pulse rounded bg-surface-elevated" />
          <div className="mt-8 divide-y divide-line-border">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="flex items-center gap-3 py-6">
                <div className="h-9 w-9 animate-pulse rounded-lg bg-surface-elevated" />
                <div className="flex-1 space-y-2">
                  <div className="h-4 w-36 animate-pulse rounded bg-surface-elevated" />
                  <div className="h-3 w-56 animate-pulse rounded bg-surface-elevated" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    );
  }

  if (erroCarga || !perfil) {
    return (
      <main className="mx-auto w-full max-w-3xl px-4 pb-safe-bottom sm:px-6">
        <div className="flex flex-col items-start gap-4 py-16">
          <AlertCircle className="h-8 w-8 text-rose-500" aria-hidden="true" />
          <div>
            <h1 className="text-lg font-semibold text-ink-text">Perfil indisponível</h1>
            <p className="mt-1 text-sm text-ink-muted">{erroCarga || "Tente novamente."}</p>
          </div>
          <Button variant="ghost" onClick={() => void recarregar()}>Tentar novamente</Button>
        </div>
      </main>
    );
  }

  const iniciais = perfil.nome_completo
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase() ?? "")
    .join("");

  const temaOptions: Array<{ valor: "light" | "dark" | "system"; label: string; icon: React.ComponentType<{ className?: string }> }> = [
    { valor: "light", label: "Claro", icon: Sun },
    { valor: "dark", label: "Escuro", icon: Moon },
    { valor: "system", label: "Sistema", icon: MonitorSmartphone },
  ];

  return (
    <main className="mx-auto w-full max-w-3xl px-4 pb-safe-bottom sm:px-6">
      {/* Cabeçalho tipográfico flat */}
      <header className="pt-8 sm:pt-10">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-subject-600 dark:text-subject-400">
          {disciplina?.nome ?? "Minha conta"}
        </p>
        <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink-text sm:text-3xl">Perfil</h1>
      </header>

      {/* Identidade */}
      <div className="mt-6 flex items-center gap-4">
        {perfil.avatar_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={perfil.avatar_url}
            alt={`Foto de ${perfil.nome_completo}`}
            className="h-16 w-16 rounded-full object-cover"
          />
        ) : (
          <div
            aria-hidden="true"
            className="flex h-16 w-16 items-center justify-center rounded-full bg-subject-wash-strong text-lg font-bold text-subject-700 dark:text-subject-300"
          >
            {iniciais || <User className="h-6 w-6" />}
          </div>
        )}
        <div className="min-w-0">
          <p className="truncate text-lg font-semibold text-ink-text">{perfil.nome_completo}</p>
          <p className="text-sm text-ink-muted">Membro desde {formatarData(perfil.criado_em)}</p>
        </div>
      </div>

      <div className="mt-2 divide-y divide-line-border">
        {/* -------------------------- Acesso -------------------------- */}
        <Section icon={AtSign} title="Acesso" description="Seus dados de login e contato.">
          <div className="divide-y divide-line-border/60">
            <FieldRow label="E-mail" value={perfil.email} />
            <FieldRow label="CPF" value={formatarCpf(perfil.cpf)} mono hint="Somente leitura — usado para recuperação de conta." />
            <TelefoneSection perfil={perfil} onSaved={setPerfil} />
          </div>
        </Section>

        {/* --------------------- Contexto acadêmico ------------------- */}
        <Section icon={School} title="Contexto acadêmico" description="Definido no cadastro; alterações passam pela secretaria acadêmica.">
          <div className="divide-y divide-line-border/60">
            <FieldRow label="Série / ano" value={perfil.serie_ano} />
            <FieldRow label="Escola" value={perfil.nome_escola || ESCOLA_TIPO_LABEL[perfil.escola_tipo] || perfil.escola_tipo} />
            <FieldRow label="Cidade" value={`${perfil.cidade} — ${perfil.uf}`} />
          </div>
        </Section>

        {/* --------------------- Responsável (menor) ------------------ */}
        {perfil.eh_menor_idade && perfil.dados_responsavel && (
          <Section icon={Users} title="Responsável legal" description="Informações do responsável pelo seu cadastro.">
            <div className="divide-y divide-line-border/60">
              {perfil.dados_responsavel.nome && <FieldRow label="Nome" value={perfil.dados_responsavel.nome} />}
              {perfil.dados_responsavel.cpf && <FieldRow label="CPF" value={formatarCpf(perfil.dados_responsavel.cpf)} mono />}
              {perfil.dados_responsavel.telefone && <FieldRow label="Telefone" value={formatarTelefone(perfil.dados_responsavel.telefone)} />}
              {perfil.dados_responsavel.email && <FieldRow label="E-mail" value={perfil.dados_responsavel.email} />}
            </div>
          </Section>
        )}

        {/* ------------------------- Aparência ------------------------ */}
        <Section icon={Sun} title="Aparência" description="O modo escuro usa superfícies neutras — a cor da matéria fica só nos destaques.">
          <div role="radiogroup" aria-label="Tema da interface" className="grid grid-cols-3 gap-2 sm:max-w-sm">
            {temaOptions.map(({ valor, label, icon: IconCmp }) => (
              <button
                key={valor}
                role="radio"
                aria-checked={tema === valor}
                onClick={() => aplicarTema(valor)}
                className={`flex min-h-11 flex-col items-center justify-center gap-1 rounded-lg border px-2 py-2.5 text-xs font-medium transition-colors ${
                  tema === valor
                    ? "border-subject-500 bg-subject-wash text-subject-700 dark:text-subject-300"
                    : "border-line-border bg-surface-card text-ink-muted hover:bg-surface-elevated"
                }`}
              >
                <IconCmp className="h-4 w-4" aria-hidden="true" />
                {label}
              </button>
            ))}
          </div>
        </Section>

        {/* ------------------------ Diagnóstico ----------------------- */}
        <Section icon={ClipboardList} title="Prova de proficiência" description="Refazer o CAT recalibra o plano de estudos com base no seu nível atual.">
          <Button variant="ghost" onClick={() => void refazerCat()} disabled={iniciandoCat}>
            {iniciandoCat ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <ClipboardList className="h-4 w-4" aria-hidden="true" />}
            Refazer prova adaptativa
            <ChevronRight className="h-4 w-4" aria-hidden="true" />
          </Button>
          {erroCat && <div className="mt-3"><Feedback kind="error">{erroCat}</Feedback></div>}
        </Section>

        {/* -------------------------- Segurança ----------------------- */}
        <Section icon={Lock} title="Segurança">
          <SenhaSection />
          <div className="mt-6 border-t border-dashed border-line-border pt-5 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-ink-text">Sair deste dispositivo</p>
                <p className="text-xs text-ink-muted">Encerra a sua sessão ativa apenas neste navegador.</p>
              </div>
              <Button variant="ghost" onClick={() => void logoutLocal()} disabled={fazendoLogoutLocal}>
                {fazendoLogoutLocal ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <LogOut className="h-4 w-4" aria-hidden="true" />}
                Sair da conta
              </Button>
            </div>

            <div className="border-t border-dashed border-line-border pt-5">
              <div className="mb-3">
                <p className="text-sm font-medium text-ink-text">Desconexão global</p>
                <p className="text-xs text-ink-muted">Encerra todas as sessões ativas em todos os dispositivos.</p>
              </div>
              {!confirmandoRemoto ? (
                <Button variant="danger" onClick={() => setConfirmandoRemoto(true)}>
                  <MonitorSmartphone className="h-4 w-4" aria-hidden="true" />
                  Desconectar todos os dispositivos
                </Button>
              ) : (
                <div className="rounded-lg border border-rose-200 bg-rose-50 p-4 dark:border-rose-900 dark:bg-rose-950/40">
                  <p className="text-sm font-medium text-rose-800 dark:text-rose-200">
                    Desconectar em todos os dispositivos?
                  </p>
                  <p className="mt-1 text-sm text-rose-700 dark:text-rose-300">
                    Todas as sessões ativas — inclusive esta — serão encerradas (RN-AUT-015).
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <Button variant="danger" onClick={() => void logoutRemoto()} disabled={fazendoRemoto}>
                      {fazendoRemoto && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
                      Confirmar desconexão
                    </Button>
                    <button
                      onClick={() => setConfirmandoRemoto(false)}
                      className="min-h-11 rounded-lg px-4 py-2.5 text-sm font-semibold text-ink-muted hover:text-ink-text"
                    >
                      Cancelar
                    </button>
                  </div>
                </div>
              )}
              {erroRemoto && <div className="mt-3"><Feedback kind="error">{erroRemoto}</Feedback></div>}
            </div>
          </div>
        </Section>

        {/* Rodapé de conformidade */}
        <div className="py-6 text-xs leading-relaxed text-ink-faint">
          <p className="flex items-center gap-1.5">
            <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
            E-mail e CPF são fixos para proteger a recuperação da sua conta.
          </p>
        </div>
      </div>
    </main>
  );
}
