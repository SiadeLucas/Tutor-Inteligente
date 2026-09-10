"""
Camada de Serviços do Módulo de Exercícios e Motor Psicométrico CAT.
Implementa lógica de 2ª chance, cálculo Bayesiano EAP, MFI e geração determinística de Questões Gêmeas.
"""
import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import select, and_, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.exercise import ItemExercicio, TentativaExercicio, CaixaReforco, ProvaCat
from app.models.content import Capitulo, VolumeDidatico, Disciplina
from app.models.user import Usuario
from app.sympy_engine.validator import SympyMathValidator
from app.cat_engine.cat_service import CatEngine, ItemTRI
from app.ai.llm_factory import LLMFactory
from app.modules.exercises.schemas import (
    SubmissaoExercicioRequest,
    SubmissaoExercicioResponse,
    IniciarCatRequest,
    IniciarCatResponse,
    SubmeterCatRequest,
    CatStatusResponse,
    ItemExercicioResponse,
    AlternativaItem,
)


class ExercisesService:
    """Orquestrador das regras de negócio de exercícios e do Motor CAT."""

    cat_engine = CatEngine()

    @classmethod
    async def submeter_exercicio(
        cls,
        payload: SubmissaoExercicioRequest,
        current_user: Usuario,
        db: AsyncSession,
    ) -> SubmissaoExercicioResponse:
        """
        Submissão com dinâmica de 2ª chance (RN-EXE-008):
        - 1ª tentativa: acerto = 1.0; erro = concede 2ª chance com pista socrática.
        - 2ª tentativa: acerto = 0.5; erro = pontuação 0.0, arquiva na Caixa de Reforço e libera Questão Gêmea.
        """
        item = await db.get(ItemExercicio, payload.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de exercício não localizado.")

        # RN-EXE-008: o número real da tentativa é autoritativo no SERVIDOR (contagem de
        # registros desta dupla usuário+item). O campo `tentativa_numero` do payload é
        # apenas um hint opcional; nunca define pontuação nem libera 2ª chance. Isso
        # impede o aluno de forjar "tentativa 1" repetidas vezes (pontuação infinita de 1.0)
        # e previne vazamento da régua acerto/erro da Prova CAT (RN-EXE-006.1 / RN-EXE-010).
        stmt_tentativas = (
            select(TentativaExercicio)
            .where(
                and_(
                    TentativaExercicio.usuario_id == current_user.id,
                    TentativaExercicio.item_id == item.id,
                )
            )
            .order_by(TentativaExercicio.criado_em.asc())
        )
        tentativas_anteriores = (await db.execute(stmt_tentativas)).scalars().all()
        tentativa_numero = len(tentativas_anteriores) + 1

        if tentativa_numero > 2:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tentativas esgotadas para este item. Pratique com uma Questão Gêmea ou revise a Caixa de Reforço.",
            )

        # Validação do gabarito (múltipla escolha vs numérico via SymPy)
        tipo_item = payload.tipo_item or item.tipo_item
        resposta_limpa = payload.resposta_enviada.strip()

        if tipo_item == "numeric_input":
            acertou = SympyMathValidator.validar_equivalencia(
                expressao_aluno_str=resposta_limpa,
                expressao_gabarito_str=item.resposta_correta,
            )
        else:
            acertou = (resposta_limpa.upper() == item.resposta_correta.strip().upper())

        # Cálculo da pontuação conforme o número REAL de tentativas (1.0 vs 0.5 vs 0.0)
        if acertou:
            pontuacao = 1.0 if tentativa_numero == 1 else 0.5
            tentativa = TentativaExercicio(
                usuario_id=current_user.id,
                item_id=item.id,
                capitulo_id=item.capitulo_id,
                tentativa_numero=tentativa_numero,
                resposta_enviada=resposta_limpa,
                acertou=True,
                pontuacao_obtida=pontuacao,
                usou_dica_ia=(tentativa_numero == 2),
                tempo_resposta_segundos=payload.tempo_resposta_segundos,
            )
            db.add(tentativa)

            # RN-EXE-008.1: acertar a Questão Gêmea valida a superação da dúvida e
            # marca o item matriz original como 'superado' na Caixa de Reforço.
            if item.tipo_origem == "gemea_ia" and item.item_matriz_id:
                stmt_superar = (
                    update(CaixaReforco)
                    .where(
                        and_(
                            CaixaReforco.usuario_id == current_user.id,
                            CaixaReforco.item_id == item.item_matriz_id,
                            CaixaReforco.status == "pendente",
                        )
                    )
                    .values(status="superado", superado_em=func.now())
                )
                await db.execute(stmt_superar)

            # Atualiza micro-ajuste psicométrico e Heatmap de Domínio (RN-PRG-006 / RN-PRG-020)
            await cls._atualizar_progresso_exercicio(db, current_user, item, pontuacao)

            await db.commit()

            return SubmissaoExercicioResponse(
                acertou=True,
                pontuacao_obtida=pontuacao,
                permite_segunda_chance=False,
                pista_socratica_ia=None,
                resolucao_completa_katex=item.resolucao_passo_a_passo,
                pode_gerar_gemea=False,
                resposta_correta=item.resposta_correta,
            )
        else:
            # Errou
            if tentativa_numero == 1:
                # 1ª Tentativa Errada: concede 2ª chance com pista socrática
                tentativa = TentativaExercicio(
                    usuario_id=current_user.id,
                    item_id=item.id,
                    capitulo_id=item.capitulo_id,
                    tentativa_numero=1,
                    resposta_enviada=resposta_limpa,
                    acertou=False,
                    pontuacao_obtida=0.0,
                    usou_dica_ia=False,
                    tempo_resposta_segundos=payload.tempo_resposta_segundos,
                )
                db.add(tentativa)

                # Atualiza métricas parciais de tentativa no heatmap
                await cls._atualizar_progresso_exercicio(db, current_user, item, 0.0)

                await db.commit()

                pista = await cls._obter_pista_socratica(item, resposta_limpa)

                return SubmissaoExercicioResponse(
                    acertou=False,
                    pontuacao_obtida=0.0,
                    permite_segunda_chance=True,
                    pista_socratica_ia=pista,
                    resolucao_completa_katex=None,
                    pode_gerar_gemea=False,
                    resposta_correta=None,
                )
            else:
                # 2ª Tentativa Errada: erro duplo (RN-EXE-008.1)
                tentativa = TentativaExercicio(
                    usuario_id=current_user.id,
                    item_id=item.id,
                    capitulo_id=item.capitulo_id,
                    tentativa_numero=2,
                    resposta_enviada=resposta_limpa,
                    acertou=False,
                    pontuacao_obtida=0.0,
                    usou_dica_ia=True,
                    tempo_resposta_segundos=payload.tempo_resposta_segundos,
                )
                db.add(tentativa)

                # Arquiva na Caixa de Reforço
                stmt_cr = select(CaixaReforco).where(
                    and_(
                        CaixaReforco.usuario_id == current_user.id,
                        CaixaReforco.item_id == item.id,
                        CaixaReforco.status == "pendente",
                    )
                )
                cr_existente = (await db.execute(stmt_cr)).scalar_one_or_none()
                if cr_existente:
                    cr_existente.total_erros += 1
                else:
                    novo_reforco = CaixaReforco(
                        usuario_id=current_user.id,
                        item_id=item.id,
                        capitulo_id=item.capitulo_id,
                        total_erros=1,
                        status="pendente",
                    )
                    db.add(novo_reforco)

                # Atualiza micro-ajuste com pontuação 0.0 e Heatmap (RN-PRG-006 / RN-PRG-020)
                await cls._atualizar_progresso_exercicio(db, current_user, item, 0.0)

                await db.commit()

                return SubmissaoExercicioResponse(
                    acertou=False,
                    pontuacao_obtida=0.0,
                    permite_segunda_chance=False,
                    pista_socratica_ia=None,
                    resolucao_completa_katex=item.resolucao_passo_a_passo,
                    pode_gerar_gemea=True,
                    resposta_correta=item.resposta_correta,
                )

    @classmethod
    async def _obter_pista_socratica(cls, item: ItemExercicio, resposta_aluno: str) -> str:
        """Recupera dica pré-configurada ou gera via LLM Socrático."""
        if item.metadados_sympy and isinstance(item.metadados_sympy, dict):
            dica_salva = item.metadados_sympy.get("dica_estagio_2")
            if dica_salva:
                return str(dica_salva)

        # Fallback dinâmico com Gemini Flash
        try:
            llm = LLMFactory.obter_provedor()
            system_prompt = (
                "Você é o Tutor Socrático de Matemática do Ensino Médio. "
                "O aluno tentou resolver a seguinte questão e errou. "
                "Dê uma pista conceitual curta (1 ou 2 frases) para orientá-lo sem dar a resposta ou o gabarito. "
                "Use fórmulas KaTeX delimitadas por $...$ quando necessário."
            )
            prompt_usuario = (
                f"Enunciado: {item.enunciado_katex}\n"
                f"Resposta incorreta do aluno: {resposta_aluno}\n"
                f"Resolução de referência: {item.resolucao_passo_a_passo}"
            )
            resposta_ia = await llm.gerar_resposta(
                prompt_usuario=prompt_usuario,
                system_instruction=system_prompt,
                historico_dialogo=[],
                temperatura=0.2,
            )
            return resposta_ia.strip()
        except Exception:
            return "Revise os conceitos fundamentais do capítulo e atente-se aos cálculos intermediários antes da 2ª tentativa."

    @classmethod
    async def gerar_questao_gemea(
        cls,
        item_matriz_id: uuid.UUID,
        current_user: Usuario,
        db: AsyncSession,
    ) -> ItemExercicioResponse:
        """
        Gera uma variação determinística do item matriz via SymPy,
        garantindo equivalência conceitual e tolerância exata (±0.01).
        """
        item_matriz = await db.get(ItemExercicio, item_matriz_id)
        if not item_matriz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item matriz não localizado.")

        # Mutação paramétrica quadrática determinística
        r1, r2 = 2, 3
        if item_matriz.metadados_sympy and isinstance(item_matriz.metadados_sympy, dict):
            raizes = item_matriz.metadados_sympy.get("raizes", [2, 3])
            if len(raizes) >= 2:
                r1, r2 = int(raizes[0]), int(raizes[1])

        dados_gemea = SympyMathValidator.gerar_questao_gemea_quadratica(r1_original=r1, r2_original=r2)

        # A geração paramétrica SymPy sempre produz múltipla escolha (5 alternativas com
        # distratores estruturados e gabarito em letra). Um item matriz numeric_input NÃO
        # pode transmitir seu tipo: a correção SymPy compararia a expressão do aluno com
        # a LETRA do gabarito e o item seria insolúvel (sempre falso).
        tipo_item_gemea = "multiple_choice"

        # Persiste a questão gêmea herdando os parâmetros TRI (RN-EXE-015)
        nova_gemea = ItemExercicio(
            id=uuid.uuid4(),
            capitulo_id=item_matriz.capitulo_id,
            tipo_origem="gemea_ia",
            tipo_item=tipo_item_gemea,
            item_matriz_id=item_matriz.id,
            enunciado_katex=dados_gemea["enunciado_katex"],
            alternativas=dados_gemea["alternativas"],
            resposta_correta=dados_gemea["resposta_correta"],
            resolucao_passo_a_passo=dados_gemea["resolucao_passo_a_passo"],
            parametro_a=item_matriz.parametro_a,
            parametro_b=item_matriz.parametro_b,
            parametro_c=item_matriz.parametro_c,
            metadados_sympy=dados_gemea["metadados_sympy"],
            validado_sympy=True,
            ativo=True,
        )
        db.add(nova_gemea)
        await db.commit()
        await db.refresh(nova_gemea)

        alternativas_dto = [
            AlternativaItem(letra=alt["letra"], texto_katex=alt["texto"])
            for alt in (nova_gemea.alternativas or [])
        ]

        return ItemExercicioResponse(
            id=nova_gemea.id,
            capitulo_id=nova_gemea.capitulo_id,
            tipo_origem="gemea_ia",
            tipo_item=nova_gemea.tipo_item,
            item_matriz_id=item_matriz.id,
            enunciado_katex=nova_gemea.enunciado_katex,
            alternativas=alternativas_dto,
            parametro_a=float(nova_gemea.parametro_a),
            parametro_b=float(nova_gemea.parametro_b),
            parametro_c=float(nova_gemea.parametro_c),
            validado_sympy=nova_gemea.validado_sympy,
            criado_em=nova_gemea.criado_em,
        )

    @classmethod
    async def iniciar_sessao_cat(
        cls,
        payload: IniciarCatRequest,
        current_user: Usuario,
        db: AsyncSession,
    ) -> IniciarCatResponse:
        """
        Instancia uma nova sessão CAT com prior N(0, 1), SE = 1.0
        e seleciona o 1º item por máxima Informação de Fisher (MFI).
        """
        # Carrega itens do banco vinculados à disciplina
        stmt_itens = (
            select(ItemExercicio)
            .join(Capitulo, ItemExercicio.capitulo_id == Capitulo.id)
            .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
            .where(
                and_(
                    VolumeDidatico.disciplina_id == payload.disciplina_id,
                    ItemExercicio.ativo == True,
                )
            )
        )
        itens_db = (await db.execute(stmt_itens)).scalars().all()

        # Fallback: se não houver itens vinculados à disciplina específica, busca todos ativos
        if not itens_db:
            stmt_fallback = select(ItemExercicio).where(ItemExercicio.ativo == True)
            itens_db = (await db.execute(stmt_fallback)).scalars().all()

        if not itens_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Banco de itens indisponível para iniciar o CAT.",
            )

        # Mapeia para objetos ItemTRI
        banco_tri = [
            ItemTRI(
                id=str(it.id),
                a=float(it.parametro_a),
                b=float(it.parametro_b),
                c=float(it.parametro_c),
                grande_area=(it.metadados_sympy.get("grande_area", "algebra_funcoes") if it.metadados_sympy else "algebra_funcoes"),
            )
            for it in itens_db
        ]

        # Seleciona o 1º item com prior theta=0.0
        primeiro_tri = cls.cat_engine.selecionar_proximo_item(
            theta_atual=0.0,
            banco_disponivel=banco_tri,
            itens_ja_aplicados_ids=[],
        )

        item_escolhido = next(it for it in itens_db if str(it.id) == primeiro_tri.id)

        # Integridade de sessão: apenas 1 prova em andamento por aluno/disciplina.
        # Reabrir o onboarding do zero reiniciaria o MFI a partir de theta=0,
        # invalidando a calibragem adaptativa já atingida.
        stmt_sessao_ativa = select(ProvaCat).where(
            and_(
                ProvaCat.usuario_id == current_user.id,
                ProvaCat.disciplina_id == payload.disciplina_id,
                ProvaCat.finalizado_em.is_(None),
            )
        )
        sessao_ativa = (await db.execute(stmt_sessao_ativa)).scalar_one_or_none()
        if sessao_ativa:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Você já possui uma prova CAT em andamento para esta disciplina. Conclua a sessão atual antes de iniciar outra.",
            )

        # Cria a sessão ProvaCat
        sessao_cat = ProvaCat(
            usuario_id=current_user.id,
            disciplina_id=payload.disciplina_id,
            tipo_prova=payload.tipo_prova,
            theta_geral=0.000,
            erro_padrao_se=1.000,
            scores_grandes_areas={},
            total_itens_aplicados=0,
            itens_respondidos_ids=[],
            respostas_detalhadas=[],
        )
        db.add(sessao_cat)
        await db.commit()
        await db.refresh(sessao_cat)

        alternativas_dto = [
            AlternativaItem(letra=alt["letra"], texto_katex=alt["texto"])
            for alt in (item_escolhido.alternativas or [])
        ]

        primeiro_item_dto = ItemExercicioResponse(
            id=item_escolhido.id,
            capitulo_id=item_escolhido.capitulo_id,
            tipo_origem=item_escolhido.tipo_origem,
            tipo_item=item_escolhido.tipo_item,
            enunciado_katex=item_escolhido.enunciado_katex,
            alternativas=alternativas_dto,
            parametro_a=float(item_escolhido.parametro_a),
            parametro_b=float(item_escolhido.parametro_b),
            parametro_c=float(item_escolhido.parametro_c),
            validado_sympy=item_escolhido.validado_sympy,
            criado_em=item_escolhido.criado_em,
        )

        return IniciarCatResponse(
            sessao_cat_id=sessao_cat.id,
            indicador_progresso="Questão 1 (Faixa: 12 a 20 questões)",
            total_itens_estimado="12 a 20 questões",
            primeiro_item=primeiro_item_dto,
        )

    @classmethod
    async def submeter_resposta_cat(
        cls,
        payload: SubmeterCatRequest,
        current_user: Usuario,
        db: AsyncSession,
    ) -> CatStatusResponse:
        """
        Submissão cega da Prova CAT (RN-EXE-010):
        Sem feedback visual de acerto/erro, com atualização iterativa do theta EAP.
        """
        prova = await db.get(ProvaCat, payload.sessao_cat_id)
        if not prova or prova.usuario_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão CAT não localizada.")

        if prova.finalizado_em is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta sessão CAT já foi concluída.")

        # Integridade da prova (anti-replay): cada item só pode ser respondido uma vez
        # por sessão. O próximo item é sempre entregue pelo servidor na resposta anterior,
        # portanto reenviar um item já respondido só faz sentido em sondagem do motor.
        ids_respondidos = {str(i) for i in (prova.itens_respondidos_ids or [])}
        if str(payload.item_id) in ids_respondidos:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este item já foi respondido nesta sessão CAT.",
            )

        item = await db.get(ItemExercicio, payload.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não localizado.")

        # Valida acerto
        resposta_limpa = payload.resposta_enviada.strip()
        if item.tipo_item == "numeric_input":
            acertou = SympyMathValidator.validar_equivalencia(resposta_limpa, item.resposta_correta)
        else:
            acertou = (resposta_limpa.upper() == item.resposta_correta.strip().upper())

        # Atualiza histórico detalhado e IDs respondidos
        itens_ids = list(prova.itens_respondidos_ids or [])
        itens_ids.append(str(item.id))
        prova.itens_respondidos_ids = itens_ids

        respostas_lista = list(prova.respostas_detalhadas or [])
        respostas_lista.append({
            "item_id": str(item.id),
            "acertou": acertou,
            "resposta": resposta_limpa,
            "tempo_segundos": payload.tempo_resposta_segundos,
            "parametro_a": float(item.parametro_a),
            "parametro_b": float(item.parametro_b),
            "parametro_c": float(item.parametro_c),
            "grande_area": (item.metadados_sympy.get("grande_area", "algebra_funcoes") if item.metadados_sympy else "algebra_funcoes"),
        })
        prova.respostas_detalhadas = respostas_lista
        prova.total_itens_aplicados += 1

        # Recomputa Theta e SE com estimador EAP Bayesiano
        historico_eap: List[Tuple[ItemTRI, int]] = []
        for r in respostas_lista:
            item_tri = ItemTRI(
                id=r["item_id"],
                a=r["parametro_a"],
                b=r["parametro_b"],
                c=r["parametro_c"],
                grande_area=r.get("grande_area", "algebra_funcoes"),
            )
            historico_eap.append((item_tri, 1 if r["acertou"] else 0))

        novo_theta, novo_se = cls.cat_engine.estimar_theta_eap(historico_eap)
        prova.theta_geral = round(float(novo_theta), 3)
        prova.erro_padrao_se = round(float(novo_se), 3)

        # Critério de parada: N >= 12 e SE <= 0.30, ou N = 20
        encerrar = cls.cat_engine.deve_encerrar_teste(
            total_itens_aplicados=prova.total_itens_aplicados,
            erro_padrao=float(prova.erro_padrao_se),
        )

        if encerrar:
            prova.finalizado_em = func.now()
            scores_radar = cls.cat_engine.calcular_scores_grandes_areas(historico_eap, float(prova.theta_geral))
            prova.scores_grandes_areas = scores_radar
            await cls._registrar_historico_cat(db, prova, scores_radar)
            await db.commit()

            classificacao = (
                "Básico" if prova.theta_geral < -0.5
                else "Intermediário" if prova.theta_geral <= 1.0
                else "Avançado"
            )

            return CatStatusResponse(
                sessao_id=prova.id,
                finalizado=True,
                indicador_progresso=f"Concluído ({prova.total_itens_aplicados} itens respondidos)",
                proximo_item=None,
                theta_final=float(prova.theta_geral),
                erro_padrao=float(prova.erro_padrao_se),
                classificacao=classificacao,
                total_questoes_respondidas=prova.total_itens_aplicados,
                scores_grandes_areas=scores_radar,
                redirecionar_url="/materias",
                mensagem="Prova Diagnóstica CAT concluída com sucesso!",
            )
        else:
            # Seleciona o próximo item MFI
            stmt_todos = select(ItemExercicio).where(ItemExercicio.ativo == True)
            todos_itens = (await db.execute(stmt_todos)).scalars().all()
            banco_tri = [
                ItemTRI(
                    id=str(it.id),
                    a=float(it.parametro_a),
                    b=float(it.parametro_b),
                    c=float(it.parametro_c),
                    grande_area=(it.metadados_sympy.get("grande_area", "algebra_funcoes") if it.metadados_sympy else "algebra_funcoes"),
                )
                for it in todos_itens
            ]

            # Política de cobertura balanceada (RN-EXE-006): enquanto alguma Grande
            # Área canônica tiver menos de 2 itens respondidos, a seleção MFI é
            # direcionada à área menos coberta; após a cobertura, MFI global puro.
            area_alvo = cls.cat_engine.selecionar_area_alvo(historico_eap, minimo_por_area=2)

            proximo_tri = cls.cat_engine.selecionar_proximo_item(
                theta_atual=float(prova.theta_geral),
                banco_disponivel=banco_tri,
                itens_ja_aplicados_ids=itens_ids,
                area_alvo=area_alvo,
            )

            if not proximo_tri:
                # Se esgotaram os itens no banco, finaliza antecipadamente
                prova.finalizado_em = func.now()
                scores_radar = cls.cat_engine.calcular_scores_grandes_areas(historico_eap, float(prova.theta_geral))
                prova.scores_grandes_areas = scores_radar
                await cls._registrar_historico_cat(db, prova, scores_radar)
                await db.commit()

                return CatStatusResponse(
                    sessao_id=prova.id,
                    finalizado=True,
                    indicador_progresso=f"Concluído ({prova.total_itens_aplicados} itens)",
                    proximo_item=None,
                    theta_final=float(prova.theta_geral),
                    erro_padrao=float(prova.erro_padrao_se),
                    classificacao="Intermediário",
                    total_questoes_respondidas=prova.total_itens_aplicados,
                    scores_grandes_areas=scores_radar,
                    redirecionar_url="/materias",
                    mensagem="Prova Diagnóstica CAT concluída!",
                )

            await db.commit()
            proximo_db = next(it for it in todos_itens if str(it.id) == proximo_tri.id)

            alternativas_dto = [
                AlternativaItem(letra=alt["letra"], texto_katex=alt["texto"])
                for alt in (proximo_db.alternativas or [])
            ]

            proximo_dto = ItemExercicioResponse(
                id=proximo_db.id,
                capitulo_id=proximo_db.capitulo_id,
                tipo_origem=proximo_db.tipo_origem,
                tipo_item=proximo_db.tipo_item,
                enunciado_katex=proximo_db.enunciado_katex,
                alternativas=alternativas_dto,
                parametro_a=float(proximo_db.parametro_a),
                parametro_b=float(proximo_db.parametro_b),
                parametro_c=float(proximo_db.parametro_c),
                validado_sympy=proximo_db.validado_sympy,
                criado_em=proximo_db.criado_em,
            )

            return CatStatusResponse(
                sessao_id=prova.id,
                finalizado=False,
                indicador_progresso=f"Questão {prova.total_itens_aplicados + 1} (Faixa: 12 a 20 questões)",
                proximo_item=proximo_dto,
                theta_final=float(prova.theta_geral),
                erro_padrao=float(prova.erro_padrao_se),
                classificacao=None,
                total_questoes_respondidas=prova.total_itens_aplicados,
                scores_grandes_areas=None,
                redirecionar_url=None,
                mensagem=None,
            )

    @classmethod
    async def obter_bateria_fixacao(
        cls,
        capitulo_id: uuid.UUID,
        db: AsyncSession,
    ) -> List[ItemExercicioResponse]:
        """
        Retorna de 3 a 5 exercícios do capítulo ordenados pelo parâmetro b (dificuldade).
        Oculta o campo 'correta' das alternativas para evitar inspeção no cliente.
        """
        stmt = (
            select(ItemExercicio)
            .where(and_(ItemExercicio.capitulo_id == capitulo_id, ItemExercicio.ativo == True))
            .order_by(ItemExercicio.parametro_b.asc())
            .limit(5)
        )
        itens = (await db.execute(stmt)).scalars().all()

        resultado = []
        for it in itens:
            alts_limpas = [
                AlternativaItem(letra=alt["letra"], texto_katex=alt["texto"])
                for alt in (it.alternativas or [])
            ]
            resultado.append(
                ItemExercicioResponse(
                    id=it.id,
                    capitulo_id=it.capitulo_id,
                    tipo_origem=it.tipo_origem,
                    tipo_item=it.tipo_item,
                    item_matriz_id=it.item_matriz_id,
                    enunciado_katex=it.enunciado_katex,
                    alternativas=alts_limpas,
                    parametro_a=float(it.parametro_a),
                    parametro_b=float(it.parametro_b),
                    parametro_c=float(it.parametro_c),
                    validado_sympy=it.validado_sympy,
                    criado_em=it.criado_em,
                )
            )
        return resultado

    @classmethod
    async def listar_historico_cat(
        cls,
        current_user: Usuario,
        db: AsyncSession,
    ) -> List[Dict[str, Any]]:
        """
        Lista as provas CAT finalizadas do estudante (mais recente primeiro).
        Suporta o disparo da prova diagnóstica no primeiro acesso a uma matéria (etapa-04)
        e o comparativo de entrada vs. atual do Radar (preparação para a Etapa 8).
        """
        stmt = (
            select(ProvaCat)
            .where(
                and_(
                    ProvaCat.usuario_id == current_user.id,
                    ProvaCat.finalizado_em.isnot(None),
                )
            )
            .order_by(ProvaCat.finalizado_em.desc())
            .limit(10)
        )
        provas = (await db.execute(stmt)).scalars().all()

        return [
            {
                "id": str(p.id),
                "disciplina_id": str(p.disciplina_id),
                "tipo_prova": p.tipo_prova,
                "theta_geral": float(p.theta_geral),
                "erro_padrao_se": float(p.erro_padrao_se),
                "classificacao": (
                    "Básico" if float(p.theta_geral) < -0.5
                    else "Intermediário" if float(p.theta_geral) <= 1.0
                    else "Avançado"
                ),
                "total_itens_aplicados": p.total_itens_aplicados,
                "scores_grandes_areas": p.scores_grandes_areas or {},
                "finalizado_em": p.finalizado_em.isoformat() if p.finalizado_em else None,
            }
            for p in provas
        ]

    @classmethod
    async def listar_caixa_reforco(
        cls,
        current_user: Usuario,
        db: AsyncSession,
    ) -> List[Dict[str, Any]]:
        """Lista os itens pendentes na Caixa de Reforço com erro duplo acumulado."""
        stmt = (
            select(CaixaReforco, ItemExercicio)
            .join(ItemExercicio, CaixaReforco.item_id == ItemExercicio.id)
            .where(
                and_(
                    CaixaReforco.usuario_id == current_user.id,
                    CaixaReforco.status == "pendente",
                )
            )
            .order_by(CaixaReforco.arquivado_em.desc())
        )
        registros = (await db.execute(stmt)).all()

        return [
            {
                "id": str(cr.id),
                "item_id": str(it.id),
                "capitulo_id": str(cr.capitulo_id),
                "enunciado_katex": it.enunciado_katex,
                "total_erros": cr.total_erros,
                "status": cr.status,
                "arquivado_em": cr.arquivado_em.isoformat() if cr.arquivado_em else datetime.utcnow().isoformat(),
            }
            for cr, it in registros
        ]

    @classmethod
    async def _atualizar_progresso_exercicio(
        cls,
        db: AsyncSession,
        current_user: Usuario,
        item: ItemExercicio,
        pontuacao: float,
    ):
        """Atualiza o micro-ajuste estocástico do Theta e o Heatmap (RN-PRG-006 / RN-PRG-020)."""
        try:
            from app.modules.progress.theta_updater import ThetaUpdaterService
            from app.models.progress import HorasEstudoDiarias
            from sqlalchemy.dialects.postgresql import insert as pg_insert
            from datetime import date

            # 1. Busca volume_id e disciplina_id do capítulo
            stmt_cap = (
                select(Capitulo.volume_id, VolumeDidatico.disciplina_id)
                .join(VolumeDidatico, Capitulo.volume_id == VolumeDidatico.id)
                .where(Capitulo.id == item.capitulo_id)
            )
            res_cap = await db.execute(stmt_cap)
            row_cap = res_cap.first()
            vol_id = row_cap[0] if row_cap else None
            disc_id = row_cap[1] if row_cap else None

            if not disc_id:
                stmt_disc = select(Disciplina.id).limit(1)
                disc_id = (await db.execute(stmt_disc)).scalar_one_or_none()

            # 2. Total de questões já respondidas pelo aluno
            stmt_cnt = select(func.count(TentativaExercicio.id)).where(
                TentativaExercicio.usuario_id == current_user.id
            )
            total_respondidas = (await db.execute(stmt_cnt)).scalar() or 0

            # 3. Micro-ajuste estocástico e Heatmap
            if disc_id:
                await ThetaUpdaterService.processar_micro_ajuste_exercicio(
                    db=db,
                    usuario_id=current_user.id,
                    disciplina_id=disc_id,
                    volume_id=vol_id,
                    capitulo_id=item.capitulo_id,
                    item=item,
                    pontuacao_ponderada=pontuacao,
                    total_questoes_respondidas_aluno=total_respondidas,
                )

            # 4. Incrementa contador diário de exercícios submetidos (Tabela 17)
            hoje = date.today()
            stmt_horas = (
                pg_insert(HorasEstudoDiarias)
                .values(
                    id=uuid.uuid4(),
                    usuario_id=current_user.id,
                    data_registro=hoje,
                    segundos_ativos=0,
                    aulas_concluidas=0,
                    exercicios_submetidos=1,
                )
                .on_conflict_do_update(
                    constraint="uk_horas_usuario_data",
                    set_={"exercicios_submetidos": HorasEstudoDiarias.exercicios_submetidos + 1},
                )
            )
            await db.execute(stmt_horas)
        except Exception:
            # Não interrompe a resolução do exercício em caso de erro secundário
            pass

    @classmethod
    async def _registrar_historico_cat(
        cls,
        db: AsyncSession,
        prova: ProvaCat,
        scores_radar: Dict[str, float],
    ):
        """Registra os marcos do CAT em historico_theta (Critério de Aceitação 7 da Etapa 8)."""
        from app.models.progress import HistoricoTheta

        origem = "onboarding_cat" if prova.tipo_prova == "onboarding_diagnostico" else "marco_cat"

        # 1. Registro do Theta Geral
        reg_geral = HistoricoTheta(
            id=uuid.uuid4(),
            usuario_id=prova.usuario_id,
            disciplina_id=prova.disciplina_id,
            volume_id=None,
            grande_area="geral",
            theta_estimado=float(prova.theta_geral),
            erro_padrao_se=float(prova.erro_padrao_se),
            origem_ajuste=origem,
        )
        db.add(reg_geral)

        # 2. Registros por Grande Área para o Radar Comparativo
        if scores_radar:
            for area_slug, score_val in scores_radar.items():
                reg_area = HistoricoTheta(
                    id=uuid.uuid4(),
                    usuario_id=prova.usuario_id,
                    disciplina_id=prova.disciplina_id,
                    volume_id=None,
                    grande_area=area_slug,
                    theta_estimado=float(score_val),
                    erro_padrao_se=float(prova.erro_padrao_se),
                    origem_ajuste=origem,
                )
                db.add(reg_area)

