"""
Schemas e DTOs tipados do Módulo de Progresso & Analytics (Pydantic v2).
Em conformidade com docs-site/docs/modules/progresso/prototype/schemas.md.
"""
from __future__ import annotations
from uuid import UUID
from datetime import datetime, date
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# 1. Indicadores Gerais, Radar e Linha do Tempo
# ============================================================================

class RadarAreaItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    area: str = Field(..., description="Nome da macro-área (ex: Álgebra e Funções)")
    slug_area: str = Field(..., description="Slug canônico (ex: algebra_funcoes)")
    score_entrada_cat: float = Field(..., description="Nível inicial diagnosticado no Onboarding (-3.0 a +3.0)")
    score_atual: float = Field(..., description="Proficiência atual calibrada em tempo real (-3.0 a +3.0)")


class TimelineThetaItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: str = Field(..., description="Data/hora formatada do registro")
    theta_estimado: float = Field(..., description="Valor psicométrico theta")
    origem_ajuste: str = Field(..., description="Origem: onboarding_cat, marco_cat, micro_ajuste_exercicio")


class ProgressoGeralResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_id: UUID
    theta_atual: float = Field(..., description="Proficiência geral contínua TRI (-3.000 a +3.000)")
    erro_padrao_se: float = Field(..., description="Erro padrão de mensuração Bayesiano")
    classificacao_nivel: Literal["Básico", "Intermediário", "Avançado"]
    completude_global_percentual: float = Field(..., description="Capítulos concluídos / Total de capítulos do currículo")
    horas_estudo_liquidas_total: float = Field(..., description="Horas líquidas ativas acumuladas")
    aulas_concluidas_count: int = Field(..., description="Total de capítulos/aulas concluídos com fixação >= 60%")
    streak_dias_consecutivos: int = Field(..., description="Sequência de dias ativos com estudo")
    radar_areas: List[RadarAreaItem]
    timeline: List[TimelineThetaItem] = Field(default_factory=list, description="Série temporal para o gráfico de evolução")


# ============================================================================
# 2. Matriz do Heatmap de Domínio
# ============================================================================

class HeatmapCapituloItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    capitulo_id: UUID
    numero_capitulo: int
    titulo: str
    taxa_acertos_ponderada: float = Field(..., description="0.0 a 100.0%")
    status_cor: Literal["cinza", "vermelho", "amarelo", "verde"]
    total_exercicios_respondidos: int
    aula_concluida: bool = Field(..., description="True se atingiu aproveitamento >= 60% na bateria")


class HeatmapVolumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    volume_id: UUID
    numero_volume: int
    titulo_volume: str
    grande_area: str
    completude_volume_percentual: float
    capitulos: List[HeatmapCapituloItem]


class VolumeResumoItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    volume_id: UUID
    numero_volume: int
    titulo_volume: str
    grande_area: str
    completude_percentual: float
    total_capitulos: int
    capitulos_concluidos: int


# ============================================================================
# 3. Hub de Ação nos Top 3 Gargalos Críticos
# ============================================================================

class TopCriticoItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    capitulo_id: UUID
    titulo_capitulo: str
    numero_volume: int
    titulo_volume: str
    taxa_acerto_ponderada: float
    total_erros_na_caixa_reforco: int
    acao_revisar_teoria_url: str = Field(..., description="Link direto para revisão da aula")
    acao_praticar_reforco_url: str = Field(..., description="Link direto para treino de reforço dinâmico")


class HubAcaoTop3Response(BaseModel):
    top_criticos: List[TopCriticoItem]
    tem_pendencias_criticas: bool


# ============================================================================
# 4. Registro Contínuo de Tempo de Estudo
# ============================================================================

class RegistrarTempoEstudoRequest(BaseModel):
    segundos_ativos: int = Field(..., ge=1, le=86400, description="Tempo líquido ativo em segundos")


class RegistrarTempoEstudoResponse(BaseModel):
    sucesso: bool
    segundos_adicionados: int
    data: str
