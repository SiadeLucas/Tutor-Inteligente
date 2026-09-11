"""
Script Canônico de População de Exercícios Calibrados TRI — Tutor Inteligente
Associa itens calibrados do modelo TRI 3PL aos capítulos canônicos
através da tupla determinística (VolumeDidatico.numero_volume, Capitulo.numero_capitulo),
carregando TRI_DATA diretamente dos 11 módulos canônicos em app.seeds.volumes.
"""

import asyncio
import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.content import Capitulo, VolumeDidatico
from app.models.exercise import ItemExercicio
from app.seeds.volumes import ALL_VOLUMES


async def seed_exercises():
    """Popula os exercícios calibrados TRI associando aos capítulos correspondentes de forma determinística."""
    print("=== Tutor Inteligente: Iniciando População Canônica de Exercícios Calibrados TRI ===")
    async with AsyncSessionLocal() as session:
        # Busca capítulos carregando o relacionamento com VolumeDidatico
        stmt_caps = select(Capitulo).options(selectinload(Capitulo.volume))
        result_caps = await session.execute(stmt_caps)
        capitulos = result_caps.scalars().all()

        mapa_capitulos: dict[tuple[int, int], uuid.UUID] = {}
        for c in capitulos:
            if c.volume:
                mapa_capitulos[(c.volume.numero_volume, c.numero_capitulo)] = c.id

        if not mapa_capitulos:
            print("[ERRO] Nenhum capítulo encontrado no banco. Execute scripts/seed_content.py primeiro!")
            return

        print(f"[INFO] {len(mapa_capitulos)} capítulos indexados por (volume_num, capitulo_num).")

        total_processados = 0
        total_inseridos = 0
        total_atualizados = 0

        for volume_mod in ALL_VOLUMES:
            vol_num = volume_mod.VOLUME_INFO["numero"]
            vol_titulo = volume_mod.VOLUME_INFO["titulo"]
            tri_items = getattr(volume_mod, "TRI_DATA", [])

            print(f" -> Processando Volume {vol_num:02d}: {vol_titulo} ({len(tri_items)} itens TRI)")

            for item_data in tri_items:
                cap_num = item_data["numero_capitulo"]
                capitulo_id = mapa_capitulos.get((vol_num, cap_num))

                if not capitulo_id:
                    print(f"    [ALERTA] Capítulo ({vol_num}, {cap_num}) não encontrado no banco. Pulando item.")
                    continue

                total_processados += 1

                # Verifica se já existe item com o mesmo enunciado no mesmo capítulo
                stmt_existente = select(ItemExercicio).where(
                    ItemExercicio.capitulo_id == capitulo_id,
                    ItemExercicio.enunciado_katex == item_data["enunciado_katex"],
                )
                existente = (await session.execute(stmt_existente)).scalars().first()

                if not existente:
                    novo_item = ItemExercicio(
                        id=uuid.uuid4(),
                        capitulo_id=capitulo_id,
                        tipo_origem=item_data.get("tipo_origem", "iezzi_original"),
                        tipo_item=item_data.get("tipo_item", "multiple_choice"),
                        enunciado_katex=item_data["enunciado_katex"],
                        alternativas=item_data.get("alternativas", []),
                        resposta_correta=item_data["resposta_correta"],
                        resolucao_passo_a_passo=item_data.get("resolucao_passo_a_passo", ""),
                        parametro_a=item_data["parametro_a"],
                        parametro_b=item_data["parametro_b"],
                        parametro_c=item_data["parametro_c"],
                        metadados_sympy=item_data.get("metadados_sympy", {}),
                        validado_sympy=True,
                        ativo=True,
                    )
                    session.add(novo_item)
                    total_inseridos += 1
                else:
                    # Atualiza parâmetros e associação correta de capítulo
                    existente.capitulo_id = capitulo_id
                    existente.tipo_origem = item_data.get("tipo_origem", "iezzi_original")
                    existente.tipo_item = item_data.get("tipo_item", "multiple_choice")
                    existente.alternativas = item_data.get("alternativas", [])
                    existente.resposta_correta = item_data["resposta_correta"]
                    existente.resolucao_passo_a_passo = item_data.get("resolucao_passo_a_passo", "")
                    existente.parametro_a = item_data["parametro_a"]
                    existente.parametro_b = item_data["parametro_b"]
                    existente.parametro_c = item_data["parametro_c"]
                    existente.metadados_sympy = item_data.get("metadados_sympy", {})
                    existente.validado_sympy = True
                    existente.ativo = True
                    total_atualizados += 1

        await session.commit()
        print(f"\n[SUCESSO] População de exercícios concluída!")
        print(f"Total processados: {total_processados} | Novos inseridos: {total_inseridos} | Atualizados: {total_atualizados}")


if __name__ == "__main__":
    asyncio.run(seed_exercises())
