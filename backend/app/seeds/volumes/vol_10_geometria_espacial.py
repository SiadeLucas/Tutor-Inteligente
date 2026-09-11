"""
Módulo Canônico de Dados Didáticos — Volume 10: Geometria Espacial
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
    "numero": 10,
    "titulo": "Geometria Espacial",
    "grande_area": "geometria",
    "ordem": 10,
    "capitulos": [
        {"num": 1, "titulo": "Postulados do Espaço, Retas e Planos", "tempo": 50},
        {"num": 2, "titulo": "Perpendicularismo e Projeções Ortogonais", "tempo": 50},
        {"num": 3, "titulo": "Poliedros Convexos e Relação de Euler", "tempo": 50},
        {"num": 4, "titulo": "Prismas e Cilindros: Áreas e Volumes", "tempo": 50},
        {"num": 5, "titulo": "Pirâmides e Cones: Apótema e Volumes", "tempo": 50},
        {"num": 6, "titulo": "A Esfera e Suas Partes: Área e Volume", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Postulados do Espaço, Retas e Planos

A geometria euclidiana tridimensional amplia os conceitos do plano, introduzindo novas posições relativas e axiomas de determinação no espaço $\mathbb{R}^3$.

### 1. Determinação do Plano
Um plano é determinado de forma única por:
1. Três pontos não-colineares.
2. Uma reta e um ponto fora dela.
3. Duas retas concorrentes.
4. Duas retas paralelas distintas.

---

### 2. Posições Relativas entre Retas no Espaço
- **Coplanares**:
  - Concorrentes (1 ponto comum).
  - Paralelas (distintas ou coincidentes).
- **Não-Coplanares**:
  - **Retas Reversas**: Não possuem ponto comum e não pertencem a um mesmo plano.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Retas Reversas no Cubo
**Enunciado:** Em um cubo $ABCD-EFGH$, qual a posição relativa entre a aresta da base $AB$ e a aresta vertical oposta $CG$?

**Resolução:**
$AB$ e $CG$ não se intersectam e não estão contidas em nenhuma face ou plano comum do espaço. Logo, são **retas reversas**.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> No espaço, duas retas sem pontos comuns **não são necessariamente paralelas**! Elas podem ser reversas.
""",
    },
    2: {
        "teoria": r"""# Perpendicularismo e Projeções Ortogonais

### 1. Reta Perpendicular a Plano
Uma reta $r$ é perpendicular a um plano $\alpha$ ($r \perp \alpha$) se for ortogonal a **todas** as retas do plano que passam pelo traço.
- **Critério Prático**: Basta que $r$ seja perpendicular a **duas retas concorrentes** de $\alpha$.

---

### 2. Teorema das Três Perpendiculares
Seja uma reta $r$ perpendicular a um plano $\alpha$ em $P$. Se por $P$ traçamos uma reta $s \subset \alpha$ perpendicular a uma reta $t \subset \alpha$ no ponto $Q$, então qualquer reta que ligue um ponto $A \in r$ ao ponto $Q$ é perpendicular a $t$:
$$AQ \perp t$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Aplicação do Teorema das Três Perpendiculares
**Enunciado:** Um segmento vertical $AP$ de comprimento $12\text{ cm}$ é perpendicular a um plano $\alpha$ em $P$. Uma reta $t \subset \alpha$ dista $5\text{ cm}$ de $P$. Qual a distância de $A$ à reta $t$?

**Resolução:**
Pelo Teorema das Três Perpendiculares, a distância de $A$ a $t$ é a hipotenusa do triângulo retângulo com catetos $12$ e $5$:
$$d = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = \sqrt{169} = 13\text{ cm}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Retas ortogonais no espaço podem ou não ser concorrentes (se não forem concorrentes, são reversas ortogonais).
""",
    },
    3: {
        "teoria": r"""# Poliedros Convexos e Relação de Euler

Um poliedro é a região fechada do espaço delimitada por polígonos planos denominados faces.

### 1. Relação de Euler para Poliedros Convexos
Para todo poliedro convexo com $V$ vértices, $A$ arestas e $F$ faces:
$$V - A + F = 2$$

- Contagem de Arestas:
  $$2A = \sum n_i \cdot F_i = \sum m_j \cdot V_j$$
  onde $F_i$ é o número de faces com $n_i$ lados.

---

### 2. Os Cinco Poliedros Regulares de Platão
1. Tetraedro regular (4 faces triangulares, $V=4, A=6, F=4$)
2. Hexaedro regular / Cubo (6 faces quadradas, $V=8, A=12, F=6$)
3. Octaedro regular (8 faces triangulares, $V=6, A=12, F=8$)
4. Dodecaedro regular (12 faces pentagonais, $V=20, A=30, F=12$)
5. Icosaedro regular (20 faces triangulares, $V=12, A=30, F=20$)
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Poliedro com Faces Mistas
**Enunciado:** Um poliedro convexo possui 6 faces quadrangulares e 8 faces triangulares. Quantos vértices ele possui?

**Resolução:**
1. Total de faces: $F = 6 + 8 = 14$.
2. Total de arestas: $2A = 6(4) + 8(3) = 24 + 24 = 48 \implies A = 24$.
3. Relação de Euler: $V - 24 + 14 = 2 \implies V - 10 = 2 \implies V = 12$ vértices.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Cada aresta pertence a exatamente **duas faces**, por isso a soma dos lados de todas as faces é sempre igual ao **dobro das arestas** ($2A$).
""",
    },
    4: {
        "teoria": r"""# Prismas e Cilindros: Áreas e Volumes

Prismas e cilindros compartilham a propriedade fundamental de possuírem duas bases paralelas e congruentes, regidos pelo Princípio de Cavalieri.

### 1. Prismas
- **Área Lateral ($A_L$)**: Soma das áreas das faces laterais.
- **Área Total**: $A_T = A_L + 2A_B$
- **Volume**:
  $$V = A_B \cdot h$$
- **Paralelepípedo Reto-Retângulo**: Dimensões $a, b, c$:
  $$d = \sqrt{a^2 + b^2 + c^2}, \quad A_T = 2(ab + ac + bc), \quad V = a \cdot b \cdot c$$
- **Cubo de Aresta $a$**: $d = a\sqrt{3}, \quad A_T = 6a^2, \quad V = a^3$

---

### 2. Cilindro Circular Reto
- Raio da base $R$ e altura $h$:
  $$A_B = \pi R^2, \quad A_L = 2\pi R h, \quad A_T = 2\pi R(h + R)$$
  $$V = \pi R^2 h$$
- **Cilindro Equilátero**: Altura igual ao diâmetro da base ($h = 2R$).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Volume do Cilindro Equilátero
**Enunciado:** Calcule o volume de um cilindro equilátero de raio $R = 3\text{ cm}$.

**Resolução:**
1. Em cilindro equilátero, $h = 2R = 2(3) = 6\text{ cm}$.
2. Volume: $V = \pi R^2 h = \pi (3^2)(6) = 54\pi\text{ cm}^3$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Pelo Princípio de Cavalieri, sólidos com mesma altura e seções transversais de áreas iguais a qualquer altura possuem **o mesmo volume**, mesmo se forem inclinados (oblíquos).
""",
    },
    5: {
        "teoria": r"""# Pirâmides e Cones: Apótema e Volumes

Pirâmides e cones convergem suas geratrizes em um único vértice comum, possuindo um terço do volume do prisma correspondente.

### 1. Pirâmides Regulares
- **Volume Geral**:
  $$V = \frac{1}{3} A_B \cdot h$$
- Relação Pitagórica Fundamental na Pirâmide Regular:
  $$g^2 = h^2 + m^2$$
  onde $g$ é o apótema da pirâmide e $m$ é o apótema da base.

---

### 2. Cone Circular Reto
- Raio $R$, altura $h$ e geratriz $g$:
  $$g^2 = h^2 + R^2$$
  $$A_B = \pi R^2, \quad A_L = \pi R g, \quad A_T = \pi R(g + R)$$
  $$V = \frac{1}{3}\pi R^2 h$$
- **Cone Equilátero**: Geratriz igual ao diâmetro da base ($g = 2R \implies h = R\sqrt{3}$).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Volume do Cone
**Enunciado:** Um cone reto tem raio da base $6\text{ cm}$ e geratriz $10\text{ cm}$. Calcule seu volume em função de $\pi$.

**Resolução:**
1. Altura por Pitágoras: $h = \sqrt{g^2 - R^2} = \sqrt{10^2 - 6^2} = \sqrt{100 - 36} = 8\text{ cm}$.
2. Volume: $V = \frac{1}{3}\pi R^2 h = \frac{1}{3}\pi (36)(8) = 12 \times 8 \pi = 96\pi\text{ cm}^3$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Não confunda a geratriz $g$ (hipotenusa) com a altura $h$ do cone! A fórmula do volume usa a altura $h$.
""",
    },
    6: {
        "teoria": r"""# A Esfera e Suas Partes: Área e Volume

A esfera é o sólido de revolução perfeito gerado pela rotação de um semicírculo em torno do seu diâmetro.

### 1. Área e Volume da Esfera
Para uma esfera de raio $R$:
- **Área da Superfície Esférica**:
  $$A = 4\pi R^2$$
- **Volume da Esfera (Arquimedes)**:
  $$V = \frac{4}{3}\pi R^3$$

---

### 2. Seção Plana da Esfera
A interseção de um plano que dista $d$ ($d < R$) do centro da esfera determina um círculo de raio $r$:
$$R^2 = d^2 + r^2$$

---

### 3. Fuso e Cunha Esférica
- **Fuso Esférico (Área)**: $A_{\text{fuso}} = \frac{4\pi R^2 \alpha}{360^\circ} = \frac{\pi R^2 \alpha}{90^\circ}$
- **Cunha Esférica (Volume)**: $V_{\text{cunha}} = \frac{\frac{4}{3}\pi R^3 \alpha}{360^\circ} = \frac{\pi R^3 \alpha}{270^\circ}$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Seção Plana da Esfera
**Enunciado:** Uma esfera de raio $R = 10\text{ cm}$ é seccionada por um plano que dista $6\text{ cm}$ do centro. Calcule a área da seção circular plana.

**Resolução:**
1. Raio da seção: $r = \sqrt{R^2 - d^2} = \sqrt{10^2 - 6^2} = \sqrt{100 - 36} = 8\text{ cm}$.
2. Área da seção circular: $A = \pi r^2 = \pi (8^2) = 64\pi\text{ cm}^2$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Na esfera o raio é elevado ao quadrado para a área ($4\pi R^2$) e ao **cubo** para o volume ($\frac{4}{3}\pi R^3$).
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"Duas retas no espaço que não possuem nenhum ponto em comum e não pertencem ao mesmo plano são chamadas de:",
            "alternativas": [r"Retas reversas", r"Retas paralelas distintas", r"Retas concorrentes", r"Retas coincidentes"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Quantos pontos não-colineares são necessários para determinar de forma única um plano no espaço?",
            "alternativas": [r"3", r"2", r"4", r"Infinitos"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se uma reta é paralela a um plano, ela tem com esse plano:",
            "alternativas": [r"Nenhum ponto em comum", r"Exatamente um ponto", r"Dois pontos", r"Infinitos pontos"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"Para que uma reta seja perpendicular a um plano, basta que seja perpendicular a:",
            "alternativas": [
                r"Duas retas concorrentes contidas no plano",
                r"Uma única reta do plano",
                r"Duas retas paralelas do plano",
                r"Três retas paralelas do plano",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A projeção ortogonal de um segmento de reta não-perpendicular sobre um plano é:",
            "alternativas": [r"Um segmento de reta", r"Um ponto", r"Uma parábola", r"Um círculo"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A projeção ortogonal de uma reta perpendicular ao plano de projeção é:",
            "alternativas": [r"Um ponto", r"Uma reta", r"Um plano", r"Um segmento"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"A relação de Euler para poliedros convexos é expressa por:",
            "alternativas": [r"$V - A + F = 2$", r"$V + A - F = 2$", r"$V + A + F = 2$", r"$V - A - F = 2$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Quantas arestas possui um cubo (hexaedro regular)?",
            "alternativas": [r"$12$", r"$8$", r"$6$", r"$16$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Um poliedro com 8 vértices e 6 faces possui quantas arestas?",
            "alternativas": [r"$12$", r"$10$", r"$14$", r"$16$"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"O volume de um paralelepípedo retângulo com dimensões 3 cm, 4 cm e 5 cm é:",
            "alternativas": [r"$60\text{ cm}^3$", r"$94\text{ cm}^3$", r"$30\text{ cm}^3$", r"$120\text{ cm}^3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O volume de um cilindro reto com raio da base 4 cm e altura 10 cm, em função de $\pi$, vale:",
            "alternativas": [r"$160\pi\text{ cm}^3$", r"$80\pi\text{ cm}^3$", r"$40\pi\text{ cm}^3$", r"$320\pi\text{ cm}^3$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A diagonal de um cubo de aresta $4\text{ cm}$ mede:",
            "alternativas": [r"$4\sqrt{3}\text{ cm}$", r"$4\sqrt{2}\text{ cm}$", r"$8\text{ cm}$", r"$12\text{ cm}$"],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"O volume de uma pirâmide regular de base quadrada com lado 6 cm e altura 10 cm é:",
            "alternativas": [r"$120\text{ cm}^3$", r"$360\text{ cm}^3$", r"$60\text{ cm}^3$", r"$180\text{ cm}^3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O volume de um cone reto com raio da base 3 cm e altura 4 cm, em função de $\pi$, é:",
            "alternativas": [r"$12\pi\text{ cm}^3$", r"$36\pi\text{ cm}^3$", r"$15\pi\text{ cm}^3$", r"$24\pi\text{ cm}^3$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A geratriz de um cone reto com raio 5 cm e altura 12 cm mede:",
            "alternativas": [r"$13\text{ cm}$", r"$17\text{ cm}$", r"$15\text{ cm}$", r"$10\text{ cm}$"],
            "indice_correto": 0,
        },
    ],
    6: [
        {
            "numero": 1,
            "enunciado": r"O volume de uma esfera de raio 3 cm, em função de $\pi$, vale:",
            "alternativas": [r"$36\pi\text{ cm}^3$", r"$12\pi\text{ cm}^3$", r"$27\pi\text{ cm}^3$", r"$108\pi\text{ cm}^3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A área da superfície de uma esfera de raio 5 cm, em função de $\pi$, é:",
            "alternativas": [r"$100\pi\text{ cm}^2$", r"$25\pi\text{ cm}^2$", r"$50\pi\text{ cm}^2$", r"$500\pi/3\text{ cm}^2$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se o raio de uma esfera for duplicado, seu volume fica multiplicado por:",
            "alternativas": [r"$8$", r"$4$", r"$2$", r"$16$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 20,
        "teorema": "Axiomas de Determinação do Plano e Retas Reversas",
        "texto": (
            "No espaço R³, três pontos não-colineares determinam um plano único. Duas retas não-coplanares sem pontos "
            "comuns são denominadas retas reversas."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 55,
        "teorema": "Teorema das Três Perpendiculares e Projeções Ortogonais",
        "texto": (
            "Se uma reta é perpendicular a um plano, qualquer reta ligando um de seus pontos ao pé de uma perpendicular "
            "no plano é ortogonal à transversal correspondente no plano."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 90,
        "teorema": "Relação de Euler e Poliedros de Platão",
        "texto": (
            "Para todo poliedro convexo vale V - A + F = 2 e 2A = Σ n_i F_i. Os poliedros regulares de Platão são exatamente "
            "cinco: tetraedro, cubo, octaedro, dodecaedro e icosaedro."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 130,
        "teorema": "Prisma, Cilindro e Princípio de Cavalieri",
        "texto": (
            "O volume de prismas e cilindros é dado por V = A_B · h. O Princípio de Cavalieri garante equivalência volumétrica "
            "entre sólidos de mesma altura com seções transversais coplanares de áreas iguais."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 165,
        "teorema": "Pirâmides, Cones e Fórmulas de Volume",
        "texto": (
            "Pirâmides e cones possuem volume dado por V = (1/3) A_B · h. No cone reto vale g² = h² + R² e a área lateral "
            "é dada por A_L = π R g."
        ),
    },
    {
        "numero_capitulo": 6,
        "pagina": 200,
        "teorema": "A Esfera: Área da Superfície e Volume de Arquimedes",
        "texto": (
            "A esfera de raio R possui área superficial A = 4πR² e volume V = (4/3)πR³. Toda seção plana a uma distância d "
            "do centro é um círculo de raio r = √(R² - d²)."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Postulados e Retas (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Duas retas reversas no espaço:",
        "alternativas": [
            {"letra": "A", "texto": r"Não são coplanares e não se intersectam", "correta": True},
            {"letra": "B", "texto": r"São coplanares e não se intersectam", "correta": False},
            {"letra": "C", "texto": r"Possuem um único ponto de interseção", "correta": False},
            {"letra": "D", "texto": r"São sempre perpendiculares", "correta": False},
            {"letra": "E", "texto": r"Pertencem a planos coincidentes", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Definição formal: retas reversas são retas não-coplanares (logo sem interseção). Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Retas reversas não estão no mesmo plano."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos planos distintos são determinados por 4 pontos não-coplanares no espaço?",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$1$", "correta": False},
            {"letra": "D", "texto": r"$8$", "correta": False},
            {"letra": "E", "texto": r"Infinitos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cada 3 pontos não-colineares formam um plano: $C_{4, 3} = 4$ planos (faces de um tetraedro). Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique $C_{4,3}$ para escolher 3 pontos."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se dois planos distintos se interceptam, sua interseção é:",
        "alternativas": [
            {"letra": "A", "texto": r"Uma única reta", "correta": True},
            {"letra": "B", "texto": r"Um único ponto", "correta": False},
            {"letra": "C", "texto": r"Dois pontos", "correta": False},
            {"letra": "D", "texto": r"Um segmento finito", "correta": False},
            {"letra": "E", "texto": r"Vazio", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pelo postulado da interseção de planos, dois planos secantes têm como interseção uma reta. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A interseção de dois planos secantes é uma reta."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"No cubo, quantas arestas são reversas a uma aresta fixada?",
        "alternativas": [],
        "resposta_correta": "4",
        "resolucao_passo_a_passo": r"1. Um cubo tem 12 arestas. Fixando uma: 1 coincidentes/própria, 3 paralelas, 4 concorrentes. Restam $12 - 1 - 3 - 4 = 4$ arestas reversas.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Conte as arestas que não são paralelas nem tocam a aresta dada."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se uma reta $r$ é paralela a uma reta $s$ contida num plano $\alpha$, então:",
        "alternativas": [
            {"letra": "A", "texto": r"$r$ é paralela a $\alpha$ ou está contida em $\alpha$", "correta": True},
            {"letra": "B", "texto": r"$r$ é obrigatoriamente concorrente com $\alpha$", "correta": False},
            {"letra": "C", "texto": r"$r$ é perpendicular a $\alpha$", "correta": False},
            {"letra": "D", "texto": r"$r$ e $\alpha$ possuem um único ponto comum", "correta": False},
            {"letra": "E", "texto": r"$r$ é reversa a $\alpha$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Se $r$ é paralela a $s \subset \alpha$, então $r$ não pode furar o plano: ou é paralela ou está contida em $\alpha$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Critério de paralelismo entre reta e plano."},
    },

    # --- Cap 2: Perpendicularismo e Projeções (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um segmento $AB = 10\text{ cm}$ forma um ângulo de $60^\circ$ com um plano $\alpha$. O comprimento de sua projeção ortogonal sobre $\alpha$ mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$5\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$5\sqrt{3}\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$10\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$20\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$5\sqrt{2}\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A'B' = AB \cdot \cos 60^\circ = 10 \cdot (1/2) = 5\text{ cm}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A projeção ortogonal vale $L \cdot \cos\theta$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O Teorema das Três Perpendiculares conecta:",
        "alternativas": [
            {"letra": "A", "texto": r"Uma reta perpendicular a um plano com perpendiculares no plano", "correta": True},
            {"letra": "B", "texto": r"Três planos mutuamente paralelos", "correta": False},
            {"letra": "C", "texto": r"Três ângulos de um triângulo equilátero", "correta": False},
            {"letra": "D", "texto": r"As alturas de um tetraedro", "correta": False},
            {"letra": "E", "texto": r"Três eixos cartesianos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O Teorema das Três Perpendiculares garante ortogonalidade entre retas espaciais e retas no plano. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Conexão de perpendicularidade reta-plano."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um ponto $P$ dista $8\text{ cm}$ de um plano $\alpha$. Um segmento traçado de $P$ a um ponto $Q \in \alpha$ mede $10\text{ cm}$. Qual é a distância da projeção de $P$ até $Q$?",
        "alternativas": [],
        "resposta_correta": "6",
        "resolucao_passo_a_passo": r"1. Por Pitágoras: $d = \sqrt{10^2 - 8^2} = \sqrt{100 - 64} = 6\text{ cm}$.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Aplique Pitágoras no triângulo retângulo formado pela distância e projeção."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se dois planos são perpendiculares a uma mesma reta, eles são entre si:",
        "alternativas": [
            {"letra": "A", "texto": r"Paralelos", "correta": True},
            {"letra": "B", "texto": r"Perpendiculares", "correta": False},
            {"letra": "C", "texto": r"Concorrentes oblíquos", "correta": False},
            {"letra": "D", "texto": r"Coincidentes necessariamente", "correta": False},
            {"letra": "E", "texto": r"Reversos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Dois planos normais à mesma reta têm vetores normais paralelos, logo são paralelos entre si. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Planos com mesma reta normal são paralelos."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O ângulo diédrico reto mede:",
        "alternativas": [
            {"letra": "A", "texto": r"$90^\circ$", "correta": True},
            {"letra": "B", "texto": r"$180^\circ$", "correta": False},
            {"letra": "C", "texto": r"$45^\circ$", "correta": False},
            {"letra": "D", "texto": r"$60^\circ$", "correta": False},
            {"letra": "E", "texto": r"$0^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O diedro formado por planos ortogonais mede $90^\circ$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Diedro reto corresponde a 90 graus."},
    },

    # --- Cap 3: Poliedros Convexos e Euler (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um poliedro convexo possui $12$ faces e $20$ vértices. O número de arestas desse poliedro é:",
        "alternativas": [
            {"letra": "A", "texto": r"$30$", "correta": True},
            {"letra": "B", "texto": r"$32$", "correta": False},
            {"letra": "C", "texto": r"$28$", "correta": False},
            {"letra": "D", "texto": r"$24$", "correta": False},
            {"letra": "E", "texto": r"$40$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Euler: $V - A + F = 2 \implies 20 - A + 12 = 2 \implies 32 - A = 2 \implies A = 30$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a relação de Euler: $V - A + F = 2$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um poliedro convexo tem 20 faces triangulares (icosaedro). Quantas arestas ele possui?",
        "alternativas": [
            {"letra": "A", "texto": r"$30$", "correta": True},
            {"letra": "B", "texto": r"$60$", "correta": False},
            {"letra": "C", "texto": r"$20$", "correta": False},
            {"letra": "D", "texto": r"$40$", "correta": False},
            {"letra": "E", "texto": r"$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $2A = 20 \times 3 = 60 \implies A = 30$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Multiplique as faces pelo número de lados e divida por 2."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Quantos vértices possui um octaedro regular ($8$ faces triangulares)?",
        "alternativas": [],
        "resposta_correta": "6",
        "resolucao_passo_a_passo": r"1. $F = 8$. $2A = 8 \times 3 = 24 \implies A = 12$. 2. $V - 12 + 8 = 2 \implies V = 6$.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Aplique Euler no octaedro regular."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma dos ângulos de todas as faces de um poliedro convexo com $V$ vértices é dada por:",
        "alternativas": [
            {"letra": "A", "texto": r"$(V - 2) \cdot 360^\circ$", "correta": True},
            {"letra": "B", "texto": r"$(F - 2) \cdot 360^\circ$", "correta": False},
            {"letra": "C", "texto": r"$(A - 2) \cdot 180^\circ$", "correta": False},
            {"letra": "D", "texto": r"$V \cdot 180^\circ$", "correta": False},
            {"letra": "E", "texto": r"$(V - 2) \cdot 180^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Teorema de Descartes para a soma dos ângulos das faces: $S = (V - 2) \cdot 360^\circ$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Fórmula de Descartes: $(V - 2) \cdot 360^\circ$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O único poliedro regular de Platão que possui faces pentagonais é o:",
        "alternativas": [
            {"letra": "A", "texto": r"Dodecaedro regular", "correta": True},
            {"letra": "B", "texto": r"Icosaedro regular", "correta": False},
            {"letra": "C", "texto": r"Octaedro regular", "correta": False},
            {"letra": "D", "texto": r"Tetraedro regular", "correta": False},
            {"letra": "E", "texto": r"Hexaedro regular", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O dodecaedro regular possui 12 faces pentagonais regulares. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Dodecaedro = 12 pentágonos."},
    },

    # --- Cap 4: Prismas e Cilindros (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A diagonal de um paralelepípedo retângulo de dimensões $2\text{ cm}, 3\text{ cm}$ e $6\text{ cm}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$7\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$11\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$\sqrt{49}\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$6\sqrt{2}\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$8\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $d = \sqrt{a^2 + b^2 + c^2} = \sqrt{2^2 + 3^2 + 6^2} = \sqrt{4 + 9 + 36} = \sqrt{49} = 7\text{ cm}$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $d = \sqrt{a^2 + b^2 + c^2}$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um cilindro reto tem raio da base $5\text{ cm}$ e altura $8\text{ cm}$. Sua área lateral, em função de $\pi$, é:",
        "alternativas": [
            {"letra": "A", "texto": r"$80\pi\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$40\pi\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$160\pi\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$200\pi\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$50\pi\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A_L = 2\pi R h = 2\pi (5)(8) = 80\pi\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Área lateral do cilindro: $2\pi R h$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule a área total de um cubo cuja aresta mede $5\text{ cm}$.",
        "alternativas": [],
        "resposta_correta": "150",
        "resolucao_passo_a_passo": r"1. $A_T = 6a^2 = 6(5^2) = 6 \times 25 = 150\text{ cm}^2$.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Multiplique 6 pela área de uma face quadrada."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um prisma triangular regular tem aresta da base $4\text{ cm}$ e altura $10\text{ cm}$. O volume desse prisma é:",
        "alternativas": [
            {"letra": "A", "texto": r"$40\sqrt{3}\text{ cm}^3$", "correta": True},
            {"letra": "B", "texto": r"$20\sqrt{3}\text{ cm}^3$", "correta": False},
            {"letra": "C", "texto": r"$80\sqrt{3}\text{ cm}^3$", "correta": False},
            {"letra": "D", "texto": r"$160\text{ cm}^3$", "correta": False},
            {"letra": "E", "texto": r"$40\text{ cm}^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Base equilátera: $A_B = \frac{4^2\sqrt{3}}{4} = 4\sqrt{3}$. 2. $V = A_B \cdot h = 4\sqrt{3} \times 10 = 40\sqrt{3}\text{ cm}^3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Calcule a área do triângulo equilátero da base e multiplique pela altura."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um cilindro equilátero, a seção meridiana é um:",
        "alternativas": [
            {"letra": "A", "texto": r"Quadrado de lado igual ao diâmetro da base", "correta": True},
            {"letra": "B", "texto": r"Retângulo de base igual à altura", "correta": False},
            {"letra": "C", "texto": r"Círculo de raio igual à altura", "correta": False},
            {"letra": "D", "texto": r"Triângulo equilátero", "correta": False},
            {"letra": "E", "texto": r"Losango", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. No cilindro equilátero $h = 2R$. A seção meridiana tem base $2R$ e altura $h = 2R$, sendo um quadrado. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Cilindro equilátero tem altura igual ao diâmetro."},
    },

    # --- Cap 5: Pirâmides e Cones (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma pirâmide regular de base quadrada tem aresta da base $8\text{ cm}$ e apótema da pirâmide $5\text{ cm}$. A altura da pirâmide é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$4\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$\sqrt{41}\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$2\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$6\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Apótema da base $m = l/2 = 4\text{ cm}$. 2. $g^2 = h^2 + m^2 \implies 5^2 = h^2 + 4^2 \implies h^2 = 25 - 16 = 9 \implies h = 3\text{ cm}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique $g^2 = h^2 + m^2$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O volume de um cone circular reto de raio $6\text{ cm}$ e altura $8\text{ cm}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$96\pi\text{ cm}^3$", "correta": True},
            {"letra": "B", "texto": r"$288\pi\text{ cm}^3$", "correta": False},
            {"letra": "C", "texto": r"$48\pi\text{ cm}^3$", "correta": False},
            {"letra": "D", "texto": r"$144\pi\text{ cm}^3$", "correta": False},
            {"letra": "E", "texto": r"$72\pi\text{ cm}^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $V = \frac{1}{3}\pi R^2 h = \frac{1}{3}\pi (36)(8) = 12 \times 8 \pi = 96\pi\text{ cm}^3$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Fórmula do volume do cone: $\frac{1}{3}\pi R^2 h$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o volume de um tetraedro regular de aresta $6$ dividido por $\sqrt{2}$?",
        "alternativas": [],
        "resposta_correta": "18",
        "resolucao_passo_a_passo": r"1. $V = \frac{a^3\sqrt{2}}{12} = \frac{216\sqrt{2}}{12} = 18\sqrt{2}$. Dividido por $\sqrt{2}$ dá 18.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Use a fórmula do tetraedro regular: $V = \frac{a^3\sqrt{2}}{12}$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A área lateral de um cone equilátero cujo raio da base mede $4\text{ cm}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$32\pi\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$16\pi\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$64\pi\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$48\pi\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$24\pi\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cone equilátero: $g = 2R = 8\text{ cm}$. 2. $A_L = \pi R g = \pi (4)(8) = 32\pi\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Em cone equilátero a geratriz é o dobro do raio."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seccionando-se uma pirâmide por um plano paralelo à base a meia altura ($h/2$), a razão entre o volume da pirâmide menor e da pirâmide original é:",
        "alternativas": [
            {"letra": "A", "texto": r"$1/8$", "correta": True},
            {"letra": "B", "texto": r"$1/4$", "correta": False},
            {"letra": "C", "texto": r"$1/2$", "correta": False},
            {"letra": "D", "texto": r"$1/16$", "correta": False},
            {"letra": "E", "texto": r"$1/3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Razão linear $k = 1/2$. Razão de volumes $= k^3 = (1/2)^3 = 1/8$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A razão volumétrica de sólidos semelhantes é $k^3$."},
    },

    # --- Cap 6: A Esfera e Suas Partes (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O volume de uma esfera de raio $3\text{ cm}$, em função de $\pi$, é:",
        "alternativas": [
            {"letra": "A", "texto": r"$36\pi\text{ cm}^3$", "correta": True},
            {"letra": "B", "texto": r"$12\pi\text{ cm}^3$", "correta": False},
            {"letra": "C", "texto": r"$27\pi\text{ cm}^3$", "correta": False},
            {"letra": "D", "texto": r"$108\pi\text{ cm}^3$", "correta": False},
            {"letra": "E", "texto": r"$9\pi\text{ cm}^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $V = \frac{4}{3}\pi R^3 = \frac{4}{3}\pi (27) = 36\pi\text{ cm}^3$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Volume da esfera: $\frac{4}{3}\pi R^3$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A área da superfície de uma esfera mede $144\pi\text{ cm}^2$. O raio dessa esfera vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$6\text{ cm}$", "correta": True},
            {"letra": "B", "texto": r"$12\text{ cm}$", "correta": False},
            {"letra": "C", "texto": r"$36\text{ cm}$", "correta": False},
            {"letra": "D", "texto": r"$3\text{ cm}$", "correta": False},
            {"letra": "E", "texto": r"$8\text{ cm}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $4\pi R^2 = 144\pi \implies R^2 = 36 \implies R = 6\text{ cm}$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Isole $R$ em $4\pi R^2 = 144\pi$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Uma esfera de raio $13\text{ cm}$ é cortada por um plano distante $5\text{ cm}$ do centro. Qual é o raio da seção plana circular resultante?",
        "alternativas": [],
        "resposta_correta": "12",
        "resolucao_passo_a_passo": r"1. $r = \sqrt{R^2 - d^2} = \sqrt{13^2 - 5^2} = \sqrt{169 - 25} = \sqrt{144} = 12\text{ cm}$.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Use a relação $R^2 = d^2 + r^2$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O volume de um hemisfério (semiesfera) de raio $6\text{ cm}$ em função de $\pi$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$144\pi\text{ cm}^3$", "correta": True},
            {"letra": "B", "texto": r"$288\pi\text{ cm}^3$", "correta": False},
            {"letra": "C", "texto": r"$72\pi\text{ cm}^3$", "correta": False},
            {"letra": "D", "texto": r"$216\pi\text{ cm}^3$", "correta": False},
            {"letra": "E", "texto": r"$96\pi\text{ cm}^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $V = \frac{1}{2} \cdot \frac{4}{3}\pi R^3 = \frac{2}{3}\pi (216) = 144\pi\text{ cm}^3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Metade do volume da esfera."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A razão entre o volume de uma esfera de raio $R$ e o volume do cilindro equilátero circunscrito a ela é:",
        "alternativas": [
            {"letra": "A", "texto": r"$2/3$", "correta": True},
            {"letra": "B", "texto": r"$1/2$", "correta": False},
            {"letra": "C", "texto": r"$3/4$", "correta": False},
            {"letra": "D", "texto": r"$4/5$", "correta": False},
            {"letra": "E", "texto": r"$1/3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cilindro equilátero circunscrito: raio $R$ e altura $h = 2R \implies V_{\text{cil}} = \pi R^2(2R) = 2\pi R^3$. 2. $V_{\text{esf}} = \frac{4}{3}\pi R^3$. 3. Razão $= \frac{4/3}{2} = \frac{2}{3}$ (famoso teorema de Arquimedes). Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Divida $\frac{4}{3}\pi R^3$ por $2\pi R^3$."},
    },
]
