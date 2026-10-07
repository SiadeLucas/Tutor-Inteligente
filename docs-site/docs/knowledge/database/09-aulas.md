---
title: Tabela 09 - aulas
type: knowledge
status: complete
related:
  - knowledge/database/index.md
  - modules/conteudo/business-rules/pedagogia-aulas.md
last_updated: "2026-10-07"
updated_by: antigravity
---

<!-- ai-summary
Tabela 09: aulas. Material instrucional em 4 blocos pedagógicos estruturados com fórmulas KaTeX,
suporte a videoaulas complementares sob demanda (video_url) e metadados de curadoria docente.
-->

# Tabela 09: `aulas`

Armazena o material instrucional formal da aula de 50 minutos, organizado rigorosamente nos **4 blocos pedagógicos estruturados com fórmulas matemáticas em KaTeX**, além de suporte a videoaulas complementares.

---

## 1. DDL SQL (PostgreSQL 16)

```sql
CREATE TABLE aulas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    capitulo_id UUID UNIQUE NOT NULL REFERENCES capitulos(id) ON DELETE CASCADE,
    bloco1_teoria_katex TEXT NOT NULL,             -- Conceito e Teoremas em KaTeX (10 min)
    bloco2_exemplos_katex TEXT NOT NULL,           -- Exemplos Resolvidos Passo a Passo (15 min)
    bloco3_dicas_ia TEXT NOT NULL,                 -- Dicas do Tutor Socrático e Pegadinhas (10 min)
    video_url TEXT,                                -- URL complementar no YouTube/Vimeo/S3 (opcional)
    publicado BOOLEAN NOT NULL DEFAULT TRUE,
    atualizado_por UUID REFERENCES usuarios(id),   -- ID do professor curador
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 2. Dicionário de Colunas

| Coluna | Tipo | Nulo | Descrição | Regras de Negócio |
|:---|:---|:---:|:---|:---|
| `id` | UUID | Não | Identificador da aula | UUID v4 |
| `capitulo_id` | UUID | Não | Chave estrangeira 1:1 para `capitulos(id)` | 1 aula por capítulo |
| `bloco1_teoria_katex` | TEXT | Não | Conceitos fundamentais e demonstrações | KaTeX delimitado por $...$ |
| `bloco2_exemplos_katex` | TEXT | Não | Problemas modelo com resolução formal | 15 minutos de leitura |
| `bloco3_dicas_ia` | TEXT | Não | Pistas conceituais e erros comuns | Curadoria do professor |
| `video_url` | TEXT | Sim | URL complementar da videoaula (YouTube, Vimeo ou direto) | Opcional; reprodução sob demanda (RN-CNT-015) |
| `publicado` | BOOLEAN | Não | Visibilidade para alunos | Controle docente |
| `atualizado_por` | UUID | Sim | ID do professor curador | FK para `usuarios(id)` |
| `atualizado_em` | TIMESTAMPTZ | Não | Data da última curadoria | Auto-update |

