"""
Endpoints REST FastAPI para Navegação de Conteúdo Didático, Skill Tree e Aulas KaTeX.
Conforme especificações em docs-site/docs/implementation/etapa-05-conteudo.md e docs-site/docs/modules/conteudo/.

Regras aplicadas:
- RN-CNT-010: conclusão de aula exige aproveitamento >= 60% na bateria de fixação.
- RN-PRG-012: cores canônicas do heatmap (cinza/vermelho/amarelo/verde) com limiares 50%/75%.
- RN-PRG-003: tempo líquido ativo consolidado em horas_estudo_diarias (Tabela 17).

Nota de segurança: toda a bateria de fixação (gabarito e correção) é processada
exclusivamente no servidor. O cliente nunca recebe a alternativa correta antes
de submeter as respostas (motor CAT completo chega na Etapa 7).
"""
from datetime import date, datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, update
from sqlalchemy.orm import selectinload

import logging
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.redis import get_redis
from app.models.content import Disciplina, VolumeDidatico, Capitulo, Aula
from app.models.progress import HeatmapDominio, HorasEstudoDiarias
from app.models.user import Usuario
from app.ai.llm_factory import LLMFactory
from app.ai.rag_engine import RAGEngine
from app.ai.prompts.socratic import SYSTEM_PROMPT_SOCRATICO
from app.ai.socratic_state import SocraticStateManager

logger = logging.getLogger("app.modules.content.router")
from app.schemas.content import (
    DisciplinaResponse,
    VolumeResponse,
    CapituloResponse,
    SkillTreeNodeResponse,
    VolumeComCapitulosResponse,
    AulaResponse,
    ConcluirAulaRequest,
    ConcluirAulaResponse,
    ChatAulaRequest,
    ChatAulaResponse,
    ChunkRAGResponse,
    SolicitarPistaRequest,
    SolicitarPistaResponse,
    BateriaFixacaoResponse,
    QuestaoFixacaoResponse,
    SubmeterFixacaoRequest,
    SubmeterFixacaoResponse,
    calcular_status_heatmap,
    STATUS_COR_PARA_FRONTEND,
    STATUS_DOMINIO_PARA_FRONTEND,
)

router = APIRouter(prefix="/api/v1/conteudo", tags=["Conteúdo Didático"])

# ============================================================================
# Baterias de fixação canônicas server-side (Volume, Capítulo) -> questões.
# Estado imutável em código: sobrevive a restarts e nunca expõe o gabarito
# ao cliente. Na Etapa 7, será substituído pelas tabelas
# itens_exercicios/tentativas_exercicios + motor CAT.
# ============================================================================
from app.modules.content.fixacao_seed import BATERIAS_FIXACAO_CANONICAS


def _obter_bateria(capitulo: Capitulo) -> Optional[list[dict]]:
    """Resolve a bateria canônica pela posição (volume, capítulo) do capítulo."""
    volume_numero = capitulo.volume.numero_volume if capitulo.volume else None
    if volume_numero is None:
        return None
    return BATERIAS_FIXACAO_CANONICAS.get((volume_numero, capitulo.numero_capitulo))


def _montar_nó_heatmap(
    cap: Capitulo,
    heatmap: Optional[HeatmapDominio],
) -> SkillTreeNodeResponse:
    """Constrói o nó da Skill Tree aplicando RN-PRG-012 sobre o heatmap real."""
    if heatmap is None:
        return SkillTreeNodeResponse(
            id=cap.id,
            volume_id=cap.volume_id,
            numero_capitulo=cap.numero_capitulo,
            titulo=cap.titulo,
            tempo_estimado_min=cap.tempo_estimado_min,
            ordem=cap.ordem,
            status_dominio="not_started",
            cor_heatmap="grey",
            percentual_acerto=0.0,
            desbloqueado=True,
        )

    taxa = float(heatmap.taxa_acertos_ponderada)
    cor = STATUS_COR_PARA_FRONTEND[heatmap.status_cor]
    return SkillTreeNodeResponse(
        id=cap.id,
        volume_id=cap.volume_id,
        numero_capitulo=cap.numero_capitulo,
        titulo=cap.titulo,
        tempo_estimado_min=cap.tempo_estimado_min,
        ordem=cap.ordem,
        status_dominio=STATUS_DOMINIO_PARA_FRONTEND[heatmap.status_cor],
        cor_heatmap=cor,
        percentual_acerto=taxa,
        desbloqueado=heatmap.aula_concluida or cap.ordem == 1,
    )


async def _obter_heatmaps(
    db: AsyncSession,
    usuario_id: UUID,
    capitulo_ids: list[UUID],
) -> dict[UUID, HeatmapDominio]:
    """Carrega os heatmaps do usuário para uma lista de capítulos em 1 query."""
    if not capitulo_ids:
        return {}
    result = await db.execute(
        select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario_id,
                HeatmapDominio.capitulo_id.in_(capitulo_ids),
            )
        )
    )
    return {h.capitulo_id: h for h in result.scalars().all()}


# ============================================================================
# 1. Catálogo e Estrutura Curricular (Disciplinas, Volumes, Capítulos)
# ============================================================================

@router.get("/disciplinas", response_model=List[DisciplinaResponse], summary="Listar disciplinas ativas")
async def listar_disciplinas(
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Retorna todas as disciplinas disponíveis para estudo (ex: Matemática)."""
    result = await db.execute(
        select(Disciplina).where(Disciplina.ativo == True).order_by(Disciplina.ordem)  # noqa: E712
    )
    return result.scalars().all()


@router.get("/volumes/{disciplina_id}", response_model=List[VolumeResponse], summary="Listar volumes de uma disciplina")
async def listar_volumes_disciplina(
    disciplina_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Retorna os volumes (coleção Iezzi) vinculados a uma disciplina, com contagem de capítulos em 1 query."""
    result = await db.execute(
        select(VolumeDidatico, func.count(Capitulo.id).label("total_capitulos"))
        .outerjoin(Capitulo, Capitulo.volume_id == VolumeDidatico.id)
        .where(and_(VolumeDidatico.disciplina_id == disciplina_id, VolumeDidatico.ativo == True))  # noqa: E712
        .group_by(VolumeDidatico.id)
        .order_by(VolumeDidatico.ordem_exibicao)
    )
    rows = result.all()
    return [
        VolumeResponse(
            id=vol.id,
            disciplina_id=vol.disciplina_id,
            nome_colecao=vol.nome_colecao,
            numero_volume=vol.numero_volume,
            titulo=vol.titulo,
            grande_area=vol.grande_area,
            ordem_exibicao=vol.ordem_exibicao,
            preco_padrao=float(vol.preco_padrao),
            ativo=vol.ativo,
            total_capitulos=total_caps,
        )
        for vol, total_caps in rows
    ]


@router.get("/capitulos/{volume_id}", response_model=List[SkillTreeNodeResponse], summary="Listar capítulos de um volume para a Skill Tree")
async def listar_capitulos_volume(
    volume_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Retorna a sequência de capítulos dimensionados para 50 minutos com o heatmap de domínio real do usuário."""
    result = await db.execute(
        select(Capitulo).where(Capitulo.volume_id == volume_id).order_by(Capitulo.ordem)
    )
    capitulos = result.scalars().all()
    if not capitulos:
        vol_check = await db.execute(select(VolumeDidatico).where(VolumeDidatico.id == volume_id))
        if not vol_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume não encontrado.")

    heatmaps = await _obter_heatmaps(db, usuario.id, [c.id for c in capitulos])
    return [_montar_nó_heatmap(cap, heatmaps.get(cap.id)) for cap in capitulos]


@router.get("/skill-tree", response_model=List[VolumeComCapitulosResponse], summary="Recuperar Árvore de Habilidades completa da disciplina ativa")
async def obter_skill_tree(
    disciplina_slug: str = Query("matematica"),
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Retorna a Skill Tree completa da disciplina, com todos os 11 volumes,
    seus capítulos e o heatmap de domínio real do usuário autenticado,
    em uma única chamada otimizada (2 queries no total).
    """
    disc_res = await db.execute(
        select(Disciplina).where(Disciplina.slug == disciplina_slug)
    )
    disciplina = disc_res.scalar_one_or_none()
    if not disciplina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina não encontrada.")

    volumes_res = await db.execute(
        select(VolumeDidatico)
        .where(and_(VolumeDidatico.disciplina_id == disciplina.id, VolumeDidatico.ativo == True))  # noqa: E712
        .options(selectinload(VolumeDidatico.capitulos))
        .order_by(VolumeDidatico.ordem_exibicao)
    )
    volumes = volumes_res.scalars().all()

    todos_capitulos = [cap for vol in volumes for cap in vol.capitulos]
    heatmaps = await _obter_heatmaps(db, usuario.id, [c.id for c in todos_capitulos])

    tree = []
    for vol in volumes:
        capitulos_nodes = [
            _montar_nó_heatmap(cap, heatmaps.get(cap.id))
            for cap in sorted(vol.capitulos, key=lambda c: c.ordem)
        ]
        tree.append(
            VolumeComCapitulosResponse(
                id=vol.id,
                numero_volume=vol.numero_volume,
                titulo=vol.titulo,
                grande_area=vol.grande_area,
                ordem_exibicao=vol.ordem_exibicao,
                capitulos=capitulos_nodes,
            )
        )
    return tree


# ============================================================================
# 2. Aula em 4 Blocos KaTeX
# ============================================================================

@router.get("/aulas/{capitulo_id}", response_model=AulaResponse, summary="Obter conteúdo completo da aula em 4 blocos")
async def obter_aula_capitulo(
    capitulo_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Recupera os 4 blocos pedagógicos (Teoria KaTeX, Exemplos, Dicas e Fixação) para o capítulo selecionado."""
    stmt = (
        select(Aula)
        .join(Capitulo, Aula.capitulo_id == Capitulo.id)
        .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
        .where(Aula.capitulo_id == capitulo_id)
        .options(
            selectinload(Aula.capitulo).selectinload(Capitulo.volume)
        )
    )
    result = await db.execute(stmt)
    aula = result.scalar_one_or_none()

    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada ou ainda não publicada para este capítulo."
        )

    return AulaResponse(
        id=aula.id,
        capitulo_id=aula.capitulo_id,
        bloco1_teoria_katex=aula.bloco1_teoria_katex,
        bloco2_exemplos_katex=aula.bloco2_exemplos_katex,
        bloco3_dicas_ia=aula.bloco3_dicas_ia,
        video_url=aula.video_url,
        publicado=aula.publicado,
        atualizado_em=aula.atualizado_em,
        capitulo_titulo=aula.capitulo.titulo,
        numero_capitulo=aula.capitulo.numero_capitulo,
        volume_id=aula.capitulo.volume.id,
        numero_volume=aula.capitulo.volume.numero_volume,
        volume_titulo=aula.capitulo.volume.titulo,
    )


@router.get(
    "/aulas/{capitulo_id}/fixacao",
    response_model=BateriaFixacaoResponse,
    summary="Obter bateria de fixação server-side (sem gabarito)",
)
async def obter_bateria_fixacao(
    capitulo_id: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """Serve a bateria de fixação do capítulo SEM expor o gabarito.
    A correção ocorre apenas no POST de submissão (anti-trapaça).
    """
    cap_res = await db.execute(
        select(Capitulo).where(Capitulo.id == capitulo_id).options(selectinload(Capitulo.volume))
    )
    capitulo = cap_res.scalar_one_or_none()
    if not capitulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capítulo não encontrado.")

    questoes_raw = _obter_bateria(capitulo)
    if not questoes_raw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bateria de fixação ainda não disponível para este capítulo.",
        )

    return BateriaFixacaoResponse(
        capitulo_id=capitulo_id,
        questoes=[
            QuestaoFixacaoResponse(
                numero=q["numero"],
                enunciado_katex=q["enunciado"],
                alternativas=q["alternativas"],
            )
            for q in questoes_raw
        ],
        percentual_minimo=60.0,
    )


@router.post(
    "/aulas/{capitulo_id}/fixacao",
    response_model=SubmeterFixacaoResponse,
    summary="Submeter respostas da fixação: corrige no servidor e registra progresso",
)
async def submeter_fixacao(
    capitulo_id: UUID,
    payload: SubmeterFixacaoRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Corrige a bateria no servidor (RN-CNT-010), atualiza o heatmap_dominio do
    usuário (RN-PRG-012) e consolida o tempo líquido ativo do dia na
    horas_estudo_diarias (RN-PRG-003 / Tabela 17).
    """
    cap_res = await db.execute(
        select(Capitulo).where(Capitulo.id == capitulo_id).options(selectinload(Capitulo.volume))
    )
    capitulo = cap_res.scalar_one_or_none()
    if not capitulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capítulo não encontrado.")

    questoes_raw = _obter_bateria(capitulo)
    if not questoes_raw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bateria de fixação ainda não disponível para este capítulo.",
        )

    # --- Correção server-side ---
    gabarito = {q["numero"]: q["indice_correto"] for q in questoes_raw}
    acertos = sum(
        1 for numero, escolhida in payload.respostas.items()
        if gabarito.get(numero) == escolhida
    )
    percentual = round((acertos / len(questoes_raw)) * 100.0, 2)
    concluida = percentual >= 60.0

    # --- Persistência: heatmap_dominio (Tabela 15) ---
    total_respondidas = len(payload.respostas)
    status_cor = calcular_status_heatmap(total_respondidas, percentual)

    hm_res = await db.execute(
        select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario.id,
                HeatmapDominio.capitulo_id == capitulo_id,
            )
        )
    )
    heatmap = hm_res.scalar_one_or_none()
    if heatmap:
        heatmap.total_questoes_respondidas = total_respondidas
        heatmap.taxa_acertos_ponderada = percentual
        heatmap.status_cor = status_cor
        heatmap.aula_concluida = heatmap.aula_concluida or concluida
        heatmap.ultima_interacao = datetime.now(timezone.utc)
    else:
        heatmap = HeatmapDominio(
            usuario_id=usuario.id,
            capitulo_id=capitulo_id,
            total_questoes_respondidas=total_respondidas,
            taxa_acertos_ponderada=percentual,
            status_cor=status_cor,
            aula_concluida=concluida,
        )
        db.add(heatmap)

    # --- Persistência: horas_estudo_diarias (Tabela 17) ---
    hoje = date.today()
    hs_res = await db.execute(
        select(HorasEstudoDiarias).where(
            and_(
                HorasEstudoDiarias.usuario_id == usuario.id,
                HorasEstudoDiarias.data_registro == hoje,
            )
        )
    )
    horas_dia = hs_res.scalar_one_or_none()
    if horas_dia:
        horas_dia.segundos_ativos += payload.segundos_estudo
        horas_dia.exercicios_submetidos += total_respondidas
        if concluida and not (heatmap.aula_concluida and percentual < 60.0):
            horas_dia.aulas_concluidas += 1
    else:
        horas_dia = HorasEstudoDiarias(
            usuario_id=usuario.id,
            data_registro=hoje,
            segundos_ativos=payload.segundos_estudo,
            exercicios_submetidos=total_respondidas,
            aulas_concluidas=1 if concluida else 0,
        )
        db.add(horas_dia)

    # --- Próximo capítulo da sequência ---
    next_cap_res = await db.execute(
        select(Capitulo)
        .where(and_(Capitulo.volume_id == capitulo.volume_id, Capitulo.ordem == capitulo.ordem + 1))
    )
    proximo_cap = next_cap_res.scalar_one_or_none()

    await db.commit()

    if concluida:
        mensagem = (
            f"Parabéns! Você atingiu {percentual:.1f}% de aproveitamento na bateria de fixação "
            f"do capítulo '{capitulo.titulo}'!"
        )
    else:
        mensagem = (
            f"Aproveitamento de {percentual:.1f}% abaixo do mínimo pedagógico (60%). "
            "Revise os conceitos no Bloco 1 ou tente a 2ª chance nas questões para avançar!"
        )

    return SubmeterFixacaoResponse(
        sucesso=True,
        percentual_acertos=percentual,
        percentual_minimo=60.0,
        concluida=concluida,
        mensagem=mensagem,
        gabarito=gabarito,
        proximo_capitulo_id=proximo_cap.id if proximo_cap else None,
    )


@router.post("/aulas/{capitulo_id}/concluir", response_model=ConcluirAulaResponse, summary="Registrar conclusão de aula com trava pedagógica de 60%")
async def concluir_aula(
    capitulo_id: UUID,
    payload: ConcluirAulaRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    RN-CNT-010: valida se o estudante atingiu o aproveitamento mínimo de 60%
    e persiste a conclusão no heatmap_dominio (Tabela 15).

    Preferencialmente use POST /aulas/{id}/fixacao, que corrige no servidor
    e já registra heatmap + tempo de estudo em uma única chamada.
    """
    cap_res = await db.execute(select(Capitulo).where(Capitulo.id == capitulo_id))
    capitulo = cap_res.scalar_one_or_none()
    if not capitulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capítulo não encontrado.")

    if payload.percentual_acertos < 60.0:
        return ConcluirAulaResponse(
            sucesso=False,
            concluida=False,
            mensagem=(
                f"Aproveitamento de {payload.percentual_acertos:.1f}% abaixo do mínimo pedagógico (60%). "
                "Revise os conceitos no Bloco 1 ou tente a 2ª chance nas questões para avançar!"
            ),
            percentual_atingido=payload.percentual_acertos,
            proximo_capitulo_id=None,
        )

    # Persistir aula_concluida no heatmap (Tabela 15)
    hm_res = await db.execute(
        select(HeatmapDominio).where(
            and_(
                HeatmapDominio.usuario_id == usuario.id,
                HeatmapDominio.capitulo_id == capitulo_id,
            )
        )
    )
    heatmap = hm_res.scalar_one_or_none()
    if heatmap:
        heatmap.aula_concluida = True
        nova_taxa = max(float(heatmap.taxa_acertos_ponderada), payload.percentual_acertos)
        heatmap.taxa_acertos_ponderada = nova_taxa
        heatmap.status_cor = calcular_status_heatmap(
            max(heatmap.total_questoes_respondidas, 3), nova_taxa
        )
        heatmap.ultima_interacao = datetime.now(timezone.utc)
    else:
        db.add(
            HeatmapDominio(
                usuario_id=usuario.id,
                capitulo_id=capitulo_id,
                total_questoes_respondidas=3,
                taxa_acertos_ponderada=payload.percentual_acertos,
                status_cor=calcular_status_heatmap(3, payload.percentual_acertos),
                aula_concluida=True,
            )
        )

    next_cap_res = await db.execute(
        select(Capitulo)
        .where(and_(Capitulo.volume_id == capitulo.volume_id, Capitulo.ordem == capitulo.ordem + 1))
    )
    proximo_cap = next_cap_res.scalar_one_or_none()
    await db.commit()

    return ConcluirAulaResponse(
        sucesso=True,
        concluida=True,
        mensagem=f"Parabéns! Aula '{capitulo.titulo}' concluída com aproveitamento de {payload.percentual_acertos:.1f}%!",
        percentual_atingido=payload.percentual_acertos,
        proximo_capitulo_id=proximo_cap.id if proximo_cap else None,
    )


# ============================================================================
# 3. Interação com Tutor Socrático e Motor RAG (Etapa 6)
# ============================================================================

MAX_MENSAGENS_CHAT_CAPITULO = 30


@router.post("/aulas/{capitulo_id}/chat", response_model=ChatAulaResponse, summary="Conversar com o Tutor Socrático da Coleção Iezzi")
async def chat_socratico(
    capitulo_id: UUID,
    payload: ChatAulaRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Processa a dúvida do estudante na aula com mediação socrática em KaTeX:
    1. Aplica Rate Limiting pedagógico (máx 30 mensagens por sessão/capítulo via Redis).
    2. Localiza o capítulo e o respectivo VolumeDidatico (particionamento do agente Iezzi).
    3. Executa busca vetorial (RAG) no pgvector sobre a coleção Iezzi filtrada por volume_id.
    4. Determina o estágio socrático adequado (1: Reflexão, 2: Pista, 3: Passo Guiado).
    5. Invoca a LLMFactory com fallback resiliente para falhas de rede/cota.
    """
    # 1. Rate limiting pedagógico via Redis (30 mensagens / capítulo / dia)
    try:
        redis_client = get_redis()
        rate_key = f"ratelimit:chat:{usuario.id}:{capitulo_id}"
        total_mensagens = await redis_client.incr(rate_key)
        if total_mensagens == 1:
            await redis_client.expire(rate_key, 86400)

        if total_mensagens > MAX_MENSAGENS_CHAT_CAPITULO:
            return ChatAulaResponse(
                resposta_katex=(
                    "Você atingiu o limite pedagógico de 30 mensagens de mentoria para este capítulo! "
                    "Para consolidar seu aprendizado, recomendo testar suas habilidades práticas na "
                    "**Aba 4 (Fixação)**. Lá você poderá colocar a teoria em prática e avançar na sua trilha!"
                ),
                chunks_utilizados=[],
                nivel_ajuda_socratico=2,
            )
    except Exception as e:
        logger.warning(f"Erro ao verificar rate limiting no Redis (prosseguindo sem bloqueio): {e}")

    # 2. Busca capítulo e volume didático
    stmt = (
        select(Capitulo)
        .options(selectinload(Capitulo.volume))
        .where(Capitulo.id == capitulo_id)
    )
    res = await db.execute(stmt)
    capitulo = res.scalar_one_or_none()
    if not capitulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capítulo não encontrado.")

    volume = capitulo.volume
    if not volume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume associado não encontrado.")

    # 3. Busca trechos no RAG particionados estritamente pelo volume_id
    query_busca = payload.mensagem
    if payload.trecho_selecionado:
        query_busca = f"Expressão selecionada: {payload.trecho_selecionado}. Dúvida: {payload.mensagem}"

    chunks = await RAGEngine.buscar_trechos_relevantes(
        db=db,
        volume_id=volume.id,
        query_aluno=query_busca,
        limite_chunks=3,
        threshold_similaridade=0.40,
    )

    if chunks:
        trechos_formatados = "\n\n".join(
            [f"Página {c.pagina or 's/n'} ({c.teorema_ou_topico or 'Teorema'}):\n{c.trecho}" for c in chunks]
        )
    else:
        trechos_formatados = (
            f"Volume {volume.numero_volume}: {volume.titulo}. "
            f"Capítulo {capitulo.numero_capitulo}: {capitulo.titulo}."
        )

    # 4. Determina o estágio socrático via Máquina de Estados (SocraticStateManager).
    # O estado (estágio + último tópico) é persistido no Redis por (usuário, capítulo):
    # sobrevive a refresh/reconexões do frontend, permite o reset pedagógico por
    # troca de tópico e nunca regride quando o histórico chega curto ao backend.
    chave_estagio = f"socratico:{usuario.id}:{capitulo_id}"
    estagio_atual = 0
    ultimo_topico = None
    redis_estagio = None
    try:
        redis_estagio = get_redis()
        estado_raw = await redis_estagio.get(chave_estagio)
        if estado_raw:
            partes_estado = estado_raw.split("|", 1)
            estagio_atual = int(partes_estado[0])
            ultimo_topico = partes_estado[1] if len(partes_estado) > 1 and partes_estado[1] else None
    except Exception as e:
        logger.warning(f"Erro ao carregar estado socrático no Redis (iniciando do zero): {e}")

    estagio_ajuda = SocraticStateManager.determinar_proximo_estagio(
        estagio_atual=estagio_atual,
        topico_atual=payload.trecho_selecionado,
        ultimo_topico_registrado=ultimo_topico,
        mensagem_aluno=payload.mensagem,
    )

    if redis_estagio is not None:
        try:
            await redis_estagio.set(
                chave_estagio,
                f"{estagio_ajuda}|{payload.trecho_selecionado or ''}",
                ex=86400,
            )
        except Exception as e:
            logger.warning(f"Erro ao persistir estado socrático no Redis: {e}")

    # 5. Constrói a instrução de sistema rigorosa do Iezzi
    system_instruction = SYSTEM_PROMPT_SOCRATICO.format(
        numero_volume=volume.numero_volume,
        titulo_volume=volume.titulo,
        trechos_rag=trechos_formatados,
        estagio_ajuda=estagio_ajuda,
    )

    # 6. Chama a LLMFactory com tolerância a falhas (fallback resiliente sem erro 500)
    historico_dicts = [
        {"papel": m.papel, "conteudo": m.conteudo}
        for m in payload.historico_recente
    ]

    try:
        provedor_llm = LLMFactory.obter_provedor()
        resposta_texto = await provedor_llm.gerar_resposta(
            prompt_usuario=payload.mensagem,
            system_instruction=system_instruction,
            historico_dialogo=historico_dicts,
            temperatura=0.2,
        )
    except Exception as err:
        logger.warning(f"Fallback no chat socrático devido a erro na API de IA: {err}")
        # Resposta pedagógica de fallback conforme especificação da Etapa 6
        if payload.trecho_selecionado:
            resposta_texto = (
                f"Estou organizando minhas anotações sobre a expressão selecionada ${payload.trecho_selecionado}$.\n\n"
                f"Enquanto isso, observe o que acontece com as restrições de domínio quando aplicamos a definição "
                f"formal do capítulo **{capitulo.titulo}**. Qual o primeiro passo que você já tentou?"
            )
        else:
            resposta_texto = (
                f"Neste momento estou organizando meus cadernos de anotações da coleção Iezzi.\n\n"
                f"Para sua dúvida sobre \"{payload.mensagem}\" em **{capitulo.titulo}**, revise os conceitos e teoremas "
                f"apresentados no **Bloco 1 (Teoria)**. Se precisar, reformule sua pergunta com uma fórmula específica!"
            )

    return ChatAulaResponse(
        resposta_katex=resposta_texto,
        chunks_utilizados=chunks,
        nivel_ajuda_socratico=estagio_ajuda,
    )


@router.post("/aulas/{capitulo_id}/pista", response_model=SolicitarPistaResponse, summary="Solicitação de Pista Cirúrgica (Estágio 2)")
async def obter_pista(
    capitulo_id: UUID,
    payload: SolicitarPistaRequest,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    RN-CNT-012: Fornece pista contextual de Estágio 2 apontando a propriedade matemática
    do Iezzi aplicável sem entregar a resposta final.
    """
    stmt = (
        select(Capitulo)
        .options(selectinload(Capitulo.volume))
        .where(Capitulo.id == capitulo_id)
    )
    res = await db.execute(stmt)
    capitulo = res.scalar_one_or_none()

    num_cap = capitulo.numero_capitulo if capitulo else 1

    # RN-CNT-012: a pista é um atalho direto ao Estágio 2 — sincroniza a FSM
    # socrática persistida para que o chat subsequente já parta do nível 2.
    if capitulo:
        try:
            redis_pista = get_redis()
            await redis_pista.set(
                f"socratico:{usuario.id}:{capitulo_id}",
                "2|",
                ex=86400,
            )
        except Exception as e:
            logger.warning(f"Erro ao sincronizar estágio socrático após pista: {e}")

    # Pistas cirúrgicas canônicas por assunto do Volume 1
    pistas_por_cap = {
        1: (
            r"Lembre-se da equivalência lógica fundamental: $\sim (p \to q) \equiv p \land \sim q$.",
            "Atenção: a negação de uma condicional NÃO é outra condicional, mas sim uma conjunção!",
        ),
        2: (
            r"Aplique as Leis de De Morgan: $\overline{A \cup B} = \overline{A} \cap \overline{B}$ e $\overline{A \cap B} = \overline{A} \cup \overline{B}$.",
            r"Cuidado ao diferenciar pertinência ($\in$) entre elemento e conjunto de inclusão ($\subset$) entre dois conjuntos.",
        ),
        3: (
            r"Para ser função, todo elemento do domínio deve ter uma e apenas uma imagem: $(\forall x \in A)(\exists! y \in B)$.",
            "No plano cartesiano, utilize o teste da reta vertical para conferir se há múltiplos valores de $y$.",
        ),
        4: (
            r"Imponha as duas restrições fundamentais: denominadores não-nulos ($h(x) \neq 0$) e radicandos de raízes pares não-negativos ($g(x) \ge 0$).",
            "Lembre-se de fazer a interseção das restrições para obter o domínio final $D(f)$.",
        ),
        5: (
            r"A taxa de variação é constante: $a = \frac{\Delta y}{\Delta x}$. A raiz ocorre quando $f(x) = 0 \iff x = -\frac{b}{a}$.",
            "Atenção ao sinal do coeficiente angular $a$: se $a < 0$, a função é estritamente decrescente.",
        ),
        6: (
            r"O vértice da parábola fornece o ponto extremo: $x_v = -\frac{b}{2a}$ e $y_v = -\frac{\Delta}{4a}$.",
            "Atenção ao sinal de $a$: se $a > 0$, o vértice é ponto de MÍNIMO; se $a < 0$, é ponto de MÁXIMO.",
        ),
    }

    pista_katex, dica = pistas_por_cap.get(
        num_cap,
        (
            r"Verifique a definição formal no Bloco 1 e isole a incógnita passo a passo.",
            "Atenção aos sinais ao transpor termos entre os membros da equação.",
        ),
    )

    return SolicitarPistaResponse(
        pista_socratica_katex=pista_katex,
        dica_pegadinha=dica,
    )
