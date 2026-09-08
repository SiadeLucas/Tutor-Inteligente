"""
Baterias de fixação canônicas server-side da Etapa 5, indexadas por
(numero_do_volume, numero_do_capitulo). O gabarito nunca é enviado ao
cliente antes da submissão — a correção acontece exclusivamente no backend.

Na Etapa 7, este banco provisório será substituído pelas tabelas
itens_exercicios / tentativas_exercicios e pelo motor CAT.
"""

BATERIAS_FIXACAO_CANONICAS: dict[tuple[int, int], list[dict]] = {
    (1, 1): [
        {
            "numero": 1,
            "enunciado": r"Seja a proposição condicional $p \to q$. Qual das alternativas representa a sua negação lógica formal $\neg(p \to q)$?",
            "alternativas": [r"$\neg p \to \neg q$", r"$p \land \neg q$", r"$\neg p \lor q$", r"$\neg(p \land q)$"],
            "indice_correto": 1,
        },
        {
            "numero": 2,
            "enunciado": r"A condicional $p \to q$ é logicamente equivalente a qual proposição?",
            "alternativas": [r"$q \to p$", r"$\neg q \to \neg p$", r"$\neg p \to \neg q$", r"$p \leftrightarrow q$"],
            "indice_correto": 1,
        },
        {
            "numero": 3,
            "enunciado": r"Sobre a disjunção inclusiva $p \lor q$, é correto afirmar que ela é falsa somente quando:",
            "alternativas": [r"$p$ é $V$ e $q$ é $V$", r"$p$ é $V$ e $q$ é $F$", r"$p$ é $F$ e $q$ é $V$", r"$p$ é $F$ e $q$ é $F$"],
            "indice_correto": 3,
        },
    ],
    (1, 2): [
        {
            "numero": 1,
            "enunciado": r"Dado $A = \{1, 2, 3\}$, quantos subconjuntos possui $\mathcal{P}(A)$?",
            "alternativas": [r"$6$", r"$7$", r"$8$", r"$9$"],
            "indice_correto": 2,
        },
        {
            "numero": 2,
            "enunciado": r"Se $n(A) = 60$, $n(B) = 50$ e $n(A \cap B) = 20$, então $n(A \cup B)$ vale:",
            "alternativas": [r"$70$", r"$80$", r"$90$", r"$110$"],
            "indice_correto": 2,
        },
        {
            "numero": 3,
            "enunciado": r"A afirmação $\emptyset \in \{\emptyset\}$ é:",
            "alternativas": [
                r"Falsa, pois $\emptyset$ não é elemento de nada",
                r"Verdadeira, pois $\emptyset$ é elemento de $\{\emptyset\}$",
                r"Falsa, o correto seria $\emptyset \subset \{\emptyset\}$",
                r"Indeterminada",
            ],
            "indice_correto": 1,
        },
    ],
    (1, 5): [
        {
            "numero": 1,
            "enunciado": r"A função $f(x) = ax + b$ contém os pontos $A(2, 7)$ e $B(5, 16)$. Qual é a lei da função?",
            "alternativas": [r"$f(x) = 2x + 3$", r"$f(x) = 3x + 1$", r"$f(x) = 3x - 1$", r"$f(x) = x + 5$"],
            "indice_correto": 1,
        },
        {
            "numero": 2,
            "enunciado": r"Na função $f(x) = -2x + 6$, para quais valores de $x$ temos $f(x) > 0$?",
            "alternativas": [r"$x > 3$", r"$x < 3$", r"$x > -3$", r"$x < -3$"],
            "indice_correto": 1,
        },
        {
            "numero": 3,
            "enunciado": r"Uma função afim $f(x) = ax + b$ é dita estritamente linear quando:",
            "alternativas": [r"$a = 1$", r"$b = 0$", r"$a = b$", r"$a = 0$"],
            "indice_correto": 1,
        },
    ],
    (1, 6): [
        {
            "numero": 1,
            "enunciado": r"O lucro é modelado por $L(x) = -x^2 + 10x - 9$. Quantas peças maximizam o lucro?",
            "alternativas": [r"$2$", r"$4$", r"$5$", r"$10$"],
            "indice_correto": 2,
        },
        {
            "numero": 2,
            "enunciado": r"Qual o lucro máximo atingido por $L(x) = -x^2 + 10x - 9$?",
            "alternativas": [r"$9$ mil reais", r"$14$ mil reais", r"$16$ mil reais", r"$25$ mil reais"],
            "indice_correto": 2,
        },
        {
            "numero": 3,
            "enunciado": r"A forma canônica da função quadrática que revela o vértice diretamente é:",
            "alternativas": [
                r"$f(x) = a(x - x_v)^2 + y_v$",
                r"$f(x) = ax^2 + bx + c$",
                r"$f(x) = a(x - x_1)(x - x_2)$",
                r"$f(x) = \frac{-b \pm \sqrt{\Delta}}{2a}$",
            ],
            "indice_correto": 0,
        },
    ],
}
