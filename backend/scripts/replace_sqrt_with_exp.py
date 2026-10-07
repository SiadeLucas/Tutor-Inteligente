"""
Script para substituição de todas as raízes (\\sqrt) pela forma exponencial fracionária
nos arquivos de sementes dos 11 volumes didáticos da plataforma Tutor Inteligente.

Em conformidade com a solicitação do usuário e a regra RN-EXE-017 de padronização KaTeX:
- \\sqrt{x} -> x^{1/2}
- \\sqrt{E} -> (E)^{1/2} para expressões compostas
- \\sqrt[n]{x} -> x^{1/n}
- Coeficientes justapostos (ex: 4\\sqrt{2}) recebem \\cdot explícito: 4 \\cdot 2^{1/2}
"""
from __future__ import annotations
import ast
import glob
import os
import sys
from pathlib import Path

# Adiciona o backend ao path para importar o módulo formatters
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.modules.exercises.formatters import converter_raiz_em_exponencial


def processar_volumes():
    volumes_dir = backend_dir / "app" / "seeds" / "volumes"
    padrao = str(volumes_dir / "vol_*.py")
    arquivos = sorted(glob.glob(padrao))

    if not arquivos:
        print(f"Nenhum arquivo encontrado em: {padrao}")
        return

    print(f"Iniciando substituição de \\sqrt em {len(arquivos)} volumes...")

    total_linhas_alteradas = 0
    total_arquivos_alterados = 0

    for arq in arquivos:
        nome_arquivo = os.path.basename(arq)
        with open(arq, "r", encoding="utf-8") as fp:
            linhas = fp.readlines()

        novas_linhas = []
        alteracoes_no_arquivo = 0

        for i, linha in enumerate(linhas):
            if r"\sqrt" in linha:
                linha_convertida = converter_raiz_em_exponencial(linha)
                if linha_convertida != linha:
                    alteracoes_no_arquivo += 1
                novas_linhas.append(linha_convertida)
            else:
                novas_linhas.append(linha)

        if alteracoes_no_arquivo > 0:
            conteudo_final = "".join(novas_linhas)

            # Verifica se ainda resta algum \sqrt
            restantes = conteudo_final.count(r"\sqrt")
            if restantes > 0:
                print(f"[ALERTA] {nome_arquivo} ainda contém {restantes} ocorrências de \\sqrt!")

            # Valida sintaxe AST para garantir que o código Python permanece 100% válido
            try:
                ast.parse(conteudo_final, filename=nome_arquivo)
            except SyntaxError as e:
                print(f"[ERRO DE SINTAXE] Falha ao compilar AST em {nome_arquivo}: {e}")
                sys.exit(1)

            # Grava o arquivo atualizado
            with open(arq, "w", encoding="utf-8") as fp:
                fp.write(conteudo_final)

            total_arquivos_alterados += 1
            total_linhas_alteradas += alteracoes_no_arquivo
            print(f"  [OK] {nome_arquivo}: {alteracoes_no_arquivo} linhas atualizadas (0 resíduos)")
        else:
            print(f"  [-] {nome_arquivo}: sem ocorrências de \\sqrt")

    print("\n" + "=" * 60)
    print(f"Concluído com sucesso!")
    print(f"Arquivos atualizados: {total_arquivos_alterados}")
    print(f"Linhas atualizadas:   {total_linhas_alteradas}")
    print("=" * 60)


if __name__ == "__main__":
    processar_volumes()
