"""
Schemas Pydantic para o Painel do Professor (Etapa 10).
Conforme especificações e regras de negócio RN-PRF-001 a RN-PRF-020.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DistribuicaoDemograficaItem(BaseModel):
    label: str
    valor: int
    percentual: float


class FaturamentoMensalItem(BaseModel):
    mes: str
    faturamento_bruto: float
    faturamento_liquido: float
    transacoes: int


class TeacherAnalyticsResponse(BaseModel):
    """Métricas agregadas do dashboard docente com zero queries N+1."""
    total_faturado_bruto: float
    total_faturado_liquido: float
    total_alunos: int
    alunos_ativos: int
    theta_medio_global: float
    distribuicao_escola: List[DistribuicaoDemograficaItem]
    distribuicao_uf: List[DistribuicaoDemograficaItem]
    distribuicao_tri: Dict[str, int]
    faturamento_mensal: List[FaturamentoMensalItem]
    metodos_pagamento: Dict[str, int]


class AlunoResumoDTO(BaseModel):
    """Resumo cadastral e pedagógico para a tabela de gestão de alunos."""
    id: UUID
    nome_completo: str
    cpf_mascarado: str
    email: str
    uf: str
    cidade: str
    escola_tipo: str
    serie_ano: str
    eh_menor_idade: bool
    theta_atual: float
    faixa_tri: str
    total_exercicios: int
    status_matricula: str
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class AlunosPaginadosResponse(BaseModel):
    """Resposta paginada da listagem de alunos."""
    total: int
    page: int
    limit: int
    total_paginas: int
    items: List[AlunoResumoDTO]


class TentativaAuditoriaDTO(BaseModel):
    """Trilha de auditoria das submissões de exercícios (RN-PRF-010)."""
    id: UUID
    item_id: UUID
    enunciado_resumo: str
    tipo_resolucao: str
    acertou: bool
    pontuacao: float
    tempo_resposta_segundos: int
    criado_em: datetime


class AlunoDossieDTO(BaseModel):
    """Ficha pedagógica completa individual do estudante (RN-PRF-006 e RN-PRF-007)."""
    id: UUID
    nome_completo: str
    cpf_mascarado: str
    email: str
    idade_anos: int
    eh_menor_idade: bool
    dados_responsavel: Optional[Dict[str, Any]] = None
    uf: str
    cidade: str
    bairro: Optional[str] = None
    escola_tipo: str
    nome_escola: Optional[str] = None
    serie_ano: str
    criado_em: datetime

    # Indicadores TRI e pedagógicos
    theta_atual: float
    erro_padrao: float
    faixa_tri: str
    historico_theta: List[Dict[str, Any]]
    radar_areas: List[Dict[str, Any]]
    horas_liquidas_total: float
    dias_estudo_total: int
    total_exercicios_resolvidos: int
    taxa_acerto_exercicios: float

    # Status comercial
    status_matricula: str
    matricula_expira_em: Optional[datetime] = None

    # Auditoria de atividade
    ultimas_tentativas: List[TentativaAuditoriaDTO]


class CuradoriaCapituloDTO(BaseModel):
    capitulo_id: UUID
    numero_capitulo: int
    titulo: str
    tempo_estimado_min: int
    tem_aula: bool
    publicado: bool
    atualizado_em: Optional[datetime] = None


class CuradoriaVolumeDTO(BaseModel):
    volume_id: UUID
    numero_volume: int
    titulo: str
    grande_area: str
    total_capitulos: int
    capitulos: List[CuradoriaCapituloDTO]


class CuradoriaAulaDetalheDTO(BaseModel):
    capitulo_id: UUID
    capitulo_titulo: str
    numero_capitulo: int
    volume_titulo: str
    numero_volume: int
    bloco1_teoria_katex: str
    bloco2_exemplos_katex: str
    bloco3_dicas_ia: str
    video_url: Optional[str] = None
    publicado: bool
    atualizado_por: Optional[UUID] = None
    atualizado_em: Optional[datetime] = None


class CuradoriaAulaUpdatePayload(BaseModel):
    """Payload para atualização instrucional KaTeX de aulas (RN-PRF-012)."""
    bloco1_teoria_katex: str = Field(..., min_length=10)
    bloco2_exemplos_katex: str = Field(..., min_length=10)
    bloco3_dicas_ia: str = Field(..., min_length=10)
    video_url: Optional[str] = None
    publicado: bool = True


class TransacaoFinanceiraDTO(BaseModel):
    id: UUID
    matricula_id: Optional[UUID] = None
    usuario_id: UUID
    aluno_nome: str
    aluno_email: str
    valor_bruto: float
    taxa_gateway: float
    valor_liquido: float
    status: str
    metodo: str
    gateway_transacao_id: str
    pago_em: Optional[datetime] = None
    criado_em: datetime


class ExtratoFinanceiroResponse(BaseModel):
    saldo_total_bruto: float
    saldo_total_liquido: float
    taxas_totais_asaas: float
    total_transacoes: int
    total_reembolsado: float
    transacoes: List[TransacaoFinanceiraDTO]


class EstornoResponse(BaseModel):
    sucesso: bool
    mensagem: str
    matricula_id: UUID
    transacao_id: Optional[UUID] = None
    novo_status: str
