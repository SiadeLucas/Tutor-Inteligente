---
title: Pagamento
type: module
status: draft
related:
  - modules/pagamento/flow/index.md
  - modules/pagamento/business-rules/index.md
  - modules/onboarding/index.md
  - modules/conteudo/index.md
  - modules/exercicios/index.md
  - modules/painel-professor/index.md
last_updated: "2026-09-01"
updated_by: claude
---

<!-- ai-summary
Módulo Pagamento. Sistema de monetização, precificação escalonada e checkout transparente 100% instantâneo do Tutor Inteligente.
Modelo de 3 níveis de produto:
1. Micro-compra por Capítulo (Sessão de Aprendizagem de 50 minutos: 10 min teoria + 15 min exemplos + 10 min tutor IA + 15 min fixação).
2. Pacote por Volume Completo do Iezzi (Todos os capítulos + Agente de IA especialista do volume).
3. Passe Global / Assinatura Ilimitada (Acesso a todos os 11 volumes, 11 Agentes de IA e testes CAT).
Vigência de 12 meses (ano letivo) para compras avulsas de capítulos e volumes.
Métodos de pagamento 100% instantâneos: PIX Dinâmico (3 a 5 segundos via webhook) e Cartão de Crédito (até 12x).
Integração total com o Painel do Professor: desdobramento de receita por produto, ranking de capítulos mais vendidos, gestão granular de acessos e vigência 100% automatizada.
-->

# Pagamento

Documentação do sistema de monetização, modelo de precificação escalonado por capítulos de 50 minutos, checkout transparente e gestão comercial do **Tutor Inteligente**.

---

## 1. Modelo de Precificação Escalonado

Para alinhar a compra sob demanda dos estudantes com a estrutura modular dos **11 volumes do Iezzi**, a plataforma implementa 3 modalidades de aquisição:

```mermaid
graph TD
    Store["🛒 Loja da Plataforma"]
    
    Store --> T1["1. Capítulo Individual (50 min) \n Micro-compra para prova pontual"]
    Store --> T2["2. Volume Completo do Iezzi \n Desbloqueio do livro + Agente IA"]
    Store --> T3["3. Passe Global Ilimitado \n Assinatura de todos os 11 Volumes"]
    
    T1 --> R1["Acesso a 1 capítulo específico \n 12 meses de vigência"]
    T2 --> R2["Acesso a todos os capítulos do volume \n 12 meses de vigência"]
    T3 --> R3["Acesso total aos 11 volumes e 11 IAs \n Mensal ou Anual"]
```

| Nível de Produto | Proposta de Valor | Formato Pedagógico | Vigência |
|:---|:---|:---|:---|
| **Capítulo Individual** | Reforço cirúrgico para a matéria escolar da semana | 1 sessão completa de 50 minutos | 12 meses (365 dias) |
| **Volume do Iezzi** | Domínio completo de uma disciplina (ex: Trigonometria) | Todos os capítulos + IA especialista | 12 meses (365 dias) |
| **Passe Global** | Preparação integral para o 2º Grau e Vestibulares | 11 volumes + 11 IAs + CATs ilimitados | Mensal / Anual recorrente |

---

## 2. A Sessão de Aprendizagem de 50 Minutos

Cada capítulo avulso adquirido é estruturado pedagogicamente para ser concluído em uma **hora-aula de 50 minutos**:

```mermaid
flowchart LR
    A["10 min: Teoria \n Conceito formal KaTeX"] --> B["15 min: Exemplos \n Demonstração guiada"]
    B --> C["10 min: Tutor IA \n Dicas e diálogo socrático"]
    C --> D["15 min: Fixação \n 3 a 5 exercícios do Iezzi"]
```

---

## 3. Checkout 100% Instantâneo (PIX & Cartão)

A plataforma opera com checkout transparente sem redirecionamentos externos e com liberação imediata:

```mermaid
sequenceDiagram
    autonumber
    actor Aluno
    participant App as Checkout In-App
    participant Gateway as Gateway de Pagamento
    participant Webhook as Webhook de Liberação
    participant DB as Controle de Acesso
    
    Aluno->>App: Seleciona Capítulo (50 min) ou Volume
    Aluno->>App: Escolhe PIX ou Cartão de Crédito
    App->>Gateway: Processa transação transparente
    alt Pagamento PIX
        Gateway-->>App: Retorna QR Code + Chave Copia e Cola
        Aluno->>Gateway: Paga no aplicativo do banco
    else Pagamento Cartão
        Gateway-->>App: Autorização imediata da operadora
    end
    Gateway->>Webhook: Notificação de Pagamento Confirmado (3-5s)
    Webhook->>DB: Registra vigência de 12 meses e libera conteúdo
    DB-->>App: Atualiza tela com status "Liberado" e abre a aula
```

---

## 4. Integração com o Painel do Professor

As decisões comerciais alimentam diretamente as métricas analíticas e pedagógicas do professor:

```mermaid
flowchart TD
    subgraph Receita["Desdobramento Financeiro"]
        R1["Faturamento por Capítulo (Micro)"] --- R2["Faturamento por Volume (Médio)"] --- R3["Receita de Assinaturas (MRR)"]
    end
    
    subgraph Pedagogico["Termômetro de Demanda"]
        P1["Ranking dos Capítulos mais Vendidos \n (Revela as maiores deficiências da turma)"]
    end
    
    subgraph Acessos["Gestão na Ficha do Aluno"]
        A1["Lista de Capítulos/Volumes Ativos"] --- A2["Auditoria de Vigência e Matrículas"]
    end
    
    Receita --> Pedagogico
    Pedagogico --> Acessos
```

---

## 5. Navegação nas Seções Detalhadas

| Seção | Descrição |
|:---|:---|
| [Fluxo](flow/index.md) | Fluxo de checkout, ciclo de webhook PIX/Cartão, desbloqueio de 12 meses e tela docente |
| [Regras de Negócio](business-rules/index.md) | Especificação das regras RN-PAG-001 a RN-PAG-020 (preços, vigência, conciliação e zero cortesias) |
