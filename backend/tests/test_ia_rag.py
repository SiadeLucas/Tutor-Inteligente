"""
Bateria de Testes Automatizados — Motor de IA, RAG e Tutor Socrático (Etapa 6).
Valida a LLMFactory, Máquina de Estados Socrática (FSM), busca semântica em pgvector
particionada por volume_id, rate limiting no Redis e resiliência a falhas da API externa.
"""
from uuid import uuid4
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from sqlalchemy import select

from app.core.config import settings
from app.ai.llm_factory import LLMFactory, GeminiLLMService, OpenAILLMService, BaseLLMService
from app.ai.socratic_state import SocraticStateManager
from app.ai.rag_engine import RAGEngine
from app.models.content import VolumeDidatico, Capitulo, DocumentoVetorialRAG


async def autenticar(async_client: AsyncClient, usuario_teste: dict) -> dict:
    """Realiza login e retorna o header Authorization com Bearer token."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "identificador": usuario_teste["email"],
            "senha": usuario_teste["senha_plana"],
        },
    )
    assert response.status_code == 200, f"Login falhou: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def obter_cap1_id(async_client: AsyncClient, headers: dict) -> str:
    """Helper: retorna o ID do primeiro capítulo do Volume 1."""
    tree_res = await async_client.get(
        "/api/v1/conteudo/skill-tree?disciplina_slug=matematica",
        headers=headers,
    )
    assert tree_res.status_code == 200
    return tree_res.json()[0]["capitulos"][0]["id"]


# ============================================================================
# 1. Testes da LLMFactory
# ============================================================================

def test_llm_factory_gemini_provider():
    """Verifica se a fábrica instancia GeminiLLMService por padrão no MVP."""
    with patch.object(settings, "LLM_PROVIDER", "gemini"):
        provedor = LLMFactory.obter_provedor()
        assert isinstance(provedor, GeminiLLMService)
        assert isinstance(provedor, BaseLLMService)


def test_llm_factory_openai_provider():
    """Verifica se a fábrica instancia OpenAILLMService para expansão comercial."""
    with patch.object(settings, "LLM_PROVIDER", "openai"):
        provedor = LLMFactory.obter_provedor()
        assert isinstance(provedor, OpenAILLMService)
        assert isinstance(provedor, BaseLLMService)


def test_llm_factory_provedor_invalido():
    """Verifica se a fábrica rejeita provedores não suportados com ValueError."""
    with patch.object(settings, "LLM_PROVIDER", "claude_invalido"):
        with pytest.raises(ValueError, match="não suportado"):
            LLMFactory.obter_provedor()


# ============================================================================
# 2. Testes da Máquina de Estados Socrática (FSM)
# ============================================================================

def test_socratic_state_progression():
    """Valida progressão pelos 3 estágios socráticos conforme o aluno pede ajuda."""
    # Estágio inicial
    assert SocraticStateManager.determinar_proximo_estagio(0) == 1
    assert SocraticStateManager.determinar_proximo_estagio(1, mensagem_aluno="qual o valor de x?") == 1

    # Aluno pede dica / expressa dificuldade -> avança para Nível 2
    assert SocraticStateManager.determinar_proximo_estagio(1, mensagem_aluno="não entendi como começar") == 2
    assert SocraticStateManager.determinar_proximo_estagio(1, mensagem_aluno="me dá uma dica por favor") == 2
    assert SocraticStateManager.determinar_proximo_estagio(1, mensagem_aluno="travei aqui") == 2

    # Aluno continua com dúvida -> avança para Nível 3 (Passo Guiado)
    assert SocraticStateManager.determinar_proximo_estagio(2, mensagem_aluno="continua explicando o passo") == 3

    # Trava no Nível 3 (não ultrapassa 3)
    assert SocraticStateManager.determinar_proximo_estagio(3, mensagem_aluno="socorro ainda não entendi") == 3


def test_socratic_state_reset_on_topic_change():
    """Valida reinício para Nível 1 quando o aluno troca de tópico ou seleciona nova fórmula."""
    estagio_reset = SocraticStateManager.determinar_proximo_estagio(
        estagio_atual=3,
        topico_atual=r"f(x) = ax + b",
        ultimo_topico_registrado=r"\Delta = b^2 - 4ac",
        mensagem_aluno="não entendi",
    )
    assert estagio_reset == 1


@pytest.mark.asyncio
async def test_chat_estado_socratico_persistido_no_redis(async_client: AsyncClient, usuario_teste):
    """
    Etapa 6: a FSM socrática deve ser persistida por (usuário, capítulo) no Redis.
    1º contato inicializa no Nível 1 (pergunta guia); a 2ª mensagem no MESMO tópico
    parte do estado salvo no Redis e avança para Nível 2 — mesmo com histórico
    vazio, provando que o estágio não regride nem reinicia entre requisições.
    """
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    with patch("app.ai.llm_factory.GeminiLLMService.gerar_resposta", AsyncMock(return_value="Ok $x$")), \
         patch("app.ai.llm_factory.GeminiLLMService.gerar_embedding", AsyncMock(return_value=[0.0] * 768)):
        # 1ª mensagem: primeiro contato no tópico -> inicializa no Nível 1
        r1 = await async_client.post(
            f"/api/v1/conteudo/aulas/{cap1_id}/chat",
            json={"capitulo_id": cap1_id, "mensagem": "Não entendi nada", "historico_recente": []},
            headers=headers,
        )
        assert r1.status_code == 200
        assert r1.json()["nivel_ajuda_socratico"] == 1

        # 2ª mensagem: histórico vazio de propósito — o estágio (1) deve vir do
        # Redis e avançar para 2 pela expressão de dificuldade no mesmo tópico.
        r2 = await async_client.post(
            f"/api/v1/conteudo/aulas/{cap1_id}/chat",
            json={"capitulo_id": cap1_id, "mensagem": "continua, ainda travei", "historico_recente": []},
            headers=headers,
        )
        assert r2.status_code == 200
        assert r2.json()["nivel_ajuda_socratico"] == 2


# ============================================================================
# 3. Testes do Motor RAG com pgvector
# ============================================================================

@pytest.mark.asyncio
async def test_rag_engine_busca_e_particionamento(db_session):
    """
    Verifica se o RAGEngine executa a busca vetorial respeitando
    rigorosamente a partição por volume_id.

    O documento de teste é removido ao final para não poluir o corpus
    canônico do pgvector (fonte real de contexto do tutor Iezzi).
    """
    # 1. Recupera o Volume 1 e cria vetor de teste
    res = await db_session.execute(select(VolumeDidatico).where(VolumeDidatico.numero_volume == 1))
    vol1 = res.scalar_one_or_none()
    assert vol1 is not None

    vetor_teste = [0.01] * 768

    # Insere um documento de teste associado ao Volume 1
    doc_teste = DocumentoVetorialRAG(
        id=uuid4(),
        volume_id=vol1.id,
        trecho_conteudo="Definição formal de função bijetora segundo Gelson Iezzi no Volume 1.",
        metadados={"pagina": 42, "teorema": "Função Bijetora"},
        embedding=vetor_teste,
    )
    db_session.add(doc_teste)
    await db_session.commit()

    try:
        # 2. Executa busca com mock do gerador de embedding
        with patch("app.ai.llm_factory.GeminiLLMService.gerar_embedding", AsyncMock(return_value=vetor_teste)):
            chunks_vol1 = await RAGEngine.buscar_trechos_relevantes(
                db=db_session,
                volume_id=vol1.id,
                query_aluno="O que é função bijetora?",
                limite_chunks=3,
                threshold_similaridade=0.10,
            )
            assert len(chunks_vol1) >= 1
            assert "bijetora" in chunks_vol1[0].trecho.lower()
            assert chunks_vol1[0].pagina == 42
            assert chunks_vol1[0].teorema_ou_topico == "Função Bijetora"

            # 3. Particionamento estrito: buscando com outro volume_id aleatório não deve retornar o chunk do Vol 1
            outro_vol_id = uuid4()
            chunks_outro = await RAGEngine.buscar_trechos_relevantes(
                db=db_session,
                volume_id=outro_vol_id,
                query_aluno="O que é função bijetora?",
                limite_chunks=3,
                threshold_similaridade=0.10,
            )
            assert len(chunks_outro) == 0
    finally:
        # Limpeza garantida: o corpus RAG canônico nunca deve acumular dados de teste
        await db_session.delete(doc_teste)
        await db_session.commit()


# ============================================================================
# 4. Endpoints de Chat Socrático e Pista Cirúrgica
# ============================================================================

@pytest.mark.asyncio
async def test_chat_socratico_com_resposta_katex(async_client: AsyncClient, usuario_teste):
    """Verifica resposta do endpoint de chat com mediação socrática em KaTeX."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    resposta_mock = "Para analisar a proposição, observe a tabela-verdade: $p \\land q$. Qual o valor de $p$?"

    with patch("app.ai.llm_factory.GeminiLLMService.gerar_resposta", AsyncMock(return_value=resposta_mock)), \
         patch("app.ai.llm_factory.GeminiLLMService.gerar_embedding", AsyncMock(return_value=[0.0] * 768)):

        response = await async_client.post(
            f"/api/v1/conteudo/aulas/{cap1_id}/chat",
            json={
                "capitulo_id": cap1_id,
                "mensagem": "Não entendi a conjunção lógica",
                "trecho_selecionado": r"p \land q",
                "historico_recente": [],
            },
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["resposta_katex"] == resposta_mock
        assert "$" in data["resposta_katex"]
        assert data["nivel_ajuda_socratico"] in (1, 2, 3)


@pytest.mark.asyncio
async def test_chat_socratico_fallback_resiliente(async_client: AsyncClient, usuario_teste):
    """
    Verifica se o backend lida com falhas da API externa da IA
    sem retornar erro 500, devolvendo mensagem de fallback acolhedora.
    """
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # Simula erro de cota ou conexão na API externa
    with patch("app.ai.llm_factory.GeminiLLMService.gerar_resposta", AsyncMock(side_effect=Exception("Google Quota Exceeded"))), \
         patch("app.ai.llm_factory.GeminiLLMService.gerar_embedding", AsyncMock(side_effect=Exception("API Timeout"))):

        response = await async_client.post(
            f"/api/v1/conteudo/aulas/{cap1_id}/chat",
            json={
                "capitulo_id": cap1_id,
                "mensagem": "Qual a fórmula de Bhaskara?",
            },
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "organizando meus cadernos" in data["resposta_katex"]
        assert data["chunks_utilizados"] == []


@pytest.mark.asyncio
async def test_chat_rate_limiting_redis(async_client: AsyncClient, usuario_teste):
    """Valida o rate limit pedagógico de 30 mensagens por sessão/capítulo."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    # Simula Redis retornando contagem 31 (limite ultrapassado)
    with patch("app.core.redis.aioredis.Redis.incr", AsyncMock(return_value=31)):
        response = await async_client.post(
            f"/api/v1/conteudo/aulas/{cap1_id}/chat",
            json={
                "capitulo_id": cap1_id,
                "mensagem": "Mais uma pergunta",
            },
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "limite pedagógico de 30 mensagens" in data["resposta_katex"]
        assert "Fixação" in data["resposta_katex"]


@pytest.mark.asyncio
async def test_pista_cirurgica_estagio_2(async_client: AsyncClient, usuario_teste):
    """Verifica se o endpoint de pista cirúrgica retorna fórmula KaTeX e dica contextual."""
    headers = await autenticar(async_client, usuario_teste)
    cap1_id = await obter_cap1_id(async_client, headers)

    response = await async_client.post(
        f"/api/v1/conteudo/aulas/{cap1_id}/pista",
        json={"capitulo_id": cap1_id},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "pista_socratica_katex" in data
    assert "$" in data["pista_socratica_katex"]
    assert "dica_pegadinha" in data
