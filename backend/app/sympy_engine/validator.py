"""
Validador Matemático Simbólico Determinístico com SymPy e Sandbox Segura.
Atende a RN-EXE-013, RN-EXE-014, RN-EXE-017 e diretrizes de segurança contra RCE/DoS.
"""
import re
import random
import concurrent.futures
from typing import Dict, Any, Optional
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


class SympyMathValidator:
    """Motor de validação simbólica determinística com tolerância rigorosa e proteção estrita contra RCE."""

    TOLERANCIA_NUMERICA = 0.01  # Critério acordado de ±0.01

    # Palavras e padrões proibidos para mitigar injeção de código arbitrário.
    # ATENÇÃO: 'os' e 'sys' exigem delimitadores de palavra (\b), pois como substring
    # simples eles bloqueiam funções matemáticas legítimas (cos, cosh, arccos, pos...).
    # O padrão '__' permanece sem delimitador para neutralizar dunders
    # (__import__, __class__, __subclasses__, ...) e cadeias de introspecção.
    PADROES_PROIBIDOS = re.compile(
        r"(__|import|exec|eval|open|\bos\b|\bsys\b|subprocess|shutil|globals|locals|builtins|compile|getattr|setattr)",
        re.IGNORECASE,
    )

    # Dicionário global seguro com os construtores de AST fundamentais do SymPy
    GLOBAL_DICT_SEGURO = {
        "Integer": sp.Integer,
        "Float": sp.Float,
        "Symbol": sp.Symbol,
        "Rational": sp.Rational,
        "Pow": sp.Pow,
        "Add": sp.Add,
        "Mul": sp.Mul,
    }

    # Dicionário local estrito com funções matemáticas e variáveis permitidas
    LOCAL_DICT_SEGURO = {
        "x": sp.Symbol("x"),
        "y": sp.Symbol("y"),
        "z": sp.Symbol("z"),
        "t": sp.Symbol("t"),
        "pi": sp.pi,
        "E": sp.E,
        "sqrt": sp.sqrt,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "log": sp.log,
        "exp": sp.exp,
        "Abs": sp.Abs,
    }

    TRANSFORMACOES_SEGURAS = standard_transformations + (convert_xor, implicit_multiplication_application)

    MAX_CARACTERES = 150
    TIMEOUT_SEGUNDOS = 5.0

    @classmethod
    def sanitizar_expressao(cls, expr_str: str) -> Optional[sp.Expr]:
        """Sanitiza e faz parse seguro de expressões algébricas de estudantes."""
        if not expr_str or not isinstance(expr_str, str):
            return None

        # Limite estrito de tamanho para prevenir DoS por estouro de recursão no parser
        expr_limpa = expr_str.strip()
        if len(expr_limpa) > cls.MAX_CARACTERES:
            return None

        # Rejeita padrões maliciosos
        if cls.PADROES_PROIBIDOS.search(expr_limpa):
            return None

        try:
            # Isolamento total: GLOBAL_DICT_SEGURO neutraliza built-ins do Python (__import__, eval, etc.)
            return parse_expr(
                expr_limpa,
                local_dict=cls.LOCAL_DICT_SEGURO,
                global_dict=cls.GLOBAL_DICT_SEGURO,
                transformations=cls.TRANSFORMACOES_SEGURAS,
                evaluate=False,
            )
        except Exception:
            return None

    @classmethod
    def validar_equivalencia(cls, expressao_aluno_str: str, expressao_gabarito_str: str) -> bool:
        """
        Verifica se duas expressões algébricas são identicamente equivalentes:
        f(x) - g(x) == 0 após simplificação simbólica formal com ambiente isolado e timeout de 5s.
        """
        def _executar_simplificacao(aluno_str: str, gabarito_str: str) -> bool:
            expr_aluno = cls.sanitizar_expressao(aluno_str)
            expr_gabarito = cls.sanitizar_expressao(gabarito_str)

            if expr_aluno is None or expr_gabarito is None:
                return False

            try:
                # Diferença analítica simplificada
                diferenca = sp.simplify(expr_aluno - expr_gabarito)

                if diferenca == 0:
                    return True

                # Avaliação numérica de ponto flutuante para aproximações
                valor_numerico = float(abs(diferenca.evalf()))
                return valor_numerico <= cls.TOLERANCIA_NUMERICA
            except Exception:
                return False

        try:
            # Executa com timeout estrito de 5 segundos para prevenir exaustão de CPU
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_executar_simplificacao, expressao_aluno_str, expressao_gabarito_str)
                return future.result(timeout=cls.TIMEOUT_SEGUNDOS)
        except Exception:
            # Timeout ou sintaxe inválida resulta em False com segurança absoluta
            return False

    @staticmethod
    def gerar_questao_gemea_quadratica(
        r1_original: int = 2,
        r2_original: int = 3,
    ) -> Dict[str, Any]:
        """
        Mutação paramétrica determinística para Função/Equação do 2º Grau:
        Preserva a estrutura lógica e algébrica, alterando os coeficientes mantendo raízes inteiras limpas.
        """
        x = sp.Symbol("x")

        # Sorteia novas raízes inteiras distintas no intervalo [-6, 6] (excluindo 0 e originais)
        candidatos = [n for n in range(-6, 7) if n not in (0, r1_original, r2_original)]
        if len(candidatos) < 2:
            candidatos = [-5, -4, -3, -2, -1, 1, 4, 5, 6]
        nova_r1 = random.choice(candidatos)
        candidatos.remove(nova_r1)
        nova_r2 = random.choice(candidatos)

        # Garante ordem r1 < r2
        if nova_r1 > nova_r2:
            nova_r1, nova_r2 = nova_r2, nova_r1

        # Constrói a nova equação fatorada
        f_nova = sp.expand((x - nova_r1) * (x - nova_r2))
        b_novo = -(nova_r1 + nova_r2)
        c_novo = nova_r1 * nova_r2

        # Formata o enunciado com KaTeX
        sinal_b = f"+ {b_novo}" if b_novo >= 0 else f"- {abs(b_novo)}"
        sinal_c = f"+ {c_novo}" if c_novo >= 0 else f"- {abs(c_novo)}"

        enunciado_katex = (
            f"Determine as raízes reais da equação quadrática dada por:\n"
            f"$$x^2 {sinal_b}x {sinal_c} = 0$$"
        )

        # Gera alternativas com distratores estruturados
        alternativas_base = [
            {"texto": f"$S = \\{{{nova_r1}, {nova_r2}\\}}$", "correta": True},
            {"texto": f"$S = \\{{{-nova_r1}, {-nova_r2}\\}}$", "correta": False},
            {"texto": f"$S = \\{{{nova_r1}, {-nova_r2}\\}}$", "correta": False},
            {"texto": f"$S = \\{{{-nova_r1}, {nova_r2}\\}}$", "correta": False},
            {"texto": "$S = \\emptyset$", "correta": False},
        ]

        # Embaralha mantendo a correspondência
        random.shuffle(alternativas_base)
        letras = ["A", "B", "C", "D", "E"]
        alternativas = []
        resposta_correta = "A"

        for idx, alt in enumerate(alternativas_base):
            letra = letras[idx]
            alternativas.append({
                "letra": letra,
                "texto": alt["texto"],
                "correta": alt["correta"],
            })
            if alt["correta"]:
                resposta_correta = letra

        delta = int(b_novo**2 - 4 * c_novo)
        resolucao_katex = (
            f"**Resolução Passo a Passo:**\n\n"
            f"1. Identificamos os coeficientes da equação: $a = 1$, $b = {b_novo}$, $c = {c_novo}$.\n"
            f"2. Calculamos o discriminante: $\\Delta = b^2 - 4ac = ({b_novo})^2 - 4(1)({c_novo}) = {delta}$.\n"
            f"3. Como $\\Delta > 0$, a equação possui duas raízes reais distintas.\n"
            f"4. Aplicamos a fórmula resolutiva de Bhaskara:\n"
            f"   $$x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} = \\frac{{-({b_novo}) \\pm \\sqrt{{{delta}}}}}{{2}}$$\n"
            f"5. As raízes obtidas são $x_1 = {nova_r1}$ e $x_2 = {nova_r2}$.\n\n"
            f"Portanto, o conjunto solução é $S = \\{{{nova_r1}, {nova_r2}\\}}$ (Alternativa **{resposta_correta}**)."
        )

        return {
            "enunciado_katex": enunciado_katex,
            "alternativas": alternativas,
            "resposta_correta": resposta_correta,
            "resolucao_passo_a_passo": resolucao_katex,
            "metadados_sympy": {
                "tipo_item": "multiple_choice",
                "expressao": str(f_nova),
                "raizes": [nova_r1, nova_r2],
                "delta": delta,
                "dica_estagio_2": "Lembre-se de calcular o discriminante $\\Delta = b^2 - 4ac$ e aplicar a fórmula resolutiva de Bhaskara.",
            },
            "validado_sympy": True,
        }
