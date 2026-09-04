---
title: Onboarding
type: module
status: draft
related:
  - modules/onboarding/flow/index.md
  - modules/onboarding/business-rules/index.md
  - modules/autenticacao/index.md
  - modules/progresso/index.md
  - modules/exercicios/index.md
  - modules/painel-professor/index.md
last_updated: "2026-08-26"
updated_by: claude
---

<!-- ai-summary
Módulo Onboarding. Cadastro do aluno em wizard de 4 etapas: (1) Dados pessoais, (2) Contato, (3) Acadêmico, (4) Prova de proficiência.
Campos: nome completo, data de nascimento, CPF, e-mail, telefone/WhatsApp, gênero, endereço completo (CEP, estado, cidade, bairro), instituição de ensino, série/ano, foto de perfil, dados do responsável (obrigatório se menor de 18).
Prova de proficiência adaptativa (CAT) ao entrar numa matéria pela primeira vez. Pode pular (classificado como Básico). Pode refazer com cooldown de 7 dias.
3 níveis: Básico, Intermediário, Avançado - calculados por área/tópico dentro de cada matéria.
Modelo hierárquico escalável: Nível de Ensino → Matéria → Área/Tópico.
Tipos de questão: multiple_choice, numeric_input, text_input (futuro).
Resultado visual: gráfico radar + resumo textual + botão para trilha personalizada.
Pós-prova: direcionado ao dashboard da matéria com trilha personalizada.
Sem inserção de boletins/notas.
-->

# Onboarding

Primeiro contato do aluno com a plataforma - cadastro em etapas (wizard), prova de proficiência adaptativa e direcionamento para trilha personalizada.

## Visão Geral

O onboarding é um **wizard de 4 etapas** que guia o aluno desde o cadastro até o início dos estudos:

| Etapa | Nome | Descrição |
|---|---|---|
| 1 | Dados Pessoais | Nome, CPF, nascimento, gênero, foto |
| 2 | Contato & Credenciais | E-mail, senha, telefone, endereço e responsável (se menor) |
| 3 | Acadêmico | Instituição de ensino, rede pública/privada, série/ano |
| 4 | Prova de Proficiência | Prova adaptativa (CAT) para classificar o aluno por área |

## Campos de Cadastro

### Dados Pessoais (Etapa 1)

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| Nome completo | texto | ✅ | Identificação civil |
| Data de nascimento | data | ✅ | Usado para calcular idade e acionar responsável na Etapa 2 |
| CPF | texto (validado) | ✅ | Identificação única matemática (11 dígitos numéricos) |
| Gênero | select | ✅ | Métricas demográficas no Painel do Professor |
| Foto de perfil | upload imagem | ❌ | Personalização do perfil |

### Contato, Credenciais e Responsável Legal (Etapa 2)

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| E-mail | e-mail | ✅ | Login único e comunicação oficial |
| Senha | senha (min 8 chars) | ✅ | Hash seguro via Argon2id (RN-AUT-005) |
| Confirmação de senha | senha | ✅ | Deve coincidir com a senha |
| Telefone/WhatsApp | telefone | ✅ | Comunicação e recuperação de conta |
| CEP | texto | ✅ | Auto-preenche UF, cidade, bairro e logradouro |
| Estado (UF) | select | ✅ | Métrica por região |
| Cidade | texto | ✅ | Métrica por região |
| Bairro | texto | ❌ | Endereçamento |
| Logradouro e número | texto | ❌ | Endereçamento completo |

#### Responsável Legal (Etapa 2 - condicional)

> Exibido **obrigatoriamente se o aluno tiver menos de 18 anos** (calculado pela data de nascimento da Etapa 1).

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| Nome do responsável | texto | ✅ (se menor) | Representante civil |
| CPF do responsável | texto (validado) | ✅ (se menor) | Validação matemática de CPF |
| Telefone do responsável | telefone | ✅ (se menor) | Contato para avisos pedagógicos |
| E-mail do responsável | e-mail | ❌ | Comunicação complementar |

### Acadêmico (Etapa 3)

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| Rede de ensino | select (pública/privada) | ✅ | Métrica demográfica institucional |
| Instituição de ensino | texto/autocomplete | ❌ | Nome da escola |
| Série/ano atual | select dinâmico | ✅ | Adaptável para Ensino Médio, Fundamental ou Pré-Vestibular |

## Prova de Proficiência (Etapa 4)

### Modelo: Computerized Adaptive Testing (CAT)

A prova utiliza o modelo **CAT** (teste adaptativo computadorizado cego com prior $\mathcal{N}(0, 1)$):

- Começa com questões de **dificuldade média** ($\theta = 0$)
- Acertou → próxima questão **mais desafiadora**
- Errou → próxima questão **de menor dificuldade**
- Critério de parada híbrido: **12 a 20 questões** com erro padrão $SE(\theta) \le 0.30$
- Revelação diagnóstica integral com Gráfico Radar apenas na conclusão do teste

### Gatilho da Prova

A prova é acionada **ao entrar numa matéria pela primeira vez**:

- No onboarding (como só existe Matemática), o aluno é direcionado automaticamente
- Quando novas matérias forem adicionadas, a prova aparece ao clicar na matéria pela primeira vez
- O aluno **pode pular** → classificado como **Básico** em todas as áreas

### Níveis de Proficiência

| Nível | Código | Descrição |
|---|---|---|
| Básico | `basic` | Pouco ou nenhum domínio da área |
| Intermediário | `intermediate` | Domínio parcial, precisa reforçar |
| Avançado | `advanced` | Bom domínio da área |

O nível é calculado **por área/tópico** dentro de cada matéria:

```
Matemática (Ensino Médio):
├── Álgebra: Avançado
├── Geometria: Básico
├── Trigonometria: Intermediário
└── Estatística: Básico
```

### Tipos de Questão

| Tipo | Código | Uso | Matérias |
|---|---|---|---|
| Múltipla escolha | `multiple_choice` | 4-5 alternativas | Todas |
| Resposta numérica | `numeric_input` | Aluno digita o resultado | Exatas (Matemática, Física...) |
| Resposta textual | `text_input` | Futuro - resposta aberta | Humanas (Português, História...) |

### Política de Refazer

- O aluno **pode refazer** a prova a qualquer momento
- **Cooldown de 7 dias** entre tentativas
- Histórico de todas as tentativas é salvo
- O nível ativo é sempre o da **última tentativa**

### Resultado da Prova

Após completar, o aluno vê:

1. **Gráfico radar** com o nível por área
2. **Resumo textual**: "Você tem domínio forte em Álgebra e pode focar mais em Geometria"
3. **Botão**: "Ir para minha trilha personalizada" → leva ao dashboard da matéria
4. **Opção de refazer** (com cooldown de 7 dias)

## Escalabilidade

### Modelo Hierárquico

O sistema utiliza uma hierarquia genérica de 3 níveis:

```
Nível de Ensino → Matéria → Área/Tópico
```

```mermaid
graph TD
    A["Nível de Ensino"] --> B["Matéria"]
    B --> C["Área/Tópico"]

    A1["Ensino Médio"] --> B1["Matemática"]
    A1 --> B2["Português (futuro)"]
    A1 --> B3["História (futuro)"]

    A2["Ensino Fundamental (futuro)"] --> B4["Matemática"]
    A2 --> B5["Português"]

    B1 --> C1["Álgebra"]
    B1 --> C2["Geometria"]
    B1 --> C3["Trigonometria"]
    B1 --> C4["Estatística"]

    B2 --> C5["Gramática"]
    B2 --> C6["Interpretação"]
```

## Métricas para o Painel do Professor

Os dados coletados no onboarding alimentam as seguintes métricas:

| Métrica | Campos utilizados |
|---|---|
| Desempenho por região | Estado, cidade, bairro |
| Desempenho por faixa etária | Data de nascimento |
| Desempenho por instituição | Instituição de ensino |
| Desempenho por rede | Rede pública/privada |
| Desempenho por série | Série/ano atual |
| Distribuição demográfica | Gênero, idade, região |
| Nível de entrada por área | Resultados da prova de proficiência |

## Seções Detalhadas no Menu

| Seção | Descrição |
|---|---|
| [Fluxo](flow/index.md) | Sub-páginas dedicadas para fluxo geral, wizard, proficiência e fluxos contínuos |
| [Regras de Negócio](business-rules/index.md) | Sub-páginas dedicadas para cadastro/validação, CAT e escalabilidade |
