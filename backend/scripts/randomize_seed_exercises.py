"""
Script Canônico de Randomização e Balanceamento das Alternativas dos Exercícios Didáticos
Tutor Inteligente — Alinha os 11 volumes didáticos (TRI_DATA e FIXACAO_DATA)
para eliminar a recorrência de gabaritos fixos na alternativa 'A'.

Distribui as respostas corretas uniformemente (~20% para cada: A, B, C, D, E).
Preserva 100% da formatação original dos arquivos, expressões KaTeX e metadados.
"""

from __future__ import annotations
import argparse
import ast
from collections import Counter
from pathlib import Path
import random
import sys

# Adiciona o diretório backend ao sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import importlib.util
spec_rand = importlib.util.spec_from_file_location(
    "randomizer",
    BASE_DIR / "app" / "modules" / "exercises" / "randomizer.py"
)
randomizer_mod = importlib.util.module_from_spec(spec_rand)
spec_rand.loader.exec_module(randomizer_mod)

LETRAS_PADRAO = randomizer_mod.LETRAS_PADRAO
atualizar_texto_resolucao = randomizer_mod.atualizar_texto_resolucao


def extrair_bytes_node(lines_bytes: list[bytes], node: ast.AST) -> bytes:
    """Extrai os bytes originais exatos correspondentes ao nó AST (offsets UTF-8)."""
    s_lineno = node.lineno - 1
    e_lineno = node.end_lineno - 1
    s_col = node.col_offset
    e_col = node.end_col_offset

    if s_lineno == e_lineno:
        return lines_bytes[s_lineno][s_col:e_col]

    partes = [lines_bytes[s_lineno][s_col:]]
    for l_idx in range(s_lineno + 1, e_lineno):
        partes.append(lines_bytes[l_idx])
    partes.append(lines_bytes[e_lineno][:e_col])
    return b"".join(partes)


def processar_volume(file_path: Path, rng: random.Random, dry_run: bool = False) -> tuple[Counter, Counter]:
    """
    Processa um arquivo de volume didático, balanceando as alternativas em TRI_DATA e FIXACAO_DATA.
    Retorna (distribuicao_anterior, distribuicao_nova).
    """
    content_bytes = file_path.read_bytes()
    content_str = content_bytes.decode("utf-8")
    lines_bytes = content_bytes.splitlines(keepends=True)
    tree = ast.parse(content_str)

    dist_antiga: Counter = Counter()
    dist_nova: Counter = Counter()

    # Coleta todas as listas de itens a processar (TRI_DATA e FIXACAO_DATA)
    listas_itens_ast: list[tuple[str, list[ast.Dict]]] = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "TRI_DATA" and isinstance(node.value, ast.List):
                        dicts = [elt for elt in node.value.elts if isinstance(elt, ast.Dict)]
                        listas_itens_ast.append(("TRI_DATA", dicts))
                    elif target.id == "FIXACAO_DATA" and isinstance(node.value, ast.Dict):
                        for val in node.value.values:
                            if isinstance(val, ast.List):
                                dicts = [elt for elt in val.elts if isinstance(elt, ast.Dict)]
                                listas_itens_ast.append(("FIXACAO_DATA", dicts))

    substituicoes_arquivo: list[tuple[int, int, int, int, bytes]] = []

    for origem_nome, itens_dicts in listas_itens_ast:
        # Filtra itens de múltipla escolha com alternativas estruturadas
        itens_mc: list[ast.Dict] = []
        for it_dict in itens_dicts:
            keys = [k.value for k in it_dict.keys if isinstance(k, ast.Constant)]
            if "alternativas" in keys:
                for k, v in zip(it_dict.keys, it_dict.values):
                    if (
                        isinstance(k, ast.Constant)
                        and k.value == "alternativas"
                        and isinstance(v, ast.List)
                        and len(v.elts) > 0
                        and all(isinstance(e, ast.Dict) for e in v.elts)
                    ):
                        itens_mc.append(it_dict)
                        break

        if not itens_mc:
            continue

        # Cria fila balanceada de letras destino para este bloco
        total_mc = len(itens_mc)
        letras_fila: list[str] = []
        while len(letras_fila) < total_mc:
            bloco = LETRAS_PADRAO.copy()
            rng.shuffle(bloco)
            letras_fila.extend(bloco)
        letras_fila = letras_fila[:total_mc]
        rng.shuffle(letras_fila)

        # Processa cada item MC
        for it_idx, it_dict in enumerate(itens_mc):
            letra_alvo = letras_fila[it_idx]

            chaves_dict: dict[str, tuple[ast.AST, ast.AST]] = {}
            for k, v in zip(it_dict.keys, it_dict.values):
                if isinstance(k, ast.Constant):
                    chaves_dict[k.value] = (k, v)

            alt_key_node, alt_val_node = chaves_dict["alternativas"]
            assert isinstance(alt_val_node, ast.List)
            num_alts = len(alt_val_node.elts)
            letras_atuais = LETRAS_PADRAO[:num_alts]

            # Encontra qual alternativa é a correta atualmente
            idx_correta_antiga = -1
            letra_antiga = "A"

            resp_key_node, resp_val_node = chaves_dict.get("resposta_correta", (None, None))
            if resp_val_node and isinstance(resp_val_node, ast.Constant):
                letra_antiga = str(resp_val_node.value).strip().upper()

            alt_nodes_info: list[dict] = []
            for a_idx, a_elt in enumerate(alt_val_node.elts):
                assert isinstance(a_elt, ast.Dict)
                a_chaves = {k.value: v for k, v in zip(a_elt.keys, a_elt.values) if isinstance(k, ast.Constant)}
                
                texto_node = a_chaves["texto"]
                raw_texto_bytes = extrair_bytes_node(lines_bytes, texto_node)
                
                correta_node = a_chaves.get("correta")
                eh_correta = False
                if correta_node and isinstance(correta_node, ast.Constant) and correta_node.value is True:
                    eh_correta = True
                    idx_correta_antiga = a_idx
                elif not correta_node and resp_val_node and a_chaves.get("letra", ast.Constant("")).value == letra_antiga:
                    eh_correta = True
                    idx_correta_antiga = a_idx

                alt_nodes_info.append({
                    "node": a_elt,
                    "raw_texto_bytes": raw_texto_bytes,
                    "eh_correta": eh_correta,
                })

            if idx_correta_antiga == -1:
                idx_correta_antiga = 0

            dist_antiga[letra_antiga] += 1
            dist_nova[letra_alvo] += 1

            # Embaralha os distratores
            alt_correta_info = alt_nodes_info[idx_correta_antiga]
            distratores_info = [a for idx, a in enumerate(alt_nodes_info) if idx != idx_correta_antiga]
            rng.shuffle(distratores_info)

            # Posiciona na letra alvo
            target_idx = letras_atuais.index(letra_alvo) if letra_alvo in letras_atuais else 0
            nova_ordem_info: list[dict] = []
            d_iter = iter(distratores_info)
            for i in range(num_alts):
                if i == target_idx:
                    nova_ordem_info.append(alt_correta_info)
                else:
                    nova_ordem_info.append(next(d_iter))

            # 1. Substituição do bloco de alternativas
            primeira_alt_node = alt_val_node.elts[0]
            indent_bytes = b" " * primeira_alt_node.col_offset

            linhas_novas_alts: list[bytes] = []
            for i, a_info in enumerate(nova_ordem_info):
                letra_i = letras_atuais[i]
                correta_bool = (i == target_idx)
                correta_bytes = b"True" if correta_bool else b"False"
                linha_b = (
                    indent_bytes
                    + f'{{"letra": "{letra_i}", "texto": '.encode("utf-8")
                    + a_info["raw_texto_bytes"]
                    + b', "correta": '
                    + correta_bytes
                    + b'},\n'
                )
                linhas_novas_alts.append(linha_b)

            ultima_alt_node = alt_val_node.elts[-1]
            substituicoes_arquivo.append((
                primeira_alt_node.lineno - 1,
                0,
                ultima_alt_node.end_lineno,
                0,
                b"".join(linhas_novas_alts)
            ))

            # 2. Substituição de resposta_correta
            if resp_val_node:
                substituicoes_arquivo.append((
                    resp_val_node.lineno - 1,
                    resp_val_node.col_offset,
                    resp_val_node.end_lineno - 1,
                    resp_val_node.end_col_offset,
                    f'"{letra_alvo}"'.encode("utf-8")
                ))

            # 3. Substituição na resolução passo a passo / explicação katex
            res_chave = "resolucao_passo_a_passo" if "resolucao_passo_a_passo" in chaves_dict else "explicacao_katex" if "explicacao_katex" in chaves_dict else None
            if res_chave:
                res_k, res_v = chaves_dict[res_chave]
                if isinstance(res_v, ast.Constant):
                    texto_original_res = res_v.value
                    novo_texto_res = atualizar_texto_resolucao(texto_original_res, letra_antiga, letra_alvo)
                    
                    raw_res_bytes = extrair_bytes_node(lines_bytes, res_v)
                    is_raw = raw_res_bytes.startswith(b"r")
                    
                    escaped_res = novo_texto_res.replace('"', '\\"')
                    prefixo = 'r"' if is_raw else '"'
                    novo_res_str = f'{prefixo}{escaped_res}"'

                    substituicoes_arquivo.append((
                        res_v.lineno - 1,
                        res_v.col_offset,
                        res_v.end_lineno - 1,
                        res_v.end_col_offset,
                        novo_res_str.encode("utf-8")
                    ))

    if dry_run or not substituicoes_arquivo:
        return dist_antiga, dist_nova

    # Aplica as substituições de baixo para cima (reverse order das posições)
    substituicoes_arquivo.sort(key=lambda x: (x[0], x[1]), reverse=True)

    novo_content_bytes = content_bytes
    for s_line, s_col, e_line, e_col, novo_bytes in substituicoes_arquivo:
        lines = novo_content_bytes.splitlines(keepends=True)
        antes = b"".join(lines[:s_line]) + lines[s_line][:s_col]
        depois = lines[e_line][e_col:] + b"".join(lines[e_line + 1:]) if e_line < len(lines) else b""
        novo_content_bytes = antes + novo_bytes + depois

    file_path.write_bytes(novo_content_bytes)
    return dist_antiga, dist_nova


def main():
    parser = argparse.ArgumentParser(description="Randomizador canônico de alternativas dos exercícios do Tutor Inteligente.")
    parser.add_argument("--seed", type=int, default=42, help="Semente determinística para reproducibilidade (default: 42).")
    parser.add_argument("--dry-run", action="store_true", help="Apenas exibe as estatísticas sem modificar os arquivos.")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    volumes_dir = BASE_DIR / "app" / "seeds" / "volumes"
    volume_files = sorted(volumes_dir.glob("vol_*.py"))

    print("================================================================================")
    print("      TUTOR INTELIGENTE — RANDOMIZADOR CANÔNICO DE ALTERNATIVAS")
    print(f"      Semente: {args.seed} | Modo: {'DRY-RUN (Simulação)' if args.dry_run else 'APLICAÇÃO DIRETA'}")
    print("================================================================================\n")

    total_dist_antiga: Counter = Counter()
    total_dist_nova: Counter = Counter()

    for vf in volume_files:
        if vf.name == "__init__.py":
            continue
        antiga, nova = processar_volume(vf, rng=rng, dry_run=args.dry_run)
        total_dist_antiga.update(antiga)
        total_dist_nova.update(nova)

        print(f"[{vf.name}]")
        print(f"  Anterior: {dict(sorted(antiga.items()))}")
        print(f"  Novo:     {dict(sorted(nova.items()))}")

    print("\n--------------------------------------------------------------------------------")
    print("DISTRIBUIÇÃO CONSOLIDADA GLOBAL (TODOS OS VOLUMES):")
    print("--------------------------------------------------------------------------------")
    print(f"Gabaritos Anteriores: {dict(sorted(total_dist_antiga.items()))}")
    total_ant = sum(total_dist_antiga.values())
    if total_ant > 0:
        for k in sorted(total_dist_antiga.keys()):
            pct = (total_dist_antiga[k] / total_ant) * 100
            print(f"  - Letra {k}: {total_dist_antiga[k]} itens ({pct:.1f}%)")

    print(f"\nGabaritos Novos Balanceados: {dict(sorted(total_dist_nova.items()))}")
    total_nov = sum(total_dist_nova.values())
    if total_nov > 0:
        for k in sorted(total_dist_nova.keys()):
            pct = (total_dist_nova[k] / total_nov) * 100
            print(f"  - Letra {k}: {total_dist_nova[k]} itens ({pct:.1f}%)")

    print("\n[SUCESSO] Operação de randomização concluída com sucesso!")


if __name__ == "__main__":
    main()
