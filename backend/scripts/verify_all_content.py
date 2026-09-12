"""
Script de auditoria e verificação de integridade de todo o conteúdo didático.
Compara o banco de dados contra os dados canônicos em app.seeds.volumes.
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.content import VolumeDidatico, Capitulo, Aula
from app.seeds.volumes import ALL_VOLUMES

async def audit():
    async with AsyncSessionLocal() as db:
        print("🔍 Iniciando auditoria completa de 11 Volumes e 63 Capítulos/Aulas...\n")
        total_divergencias = 0
        total_aulas_verificadas = 0

        for vol_mod in ALL_VOLUMES:
            vol_num = vol_mod.VOLUME_INFO["numero"]
            vol_titulo = vol_mod.VOLUME_INFO["titulo"]
            aulas_canonicas = getattr(vol_mod, "AULAS_DATA", {})

            # Busca o volume no banco
            res_vol = await db.execute(
                select(VolumeDidatico).where(VolumeDidatico.numero_volume == vol_num)
            )
            vol_db = res_vol.scalar_one_or_none()
            if not vol_db:
                print(f"❌ [VOLUME AUSENTE] Vol. {vol_num:02d} ({vol_titulo}) não existe no banco!")
                total_divergencias += 1
                continue

            for cap_info in vol_mod.VOLUME_INFO["capitulos"]:
                cap_num = cap_info["num"]
                cap_titulo = cap_info["titulo"]

                # Busca capítulo no banco
                res_cap = await db.execute(
                    select(Capitulo).where(
                        Capitulo.volume_id == vol_db.id,
                        Capitulo.numero_capitulo == cap_num
                    )
                )
                cap_db = res_cap.scalar_one_or_none()
                if not cap_db:
                    print(f"❌ [CAPÍTULO AUSENTE] Vol. {vol_num:02d} Cap. {cap_num:02d}: '{cap_titulo}'")
                    total_divergencias += 1
                    continue

                # Busca aula no banco
                res_aula = await db.execute(select(Aula).where(Aula.capitulo_id == cap_db.id))
                aula_db = res_aula.scalar_one_or_none()

                total_aulas_verificadas += 1

                if not aula_db:
                    print(f"⚠️ [AULA NÃO CADASTRADA] Vol. {vol_num:02d} Cap. {cap_num:02d} ({cap_titulo})")
                    total_divergencias += 1
                    continue

                # Verifica se a aula canônica existe no arquivo seed
                if cap_num not in aulas_canonicas:
                    print(f"⚠️ [SEED SEM AULA] Vol. {vol_num:02d} Cap. {cap_num:02d} não tem entrada em AULAS_DATA")
                    continue

                aula_canon = aulas_canonicas[cap_num]
                teoria_canon = aula_canon.get("teoria", "").strip()
                exemplos_canon = aula_canon.get("exemplos", "").strip()
                dicas_canon = aula_canon.get("dicas", "").strip()

                teoria_db = (aula_db.bloco1_teoria_katex or "").strip()
                exemplos_db = (aula_db.bloco2_exemplos_katex or "").strip()
                dicas_db = (aula_db.bloco3_dicas_ia or "").strip()

                divergiu = False
                detalhes = []

                if teoria_canon != teoria_db:
                    divergiu = True
                    detalhes.append(f"Teoria diverge ({len(teoria_db)} chars no DB vs {len(teoria_canon)} chars canônicos)")
                if exemplos_canon != exemplos_db:
                    divergiu = True
                    detalhes.append(f"Exemplos divergem ({len(exemplos_db)} chars no DB vs {len(exemplos_canon)} chars canônicos)")
                if dicas_canon != dicas_db:
                    divergiu = True
                    detalhes.append(f"Dicas divergem ({len(dicas_db)} chars no DB vs {len(dicas_canon)} chars canônicos)")
                if aula_db.video_url:
                    detalhes.append(f"video_url presente: {aula_db.video_url}")

                if divergiu:
                    total_divergencias += 1
                    print(f"🚨 [DIVERGÊNCIA] Vol. {vol_num:02d} Cap. {cap_num:02d} ({cap_titulo}):")
                    for d in detalhes:
                        print(f"    - {d}")
                    print(f"    Início no DB: {teoria_db[:100]!r}...")

        print(f"\n==================================================")
        print(f"Auditoria finalizada: {total_aulas_verificadas} aulas verificadas.")
        print(f"Total de divergências encontradas: {total_divergencias}")
        print(f"==================================================")

if __name__ == "__main__":
    asyncio.run(audit())
