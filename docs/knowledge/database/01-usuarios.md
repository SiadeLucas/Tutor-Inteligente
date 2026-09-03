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
    uf CHAR(2) NOT NULL,                           -- Estado da federação (ex: 'SP', 'RJ')
    cidade VARCHAR(100) NOT NULL,
    cep VARCHAR(8) NOT NULL,                       -- 8 dígitos numéricos
    escola_tipo VARCHAR(50) NOT NULL,              -- 'publica' | 'privada' | 'outro'
    nome_escola VARCHAR(200),
    serie_ano VARCHAR(50) NOT NULL,                -- '1_ano', '2_ano', '3_ano', 'outro'
    role VARCHAR(20) NOT NULL DEFAULT 'student',   -- 'student' | 'teacher'
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices para otimização de login e buscas rápidas
CREATE INDEX idx_usuarios_cpf ON usuarios(cpf);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_role ON usuarios(role);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador primário universal único | Gerado via `gen_random_uuid()` |
| `cpf` | VARCHAR(11) | Não | CPF do titular (apenas números) | RN-ONB-001 / RN-AUT-001 (Unique) |
| `email` | VARCHAR(255) | Não | E-mail corporativo ou pessoal | RN-ONB-002 / RN-AUT-002 (Unique) |
| `senha_hash` | VARCHAR(255) | Não | Hash criptográfico da senha | Mínimo 8 caracteres no cadastro |
| `idade_anos` | INT | Não | Idade do estudante em anos completos | Calculado via data_nascimento |
| `eh_menor_idade` | BOOLEAN | Não | Flag indicativa de menoridade (< 18) | RN-ONB-004 |
| `dados_responsavel` | JSONB | Sim | `{"nome": "...", "cpf": "...", "telefone": "...", "email": "..."}` | Obrigatório se `eh_menor_idade = true` |
| `serie_ano` | VARCHAR(50) | Não | Série cadastrada no Onboarding | RN-ONB-009 |
| `role` | VARCHAR(20) | Não | Perfil de permissão (`student` ou `teacher`) | RN-AUT-005 |
