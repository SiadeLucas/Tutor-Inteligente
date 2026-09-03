---
title: Conteúdo - Fábrica de LLM Desacoplada (Gemini Flash & Pluggable)
type: module
status: draft
related:
  - modules/conteudo/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Fábrica de LLM Desacoplada (`LLMFactory`)

Implementação executável do padrão de arquitetura **Factory**, garantindo **custo zero de IA no MVP através do Google Gemini Flash e Google Embeddings**, com compatibilidade nativa para modelos pagos (OpenAI GPT-4o / Anthropic Claude) via configuração de ambiente.

---

## Código Fonte (`backend/app/ai/llm_factory.py`)

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from app.core.config import settings


# ============================================================================
# 1. Interface Abstrata Comum
# ============================================================================

class BaseLLMService(ABC):
    """Contrato base que qualquer provedor de IA deve satisfazer."""

    @abstractmethod
    async def gerar_resposta(
        self, 
        prompt_usuario: str, 
        system_instruction: str, 
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2
    ) -> str:
        """Gera uma resposta textual ou em KaTeX formatada."""
        pass

    @abstractmethod
    async def gerar_embedding(self, texto: str) -> List[float]:
        """Gera um vetor denso para indexação ou busca no pgvector."""
        pass


# ============================================================================
# 2. Implementação do Provedor MVP Gratuito (Google Gemini Flash)
# ============================================================================

class GeminiLLMService(BaseLLMService):
    """
    Provedor padrão para o MVP da plataforma.
    Utiliza a cota gratuita do Google AI Studio (até 1.500 requisições diárias
    e embeddings text-embedding-004 com custo zero).
    """

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.modelo_texto_nome = "gemini-1.5-flash"
        self.modelo_embedding_nome = "models/text-embedding-004"

    async def gerar_resposta(
        self, 
        prompt_usuario: str, 
        system_instruction: str, 
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2
    ) -> str:
        # Configuração do modelo com instruções de sistema (System Prompt)
        model = genai.GenerativeModel(
            model_name=self.modelo_texto_nome,
            system_instruction=system_instruction,
            generation_config=genai.types.GenerationConfig(
                temperature=temperatura,
                max_output_tokens=1024
            )
        )

        # Formata o histórico de mensagens para a estrutura do Gemini
        mensagens_chat = []
        for msg in historico_dialogo:
            role = "user" if msg["papel"] == "user" else "model"
            mensagens_chat.append({"role": role, "parts": [msg["conteudo"]]})

        # Inicia a sessão de chat e envia a nova dúvida
        chat = model.start_chat(history=mensagens_chat)
        response = await chat.send_message_async(prompt_usuario)
        return response.text

    async def gerar_embedding(self, texto: str) -> List[float]:
        """Gera vetor de 768 dimensões com text-embedding-004."""
        result = genai.embed_content(
            model=self.modelo_embedding_nome,
            content=texto,
            task_type="retrieval_query"
        )
        return result["embedding"]


# ============================================================================
# 3. Implementação para Expansão Comercial Paga (OpenAI / GPT-4o)
# ============================================================================

class OpenAILLMService(BaseLLMService):
    """
    Provedor plugável para quando o cliente decidir migrar para OpenAI.
    Basta definir LLM_PROVIDER=openai no .env!
    """

    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = "gpt-4o-mini"

    async def gerar_resposta(
        self, 
        prompt_usuario: str, 
        system_instruction: str, 
        historico_dialogo: List[Dict[str, str]],
        temperatura: float = 0.2
    ) -> str:
        messages = [{"role": "system", "content": system_instruction}]
        for msg in historico_dialogo:
            messages.append({"role": msg["papel"], "content": msg["conteudo"]})
        messages.append({"role": "user", "content": prompt_usuario})

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperatura
        )
        return response.choices[0].message.content

    async def gerar_embedding(self, texto: str) -> List[float]:
        """Gera vetor truncado para 768 dimensões garantindo compatibilidade com o schema pgvector(768)."""
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texto,
            dimensions=768
        )
        return response.data[0].embedding


# ============================================================================
# 4. Fábrica Dinâmica com Injeção de Dependência
# ============================================================================

class LLMFactory:
    """Instancia o provedor de IA com base nas variáveis de ambiente."""

    @staticmethod
    def obter_provedor() -> BaseLLMService:
        provedor = settings.LLM_PROVIDER.lower()  # 'gemini' (default) ou 'openai'
        if provedor == "gemini":
            return GeminiLLMService()
        elif provedor == "openai":
            return OpenAILLMService()
        else:
            raise ValueError(f"Provedor de LLM não suportado: {provedor}")
```
