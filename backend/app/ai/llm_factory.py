"""
Fábrica de LLM Desacoplada (LLMFactory) - Suporte a Gemini Flash e OpenAI.
Conforme especificação em docs-site/docs/modules/conteudo/prototype/llm-factory.md
e docs-site/docs/implementation/etapa-06-ia-rag.md.
"""
from abc import ABC, abstractmethod
import asyncio
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from app.core.config import settings


class BaseLLMService(ABC):
    """Contrato base que qualquer provedor de IA deve satisfazer."""

    @abstractmethod
    async def gerar_resposta(
        self,
        prompt_usuario: str,
        system_instruction: str,
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2,
    ) -> str:
        """Gera uma resposta textual com fórmulas KaTeX delimitadas."""
        pass

    @abstractmethod
    async def gerar_embedding(self, texto: str) -> List[float]:
        """Gera vetor denso de 768 dimensões para indexação ou busca no pgvector."""
        pass


class GeminiLLMService(BaseLLMService):
    """
    Provedor padrão para o MVP da plataforma Tutor Inteligente.
    Utiliza Google Gemini Flash e embeddings do Google AI Studio com dimensão 768.
    """

    def __init__(self):
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.modelo_texto_nome = settings.LLM_MODEL_NAME
        self.modelo_embedding_nome = settings.EMBEDDING_MODEL_NAME

    async def gerar_resposta(
        self,
        prompt_usuario: str,
        system_instruction: str,
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2,
    ) -> str:
        # Formata o histórico recente para a estrutura esperada pelo Gemini.
        # A API exige que o histórico inicie com role 'user' (a instrução de
        # sistema é o primeiro turno efetivo, nunca o do modelo).
        mensagens_chat = []
        for msg in historico_dialogo:
            role = "user" if msg.get("papel") in ("user", "aluno") else "model"
            conteudo = msg.get("conteudo") or msg.get("texto") or ""
            if conteudo.strip():
                mensagens_chat.append({"role": role, "parts": [conteudo]})
        while mensagens_chat and mensagens_chat[0]["role"] != "user":
            mensagens_chat.pop(0)

        # Configura o modelo generativo com system_instruction
        model = genai.GenerativeModel(
            model_name=self.modelo_texto_nome,
            system_instruction=system_instruction,
            generation_config=genai.types.GenerationConfig(
                temperature=temperatura,
                max_output_tokens=1024,
            ),
        )

        def _executar_chat() -> str:
            chat = model.start_chat(history=mensagens_chat)
            resp = chat.send_message(prompt_usuario)
            return resp.text

        # Executa em threadpool assíncrono para não bloquear o event loop
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _executar_chat)

    async def gerar_embedding(self, texto: str, task_type: str = "retrieval_query") -> List[float]:
        """
        Gera vetor de 768 dimensões compatível com pgvector(768).

        task_type: 'retrieval_document' para indexação (ingestão) e
        'retrieval_query' para consultas — pratica recomendada do Google para
        manter os vetores no mesmo espaço semântico.
        """
        def _executar_embedding() -> List[float]:
            modelo = self.modelo_embedding_nome or "models/gemini-embedding-001"
            result = genai.embed_content(
                model=modelo,
                content=texto,
                task_type=task_type,
                output_dimensionality=768,
            )
            emb = result["embedding"]
            if len(emb) > 768:
                return emb[:768]
            if len(emb) < 768:
                return emb + [0.0] * (768 - len(emb))
            return emb

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _executar_embedding)


class OpenAILLMService(BaseLLMService):
    """Provedor plugável para expansão comercial com OpenAI GPT-4o e text-embedding-3-small."""

    def __init__(self):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        except ImportError:
            self.client = None
        self.model_name = "gpt-4o-mini"
        self.embedding_model = "text-embedding-3-small"

    async def gerar_resposta(
        self,
        prompt_usuario: str,
        system_instruction: str,
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2,
    ) -> str:
        if not self.client:
            raise RuntimeError("Pacote 'openai' não instalado no ambiente.")
        messages = [{"role": "system", "content": system_instruction}]
        for msg in historico_dialogo:
            role = "user" if msg.get("papel") in ("user", "aluno") else "assistant"
            conteudo = msg.get("conteudo") or msg.get("texto") or ""
            if conteudo.strip():
                messages.append({"role": role, "content": conteudo})
        messages.append({"role": "user", "content": prompt_usuario})

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperatura,
        )
        return response.choices[0].message.content or ""

    async def gerar_embedding(self, texto: str, task_type: str = "retrieval_query") -> List[float]:
        """Gera vetor truncado para 768 dimensões garantindo compatibilidade com pgvector(768)."""
        if not self.client:
            raise RuntimeError("Pacote 'openai' não instalado no ambiente.")
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=texto,
            dimensions=768,
        )
        return response.data[0].embedding


class LLMFactory:
    """Instancia o provedor de IA com base nas variáveis de ambiente configuradas."""

    @staticmethod
    def obter_provedor() -> BaseLLMService:
        provedor = settings.LLM_PROVIDER.lower().strip()
        if provedor == "gemini":
            return GeminiLLMService()
        elif provedor == "openai":
            return OpenAILLMService()
        else:
            raise ValueError(f"Provedor de LLM '{provedor}' não suportado.")
