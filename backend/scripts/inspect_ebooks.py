"""
Script de Inspeção e Auditoria dos E-books de Gelson Iezzi
Analisa os 11 arquivos baixados para verificar integridade, contagem de páginas e presença de camada de texto (OCR vs Scan).
"""

import sys
import json
import hashlib
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ebooks"

VOLUMES_INFO = [
    {"vol": 1, "titulo": "Conjuntos e Funções", "file": "vol_01_conjuntos_e_funcoes.pdf", "area": "Álgebra e Funções"},
    {"vol": 2, "titulo": "Logaritmos", "file": "vol_02_logaritmos.pdf", "area": "Álgebra e Funções"},
    {"vol": 3, "titulo": "Trigonometria", "file": "vol_03_trigonometria.pdf", "area": "Geometria e Trigonometria"},
    {"vol": 4, "titulo": "Sequências, Matrizes, Determinantes e Sistemas", "file": "vol_04_sequencias_matrizes_sistemas.pdf", "area": "Álgebra Linear e Sequências"},
    {"vol": 5, "titulo": "Combinatória e Probabilidade", "file": "vol_05_combinatoria_probabilidade.pdf", "area": "Matemática Aplicada e Estatística"},
    {"vol": 6, "titulo": "Complexos, Polinômios e Equações", "file": "vol_06_complexos_polinomios_equacoes.pdf", "area": "Álgebra e Funções"},
    {"vol": 7, "titulo": "Geometria Analítica", "file": "vol_07_geometria_analitica.pdf", "area": "Geometria e Trigonometria"},
    {"vol": 8, "titulo": "Limites, Derivadas e Noções de Integral", "file": "vol_08_limites_derivadas_integral.pdf", "area": "Álgebra e Funções"},
    {"vol": 9, "titulo": "Geometria Plana", "file": "vol_09_geometria_plana.pdf", "area": "Geometria e Trigonometria"},
    {"vol": 10, "titulo": "Geometria Espacial", "file": "vol_10_geometria_espacial.pdf", "area": "Geometria e Trigonometria"},
    {"vol": 11, "titulo": "Matemática Financeira e Estatística Descritiva", "file": "vol_11_financeira_estatistica.pdf", "area": "Matemática Aplicada e Estatística"},
]


def analyze_pdf(pdf_path: Path):
    if not pdf_path.exists():
        return {"status": "missing"}
    
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    
    try:
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        
        # Amostragem de páginas (páginas 5 a 15 ou início se menor)
        sample_pages = range(min(5, num_pages - 1), min(25, num_pages))
        extracted_chars = 0
        sample_snippet = ""
        
        for p_idx in sample_pages:
            try:
                page_text = reader.pages[p_idx].extract_text() or ""
                extracted_chars += len(page_text.strip())
                if not sample_snippet and len(page_text.strip()) > 60:
                    sample_snippet = " ".join(page_text.strip().split()[:35]) + "..."
            except Exception:
                pass

        avg_chars = extracted_chars / (len(sample_pages) if sample_pages else 1)
        
        if avg_chars > 80:
            camada_texto = "Texto Nativo / OCR OK"
            tipo = "ocr_ok"
        elif avg_chars > 10:
            camada_texto = "OCR Parcial"
            tipo = "ocr_parcial"
        else:
            camada_texto = "Scan (Imagem Pura)"
            tipo = "scan_image"
            sample_snippet = "[Páginas escaneadas em imagem — sem camada de texto]"

        return {
            "status": "ok",
            "size_mb": round(size_mb, 2),
            "num_pages": num_pages,
            "avg_chars_per_page": round(avg_chars, 1),
            "camada_texto": camada_texto,
            "tipo": tipo,
            "snippet": sample_snippet
        }
    except Exception as e:
        return {
            "status": "error",
            "size_mb": round(size_mb, 2),
            "error": str(e)
        }


def main():
    results = []
    print("=== Relatório de Inspeção dos 11 Volumes da Coleção Iezzi ===\n")
    
    for item in VOLUMES_INFO:
        pdf_path = DATA_DIR / item["file"]
        info = analyze_pdf(pdf_path)
        item_data = {**item, **info}
        results.append(item_data)
        
        print(f"Vol. {item['vol']:02d} | {item['titulo']}")
        print(f"   Arquivo: {item['file']} ({info.get('size_mb', 0)} MB)")
        print(f"   Páginas: {info.get('num_pages', 'N/A')} | Camada: {info.get('camada_texto', 'N/A')}")
        print(f"   Amostra: {info.get('snippet', 'N/A')}\n")

    # Salva json para facilitar compilação do artifact
    json_path = DATA_DIR / "inspection_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Resultados salvos em: {json_path}")


if __name__ == "__main__":
    main()
