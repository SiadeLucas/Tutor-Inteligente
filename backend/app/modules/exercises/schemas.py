"""
Schemas Pydantic v2 para o Módulo de Exercícios e Motor CAT.
Conforme especificação em docs-site/docs/modules/exercicios/prototype/schemas.md.
"""
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


# ============================================================================
# 1. Componentes de Questão e Alternativas
# ============================================================================

class AlternativaItem(BaseModel):
    letra: Literal["A", "B", "C", "D", "E"] = Field(..., description="Identificador da alternativa")
    texto_katex: str = Field(..., description="Texto da alternativa com fórmulas KaTeX delimitadas por $...$")
    correta: Optional[bool] = Field(None, description="Flag indicando se é o gabarito (oculto no envio normal ao aluno)")


class ItemExercicioResponse(BaseModel):
    id: UUID
    capitulo_id: UUID
    tipo_origem: Literal["iezzi_original", "gemea_ia"] = "iezzi_original"
    tipo_item: Literal["multiple_choice", "numeric_input"] = "multiple_choice"
    item_matriz_id: Optional[UUID] = None
    enunciado_katex: str = Field(..., description="Enunciado completo formatado em Markdown + KaTeX")
    alternativas: Optional[List[AlternativaItem]] = None
    parametro_a: float = Field(1.0, description="Discriminação da TRI (típico: 0.5 a 2.5)")
    parametro_b: float = Field(0.0, description="Dificuldade da TRI (escala -3.0 a +3.0)")
    parametro_c: float = Field(0.2, description="Acerto casual (0.2 para 5 alternativas)")
    validado_sympy: bool = True
    criado_em: Optional[datetime] = None

    model_config = {"from_attributes": True}



# ============================================================================
# 2. Submissão com Lógica de 2ª Chance e Ponderação
# ============================================================================

class SubmissaoExercicioRequest(BaseModel):
    item_id: UUID
    capitulo_id: UUID
    tentativa_numero: Literal[1, 2] = Field(
        1,
        description="Hint informativo do cliente. O número REAL da tentativa é contado no servidor (RN-EXE-008) e define a pontuação (1.0 / 0.5 / 0.0).",
    )
    tipo_item: Literal["multiple_choice", "numeric_input"] = Field("multiple_choice", description="Tipo do item submetido")
    resposta_enviada: str = Field(..., description="Letra da alternativa ('A'..'E') ou expressão numérica/algébrica")
    tempo_resposta_segundos: int = Field(..., ge=1, description="Tempo cronometrado em segundos para resolução")


class SubmissaoExercicioResponse(BaseModel):
    acertou: bool
    pontuacao_obtida: float = Field(
        ...,
        description="1.0 para acerto na 1ª tentativa; 0.5 para acerto na 2ª; 0.0 para erro",
    )
    permite_segunda_chance: bool = Field(
        False,
        description="True se errou na 1ª tentativa e tem direito a tentar de novo com dica",
    )
    pista_socratica_ia: Optional[str] = Field(
        None,
        description="Pista conceitual gradual da IA (fornecida apenas na 2ª chance)",
    )
    resolucao_completa_katex: Optional[str] = Field(
        None,
        description="Resolução passo a passo (fornecida após acerto ou erro duplo)",
    )
    pode_gerar_gemea: bool = Field(
        False,
        description="True se ocorreu erro duplo e o aluno pode acionar uma Questão Gêmea",
    )
    resposta_correta: Optional[str] = Field(
        None,
        description="Letra ou gabarito revelado em caso de término (acerto ou erro duplo)",
    )


# ============================================================================
# 3. Sessão da Prova Adaptativa (CAT)
# ============================================================================

class IniciarCatRequest(BaseModel):
    disciplina_id: UUID
    tipo_prova: Literal["onboarding_diagnostico", "marco_periodico"] = "onboarding_diagnostico"


class IniciarCatResponse(BaseModel):
    sessao_cat_id: UUID
    indicador_progresso: str
    total_itens_estimado: str = "12 a 20 questões"
    primeiro_item: ItemExercicioResponse


class SubmeterCatRequest(BaseModel):
    sessao_cat_id: UUID
    item_id: UUID
    resposta_enviada: str
    tempo_resposta_segundos: int = Field(..., ge=1)


class CatStatusResponse(BaseModel):
    sessao_id: UUID
    finalizado: bool = False
    indicador_progresso: str
    proximo_item: Optional[ItemExercicioResponse] = None
    theta_final: Optional[float] = None
    erro_padrao: Optional[float] = None
    classificacao: Optional[str] = None
    total_questoes_respondidas: Optional[int] = None
    scores_grandes_areas: Optional[Dict[str, float]] = None
    redirecionar_url: Optional[str] = None
    mensagem: Optional[str] = None


# ============================================================================
# 4. Caixa de Reforço
# ============================================================================

class ItemCaixaReforcoResponse(BaseModel):
    id: UUID
    item_id: UUID
    capitulo_id: UUID
    enunciado_katex: str
    total_erros: int
    status: str
    arquivado_em: datetime
    superado_em: Optional[datetime] = None

    model_config = {"from_attributes": True}

