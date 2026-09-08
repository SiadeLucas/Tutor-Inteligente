---
title: "Etapa 6: Motor de IA e RAG"
type: "implementation"
status: "completed"
related: ["etapa-05-conteudo.md"]
last_updated: "2026-09-07"
updated_by: "antigravity"
---
<!-- ai-summary: Implementação do motor de inteligência artificial com Google Gemini Flash e sistema RAG com pgvector. Inclui factory de LLM, ingestão de embeddings, tutor socrático em três estágios, endpoints de chat e integração no frontend com suporte a KaTeX. -->

# Etapa 6: Motor de IA e RAG

**Duração:** 1 a 2 semanas
**Pré-requisito:** Etapa 5 concluída (Estrutura de conteúdo funcionando)
**Entregável:** Chat socrático funcional na página de aula, com respostas contextuais baseadas nos volumes de Iezzi.

Nesta etapa, daremos vida ao núcleo inteligente do projeto. Você vai configurar a integração com o Google Gemini Flash via `LLMFactory`, construir o motor RAG (Retrieval-Augmented Generation) com `pgvector` e implementar a lógica pedagógica do Tutor Socrático em 3 estágios.

---

## 6.1 Configuração do Gemini Flash

Para processamento de linguagem natural e geração de embeddings, utilizaremos o Google Gemini Flash.

1. **Obter Chave da API:**
   - Acesse o [Google AI Studio](https://aistudio.google.com/apikey).
   - Gere e copie a sua API key.

2. **Configuração de Variáveis de Ambiente:**
   - Adicione a chave no arquivo `.env` na raiz do backend:
   ```env
   GOOGLE_API_KEY="sua-chave-api-aqui"
   LLM_PROVIDER="gemini" # Padrão: gemini (suporta 'openai' no futuro)
   ```

3. **Implementação da LLMFactory:**
   - Crie o arquivo `backend/app/services/llm_factory.py`.
   - Implemente o suporte para inicializar a classe baseada no `LLM_PROVIDER`.
   - **Modelo de chat:** `gemini-1.5-flash`
   - **Modelo de embedding:** `text-embedding-004` (dimensão 768)

   ```python
   # backend/app/services/llm_factory.py
   import os
   from typing import List
   import google.generativeai as genai

   class LLMFactory:
       def __init__(self):
           self.provider = os.getenv("LLM_PROVIDER", "gemini")
           
           if self.provider == "gemini":
               genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
               self.chat_model = genai.GenerativeModel('gemini-1.5-flash')
               
       async def gerar_resposta(self, prompt: str, contexto: str) -> str:
           if self.provider == "gemini":
               full_prompt = f"Contexto:\n{contexto}\n\nPrompt:\n{prompt}"
               response = self.chat_model.generate_content(full_prompt)
               return response.text
           # Adicionar fallback para openai futuramente
           raise NotImplementedError("Provider não suportado.")

       async def gerar_embedding(self, texto: str) -> List[float]:
           if self.provider == "gemini":
               result = genai.embed_content(
                   model="models/text-embedding-004",
                   content=texto,
                   task_type="retrieval_document"
               )
               return result['embedding']
           raise NotImplementedError("Provider não suportado.")
   ```

> [!NOTE]
> A utilização da `LLMFactory` permite que futuramente você altere o provedor de IA com facilidade (como para a OpenAI) sem quebrar o restante da aplicação.

---

## 6.2 Motor RAG com pgvector

Para que o Gemini responda com base nos materiais de Iezzi, utilizaremos busca vetorial no PostgreSQL.

1. **Ativar pgvector:**
   Certifique-se de que a extensão está ativada no seu banco de dados via Alembic ou script SQL:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

2. **Índice HNSW:**
   Para buscas de similaridade rápidas (Cosine Similarity), crie um índice HNSW na coluna `embedding` da tabela `documentos_vetoriais_rag`.
   ```sql
   CREATE INDEX ON documentos_vetoriais_rag USING hnsw (embedding vector_cosine_ops);
   ```

3. **Lógica de Ingestão e Consulta (RAG Engine):**
   - **Ingestão:** Dividir o texto em chunks, gerar embedding (768 dimensões) e salvar.
   - **Busca (Query):** Converter a pergunta do aluno em embedding, buscar os Top-5 chunks por similaridade de cosseno, particionando estritamente pelo `volume_id`.

> [!IMPORTANT]
> É crucial **filtrar pelo `volume_id`** ao buscar contexto. Isso garante que, se o aluno está estudando o Volume 1, o RAG não recupere partes de geometria analítica do Volume 7.

---

## 6.3 Ingestão de Embeddings

Crie um script para processar e popular fragmentos de exemplo.

**Estratégia de Chunking:**
- Pedaços de ~500 tokens.
- Sobreposição (overlap) de ~100 tokens para não quebrar contextos no meio de parágrafos.

**Script de Exemplo:**
```python
# backend/scripts/ingest_iezzi.py
import asyncio
from app.services.llm_factory import LLMFactory
# Imports do banco de dados omitidos por brevidade

async def run_ingestion():
    factory = LLMFactory()
    
    # Exemplo: Conteúdo do Volume 1 (Conjuntos e Funções)
    documento = {
        "volume_id": "vol-1",
        "capitulo_id": "cap-1",
        "page_number": 15,
        "section_title": "1. Noções Básicas de Conjuntos",
        "texto": "Um conjunto é uma coleção de elementos..." # Texto extraído do PDF/Markdown
    }
    
    chunks = chunk_text(documento["texto"], chunk_size=500, overlap=100)
    
    for chunk in chunks:
        vetor = await factory.gerar_embedding(chunk)
        # Salvar no DB: documento["volume_id"], chunk, vetor, metadados
        await salvar_no_banco(documento, chunk, vetor)

if __name__ == "__main__":
    asyncio.run(run_ingestion())
```

---

## 6.4 Tutor Socrático em 3 Estágios

A metodologia pedagógica exige que não entreguemos as respostas imediatamente.

1. **Estágio 1: Pergunta Guia**
   Faz uma pergunta que induza o raciocínio.
2. **Estágio 2: Pista Cirúrgica**
   Fornece uma dica matemática específica (ex: qual fórmula aplicar).
3. **Estágio 3: Explicação Completa**
   Resolução detalhada passo a passo usando formato LaTeX (KaTeX).

**System Prompt Engineering:**
Crie uma classe para gerenciar o estado da sessão de chat e em qual estágio o aluno se encontra no capítulo atual.

```python
SYSTEM_PROMPT_BASE = """
Você é o Tutor Inteligente, um professor de matemática especializado na coleção de Gelson Iezzi.
Sempre formate equações usando notação LaTeX para KaTeX ($ para inline, $$ para bloco).
Utilize o contexto fornecido para embasar suas respostas.

ESTÁGIO ATUAL DO ALUNO: {estagio}
Regras do Estágio:
1 (Pergunta Guia): Não resolva. Faça uma pergunta que ajude o aluno a começar.
2 (Pista Cirúrgica): Dê uma dica matemática ou fórmula aplicável, sem dar o resultado final.
3 (Explicação): Resolva o problema passo a passo.
"""
```

---

## 6.5 Backend: Implementar Endpoints de IA

Substitua os endpoints mockados da Etapa 5 com a implementação real.

**POST `/api/v1/conteudo/aulas/{capitulo_id}/chat`**
- Recebe a mensagem.
- Recupera o estado atual do aluno no capítulo (para saber o Estágio Socrático).
- Faz busca vetorial no pgvector (RAG) limitando ao `volume_id` correspondente.
- Chama o `LLMFactory`.
- Rate limiting: máximo de 30 mensagens por capítulo/sessão.

**POST `/api/v1/conteudo/aulas/{capitulo_id}/pista`**
- Um atalho para forçar o backend a pular para o Estágio 2 de ajuda sem o aluno precisar digitar.

> [!WARNING]
> Adicione tratamento de erros caso a API do Google Gemini falhe (timeout, quota, etc). Retorne uma mensagem genérica amigável do tipo: *"Neste momento estou organizando meus cadernos, podemos tentar de novo em alguns segundos?"*

---

## 6.6 Frontend: Chat em Tempo Real

Integre a IA na interface de aula construída no Next.js (TypeScript).

1. **Layout do Painel (Split-Screen):**
   - O painel de conteúdo ocupa 65%, o chat 35% da tela.
2. **Componente de Mensagens:**
   - Renderize o texto em Markdown e, crucialmente, integre o componente **KaTeX** ou `react-mathjax` para renderizar o LaTeX devolvido pela IA.
3. **Indicador de Digitação:**
   - Exibir loading state visual enquanto a chamada à API ocorre.
4. **Histórico:**
   - O array de mensagens deve ser mantido no state (React) para compor a conversa.

---

## 6.7 Testes e Critérios de Aceitação

### Testes a Implementar

- `test_llm_factory_gemini_response`: Verifica se o provider retorna um string após formatar o prompt.
- `test_rag_engine_similarity_search`: Testa a busca vetorial (mock do pgvector) filtrando por `volume_id`.
- `test_socratic_stages`: Assegura que o estágio incrementa/altera conforme a interação com a IA.

### Critérios de Aceitação

- [x] A chave da API do Gemini (`GOOGLE_API_KEY`) pode ser configurada e carregada pelo `.env`.
- [x] A classe `LLMFactory` suporta a geração de chat e embeddings corretamente usando `gemini-1.5-flash` / `gemini-flash-latest` e `text-embedding-004` / `gemini-embedding-001`.
- [x] A extensão pgvector está ativada com índice HNSW para o campo embedding de 768 dimensões.
- [x] A busca vetorial por similaridade consegue trazer os chunks corretos e **respeita a restrição por `volume_id`**.
- [x] O backend implementa o fluxo Socrático em 3 estágios (Pergunta, Pista, Resolução).
- [x] Os endpoints de `/chat` e `/pista` não retornam erro 500 caso a API externa falhe.
- [x] O frontend exibe o layout dividido em 65/35 e o chat é capaz de processar os blocos matemáticos do KaTeX adequadamente.
- [x] O usuário consegue teclar "Enter" para enviar a mensagem e há um estado visual de carregamento.
- [x] Conversa manual na página de aula reflete perfeitamente as expectativas acima.
