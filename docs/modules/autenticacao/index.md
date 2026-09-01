---
title: Autenticação
type: module
status: draft
related:
  - modules/autenticacao/flow/index.md
  - modules/autenticacao/business-rules/index.md
  - modules/onboarding/index.md
  - modules/interface/index.md
  - modules/painel-professor/index.md
  - modules/pagamento/index.md
last_updated: "2026-09-01"
updated_by: claude
---

<!-- ai-summary
Módulo Autenticação. Sistema de controle de acesso, identificação e segurança de sessões do Tutor Inteligente.
Login híbrido por E-mail ou CPF + Senha.
2 perfis de usuário: Aluno (`student`) e Professor (`teacher`).
Controle de 1 sessão ativa concorrente por aluno (desconexão automática do dispositivo anterior para evitar rateio de contas pagas).
Recuperação de senha via Link Mágico enviado por e-mail com token temporário de 15 minutos.
Segurança com hash criptográfico seguro (bcrypt/Argon2id), Rate Limiting contra força bruta e JWT com cookies HTTP-Only.
-->

# Autenticação

Documentação do sistema de identificação de usuários, gerenciamento de perfis (`student` e `teacher`), controle de sessões simultâneas e segurança de credenciais do **Tutor Inteligente**.

---

## 1. Pilares de Autenticação e Segurança

O módulo de Autenticação garante acesso ágil e proteção contra compartilhamento indevido de contas:

```mermaid
graph TD
    Auth["🔐 Sistema de Autenticação"]
    
    Auth --> P1["1. Identificação Flexível \n Login por E-mail OU CPF + Senha"]
    Auth --> P2["2. Perfis Binários \n Aluno ('student') e Professor ('teacher')"]
    Auth --> P3["3. Sessão Única Ativa \n 1 Dispositivo Concorrente por Aluno"]
    Auth --> P4["4. Recuperação Ágil \n Link Mágico por E-mail (15 min)"]
```

| Pilar | Descrição | Regra Chave |
|:---|:---|:---|
| **Login por E-mail ou CPF** | Facilidade de entrada para estudantes brasileiros | Validação de formato e máscara automática |
| **Dois Níveis de Acesso** | Separação entre interface de estudo e painel gestor | `student` (Aulas/Exercícios) e `teacher` (Gestão Total) |
| **Sessão Única Concorrente** | Proteção contra rateio de contas pagas | Desconecta automaticamente o aparelho anterior |
| **Link Mágico por E-mail** | Redefinição de senha sem atrito | Token criptografado de uso único válido por 15 min |

---

## 2. Fluxo de Entrada e Roteamento Inteligente

Após autenticar com sucesso, o sistema direciona o usuário conforme seu perfil e status no Onboarding:

```mermaid
flowchart TD
    A["Usuário insere E-mail ou CPF + Senha"] --> B{"Credenciais Válidas?"}
    
    B -->|Não| C["Mensagem de erro amigável + Contador de Rate Limit"]
    B -->|Sim| D{"Qual o Perfil (Role)?"}
    
    D -->|"teacher"| E["Abre diretamente o Painel do Professor"]
    D -->|"student"| F{"Completou o Onboarding?"}
    
    F -->|Não| G["Redireciona para o Wizard do Onboarding (Prova CAT)"]
    F -->|Sim| H["Abre a Skill Tree dos 11 Volumes do Iezzi"]
```

---

## 3. Política de 1 Dispositivo Concorrente

Para proteger o modelo comercial de venda por capítulos e volumes:

```mermaid
sequenceDiagram
    autonumber
    actor Aluno as Aluno (Celular)
    actor Amigo as Dispositivo B (Computador)
    participant Server as Servidor de Autenticação
    participant DB as Tabela de Sessões Ativas
    
    Aluno->>Server: Login no Celular (Sessão A criada)
    Server->>DB: Registra Sessão A como "Ativa"
    Aluno->>Server: Assiste aula de 50 min normalmente
    
    Amigo->>Server: Login no Computador com mesma conta
    Server->>DB: Invalida Sessão A e ativa Sessão B
    Server-->>Amigo: Acesso liberado no Computador
    
    Aluno->>Server: Próxima requisição no Celular
    Server-->>Aluno: Erro 401 ("Conta conectada em outro dispositivo")
```

---

## 4. Recuperação de Senha por Link Mágico

Fluxo sem atrito para redefinição segura de credenciais:

```mermaid
flowchart LR
    A["Esqueci minha senha"] --> B["Informa E-mail ou CPF"]
    B --> C["Disparo de E-mail com Link Mágico"]
    C --> D["Aluno clica no botão do e-mail"]
    D --> E["Validação de Token (15 min)"]
    E --> F["Tela de Cadastro de Nova Senha"]
    F --> G["Senha redefinida com sucesso"]
```

---

## 5. Navegação nas Seções Detalhadas

| Seção | Descrição |
|:---|:---|
| [Fluxo](flow/index.md) | Diagramas de login por CPF/E-mail, roteamento de perfis, sessão única e link mágico |
| [Regras de Negócio](business-rules/index.md) | Especificação das regras RN-AUT-001 a RN-AUT-020 (validação de CPF, roles, tokens e antifraude) |
