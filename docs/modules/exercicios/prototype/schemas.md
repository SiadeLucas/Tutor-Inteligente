---
title: Exercícios - Schemas e DTOs
type: module
status: draft
related:
  - modules/exercicios/prototype/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 1. Schemas e DTOs (Pydantic v2 & TypeScript)

Especificação dos contratos de dados tipados para tráfego entre o frontend (Next.js) e o backend (FastAPI).

---

## 1. Modelos Backend em Python (`app/modules/exercises/schemas.py`)

```python
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# 1. Componentes de Questão e Alternativas
# ============================================================================

class AlternativaItem(BaseModel):
    letra: Literal["A", "B", "C", "D", "E"] = Field(..., description="Identificador da alternativa")
    texto_katex: str = Field(..., description="Texto da alternativa com fórmulas KaTeX delimitadas por $...$")
    correta: bool = Field(False, description="Flag indicando se é o gabarito (oculto no envio ao aluno)")


class ItemExercicioResponse(BaseModel):
    id: UUID
    capitulo_id: UUID
    tipo_origem: Literal["iezzi_original", "gemea_ia"]
    enunciado_katex: str = Field(..., description="Enunciado completo formatado em Markdown + KaTeX")
    alternativas: List[AlternativaItem]
    parametro_a: float = Field(..., description="Discriminação da TRI (típico: 0.5 a 2.5)")
    parametro_b: float = Field(..., description="Dificuldade da TRI (escala -3.0 a +3.0)")
    parametro_c: float = Field(0.2, description="Acerto casual (0.2 para 5 alternativas)")
    validado_sympy: bool
    criado_em: datetime


# ============================================================================
# 2. Submissão com Lógica de 2ª Chance e Ponderação
# ============================================================================

class SubmissaoExercicioRequest(BaseModel):
    item_id: UUID
    capitulo_id: UUID
    tentativa_numero: Literal[1, 2] = Field(..., description="1 para a primeira tentativa; 2 para a segunda com dica")
    resposta_enviada: Literal["A", "B", "C", "D", "E"]
    tempo_resposta_segundos: int = Field(..., ge=1, description="Tempo cronometrado em segundos para resolução")


class SubmissaoExercicioResponse(BaseModel):
    acertou: bool
    pontuacao_obtida: float = Field(
        ..., 
        description="1.0 para acerto na 1ª tentativa; 0.5 para acerto na 2ª; 0.0 para erro"
    )
    permite_segunda_chance: bool = Field(
        False, 
        description="True se errou na 1ª tentativa e tem direito a tentar de novo com dica"
    )
    pista_socratica_ia: Optional[str] = Field(
        None, 
        description="Pista conceitual gradual da IA (fornecida apenas na 2ª chance)"
    )
    resolucao_completa_katex: Optional[str] = Field(
        None, 
        description="Resolução passo a passo (fornecida após acerto ou erro duplo)"
    )
    pode_gerar_gemea: bool = Field(
        False, 
        description="True se ocorreu erro duplo e o aluno pode acionar uma Questão Gêmea"
    )


# ============================================================================
# 3. Sessão da Prova Adaptativa (CAT)
# ============================================================================

class IniciarCatRequest(BaseModel):
    disciplina_id: UUID
    tipo_prova: Literal["onboarding_diagnostico", "marco_periodico"]


class CatStatusResponse(BaseModel):
    sessao_id: UUID
    item_atual_numero: int
    theta_estimado_atual: float
    erro_padrao_se: float
    proximo_item: Optional[ItemExercicioResponse] = None
    finalizado: bool = False
    scores_grandes_areas: Optional[Dict[str, float]] = None
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/exercise.ts`)

```typescript
export type LetraAlternativa = "A" | "B" | "C" | "D" | "E";

export interface Alternativa {
  letra: LetraAlternativa;
  texto_katex: string;
}

export interface ItemExercicio {
  id: string;
  capitulo_id: string;
  tipo_origem: "iezzi_original" | "gemea_ia";
  enunciado_katex: string;
  alternativas: Alternativa[];
  parametro_a: number;
  parametro_b: number;
  parametro_c: number;
  validado_sympy: boolean;
}

export interface SubmissaoResult {
  acertou: boolean;
  pontuacao_obtida: 1.0 | 0.5 | 0.0;
  permite_segunda_chance: boolean;
  pista_socratica_ia?: string;
  resolucao_completa_katex?: string;
  pode_gerar_gemea: boolean;
}
```
