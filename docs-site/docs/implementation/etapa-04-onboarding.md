---
title: "Etapa 4: Onboarding e Cadastro"
type: implementation-guide
status: complete
related: ["etapa-03-autenticacao.md", "etapa-05-conteudo.md", "../modules/onboarding/index.md"]
last_updated: "2026-09-07"
updated_by: antigravity
---
<!-- ai-summary: Guia detalhado de implementação do wizard de cadastro em 3 etapas (Dados Pessoais → Contato/Credenciais → Acadêmico/Endereço), com rascunho no Redis (48h), validação de CPF (Módulo 11), faixa etária (6 a 120 anos), auto-preenchimento ViaCEP, menoridade civil e integração atômica com PostgreSQL no FastAPI. Não inicializa sessão CAT: a prova diagnóstica ocorre no primeiro acesso a uma matéria (Etapa 7). -->

# Etapa 4: Onboarding e Cadastro

Este documento detalha a implementação do fluxo de onboarding para o Tutor Inteligente, focado em conversão e experiência de usuário, mantendo robustez na validação de dados.

**Duração Estimada:** 1-2 semanas
**Pré-requisito:** Etapa 3 concluída (Autenticação funcional)
**Entregável:** Assistente de cadastro (wizard) de 3 etapas funcional com rascunhos no Redis e persistência final no PostgreSQL. [x] Concluído!

> [!NOTE]
> **Status da implementação (2026-09-07):** backend completo (15 testes de integração em `backend/tests/test_onboarding.py`, suíte total 39/39 aprovada no container `ti-backend`), frontend wizard em `(auth)/cadastro` com auto-save, recuperação de rascunho, máscaras, força, requisitos e correspondência de senha em tempo real, botão mostrar/ocultar senha com `autoComplete` semântico, aviso de Caps Lock, validação inline dos dígitos verificadores do CPF e validação de limites de idade (6 a 120 anos), bloco condicional do responsável e auto-fill ViaCEP.

> [!NOTE]
> O onboarding é o primeiro contato real do aluno com a plataforma. A taxa de conversão depende de um fluxo sem fricções. O uso do Redis para salvar rascunhos garante que o usuário possa retomar o cadastro caso a página seja recarregada ou a internet caia.
>
> **Decisão arquitetural (2026-09-07):** o wizard tem **3 etapas** e **não inicializa sessão CAT**. A prova de proficiência é disparada ao entrar numa matéria pela primeira vez (motor CAT da Etapa 7). Nenhuma tabela da Etapa 7 é criada nesta etapa.

> [!IMPORTANT]
> **Fundação já implementada** (migração `f3a9c1d24b57`): as colunas `genero`, `telefone`, `logradouro` e `numero` já existem na tabela `usuarios`, e o validador de CPF já está implementado em `backend/app/core/validators.py` (`CPFValidator`) com testes em `backend/tests/test_validators.py`.

---

## 4.1 Backend: Schemas Pydantic v2 do Onboarding

Precisamos de schemas específicos para validar cada etapa do fluxo separadamente e um schema final para o registro.

Crie o arquivo `backend/app/modules/onboarding/schemas.py` (especificação canônica em `modules/onboarding/prototype/schemas.md`):

```python
from __future__ import annotations
import re
from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class Etapa1Request(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=200)
    cpf: str = Field(..., description="CPF com ou sem pontuação")
    data_nascimento: date
    genero: Literal["masculino", "feminino", "outro", "nao_informar"] = "nao_informar"
    foto_perfil: Optional[str] = None  # URL ou Base64 (máx 5MB), opcional

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        return digitos

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: date) -> date:
        hoje = date.today()
        if v >= hoje:
            raise ValueError("A data de nascimento deve ser uma data no passado.")
        idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
        if idade < 6:
            raise ValueError("O estudante deve ter no mínimo 6 anos de idade.")
        if idade > 120:
            raise ValueError("Data de nascimento inválida. A idade máxima permitida é de 120 anos.")
        return v

    @property
    def idade_anos(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def eh_menor_idade(self) -> bool:
        return self.idade_anos < 18


class DadosResponsavelSchema(BaseModel):
    nome_completo: str = Field(..., min_length=3)
    cpf: str = Field(...)
    telefone: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None  # opcional (RN-ONB-005)

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf_resp(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 11:
            raise ValueError("O CPF do responsável deve conter exatamente 11 dígitos numéricos.")
        return digitos


class Etapa2Request(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=8)
    confirmacao_senha: str
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone/WhatsApp (obrigatório)")
    dados_responsavel: Optional[DadosResponsavelSchema] = None

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        return v.strip().lower()

    @model_validator(mode="after")
    def verificar_senhas_iguais(self):
        if self.senha != self.confirmacao_senha:
            raise ValueError("As senhas não conferem.")
        return self


class Etapa3Request(BaseModel):
    cep: str = Field(..., description="CEP com 8 dígitos numéricos")
    uf: str = Field(..., min_length=2, max_length=2)
    cidade: str
    bairro: Optional[str] = None
    logradouro: Optional[str] = None   # auto-preenchido pelo ViaCEP, editável
    numero: Optional[str] = None
    escola_tipo: Literal["publica", "privada", "outro"]
    nome_escola: Optional[str] = None
    serie_ano: str  # dinâmico: 1_ano, 2_ano, 3_ano, 9_ano, pre_vestibular

    @field_validator("cep")
    @classmethod
    def limpar_cep(cls, v: str) -> str:
        digitos = re.sub(r"\D", "", v)
        if len(digitos) != 8:
            raise ValueError("O CEP deve conter exatamente 8 dígitos numéricos.")
        return digitos


class FinalizarCadastroRequest(BaseModel):
    etapa1: Etapa1Request
    etapa2: Etapa2Request
    etapa3: Etapa3Request

    @model_validator(mode="after")
    def validar_responsavel_se_menor(self):
        if self.etapa1.eh_menor_idade and not self.etapa2.dados_responsavel:
            raise ValueError(
                "Estudantes menores de 18 anos exigem obrigatoriamente os dados do responsável legal na Etapa 2."
            )
        return self


class CadastroConcluidoResponse(BaseModel):
    """O refresh token NUNCA retorna no corpo: é injetado em cookie HTTP-Only (padrão da Etapa 3)."""
    usuario_id: str
    nome_completo: str
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in_seconds: int = 900
    sessao_id: str
    mensagem: str = "Cadastro realizado com sucesso! Redirecionando para o dashboard de matérias."
```

---

## 4.2 Backend: Validador de CPF (Módulo 11) — JÁ IMPLEMENTADO

A validação de CPF confere os dígitos verificadores para evitar CPFs falsos (ex: geradores simples).

**Já implementado** em `backend/app/core/validators.py` (classe `CPFValidator`, com os métodos `validar()` e `normalizar()`), conforme o protótipo `modules/onboarding/prototype/cpf-validator.md`. Os testes unitários estão em `backend/tests/test_validators.py`.

---

## 4.3 Backend: OnboardingService

Serviço responsável pelas regras de negócio de criação do usuário: revalidação de unicidade, cálculo de idade/menoridade e criação da sessão única via `SessionManager` da Etapa 3.

Crie `backend/app/modules/onboarding/onboarding_service.py` (especificação canônica em `modules/onboarding/prototype/onboarding-service.md`). Pontos obrigatórios:

1. **Unicidade revalidada na transação final**: consulta `or_(Usuario.email == email.lower(), Usuario.cpf == cpf)` → `409 Conflict` detalhado (CPF vs E-mail).
2. **Cálculo exato de idade** (considera aniversário ainda não ocorrido no ano corrente) + rejeição de datas futuras.
3. **Menoridade**: sem `dados_responsavel` → `400`; com responsável → persiste JSONB em `usuarios.dados_responsavel`.
4. **Normalizações**: e-mail em minúsculas, UF em maiúsculas.
5. **Sessão única**: `SessionManager.registrar_nova_sessao(...)` do módulo de autenticação; persistir o hash SHA-256 do refresh token em `sessao.refresh_token_hash` (nunca placeholder).
6. **Rascunho**: após o commit, deletar `onboarding_draft:{X-Draft-Session-ID}` do Redis.
7. **Atomicidade**: `db.commit()` único no final; qualquer falha antes disso é coberta pelo rollback da sessão async (`get_db`).

---

## 4.4 Backend: 7 Endpoints do Onboarding

Crie `backend/app/modules/onboarding/router.py` (prefixo `/api/v1/onboarding`) e registre-o em `backend/app/main.py`. Todos os endpoints que manipulam o rascunho devem ler o header `X-Draft-Session-ID`.

> [!IMPORTANT]
> A requisição no ViaCEP (Endpoint 6) deve ter um timeout curto (4s) via `httpx.AsyncClient(timeout=4.0)` para não prender o event loop em caso de instabilidade externa.

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/validar-etapa-1` | `POST` | Valida CPF (Módulo 11) e verifica duplicidade no banco. |
| `/validar-etapa-2` | `POST` | Valida formato/disponibilidade do e-mail e CPF do responsável (se presente). |
| `/validar-etapa-3` | `POST` | Valida preenchimento dos dados escolares e de endereço. |
| `/salvar-rascunho` | `POST` | Guarda payload parcial no Redis (`onboarding_draft:{id}`, TTL 48h). Header `X-Draft-Session-ID`. |
| `/rascunho` | `GET` | Recupera o rascunho baseado no `X-Draft-Session-ID`. |
| `/cep/{cep}` | `GET` | Proxy seguro para o ViaCEP (auto-complete), timeout de 4s; `503` em indisponibilidade para liberar digitação manual. |
| `/finalizar-cadastro` | `POST` | Validações finais, cria usuário + sessão no PG, emite tokens (refresh em cookie HTTP-Only) e limpa o rascunho. |

> [!TIP]
> O módulo de autenticação já expõe as dependências `get_current_user` / `get_current_session` em `backend/app/core/deps.py`. Os endpoints de onboarding são públicos (cadastro), mas esta base já está pronta para as rotas protegidas das etapas seguintes.

---

## 4.5 Frontend: Wizard Multi-Step

O assistente de cadastro guia o usuário em 3 etapas. Rota canônica: `frontend/src/app/(auth)/cadastro/page.tsx` (a rota `(student)/onboarding` fica reservada para a prova diagnóstica CAT, Etapa 7). Utilize Zustand ou Context API para o estado global do formulário, sincronizado com o Redis via backend.

### Estrutura Sugerida de Componentes React

```tsx
// frontend/src/app/(auth)/cadastro/page.tsx
'use client'

import { useState } from 'react';
import { OnboardingProvider } from '@/contexts/OnboardingContext';
import Step1Identity from './_components/Step1Identity';
import Step2Credentials from './_components/Step2Credentials';
import Step3Academic from './_components/Step3Academic';
import ProgressBar from './_components/ProgressBar';

export default function CadastroPage() {
  const [currentStep, setCurrentStep] = useState(1);

  return (
    <OnboardingProvider>
      <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg">
        <h1 className="text-2xl font-bold mb-6">Crie sua Conta no Tutor Inteligente</h1>
        <ProgressBar currentStep={currentStep} totalSteps={3} />

        <div className="mt-8">
          {currentStep === 1 && <Step1Identity onNext={() => setCurrentStep(2)} />}
          {currentStep === 2 && <Step2Credentials onNext={() => setCurrentStep(3)} onBack={() => setCurrentStep(1)} />}
          {currentStep === 3 && <Step3Academic onBack={() => setCurrentStep(2)} onSubmit={submitFinal} />}
        </div>
      </div>
    </OnboardingProvider>
  );
}
```

> [!TIP]
> Use `react-hook-form`, `zod` e `react-imask` para máscaras (CPF: `000.000.000-00`, CEP: `00000-000`, Telefone: `(00) 00000-0000`). Para o auto-save, coloque um `useEffect` na alteração de campos chave com `debounce` de 1000ms.

### Funcionalidades do Frontend:
1. **Auto-save no Redis**: a cada field change (com debounce), chama `/salvar-rascunho` com o header `X-Draft-Session-ID`.
2. **Recuperação de Rascunho**: no mount da página (`useEffect` vazio), busca `/rascunho` usando o ID armazenado no localStorage.
3. **Indicador de Força de Senha**: no Step 2, validar as regras de segurança em tempo real.
4. **Verificação instantânea de correspondência de senha**: no Step 2, o rótulo "Senhas coincidem / Não coincidem" (com borda verde/vermelha no campo) aparece assim que o usuário digita a confirmação — sem esperar o submit.
5. **Botão mostrar/ocultar senha (eye toggle)**: presente em todos os campos de senha do sistema (login, cadastro Step 2 — campos senha e confirmação, e redefinir-senha). Ícones `Eye`/`EyeOff` no lado direito do campo, com `aria-label` e `aria-pressed` para acessibilidade; o botão só é exibido quando o campo tem conteúdo. Complementado por `autoComplete` correto (`new-password` no cadastro/redefinição, `current-password` no login) para integrar com gerenciadores de senha do navegador.
6. **Checklist de requisitos de senha**: exibido em tempo real no Step 2 abaixo do indicador de força (`requisitosSenha()` em `src/lib/formatters.ts`). Apenas "Mínimo 8 caracteres" é obrigatório (regra do backend: `senha.min_length=8`); maiúscula/minúscula, número e símbolo são recomendações que elevam o indicador de força. Itens cumpridos ficam verdes com ícone de check.
7. **Aviso de Caps Lock**: exibido nos campos de senha do login, redefinir-senha e cadastro (Step 2) quando `getModifierState("CapsLock")` detecta a tecla ativa; some ao digitar ou desfocar o campo.
8. **Validação inline de CPF (Step 1)**: ao sair do campo (blur) com 11 dígitos, os dígitos verificadores são conferidos localmente via `validarCPF()` em `src/lib/formatters.ts` (espelho fiel do `CPFValidator` do backend, Módulo 11, incluindo rejeição de sequências repetidas). Feedback visual imediato: borda vermelha + mensagem de erro, ou confirmação verde "CPF válido". A validação definitiva continua no backend via `/validar-etapa-1`.
9. **Auto-fill de CEP**: ao digitar 8 dígitos no Step 3, acionar `/cep/{cep}` e popular `cidade`, `uf`, `bairro` e `logradouro` (campos permanecem editáveis; em falha do ViaCEP, aviso inline libera digitação manual — RN-ONB-006).
10. **Bloco condicional do responsável**: exibido no Step 2 quando a idade calculada no Step 1 for < 18.

---

## 4.6 Testes

Crie os testes em `backend/tests/test_onboarding.py` (o arquivo `backend/tests/test_validators.py` do validador de CPF já existe).

```powershell
# Comando para rodar testes específicos do onboarding
docker exec ti-backend pytest tests/test_onboarding.py -v
```

**Casos a Cobrir:**
- `test_duplicate_cpf_rejection`: cadastro com CPF já salvo acusa erro 409 Conflict.
- `test_duplicate_email_rejection`: cadastro com e-mail já salvo acusa erro 409 Conflict.
- `test_email_normalizado_lowercase`: e-mail maiúsculo no cadastro permite login com minúsculas.
- `test_minor_requires_responsavel`: idade < 18 recusa cadastro sem `dados_responsavel` (400).
- `test_telefone_obrigatorio`: payload sem telefone (ou < 10 dígitos) é rejeitado na Etapa 2.
- `test_complete_registration_flow`: payload final completo cria o usuário no PostgreSQL (incl. `genero`, `telefone`, `logradouro`, `numero`), abre sessão única e retorna JWT + cookie HTTP-Only.
- `test_draft_save_and_recovery`: salva o rascunho, recupera e valida os dados correspondentes; TTL de 48h (`setex` 172800s).
- `test_cep_proxy_timeout`: ViaCEP indisponível → 503 com permissão de digitação manual.
- `test_refresh_token_hash_persistido`: `sessoes_ativas.refresh_token_hash` contém o SHA-256 do cookie emitido.

---

## 4.7 Critérios de Aceitação

Verifique os itens abaixo antes de considerar a Etapa 4 concluída:

- [x] Schemas Pydantic v2 separados em três etapas, validando inputs antes de processar (com `@field_validator` / `@model_validator`).
- [x] `OnboardingService` calcula a idade via `data_nascimento` de forma exata (considerando aniversário do ano corrente e datas futuras rejeitadas).
- [x] Caso o usuário seja menor, o cadastro falha sem informar `dados_responsavel` (422 na validação do schema; 400 como defesa no serviço).
- [x] Campos `genero`, `telefone`, `logradouro` e `numero` persistidos corretamente em `usuarios` (migração `f3a9c1d24b57`).
- [x] E-mail armazenado em minúsculas; UF em maiúsculas.
- [x] O endpoint do ViaCEP tem timeout de 4s e trata falhas graciosamente (permite digitação manual pelo usuário se a API cair).
- [x] Ao salvar rascunhos no Redis, eles expiram sozinhos em 48 horas (TTL 172800s).
- [x] Transação final no banco é atômica (`db.commit()` único); a sessão única é criada via `SessionManager` com o hash SHA-256 real do refresh token.
- [x] O refresh token é entregue exclusivamente em cookie HTTP-Only (nunca no corpo da resposta).
- [x] Nenhuma tabela da Etapa 7 (CAT) é criada ou referenciada nesta etapa.
- [x] O Frontend exibe uma Progress Bar indicativa das 3 etapas, em `(auth)/cadastro`.
- [x] Inputs possuem máscara (CPF, CEP, Telefone) bloqueando letras (`src/lib/formatters.ts`), que também expõe `validarCPF` (Módulo 11, espelho do backend) e `requisitosSenha` (checklist em tempo real).
- [x] Auto-save funcional no frontend (não gera loop infinito de requests; debounce 1000ms só após recuperação do rascunho).
- [x] Mobile responsive: o wizard não quebra em telas de 320px (ex: iPhone SE). (Verificado por revisão de código: layout fluido com `w-full`, paddings responsivos `p-4 sm:p-6`, grids que colapsam para coluna única `grid-cols-1 sm:grid-cols-2`, sem larguras fixas ou overflow horizontal.)
