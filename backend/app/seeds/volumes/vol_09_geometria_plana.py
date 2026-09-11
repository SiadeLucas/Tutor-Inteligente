"""
Módulo Canônico de Dados Didáticos — Volume 9: Geometria Plana
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
    "numero": 9,
    "titulo": "Geometria Plana",
    "grande_area": "geometria",
    "ordem": 9,
    "capitulos": [
        {"num": 1, "titulo": "Noções Primitivas, Segmentos e Axiomas de Ordem", "tempo": 50},
        {"num": 2, "titulo": "Ângulos, Triângulos e Casos de Congruência", "tempo": 50},
        {"num": 3, "titulo": "Quadriláteros Notáveis e Retas Paralelas", "tempo": 50},
        {"num": 4, "titulo": "Semelhança de Triângulos e Teorema de Tales", "tempo": 50},
        {"num": 5, "titulo": "Relações Métricas no Triângulo Retângulo e Pitágoras", "tempo": 50},
        {"num": 6, "titulo": "Áreas das Principais Figuras Planas e do Círculo", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Noções Primitivas, Segmentos e Axiomas de Ordem

A geometria euclidiana plana ergue-se sobre conceitos primitivos aceitos sem definição e axiomas fundamentais de ordem e incidência.

### 1. Conceitos Primitivos
- Ponto (adimensional), Reta (unidimensional e infinita) e Plano (bidimensional e ilimitado).

### 2. Segmento de Reta e Semirreta
- **Segmento $AB$**: Conjunto dos pontos entre $A$ e $B$, incluindo os extremos:
  $$AB = \{P \mid P \text{ está entre } A \text{ e } B\} \cup \{A, B\}$$
- **Ponto Médio**: Ponto $M \in AB$ tal que $AM \cong MB$.

### 3. Postulado de Euclides (Axioma das Paralelas)
Por um ponto fora de uma reta passa uma única reta paralela à reta dada.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Segmentos Consecutivos e Colineares
**Enunciado:** Em uma reta orientada, $B$ está entre $A$ e $C$. Se $AB = 7\text{ cm}$ e $AC = 19\text{ cm}$, determine $BC$.

**Resolução:**
Pelo axioma de adição de segmentos colineares:
$$AB + BC = AC \implies 7 + BC = 19 \implies BC = 12\text{ cm}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Segmentos consecutivos compartilham uma extremidade comum; se estiverem na mesma reta, são ditos colineares.
""",
    },
    2: {
        "teoria": r"""# Ângulos, Triângulos e Casos de Congruência

### 1. Classificação de Ângulos
- Agudo ($0^\circ < \alpha < 90^\circ$), Reto ($\alpha = 90^\circ$), Obtuso ($90^\circ < \alpha < 180^\circ$), Raso ($\alpha = 180^\circ$).
- Complementares: $\alpha + \beta = 90^\circ$.
- Suplementares: $\alpha + \beta = 180^\circ$.

---

### 2. Soma dos Ângulos Internos de um Triângulo
Para qualquer triângulo no plano euclidiano:
$$\hat{A} + \hat{B} + \hat{C} = 180^\circ$$
- Ângulo externo: $\hat{E}_A = \hat{B} + \hat{C}$.

---

### 3. Casos Clássicos de Congruência de Triângulos
Dois triângulos são congruentes ($\triangle ABC \cong \triangle A'B'C'$) se satisfizerem um dos critérios:
1. **LAL**: Dois lados e o ângulo compreendido.
2. **ALA**: Um lado e os dois ângulos adjacentes.
3. **LLL**: Os três lados respectivamente congruentes.
4. **LAAo**: Um lado, um ângulo adjacente e o ângulo oposto.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Ângulo Externo do Triângulo
**Enunciado:** Em um triângulo $ABC$, os ângulos internos $\hat{A}$ e $\hat{B}$ medem $40^\circ$ e $65^\circ$. Calcule o ângulo externo no vértice $C$.

**Resolução:**
Pelo Teorema do Ângulo Externo:
$$\hat{E}_C = \hat{A} + \hat{B} = 40^\circ + 65^\circ = 105^\circ$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Caso "Lado-Lado-Ângulo" (LLA) **não garante** congruência a menos que o ângulo seja reto ou obtuso oposto ao maior lado.
""",
    },
    3: {
        "teoria": r"""# Quadriláteros Notáveis e Retas Paralelas

### 1. Retas Paralelas Cortadas por uma Transversal
Duas retas paralelas $r \parallel s$ cortadas por uma transversal $t$ determinam pares de ângulos:
- Alternos internos e externos: **Congruentes**.
- Correspondentes: **Congruentes**.
- Colaterais internos e externos: **Suplementares** ($\alpha + \beta = 180^\circ$).

---

### 2. Quadriláteros Notáveis
- **Trapézio**: Possui pelo menos um par de lados opostos paralelos (bases).
- **Paralelogramo**: Lados opostos paralelos e congruentes; ângulos opostos congruentes; diagonais cruzam-se nos respectivos pontos médios.
- **Retângulo**: Paralelogramo equiângulo ($90^\circ$); diagonais congruentes.
- **Losango**: Paralelogramo equilátero; diagonais perpendiculares e bissetrizes.
- **Quadrado**: Simultaneamente retângulo e losango.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Base Média do Trapézio
**Enunciado:** Em um trapézio de bases medindo $14\text{ cm}$ e $8\text{ cm}$, determine a medida da base média.

**Resolução:**
$$B_m = \frac{B + b}{2} = \frac{14 + 8}{2} = \frac{22}{2} = 11\text{ cm}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Todo quadrado é retângulo e todo quadrado é losango, mas a recíproca não é verdadeira.
""",
    },
    4: {
        "teoria": r"""# Semelhança de Triângulos e Teorema de Tales

### 1. Teorema de Tales
Um feixe de retas paralelas determina sobre duas transversais quaisquer segmentos correspondentes estritamente proporcionais:
$$\frac{AB}{BC} = \frac{A'B'}{B'C'}$$

---

### 2. Semelhança de Triângulos
Dois triângulos são semelhantes ($\triangle ABC \sim \triangle A'B'C'$) quando possuem ângulos correspondentes congruentes e lados homólogos proporcionais:
$$\frac{a}{a'} = \frac{b}{b'} = \frac{c}{c'} = k \quad (\text{razão de semelhança})$$

- Razão entre perímetros: $k$
- Razão entre áreas: $k^2$
- **Critério Principal (AA)**: Se dois triângulos possuem dois ângulos correspondentes congruentes, eles são semelhantes.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Aplicação de Tales
**Enunciado:** Três retas paralelas cortam duas transversais. Na primeira, os segmentos medem $6$ e $9$. Na segunda, o primeiro segmento mede $8$. Quanto mede o outro?

**Resolução:**
$$\frac{6}{9} = \frac{8}{x} \implies \frac{2}{3} = \frac{8}{x} \implies 2x = 24 \implies x = 12$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Se a razão linear entre duas figuras semelhantes for $k$, a razão entre suas áreas é $k^2$, e entre volumes é $k^3$.
""",
    },
    5: {
        "teoria": r"""# Relações Métricas no Triângulo Retângulo e Pitágoras

O triângulo retângulo é a figura central de toda a metrologia geométrica.

### 1. Elementos e Projeções
No $\triangle ABC$ retângulo em $A$, com hipotenusa $a$, catetos $b, c$, altura relativa à hipotenusa $h$, e projeções ortogonais dos catetos $m$ (de $c$) e $n$ (de $b$):
- $m + n = a$

---

### 2. As Cinco Relações Métricas Fundamentais
1. **Teorema de Pitágoras**:
   $$a^2 = b^2 + c^2$$
2. Quadrado do cateto:
   $$b^2 = a \cdot n \quad \text{e} \quad c^2 = a \cdot m$$
3. Altura e projeções:
   $$h^2 = m \cdot n$$
4. Produto dos catetos e hipotenusa:
   $$b \cdot c = a \cdot h$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Cálculo da Altura Relativa à Hipotenusa
**Enunciado:** Em um triângulo retângulo de catetos $6\text{ cm}$ e $8\text{ cm}$, determine a hipotenusa e a altura $h$.

**Resolução:**
1. Hipotenusa: $a = \sqrt{6^2 + 8^2} = \sqrt{36 + 64} = 10\text{ cm}$.
2. Pela relação $a \cdot h = b \cdot c$:
   $$10 \cdot h = 6 \cdot 8 = 48 \implies h = 4{,}8\text{ cm}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Triângulos pitagóricos notáveis poupam tempo em exames: $(3, 4, 5)$, $(5, 12, 13)$, $(8, 15, 17)$ e seus múltiplos.
""",
    },
    6: {
        "teoria": r"""# Áreas das Principais Figuras Planas e do Círculo

A área quantifica a medida da superfície bidimensional ocupada por uma figura poligonal ou curva.

### 1. Fórmulas de Áreas de Polígonos
- **Retângulo**: $A = b \cdot h$
- **Quadrado**: $A = l^2 = \frac{d^2}{2}$
- **Paralelogramo**: $A = b \cdot h$
- **Triângulo Geral**: $A = \frac{b \cdot h}{2} = \frac{a \cdot b \cdot \sin\theta}{2}$
- **Triângulo Equilátero**: $A = \frac{l^2\sqrt{3}}{4}$
- **Fórmula de Heron** ($p = \text{semiperímetro}$): $A = \sqrt{p(p-a)(p-b)(p-c)}$
- **Losango**: $A = \frac{D \cdot d}{2}$
- **Trapézio**: $A = \frac{(B + b)h}{2}$

---

### 2. Círculo e Suas Partes
- Área do Círculo: $A = \pi R^2$
- Comprimento da Circunferência: $C = 2\pi R$
- Setor Circular de ângulo $\alpha$ (em graus): $A_{\text{setor}} = \frac{\pi R^2 \alpha}{360^\circ}$
- Coroa Circular: $A_{\text{coroa}} = \pi(R^2 - r^2)$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Área do Triângulo Equilátero
**Enunciado:** Calcule a área de um triângulo equilátero cujo lado mede $6\text{ cm}$.

**Resolução:**
$$A = \frac{l^2\sqrt{3}}{4} = \frac{6^2\sqrt{3}}{4} = \frac{36\sqrt{3}}{4} = 9\sqrt{3}\text{ cm}^2$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Não confunda área ($A = \pi R^2$) com comprimento da circunferência ($C = 2\pi R$).
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"Se $B$ é o ponto médio de $AC$ e $AC = 16\text{ cm}$, a medida do segmento $AB$ é:",
            "alternativas": [r"$8\text{ cm}$", r"$4\text{ cm}$", r"$16\text{ cm}$", r"$12\text{ cm}$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O postulado de Euclides afirma que por um ponto fora de uma reta passa:",
            "alternativas": [
                r"Uma única reta paralela à reta dada",
                r"Infinitas retas paralelas",
                r"Nenhuma reta paralela",
                r"Duas retas perpendiculares",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Três pontos colineares distintos determinam quantas retas?",
            "alternativas": [r"Exatamente uma reta", r"Três retas distintas", r"Duas retas", r"Infinitas retas"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"Dois ângulos são suplementares quando a soma de suas medidas é:",
            "alternativas": [r"$180^\circ$", r"$90^\circ$", r"$360^\circ$", r"$45^\circ$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Em um triângulo isósceles com ângulo do vértice medindo $40^\circ$, cada ângulo da base mede:",
            "alternativas": [r"$70^\circ$", r"$80^\circ$", r"$40^\circ$", r"$60^\circ$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Qual caso garante a congruência de dois triângulos conhecendo seus três lados?",
            "alternativas": [r"LLL", r"AAA", r"LAL", r"ALA"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"As diagonais de um losango possuem a propriedade fundamental de serem:",
            "alternativas": [
                r"Perpendiculares entre si e bissetrizes dos ângulos internos",
                r"Congruentes e paralelas",
                r"Sempre de mesma medida",
                r"Exteriores ao polígono",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A soma dos ângulos internos de um quadrilátero convexo qualquer vale:",
            "alternativas": [r"$360^\circ$", r"$180^\circ$", r"$540^\circ$", r"$720^\circ$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Em um paralelogramo, os ângulos consecutivos são sempre:",
            "alternativas": [r"Suplementares", r"Complementares", r"Congruentes", r"Retos"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"Se a razão de semelhança entre dois triângulos é $k = 3$, a razão entre suas áreas é:",
            "alternativas": [r"$9$", r"$3$", r"$6$", r"$27$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O Teorema de Tales garante a proporcionalidade entre segmentos quando retas transversais cortam:",
            "alternativas": [
                r"Um feixe de retas paralelas",
                r"Retas concorrentes perpendiculares",
                r"Dois círculos concêntricos",
                r"Segmentos colineares",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se um triângulo tem lados 4, 6 e 8, um triângulo semelhante com menor lado medindo 8 terá maior lado igual a:",
            "alternativas": [r"$16$", r"$12$", r"$14$", r"$20$"],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"Em um triângulo retângulo com catetos 5 cm e 12 cm, a hipotenusa mede:",
            "alternativas": [r"$13\text{ cm}$", r"$17\text{ cm}$", r"$15\text{ cm}$", r"$14\text{ cm}$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Pela relação métrica $h^2 = m \cdot n$, a altura relativa à hipotenusa cujas projeções medem 4 e 9 vale:",
            "alternativas": [r"$6$", r"$36$", r"$13$", r"$5$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A relação que vincula hipotenusa $a$, catetos $b, c$ e altura $h$ é expressa por:",
            "alternativas": [r"$a \cdot h = b \cdot c$", r"$a^2 = b \cdot h$", r"$h = b + c - a$", r"$a + h = b + c$"],
            "indice_correto": 0,
        },
    ],
    6: [
        {
            "numero": 1,
            "enunciado": r"A área de um triângulo retângulo com catetos medindo 8 cm e 10 cm é:",
            "alternativas": [r"$40\text{ cm}^2$", r"$80\text{ cm}^2$", r"$20\text{ cm}^2$", r"$18\text{ cm}^2$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A área de um círculo de raio 5 cm, em função de $\pi$, vale:",
            "alternativas": [r"$25\pi\text{ cm}^2$", r"$10\pi\text{ cm}^2$", r"$50\pi\text{ cm}^2$", r"$5\pi\text{ cm}^2$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A área de um trapézio de bases 10 cm e 6 cm e altura 4 cm vale:",
            "alternativas": [r"$32\text{ cm}^2$", r"$64\text{ cm}^2$", r"$24\text{ cm}^2$", r"$40\text{ cm}^2$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 15,
        "teorema": "Postulado das Paralelas e Axiomas Fundamentais",
        "texto": (
            "Na geometria euclidiana, por um ponto exterior a uma reta passa uma única paralela à reta dada. "
            "Os conceitos primitivos de ponto, reta e plano estruturam todos os postulados de ordem e separação."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 45,
        "teorema": "Soma dos Ângulos Internos e Casos de Congruência",
        "texto": (
            "A soma dos ângulos internos de um triângulo é 180°. Os quatro casos de congruência (LAL, ALA, LLL, LAAo) "
            "garantem a congruência biunívoca entre todos os lados e ângulos correspondentes."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 85,
        "teorema": "Propriedades dos Paralelogramos e Trapézios",
        "texto": (
            "Paralelogramos possuem lados e ângulos opostos congruentes e diagonais que se cortam nos pontos médios. "
            "O retângulo tem diagonais congruentes e o losango tem diagonais perpendiculares entre si."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 120,
        "teorema": "Teorema de Tales e Semelhança de Triângulos",
        "texto": (
            "O Teorema de Tales assegura que feixes de paralelas determinam segmentos proporcionais em transversais. "
            "Triângulos com ângulos congruentes são semelhantes e suas áreas variam com a razão k²."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 155,
        "teorema": "Relações Métricas no Triângulo Retângulo e Pitágoras",
        "texto": (
            "No triângulo retângulo valem: a² = b² + c² (Pitágoras), h² = m · n, b² = a · n, c² = a · m e ah = bc, "
            "onde m e n são as projeções dos catetos na hipotenusa e h é a altura relativa."
        ),
    },
    {
        "numero_capitulo": 6,
        "pagina": 190,
        "teorema": "Cálculo de Áreas de Superfícies Planas e Círculos",
        "texto": (
            "Áreas fundamentais: triângulo equilátero l²√3/4, losango Dd/2, trapézio (B+b)h/2 e círculo πR². "
            "A fórmula de Heron calcula a área do triângulo exclusivamente em função dos seus três lados e do semiperímetro."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Segmentos e Axiomas (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma reta, os pontos $A, B, C$ estão nessa ordem. Se $AB = 2x + 1$, $BC = 3x - 4$ e $AC = 22$, o valor de $x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$6$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $AB + BC = AC \implies (2x + 1) + (3x - 4) = 22 \implies 5x - 3 = 22 \implies 5x = 25 \implies x = 5$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Some as medidas dos segmentos adjacentes e iguale a 22."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos segmentos de reta distintos são determinados por $5$ pontos colineares distintos?",
        "alternativas": [
            {"letra": "A", "texto": r"$10$", "correta": True},
            {"letra": "B", "texto": r"$5$", "correta": False},
            {"letra": "C", "texto": r"$15$", "correta": False},
            {"letra": "D", "texto": r"$20$", "correta": False},
            {"letra": "E", "texto": r"$25$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cada par de pontos define um segmento: $C_{5, 2} = \frac{5 \times 4}{2} = 10$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a combinação simples $C_{5,2}$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"O ponto $M$ é ponto médio de $AB$. Se $AM = 3x - 5$ e $MB = x + 7$, calcule o comprimento total de $AB$.",
        "alternativas": [],
        "resposta_correta": "26",
        "resolucao_passo_a_passo": r"1. $3x - 5 = x + 7 \implies 2x = 12 \implies x = 6$. 2. $AM = 3(6) - 5 = 13$. $AB = 2 \times 13 = 26$.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Iguale $AM$ a $MB$ e multiplique por 2 no final."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dois segmentos de reta são congruentes quando possuem:",
        "alternativas": [
            {"letra": "A", "texto": r"A mesma medida de comprimento", "correta": True},
            {"letra": "B", "texto": r"A mesma inclinação", "correta": False},
            {"letra": "C", "texto": r"Extremidades coincidentes", "correta": False},
            {"letra": "D", "texto": r"A mesma reta suporte", "correta": False},
            {"letra": "E", "texto": r"Ponto médio comum", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Congruência geométrica de segmentos equivale à igualdade de suas medidas euclidianas. Alternativa A.",
        "parametro_a": 1.100,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Segmentos congruentes têm o mesmo comprimento numérico."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual axioma garante que uma reta contém pelo menos dois pontos distintos?",
        "alternativas": [
            {"letra": "A", "texto": r"Axioma da determinação da reta", "correta": True},
            {"letra": "B", "texto": r"Axioma das paralelas de Euclides", "correta": False},
            {"letra": "C", "texto": r"Axioma de Pasch", "correta": False},
            {"letra": "D", "texto": r"Postulado de Dedekind", "correta": False},
            {"letra": "E", "texto": r"Teorema de Tales", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O axioma de incidência/determinação afirma que dois pontos determinam uma única reta. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Axioma fundamental de incidência euclidiano."},
    },

    # --- Cap 2: Ângulos e Triângulos (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dois ângulos opostos pelo vértice (OPV) medem $3x - 10^\circ$ e $x + 40^\circ$. A medida desses ângulos é:",
        "alternativas": [
            {"letra": "A", "texto": r"$65^\circ$", "correta": True},
            {"letra": "B", "texto": r"$25^\circ$", "correta": False},
            {"letra": "C", "texto": r"$50^\circ$", "correta": False},
            {"letra": "D", "texto": r"$70^\circ$", "correta": False},
            {"letra": "E", "texto": r"$40^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. OPV são congruentes: $3x - 10 = x + 40 \implies 2x = 50 \implies x = 25^\circ$. 2. Ângulo $= 25 + 40 = 65^\circ$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Ângulos opostos pelo vértice têm medidas iguais."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um triângulo, dois ângulos internos medem $55^\circ$ e $65^\circ$. O terceiro ângulo interno mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$60^\circ$", "correta": True},
            {"letra": "B", "texto": r"$70^\circ$", "correta": False},
            {"letra": "C", "texto": r"$50^\circ$", "correta": False},
            {"letra": "D", "texto": r"$80^\circ$", "correta": False},
            {"letra": "E", "texto": r"$65^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A soma dos ângulos internos é $180^\circ$: $180 - (55 + 65) = 180 - 120 = 60^\circ$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Subtraia os dois ângulos de 180 graus."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é a medida em graus do suplemento de um ângulo de $68^\circ$?",
        "alternativas": [],
        "resposta_correta": "112",
        "resolucao_passo_a_passo": r"1. $180 - 68 = 112^\circ$.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Ângulos suplementares somam 180 graus."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Podem constituir os lados de um triângulo os seguintes comprimentos:",
        "alternativas": [
            {"letra": "A", "texto": r"$5\text{ cm}, 7\text{ cm} \text{ e } 10\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$3\text{ cm}, 4\text{ cm} \text{ e } 8\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$2\text{ cm}, 5\text{ cm} \text{ e } 7\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$1\text{ cm}, 2\text{ cm} \text{ e } 4\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$6\text{ cm}, 6\text{ cm} \text{ e } 13\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela desigualdade triangular: a soma dos dois menores deve ser maior que o maior: $5 + 7 = 12 > 10$ (Válido). Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique a desigualdade triangular: a soma de dois lados é sempre maior que o terceiro."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um triângulo retângulo, a mediana relativa à hipotenusa mede $7\text{ cm}$. A hipotenusa mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$14\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$7\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$21\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$10\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$7\sqrt{2}\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Em todo triângulo retângulo, a mediana relativa à hipotenusa vale metade da hipotenusa: $a = 2 \cdot m_a = 2 \times 7 = 14\text{ cm}$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A mediana da hipotenusa é o raio do círculo circunscrito."},
    },

    # --- Cap 3: Quadriláteros Notáveis (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"As diagonais de um losango medem $10\text{ cm}$ e $24\text{ cm}$. O lado desse losango mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$13\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$12\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$15\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$14\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$17\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. As semidiagonais são perpendiculares: $5\text{ cm}$ e $12\text{ cm}$. 2. Lado: $l = \sqrt{5^2 + 12^2} = \sqrt{25 + 144} = \sqrt{169} = 13\text{ cm}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "As metades das diagonais formam um triângulo retângulo com o lado."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma dos ângulos internos de um hexágono convexo ($n = 6$) vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$720^\circ$", "correta": True},
            {"letra": "B", "texto": r"$540^\circ$", "correta": False},
            {"letra": "C", "texto": r"$900^\circ$", "correta": False},
            {"letra": "D", "texto": r"$1080^\circ$", "correta": False},
            {"letra": "E", "texto": r"$360^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $S_i = (n - 2) \cdot 180^\circ = (6 - 2) \cdot 180^\circ = 4 \cdot 180^\circ = 720^\circ$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Fórmula da soma dos ângulos internos: $(n-2) \cdot 180^\circ$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Quantas diagonais possui um octógono convexo ($n = 8$)?",
        "alternativas": [],
        "resposta_correta": "20",
        "resolucao_passo_a_passo": r"1. $d = \frac{n(n - 3)}{2} = \frac{8(5)}{2} = 20$.",
        "parametro_a": 1.300,
        "parametro_b": 0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Use $d = \frac{n(n-3)}{2}$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um trapézio isósceles, os ângulos adjacentes à mesma base são:",
        "alternativas": [
            {"letra": "A", "texto": r"Congruentes", "correta": True},
            {"letra": "B", "texto": r"Suplementares", "correta": False},
            {"letra": "C", "texto": r"Complementares", "correta": False},
            {"letra": "D", "texto": r"Retos", "correta": False},
            {"letra": "E", "texto": r"Diferentes", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela simetria do trapézio isósceles, os ângulos de cada base são rigorosamente congruentes. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Trapézios isósceles possuem eixo de simetria mediador das bases."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O segmento que une os pontos médios das diagonais de um trapézio de bases $B = 18$ e $b = 10$ mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$14$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$5$", "correta": False},
            {"letra": "E", "texto": r"$2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Segmento de Euler: $\frac{B - b}{2} = \frac{18 - 10}{2} = \frac{8}{2} = 4$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Fórmula do segmento que une os pontos médios das diagonais: $\frac{B-b}{2}$."},
    },

    # --- Cap 4: Tales e Semelhança (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma reta paralela ao lado $BC$ do triângulo $ABC$ corta $AB$ em $D$ e $AC$ em $E$. Se $AD = 6$, $DB = 3$ e $AE = 8$, o segmento $EC$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$12$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\frac{6}{3} = \frac{8}{EC} \implies 2 = \frac{8}{EC} \implies EC = 4$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Pelo Teorema de Tales: $\frac{AD}{DB} = \frac{AE}{EC}$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dois triângulos semelhantes têm perímetros $20\text{ cm}$ e $50\text{ cm}$. Se a área do menor é $16\text{ cm}^2$, a área do maior é:",
        "alternativas": [
            {"letra": "A", "texto": r"$100\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$40\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$64\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$80\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$250\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Razão linear $k = 50/20 = 5/2 = 2{,}5$. 2. Razão das áreas $k^2 = (5/2)^2 = 25/4$. 3. Área maior $= 16 \times (25/4) = 100\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A razão de áreas é o quadrado da razão de perímetros."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um poste vertical projeta uma sombra de $4\text{ m}$ ao mesmo tempo que uma haste vertical de $1\text{ m}$ projeta sombra de $0{,}5\text{ m}$. Qual é a altura do poste em metros?",
        "alternativas": [],
        "resposta_correta": "8",
        "resolucao_passo_a_passo": r"1. Por semelhança: $\frac{H}{4} = \frac{1}{0{,}5} \implies H = 4 \times 2 = 8\text{ m}$.",
        "parametro_a": 1.200,
        "parametro_b": -0.700,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Proporção entre altura e sombra."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O Teorema da Bissetriz Interna divide o lado oposto em segmentos proporcionais aos lados adjacentes. Em um $\triangle ABC$ com $AB = 6, AC = 9$ e $BC = 10$, o menor segmento determinado pela bissetriz de $\hat{A}$ sobre $BC$ mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$5$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$4{,}5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\frac{x}{10 - x} = \frac{6}{9} = \frac{2}{3} \implies 3x = 20 - 2x \implies 5x = 20 \implies x = 4$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique o Teorema da Bissetriz Interna: $\frac{x}{y} = \frac{c}{b}$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dois triângulos equiláteros são sempre:",
        "alternativas": [
            {"letra": "A", "texto": r"Semelhantes", "correta": True},
            {"letra": "B", "texto": r"Congruentes", "correta": False},
            {"letra": "C", "texto": r"Equivalentes em área", "correta": False},
            {"letra": "D", "texto": r"Isoperimétricos", "correta": False},
            {"letra": "E", "texto": r"Retângulos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Todos os ângulos internos de qualquer triângulo equilátero medem $60^\circ$. Pelo critério AA, são semelhantes. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Todos os triângulos regulares com mesma quantidade de lados são semelhantes."},
    },

    # --- Cap 5: Triângulo Retângulo e Pitágoras (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um triângulo retângulo possui catetos medindo $6\text{ cm}$ e $8\text{ cm}$. Qual é a medida da hipotenusa em centímetros?",
        "alternativas": [
            {"letra": "A", "texto": r"$10\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$12\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$14\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$9\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$7\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $h^2 = 6^2 + 8^2 = 36 + 64 = 100 \implies h = 10\text{ cm}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique o Teorema de Pitágoras."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um triângulo retângulo, a hipotenusa mede $25$ e a projeção de um dos catetos sobre ela mede $9$. O cateto correspondente mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$15$", "correta": True},
            {"letra": "B", "texto": r"$12$", "correta": False},
            {"letra": "C", "texto": r"$20$", "correta": False},
            {"letra": "D", "texto": r"$16$", "correta": False},
            {"letra": "E", "texto": r"$10$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Relação métrica: $c^2 = a \cdot m = 25 \times 9 = 225 \implies c = 15$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a relação $c^2 = a \cdot m$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"A altura de um triângulo equilátero de lado $6\sqrt{3}$ vale:",
        "alternativas": [],
        "resposta_correta": "9",
        "resolucao_passo_a_passo": r"1. $h = \frac{l\sqrt{3}}{2} = \frac{6\sqrt{3} \cdot \sqrt{3}}{2} = \frac{6 \cdot 3}{2} = 9$.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Use $h = \frac{l\sqrt{3}}{2}$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A diagonal de um quadrado de lado $5\text{ cm}$ mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$5\sqrt{2}\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$10\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$5\sqrt{3}\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$25\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$7\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $d = l\sqrt{2} = 5\sqrt{2}\text{ cm}$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A diagonal do quadrado é $l\sqrt{2}$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um triângulo retângulo com catetos $9$ e $12$, a altura relativa à hipotenusa é:",
        "alternativas": [
            {"letra": "A", "texto": r"$7{,}2$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$7$", "correta": False},
            {"letra": "E", "texto": r"$5{,}4$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Hipotenusa: $\sqrt{9^2 + 12^2} = 15$. 2. $a \cdot h = b \cdot c \implies 15h = 9 \times 12 = 108 \implies h = 108/15 = 7{,}2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique $a \cdot h = b \cdot c$."},
    },

    # --- Cap 6: Áreas de Figuras Planas (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é a área de um círculo de raio $6\text{ cm}$, em função de $\pi$?",
        "alternativas": [
            {"letra": "A", "texto": r"$36\pi\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$12\pi\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$18\pi\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$6\pi\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$72\pi\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A = \pi r^2 = \pi \cdot 6^2 = 36\pi\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $A = \pi r^2$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A área de um setor circular de $60^\circ$ em um círculo de raio $6\text{ cm}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6\pi\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$12\pi\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$3\pi\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$36\pi\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$\pi\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A_{\text{setor}} = \frac{60^\circ}{360^\circ} \times \pi(6^2) = \frac{1}{6} \times 36\pi = 6\pi\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Calcule a fração da área total correspondente a 60 graus."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"A área de um paralelogramo com base $15\text{ cm}$ e altura $8\text{ cm}$ é:",
        "alternativas": [],
        "resposta_correta": "120",
        "resolucao_passo_a_passo": r"1. $A = b \cdot h = 15 \times 8 = 120\text{ cm}^2$.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Multiplique base por altura."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A área de uma coroa circular delimitada por raios $R = 5\text{ cm}$ e $r = 3\text{ cm}$ em função de $\pi$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$16\pi\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$25\pi\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$9\pi\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$4\pi\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$8\pi\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A = \pi(R^2 - r^2) = \pi(25 - 9) = 16\pi\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Subtraia a área do círculo menor da do círculo maior."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dobrando-se o raio de um círculo, sua área fica multiplicada por:",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$2$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$16$", "correta": False},
            {"letra": "E", "texto": r"Permanece inalterada", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A' = \pi(2R)^2 = 4\pi R^2 = 4A$. A área quadruplica. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "O raio é elevado ao quadrado no cálculo da área."},
    },
]
