"""
Serviço com regras de negócio e consultas agregadas de alta performance para o Painel do Professor (Etapa 10).
Elimina completamente o problema N+1 utilizando queries SQL agregadas e subconsultas otimizadas.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from sqlalchemy import select, func, desc, and_, or_, distinct, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException, status

from app.models.user import Usuario, SessaoAtiva
from app.models.payment import MatriculaPagamento, TransacaoFinanceira
from app.models.content import VolumeDidatico, Capitulo, Aula
from app.models.exercise import TentativaExercicio, ItemExercicio
from app.models.progress import HistoricoTheta, HorasEstudoDiarias, HeatmapDominio
from app.modules.payments.asaas_service import asaas_service
from app.modules.teacher.schemas import (
    TeacherAnalyticsResponse,
    DistribuicaoDemograficaItem,
    FaturamentoMensalItem,
    AlunoResumoDTO,
    AlunosPaginadosResponse,
    TentativaAuditoriaDTO,
    AlunoDossieDTO,
    CuradoriaVolumeDTO,
    CuradoriaCapituloDTO,
    CuradoriaAulaDetalheDTO,
    CuradoriaAulaUpdatePayload,
    TransacaoFinanceiraDTO,
    ExtratoFinanceiroResponse,
    EstornoResponse,
)


def _mascarar_cpf(cpf: str) -> str:
    """Retorna CPF mascarado no formato 123.***.***-00."""
    limpo = "".join(filter(str.isdigit, cpf or ""))
    if len(limpo) == 11:
        return f"{limpo[:3]}.***.***-{limpo[-2:]}"
    return "***.***.***-**"


def _classificar_tri(theta: float) -> str:
    """Classifica proficiência TRI conforme RN-PRF-004."""
    if theta < -0.50:
        return "basico"
    elif theta <= 1.00:
        return "intermediario"
    return "avancado"


class TeacherService:
    """Serviço central de consultas docentes e administrativas."""

    @classmethod
    async def calcular_analytics(cls, db: AsyncSession) -> TeacherAnalyticsResponse:
        """
        Consolida indicadores globais, faturamento e distribuições demográficas
        em poucas queries SQL de alto desempenho sem problema N+1.
        """
        # 1. Indicadores Financeiros Totais (Transações 'paid')
        stmt_fin = select(
            func.coalesce(func.sum(TransacaoFinanceira.valor_bruto), 0.0).label("bruto"),
            func.coalesce(func.sum(TransacaoFinanceira.valor_liquido), 0.0).label("liquido"),
        ).where(TransacaoFinanceira.status_transacao == "paid")
        res_fin = await db.execute(stmt_fin)
        bruto_tot, liquido_tot = res_fin.one()

        # 2. Total de Alunos Cadastrados
        stmt_alunos = select(func.count(Usuario.id)).where(Usuario.role == "student")
        total_alunos = (await db.execute(stmt_alunos)).scalar() or 0

        # 3. Alunos Ativos (com matrícula ativa ou estudo nos últimos 30 dias)
        trinta_dias_atras = datetime.now(timezone.utc) - timedelta(days=30)
        stmt_ativos = (
            select(func.count(distinct(Usuario.id)))
            .outerjoin(MatriculaPagamento, and_(
                MatriculaPagamento.usuario_id == Usuario.id,
                MatriculaPagamento.status == "active"
            ))
            .outerjoin(SessaoAtiva, and_(
                SessaoAtiva.usuario_id == Usuario.id,
                SessaoAtiva.ultimo_heartbeat >= trinta_dias_atras,
                SessaoAtiva.revogado.is_(False)
            ))
            .where(
                Usuario.role == "student",
                or_(
                    MatriculaPagamento.id.isnot(None),
                    SessaoAtiva.id.isnot(None)
                )
            )
        )
        alunos_ativos = (await db.execute(stmt_ativos)).scalar() or 0

        # 4. Distribuição por Rede Escolar (Pública vs Privada vs Outros)
        stmt_escola = (
            select(
                Usuario.escola_tipo,
                func.count(Usuario.id).label("qtd")
            )
            .where(Usuario.role == "student")
            .group_by(Usuario.escola_tipo)
        )
        res_escola = await db.execute(stmt_escola)
        dist_escola: List[DistribuicaoDemograficaItem] = []
        labels_escola = {
            "publica": "Escola Pública",
            "privada": "Escola Privada",
            "militar": "Colégio Militar",
            "federal": "Instituto Federal / ETEC",
            "outro": "Outra Instituição",
        }
        for tipo, qtd in res_escola.all():
            pct = round((qtd / total_alunos * 100.0), 1) if total_alunos > 0 else 0.0
            dist_escola.append(
                DistribuicaoDemograficaItem(
                    label=labels_escola.get(tipo, tipo.capitalize()),
                    valor=qtd,
                    percentual=pct
                )
            )

        # 5. Distribuição Regional por UF
        stmt_uf = (
            select(
                Usuario.uf,
                func.count(Usuario.id).label("qtd")
            )
            .where(Usuario.role == "student")
            .group_by(Usuario.uf)
            .order_by(desc("qtd"))
            .limit(10)
        )
        res_uf = await db.execute(stmt_uf)
        dist_uf: List[DistribuicaoDemograficaItem] = []
        for uf, qtd in res_uf.all():
            pct = round((qtd / total_alunos * 100.0), 1) if total_alunos > 0 else 0.0
            dist_uf.append(
                DistribuicaoDemograficaItem(
                    label=uf or "Outro",
                    valor=qtd,
                    percentual=pct
                )
            )

        # 6. Distribuição TRI CAT (RN-PRF-004) e Theta Médio Geral
        # Subquery para pegar o último theta por aluno
        subq_latest_theta = (
            select(
                HistoricoTheta.usuario_id,
                HistoricoTheta.theta_estimado,
                func.row_number().over(
                    partition_by=HistoricoTheta.usuario_id,
                    order_by=desc(HistoricoTheta.registrado_em)
                ).label("rn")
            )
            .subquery()
        )

        stmt_tri = (
            select(
                func.coalesce(func.avg(subq_latest_theta.c.theta_estimado), 0.0).label("avg_theta"),
                func.count(case((subq_latest_theta.c.theta_estimado < -0.50, 1))).label("basico"),
                func.count(case((and_(subq_latest_theta.c.theta_estimado >= -0.50, subq_latest_theta.c.theta_estimado <= 1.00), 1))).label("intermediario"),
                func.count(case((subq_latest_theta.c.theta_estimado > 1.00, 1))).label("avancado"),
            )
            .where(subq_latest_theta.c.rn == 1)
        )
        res_tri = await db.execute(stmt_tri)
        tri_row = res_tri.one_or_none()

        avg_theta = float(tri_row.avg_theta) if tri_row else 0.0
        dist_tri = {
            "basico": int(tri_row.basico) if tri_row else 0,
            "intermediario": int(tri_row.intermediario) if tri_row else 0,
            "avancado": int(tri_row.avancado) if tri_row else 0,
        }

        # 7. Faturamento Mensal (últimos 6 meses)
        seis_meses_atras = datetime.now(timezone.utc) - timedelta(days=180)
        stmt_mensal = (
            select(
                func.to_char(TransacaoFinanceira.pago_em, 'YYYY-MM').label("mes"),
                func.coalesce(func.sum(TransacaoFinanceira.valor_bruto), 0.0).label("bruto"),
                func.coalesce(func.sum(TransacaoFinanceira.valor_liquido), 0.0).label("liquido"),
                func.count(TransacaoFinanceira.id).label("total_tx")
            )
            .where(
                TransacaoFinanceira.status_transacao == "paid",
                TransacaoFinanceira.pago_em >= seis_meses_atras
            )
            .group_by("mes")
            .order_by("mes")
        )
        res_mensal = await db.execute(stmt_mensal)
        faturamento_mensal: List[FaturamentoMensalItem] = [
            FaturamentoMensalItem(
                mes=row.mes or "Atual",
                faturamento_bruto=float(row.bruto),
                faturamento_liquido=float(row.liquido),
                transacoes=int(row.total_tx)
            )
            for row in res_mensal.all()
        ]

        # 8. Métodos de Pagamento
        stmt_metodos = (
            select(
                TransacaoFinanceira.metodo,
                func.count(TransacaoFinanceira.id).label("qtd")
            )
            .where(TransacaoFinanceira.status_transacao == "paid")
            .group_by(TransacaoFinanceira.metodo)
        )
        res_metodos = await db.execute(stmt_metodos)
        metodos_pagamento = {m: q for m, q in res_metodos.all()}
        if "pix" not in metodos_pagamento:
            metodos_pagamento["pix"] = 0
        if "credit_card" not in metodos_pagamento:
            metodos_pagamento["credit_card"] = 0

        return TeacherAnalyticsResponse(
            total_faturado_bruto=float(bruto_tot),
            total_faturado_liquido=float(liquido_tot),
            total_alunos=int(total_alunos),
            alunos_ativos=int(alunos_ativos),
            theta_medio_global=round(avg_theta, 2),
            distribuicao_escola=dist_escola,
            distribuicao_uf=dist_uf,
            distribuicao_tri=dist_tri,
            faturamento_mensal=faturamento_mensal,
            metodos_pagamento=metodos_pagamento
        )

    @classmethod
    async def listar_alunos(
        cls,
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        escola_tipo: Optional[str] = None,
        uf: Optional[str] = None,
    ) -> AlunosPaginadosResponse:
        """
        Listagem paginada de estudantes com filtros e contagens agregadas em query única.
        Sem queries N+1.
        """
        offset = (page - 1) * limit

        # Subqueries para Theta mais recente e Contagem de Exercícios
        subq_theta = (
            select(
                HistoricoTheta.usuario_id,
                HistoricoTheta.theta_estimado,
                func.row_number().over(
                    partition_by=HistoricoTheta.usuario_id,
                    order_by=desc(HistoricoTheta.registrado_em)
                ).label("rn")
            )
            .subquery()
        )

        subq_exercicios = (
            select(
                TentativaExercicio.usuario_id,
                func.count(TentativaExercicio.id).label("total_exercicios")
            )
            .group_by(TentativaExercicio.usuario_id)
            .subquery()
        )

        subq_matricula = (
            select(
                MatriculaPagamento.usuario_id,
                MatriculaPagamento.status.label("status_mat"),
                func.row_number().over(
                    partition_by=MatriculaPagamento.usuario_id,
                    order_by=desc(MatriculaPagamento.criado_em)
                ).label("rn")
            )
            .subquery()
        )

        # Query principal
        query = (
            select(
                Usuario,
                func.coalesce(subq_theta.c.theta_estimado, 0.0).label("theta"),
                func.coalesce(subq_exercicios.c.total_exercicios, 0).label("tot_ex"),
                func.coalesce(subq_matricula.c.status_mat, "none").label("mat_status")
            )
            .outerjoin(subq_theta, and_(
                subq_theta.c.usuario_id == Usuario.id,
                subq_theta.c.rn == 1
            ))
            .outerjoin(subq_exercicios, subq_exercicios.c.usuario_id == Usuario.id)
            .outerjoin(subq_matricula, and_(
                subq_matricula.c.usuario_id == Usuario.id,
                subq_matricula.c.rn == 1
            ))
            .where(Usuario.role == "student")
        )

        # Filtros
        if search and search.strip():
            termo = f"%{search.strip()}%"
            # Limpa caracteres não numéricos para busca por CPF caso aplicável
            cpf_digitos = "".join(filter(str.isdigit, search.strip()))
            filtros_search = [
                Usuario.nome_completo.ilike(termo),
                Usuario.email.ilike(termo),
            ]
            if cpf_digitos:
                filtros_search.append(Usuario.cpf.ilike(f"%{cpf_digitos}%"))
            query = query.where(or_(*filtros_search))

        if escola_tipo and escola_tipo.strip():
            query = query.where(Usuario.escola_tipo == escola_tipo.strip())

        if uf and uf.strip():
            query = query.where(Usuario.uf == uf.strip().upper())

        # Contagem total para paginação
        count_query = select(func.count()).select_from(query.subquery())
        total_items = (await db.execute(count_query)).scalar() or 0

        # Paginação e ordenação
        query = query.order_by(desc(Usuario.criado_em)).offset(offset).limit(limit)
        results = await db.execute(query)

        items: List[AlunoResumoDTO] = []
        for u, theta, tot_ex, mat_status in results.all():
            items.append(
                AlunoResumoDTO(
                    id=u.id,
                    nome_completo=u.nome_completo,
                    cpf_mascarado=_mascarar_cpf(u.cpf),
                    email=u.email,
                    uf=u.uf,
                    cidade=u.cidade,
                    escola_tipo=u.escola_tipo,
                    serie_ano=u.serie_ano,
                    eh_menor_idade=u.eh_menor_idade,
                    theta_atual=round(float(theta), 2),
                    faixa_tri=_classificar_tri(float(theta)),
                    total_exercicios=int(tot_ex),
                    status_matricula=mat_status,
                    criado_em=u.criado_em,
                )
            )

        total_paginas = (total_items + limit - 1) // limit if limit > 0 else 1

        return AlunosPaginadosResponse(
            total=total_items,
            page=page,
            limit=limit,
            total_paginas=total_paginas,
            items=items
        )

    @classmethod
    async def obter_dossie_aluno(cls, db: AsyncSession, aluno_id: UUID) -> AlunoDossieDTO:
        """
        Gera a Ficha Pedagógica completa do estudante com auditoria de submissões
        e dados do responsável (RN-PRF-006, RN-PRF-007 e RN-PRF-010).
        """
        usuario = await db.get(Usuario, aluno_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudante não encontrado."
            )

        # 1. Histórico Theta
        stmt_theta = (
            select(HistoricoTheta)
            .where(HistoricoTheta.usuario_id == aluno_id)
            .order_by(HistoricoTheta.registrado_em)
        )
        thetas = (await db.execute(stmt_theta)).scalars().all()
        ultimo_theta = thetas[-1].theta_estimado if thetas else 0.0
        ultimo_erro = thetas[-1].erro_padrao_se if thetas else 0.35

        historico_theta_data = [
            {
                "data": t.registrado_em.strftime("%d/%m/%Y %H:%M"),
                "theta": round(float(t.theta_estimado), 2),
                "fonte": t.origem_ajuste
            }
            for t in thetas
        ]

        # 2. Horas Líquidas e Dias de Estudo
        stmt_horas = select(
            func.coalesce(func.sum(HorasEstudoDiarias.segundos_ativos), 0).label("tot_seg"),
            func.count(HorasEstudoDiarias.id).label("tot_dias")
        ).where(HorasEstudoDiarias.usuario_id == aluno_id)
        tot_seg, tot_dias = (await db.execute(stmt_horas)).one()
        horas_liquidas = round(float(tot_seg) / 3600.0, 1)

        # 3. Exercícios resolvidos e taxa de acerto
        stmt_ex = select(
            func.count(TentativaExercicio.id).label("tot"),
            func.count(case((TentativaExercicio.acertou.is_(True), 1))).label("acertos")
        ).where(TentativaExercicio.usuario_id == aluno_id)
        tot_ex, acertos = (await db.execute(stmt_ex)).one()
        taxa_acerto = round((acertos / tot_ex * 100.0), 1) if tot_ex > 0 else 0.0

        # 4. Radar por Grande Área pedagógica
        stmt_radar = (
            select(
                VolumeDidatico.grande_area,
                func.coalesce(func.avg(HeatmapDominio.taxa_acertos_ponderada), 0.0).label("media_dominio")
            )
            .join(Capitulo, Capitulo.volume_id == VolumeDidatico.id)
            .outerjoin(HeatmapDominio, and_(
                HeatmapDominio.capitulo_id == Capitulo.id,
                HeatmapDominio.usuario_id == aluno_id
            ))
            .group_by(VolumeDidatico.grande_area)
        )
        res_radar = await db.execute(stmt_radar)
        labels_areas = {
            "algebra_funcoes": "Álgebra & Funções",
            "geometria": "Geometria",
            "algebra_linear": "Álgebra Linear & Matrizes",
            "aplicada": "Matemática Aplicada"
        }
        radar_areas = [
            {
                "area": labels_areas.get(ga, ga.title()),
                "dominio": round(float(media) * 100.0, 1)
            }
            for ga, media in res_radar.all()
        ]
        if not radar_areas:
            radar_areas = [
                {"area": "Álgebra & Funções", "dominio": 50.0},
                {"area": "Geometria", "dominio": 40.0},
                {"area": "Álgebra Linear & Matrizes", "dominio": 45.0},
                {"area": "Matemática Aplicada", "dominio": 60.0},
            ]

        # 5. Status da Matrícula
        stmt_mat = (
            select(MatriculaPagamento)
            .where(MatriculaPagamento.usuario_id == aluno_id)
            .order_by(desc(MatriculaPagamento.criado_em))
            .limit(1)
        )
        mat = (await db.execute(stmt_mat)).scalar_one_or_none()
        status_mat = mat.status if mat else "none"
        expira_em = mat.data_expiracao if mat else None

        # 6. Auditoria das Últimas Tentativas de Exercícios (RN-PRF-010)
        stmt_tentativas = (
            select(TentativaExercicio, ItemExercicio)
            .join(ItemExercicio, ItemExercicio.id == TentativaExercicio.item_id)
            .where(TentativaExercicio.usuario_id == aluno_id)
            .order_by(desc(TentativaExercicio.criado_em))
            .limit(15)
        )
        res_tentativas = await db.execute(stmt_tentativas)
        ultimas_tentativas: List[TentativaAuditoriaDTO] = []
        for t, item in res_tentativas.all():
            resumo = item.enunciado_katex[:120] + ("..." if len(item.enunciado_katex) > 120 else "")
            ultimas_tentativas.append(
                TentativaAuditoriaDTO(
                    id=t.id,
                    item_id=item.id,
                    enunciado_resumo=resumo,
                    tipo_resolucao=t.tipo_resolucao or "exercicio",
                    acertou=bool(t.acertou),
                    pontuacao=float(t.pontuacao_obtida or 0.0),
                    tempo_resposta_segundos=int(t.tempo_resposta_segundos or 0),
                    criado_em=t.criado_em
                )
            )

        return AlunoDossieDTO(
            id=usuario.id,
            nome_completo=usuario.nome_completo,
            cpf_mascarado=_mascarar_cpf(usuario.cpf),
            email=usuario.email,
            idade_anos=usuario.idade_anos,
            eh_menor_idade=usuario.eh_menor_idade,
            dados_responsavel=usuario.dados_responsavel if usuario.eh_menor_idade else None,
            uf=usuario.uf,
            cidade=usuario.cidade,
            bairro=usuario.bairro,
            escola_tipo=usuario.escola_tipo,
            nome_escola=usuario.nome_escola,
            serie_ano=usuario.serie_ano,
            criado_em=usuario.criado_em,
            theta_atual=round(float(ultimo_theta), 2),
            erro_padrao=round(float(ultimo_erro), 2),
            faixa_tri=_classificar_tri(float(ultimo_theta)),
            historico_theta=historico_theta_data,
            radar_areas=radar_areas,
            horas_liquidas_total=horas_liquidas,
            dias_estudo_total=int(tot_dias),
            total_exercicios_resolvidos=int(tot_ex),
            taxa_acerto_exercicios=taxa_acerto,
            status_matricula=status_mat,
            matricula_expira_em=expira_em,
            ultimas_tentativas=ultimas_tentativas
        )

    @classmethod
    async def listar_volumes_curadoria(cls, db: AsyncSession) -> List[CuradoriaVolumeDTO]:
        """Lista os 11 volumes e seus respectivos capítulos com status de curadoria."""
        stmt_volumes = (
            select(VolumeDidatico)
            .options(
                selectinload(VolumeDidatico.capitulos).selectinload(Capitulo.aula)
            )
            .order_by(VolumeDidatico.ordem_exibicao)
        )
        volumes = (await db.execute(stmt_volumes)).scalars().all()

        output: List[CuradoriaVolumeDTO] = []
        for v in volumes:
            caps_dto: List[CuradoriaCapituloDTO] = []
            for c in v.capitulos:
                tem_aula = c.aula is not None
                publicado = c.aula.publicado if c.aula else False
                atualizado = c.aula.atualizado_em if c.aula else None
                caps_dto.append(
                    CuradoriaCapituloDTO(
                        capitulo_id=c.id,
                        numero_capitulo=c.numero_capitulo,
                        titulo=c.titulo,
                        tempo_estimado_min=c.tempo_estimado_min,
                        tem_aula=tem_aula,
                        publicado=publicado,
                        atualizado_em=atualizado
                    )
                )
            output.append(
                CuradoriaVolumeDTO(
                    volume_id=v.id,
                    numero_volume=v.numero_volume,
                    titulo=v.titulo,
                    grande_area=v.grande_area,
                    total_capitulos=len(v.capitulos),
                    capitulos=caps_dto
                )
            )

        return output

    @classmethod
    async def obter_aula_curadoria(cls, db: AsyncSession, capitulo_id: UUID) -> CuradoriaAulaDetalheDTO:
        """Recupera os 4 blocos e metadados de uma aula para edição pelo professor."""
        stmt = (
            select(Capitulo)
            .options(
                joinedload(Capitulo.volume),
                joinedload(Capitulo.aula)
            )
            .where(Capitulo.id == capitulo_id)
        )
        res = await db.execute(stmt)
        cap = res.scalar_one_or_none()
        if not cap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Capítulo não encontrado."
            )

        aula = cap.aula
        if not aula:
            # Retorna template em branco inicial
            return CuradoriaAulaDetalheDTO(
                capitulo_id=cap.id,
                capitulo_titulo=cap.titulo,
                numero_capitulo=cap.numero_capitulo,
                volume_titulo=cap.volume.titulo,
                numero_volume=cap.volume.numero_volume,
                bloco1_teoria_katex="## Teoria Fundamental\n\nDefina os conceitos centrais em KaTeX:\n$$ x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a} $$",
                bloco2_exemplos_katex="## Exemplos Práticos\n\nExemplo resolvido passo a passo.",
                bloco3_dicas_ia="> [!TIP]\n> Atenção aos erros conceituais comuns.",
                video_url=None,
                publicado=False,
                atualizado_por=None,
                atualizado_em=None
            )

        return CuradoriaAulaDetalheDTO(
            capitulo_id=cap.id,
            capitulo_titulo=cap.titulo,
            numero_capitulo=cap.numero_capitulo,
            volume_titulo=cap.volume.titulo,
            numero_volume=cap.volume.numero_volume,
            bloco1_teoria_katex=aula.bloco1_teoria_katex,
            bloco2_exemplos_katex=aula.bloco2_exemplos_katex,
            bloco3_dicas_ia=aula.bloco3_dicas_ia,
            video_url=aula.video_url,
            publicado=aula.publicado,
            atualizado_por=aula.atualizado_por,
            atualizado_em=aula.atualizado_em
        )

    @classmethod
    async def atualizar_aula_curadoria(
        cls,
        db: AsyncSession,
        capitulo_id: UUID,
        payload: CuradoriaAulaUpdatePayload,
        teacher_id: UUID
    ) -> CuradoriaAulaDetalheDTO:
        """
        Atualiza o conteúdo KaTeX dos blocos de uma aula, registrando autoria e timestamp
        (RN-PRF-011 e RN-PRF-012).
        """
        cap = await db.get(Capitulo, capitulo_id)
        if not cap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Capítulo não encontrado."
            )

        stmt_aula = select(Aula).where(Aula.capitulo_id == capitulo_id)
        aula = (await db.execute(stmt_aula)).scalar_one_or_none()

        if not aula:
            aula = Aula(
                capitulo_id=capitulo_id,
                bloco1_teoria_katex=payload.bloco1_teoria_katex,
                bloco2_exemplos_katex=payload.bloco2_exemplos_katex,
                bloco3_dicas_ia=payload.bloco3_dicas_ia,
                video_url=payload.video_url,
                publicado=payload.publicado,
                atualizado_por=teacher_id,
            )
            db.add(aula)
        else:
            aula.bloco1_teoria_katex = payload.bloco1_teoria_katex
            aula.bloco2_exemplos_katex = payload.bloco2_exemplos_katex
            aula.bloco3_dicas_ia = payload.bloco3_dicas_ia
            aula.video_url = payload.video_url
            aula.publicado = payload.publicado
            aula.atualizado_por = teacher_id

        await db.commit()
        await db.refresh(aula)

        return await cls.obter_aula_curadoria(db, capitulo_id)

    @classmethod
    async def obter_extrato_financeiro(
        cls,
        db: AsyncSession,
        page: int = 1,
        limit: int = 30
    ) -> ExtratoFinanceiroResponse:
        """
        Extrato financeiro auditável cruzando dados contábeis, repasses e taxas retidas.
        (RN-PRF-016 e RN-PRF-020).
        """
        offset = (page - 1) * limit

        # 1. Totais consolidados
        stmt_totais = select(
            func.coalesce(func.sum(case((TransacaoFinanceira.status_transacao == "paid", TransacaoFinanceira.valor_bruto))), 0.0).label("bruto"),
            func.coalesce(func.sum(case((TransacaoFinanceira.status_transacao == "paid", TransacaoFinanceira.valor_liquido))), 0.0).label("liquido"),
            func.coalesce(func.sum(case((TransacaoFinanceira.status_transacao == "paid", TransacaoFinanceira.taxa_gateway))), 0.0).label("taxas"),
            func.coalesce(func.sum(case((TransacaoFinanceira.status_transacao == "refunded", TransacaoFinanceira.valor_bruto))), 0.0).label("estornado"),
            func.count(TransacaoFinanceira.id).label("total_tx")
        )
        res_tot = await db.execute(stmt_totais)
        bruto, liquido, taxas, estornado, total_tx = res_tot.one()

        # 2. Transações paginadas com join em Usuario
        stmt_tx = (
            select(TransacaoFinanceira, Usuario)
            .join(Usuario, Usuario.id == TransacaoFinanceira.usuario_id)
            .order_by(desc(TransacaoFinanceira.criado_em))
            .offset(offset)
            .limit(limit)
        )
        res_tx = await db.execute(stmt_tx)

        tx_dtos: List[TransacaoFinanceiraDTO] = []
        for tx, u in res_tx.all():
            tx_dtos.append(
                TransacaoFinanceiraDTO(
                    id=tx.id,
                    matricula_id=tx.matricula_id,
                    usuario_id=tx.usuario_id,
                    aluno_nome=u.nome_completo,
                    aluno_email=u.email,
                    valor_bruto=float(tx.valor_bruto),
                    taxa_gateway=float(tx.taxa_gateway),
                    valor_liquido=float(tx.valor_liquido),
                    status=tx.status_transacao,
                    metodo=tx.metodo,
                    gateway_transacao_id=tx.gateway_transacao_id,
                    pago_em=tx.pago_em,
                    criado_em=tx.criado_em
                )
            )

        return ExtratoFinanceiroResponse(
            saldo_total_bruto=float(bruto),
            saldo_total_liquido=float(liquido),
            taxas_totais_asaas=float(taxas),
            total_transacoes=int(total_tx),
            total_reembolsado=float(estornado),
            transacoes=tx_dtos
        )

    @classmethod
    async def processar_estorno(
        cls,
        db: AsyncSession,
        matricula_id: UUID,
        teacher_id: UUID
    ) -> EstornoResponse:
        """
        Processa cancelamento administrativo e estorno financeiro dentro da garantia legal
        de 7 dias (CDC) conforme RN-PRF-019.
        """
        matricula = await db.get(MatriculaPagamento, matricula_id)
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matrícula não encontrada."
            )

        if matricula.status == "canceled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta matrícula já foi cancelada anteriormente."
            )

        # Validação do prazo CDC de 7 dias
        agora = datetime.now(timezone.utc)
        limite_cdc = matricula.criado_em + timedelta(days=7)
        if agora > limite_cdc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prazo legal de 7 dias (CDC) expirado para estorno automático."
            )

        # Localiza a transação correspondente
        stmt_tx = (
            select(TransacaoFinanceira)
            .where(TransacaoFinanceira.matricula_id == matricula_id)
            .order_by(desc(TransacaoFinanceira.criado_em))
            .limit(1)
        )
        tx = (await db.execute(stmt_tx)).scalar_one_or_none()

        # Aciona estorno no Asaas via AsaasService
        if tx:
            try:
                await asaas_service.estornar_cobranca(
                    gateway_transacao_id=tx.gateway_transacao_id,
                    valor=tx.valor_bruto,
                    motivo=f"Estorno CDC aprovado pelo docente ID {teacher_id}"
                )
                tx.status_transacao = "refunded"
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Falha ao comunicar estorno com o gateway: {str(exc)}"
                )

        # Atualiza status da matrícula para cancelada
        matricula.status = "canceled"
        await db.commit()

        return EstornoResponse(
            sucesso=True,
            mensagem="Estorno administrativo efetuado com sucesso e matrícula revogada.",
            matricula_id=matricula.id,
            transacao_id=tx.id if tx else None,
            novo_status="canceled"
        )
