"use client";

/**
 * Estado global do wizard de cadastro com auto-save do rascunho no Redis
 * (via backend, TTL 48h) e recuperação automática ao montar a página.
 * Referência: docs-site/docs/implementation/etapa-04-onboarding.md (seção 4.5)
 */
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { api } from "@/lib/api";
import { calcularIdade } from "@/lib/formatters";
import {
  CadastroConcluidoResponse,
  DraftSessionResponse,
  ONBOARDING_FORM_INICIAL,
  OnboardingFormState,
} from "@/types/onboarding";

const DRAFT_STORAGE_KEY = "ti_draft_session_id";
const DEBOUNCE_AUTOSAVE_MS = 1000;

interface OnboardingContextValue {
  form: OnboardingFormState;
  setCampo: <K extends keyof OnboardingFormState>(
    campo: K,
    valor: OnboardingFormState[K]
  ) => void;
  setResponsavel: (dados: Partial<NonNullable<OnboardingFormState["dados_responsavel"]>>) => void;
  calcularIdadeAluno: () => number | null;
  ehMenorIdade: () => boolean;
  carregandoRascunho: boolean;
  salvandoRascunho: boolean;
  rascunhoRecuperado: boolean;
  limparRascunho: () => void;
  finalizarCadastro: () => Promise<CadastroConcluidoResponse>;
}

const OnboardingContext = createContext<OnboardingContextValue | null>(null);

function gerarDraftSessionId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function OnboardingProvider({ children }: { children: React.ReactNode }) {
  const [form, setForm] = useState<OnboardingFormState>(ONBOARDING_FORM_INICIAL);
  const [carregandoRascunho, setCarregandoRascunho] = useState(true);
  const [salvandoRascunho, setSalvandoRascunho] = useState(false);
  const [rascunhoRecuperado, setRascunhoRecuperado] = useState(false);

  const draftSessionIdRef = useRef<string | null>(null);
  const recuperadoRef = useRef(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // 1. Recuperação do rascunho no mount (useEffect vazio)
  useEffect(() => {
    const inicializar = async () => {
      let draftId = localStorage.getItem(DRAFT_STORAGE_KEY);
      if (!draftId) {
        draftId = gerarDraftSessionId();
        localStorage.setItem(DRAFT_STORAGE_KEY, draftId);
      }
      draftSessionIdRef.current = draftId;

      try {
        const resposta = await api.get<DraftSessionResponse>("/api/v1/onboarding/rascunho", {
          headers: { "X-Draft-Session-ID": draftId },
        });
        if (resposta?.dados_parciais && Object.keys(resposta.dados_parciais).length > 0) {
          setForm((anterior) => ({
            ...anterior,
            ...resposta.dados_parciais,
          }));
          setRascunhoRecuperado(true);
        }
      } catch {
        // Rascunho indisponível: segue com formulário em branco
      } finally {
        recuperadoRef.current = true;
        setCarregandoRascunho(false);
      }
    };

    void inicializar();
  }, []);

  // 2. Auto-save com debounce de 1000ms (sem loop infinito: só após recuperação)
  useEffect(() => {
    if (!recuperadoRef.current || !draftSessionIdRef.current) return;
    if (carregandoRascunho) return;

    if (debounceRef.current) clearTimeout(debounceRef.current);

    debounceRef.current = setTimeout(async () => {
      const draftId = draftSessionIdRef.current;
      if (!draftId) return;
      setSalvandoRascunho(true);
      try {
        await api.post(
          "/api/v1/onboarding/salvar-rascunho",
          form,
          { headers: { "X-Draft-Session-ID": draftId } }
        );
      } catch {
        // Auto-save best-effort: falha não interrompe o preenchimento
      } finally {
        setSalvandoRascunho(false);
      }
    }, DEBOUNCE_AUTOSAVE_MS);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [form, carregandoRascunho]);

  const setCampo = useCallback(
    <K extends keyof OnboardingFormState>(campo: K, valor: OnboardingFormState[K]) => {
      setForm((anterior) => ({ ...anterior, [campo]: valor }));
    },
    []
  );

  const setResponsavel = useCallback(
    (dados: Partial<NonNullable<OnboardingFormState["dados_responsavel"]>>) => {
      setForm((anterior) => ({
        ...anterior,
        dados_responsavel: {
          nome_completo: anterior.dados_responsavel?.nome_completo ?? "",
          cpf: anterior.dados_responsavel?.cpf ?? "",
          telefone: anterior.dados_responsavel?.telefone ?? "",
          email: anterior.dados_responsavel?.email ?? "",
          ...dados,
        },
      }));
    },
    []
  );

  const calcularIdadeAluno = useCallback(() => calcularIdade(form.data_nascimento), [form.data_nascimento]);

  const ehMenorIdade = useCallback(() => {
    const idade = calcularIdade(form.data_nascimento);
    return idade !== null && idade < 18;
  }, [form.data_nascimento]);

  const limparRascunho = useCallback(() => {
    localStorage.removeItem(DRAFT_STORAGE_KEY);
    draftSessionIdRef.current = null;
    setForm(ONBOARDING_FORM_INICIAL);
  }, []);

  const finalizarCadastro = useCallback(async () => {
    const draftId = draftSessionIdRef.current;
    const menor = ehMenorIdade();
    const payload = {
      etapa1: {
        nome_completo: form.nome_completo,
        cpf: form.cpf,
        data_nascimento: form.data_nascimento,
        genero: form.genero,
        foto_perfil: form.foto_perfil,
      },
      etapa2: {
        email: form.email,
        senha: form.senha,
        confirmacao_senha: form.confirmacao_senha,
        telefone: form.telefone,
        dados_responsavel:
          menor && form.dados_responsavel
            ? {
                nome_completo: form.dados_responsavel.nome_completo,
                cpf: form.dados_responsavel.cpf,
                telefone: form.dados_responsavel.telefone,
                email: form.dados_responsavel.email?.trim() ? form.dados_responsavel.email.trim() : undefined,
              }
            : undefined,
      },
      etapa3: {
        cep: form.cep,
        uf: form.uf,
        cidade: form.cidade,
        bairro: form.bairro || undefined,
        logradouro: form.logradouro || undefined,
        numero: form.numero || undefined,
        escola_tipo: form.escola_tipo,
        nome_escola: form.nome_escola || undefined,
        serie_ano: form.serie_ano,
      },
    };

    const resposta = await api.post<CadastroConcluidoResponse>(
      "/api/v1/onboarding/finalizar-cadastro",
      payload,
      draftId ? { headers: { "X-Draft-Session-ID": draftId } } : undefined
    );
    // Cadastro concluído: rascunho não é mais necessário
    localStorage.removeItem(DRAFT_STORAGE_KEY);
    draftSessionIdRef.current = null;
    return resposta;
  }, [form, ehMenorIdade]);

  const value = useMemo<OnboardingContextValue>(
    () => ({
      form,
      setCampo,
      setResponsavel,
      calcularIdadeAluno,
      ehMenorIdade,
      carregandoRascunho,
      salvandoRascunho,
      rascunhoRecuperado,
      limparRascunho,
      finalizarCadastro,
    }),
    [
      form,
      setCampo,
      setResponsavel,
      calcularIdadeAluno,
      ehMenorIdade,
      carregandoRascunho,
      salvandoRascunho,
      rascunhoRecuperado,
      limparRascunho,
      finalizarCadastro,
    ]
  );

  return <OnboardingContext.Provider value={value}>{children}</OnboardingContext.Provider>;
}

export function useOnboarding(): OnboardingContextValue {
  const contexto = useContext(OnboardingContext);
  if (!contexto) {
    throw new Error("useOnboarding deve ser usado dentro de um OnboardingProvider.");
  }
  return contexto;
}
