"""
Script de Download Automatizado — Coleção Fundamentos de Matemática Elementar (Gelson Iezzi)
Baixa os 11 volumes didáticos do repositório público do Internet Archive para backend/data/ebooks/.
"""

import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Diretório de destino
DEST_DIR = Path(__file__).resolve().parent.parent / "data" / "ebooks"
DEST_DIR.mkdir(parents=True, exist_ok=True)

ITEM_IDENTIFIER = "fundamentos-de-matematica-elementar_202403"
BASE_URL = f"https://archive.org/download/{ITEM_IDENTIFIER}"

# Mapeamento oficial dos 11 volumes canônicos
VOLUMES = [
    {
        "volume": 1,
        "titulo": "Conjuntos e Funções",
        "grande_area": "algebra_funcoes",
        "remote_file": "fundamentos-da-matematica-elementar-1-.pdf",
        "local_file": "vol_01_conjuntos_e_funcoes.pdf",
    },
    {
        "volume": 2,
        "titulo": "Logaritmos",
        "grande_area": "algebra_funcoes",
        "remote_file": "fundamentos-da-matematica-elementar-2-.pdf",
        "local_file": "vol_02_logaritmos.pdf",
    },
    {
        "volume": 3,
        "titulo": "Trigonometria",
        "grande_area": "geometria",
        "remote_file": "fundamentos-da-matematica-elementar-3.pdf",
        "local_file": "vol_03_trigonometria.pdf",
    },
    {
        "volume": 4,
        "titulo": "Sequências, Matrizes, Determinantes e Sistemas",
        "grande_area": "algebra_linear",
        "remote_file": "fundamentos-da-matematica-elementar-4.pdf",
        "local_file": "vol_04_sequencias_matrizes_sistemas.pdf",
    },
    {
        "volume": 5,
        "titulo": "Combinatória e Probabilidade",
        "grande_area": "aplicada",
        "remote_file": "fundamentos-da-matematica-elementar-5-1-1.pdf",
        "local_file": "vol_05_combinatoria_probabilidade.pdf",
    },
    {
        "volume": 6,
        "titulo": "Complexos, Polinômios e Equações",
        "grande_area": "algebra_funcoes",
        "remote_file": "fundamentos-da-matematica-elementar-6-1.pdf",
        "local_file": "vol_06_complexos_polinomios_equacoes.pdf",
    },
    {
        "volume": 7,
        "titulo": "Geometria Analítica",
        "grande_area": "geometria",
        "remote_file": "fundamentos-da-matematica-elementar-7-1.pdf",
        "local_file": "vol_07_geometria_analitica.pdf",
    },
    {
        "volume": 8,
        "titulo": "Limites, Derivadas e Noções de Integral",
        "grande_area": "algebra_funcoes",
        "remote_file": "fundamentos-da-matematica-elementar-8.pdf",
        "local_file": "vol_08_limites_derivadas_integral.pdf",
    },
    {
        "volume": 9,
        "titulo": "Geometria Plana",
        "grande_area": "geometria",
        "remote_file": "fundamentos-da-matematica-elementar-9.pdf",
        "local_file": "vol_09_geometria_plana.pdf",
    },
    {
        "volume": 10,
        "titulo": "Geometria Espacial",
        "grande_area": "geometria",
        "remote_file": "fundamentos-da-matematica-elementar-10.pdf",
        "local_file": "vol_10_geometria_espacial.pdf",
    },
    {
        "volume": 11,
        "titulo": "Matemática Financeira e Estatística Descritiva",
        "grande_area": "aplicada",
        "remote_file": "fundamentos-da-matematica-elementar-11.pdf",
        "local_file": "vol_11_financeira_estatistica.pdf",
    },
]


def download_file(url: str, dest_path: Path):
    """Baixa um arquivo com stream e reporte de progresso."""
    temp_path = dest_path.with_suffix(".tmp")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )

    with urllib.request.urlopen(req) as response, open(temp_path, "wb") as out_file:
        total_size = int(response.info().get("Content-Length", 0))
        chunk_size = 1024 * 1024  # 1MB
        downloaded = 0
        start_time = time.time()

        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = downloaded / total_size * 100
                elapsed = time.time() - start_time
                speed = (downloaded / (1024 * 1024)) / (elapsed if elapsed > 0 else 1)
                sys.stdout.write(
                    f"\r    Progresso: {percent:5.1f}% ({downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB) @ {speed:.2f} MB/s"
                )
                sys.stdout.flush()

    if temp_path.exists():
        temp_path.replace(dest_path)
    print()


def main():
    print(f"=== Tutor Inteligente: Download da Coleção Gelson Iezzi (11 Volumes) ===")
    print(f"Destino local: {DEST_DIR}")
    print(f"Repositório: {BASE_URL}\n")

    for item in VOLUMES:
        vol_num = item["volume"]
        titulo = item["titulo"]
        remote_file = item["remote_file"]
        local_file = item["local_file"]
        dest_path = DEST_DIR / local_file

        url = f"{BASE_URL}/{urllib.parse.quote(remote_file)}"

        if dest_path.exists() and dest_path.stat().st_size > 1024 * 1024:
            size_mb = dest_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Vol. {vol_num:02d}: {titulo} já baixado ({size_mb:.1f} MB)")
            continue

        print(f"[*] Baixando Vol. {vol_num:02d}: {titulo}...")
        try:
            download_file(url, dest_path)
            size_mb = dest_path.stat().st_size / (1024 * 1024)
            print(f"    -> Salvo com sucesso: {local_file} ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"    [ERRO] Falha ao baixar {local_file}: {e}")

    print("\nDownload concluído! Verificando arquivos baixados:")
    total_mb = sum(f.stat().st_size for f in DEST_DIR.glob("*.pdf")) / (1024 * 1024)
    count = len(list(DEST_DIR.glob("*.pdf")))
    print(f"Total: {count} arquivos PDF | {total_mb:.1f} MB em {DEST_DIR}\n")


if __name__ == "__main__":
    main()
