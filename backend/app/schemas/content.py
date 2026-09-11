"""
Schemas Pydantic v2 para o Módulo de Conteúdo Didático.
Representa disciplinas, volumes do Iezzi, capítulos para Skill Tree e aulas em 4 blocos KaTeX.
"""
from __future__ import annotations
from uuid import UUID
from datetime import datetime, timezone
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# RN-PRG-012: Mapeamento canônico do Heatmap de Domínio (Tabela 15)
# Cinza (<3 itens respondidos) | Vermelho (<50%) | Amarelo (<75%) | Verde (>=75%)
# ============================================================================

HEATMAP_MIN_ITENS = 3
HEATMAP_LIMIAR_VERDE = 75.0
HEATMAP_LIMIAR_AMARELO = 50.0


def calcular_status_heatmap(total_respondidas: int, taxa_acertos: float) -> Literal["cinza", "vermelho", "amarelo", "verde"]:
    """Aplica RN-PRG-012 para derivar a cor canônica do heatmap (Tabela 15)."""
    if total_respondidas < HEATMAP_MIN_ITENS:
        return "cinza"
    if taxa_acertos >= HEATMAP_LIMIAR_VERDE:
        return "verde"
    if taxa_acertos >= HEATMAP_LIMIAR_AMARELO:
        return "amarelo"
    return "vermelho"


# Mapeamento interno (português, canônico no banco) -> exibição (inglês, frontend)
STATUS_COR_PARA_FRONTEND = {
    "cinza": "grey",
    "vermelho": "red",
    "amarelo": "yellow",
    "verde": "green",
}

STATUS_DOMINIO_PARA_FRONTEND = {
    "cinza": "not_started",
    "vermelho": "struggling",
    "amarelo": "in_progress",
    "verde": "mastered",
}


# ============================================================================
# 1. Estrutura Canônica (Disciplinas, Volumes, Capítulos)
# ============================================================================

class DisciplinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    nome: str
    nivel_ensino: str
    icone: str
    cor_tema: str
    ordem: int
    ativo: bool


class VolumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    disciplina_id: UUID
    nome_colecao: str
    numero_volume: int
    titulo: str
    grande_area: str
    ordem_exibicao: int
    preco_padrao: float
    ativo: bool
    total_capitulos: Optional[int] = 0


class CapituloResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    volume_id: UUID
    numero_capitulo: int
    titulo: str
    tempo_estimado_min: int
    preco_avulso: float
    pre_requisitos_ids: Optional[List[UUID]] = []
    ordem: int


class SkillTreeNodeResponse(BaseModel):
    """Nó formatado para a Skill Tree com heatmap de domínio do estudante."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    volume_id: UUID
    numero_capitulo: int
    titulo: str
    tempo_estimado_min: int
    ordem: int
    status_dominio: Literal["mastered", "in_progress", "struggling", "not_started"] = "not_started"
    cor_heatmap: Literal["green", "yellow", "red", "grey"] = "grey"
    percentual_acerto: float = 0.0
    desbloqueado: bool = True
    tem_conteudo: bool = True
    pre_requisito_pendente: bool = False


class VolumeComCapitulosResponse(BaseModel):
    """Volume acompanhado da lista hierárquica de seus capítulos para a Skill Tree."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    numero_volume: int
    titulo: str
    grande_area: str
    ordem_exibicao: int
    capitulos: List[SkillTreeNodeResponse] = []


# ============================================================================
# 2. Aulas em 4 Blocos KaTeX
# ============================================================================

class AulaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    capitulo_id: UUID
    bloco1_teoria_katex: str
    bloco2_exemplos_katex: str
    bloco3_dicas_ia: str
    video_url: Optional[str] = None
    publicado: bool
    atualizado_em: datetime
    # Metadados de navegação da aula
    capitulo_titulo: Optional[str] = None
    numero_capitulo: Optional[int] = None
    volume_id: Optional[UUID] = None
    numero_volume: Optional[int] = None
    volume_titulo: Optional[str] = None


class ConcluirAulaRequest(BaseModel):
    percentual_acertos: float = Field(..., ge=0.0, le=100.0, description="Percentual de acertos na bateria de fixação (Mínimo 60% para concluir)")


class ConcluirAulaResponse(BaseModel):
    sucesso: bool
    concluida: bool
    mensagem: str
    percentual_atingido: float
    proximo_capitulo_id: Optional[UUID] = None


# ============================================================================
# 3. Interações da Aula (Tutor Socrático & Pistas - Placeholders Etapa 5/6)
# ============================================================================

class MensagemChat(BaseModel):
    papel: Literal["user", "assistant", "system"]
    conteudo: str = Field(..., description="Texto da mensagem com fórmulas KaTeX delimitadas por $...$ ou $$...$$")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatAulaRequest(BaseModel):
    capitulo_id: UUID = Field(..., description="ID do capítulo atual")
    mensagem: str = Field(..., min_length=1, max_length=1000, description="Dúvida ou questionamento do estudante")
    trecho_selecionado: Optional[str] = Field(default=None, description="Fórmula ou trecho LaTeX selecionado")
    historico_recente: List[MensagemChat] = Field(default=[], max_length=6)


class ChunkRAGResponse(BaseModel):
    trecho: str
    pagina: Optional[int] = None
    teorema_ou_topico: Optional[str] = None
    score_similaridade: float = 0.0


class ChatAulaResponse(BaseModel):
    resposta_katex: str = Field(..., description="Resposta pedagógica do tutor socrático formatada em KaTeX")
    chunks_utilizados: List[ChunkRAGResponse] = Field(default=[])
    nivel_ajuda_socratico: Literal[1, 2, 3] = Field(default=1, description="1: Pergunta reflexiva | 2: Dica | 3: Explicação")


class SolicitarPistaRequest(BaseModel):
    capitulo_id: UUID
    contexto_exercicio: Optional[str] = None


class SolicitarPistaResponse(BaseModel):
    pista_socratica_katex: str
    dica_pegadinha: Optional[str] = None


# ============================================================================
# 4. Bateria de Fixação Server-Side (anti-trapaça; motor CAT completo na Etapa 7)
# ============================================================================

class QuestaoFixacaoResponse(BaseModel):
    """Questão da bateria de fixação SEM a alternativa correta exposta."""
    model_config = ConfigDict(from_attributes=True)

    numero: int
    enunciado_katex: str
    alternativas: List[str] = Field(..., description="Alternativas em KaTeX, sem indicação da correta")


class BateriaFixacaoResponse(BaseModel):
    """Bateria de fixação do capítulo, servida pelo backend."""
    model_config = ConfigDict(from_attributes=True)

    capitulo_id: UUID
    questoes: List[QuestaoFixacaoResponse]
    percentual_minimo: float = 60.0


class SubmeterFixacaoRequest(BaseModel):
    """Respostas do aluno: { numero_da_questao: indice_da_alternativa }"""
    respostas: Dict[int, int] = Field(..., min_length=1)
    segundos_estudo: int = Field(
        default=0,
        ge=0,
        deprecated=True,
        description="[LEGADO/IGNORADO] Tempo ativo agora é persistido exclusivamente pelo auto-sync do useStudyTimer via POST /api/v1/progresso/tempo-estudo (RN-PRG-003). Mantido apenas para compatibilidade de clientes antigos.",
    )


class SubmeterFixacaoResponse(BaseModel):
    sucesso: bool
    percentual_acertos: float
    percentual_minimo: float = 60.0
    concluida: bool
    mensagem: str
    gabarito: Dict[int, int] = Field(default={}, description="Correção: número da questão -> índice da alternativa correta")
    proximo_capitulo_id: Optional[UUID] = None
