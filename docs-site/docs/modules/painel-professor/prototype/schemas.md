---
title: Painel do Professor - Schemas e DTOs Docentes
type: module
status: draft
related:
  - modules/painel-professor/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 1. Schemas e DTOs Docentes (Pydantic v2 & TypeScript)

Contratos tipados para o painel analítico do professor, ficha de acompanhamento do estudante, extrato financeiro e curadoria de conteúdos.

---

## 1. Modelos Backend em Python (`app/modules/teacher/schemas.py`)

```python
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# 1. Dashboard de Analytics Executivo
# ============================================================================

class DistribuicaoUfItem(BaseModel):
    uf: str
    total_alunos: int
    percentual: float


class DashboardAnalyticsResponse(BaseModel):
    total_estudantes_ativos: int
    faturamento_bruto_mes_atual: float
    taxa_gateway_mes_atual: float
    faturamento_liquido_mes_atual: float
    theta_medio_geral: float = Field(..., description="Média do nível de proficiência da base")
    horas_estudo_liquidas_total: float
    distribuicao_rede: Dict[str, int] = Field(
        ..., description="Contagem por tipo de escola (publica, privada, outro)"
    )
    distribuicao_uf: List[DistribuicaoUfItem]


# ============================================================================
# 2. Dossiê Individual do Aluno (Somente Leitura)
# ============================================================================

class AlunoFichaResponse(BaseModel):
    usuario_id: UUID
    nome_completo: str
    email: str
    cpf: str
    cidade: str
    uf: str
    escola_tipo: str
    nome_escola: Optional[str]
    serie_ano: str
    eh_menor_idade: bool
    dados_responsavel: Optional[Dict[str, Any]]
    theta_atual: float
    horas_liquidas_estudo: float
    total_capitulos_concluidos: int
    erros_pendentes_caixa_reforco: int
    data_cadastro: datetime


# ============================================================================
# 3. Extrato Financeiro de Vendas
# ============================================================================

class TransacaoExtratoItem(BaseModel):
    id: UUID
    aluno_nome: str
    tipo_produto: str
    metodo: str
    valor_bruto: float
    taxa_gateway: float
    valor_liquido: float
    status_transacao: str
    pago_em: Optional[datetime]


class ExtratoFinanceiroResponse(BaseModel):
    total_liquido_acumulado: float
    saldo_disponivel_repasse: float
    transacoes: List[TransacaoExtratoItem]


# ============================================================================
# 4. Curadoria de Conteúdo KaTeX
# ============================================================================

class CuradoriaAulaRequest(BaseModel):
    bloco1_teoria_katex: str = Field(..., min_length=20)
    bloco2_exemplos_katex: str = Field(..., min_length=20)
    bloco3_dicas_ia: str = Field(..., min_length=10)
    video_url: Optional[str] = None
```

---

## 2. Tipos Equivalentes em TypeScript (`frontend/src/types/teacher.ts`)

```typescript
export interface DistribuicaoUf {
  uf: string;
  total_alunos: number;
  percentual: number;
}

export interface TeacherDashboardAnalytics {
  total_estudantes_ativos: number;
  faturamento_bruto_mes_atual: number;
  taxa_gateway_mes_atual: number;
  faturamento_liquido_mes_atual: number;
  theta_medio_geral: number;
  horas_estudo_liquidas_total: number;
  distribuicao_rede: Record<string, number>;
  distribuicao_uf: DistribuicaoUf[];
}

export interface AlunoFicha {
  usuario_id: string;
  nome_completo: string;
  email: string;
  cpf: string;
  cidade: string;
  uf: string;
  escola_tipo: string;
  nome_escola?: string;
  serie_ano: string;
  eh_menor_idade: boolean;
  dados_responsavel?: {
    nome: string;
    cpf: string;
    telefone: string;
    email: string;
  };
  theta_atual: number;
  horas_liquidas_estudo: number;
  total_capitulos_concluidos: number;
  erros_pendentes_caixa_reforco: number;
  data_cadastro: string;
}

export interface TransacaoExtrato {
  id: string;
  aluno_nome: string;
  tipo_produto: string;
  metodo: "pix" | "credit_card";
  valor_bruto: number;
  taxa_gateway: number;
  valor_liquido: number;
  status_transacao: "paid" | "waiting_payment" | "refunded";
  pago_em?: string;
}
```
