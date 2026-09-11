"""
Módulo Canônico de Dados Didáticos — Volume 7: Geometria Analítica
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (5 caps), FIXACAO_DATA (15 questões), RAG_DATA (5 fragmentos), TRI_DATA (25 itens).
"""

VOLUME_INFO = {
    "numero": 7,
    "titulo": "Geometria Analítica",
    "grande_area": "geometria",
    "ordem": 7,
    "capitulos": [
        {"num": 1, "titulo": "Coordenadas Cartesianas no Plano e Ponto Médio", "tempo": 50},
        {"num": 2, "titulo": "Equação Geral e Reduzida da Reta", "tempo": 50},
        {"num": 3, "titulo": "Posições Relativas e Distância Ponto-Reta", "tempo": 50},
        {"num": 4, "titulo": "Equação da Circunferência e Posições Relativas", "tempo": 50},
        {"num": 5, "titulo": "Cônicas: Elipse, Hipérbole e Parábola", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Coordenadas Cartesianas no Plano e Ponto Médio

A Geometria Analítica de Descartes estabelece a correspondência biunívoca entre os pontos do plano geométrico e os pares ordenados de números reais em $\mathbb{R}^2$.

### 1. Sistema Cartesiano Ortogonal
Dois eixos perpendiculares $Ox$ (eixo das abscissas) e $Oy$ (eixo das ordenadas) dividem o plano em quatro quadrantes numerados no sentido anti-horário.
Todo ponto $P$ tem coordenadas $(x_P, y_P)$.

---

### 2. Distância entre Dois Pontos
Dados $A(x_A, y_A)$ e $B(x_B, y_B)$, pelo Teorema de Pitágoras no triângulo retângulo de catetos $|\Delta x|$ e $|\Delta y|$:
$$d(A, B) = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}$$

---

### 3. Ponto Médio de um Segmento
O ponto médio $M(x_M, y_M)$ do segmento $AB$ é a média aritmética das coordenadas dos extremos:
$$x_M = \frac{x_A + x_B}{2}, \quad y_M = \frac{y_A + y_B}{2}$$
- **Baricentro do Triângulo ($G$)**:
  $$G = \left(\frac{x_A + x_B + x_C}{3}, \frac{y_A + y_B + y_C}{3}\right)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Distância entre Dois Pontos
**Enunciado:** Calcule a distância entre os pontos $A(1, 2)$ e $B(4, 6)$.

**Resolução:**
$$d(A, B) = \sqrt{(4 - 1)^2 + (6 - 2)^2} = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> A ordem dos pontos na fórmula da distância é irrelevante devido ao quadrado: $(x_B - x_A)^2 = (x_A - x_B)^2$.
""",
    },
    2: {
        "teoria": r"""# Equação Geral e Reduzida da Reta

Toda reta no plano cartesiano é uma variedade linear de dimensão 1, descrita por uma equação polinomial de primeiro grau em duas variáveis.

### 1. Equação Geral da Reta
$$ax + by + c = 0 \quad (a^2 + b^2 \neq 0)$$

---

### 2. Equação Reduzida e Coeficiente Angular
Isolando $y$ (para retas não verticais, $b \neq 0$):
$$y = mx + q$$
- $m = \tan\alpha = \frac{y_B - y_A}{x_B - x_A}$: **Coeficiente angular** ou declividade da reta.
- $q$: **Coeficiente linear**, indicando o ponto de corte com o eixo $y$ em $(0, q)$.

---

### 3. Equação Fundamental (Ponto-Declividade)
Conhecendo um ponto $P(x_0, y_0)$ e a declividade $m$:
$$y - y_0 = m(x - x_0)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Reta por Dois Pontos
**Enunciado:** Determine a equação reduzida da reta que passa por $A(2, 3)$ e $B(4, 7)$.

**Resolução:**
1. $m = \frac{7 - 3}{4 - 2} = \frac{4}{2} = 2$.
2. $y - 3 = 2(x - 2) \implies y - 3 = 2x - 4 \implies y = 2x - 1$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Retas verticais são paralelas ao eixo $y$ e têm equação da forma $x = k$. Elas **não possuem coeficiente angular definido** (divisão por zero na tangente de $90^\circ$).
""",
    },
    3: {
        "teoria": r"""# Posições Relativas e Distância Ponto-Reta

O paralelismo, a perpendicularidade e o cálculo de distâncias métricas formam a base operacional dos problemas de geometria com retas.

### 1. Posições Relativas entre Duas Retas
Dadas $r: y = m_r x + q_r$ e $s: y = m_s x + q_s$:
- **Paralelas ($r \parallel s$)**: Mesma declividade:
  $$m_r = m_s \quad (q_r \neq q_s \implies \text{paralelas distintas})$$
- **Perpendiculares ($r \perp s$)**: O produto das declividades é $-1$:
  $$m_r \cdot m_s = -1 \iff m_s = -\frac{1}{m_r}$$

---

### 2. Distância de um Ponto a uma Reta
A distância do ponto $P(x_0, y_0)$ à reta $r: ax + by + c = 0$ é dada por:
$$d(P, r) = \frac{|a x_0 + b y_0 + c|}{\sqrt{a^2 + b^2}}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Distância de Ponto a Reta
**Enunciado:** Calcule a distância do ponto $P(3, 4)$ à reta $3x + 4y - 5 = 0$.

**Resolução:**
$$d(P, r) = \frac{|3(3) + 4(4) - 5|}{\sqrt{3^2 + 4^2}} = \frac{|9 + 16 - 5|}{\sqrt{25}} = \frac{|20|}{5} = 4$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Antes de aplicar a fórmula da distância ponto-reta, certifique-se de que a reta esteja na **forma geral** ($ax + by + c = 0$). Se estiver na forma reduzida, passe todos os termos para um mesmo membro.
""",
    },
    4: {
        "teoria": r"""# Equação da Circunferência e Posições Relativas

A circunferência é o lugar geométrico dos pontos equidistantes de um ponto fixo denominado centro.

### 1. Equação Reduzida
Circunferência de centro $C(a, b)$ e raio $R > 0$:
$$(x - a)^2 + (y - b)^2 = R^2$$

---

### 2. Equação Geral
Expandindo a forma reduzida:
$$x^2 + y^2 - 2ax - 2by + (a^2 + b^2 - R^2) = 0$$

---

### 3. Posição Relativa entre Reta e Circunferência
Comparando a distância $d(C, r)$ do centro à reta com o raio $R$:
- $d(C, r) > R$: Reta **externa** (0 pontos comuns).
- $d(C, r) = R$: Reta **tangente** (1 ponto comum).
- $d(C, r) < R$: Reta **secante** (2 pontos comuns).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Identificação de Centro e Raio
**Enunciado:** Determine o centro e o raio de $x^2 + y^2 - 6x + 8y = 0$.

**Resolução:**
1. Completamos quadrados:
   $$(x^2 - 6x + 9) + (y^2 + 8y + 16) = 9 + 16$$
   $$(x - 3)^2 + (y + 4)^2 = 25$$
2. Centro $C(3, -4)$ e raio $R = \sqrt{25} = 5$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Cuidado com os sinais do centro: $(x - 3)^2 + (y + 4)^2 = 25$ tem centro $(3, -4)$, pois a forma é $(x - a)^2 + (y - b)^2$.
""",
    },
    5: {
        "teoria": r"""# Cônicas: Elipse, Hipérbole e Parábola

As seções cônicas resultam da interseção de um plano com um cone circular reto duplo, definidas geometricamente por focos e excentricidades.

### 1. Elipse
Lugar geométrico dos pontos cuja soma das distâncias aos focos é constante ($d(P, F_1) + d(P, F_2) = 2a$):
- Centro na origem e eixo maior sobre $Ox$:
  $$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \quad (a^2 = b^2 + c^2)$$
  Excentricidade: $e = c/a < 1$.

---

### 2. Hipérbole
Lugar geométrico dos pontos cuja diferença modular das distâncias aos focos é constante ($|d(P, F_1) - d(P, F_2)| = 2a$):
- Focos no eixo $Ox$:
  $$\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1 \quad (c^2 = a^2 + b^2)$$
  Excentricidade: $e = c/a > 1$.

---

### 3. Parábola
Lugar geométrico dos pontos equidistantes de um foco $F$ e de uma reta diretriz $d$:
- Vértice na origem e eixo de simetria horizontal:
  $$y^2 = 2px \quad \text{ou} \quad x^2 = 2py$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Elementos da Elipse
**Enunciado:** Dada a elipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$, determine os semi-eixos $a, b$ e a distância focal $2c$.

**Resolução:**
1. $a^2 = 25 \implies a = 5$ (semi-eixo maior).
2. $b^2 = 9 \implies b = 3$ (semi-eixo menor).
3. Relação fundamental: $a^2 = b^2 + c^2 \implies 25 = 9 + c^2 \implies c^2 = 16 \implies c = 4$.
4. Distância focal: $2c = 8$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Na elipse a relação é $a^2 = b^2 + c^2$ ($a$ é o maior). Na hipérbole a relação é $c^2 = a^2 + b^2$ ($c$ é o maior). Não confunda as duas!
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"A distância entre os pontos $A(0, 0)$ e $B(6, 8)$ no plano cartesiano é:",
            "alternativas": [r"$10$", r"$14$", r"$8$", r"$12$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"As coordenadas do ponto médio do segmento que une $P(-2, 4)$ e $Q(6, 8)$ são:",
            "alternativas": [r"$(2, 6)$", r"$(4, 6)$", r"$(2, 4)$", r"$(4, 12)$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O baricentro do triângulo de vértices $A(1, 2)$, $B(3, 4)$ e $C(5, 6)$ é o ponto:",
            "alternativas": [r"$(3, 4)$", r"$(9, 12)$", r"$(4, 3)$", r"$(3, 3)$"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"O coeficiente angular da reta que passa pelos pontos $(1, 2)$ e $(3, 8)$ vale:",
            "alternativas": [r"$3$", r"$2$", r"$4$", r"$1/3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A reta de equação reduzida $y = -2x + 5$ intersecta o eixo das ordenadas no ponto:",
            "alternativas": [r"$(0, 5)$", r"$(5, 0)$", r"$(0, -2)$", r"$(5/2, 0)$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A equação da reta que passa pela origem e tem inclinação de $45^\circ$ ($m = 1$) é:",
            "alternativas": [r"$y = x$", r"$y = -x$", r"$x + y = 1$", r"$y = 2x$"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"Se a reta $r$ tem declividade $m_r = 3$, uma reta $s$ perpendicular a $r$ tem declividade:",
            "alternativas": [r"$-1/3$", r"$3$", r"$-3$", r"$1/3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Duas retas distintas são paralelas se, e somente se, possuem:",
            "alternativas": [
                r"O mesmo coeficiente angular",
                r"O mesmo coeficiente linear",
                r"Produto dos coeficientes angulares igual a -1",
                r"A mesma equação geral",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A distância da origem $(0, 0)$ à reta $3x + 4y - 15 = 0$ vale:",
            "alternativas": [r"$3$", r"$5$", r"$15$", r"$4$"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"O raio da circunferência de equação $(x - 2)^2 + (y + 1)^2 = 16$ é:",
            "alternativas": [r"$4$", r"$16$", r"$2$", r"$8$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O centro da circunferência $x^2 + y^2 - 4x + 6y - 12 = 0$ é o ponto:",
            "alternativas": [r"$(2, -3)$", r"$(-2, 3)$", r"$(4, -6)$", r"$(2, 3)$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se a distância do centro de uma circunferência a uma reta for estritamente igual ao raio, a reta é:",
            "alternativas": [r"Tangente", r"Secante", r"Externa", r"Diâmetro"],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"Na elipse $\frac{x^2}{16} + \frac{y^2}{9} = 1$, o comprimento do eixo maior é:",
            "alternativas": [r"$8$", r"$4$", r"$6$", r"$16$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A cônica que possui excentricidade estritamente menor que 1 ($e < 1$) é a:",
            "alternativas": [r"Elipse", r"Hipérbole", r"Parábola", r"Circunferência"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A equação $y^2 = 8x$ representa no plano cartesiano uma:",
            "alternativas": [r"Parábola", r"Elipse", r"Hipérbole", r"Circunferência"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 20,
        "teorema": "Distância Euclidiana e Ponto Médio no Plano",
        "texto": (
            "A distância entre dois pontos A e B decorre diretamente de Pitágoras: d = √((Δx)² + (Δy)²). "
            "O ponto médio do segmento é a média aritmética das respectivas coordenadas dos extremos."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 50,
        "teorema": "Equações Geral e Reduzida da Reta",
        "texto": (
            "A equação geral ax + by + c = 0 representa qualquer reta. Na forma reduzida y = mx + q, "
            "m = tan α expressa a taxa de inclinação e q a ordenada do ponto onde a reta intercepta o eixo Oy."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 80,
        "teorema": "Condições de Paralelismo, Perpendicularismo e Distância Ponto-Reta",
        "texto": (
            "Retas paralelas possuem declividades iguais (mr = ms). Retas perpendiculares possuem mr · ms = -1. "
            "A distância do ponto P(x0, y0) à reta ax + by + c = 0 é d = |ax0 + by0 + c| / √(a² + b²)."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 110,
        "teorema": "Equação da Circunferência e Posições Relativas",
        "texto": (
            "A circunferência de centro C(a, b) e raio R tem equação (x - a)² + (y - b)² = R². "
            "Uma reta é tangente se a distância do centro à reta for exatamente igual ao raio R."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 140,
        "teorema": "Classificação das Seções Cônicas",
        "texto": (
            "A elipse satisfaz d(P, F1) + d(P, F2) = 2a com a² = b² + c² (e < 1). A hipérbole satisfaz "
            "|d(P, F1) - d(P, F2)| = 2a com c² = a² + b² (e > 1). A parábola é o lugar dos pontos equidistantes de foco e diretriz."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Coordenadas e Ponto Médio (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A distância entre os pontos $A(-1, 3)$ e $B(2, 7)$ no plano cartesiano é:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$\sqrt{7}$", "correta": False},
            {"letra": "C", "texto": r"$25$", "correta": False},
            {"letra": "D", "texto": r"$7$", "correta": False},
            {"letra": "E", "texto": r"$\sqrt{5}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\Delta x = 2 - (-1) = 3$. 2. $\Delta y = 7 - 3 = 4$. 3. $d = \sqrt{3^2 + 4^2} = \sqrt{25} = 5$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique a fórmula da distância com Pitágoras."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se o ponto $M(3, 5)$ é o ponto médio do segmento $AB$, e $A(1, 2)$, as coordenadas de $B$ são:",
        "alternativas": [
            {"letra": "A", "texto": r"$B(5, 8)$", "correta": True},
            {"letra": "B", "texto": r"$B(2, 3)$", "correta": False},
            {"letra": "C", "texto": r"$B(4, 7)$", "correta": False},
            {"letra": "D", "texto": r"$B(5, 7)$", "correta": False},
            {"letra": "E", "texto": r"$B(6, 10)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3 = (1 + x_B)/2 \implies x_B = 5$. 2. $5 = (2 + y_B)/2 \implies y_B = 8$. $B(5, 8)$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a fórmula do ponto médio isolando as coordenadas de B."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é a abscissa do baricentro do triângulo com vértices $(2, 1)$, $(4, 5)$ e $(6, 3)$?",
        "alternativas": [],
        "resposta_correta": "4",
        "resolucao_passo_a_passo": r"1. $x_G = (2 + 4 + 6) / 3 = 12 / 3 = 4$.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Some as três abscissas e divida por 3."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Os pontos $A(1, 2)$, $B(3, 6)$ e $C(k, 10)$ são colineares quando $k$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$6$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Declividade $m_{AB} = \frac{6 - 2}{3 - 1} = 2$. 2. $m_{BC} = \frac{10 - 6}{k - 3} = 2 \implies \frac{4}{k - 3} = 2 \implies k - 3 = 2 \implies k = 5$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Iguale as declividades dos segmentos."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A área do triângulo de vértices $A(0, 0)$, $B(4, 0)$ e $C(0, 6)$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$12$", "correta": True},
            {"letra": "B", "texto": r"$24$", "correta": False},
            {"letra": "C", "texto": r"$10$", "correta": False},
            {"letra": "D", "texto": r"$14$", "correta": False},
            {"letra": "E", "texto": r"$6$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Triângulo retângulo com catetos sobre os eixos medindo 4 e 6. Área = $(4 \times 6) / 2 = 12$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $\text{base} \times \text{altura} / 2$."},
    },

    # --- Cap 2: Equação da Reta (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação da reta que passa pelo ponto $P(1, 3)$ com coeficiente angular $m = 4$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$4x - y - 1 = 0$", "correta": True},
            {"letra": "B", "texto": r"$4x - y + 1 = 0$", "correta": False},
            {"letra": "C", "texto": r"$4x + y - 7 = 0$", "correta": False},
            {"letra": "D", "texto": r"$x - 4y + 11 = 0$", "correta": False},
            {"letra": "E", "texto": r"$4x - y = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $y - 3 = 4(x - 1) \implies y - 3 = 4x - 4 \implies 4x - y - 1 = 0$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $y - y_0 = m(x - x_0)$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O coeficiente linear da reta de equação geral $2x + 3y - 9 = 0$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3$", "correta": True},
            {"letra": "B", "texto": r"$-2/3$", "correta": False},
            {"letra": "C", "texto": r"$9$", "correta": False},
            {"letra": "D", "texto": r"$-3$", "correta": False},
            {"letra": "E", "texto": r"$2/3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3y = -2x + 9 \implies y = -\frac{2}{3}x + 3$. O coeficiente linear é $3$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Isole $y$ e observe o termo independente."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o coeficiente angular da reta $6x - 2y + 7 = 0$?",
        "alternativas": [],
        "resposta_correta": "3",
        "resolucao_passo_a_passo": r"1. $2y = 6x + 7 \implies y = 3x + 3{,}5$. Coeficiente angular é 3.",
        "parametro_a": 1.250,
        "parametro_b": -0.700,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Isole $y$ para achar $m$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação da reta vertical que passa pelo ponto $(-3, 5)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = -3$", "correta": True},
            {"letra": "B", "texto": r"$y = 5$", "correta": False},
            {"letra": "C", "texto": r"$x + y = 2$", "correta": False},
            {"letra": "D", "texto": r"$x = 5$", "correta": False},
            {"letra": "E", "texto": r"$y = -3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Retas verticais têm abscissa constante: $x = -3$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Retas verticais são descritas por $x = k$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação segmentária da reta que corta o eixo $x$ em $4$ e o eixo $y$ em $3$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{x}{4} + \frac{y}{3} = 1$", "correta": True},
            {"letra": "B", "texto": r"$\frac{x}{3} + \frac{y}{4} = 1$", "correta": False},
            {"letra": "C", "texto": r"$4x + 3y = 1$", "correta": False},
            {"letra": "D", "texto": r"$\frac{x}{4} - \frac{y}{3} = 1$", "correta": False},
            {"letra": "E", "texto": r"$3x + 4y = 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Forma segmentária: $x/p + y/q = 1$, onde $p = 4$ e $q = 3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a forma segmentária $x/p + y/q = 1$."},
    },

    # --- Cap 3: Posições Relativas e Distância Ponto-Reta (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação da reta paralela a $y = 3x - 1$ que passa por $(2, 4)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$y = 3x - 2$", "correta": True},
            {"letra": "B", "texto": r"$y = 3x + 2$", "correta": False},
            {"letra": "C", "texto": r"$y = -1/3x + 4$", "correta": False},
            {"letra": "D", "texto": r"$y = 3x - 4$", "correta": False},
            {"letra": "E", "texto": r"$y = 2x$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Paralela $\implies m = 3$. 2. $y - 4 = 3(x - 2) \implies y = 3x - 2$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Retas paralelas possuem a mesma declividade."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A reta $r: y = 2x + 1$ e a reta $s: y = -\frac{1}{2}x + 4$ são:",
        "alternativas": [
            {"letra": "A", "texto": r"Perpendiculares", "correta": True},
            {"letra": "B", "texto": r"Paralelas distintas", "correta": False},
            {"letra": "C", "texto": r"Coincidentes", "correta": False},
            {"letra": "D", "texto": r"Concorrentes não perpendiculares", "correta": False},
            {"letra": "E", "texto": r"Reversas", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $m_r \cdot m_s = 2 \cdot (-1/2) = -1 \implies$ perpendiculares. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "O produto das declividades é -1."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule a distância do ponto $P(0, 0)$ à reta $3x + 4y - 20 = 0$.",
        "alternativas": [],
        "resposta_correta": "4",
        "resolucao_passo_a_passo": r"1. $d = \frac{|3(0) + 4(0) - 20|}{\sqrt{3^2 + 4^2}} = \frac{20}{5} = 4$.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Aplique $d = |c|/\sqrt{a^2+b^2}$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A distância entre as retas paralelas $r: 3x + 4y - 5 = 0$ e $s: 3x + 4y + 10 = 0$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3$", "correta": True},
            {"letra": "B", "texto": r"$5$", "correta": False},
            {"letra": "C", "texto": r"$15$", "correta": False},
            {"letra": "D", "texto": r"$1$", "correta": False},
            {"letra": "E", "texto": r"$2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $d = \frac{|c_1 - c_2|}{\sqrt{a^2 + b^2}} = \frac{|-5 - 10|}{\sqrt{9 + 16}} = \frac{15}{5} = 3$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $d = |c_1 - c_2|/\sqrt{a^2+b^2}$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para qual valor de $k$ as retas $2x - 3y + 1 = 0$ e $kx + 4y - 5 = 0$ são perpendiculares?",
        "alternativas": [
            {"letra": "A", "texto": r"$6$", "correta": True},
            {"letra": "B", "texto": r"$-6$", "correta": False},
            {"letra": "C", "texto": r"$8/3$", "correta": False},
            {"letra": "D", "texto": r"$-8/3$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $m_1 = 2/3$. 2. Para perpendicular: $m_2 = -3/2$. 3. $m_2 = -k/4 \implies -k/4 = -3/2 \implies k = 6$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Iguale o produto das declividades a -1."},
    },

    # --- Cap 4: Equação da Circunferência (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O centro e o raio da circunferência $(x - 3)^2 + (y + 5)^2 = 49$ são:",
        "alternativas": [
            {"letra": "A", "texto": r"$C(3, -5)$ e $R = 7$", "correta": True},
            {"letra": "B", "texto": r"$C(-3, 5)$ e $R = 7$", "correta": False},
            {"letra": "C", "texto": r"$C(3, -5)$ e $R = 49$", "correta": False},
            {"letra": "D", "texto": r"$C(-3, -5)$ e $R = 7$", "correta": False},
            {"letra": "E", "texto": r"$C(3, 5)$ e $R = 7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Comparando com $(x - a)^2 + (y - b)^2 = R^2$: $a = 3$, $b = -5$, $R = \sqrt{49} = 7$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Inverta os sinais de $a$ e $b$ e tire a raiz do termo constante."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação $x^2 + y^2 - 6x - 8y = 0$ descreve uma circunferência cujo raio vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$25$", "correta": False},
            {"letra": "C", "texto": r"$10$", "correta": False},
            {"letra": "D", "texto": r"$\sqrt{5}$", "correta": False},
            {"letra": "E", "texto": r"$7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $(x - 3)^2 + (y - 4)^2 = 9 + 16 = 25$. 2. $R = \sqrt{25} = 5$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Complete os quadrados para $x$ e $y$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A reta $y = 4$ em relação à circunferência $x^2 + y^2 = 25$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"Secante", "correta": True},
            {"letra": "B", "texto": r"Tangente", "correta": False},
            {"letra": "C", "texto": r"Externa", "correta": False},
            {"letra": "D", "texto": r"Diâmetro", "correta": False},
            {"letra": "E", "texto": r"Assíntota", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Centro $(0, 0)$, $R = 5$. Distância à reta $y = 4$ é $d = 4$. 2. Como $d = 4 < R = 5$, a reta é secante. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Compare a distância do centro com o raio: $d < R$ secante."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o raio da circunferência de equação $x^2 + y^2 = 36$?",
        "alternativas": [],
        "resposta_correta": "6",
        "resolucao_passo_a_passo": r"1. $R^2 = 36 \implies R = 6$.",
        "parametro_a": 1.100,
        "parametro_b": -1.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Tire a raiz quadrada de 36."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação da circunferência com centro em $(0, 0)$ tangente à reta $x = 3$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x^2 + y^2 = 9$", "correta": True},
            {"letra": "B", "texto": r"$x^2 + y^2 = 3$", "correta": False},
            {"letra": "C", "texto": r"$x^2 + y^2 = 6$", "correta": False},
            {"letra": "D", "texto": r"$(x - 3)^2 + y^2 = 9$", "correta": False},
            {"letra": "E", "texto": r"$x^2 + y^2 = 12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Distância da origem a $x = 3$ é $d = 3$. Como é tangente, $R = 3$. 2. $x^2 + y^2 = 3^2 = 9$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "O raio é igual à distância da origem à reta tangente."},
    },

    # --- Cap 5: Cônicas (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Os focos da elipse $\frac{x^2}{25} + \frac{y^2}{9} = 1$ estão localizados nos pontos:",
        "alternativas": [
            {"letra": "A", "texto": r"$(-4, 0) \text{ e } (4, 0)$", "correta": True},
            {"letra": "B", "texto": r"$(0, -4) \text{ e } (0, 4)$", "correta": False},
            {"letra": "C", "texto": r"$(-5, 0) \text{ e } (5, 0)$", "correta": False},
            {"letra": "D", "texto": r"$(-3, 0) \text{ e } (3, 0)$", "correta": False},
            {"letra": "E", "texto": r"$(-16, 0) \text{ e } (16, 0)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a^2 = 25 \implies a = 5$; $b^2 = 9 \implies b = 3$. 2. $c^2 = a^2 - b^2 = 25 - 9 = 16 \implies c = 4$. Focos no eixo $x$: $(\pm 4, 0)$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Na elipse $a^2 = b^2 + c^2$ com focos sobre o maior eixo."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A excentricidade da elipse $\frac{x^2}{100} + \frac{y^2}{64} = 1$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$0{,}6$", "correta": True},
            {"letra": "B", "texto": r"$0{,}8$", "correta": False},
            {"letra": "C", "texto": r"$0{,}5$", "correta": False},
            {"letra": "D", "texto": r"$0{,}64$", "correta": False},
            {"letra": "E", "texto": r"$1{,}25$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a = 10$, $b = 8$. $c = \sqrt{100 - 64} = \sqrt{36} = 6$. 2. $e = c/a = 6/10 = 0{,}6$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A excentricidade é $e = c/a$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação da hipérbole com focos no eixo $x$ e vértices em $(\pm 3, 0)$ e focos em $(\pm 5, 0)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{x^2}{9} - \frac{y^2}{16} = 1$", "correta": True},
            {"letra": "B", "texto": r"$\frac{x^2}{9} + \frac{y^2}{16} = 1$", "correta": False},
            {"letra": "C", "texto": r"$\frac{x^2}{16} - \frac{y^2}{9} = 1$", "correta": False},
            {"letra": "D", "texto": r"$\frac{x^2}{9} - \frac{y^2}{25} = 1$", "correta": False},
            {"letra": "E", "texto": r"$\frac{y^2}{9} - \frac{x^2}{16} = 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a = 3$, $c = 5$. 2. Na hipérbole $c^2 = a^2 + b^2 \implies 25 = 9 + b^2 \implies b^2 = 16$. 3. $\frac{x^2}{9} - \frac{y^2}{16} = 1$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a relação $c^2 = a^2 + b^2$ da hipérbole."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o comprimento do semi-eixo maior da elipse $9x^2 + 25y^2 = 225$?",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": r"1. Dividindo por 225: $\frac{x^2}{25} + \frac{y^2}{9} = 1$. 2. $a^2 = 25 \implies a = 5$.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Divida todos os termos por 225."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O foco da parábola de equação $y^2 = 12x$ é o ponto:",
        "alternativas": [
            {"letra": "A", "texto": r"$(3, 0)$", "correta": True},
            {"letra": "B", "texto": r"$(0, 3)$", "correta": False},
            {"letra": "C", "texto": r"$(6, 0)$", "correta": False},
            {"letra": "D", "texto": r"$(12, 0)$", "correta": False},
            {"letra": "E", "texto": r"$(0, 6)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Forma $y^2 = 4px \implies 4p = 12 \implies p = 3$. Foco em $(p, 0) = (3, 0)$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Compare com $y^2 = 4px$."},
    },
]
