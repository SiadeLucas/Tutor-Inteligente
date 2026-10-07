"""
Módulo de Formatação e Sanitização Matemática — Tutor Inteligente
Fornece utilitários para conversão e padronização de expressões KaTeX,
especialmente a substituição de radicais (\\sqrt) por expoentes fracionários (RN-EXE-017).
"""
from __future__ import annotations
import re
from typing import Tuple


def extrair_bloco_chaves(texto: str, pos_inicio: int) -> Tuple[str, int]:
    """
    A partir de pos_inicio (onde texto[pos_inicio] == '{'),
    encontra o fechamento correspondente '}' considerando chaves aninhadas.
    Retorna (conteudo_interno, pos_fechamento_exclusivo).
    """
    if texto[pos_inicio] != '{':
        raise ValueError(f"Esperado '{{' em {pos_inicio}")
    nivel = 1
    i = pos_inicio + 1
    tamanho = len(texto)
    while i < tamanho and nivel > 0:
        c = texto[i]
        if c == '{':
            nivel += 1
        elif c == '}':
            nivel -= 1
        i += 1
    if nivel != 0:
        raise ValueError(f"Chaves desbalanceadas a partir da posição {pos_inicio}")
    return texto[pos_inicio + 1 : i - 1], i


def extrair_bloco_colchetes(texto: str, pos_inicio: int) -> Tuple[str, int]:
    """
    Extrai bloco [...] correspondente ao índice de raiz em \\sqrt[n]{x}.
    Retorna (conteudo_interno, pos_fechamento_exclusivo).
    """
    if texto[pos_inicio] != '[':
        raise ValueError(f"Esperado '[' em {pos_inicio}")
    nivel = 1
    i = pos_inicio + 1
    tamanho = len(texto)
    while i < tamanho and nivel > 0:
        c = texto[i]
        if c == '[':
            nivel += 1
        elif c == ']':
            nivel -= 1
        i += 1
    if nivel != 0:
        raise ValueError(f"Colchetes desbalanceados a partir da posição {pos_inicio}")
    return texto[pos_inicio + 1 : i - 1], i


def converter_raiz_em_exponencial(texto: str) -> str:
    """
    Substitui recursivamente todas as raízes \\sqrt e \\sqrt[n] pela forma exponencial fracionária.
    Preserva parênteses e insere multiplicação explícita (\\cdot) quando precedida por número ou variável.

    Exemplos:
      \\sqrt{2} -> 2^{1/2}
      4\\sqrt{2} -> 4 \\cdot 2^{1/2}
      4 \\sqrt{2} -> 4 \\cdot 2^{1/2}
      \\cdot\\sqrt{2} -> \\cdot 2^{1/2}
      \\frac{\\sqrt{3}}{2} -> \\frac{3^{1/2}}{2}
      \\pm \\sqrt{\\Delta} -> \\pm \\Delta^{1/2}
      l\\sqrt{3} -> l \\cdot 3^{1/2}
      \\sqrt{3x - 12} -> (3x - 12)^{1/2}
      \\sqrt[3]{8} -> 8^{1/3}
      \\sqrt{(-2)^2 + (2\\sqrt{3})^2} -> ((-2)^2 + (2 \\cdot 3^{1/2})^2)^{1/2}
    """
    if not texto or r"\sqrt" not in texto:
        return texto

    idx_sqrt = texto.rfind(r"\sqrt")
    if idx_sqrt == -1:
        return texto

    pos_depois_sqrt = idx_sqrt + 5  # len(r"\sqrt") == 5
    indice = "2"
    pos_chave = pos_depois_sqrt

    # Pula espaços em branco entre \sqrt e os delimitadores [ ou {
    while pos_chave < len(texto) and texto[pos_chave].isspace():
        pos_chave += 1

    # Verifica se há índice nos colchetes: \sqrt[n]{x}
    if pos_chave < len(texto) and texto[pos_chave] == '[':
        try:
            indice_bruto, pos_depois_colchete = extrair_bloco_colchetes(texto, pos_chave)
            indice = indice_bruto.strip()
            pos_chave = pos_depois_colchete
            while pos_chave < len(texto) and texto[pos_chave].isspace():
                pos_chave += 1
        except ValueError:
            # Caso os colchetes estejam malformados, continua sem índice
            pass

    if pos_chave >= len(texto) or texto[pos_chave] != '{':
        # Não é um \sqrt com chaves bem formadas
        prefixo = converter_raiz_em_exponencial(texto[:idx_sqrt])
        return prefixo + texto[idx_sqrt:]

    try:
        radicando_bruto, pos_fim = extrair_bloco_chaves(texto, pos_chave)
    except ValueError:
        # Se chaves estiverem desbalanceadas, processa o restante antes de idx_sqrt
        prefixo = converter_raiz_em_exponencial(texto[:idx_sqrt])
        return prefixo + texto[idx_sqrt:]

    # Converte recursivamente dentro do radicando (suporte a raízes aninhadas)
    radicando = converter_raiz_em_exponencial(radicando_bruto)

    rad_strip = radicando.strip()
    tem_parenteses_externos = (
        rad_strip.startswith("(") and rad_strip.endswith(")")
        and rad_strip.count("(") == rad_strip.count(")")
    )

    eh_simples = (
        re.fullmatch(r"[0-9]+", rad_strip)
        or re.fullmatch(r"[a-zA-Z]", rad_strip)
        or re.fullmatch(r"\\[a-zA-Z]+", rad_strip)
    )

    if eh_simples or tem_parenteses_externos:
        base_exp = rad_strip
    else:
        base_exp = f"({rad_strip})"

    if indice == "2":
        exp_str = "^{1/2}"
    else:
        exp_str = f"^{{1/{indice}}}"

    substituicao = f"{base_exp}{exp_str}"

    prefixo_tudo = texto[:idx_sqrt]
    pref_strip = prefixo_tudo.rstrip()

    if pref_strip and re.search(r"\\[a-zA-Z]+$", pref_strip):
        # Termina com comando LaTeX (ex: \cdot, \pm): garante espaço separador se não houver
        prefixo_ajustado = pref_strip + " "
    elif (
        pref_strip
        and pref_strip[-1] not in "+-*/=<>~([{|&^,:;?!$"
        and (pref_strip[-1].isalnum() or pref_strip.endswith(")"))
    ):
        # Termina com dígito, variável ou parêntese fechado: insere multiplicação explícita
        prefixo_ajustado = pref_strip + " \\cdot "
    else:
        prefixo_ajustado = prefixo_tudo

    texto_atualizado = prefixo_ajustado + substituicao + texto[pos_fim:]
    return converter_raiz_em_exponencial(texto_atualizado)
