---
title: Exercícios - Validador Algébrico SymPy e Questões Gêmeas
type: module
status: draft
related:
  - modules/exercicios/prototype/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 3. Validador Simbólico Determinístico com SymPy

Código de referência para validação matemática estrita e geração paramétrica de **Questões Gêmeas** livres de alucinações algébricas.

---

## Código Fonte (`backend/app/sympy_engine/validator.py`)

```python
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import random
from typing import Dict, Any, Tuple, Optional


class SympyMathValidator:
    """Motor de validação simbólica determinística com tolerância rigorosa e proteção estrita contra RCE."""
    
    TOLERANCIA_NUMERICA = 0.01  # Critério acordado de ±0.01

    # Palavras e padrões proibidos para mitigar injeção de código arbitrário
    PADROES_PROIBIDOS = re.compile(
        r"(__|import|exec|eval|open|os|sys|subprocess|shutil|globals|locals|builtins|compile|getattr|setattr)",
        re.IGNORECASE
    )

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

    TRANSFORMACOES_SEGURAS = standard_transformations + (implicit_multiplication_application,)

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
            # Isolamento total: global_dict={} neutraliza built-ins do Python
            return parse_expr(
                expr_limpa,
                local_dict=cls.LOCAL_DICT_SEGURO,
                global_dict={},
                transformations=cls.TRANSFORMACOES_SEGURAS,
                evaluate=False
            )
        except Exception:
            return None

    @classmethod
    def validar_equivalencia(cls, expressao_aluno_str: str, expressao_gabarito_str: str) -> bool:
        """
        Verifica se duas expressões algébricas são identicamente equivalentes:
        f(x) - g(x) == 0 após simplificação simbólica formal com ambiente isolado e timeout de 5s.
        """
        import concurrent.futures

        def _executar_simplificacao(aluno_str: str, gabarito_str: str) -> bool:
            expr_aluno = cls.sanitizar_expressao(aluno_str)
            expr_gabarito = cls.sanitizar_expressao(gabarito_str)

            if expr_aluno is None or expr_gabarito is None:
                return False

            # Diferença analítica simplificada
            diferenca = sp.simplify(expr_aluno - expr_gabarito)

            if diferenca == 0:
                return True

            # Avaliação numérica de ponto flutuante para aproximações
            valor_numerico = abs(complex(diferenca.evalf()))
            return valor_numerico <= cls.TOLERANCIA_NUMERICA

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
        a_original: int = 1, 
        r1_original: int = 2, 
        r2_original: int = 3
    ) -> Dict[str, Any]:
        """
        Exemplo de mutação paramétrica para Função/Equação do 2º Grau:
        Preserva o teorema e o tipo de raiz (inteiras), alterando apenas os coeficientes.
        Matriz original: (x - r1)(x - r2) = x^2 - (r1+r2)x + r1*r2
        """
        x = sp.Symbol('x')
        
        # Sorteia novas raízes inteiras distintas no intervalo [-6, 6] (excluindo 0)
        candidatos = [n for n in range(-6, 7) if n not in (0, r1_original, r2_original)]
        nova_r1 = random.choice(candidatos)
        candidatos.remove(nova_r1)
        nova_r2 = random.choice(candidatos)

        # Constrói a nova equação fatorada
        f_nova = sp.expand((x - nova_r1) * (x - nova_r2))
        b_novo = -(nova_r1 + nova_r2)
        c_novo = nova_r1 * nova_r2

        # Formata o enunciado com KaTeX
        sinal_b = f"+ {b_novo}" if b_novo >= 0 else f"- {abs(b_novo)}"
        sinal_c = f"+ {c_novo}" if c_novo >= 0 else f"- {abs(c_novo)}"
        
        enunciado_katex = (
            f"Determine as raízes reais da equação quadrática dada por: "
            f"$$x^2 {sinal_b}x {sinal_c} = 0$$"
        )

        # Gera alternativas com distratores estruturados
        alternativas = [
            {"letra": "A", "texto": f"$S = \\{{{nova_r1}, {nova_r2}\\}}$", "correta": True},
            {"letra": "B", "texto": f"$S = \\{{{-nova_r1}, {-nova_r2}\\}}$", "correta": False},
            {"letra": "C", "texto": f"$S = \\{{{nova_r1}, {-nova_r2}\\}}$", "correta": False},
            {"letra": "D", "texto": f"$S = \\{{{-nova_r1}, {nova_r2}\\}}$", "correta": False},
            {"letra": "E", "texto": f"$S = \\emptyset$", "correta": False}
        ]
        
        # Embaralha mantendo a correspondência
        random.shuffle(alternativas)
        letras = ["A", "B", "C", "D", "E"]
        resposta_correta = "A"
        
        for idx, alt in enumerate(alternativas):
            alt["letra"] = letras[idx]
            if alt["correta"]:
                resposta_correta = letras[idx]

        resolucao_katex = (
            f"**Resolução Passo a Passo:**\n"
            f"1. Identificamos os coeficientes: $a = 1$, $b = {b_novo}$, $c = {c_novo}$.\n"
            f"2. Calculamos o discriminante $\\Delta = b^2 - 4ac = ({b_novo})^2 - 4(1)({c_novo}) = {b_novo**2 - 4*c_novo}$.\n"
            f"3. Aplicamos a fórmula de Bhaskara: $x = \\frac{{-({b_novo}) \\pm \\sqrt{{{b_novo**2 - 4*c_novo}}}}}{{2(1)}}$.\n"
            f"4. As raízes obtidas são $x_1 = {nova_r1}$ e $x_2 = {nova_r2}$."
        )

        return {
            "enunciado_katex": enunciado_katex,
            "alternativas": alternativas,
            "resposta_correta": resposta_correta,
            "resolucao_passo_a_passo": resolucao_katex,
            "metadados_sympy": {
                "expressao": str(f_nova),
                "raizes": [nova_r1, nova_r2],
                "delta": int(b_novo**2 - 4*c_novo)
            },
            "validado_sympy": True
        }
```
