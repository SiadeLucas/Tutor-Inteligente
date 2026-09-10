"""
Script de População de Exercícios Calibrados (TRI 3PL) — Tutor Inteligente.
Cria itens de fixação e itens calibrados para o CAT referentes ao Volume 1 (Conjuntos e Funções).
"""
import asyncio
import uuid
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.content import Capitulo, VolumeDidatico
from app.models.exercise import ItemExercicio


ITENS_CALIBRADOS = [
    # --- Capítulo 4 / 5 / 6: Funções Afim e Quadrática ---
    {
        "titulo_capitulo": "Função Afim (1º Grau) e Variação",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Seja a função real afim dada por $f(x) = 3x - 12$. Determine o ponto onde o gráfico de $f(x)$ intersecta o eixo das abscissas (zero da função).",
        "alternativas": [
            {"letra": "A", "texto": "$x = 4$", "correta": True},
            {"letra": "B", "texto": "$x = -4$", "correta": False},
            {"letra": "C", "texto": "$x = 12$", "correta": False},
            {"letra": "D", "texto": "$x = 3$", "correta": False},
            {"letra": "E", "texto": "$x = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Para encontrar a interseção com o eixo das abscissas ($Ox$), fazemos $f(x) = 0$.\n"
            "2. $3x - 12 = 0 \\implies 3x = 12$.\n"
            "3. $x = \\frac{12}{3} = 4$.\n"
            "4. Logo, a raiz da função é $x = 4$ (Alternativa A)."
        ),
        "parametro_a": 1.200,
        "parametro_b": -1.500,  # Fácil
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Para achar a raiz de uma função afim $f(x) = ax + b$, basta igualar $f(x) = 0$ e isolar a incógnita $x$.",
        },
    },
    {
        "titulo_capitulo": "Função Afim (1º Grau) e Variação",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Uma reta passa pelos pontos $A(1, 3)$ e $B(3, 7)$. O coeficiente angular ($m$) dessa reta vale:",
        "alternativas": [
            {"letra": "A", "texto": "$m = 1$", "correta": False},
            {"letra": "B", "texto": "$m = 2$", "correta": True},
            {"letra": "C", "texto": "$m = 3$", "correta": False},
            {"letra": "D", "texto": "$m = 4$", "correta": False},
            {"letra": "E", "texto": "$m = \\frac{1}{2}$", "correta": False},
        ],
        "resposta_correta": "B",
        "resolucao_passo_a_passo": (
            "1. O coeficiente angular é dado pela razão da variação: $m = \\frac{y_B - y_A}{x_B - x_A}$.\n"
            "2. Substituindo os pontos: $m = \\frac{7 - 3}{3 - 1} = \\frac{4}{2} = 2$.\n"
            "3. Logo, o coeficiente angular é $m = 2$ (Alternativa B)."
        ),
        "parametro_a": 1.100,
        "parametro_b": -0.800,  # Médio-Fácil
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Lembre-se da taxa de variação média: $m = \\frac{\\Delta y}{\\Delta x} = \\frac{y_2 - y_1}{x_2 - x_1}$.",
        },
    },
    {
        "titulo_capitulo": "Função Quadrática (2º Grau) e Vértice da Parábola",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Dada a função quadrática $f(x) = x^2 - 6x + 8$, determine as coordenadas do seu vértice $V(x_v, y_v)$.",
        "alternativas": [
            {"letra": "A", "texto": "$V(3, -1)$", "correta": True},
            {"letra": "B", "texto": "$V(3, 1)$", "correta": False},
            {"letra": "C", "texto": "$V(-3, -1)$", "correta": False},
            {"letra": "D", "texto": "$V(6, 8)$", "correta": False},
            {"letra": "E", "texto": "$V(2, 4)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Identificamos os coeficientes: $a = 1$, $b = -6$, $c = 8$.\n"
            "2. A abscissa do vértice é: $x_v = -\\frac{b}{2a} = -\\frac{-6}{2(1)} = 3$.\n"
            "3. O valor do discriminante é: $\\Delta = b^2 - 4ac = (-6)^2 - 4(1)(8) = 36 - 32 = 4$.\n"
            "4. A ordenada do vértice é: $y_v = -\\frac{\\Delta}{4a} = -\\frac{4}{4(1)} = -1$.\n"
            "5. Portanto, o vértice é o ponto $V(3, -1)$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 0.000,  # Médio
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "raizes": [2, 4],
            "dica_estagio_2": "Utilize as fórmulas das coordenadas do vértice: $x_v = -\\frac{b}{2a}$ e $y_v = f(x_v) = -\\frac{\\Delta}{4a}$.",
        },
    },
    {
        "titulo_capitulo": "Função Quadrática (2º Grau) e Vértice da Parábola",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Qual é o valor máximo assumido pela função real $g(x) = -2x^2 + 8x - 3$?",
        "alternativas": [
            {"letra": "A", "texto": "$g_{\\max} = 5$", "correta": True},
            {"letra": "B", "texto": "$g_{\\max} = 2$", "correta": False},
            {"letra": "C", "texto": "$g_{\\max} = 8$", "correta": False},
            {"letra": "D", "texto": "$g_{\\max} = -3$", "correta": False},
            {"letra": "E", "texto": "$g_{\\max} = 10$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Como $a = -2 < 0$, a concavidade da parábola é voltada para baixo, possuindo valor máximo em seu vértice.\n"
            "2. $x_v = -\\frac{b}{2a} = -\\frac{8}{2(-2)} = 2$.\n"
            "3. O valor máximo é a ordenada $y_v = g(x_v) = -2(2)^2 + 8(2) - 3 = -8 + 16 - 3 = 5$.\n"
            "4. Logo, o valor máximo é 5 (Alternativa A)."
        ),
        "parametro_a": 1.500,
        "parametro_b": 0.700,  # Médio-Difícil
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Quando $a < 0$, o valor máximo da função ocorre no vértice: $y_v = g(x_v)$.",
        },
    },
    {
        "titulo_capitulo": "Função Quadrática (2º Grau) e Vértice da Parábola",
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": "Determine a soma das raízes da equação quadrática $2x^2 - 10x + 12 = 0$. Digite o valor numérico exato.",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": (
            "1. Pelas relações de Girard (Soma e Produto): $S = x_1 + x_2 = -\\frac{b}{a}$.\n"
            "2. Aqui, $a = 2$ e $b = -10$.\n"
            "3. Logo, $S = -\\frac{-10}{2} = 5$."
        ),
        "parametro_a": 1.300,
        "parametro_b": 0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {
            "tipo_item": "numeric_input",
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Lembre-se da relação de Girard para a soma das raízes: $S = -\\frac{b}{a}$.",
        },
    },
    {
        "titulo_capitulo": "Conceito Geral de Função e Gráficos",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Seja $f: \\mathbb{R} \\to \\mathbb{R}$ dada por $f(x) = 2x + 1$ e $g(x) = x^2$. O valor da função composta $(f \\circ g)(3)$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$19$", "correta": True},
            {"letra": "B", "texto": "$49$", "correta": False},
            {"letra": "C", "texto": "$7$", "correta": False},
            {"letra": "D", "texto": "$18$", "correta": False},
            {"letra": "E", "texto": "$37$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. A composta $(f \\circ g)(3)$ significa $f(g(3))$.\n"
            "2. Primeiro calculamos $g(3) = 3^2 = 9$.\n"
            "3. Em seguida, aplicamos $f(9) = 2(9) + 1 = 18 + 1 = 19$.\n"
            "4. Logo, a resposta é 19 (Alternativa A)."
        ),
        "parametro_a": 1.600,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Avalie a função de dentro primeiro: $(f \\circ g)(x) = f(g(x))$. Calcule $g(3)$ e substitua em $f$.",
        },
    },
    {
        "titulo_capitulo": "Conjuntos e Operações Fundamentais",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Sejam os conjuntos $A = \\{1, 2, 3, 4, 5\\}$ e $B = \\{3, 4, 5, 6, 7\\}$. O número de elementos de $(A \\cup B) - (A \\cap B)$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$4$", "correta": True},
            {"letra": "B", "texto": "$7$", "correta": False},
            {"letra": "C", "texto": "$3$", "correta": False},
            {"letra": "D", "texto": "$2$", "correta": False},
            {"letra": "E", "texto": "$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. $A \\cup B = \\{1, 2, 3, 4, 5, 6, 7\\}$, possuindo 7 elementos.\n"
            "2. $A \\cap B = \\{3, 4, 5\\}$, possuindo 3 elementos.\n"
            "3. A diferença $(A \\cup B) - (A \\cap B) = \\{1, 2, 6, 7\\}$, que é a diferença simétrica $A \\Delta B$.\n"
            "4. O conjunto resultante possui exatamente 4 elementos (Alternativa A)."
        ),
        "parametro_a": 1.250,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Determine primeiro os elementos da união e da interseção, e subtraia os elementos que estão em ambos.",
        },
    },
    {
        "titulo_capitulo": "Função Modular e Equações",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "O conjunto solução da equação modular $|2x - 6| = 8$ em $\\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$S = \\{-1, 7\\}$", "correta": True},
            {"letra": "B", "texto": "$S = \\{1, 7\\}$", "correta": False},
            {"letra": "C", "texto": "$S = \\{-7, 1\\}$", "correta": False},
            {"letra": "D", "texto": "$S = \\{7\\}$", "correta": False},
            {"letra": "E", "texto": "$S = \\emptyset$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Pela definição de módulo, $|y| = k \\iff y = k$ ou $y = -k$ (para $k \\ge 0$).\n"
            "2. Caso 1: $2x - 6 = 8 \\implies 2x = 14 \\implies x = 7$.\n"
            "3. Caso 2: $2x - 6 = -8 \\implies 2x = -2 \\implies x = -1$.\n"
            "4. Logo, $S = \\{-1, 7\\}$ (Alternativa A)."
        ),
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Lembre-se de abrir a equação modular em dois casos: $2x - 6 = 8$ e $2x - 6 = -8$.",
        },
    },
    {
        "titulo_capitulo": "Função Inversa e Composição",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "A lei da função inversa $f^{-1}(x)$ da função bijetora $f: \\mathbb{R} \\to \\mathbb{R}$ definida por $f(x) = 5x - 3$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$f^{-1}(x) = \\frac{x + 3}{5}$", "correta": True},
            {"letra": "B", "texto": "$f^{-1}(x) = \\frac{x - 3}{5}$", "correta": False},
            {"letra": "C", "texto": "$f^{-1}(x) = 5x + 3$", "correta": False},
            {"letra": "D", "texto": "$f^{-1}(x) = \\frac{5}{x + 3}$", "correta": False},
            {"letra": "E", "texto": "$f^{-1}(x) = 3x - 5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Escrevemos $y = 5x - 3$.\n"
            "2. Permutamos as variáveis $x$ e $y$: $x = 5y - 3$.\n"
            "3. Isolamos $y$: $5y = x + 3 \\implies y = \\frac{x + 3}{5}$.\n"
            "4. Portanto, $f^{-1}(x) = \\frac{x + 3}{5}$ (Alternativa A)."
        ),
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Para encontrar a função inversa, troque $x$ por $y$ e resolva para a nova variável $y$.",
        },
    },
    {
        "titulo_capitulo": "Noções de Lógica e Proposições",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "A negação lógica da proposição condicional $p \\to q$ é logicamente equivalente a:",
        "alternativas": [
            {"letra": "A", "texto": "$p \\land \\neg q$", "correta": True},
            {"letra": "B", "texto": "$\\neg p \\lor q$", "correta": False},
            {"letra": "C", "texto": "$\\neg p \\land \\neg q$", "correta": False},
            {"letra": "D", "texto": "$q \\to p$", "correta": False},
            {"letra": "E", "texto": "$\\neg p \\to \\neg q$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Sabemos que a condicional $p \\to q$ é equivalente a $\\neg p \\lor q$.\n"
            "2. Pela Lei de De Morgan, a negação $\\neg(p \\to q) \\equiv \\neg(\\neg p \\lor q) \\equiv \\neg(\\neg p) \\land \\neg q \\equiv p \\land \\neg q$.\n"
            "3. Logo, nega-se mantendo o antecedente e negando o consequente (Alternativa A)."
        ),
        "parametro_a": 1.150,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "A negação de 'Se P então Q' é 'P e não Q' (regra do Mané: MANTÉM o primeiro E NEGA o segundo).",
        },
    },
    # --- Itens com dificuldade mais alta para o topo da escala CAT ---
    {
        "titulo_capitulo": "Função Quadrática (2º Grau) e Vértice da Parábola",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Para quais valores reais do parâmetro $k$ a equação quadrática $x^2 - 2(k - 1)x + (k^2 - 2k) = 0$ admite duas raízes reais e distintas?",
        "alternativas": [
            {"letra": "A", "texto": "Para todo $k \\in \\mathbb{R}$", "correta": True},
            {"letra": "B", "texto": "$k > 1$", "correta": False},
            {"letra": "C", "texto": "$k < 0$", "correta": False},
            {"letra": "D", "texto": "$k = 2$", "correta": False},
            {"letra": "E", "texto": "Nenhum valor real de $k$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Para admitir raízes reais e distintas, devemos impor $\\Delta > 0$.\n"
            "2. $\\Delta = b^2 - 4ac = [-2(k - 1)]^2 - 4(1)(k^2 - 2k) = 4(k^2 - 2k + 1) - 4k^2 + 8k$.\n"
            "3. $\\Delta = 4k^2 - 8k + 4 - 4k^2 + 8k = 4$.\n"
            "4. Como $\\Delta = 4 > 0$ independentemente do valor de $k$, a condição é satisfeita para todo $k \\in \\mathbb{R}$ (Alternativa A)."
        ),
        "parametro_a": 1.800,
        "parametro_b": 1.600,  # Difícil
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Calcule a expressão do discriminante $\\Delta = b^2 - 4ac$ em termos de $k$ e simplifique os termos algébricos.",
        },
    },
    {
        "titulo_capitulo": "Função Afim (1º Grau) e Variação",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Considere as funções $f(x) = 2x - 5$ e $g(x) = -x + 4$. A solução da inequação produto $f(x) \\cdot g(x) \\ge 0$ no conjunto dos números reais é:",
        "alternativas": [
            {"letra": "A", "texto": "$S = \\{x \\in \\mathbb{R} \\mid \\frac{5}{2} \\le x \\le 4\\}$", "correta": True},
            {"letra": "B", "texto": "$S = \\{x \\in \\mathbb{R} \\mid x \\le \\frac{5}{2} \\text{ ou } x \\ge 4\\}$", "correta": False},
            {"letra": "C", "texto": "$S = \\{x \\in \\mathbb{R} \\mid -4 \\le x \\le \\frac{5}{2}\\}$", "correta": False},
            {"letra": "D", "texto": "$S = \\mathbb{R}$", "correta": False},
            {"letra": "E", "texto": "$S = \\emptyset$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. As raízes dos fatores são: $f(x) = 0 \\implies x = 5/2 = 2.5$; $g(x) = 0 \\implies x = 4$.\n"
            "2. O produto $(2x - 5)(-x + 4) = -2x^2 + 13x - 20$ é uma parábola com concavidade voltada para baixo ($a = -2 < 0$).\n"
            "3. O sinal é não-negativo ($\ge 0$) no intervalo compreendido entre as raízes.\n"
            "4. Logo, $\\frac{5}{2} \\le x \\le 4$ (Alternativa A)."
        ),
        "parametro_a": 1.700,
        "parametro_b": 1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_funcoes",
            "dica_estagio_2": "Faça o quadro de sinais para o produto dos fatores lineares $2x - 5$ e $-x + 4$.",
        },
    },
    # ===========================================================================
    # GEOMETRIA (Plana e Espacial) — cobertura da Grande Área no banco CAT
    # ===========================================================================
    {
        "titulo_capitulo": "Relações Métricas no Triângulo Retângulo e Pitágoras",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Um triângulo retângulo possui catetos medindo $6\\,\\text{cm}$ e $8\\,\\text{cm}$. Qual é a medida da hipotenusa, em centímetros?",
        "alternativas": [
            {"letra": "A", "texto": "$10\\,\\text{cm}$", "correta": True},
            {"letra": "B", "texto": "$12\\,\\text{cm}$", "correta": False},
            {"letra": "C", "texto": "$14\\,\\text{cm}$", "correta": False},
            {"letra": "D", "texto": "$9\\,\\text{cm}$", "correta": False},
            {"letra": "E", "texto": "$7\\,\\text{cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Pelo Teorema de Pitágoras: $h^2 = c_1^2 + c_2^2$.\n"
            "2. Substituindo: $h^2 = 6^2 + 8^2 = 36 + 64 = 100$.\n"
            "3. Logo, $h = \\sqrt{100} = 10\\,\\text{cm}$ (Alternativa A)."
        ),
        "parametro_a": 1.300,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "geometria",
            "dica_estagio_2": "Aplique o Teorema de Pitágoras: a hipotenusa ao quadrado é a soma dos quadrados dos catetos.",
        },
    },
    {
        "titulo_capitulo": "Áreas das Principais Figuras Planas e do Círculo",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Qual é a área de um círculo de raio $6\\,\\text{cm}$, em função de $\\pi$?",
        "alternativas": [
            {"letra": "A", "texto": "$36\\pi\\,\\text{cm}^2$", "correta": True},
            {"letra": "B", "texto": "$12\\pi\\,\\text{cm}^2$", "correta": False},
            {"letra": "C", "texto": "$18\\pi\\,\\text{cm}^2$", "correta": False},
            {"letra": "D", "texto": "$6\\pi\\,\\text{cm}^2$", "correta": False},
            {"letra": "E", "texto": "$72\\pi\\,\\text{cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. A área do círculo é dada por $A = \\pi r^2$.\n"
            "2. Com $r = 6$: $A = \\pi \\cdot 6^2 = 36\\pi\\,\\text{cm}^2$ (Alternativa A)."
        ),
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "geometria",
            "dica_estagio_2": "Lembre-se: $A = \\pi r^2$ (área) e $C = 2\\pi r$ (comprimento). Não confunda as duas fórmulas.",
        },
    },
    {
        "titulo_capitulo": "Semelhança de Triângulos e Teorema de Tales",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Uma reta paralela ao lado $BC$ do triângulo $ABC$ corta o lado $AB$ em $D$ e o lado $AC$ em $E$. Se $AD = 6$, $DB = 3$ e $AE = 8$, o comprimento do segmento $EC$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$EC = 4$", "correta": True},
            {"letra": "B", "texto": "$EC = 6$", "correta": False},
            {"letra": "C", "texto": "$EC = 12$", "correta": False},
            {"letra": "D", "texto": "$EC = 3$", "correta": False},
            {"letra": "E", "texto": "$EC = 5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Pelo Teorema de Tales: $\\frac{AD}{DB} = \\frac{AE}{EC}$.\n"
            "2. Substituindo: $\\frac{6}{3} = \\frac{8}{EC} \\implies 2 = \\frac{8}{EC}$.\n"
            "3. Logo, $EC = \\frac{8}{2} = 4$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "geometria",
            "dica_estagio_2": "O Teorema de Tales garante a proporção $\\frac{AD}{DB} = \\frac{AE}{EC}$ quando a reta é paralela ao terceiro lado.",
        },
    },
    {
        "titulo_capitulo": "A Esfera e Suas Partes: Área e Volume",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "O volume de uma esfera de raio $3\\,\\text{cm}$, em função de $\\pi$, é:",
        "alternativas": [
            {"letra": "A", "texto": "$36\\pi\\,\\text{cm}^3$", "correta": True},
            {"letra": "B", "texto": "$12\\pi\\,\\text{cm}^3$", "correta": False},
            {"letra": "C", "texto": "$27\\pi\\,\\text{cm}^3$", "correta": False},
            {"letra": "D", "texto": "$108\\pi\\,\\text{cm}^3$", "correta": False},
            {"letra": "E", "texto": "$9\\pi\\,\\text{cm}^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. O volume da esfera é $V = \\frac{4}{3}\\pi r^3$.\n"
            "2. Com $r = 3$: $V = \\frac{4}{3}\\pi \\cdot 27 = 36\\pi\\,\\text{cm}^3$ (Alternativa A)."
        ),
        "parametro_a": 1.500,
        "parametro_b": 1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "geometria",
            "dica_estagio_2": "Aplique $V = \\frac{4}{3}\\pi r^3$. Atenção: o raio é elevado ao cubo no cálculo do volume.",
        },
    },
    # ===========================================================================
    # APLICADA — Combinatória e Probabilidade (Vol 5)
    # ===========================================================================
    {
        "titulo_capitulo": "Princípio Fundamental da Contagem (PFC)",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Uma pessoa possui $4$ camisetas e $3$ calças distintas. De quantas maneiras diferentes ela pode se vestir escolhendo uma camiseta e uma calça?",
        "alternativas": [
            {"letra": "A", "texto": "$12$", "correta": True},
            {"letra": "B", "texto": "$7$", "correta": False},
            {"letra": "C", "texto": "$24$", "correta": False},
            {"letra": "D", "texto": "$10$", "correta": False},
            {"letra": "E", "texto": "$34$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Pelo Princípio Fundamental da Contagem, escolhas sucessivas se multiplicam.\n"
            "2. Total $= 4 \\times 3 = 12$ maneiras (Alternativa A)."
        ),
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "O PFC diz que decisões independentes em sequência se multiplicam: multiplique as opções de cada escolha.",
        },
    },
    {
        "titulo_capitulo": "Arranjos e Permutações Simples e com Repetição",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "De quantas maneiras distintas $5$ pessoas podem se posicionar em uma fila indiana?",
        "alternativas": [
            {"letra": "A", "texto": "$120$", "correta": True},
            {"letra": "B", "texto": "$25$", "correta": False},
            {"letra": "C", "texto": "$60$", "correta": False},
            {"letra": "D", "texto": "$24$", "correta": False},
            {"letra": "E", "texto": "$720$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. O número de permutações de $n$ elementos distintos é $P_n = n!$.\n"
            "2. Para $n = 5$: $P_5 = 5! = 5 \\cdot 4 \\cdot 3 \\cdot 2 \\cdot 1 = 120$ (Alternativa A)."
        ),
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Permutação simples de $n$ pessoas em fila é $n!$: multiplique todos os inteiros de $n$ até $1$.",
        },
    },
    {
        "titulo_capitulo": "Combinações Simples e Problemas de Escolha",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Quantas comissões distintas de $3$ pessoas podem ser formadas a partir de um grupo de $10$ pessoas?",
        "alternativas": [
            {"letra": "A", "texto": "$120$", "correta": True},
            {"letra": "B", "texto": "$720$", "correta": False},
            {"letra": "C", "texto": "$30$", "correta": False},
            {"letra": "D", "texto": "$1000$", "correta": False},
            {"letra": "E", "texto": "$360$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Como a ordem não importa (comissão), usamos combinação: $C_{10,3} = \\frac{10!}{3!\\,7!}$.\n"
            "2. $C_{10,3} = \\frac{10 \\cdot 9 \\cdot 8}{3 \\cdot 2 \\cdot 1} = \\frac{720}{6} = 120$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Se a ordem não importa (formar grupo), use $C_{n,p} = \\frac{n!}{p!(n-p)!}$.",
        },
    },
    {
        "titulo_capitulo": "Conceito de Probabilidade e Espaço Amostral",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Lançando-se simultaneamente dois dados honestos de $6$ faces, a probabilidade de a soma dos resultados ser igual a $7$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$\\frac{1}{6}$", "correta": True},
            {"letra": "B", "texto": "$\\frac{1}{12}$", "correta": False},
            {"letra": "C", "texto": "$\\frac{7}{36}$", "correta": False},
            {"letra": "D", "texto": "$\\frac{1}{9}$", "correta": False},
            {"letra": "E", "texto": "$\\frac{5}{36}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. O espaço amostral tem $6 \\times 6 = 36$ resultados equiprováveis.\n"
            "2. Os pares com soma $7$ são: $(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)$ — $6$ casos favoráveis.\n"
            "3. $P = \\frac{6}{36} = \\frac{1}{6}$ (Alternativa A)."
        ),
        "parametro_a": 1.500,
        "parametro_b": 1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Conte o espaço amostral ($36$ pares) e liste os casos favoráveis à soma $7$: são $6$ pares distintos.",
        },
    },
    # ===========================================================================
    # APLICADA — Matemática Financeira e Estatística (Vol 11)
    # ===========================================================================
    {
        "titulo_capitulo": "Porcentagem, Lucro e Prejuízo Comercial",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Um produto com preço de tabela de $R\\$\\,200{,}00$ recebe um desconto de $15\\%$. O preço final a ser pago é:",
        "alternativas": [
            {"letra": "A", "texto": "$R\\$\\,170{,}00$", "correta": True},
            {"letra": "B", "texto": "$R\\$\\,180{,}00$", "correta": False},
            {"letra": "C", "texto": "$R\\$\\,165{,}00$", "correta": False},
            {"letra": "D", "texto": "$R\\$\\,150{,}00$", "correta": False},
            {"letra": "E", "texto": "$R\\$\\,175{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. O desconto equivale a $15\\%$ de $200$: $0{,}15 \\times 200 = 30$.\n"
            "2. Preço final: $200 - 30 = 170$, ou seja, $R\\$\\,170{,}00$ (Alternativa A)."
        ),
        "parametro_a": 1.200,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Calcule o desconto ($15\\%$ de $200$) e subtraia do preço de tabela — ou aplique o fator $(1 - 0{,}15)$ diretamente.",
        },
    },
    {
        "titulo_capitulo": "Regime de Juros Simples e Compostos",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Um capital de $R\\$\\,1.000{,}00$ é aplicado a juros simples de $2\\%$ ao mês durante $6$ meses. Os juros produzidos totalizam:",
        "alternativas": [
            {"letra": "A", "texto": "$R\\$\\,120{,}00$", "correta": True},
            {"letra": "B", "texto": "$R\\$\\,126{,}16$", "correta": False},
            {"letra": "C", "texto": "$R\\$\\,60{,}00$", "correta": False},
            {"letra": "D", "texto": "$R\\$\\,200{,}00$", "correta": False},
            {"letra": "E", "texto": "$R\\$\\,102{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Em juros simples: $J = C \\cdot i \\cdot t$.\n"
            "2. $J = 1000 \\cdot 0{,}02 \\cdot 6 = 120$, ou seja, $R\\$\\,120{,}00$ (Alternativa A)."
        ),
        "parametro_a": 1.300,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Juros simples não capitalizam: $J = C \\cdot i \\cdot t$, sem exponenciação do fator de crescimento.",
        },
    },
    {
        "titulo_capitulo": "Regime de Juros Simples e Compostos",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Aplicando-se $R\\$\\,1.000{,}00$ a juros compostos de $10\\%$ ao ano, o montante após $2$ anos será de:",
        "alternativas": [
            {"letra": "A", "texto": "$R\\$\\,1.210{,}00$", "correta": True},
            {"letra": "B", "texto": "$R\\$\\,1.200{,}00$", "correta": False},
            {"letra": "C", "texto": "$R\\$\\,1.100{,}00$", "correta": False},
            {"letra": "D", "texto": "$R\\$\\,1.220{,}00$", "correta": False},
            {"letra": "E", "texto": "$R\\$\\,1.331{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Em juros compostos: $M = C(1+i)^t$.\n"
            "2. $M = 1000 \\cdot (1{,}10)^2 = 1000 \\cdot 1{,}21 = 1210$, ou seja, $R\\$\\,1.210{,}00$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Juros compostos capitalizam período a período: $M = C(1+i)^t$ com o tempo no expoente.",
        },
    },
    {
        "titulo_capitulo": "Estatística Descritiva: Tabelas, Média, Mediana e Moda",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Um aluno obteve as notas $8$ (com peso $2$) e $6$ (com peso $3$). Sua média ponderada final é:",
        "alternativas": [
            {"letra": "A", "texto": "$6{,}8$", "correta": True},
            {"letra": "B", "texto": "$7{,}0$", "correta": False},
            {"letra": "C", "texto": "$6{,}5$", "correta": False},
            {"letra": "D", "texto": "$7{,}2$", "correta": False},
            {"letra": "E", "texto": "$6{,}0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Média ponderada: $\\bar{x} = \\frac{\\sum (x_i \\cdot p_i)}{\\sum p_i}$.\n"
            "2. $\\bar{x} = \\frac{8 \\cdot 2 + 6 \\cdot 3}{2 + 3} = \\frac{16 + 18}{5} = \\frac{34}{5} = 6{,}8$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "aplicada",
            "dica_estagio_2": "Na média ponderada, multiplique cada nota pelo seu peso, some tudo e divida pela soma dos pesos.",
        },
    },
    # ===========================================================================
    # ÁLGEBRA LINEAR E SEQUÊNCIAS (Vol 4) — cobertura da 4ª área canônica
    # ===========================================================================
    {
        "titulo_capitulo": "Progressão Aritmética (PA)",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Em uma PA, o primeiro termo é $a_1 = 5$ e a razão é $r = 3$. O valor do décimo termo $a_{10}$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$32$", "correta": True},
            {"letra": "B", "texto": "$35$", "correta": False},
            {"letra": "C", "texto": "$30$", "correta": False},
            {"letra": "D", "texto": "$29$", "correta": False},
            {"letra": "E", "texto": "$50$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Fórmula do termo geral da PA: $a_n = a_1 + (n - 1)\\,r$.\n"
            "2. $a_{10} = 5 + (10 - 1) \\cdot 3 = 5 + 27 = 32$ (Alternativa A)."
        ),
        "parametro_a": 1.300,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_linear",
            "dica_estagio_2": "Use o termo geral da PA: $a_n = a_1 + (n-1)\\,r$. Atenção ao fator $(n-1)$, e não $n$.",
        },
    },
    {
        "titulo_capitulo": "Progressão Geométrica (PG)",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "Em uma PG de razão $2$, o terceiro termo vale $12$. O quinto termo $a_5$ dessa PG é:",
        "alternativas": [
            {"letra": "A", "texto": "$48$", "correta": True},
            {"letra": "B", "texto": "$24$", "correta": False},
            {"letra": "C", "texto": "$36$", "correta": False},
            {"letra": "D", "texto": "$96$", "correta": False},
            {"letra": "E", "texto": "$14$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Em uma PG, cada termo é obtido multiplicando o anterior pela razão $q = 2$.\n"
            "2. $a_4 = a_3 \\cdot q = 12 \\cdot 2 = 24$.\n"
            "3. $a_5 = a_4 \\cdot q = 24 \\cdot 2 = 48$ (Alternativa A)."
        ),
        "parametro_a": 1.400,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_linear",
            "dica_estagio_2": "Na PG, avançar $k$ casas multiplica o termo por $q^k$: $a_5 = a_3 \\cdot q^2$.",
        },
    },
    {
        "titulo_capitulo": "Determinantes e Teorema de Laplace",
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": "O determinante da matriz $A = \\begin{bmatrix} 3 \\& 2 \\\\ 1 \\& 4 \\end{bmatrix}$ é:",
        "alternativas": [
            {"letra": "A", "texto": "$10$", "correta": True},
            {"letra": "B", "texto": "$14$", "correta": False},
            {"letra": "C", "texto": "$-10$", "correta": False},
            {"letra": "D", "texto": "$6$", "correta": False},
            {"letra": "E", "texto": "$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": (
            "1. Para uma matriz $2 \\times 2$, $\\det(A) = a_{11}\\,a_{22} - a_{12}\\,a_{21}$.\n"
            "2. $\\det(A) = 3 \\cdot 4 - 2 \\cdot 1 = 12 - 2 = 10$ (Alternativa A)."
        ),
        "parametro_a": 1.500,
        "parametro_b": 1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {
            "grande_area": "algebra_linear",
            "dica_estagio_2": "Determinante $2\\times 2$: produto da diagonal principal menos produto da diagonal secundária.",
        },
    },
]


async def seed_exercises():
    """Popula os exercícios calibrados associando aos capítulos correspondentes."""
    print(" Iniciando população de exercícios calibrados TRI...")
    async with AsyncSessionLocal() as session:
        # Busca capítulos
        stmt_caps = select(Capitulo)
        result_caps = await session.execute(stmt_caps)
        capitulos = result_caps.scalars().all()

        mapa_capitulos = {c.titulo: c.id for c in capitulos}
        if not mapa_capitulos:
            print(" ERRO: Nenhum capítulo encontrado no banco. Execute scripts/seed_content.py primeiro!")
            return

        total_inseridos = 0
        for item_data in ITENS_CALIBRADOS:
            titulo_cap = item_data["titulo_capitulo"]
            capitulo_id = mapa_capitulos.get(titulo_cap)

            if not capitulo_id:
                # Se não encontrar pelo título exato, pega o primeiro capítulo disponível
                capitulo_id = capitulos[0].id

            # Verifica se já existe item com mesmo enunciado
            stmt_existente = select(ItemExercicio).where(
                ItemExercicio.enunciado_katex == item_data["enunciado_katex"]
            )
            existente = (await session.execute(stmt_existente)).scalar_one_or_none()

            if not existente:
                novo_item = ItemExercicio(
                    id=uuid.uuid4(),
                    capitulo_id=capitulo_id,
                    tipo_origem=item_data["tipo_origem"],
                    tipo_item=item_data["tipo_item"],
                    enunciado_katex=item_data["enunciado_katex"],
                    alternativas=item_data["alternativas"],
                    resposta_correta=item_data["resposta_correta"],
                    resolucao_passo_a_passo=item_data["resolucao_passo_a_passo"],
                    parametro_a=item_data["parametro_a"],
                    parametro_b=item_data["parametro_b"],
                    parametro_c=item_data["parametro_c"],
                    metadados_sympy=item_data["metadados_sympy"],
                    validado_sympy=True,
                    ativo=True,
                )
                session.add(novo_item)
                total_inseridos += 1

        await session.commit()
        print(f" População concluída! {total_inseridos} novos itens calibrados inseridos com sucesso.")


if __name__ == "__main__":
    asyncio.run(seed_exercises())
