---
title: Painel do Professor - Agregador de Analytics e Métricas
type: module
status: draft
related:
  - modules/painel-professor/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Agregador de Analytics e Métricas (`teacher_analytics.py`)

Serviço de alta performance em **SQLAlchemy assíncrono** que consolida as métricas executivas, faturamento contábil e demografia estudantil para o professor.

---

## Código Fonte (`backend/app/modules/teacher/analytics_service.py`)

```python
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc

from app.models.user import Usuario
from app.models.payment import TransacaoFinanceira
from app.models.progress import HistoricoTheta, HorasEstudoDiaria, HeatmapDominio
from app.models.exercise import CaixaReforco
from app.modules.teacher.schemas import (
    DashboardAnalyticsResponse,
    DistribuicaoUfItem,
    AlunoFichaResponse,
    ExtratoFinanceiroResponse,
    TransacaoExtratoItem
)


class TeacherAnalyticsService:
    """Consolidador analítico de supervisão passiva para o professor."""

    @staticmethod
    async def obter_dashboard_analytics(db: AsyncSession) -> DashboardAnalyticsResponse:
        """Calcula os indicadores macroeconômicos e pedagógicos da plataforma."""
        # 1. Total de estudantes ativos
        stmt_alunos = select(func.count(Usuario.id)).where(
            and_(Usuario.role == "student", Usuario.ativo == True)
        )
        total_alunos = (await db.execute(stmt_alunos)).scalar() or 0

        # 2. Faturamento do Mês Atual (Bruto, Taxa de Gateway e Líquido)
        primeiro_dia_mes = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        stmt_financeiro = select(
            func.coalesce(func.sum(TransacaoFinanceira.valor_bruto), 0.0),
            func.coalesce(func.sum(TransacaoFinanceira.taxa_gateway), 0.0),
            func.coalesce(func.sum(TransacaoFinanceira.valor_liquido), 0.0)
        ).where(
            and_(
                TransacaoFinanceira.status_transacao == "paid",
                TransacaoFinanceira.criado_em >= primeiro_dia_mes
            )
        )
        res_fin = await db.execute(stmt_financeiro)
        bruto_mes, taxa_mes, liquido_mes = res_fin.first()

        # 3. Proficiência média atual da base estudantil (Theta médio)
        # Subquery para pegar o último theta de cada usuário
        subquery_ultimo = (
            select(
                HistoricoTheta.usuario_id,
                func.max(HistoricoTheta.registrado_em).label("max_data")
            )
            .group_by(HistoricoTheta.usuario_id)
            .subquery()
        )
        stmt_theta_medio = (
            select(func.avg(HistoricoTheta.theta_estimado))
            .join(
                subquery_ultimo,
                and_(
                    HistoricoTheta.usuario_id == subquery_ultimo.c.usuario_id,
                    HistoricoTheta.registrado_em == subquery_ultimo.c.max_data
                )
            )
        )
        theta_medio = (await db.execute(stmt_theta_medio)).scalar() or 0.0

        # 4. Distribuição por Tipo de Rede Escolar (Pública vs Privada)
        stmt_rede = select(Usuario.escola_tipo, func.count(Usuario.id)).where(
            Usuario.role == "student"
        ).group_by(Usuario.escola_tipo)
        res_rede = await db.execute(stmt_rede)
        mapa_rede = {tipo: qtd for tipo, qtd in res_rede.all()}

        # 5. Distribuição Geográfica por UF
        stmt_uf = select(Usuario.uf, func.count(Usuario.id)).where(
            Usuario.role == "student"
        ).group_by(Usuario.uf).order_by(desc(func.count(Usuario.id)))
        res_uf = await db.execute(stmt_uf)
        linhas_uf = res_uf.all()

        lista_uf = [
            DistribuicaoUfItem(
                uf=uf,
                total_alunos=qtd,
                percentual=round((qtd / total_alunos) * 100.0, 1) if total_alunos > 0 else 0.0
            )
            for uf, qtd in linhas_uf
        ]

        # 5. Total de horas líquidas ativas acumuladas
        stmt_horas_totais = select(func.sum(HorasEstudoDiaria.segundos_ativos))
        segundos_totais = (await db.execute(stmt_horas_totais)).scalar() or 0
        horas_liquidas_totais = round(segundos_totais / 3600.0, 1)

        return DashboardAnalyticsResponse(
            total_estudantes_ativos=total_alunos,
            faturamento_bruto_mes_atual=float(bruto_mes),
            taxa_gateway_mes_atual=float(taxa_mes),
            faturamento_liquido_mes_atual=float(liquido_mes),
            theta_medio_geral=round(float(theta_medio), 2),
            horas_estudo_liquidas_total=horas_liquidas_totais,
            distribuicao_rede=mapa_rede,
            distribuicao_uf=lista_uf
        )

    @staticmethod
    async def obter_ficha_aluno(db: AsyncSession, aluno_id: UUID) -> AlunoFichaResponse:
        """Recupera o dossiê detalhado do estudante em modo somente leitura."""
        stmt = select(Usuario).where(and_(Usuario.id == aluno_id, Usuario.role == "student"))
        usuario = (await db.execute(stmt)).scalar_one_or_none()
        if not usuario:
            raise ValueError("Estudante não localizado.")

        # Último Theta
        stmt_theta = (
            select(HistoricoTheta.theta_estimado)
            .where(HistoricoTheta.usuario_id == aluno_id)
            .order_by(HistoricoTheta.registrado_em.desc())
            .limit(1)
        )
        theta_val = (await db.execute(stmt_theta)).scalar() or 0.0

        # Total de capítulos concluídos
        stmt_cap = select(func.count(HeatmapDominio.id)).where(
            and_(HeatmapDominio.usuario_id == aluno_id, HeatmapDominio.aula_concluida == True)
        )
        total_caps = (await db.execute(stmt_cap)).scalar() or 0

        # Erros pendentes na Caixa de Reforço
        stmt_cr = select(func.count(CaixaReforco.id)).where(
            and_(CaixaReforco.usuario_id == aluno_id, CaixaReforco.status == "pendente")
        )
        erros_cr = (await db.execute(stmt_cr)).scalar() or 0

        # Horas líquidas ativas do estudante
        stmt_horas_aluno = select(func.sum(HorasEstudoDiaria.segundos_ativos)).where(
            HorasEstudoDiaria.usuario_id == aluno_id
        )
        segundos_aluno = (await db.execute(stmt_horas_aluno)).scalar() or 0
        horas_aluno = round(segundos_aluno / 3600.0, 1)

        return AlunoFichaResponse(
            usuario_id=usuario.id,
            nome_completo=usuario.nome_completo,
            email=usuario.email,
            cpf=usuario.cpf,
            cidade=usuario.cidade,
            uf=usuario.uf,
            escola_tipo=usuario.escola_tipo,
            nome_escola=usuario.nome_escola,
            serie_ano=usuario.serie_ano,
            eh_menor_idade=usuario.eh_menor_idade,
            dados_responsavel=usuario.dados_responsavel,
            theta_atual=float(theta_val),
            horas_liquidas_estudo=horas_aluno,
            total_capitulos_concluidos=total_caps,
            erros_pendentes_caixa_reforco=erros_cr,
            data_cadastro=usuario.criado_em
        )
```
