"""
Baterias de fixação canônicas server-side da Etapa 5, indexadas por
(numero_do_volume, numero_do_capitulo). O gabarito nunca é enviado ao
cliente antes da submissão — a correção acontece exclusivamente no backend.

Agregado dinamicamente a partir dos 11 módulos canônicos de volumes em app.seeds.volumes.
Na Etapa 7, este banco provisório será integrado às tabelas
itens_exercicios / tentativas_exercicios e ao motor CAT.
"""

from typing import Any
from app.seeds.volumes import ALL_VOLUMES

BATERIAS_FIXACAO_CANONICAS: dict[tuple[int, int], list[dict[str, Any]]] = {}

for volume_mod in ALL_VOLUMES:
    vol_num = volume_mod.VOLUME_INFO["numero"]
    fixacao_dict = getattr(volume_mod, "FIXACAO_DATA", {})
    for cap_num, questoes in fixacao_dict.items():
        lista_formatada = []
        for idx, q in enumerate(questoes, start=1):
            enunciado = q.get("enunciado") or q.get("enunciado_katex", "")
            alts_raw = q.get("alternativas", [])
            if alts_raw and isinstance(alts_raw[0], dict):
                alternativas = [a.get("texto") or a.get("texto_katex", "") for a in alts_raw]
                indice_correto = 0
                for a_idx, a in enumerate(alts_raw):
                    if a.get("correta") is True or (q.get("resposta_correta") and a.get("letra") == q.get("resposta_correta")):
                        indice_correto = a_idx
                        break
            else:
                alternativas = list(alts_raw)
                indice_correto = q.get("indice_correto", 0)

            lista_formatada.append({
                "numero": q.get("numero", idx),
                "enunciado": enunciado,
                "alternativas": alternativas,
                "indice_correto": indice_correto,
            })
        BATERIAS_FIXACAO_CANONICAS[(vol_num, cap_num)] = lista_formatada
