---
title: Progresso - Schemas e DTOs de Analytics
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs de Analytics (Pydantic v2 & TypeScript)

Contratos tipados para o painel de evolução do estudante, matriz visual do heatmap e recomendações ativas.

---

## 1. Modelos Backend em Python (`app/modules/progress/schemas.py`)

```python
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field


# ============================================================================
# 1. Visão Geral de Progresso e Métricas Tridimensionais
# ============================================================================

class RadarAreaItem(BaseModel):
    area: str = Field(..., description="Nome da macro-área (ex: Álgebra e Funções)")
    score_entrada_cat: float = Field(..., description="Nível inicial diagnosticado no Onboarding (-3.0 a +3.0)")
    score_atual: float = Field(..., description="Proficiência atual calibrada em tempo real (-3.0 a +3.0)")


class ProgressoGeralResponse(BaseModel):
    usuario_id: UUID
    theta_atual: float = Field(..., description="Proficiência geral na escala contínua da TRI (-3.000 a +3.000)")
    erro_padrao_se: float
    classificacao_nivel: Literal["Básico", "Intermediário", "Avançado"]
    completude_global_percentual: float = Field(..., description="Capítulos concluídos / Total de capítulos da matéria")
    horas_estudo_liquidas_total: float = Field(..., description="Horas líquidas acumuladas (excluindo inatividades >3min)")
    streak_dias_consecutivos: int = Field(..., description="Dias consecutivos com estudo ativo")
    radar_areas: List[RadarAreaItem]


# ============================================================================
# 2. Matriz do Heatmap de Domínio dos Volumes
# ============================================================================

class HeatmapCapituloItem(BaseModel):
    capitulo_id: UUID
    numero_capitulo: int
    titulo: str
    taxa_acertos_ponderada: float = Field(..., description="0.0 a 100.0%")
    status_cor: Literal["cinza", "vermelho", "amarelo", "verde"]
    total_exercicios_respondidos: int
    aula_concluida: bool = Field(..., description="True se a aula de 50 min e a bateria de fixação foram entregues")


class HeatmapVolumeResponse(BaseModel):
    volume_id: UUID
    numero_volume: int
    titulo_volume: str
    grande_area: str
    completude_volume_percentual: float
    capitulos: List[HeatmapCapituloItem]


# ============================================================================
# 3. Hub de Ação dos Top 3 Tópicos Críticos
# ============================================================================

class TopCriticoItem(BaseModel):
    capitulo_id: UUID
    titulo_capitulo: str
    numero_volume: int
    titulo_volume: str
    taxa_acerto_ponderada: float
    total_erros_na_caixa_reforco: int
    acao_revisar_teoria_url: str = Field(..., description="Link direto para os Blocos 1 e 2 da aula")
    acao_praticar_reforco_url: str = Field(..., description="Link para iniciar bateria imediata de 5 itens com questões gêmeas")


class HubAcaoTop3Response(BaseModel):
    top_criticos: List[TopCriticoItem]
    tem_pendencias_criticas: bool
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/progress.ts`)

```typescript
export type StatusCorHeatmap = "cinza" | "vermelho" | "amarelo" | "verde";

export interface RadarArea {
  area: string;
  score_entrada_cat: number;
  score_atual: number;
}

export interface ProgressoGeral {
  theta_atual: number;
  erro_padrao_se: number;
  classificacao_nivel: "Básico" | "Intermediário" | "Avançado";
  completude_global_percentual: number;
  horas_estudo_liquidas_total: number;
  streak_dias_consecutivos: number;
  radar_areas: RadarArea[];
}

export interface CapituloHeatmap {
  capitulo_id: string;
  numero_capitulo: number;
  titulo: string;
  taxa_acertos_ponderada: number;
  status_cor: StatusCorHeatmap;
  total_exercicios_respondidos: number;
  aula_concluida: bool;
}

export interface TopCritico {
  capitulo_id: string;
  titulo_capitulo: string;
  numero_volume: number;
  titulo_volume: string;
  taxa_acerto_ponderada: number;
  total_erros_na_caixa_reforco: number;
  acao_revisar_teoria_url: string;
  acao_praticar_reforco_url: string;
}
```
