"""
Script Canônico de Ingestão de Fragmentos do Iezzi (RAG - pgvector 768d).
Conforme especificação em docs-site/docs/implementation/etapa-06-ia-rag.md (Seção 6.3)
e docs-site/docs/knowledge/database/10-documentos-vetoriais-rag.md.

Suporta a ingestão de todos os 11 volumes canônicos da coleção Iezzi
ou de um volume específico via argumento de linha de comando:
    python scripts/ingest_iezzi.py       # Ingestão de todos os 11 volumes
    python scripts/ingest_iezzi.py 1     # Ingestão exclusiva do Volume 1
"""
import asyncio
import sys
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, delete

from app.core.config import settings
from app.models.content import VolumeDidatico, Capitulo, DocumentoVetorialRAG
from app.ai.llm_factory import LLMFactory
from app.seeds.volumes import ALL_VOLUMES, VOLUMES_BY_NUMBER


async def run_ingestion(filtro_volume: int | None = None):
    """Executa a ingestão e indexação vetorial no pgvector via Gemini Embeddings."""
    print("=== Tutor Inteligente: Ingestão de Fragmentos do Iezzi para RAG (pgvector 768d) ===")

    # 1. Instancia provedor de LLM para embeddings
    try:
        provedor = LLMFactory.obter_provedor()
        print(f"[OK] Provedor de LLM carregado: {provedor.__class__.__name__}")
    except Exception as exc:
        print(f"[ERRO] Falha ao instanciar provedor de LLM: {exc}")
        sys.exit(1)

    # 2. Conexão com o banco de dados
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    volumes_para_processar = (
        [VOLUMES_BY_NUMBER[filtro_volume]]
        if filtro_volume and filtro_volume in VOLUMES_BY_NUMBER
        else ALL_VOLUMES
    )

    total_geral_sucessos = 0
    total_geral_falhas = []

    async with session_factory() as session:
        for volume_mod in volumes_para_processar:
            vol_numero = volume_mod.VOLUME_INFO["numero"]
            vol_titulo = volume_mod.VOLUME_INFO["titulo"]
            fragmentos = getattr(volume_mod, "RAG_DATA", [])

            if not fragmentos:
                print(f"[PULANDO] Volume {vol_numero:02d}: {vol_titulo} (sem fragmentos RAG definidos).")
                continue

            print(f"\n--- Processando Volume {vol_numero:02d}: {vol_titulo} ({len(fragmentos)} fragmentos) ---")

            # Busca o volume no banco
            vol_res = await session.execute(
                select(VolumeDidatico).where(VolumeDidatico.numero_volume == vol_numero)
            )
            volume_db = vol_res.scalar_one_or_none()
            if not volume_db:
                print(f"  [AVISO] Volume {vol_numero} não encontrado no banco de dados. Execute scripts/seed_content.py primeiro.")
                continue

            # Mapeia capítulos do volume
            caps_res = await session.execute(
                select(Capitulo).where(Capitulo.volume_id == volume_db.id)
            )
            capitulos_map = {c.numero_capitulo: c.id for c in caps_res.scalars().all()}

            # Limpa fragmentos anteriores do volume para reindexação limpa (idempotente)
            await session.execute(
                delete(DocumentoVetorialRAG).where(DocumentoVetorialRAG.volume_id == volume_db.id)
            )
            await session.commit()
            print(f"  [OK] Fragmentos anteriores do Volume {vol_numero} removidos para reindexação limpa.")

            # Processamento de cada fragmento
            MAX_TENTATIVAS = 3
            sucessos_vol = 0

            for i, frag in enumerate(fragmentos, start=1):
                num_cap = frag.get("numero_capitulo", 1)
                cap_id = capitulos_map.get(num_cap)
                texto = frag.get("texto") or frag.get("conteudo_markdown", "")
                teorema = frag.get("teorema") or frag.get("titulo", f"Teorema Cap {num_cap}")
                pagina = frag.get("pagina", 1)

                print(f"  [{i}/{len(fragmentos)}] Gerando embedding: '{teorema}' (Cap. {num_cap})...")

                embedding = None
                for tentativa in range(1, MAX_TENTATIVAS + 1):
                    try:
                        embedding = await provedor.gerar_embedding(texto, task_type="retrieval_document")
                        break
                    except Exception as err:
                        print(f"    Tentativa {tentativa}/{MAX_TENTATIVAS} falhou: {err}")
                        if tentativa < MAX_TENTATIVAS:
                            await asyncio.sleep(2 ** tentativa)

                if embedding is None:
                    print(f"    [ERRO] Fragmento '{teorema}' não indexado após {MAX_TENTATIVAS} tentativas.")
                    total_geral_falhas.append(f"Vol {vol_numero} - {teorema}")
                    continue

                # Ajuste de dimensionalidade (pgvector 768d)
                if len(embedding) != 768:
                    embedding = embedding[:768] if len(embedding) > 768 else embedding + [0.0] * (768 - len(embedding))

                doc = DocumentoVetorialRAG(
                    id=uuid4(),
                    volume_id=volume_db.id,
                    capitulo_id=cap_id,
                    trecho_conteudo=texto,
                    metadados={
                        "pagina": pagina,
                        "teorema": teorema,
                        "numero_capitulo": num_cap,
                        "fonte": f"Fundamentos de Matemática Elementar - Gelson Iezzi, Vol. {vol_numero}",
                    },
                    embedding=embedding,
                )
                session.add(doc)
                sucessos_vol += 1
                total_geral_sucessos += 1

                # Rate-limiting gentil para evitar estouro de RPM na API do Gemini
                await asyncio.sleep(0.3)

            await session.commit()
            print(f"  [OK] Volume {vol_numero} concluído: {sucessos_vol}/{len(fragmentos)} fragmentos indexados.")

        print(f"\n=======================================================")
        print(f"Ingestão RAG finalizada: {total_geral_sucessos} fragmentos indexados com sucesso.")
        if total_geral_falhas:
            print(f"Fragmentos com falha: {total_geral_falhas}")
            sys.exit(2)

    await engine.dispose()


if __name__ == "__main__":
    filtro = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    asyncio.run(run_ingestion(filtro))
