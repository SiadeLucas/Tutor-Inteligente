---
title: "Etapa 4: Onboarding e Cadastro"
type: implementation-guide
status: planned
related: ["etapa-03-autenticacao.md", "etapa-05-conteudo.md"]
last_updated: "2026-09-06"
---
<!-- ai-summary: Guia detalhado de implementação do fluxo multi-step de onboarding e cadastro de alunos, com salvamento de rascunho via Redis, validação robusta de CPF, preenchimento automático por CEP e integração atômica com PostgreSQL no FastAPI. -->

# Etapa 4: Onboarding e Cadastro

Este documento detalha a implementação do fluxo de onboarding para o Tutor Inteligente, focado em conversão e experiência de usuário, mantendo robustez na validação de dados.

**Duração Estimada:** 1-2 semanas
**Pré-requisito:** Etapa 3 concluída (Autenticação funcional)
**Entregável:** Assistente de cadastro (wizard) multi-step funcional com rascunhos no Redis e persistência final no PostgreSQL.

> [!NOTE]
> O onboarding é o primeiro contato real do aluno com a plataforma. A taxa de conversão depende de um fluxo sem fricções. O uso do Redis para salvar rascunhos garante que o usuário possa retomar o cadastro caso a página seja recarregada ou a internet caia.

---

## 4.1 Backend: Schemas Pydantic do Onboarding

Precisamos de schemas específicos para validar cada etapa do fluxo separadamente e um schema final para o registro.

Crie o arquivo `backend/app/schemas/onboarding.py`:

```python
from pydantic import BaseModel, EmailStr, constr, validator, Field
from datetime import date
from typing import Optional
from app.utils.validators import validar_cpf

class Etapa1Request(BaseModel):
    cpf: str
    nome_completo: constr(min_length=3, max_length=150)
    data_nascimento: date

    @validator("cpf")
    def valida_formato_e_digito_cpf(cls, v):
        cpf_limpo = ''.join(filter(str.isdigit, v))
        if not validar_cpf(cpf_limpo):
            raise ValueError("CPF inválido")
        return cpf_limpo

class Etapa2Request(BaseModel):
    email: EmailStr
    senha: constr(min_length=8)
    confirmacao_senha: str
    celular: Optional[str] = Field(None, pattern=r"^\d{10,11}$")

    @validator("confirmacao_senha")
    def senhas_iguais(cls, v, values):
        if "senha" in values and v != values["senha"]:
            raise ValueError("As senhas não conferem")
        return v

class Etapa3Request(BaseModel):
    uf: constr(length=2)
    cidade: str
    bairro: str
    cep: str
    escola_tipo: str = Field(..., description="Pública ou Privada")
    nome_escola: Optional[str] = None
    serie_ano: str

class FinalizarCadastroRequest(BaseModel):
    etapa1: Etapa1Request
    etapa2: Etapa2Request
    etapa3: Etapa3Request
    dados_responsavel: Optional[dict] = None

class CadastroConcluidoResponse(BaseModel):
    usuario_id: str
    access_token: str
    refresh_token: str
    mensagem: str = "Cadastro realizado com sucesso"
```

---

## 4.2 Backend: Validador de CPF (Módulo 11)

A validação de CPF deve conferir os dígitos verificadores para evitar CPFs falsos (ex: geradores simples).

Crie `backend/app/utils/validators.py`:

```python
import re

def validar_cpf(cpf: str) -> bool:
    """Valida um CPF completo (algoritmo Módulo 11)"""
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    
    if len(cpf) != 11:
        return False
        
    # Rejeita CPFs conhecidos inválidos (todos os dígitos iguais)
    if cpf in (str(i) * 11 for i in range(10)):
        return False

    # Validação do primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if digito1 != int(cpf[9]):
        return False

    # Validação do segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if digito2 != int(cpf[10]):
        return False

    return True
```

---

## 4.3 Backend: OnboardingService

Serviço responsável por regras de negócio de criação do usuário, incluindo cálculo de idade e gerenciamento de rascunhos no Redis.

Crie `backend/app/services/onboarding_service.py`:

```python
import json
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.usuario import Usuario
from app.core.security import get_password_hash
from app.core.redis import redis_client

class OnboardingService:
    @staticmethod
    def calcular_idade(data_nascimento: date) -> int:
        hoje = date.today()
        return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

    @staticmethod
    async def salvar_rascunho(session_id: str, dados: dict):
        # 48h TTL = 172800 segundos
        await redis_client.setex(f"onboarding_draft:{session_id}", 172800, json.dumps(dados))

    @staticmethod
    async def obter_rascunho(session_id: str) -> dict:
        dados = await redis_client.get(f"onboarding_draft:{session_id}")
        return json.loads(dados) if dados else {}

    @staticmethod
    async def finalizar_cadastro(db: AsyncSession, dados: FinalizarCadastroRequest) -> Usuario:
        # Verifica se CPF ou Email já existem (revisão de segurança na transação atômica)
        # Calcula idade
        idade = OnboardingService.calcular_idade(dados.etapa1.data_nascimento)
        eh_menor = idade < 18

        if eh_menor and not dados.dados_responsavel:
            raise HTTPException(status_code=400, detail="Dados do responsável são obrigatórios para menores de idade")

        # Criação Atômica
        novo_usuario = Usuario(
            cpf=dados.etapa1.cpf,
            nome_completo=dados.etapa1.nome_completo,
            data_nascimento=dados.etapa1.data_nascimento,
            email=dados.etapa2.email,
            senha_hash=get_password_hash(dados.etapa2.senha),
            celular=dados.etapa2.celular,
            cep=dados.etapa3.cep,
            # (outros campos mapeados...)
            eh_menor_idade=eh_menor
        )

        db.add(novo_usuario)
        await db.commit()
        await db.refresh(novo_usuario)
        
        return novo_usuario
```

---

## 4.4 Backend: 7 Endpoints do Onboarding

Adicione as rotas em `backend/app/api/v1/onboarding.py`. Todos os endpoints que manipulam o rascunho devem ler/receber o header `X-Draft-Session-ID`.

> [!IMPORTANT]
> A requisição no ViaCEP (Endpoint 6) deve ter um timeout curto (4s) para não prender a thread em caso de instabilidade externa.

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/validar-etapa-1` | `POST` | Valida formatação do CPF, Módulo 11 e verifica se já existe no banco. |
| `/validar-etapa-2` | `POST` | Valida formato de email e verifica duplicidade. |
| `/validar-etapa-3` | `POST` | Valida preenchimento dos dados escolares. |
| `/salvar-rascunho` | `POST` | Recebe payload parcial e guarda no Redis (48h TTL). Usa header `X-Draft-Session-ID`. |
| `/rascunho` | `GET` | Recupera rascunho baseado no `X-Draft-Session-ID`. |
| `/cep/{cep}` | `GET` | Faz proxy seguro pro ViaCEP para auto-complete, com timeout de 4s (Httpx). |
| `/finalizar-cadastro` | `POST` | Junta dados, aplica regras de menor de idade, cria no PG e emite tokens. |

---

## 4.5 Frontend: Wizard Multi-Step

O assistente de cadastro deve guiar o usuário em 3 etapas claras. Utilizaremos Zustand ou ContextAPI para guardar o estado global do formulário e sincronizar com o Redis.

### Estrutura Sugerida de Componentes React

```tsx
// frontend/src/app/(auth)/onboarding/page.tsx
'use client'

import { useState, useEffect } from 'react';
import { OnboardingProvider } from '@/contexts/OnboardingContext';
import Step1Identity from './_components/Step1Identity';
import Step2Credentials from './_components/Step2Credentials';
import Step3Academic from './_components/Step3Academic';
import ProgressBar from './_components/ProgressBar';

export default function OnboardingPage() {
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
> Use as bibliotecas `react-hook-form`, `zod` e `react-input-mask` (ou `react-imask`) para máscaras (CPF: `000.000.000-00`, CEP: `00000-000`). Para o auto-save, coloque um `useEffect` na alteração de campos chave, implementando `debounce` de 1000ms.

### Funcionalidades do Frontend:
1. **Auto-save no Redis**: A cada field change (com debounce), chama `/salvar-rascunho`.
2. **Recuperação de Rascunho**: No montante inicial da página (`useEffect` vazio), tenta buscar o `/rascunho` no backend usando o ID armazenado no localStorage ou Cookies.
3. **Indicador de Força de Senha**: No Step 2, ao digitar, validar regras de segurança em tempo real.
4. **Auto-fill de CEP**: Ao digitar 8 dígitos no Step 3, acionar `/cep/{cep}` e popular `cidade`, `uf` e `bairro`.

---

## 4.6 Testes

É essencial cobrir os fluxos lógicos no pytest. Crie os testes em `backend/tests/api/test_onboarding.py` e `backend/tests/utils/test_validators.py`.

```powershell
# Comando para rodar testes específicos do onboarding
pytest tests/api/test_onboarding.py -v
```

**Casos a Cobrir:**
- `test_cpf_validation`: CPF válido retorna True, inválido retorna False, CPF com dígitos iguais (ex `111.111.111-11`) retorna False.
- `test_duplicate_cpf_rejection`: Cadastro com CPF já salvo acusa erro 409 Conflict.
- `test_duplicate_email_rejection`: Cadastro com email já salvo acusa erro 409 Conflict.
- `test_minor_requires_responsavel`: Se calcular a idade < 18, recusa caso o bloco `dados_responsavel` esteja nulo.
- `test_complete_registration_flow`: Envia payload final completo, verifica se o usuário foi criado no PostgreSQL e JWT emitido.
- `test_draft_save_and_recovery`: Salva o rascunho, recupera e valida os dados correspondentes.

---

## 4.7 Critérios de Aceitação

Verifique os itens abaixo antes de considerar a Etapa 4 concluída:

- [ ] `Validador de CPF` com Módulo 11 funcionando corretamente no backend.
- [ ] Schema de Pydantic separado em três etapas e validando inputs antes de processar.
- [ ] O `OnboardingService` calcula a idade via `data_nascimento` de forma exata (considerando anos bissextos).
- [ ] Caso o usuário seja menor, o cadastro falha sem informar `dados_responsavel`.
- [ ] O endpoint do ViaCEP tem timeout configurado e trata falhas graciosamente (permite digitação manual pelo usuário se a API cair).
- [ ] Ao salvar rascunhos no Redis, eles expiram sozinhos em exatos 48 horas (TTL).
- [ ] Transação final no banco é atômica (`db.commit()`), se houver erro ao salvar o perfil de estudante vinculado, faz *rollback* de tudo.
- [ ] O Frontend exibe uma Progress Bar indicativa clara das 3 etapas.
- [ ] Inputs possuem máscara (CPF, CEP, Celular) bloqueando letras.
- [ ] Auto-save funcional no frontend (não gera loop infinito de requests).
- [ ] Mobile responsive: o wizard não quebra em telas de 320px (ex: iPhone SE).
