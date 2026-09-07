---
title: Tabela 01 - usuarios
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/autenticacao/business-rules/regras-credenciais.md
last_updated: "2026-09-03"
updated_by: claude
---

# Tabela 01: `usuarios`

Armazena as informações cadastrais e de autenticação de todos os estudantes e professores da plataforma, contemplando validações de idade e menoridade civil.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cpf VARCHAR(11) UNIQUE NOT NULL,               -- 11 dígitos normalizados (apenas números)
    email VARCHAR(255) UNIQUE NOT NULL,            -- Normalizado em minúsculas
    senha_hash VARCHAR(255) NOT NULL,              -- Hash seguro via Argon2id ou bcrypt
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    idade_anos INT NOT NULL,                       -- Calculado no onboarding
    eh_menor_idade BOOLEAN NOT NULL DEFAULT FALSE, -- True se idade_anos < 18
    dados_responsavel JSONB,                       -- Obrigatório se eh_menor_idade = true
    uf VARCHAR(2) NOT NULL,                        -- Estado da federação (ex: 'SP', 'RJ')
    cidade VARCHAR(100) NOT NULL,
    bairro VARCHAR(100),
    cep VARCHAR(8) NOT NULL,                       -- 8 dígitos numéricos
    escola_tipo VARCHAR(50) NOT NULL,              -- 'publica' | 'privada' | 'outro'
    nome_escola VARCHAR(200),
    serie_ano VARCHAR(50) NOT NULL,                -- Validação dinâmica pela disciplina
    role VARCHAR(20) NOT NULL DEFAULT 'student',   -- 'student' | 'teacher'
    avatar_url TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices para otimização de login e buscas rápidas
CREATE INDEX idx_usuarios_cpf ON usuarios(cpf);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_role ON usuarios(role);
CREATE INDEX idx_usuarios_uf_cidade ON usuarios(uf, cidade);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário universal único | Gerado via `gen_random_uuid()` |
| `cpf` | VARCHAR(11) | Não | CPF do titular (apenas números) | RN-ONB-002 / RN-AUT-002 / RN-AUT-003 (Unique) |
| `email` | VARCHAR(255) | Não | E-mail corporativo ou pessoal | RN-ONB-003 / RN-AUT-003 (Unique) |
| `senha_hash` | VARCHAR(255) | Não | Hash criptográfico da senha (Argon2id) | RN-AUT-005 (Mínimo 8 caracteres) |
| `nome_completo` | VARCHAR(255) | Não | Nome civil completo do estudante ou professor | RN-ONB-001 |
| `data_nascimento` | DATE | Não | Data de nascimento para cômputo da idade | RN-ONB-004 |
| `idade_anos` | INT | Não | Idade do estudante em anos completos | Calculado via `data_nascimento` |
| `eh_menor_idade` | BOOLEAN | Não | Flag indicativa de menoridade civil (< 18 anos) | RN-ONB-005 |
| `dados_responsavel` | JSONB | Sim | `{"nome": "...", "cpf": "...", "telefone": "...", "email": "..."}` | Obrigatório se `eh_menor_idade = true` (RN-ONB-005) |
| `uf` | VARCHAR(2) | Não | Unidade federativa do estudante | RN-ONB-006 |
| `cidade` | VARCHAR(100) | Não | Município de residência | RN-ONB-006 |
| `bairro` | VARCHAR(100) | Sim | Bairro de residência | RN-ONB-006 |
| `cep` | VARCHAR(8) | Não | Código de Endereçamento Postal (8 dígitos) | RN-ONB-006 |
| `escola_tipo` | VARCHAR(50) | Não | Categoria da instituição (`publica` ou `privada`) | RN-ONB-008 |
| `nome_escola` | VARCHAR(200) | Sim | Nome da escola ou instituição de ensino | RN-ONB-008 |
| `serie_ano` | VARCHAR(50) | Não | Série cadastrada com validação dinâmica | RN-ONB-009 |
| `role` | VARCHAR(20) | Não | Perfil de permissão (`student` ou `teacher`) | RN-AUT-006 / RN-AUT-007 |
| `avatar_url` | TEXT | Sim | URL ou identificador de avatar no S3 | RN-ONB-007 |
| `ativo` | BOOLEAN | Não | Status de conta ativa | RN-AUT-008 |
| `criado_em` | TIMESTAMPTZ | Não | Data e hora de criação da conta | Auditoria |
| `atualizado_em` | TIMESTAMPTZ | Não | Data e hora da última modificação cadastral | Auditoria |

---

## 3. Arquitetura de Sessões e Presença (Redis + PostgreSQL)

Para suportar milhares de alunos simultâneos sem saturação de I/O por updates contínuos de heartbeat (30s):
- **Camada Volátil (Redis)**: O heartbeat periódico de 30 segundos e a checagem de 1 dispositivo concorrente são gerenciados em chaves Redis com TTL de 45 segundos (`session:{usuario_id}:active`).
- **Camada de Persistência (PostgreSQL)**: A tabela `sessoes_ativas` registra a abertura, encerramento formal ou revogação forçada da sessão para auditoria de segurança.
