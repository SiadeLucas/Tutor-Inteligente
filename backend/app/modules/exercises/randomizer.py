"""
Módulo de Randomização e Balanceamento de Alternativas — Tutor Inteligente
Responsável por eliminar o vício de gabaritos fixos na alternativa "A" tanto
estaticamente nos dados dos volumes didáticos quanto dinamicamente na Prova CAT.
"""

from __future__ import annotations
import copy
import hashlib
import random
import re
from typing import Any, Dict, List, Optional, Tuple


LETRAS_PADRAO = ["A", "B", "C", "D", "E"]


def embaralhar_alternativas(
    alternativas: List[Dict[str, Any]],
    resposta_correta: Optional[str] = None,
    letra_alvo: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> Tuple[List[Dict[str, Any]], str, str]:
    """
    Embaralha uma lista de alternativas, reatribuindo as letras sequenciais (A, B, C, D, E).

    Se letra_alvo for fornecida (ex.: 'C'), garante que a alternativa correta seja
    alocada especificamente naquela letra, e os distratores sejam distribuídos
    nas demais posições. Caso contrário, realiza um sorteio aleatório usando rng.

    Retorna:
        Tuple[novas_alternativas, nova_letra_correta, letra_antiga]
    """
    if not alternativas:
        return [], resposta_correta or "A", resposta_correta or "A"

    if rng is None:
        rng = random.Random()

    total = len(alternativas)
    letras_disponiveis = LETRAS_PADRAO[:total] if total <= len(LETRAS_PADRAO) else [chr(ord('A') + i) for i in range(total)]

    # 1. Identifica a alternativa correta e a letra antiga
    idx_correta = -1
    letra_antiga = "A"

    # Primeiro tenta pelo booleano 'correta'
    for i, alt in enumerate(alternativas):
        if alt.get("correta") is True:
            idx_correta = i
            letra_antiga = str(alt.get("letra", "A")).strip().upper()
            break

    # Se não encontrou pelo booleano, tenta pela resposta_correta
    if idx_correta == -1 and resposta_correta:
        resp_clean = resposta_correta.strip().upper()
        for i, alt in enumerate(alternativas):
            if str(alt.get("letra", "")).strip().upper() == resp_clean:
                idx_correta = i
                letra_antiga = resp_clean
                break

    # Fallback seguro: se nenhuma alternativa for marcada, assume a primeira
    if idx_correta == -1:
        idx_correta = 0
        letra_antiga = str(alternativas[0].get("letra", "A")).strip().upper()

    alt_correta = copy.deepcopy(alternativas[idx_correta])
    distratores = [copy.deepcopy(alt) for i, alt in enumerate(alternativas) if i != idx_correta]

    # Embaralha os distratores
    rng.shuffle(distratores)

    # 2. Determina a posição da alternativa correta
    if letra_alvo and letra_alvo.upper() in letras_disponiveis:
        target_idx = letras_disponiveis.index(letra_alvo.upper())
    else:
        target_idx = rng.randint(0, total - 1)

    # 3. Monta a nova lista na ordem final
    nova_lista_base: List[Dict[str, Any]] = []
    distrator_iter = iter(distratores)
    for i in range(total):
        if i == target_idx:
            nova_lista_base.append(alt_correta)
        else:
            nova_lista_base.append(next(distrator_iter))

    # 4. Re-etiqueta com as novas letras e flags
    novas_alternativas: List[Dict[str, Any]] = []
    nova_letra_correta = letras_disponiveis[target_idx]

    for i, alt in enumerate(nova_lista_base):
        letra_atual = letras_disponiveis[i]
        eh_correta = (i == target_idx)
        novas_alternativas.append({
            "letra": letra_atual,
            "texto": alt["texto"],
            "correta": eh_correta,
        })

    return novas_alternativas, nova_letra_correta, letra_antiga


def atualizar_texto_resolucao(texto: str, letra_antiga: str, nova_letra: str) -> str:
    """
    Atualiza as referências ao gabarito no texto explicativo KaTeX (ex: 'Alternativa A.' -> 'Alternativa C.').
    Garante também que haja uma indicação clara da alternativa correta no final do texto.
    """
    if not texto:
        return f"Alternativa {nova_letra}."

    antiga_up = letra_antiga.strip().upper()
    nova_up = nova_letra.strip().upper()

    texto_atualizado = texto

    # Substituição padrão: 'Alternativa A' ou 'Alternativa A.'
    padrao_alt = re.compile(rf"\b(Alternativa|Letra)\s+{re.escape(antiga_up)}\b", re.IGNORECASE)
    if padrao_alt.search(texto_atualizado):
        texto_atualizado = padrao_alt.sub(rf"\g<1> {nova_up}", texto_atualizado)
    else:
        # Se não encontrou "Alternativa {antiga}", mas há qualquer "Alternativa [A-E]" no texto
        padrao_qualquer_alt = re.compile(r"\b(Alternativa|Letra)\s+[A-E]\b", re.IGNORECASE)
        if padrao_qualquer_alt.search(texto_atualizado):
            texto_atualizado = padrao_qualquer_alt.sub(rf"\g<1> {nova_up}", texto_atualizado)
        else:
            # Não continha menção explícita à alternativa: anexa ao final
            texto_limpo = texto_atualizado.rstrip()
            if not texto_limpo.endswith("."):
                texto_atualizado = f"{texto_limpo}. Alternativa {nova_up}."
            else:
                texto_atualizado = f"{texto_limpo} Alternativa {nova_up}."

    return texto_atualizado


def randomizar_item_exercicio(
    item: Dict[str, Any],
    letra_alvo: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> Dict[str, Any]:
    """
    Aplica randomização em um dicionário de item de exercício.
    Itens do tipo 'numeric_input' ou sem alternativas permanecem inalterados.
    """
    tipo_item = item.get("tipo_item", "multiple_choice")
    alternativas = item.get("alternativas")

    if tipo_item != "multiple_choice" or not alternativas:
        return item

    novas_alts, nova_letra, letra_antiga = embaralhar_alternativas(
        alternativas=alternativas,
        resposta_correta=item.get("resposta_correta"),
        letra_alvo=letra_alvo,
        rng=rng,
    )

    item["alternativas"] = novas_alts
    item["resposta_correta"] = nova_letra

    if "resolucao_passo_a_passo" in item:
        item["resolucao_passo_a_passo"] = atualizar_texto_resolucao(
            item["resolucao_passo_a_passo"], letra_antiga, nova_letra
        )

    if "explicacao_katex" in item:
        item["explicacao_katex"] = atualizar_texto_resolucao(
            item["explicacao_katex"], letra_antiga, nova_letra
        )

    return item


def balancear_itens(itens: List[Dict[str, Any]], seed: int = 42) -> List[Dict[str, Any]]:
    """
    Distribui uniformemente as alternativas corretas de uma coleção de itens
    entre as letras A, B, C, D e E (aprox. 20% para cada letra).
    """
    rng = random.Random(seed)

    itens_mc = [it for it in itens if it.get("tipo_item", "multiple_choice") == "multiple_choice" and it.get("alternativas")]
    total_mc = len(itens_mc)

    if total_mc == 0:
        return itens

    # Gera a fila equilibrada de letras destino
    letras_fila: List[str] = []
    while len(letras_fila) < total_mc:
        bloco = LETRAS_PADRAO.copy()
        rng.shuffle(bloco)
        letras_fila.extend(bloco)

    letras_fila = letras_fila[:total_mc]
    rng.shuffle(letras_fila)

    fila_iter = iter(letras_fila)
    for it in itens:
        if it.get("tipo_item", "multiple_choice") == "multiple_choice" and it.get("alternativas"):
            letra_alvo = next(fila_iter)
            randomizar_item_exercicio(it, letra_alvo=letra_alvo, rng=rng)

    return itens


def obter_alternativas_randomizadas_cat(
    alternativas: List[Dict[str, Any]],
    resposta_correta_db: str,
    sessao_id: str,
    item_id: str,
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Gera alternativas randomizadas deterministicamente para uma sessão CAT.
    A semente é derivada do hash SHA-256 de f'{sessao_id}:{item_id}'.
    Garante que recarregamentos da página pelo aluno mantenham exatamente
    a mesma ordem sem necessidade de persistir estado no banco.
    """
    seed_str = f"{sessao_id}:{item_id}"
    seed_int = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:16], 16)
    rng = random.Random(seed_int)

    novas_alts, nova_letra, _ = embaralhar_alternativas(
        alternativas=alternativas,
        resposta_correta=resposta_correta_db,
        rng=rng,
    )
    return novas_alts, nova_letra
