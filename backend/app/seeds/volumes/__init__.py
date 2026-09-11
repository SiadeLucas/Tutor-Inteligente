"""
Pacote Canônico de Módulos Didáticos por Volume
Coleção Fundamentos de Matemática Elementar (Gelson Iezzi) - 11 Volumes, 63 Capítulos.
"""

from app.seeds.volumes import (
    vol_01_conjuntos,
    vol_02_logaritmos,
    vol_03_trigonometria,
    vol_04_algebra_linear,
    vol_05_combinatoria,
    vol_06_complexos,
    vol_07_geometria_analitica,
    vol_08_calculo,
    vol_09_geometria_plana,
    vol_10_geometria_espacial,
    vol_11_financeira_estatistica,
)

ALL_VOLUMES = [
    vol_01_conjuntos,
    vol_02_logaritmos,
    vol_03_trigonometria,
    vol_04_algebra_linear,
    vol_05_combinatoria,
    vol_06_complexos,
    vol_07_geometria_analitica,
    vol_08_calculo,
    vol_09_geometria_plana,
    vol_10_geometria_espacial,
    vol_11_financeira_estatistica,
]

VOLUMES_BY_NUMBER = {
    mod.VOLUME_INFO["numero"]: mod for mod in ALL_VOLUMES
}

__all__ = [
    "ALL_VOLUMES",
    "VOLUMES_BY_NUMBER",
    "vol_01_conjuntos",
    "vol_02_logaritmos",
    "vol_03_trigonometria",
    "vol_04_algebra_linear",
    "vol_05_combinatoria",
    "vol_06_complexos",
    "vol_07_geometria_analitica",
    "vol_08_calculo",
    "vol_09_geometria_plana",
    "vol_10_geometria_espacial",
    "vol_11_financeira_estatistica",
]
