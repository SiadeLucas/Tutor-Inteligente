"""
Script de População Canônica de Conteúdo Didático — Tutor Inteligente
Popula a disciplina de Matemática, os 11 volumes da Coleção Iezzi,
todos os 63 capítulos canônicos e as 63 aulas ricas em KaTeX
a partir dos módulos canônicos em app.seeds.volumes.
"""
import asyncio
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.content import Disciplina, VolumeDidatico, Capitulo, Aula
from app.seeds.volumes import ALL_VOLUMES


async def seed():
    print("=== Tutor Inteligente: Iniciando Seed Canônico de Conteúdo Didático (11 Volumes / 63 Capítulos) ===")
    async with AsyncSessionLocal() as db:
        # 1. Disciplina de Matemática
        disc_res = await db.execute(select(Disciplina).where(Disciplina.slug == "matematica"))
        disciplina = disc_res.scalar_one_or_none()

        if not disciplina:
            disciplina = Disciplina(
                slug="matematica",
                nome="Matemática",
                nivel_ensino="ensino_medio",
                icone="calculate",
                cor_tema="#F57C00",
                ordem=1,
                ativo=True,
            )
            db.add(disciplina)
            await db.flush()
            print(f"[OK] Disciplina cadastrada: {disciplina.nome} ({disciplina.slug})")
        else:
            print(f"[OK] Disciplina já existente: {disciplina.nome}")

        # 2. Volumes, Capítulos e Aulas a partir de ALL_VOLUMES
        total_volumes = 0
        total_caps = 0
        total_aulas = 0

        for volume_mod in ALL_VOLUMES:
            vol_info = volume_mod.VOLUME_INFO
            aulas_dict = getattr(volume_mod, "AULAS_DATA", {})

            vol_res = await db.execute(
                select(VolumeDidatico).where(
                    VolumeDidatico.disciplina_id == disciplina.id,
                    VolumeDidatico.numero_volume == vol_info["numero"],
                )
            )
            volume = vol_res.scalar_one_or_none()

            if not volume:
                volume = VolumeDidatico(
                    disciplina_id=disciplina.id,
                    nome_colecao="Fundamentos de Matemática Elementar - Gelson Iezzi",
                    numero_volume=vol_info["numero"],
                    titulo=vol_info["titulo"],
                    grande_area=vol_info["grande_area"],
                    ordem_exibicao=vol_info["ordem"],
                    preco_padrao=49.90,
                    ativo=True,
                )
                db.add(volume)
                await db.flush()
                print(f"  [+] Volume {volume.numero_volume:02d}: {volume.titulo} ({volume.grande_area})")
            else:
                # Atualiza título e grande área se necessário
                volume.titulo = vol_info["titulo"]
                volume.grande_area = vol_info["grande_area"]
                volume.ordem_exibicao = vol_info["ordem"]
                await db.flush()
                print(f"  [OK] Volume {volume.numero_volume:02d} existente: {volume.titulo}")

            total_volumes += 1

            # Capítulos do Volume
            for cap_idx, cap_info in enumerate(vol_info["capitulos"], start=1):
                cap_res = await db.execute(
                    select(Capitulo).where(
                        Capitulo.volume_id == volume.id,
                        Capitulo.numero_capitulo == cap_info["num"],
                    )
                )
                capitulo = cap_res.scalar_one_or_none()

                if not capitulo:
                    capitulo = Capitulo(
                        volume_id=volume.id,
                        numero_capitulo=cap_info["num"],
                        titulo=cap_info["titulo"],
                        tempo_estimado_min=cap_info["tempo"],
                        preco_avulso=9.90,
                        pre_requisitos_ids=[],
                        ordem=cap_idx,
                    )
                    db.add(capitulo)
                    await db.flush()
                else:
                    capitulo.titulo = cap_info["titulo"]
                    capitulo.tempo_estimado_min = cap_info["tempo"]
                    capitulo.ordem = cap_idx
                    await db.flush()

                total_caps += 1

                # Criação ou atualização da Aula com KaTeX completo
                if cap_info["num"] in aulas_dict:
                    aula_data = aulas_dict[cap_info["num"]]
                    aula_res = await db.execute(select(Aula).where(Aula.capitulo_id == capitulo.id))
                    aula = aula_res.scalar_one_or_none()

                    if not aula:
                        aula = Aula(
                            capitulo_id=capitulo.id,
                            bloco1_teoria_katex=aula_data["teoria"],
                            bloco2_exemplos_katex=aula_data["exemplos"],
                            bloco3_dicas_ia=aula_data["dicas"],
                            publicado=True,
                        )
                        db.add(aula)
                        await db.flush()
                        print(f"      [*] Aula cadastrada: Vol {volume.numero_volume:02d} Cap {capitulo.numero_capitulo} - {capitulo.titulo}")
                    else:
                        aula.bloco1_teoria_katex = aula_data["teoria"]
                        aula.bloco2_exemplos_katex = aula_data["exemplos"]
                        aula.bloco3_dicas_ia = aula_data["dicas"]
                        aula.publicado = True
                        await db.flush()

                    total_aulas += 1

        await db.commit()
        print(f"\n Seed de conteúdo concluído com sucesso!")
        print(f"Total: 1 Disciplina | {total_volumes} Volumes | {total_caps} Capítulos | {total_aulas} Aulas completas com KaTeX.")


if __name__ == "__main__":
    asyncio.run(seed())
