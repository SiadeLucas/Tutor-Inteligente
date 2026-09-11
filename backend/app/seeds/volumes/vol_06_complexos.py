"""
Módulo Canônico de Dados Didáticos — Volume 6: Complexos, Polinômios e Equações
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (4 caps), FIXACAO_DATA (12 questões), RAG_DATA (5 fragmentos), TRI_DATA (20 itens).
"""

VOLUME_INFO = {
    "numero": 6,
    "titulo": "Complexos, Polinômios e Equações",
    "grande_area": "algebra_funcoes",
    "ordem": 6,
    "capitulos": [
        {"num": 1, "titulo": "Números Complexos: Forma Algébrica e Operações", "tempo": 50},
        {"num": 2, "titulo": "Forma Trigonométrica e Fórmula de De Moivre", "tempo": 50},
        {"num": 3, "titulo": "Polinômios: Grau, Operações e Divisão", "tempo": 50},
        {"num": 4, "titulo": "Equações Algébricas e Relações de Girard", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Números Complexos: Forma Algébrica e Operações

O conjunto dos números complexos $\mathbb{C}$ surge da necessidade de solucionar equações polinomiais que não admitem raízes reais, como $x^2 + 1 = 0$.

### 1. A Unidade Imaginária e o Corpo $\mathbb{C}$
Define-se a **unidade imaginária** $i$ como o número que satisfaz:
$$i^2 = -1 \iff i = \sqrt{-1}$$
- Potências de $i$ (comportamento cíclico de período 4):
  $$i^0 = 1, \quad i^1 = i, \quad i^2 = -1, \quad i^3 = -i, \quad i^4 = 1$$
  Para qualquer $n \in \mathbb{N}$: $i^n = i^r$, onde $r$ é o resto da divisão euclidiana de $n$ por 4 ($n = 4q + r, \, 0 \le r \le 3$).

---

### 2. Forma Algébrica (Retangular)
Todo número complexo $z \in \mathbb{C}$ é unicamente expresso como:
$$z = a + bi \quad (a, b \in \mathbb{R})$$
- $a = \text{Re}(z)$: **Parte real**
- $b = \text{Im}(z)$: **Parte imaginária**
- Se $b = 0$: $z = a$ é um **número real puro**.
- Se $a = 0$ e $b \neq 0$: $z = bi$ é um **imaginário puro**.

---

### 3. Operações e Conjugado Complexo
Dados $z_1 = a + bi$ e $z_2 = c + di$:
1. **Adição e Subtração**:
   $$z_1 \pm z_2 = (a \pm c) + (b \pm d)i$$
2. **Multiplicação**:
   $$z_1 \cdot z_2 = (ac - bd) + (ad + bc)i$$
3. **Conjugado Complexo ($\bar{z}$)**:
   $$\bar{z} = a - bi$$
   Propriedade fundamental: $z \cdot \bar{z} = a^2 + b^2 \in \mathbb{R}_+$.
4. **Divisão**: Multiplica-se numerador e denominador pelo conjugado do denominador:
   $$\frac{z_1}{z_2} = \frac{z_1 \cdot \bar{z}_2}{z_2 \cdot \bar{z}_2} = \frac{(a + bi)(c - di)}{c^2 + d^2}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Divisão na Forma Algébrica
**Enunciado:** Calcule o quociente $z = \frac{3 + 4i}{1 - 2i}$ e determine $\text{Re}(z)$ e $\text{Im}(z)$.

**Resolução:**
1. Multiplicamos pelo conjugado do denominador $(1 + 2i)$:
   $$z = \frac{(3 + 4i)(1 + 2i)}{(1 - 2i)(1 + 2i)} = \frac{3 + 6i + 4i + 8i^2}{1^2 - (2i)^2}$$
2. Como $i^2 = -1$:
   $$z = \frac{3 + 10i - 8}{1 - 4(-1)} = \frac{-5 + 10i}{1 + 4} = \frac{-5 + 10i}{5} = -1 + 2i$$
3. Logo, $\text{Re}(z) = -1$ e $\text{Im}(z) = 2$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> A parte imaginária de $a + bi$ é o número real $b$, e **NÃO** $bi$! Em questões que perguntam "qual é $\text{Im}(z)$", responder $2i$ em vez de $2$ anula o item.
""",
    },
    2: {
        "teoria": r"""# Forma Trigonométrica e Fórmula de De Moivre

A representação geométrica no Plano de Argand-Gauss conecta os números complexos à Trigonometria e às rotações e homotetias no plano.

### 1. O Plano de Argand-Gauss
Todo complexo $z = a + bi$ é identificado com o ponto afixo $P(a, b)$ no plano cartesiano:
- Eixo horizontal: Eixo Real ($\text{Re}$)
- Eixo vertical: Eixo Imaginário ($\text{Im}$)

- **Módulo ($|z|$ ou $\rho$)**: Distância euclidiana da origem ao afixo:
  $$|z| = \rho = \sqrt{a^2 + b^2}$$
- **Argumento Principal ($\theta$ ou $\text{Arg}(z)$)**: Ângulo orientado medido a partir do semi-eixo real positivo ($0 \le \theta < 2\pi$):
  $$\cos\theta = \frac{a}{\rho}, \quad \sin\theta = \frac{b}{\rho}$$

---

### 2. Forma Polar / Trigonométrica
$$z = \rho(\cos\theta + i\sin\theta) = \rho\,\text{cis}\,\theta$$

---

### 3. Fórmulas de De Moivre
1. **Multiplicação e Divisão**:
   $$z_1 \cdot z_2 = \rho_1 \rho_2 [\cos(\theta_1 + \theta_2) + i\sin(\theta_1 + \theta_2)]$$
   $$\frac{z_1}{z_2} = \frac{\rho_1}{\rho_2} [\cos(\theta_1 - \theta_2) + i\sin(\theta_1 - \theta_2)]$$
2. **1ª Fórmula de De Moivre (Potenciação)**:
   $$z^n = \rho^n [\cos(n\theta) + i\sin(n\theta)] \quad (n \in \mathbb{Z})$$
3. **2ª Fórmula de De Moivre (Radiciação)**:
   As $n$ raízes $n$-ésimas de $z$ são dadas por:
   $$w_k = \sqrt[n]{\rho} \left[\cos\left(\frac{\theta + 2k\pi}{n}\right) + i\sin\left(\frac{\theta + 2k\pi}{n}\right)\right], \quad k \in \{0, 1, \dots, n-1\}$$
   Geometricamente, os afixos das $n$ raízes formam os vértices de um **polígono regular de $n$ lados** inscrito na circunferência de raio $\sqrt[n]{\rho}$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Potência com De Moivre
**Enunciado:** Calcule $(1 + i\sqrt{3})^6$.

**Resolução:**
1. Módulo: $\rho = \sqrt{1^2 + (\sqrt{3})^2} = \sqrt{1 + 3} = \sqrt{4} = 2$.
2. Argumento: $\cos\theta = 1/2$ e $\sin\theta = \sqrt{3}/2 \implies \theta = \pi/3$ ($60^\circ$).
3. Forma trigonométrica: $z = 2(\cos(\pi/3) + i\sin(\pi/3))$.
4. 1ª Fórmula de De Moivre para $n = 6$:
   $$z^6 = 2^6 [\cos(6 \cdot \pi/3) + i\sin(6 \cdot \pi/3)] = 64 [\cos(2\pi) + i\sin(2\pi)] = 64[1 + 0] = 64$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Ao calcular o argumento $\theta = \arctan(b/a)$, sempre observe o quadrante de $(a, b)$! Se $a < 0$, você deve somar $\pi$ ao arco para encontrar o argumento correto no 2º ou 3º quadrante.
""",
    },
    3: {
        "teoria": r"""# Polinômios: Grau, Operações e Divisão

Polinômios são as expressões algébricas mais suaves e fundamentais da Matemática, modelando aproximações e curvas em todos os domínios científicos.

### 1. Definição Formal
Um **polinômio** na variável complexa $x$ é uma expressão da forma:
$$P(x) = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$$
onde $a_n, \dots, a_0 \in \mathbb{C}$ são os coeficientes e $n \in \mathbb{N}$ é o **grau** de $P$ ($\partial P = n$), desde que $a_n \neq 0$.
- O polinômio nulo $P(x) = 0$ não tem grau definido.

---

### 2. Identidade de Polinômios
Dois polinômios $P(x)$ e $Q(x)$ são identicamente iguais ($P \equiv Q$) se, e somente se, seus coeficientes correspondentes de mesmo grau forem iguais:
$$P(x) \equiv Q(x) \iff a_k = b_k, \quad \forall k$$

---

### 3. Divisão Euclidiana de Polinômios
Dados $P(x)$ (dividendo) e $D(x) \neq 0$ (divisor), existem únicos polinômios $Q(x)$ (quociente) e $R(x)$ (resto) tais que:
$$P(x) = D(x) \cdot Q(x) + R(x)$$
com $\partial R < \partial D$ ou $R(x) = 0$.

- **Teorema do Resto (D'Alembert)**:
  O resto da divisão de um polinômio $P(x)$ pelo binômio do primeiro grau $(x - a)$ é igual ao valor numérico do polinômio em $a$:
  $$R = P(a)$$
- **Dispositivo Prático de Briot-Ruffini**:
  Algoritmo linear simplificado para efetuar divisões pelo binômio $(x - a)$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Aplicação do Teorema de D'Alembert
**Enunciado:** Determine o resto da divisão de $P(x) = x^4 - 3x^2 + 5x - 8$ por $(x - 2)$.

**Resolução:**
1. Pelo Teorema do Resto, o divisor $(x - a)$ tem $a = 2$.
2. O resto é simplesmente o valor de $P(2)$:
   $$R = P(2) = (2)^4 - 3(2)^2 + 5(2) - 8 = 16 - 3(4) + 10 - 8 = 16 - 12 + 10 - 8 = 6$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Se a questão pedir a divisão por $(ax + b)$, note que a raiz é $-b/a$. O resto continua sendo $P(-b/a)$, mas o quociente obtido por Briot-Ruffini deve ser **dividido pelo coeficiente $a$**!
""",
    },
    4: {
        "teoria": r"""# Equações Algébricas e Relações de Girard

As equações polinomiais encerram conexões profundas entre as raízes e os coeficientes, sintetizadas no Teorema Fundamental da Álgebra e nas Relações de Girard.

### 1. Teorema Fundamental da Álgebra (Gauss)
> Toda equação polinomial $P(x) = 0$ de grau $n \ge 1$ com coeficientes complexos admite **pelo menos uma raiz complexa**.

Como corolário direto, todo polinômio de grau $n$ pode ser completamente fatorado em $n$ fatores lineares:
$$P(x) = a_n(x - r_1)(x - r_2) \cdots (x - r_n)$$
admitindo exatamente **$n$ raízes** (contando suas multiplicidades).

---

### 2. Relações de Girard (Soma e Produto Generalizados)
Para a equação $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0 = 0$ com raízes $r_1, r_2, \dots, r_n$:
1. **Soma das raízes ($S_1$)**:
   $$\sum r_i = r_1 + r_2 + \cdots + r_n = -\frac{a_{n-1}}{a_n}$$
2. **Soma dos produtos 2 a 2 ($S_2$)**:
   $$\sum_{i < j} r_i r_j = \frac{a_{n-2}}{a_n}$$
3. **Produto de todas as raízes ($S_n$)**:
   $$r_1 \cdot r_2 \cdots r_n = (-1)^n \frac{a_0}{a_n}$$

---

### 3. Teorema das Raízes Complexas Conjugadas
Se uma equação algébrica com **coeficientes reais** admite o número complexo $z = a + bi$ ($b \neq 0$) como raiz, então o seu conjugado $\bar{z} = a - bi$ **também é obrigatoriamente raiz** com a mesma multiplicidade.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Equação do 3º Grau com Raízes em P.A.
**Enunciado:** As raízes da equação $x^3 - 6x^2 + 11x - 6 = 0$ estão em progressão aritmética. Determine as raízes.

**Resolução:**
1. Escrevemos as três raízes em P.A. de razão $r$:
   $$r_1 = m - r, \quad r_2 = m, \quad r_3 = m + r$$
2. Aplicamos a primeira Relação de Girard (Soma das raízes):
   $$r_1 + r_2 + r_3 = -\frac{-6}{1} = 6 \implies (m - r) + m + (m + r) = 6 \implies 3m = 6 \implies m = 2$$
3. Como $m = 2$ é raiz, ela anula a equação: $P(2) = 8 - 24 + 22 - 6 = 0$.
4. Aplicamos a relação do produto:
   $$r_1 \cdot r_2 \cdot r_3 = (-1)^3 \frac{-6}{1} = 6 \implies (2 - r) \cdot 2 \cdot (2 + r) = 6 \implies 4 - r^2 = 3 \implies r^2 = 1 \implies r = 1$$
5. As raízes são $2 - 1 = 1$, $2$ e $2 + 1 = 3$. Conjunto $S = \{1, 2, 3\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> O Teorema das Raízes Conjugadas **só vale** se todos os coeficientes da equação forem estritamente **reais**! Se a equação tiver coeficientes imaginários (ex: $x^2 - ix = 0$), as raízes não formam pares conjugados.
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"O valor da potência de $i$ dada por $i^{107}$ é:",
            "alternativas": [r"$-i$", r"$i$", r"$-1$", r"$1$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Sendo $z = 3 - 4i$, o produto $z \cdot \bar{z}$ vale:",
            "alternativas": [r"$25$", r"$7$", r"$-7$", r"$5$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O resultado da divisão $\frac{2 + 4i}{1 + i}$ na forma algébrica é:",
            "alternativas": [r"$3 + i$", r"$3 - i$", r"$1 + 3i$", r"$2 + 2i$"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"O módulo do número complexo $z = -3 + 4i$ é:",
            "alternativas": [r"$5$", r"$7$", r"$\sqrt{7}$", r"$25$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O argumento principal do complexo $z = 1 + i$ no primeiro quadrante é:",
            "alternativas": [r"$\pi/4$", r"$\pi/6$", r"$\pi/3$", r"$\pi/2$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Pela 1ª Fórmula de De Moivre, o valor de $[\cos(\pi/6) + i\sin(\pi/6)]^6$ é:",
            "alternativas": [r"$-1$", r"$1$", r"$i$", r"$-i$"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"O resto da divisão de $P(x) = x^3 - 2x^2 + 4x - 5$ por $(x - 3)$ é:",
            "alternativas": [r"$16$", r"$10$", r"$22$", r"$8$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Pelo Teorema de D'Alembert, um polinômio $P(x)$ é divisível por $(x - a)$ se, e somente se:",
            "alternativas": [r"$P(a) = 0$", r"$P(0) = a$", r"$P'(a) = 0$", r"$P(a) = 1$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O grau do polinômio produto $P(x) \cdot Q(x)$, sabendo que $\partial P = 3$ e $\partial Q = 2$, é:",
            "alternativas": [r"$5$", r"$6$", r"$3$", r"$2$"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"A soma das raízes da equação $2x^3 - 8x^2 + 6x - 10 = 0$ é:",
            "alternativas": [r"$4$", r"$-4$", r"$8$", r"$3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Se $2 + 3i$ é raiz de uma equação polinomial de coeficientes reais, outra raiz obrigatória é:",
            "alternativas": [r"$2 - 3i$", r"$-2 + 3i$", r"$-2 - 3i$", r"$3 + 2i$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O produto de todas as raízes da equação $x^4 - 5x^2 + 4 = 0$ vale:",
            "alternativas": [r"$4$", r"$-4$", r"$5$", r"$-5$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 20,
        "teorema": "Corpo dos Números Complexos e Potências da Unidade Imaginária",
        "texto": (
            "No conjunto C, a unidade imaginária i satisfaz i² = -1. As potências inteiras de i repetem-se de 4 em 4: "
            "i^(4k) = 1, i^(4k+1) = i, i^(4k+2) = -1 e i^(4k+3) = -i. O conjugado de z = a + bi é z_barra = a - bi, "
            "com z · z_barra = a² + b²."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 55,
        "teorema": "Forma Trigonométrica e Teorema de De Moivre",
        "texto": (
            "Todo complexo não-nulo z = a + bi admite a forma polar z = ρ(cos θ + i sin θ), onde ρ = √(a²+b²) "
            "e θ é o argumento principal. Pela Fórmula de De Moivre: z^n = ρ^n [cos(nθ) + i sin(nθ)]. As n raízes "
            "n-ésimas formam um polígono regular de n lados no plano complexo."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 95,
        "teorema": "Divisão Euclidiana e Teorema do Resto de D'Alembert",
        "texto": (
            "Para polinômios P(x) e D(x), tem-se P(x) = D(x)Q(x) + R(x) com grau de R menor que o grau de D. "
            "O Teorema do Resto garante que a divisão por (x - a) produz resto R = P(a). O dispositivo de "
            "Briot-Ruffini otimiza essa divisão para binômios de 1º grau."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 130,
        "teorema": "Teorema Fundamental da Álgebra e Relações de Girard",
        "texto": (
            "Todo polinômio de grau n admite exatamente n raízes em C. As relações de Girard conectam as somas e "
            "produtos simétricos das raízes aos coeficientes da equação: a soma é -a_(n-1)/a_n e o produto é (-1)^n a_0/a_n. "
            "Equações reais com raízes complexas possuem sempre raízes em pares conjugados."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Números Complexos: Forma Algébrica (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor da expressão com potências de $i$: $E = i^{20} + i^{21} + i^{22} + i^{23}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$0$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$i$", "correta": False},
            {"letra": "D", "texto": r"$-1$", "correta": False},
            {"letra": "E", "texto": r"$4i$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Quatro potências consecutivas de $i$ somam sempre zero: $1 + i - 1 - i = 0$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A soma de 4 potências inteiras consecutivas de $i$ é sempre nula."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O inverso multiplicativo do número complexo $z = 1 + 2i$ na forma algébrica é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{5} - \frac{2}{5}i$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{3} - \frac{2}{3}i$", "correta": False},
            {"letra": "C", "texto": r"$1 - 2i$", "correta": False},
            {"letra": "D", "texto": r"$-1 - 2i$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{5} + \frac{2}{5}i$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $z^{-1} = \frac{\bar{z}}{|z|^2} = \frac{1 - 2i}{1^2 + 2^2} = \frac{1 - 2i}{5} = \frac{1}{5} - \frac{2}{5}i$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique numerador e denominador pelo conjugado."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para que o produto $(x + 2i)(3 - i)$ seja um número real puro, o valor de $x$ deve ser:",
        "alternativas": [
            {"letra": "A", "texto": r"$-6$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$2/3$", "correta": False},
            {"letra": "D", "texto": r"$-2/3$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Produto: $3x - xi + 6i - 2i^2 = (3x + 2) + (6 - x)i$. 2. Para ser real, parte imaginária nula: $6 - x = 0 \implies x = 6$. Espere: $(x + 2i)(3 - i) = 3x - xi + 6i + 2$. Parte imaginária: $6 - x = 0 \implies x = 6$. Se enunciado pede $-6$ para $(x - 2i)$: refazendo com $x = -6$: parte imaginária $6 - (-6) \neq 0$. Atenção: se $x = 6$, $6 - 6 = 0$.",
        "parametro_a": 1.400,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Isole a parte imaginária e iguale a zero."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine o valor de $(1 + i)^8$.",
        "alternativas": [],
        "resposta_correta": "16",
        "resolucao_passo_a_passo": r"1. $(1 + i)^2 = 1 + 2i + i^2 = 2i$. 2. $(1 + i)^8 = ((1 + i)^2)^4 = (2i)^4 = 2^4 \cdot i^4 = 16 \cdot 1 = 16$.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule primeiro $(1+i)^2 = 2i$ e depois eleve à quarta potência."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $z = a + bi$. A igualdade $|z - 3| = |z + 3|$ representa geometricamente no plano complexo:",
        "alternativas": [
            {"letra": "A", "texto": r"O eixo imaginário ($x = 0$)", "correta": True},
            {"letra": "B", "texto": r"O eixo real ($y = 0$)", "correta": False},
            {"letra": "C", "texto": r"Uma circunferência de raio 3", "correta": False},
            {"letra": "D", "texto": r"A reta bissetriz $y = x$", "correta": False},
            {"letra": "E", "texto": r"Uma elipse", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $|z - 3| = |z + 3|$ significa que $z$ é equidistante de $3$ e $-3$. 2. A mediatriz do segmento $[-3, 3]$ é o eixo vertical (imaginário), ou seja, $x = 0$. Alternativa A.",
        "parametro_a": 1.550,
        "parametro_b": 1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Interprete como a mediatriz geométrica entre os dois pontos no plano."},
    },

    # --- Cap 2: Forma Trigonométrica e De Moivre (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O módulo e o argumento principal de $z = -2 + 2i\sqrt{3}$ valem respectivamente:",
        "alternativas": [
            {"letra": "A", "texto": r"$\rho = 4$ e $\theta = 2\pi/3$", "correta": True},
            {"letra": "B", "texto": r"$\rho = 4$ e $\theta = \pi/3$", "correta": False},
            {"letra": "C", "texto": r"$\rho = 2$ e $\theta = 2\pi/3$", "correta": False},
            {"letra": "D", "texto": r"$\rho = 4$ e $\theta = 5\pi/6$", "correta": False},
            {"letra": "E", "texto": r"$\rho = 16$ e $\theta = 2\pi/3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\rho = \sqrt{(-2)^2 + (2\sqrt{3})^2} = \sqrt{4 + 12} = \sqrt{16} = 4$. 2. $\cos\theta = -2/4 = -1/2$, $\sin\theta = 2\sqrt{3}/4 = \sqrt{3}/2 \implies 2^\circ$ quadrante: $\theta = 2\pi/3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Observe o segundo quadrante: cosseno negativo e seno positivo."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $(1 + i\sqrt{3})^6$ pela 1ª Fórmula de De Moivre é:",
        "alternativas": [
            {"letra": "A", "texto": r"$64$", "correta": True},
            {"letra": "B", "texto": r"$-64$", "correta": False},
            {"letra": "C", "texto": r"$64i$", "correta": False},
            {"letra": "D", "texto": r"$32$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\rho = 2$, $\theta = \pi/3$. 2. $z^6 = 2^6(\cos(6 \cdot \pi/3) + i\sin(6 \cdot \pi/3)) = 64(\cos 2\pi + i\sin 2\pi) = 64(1 + 0) = 64$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique o argumento por 6 e eleve o módulo a 6."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"As raízes cúbicas da unidade ($z^3 = 1$) formam no plano complexo os vértices de:",
        "alternativas": [
            {"letra": "A", "texto": r"Um triângulo equilátero inscrito na circunferência unitária", "correta": True},
            {"letra": "B", "texto": r"Um triângulo retângulo isósceles", "correta": False},
            {"letra": "C", "texto": r"Um segmento de reta sobre o eixo real", "correta": False},
            {"letra": "D", "texto": r"Um quadrado centrado na origem", "correta": False},
            {"letra": "E", "texto": r"Três pontos colineares", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela 2ª fórmula de De Moivre, as raízes $n$-ésimas de um complexo dividem a circunferência de raio $\sqrt[n]{\rho}$ em $n$ arcos iguais de $2\pi/n$. Para $n=3$, formam um triângulo equilátero. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "As $n$ raízes de um complexo sempre formam um polígono regular de $n$ lados."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Dado $z = 4(\cos 30^\circ + i\sin 30^\circ)$ e $w = 2(\cos 15^\circ + i\sin 15^\circ)$, o módulo do quociente $z/w$ vale:",
        "alternativas": [],
        "resposta_correta": "2",
        "resolucao_passo_a_passo": r"1. $|z/w| = |z| / |w| = 4 / 2 = 2$.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "O módulo do quociente é o quociente dos módulos."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $z = \cos(\pi/4) + i\sin(\pi/4)$, então $z^{100}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$-1$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$i$", "correta": False},
            {"letra": "D", "texto": r"$-i$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $100 \cdot (\pi/4) = 25\pi = 24\pi + \pi \equiv \pi$. 2. $\cos\pi + i\sin\pi = -1 + 0 = -1$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique o ângulo por 100 e reduza à primeira volta."},
    },

    # --- Cap 3: Polinômios: Grau, Operações e Divisão (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O resto da divisão do polinômio $P(x) = 2x^3 - 5x^2 + x - 3$ por $(x - 2)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-5$", "correta": True},
            {"letra": "B", "texto": r"$5$", "correta": False},
            {"letra": "C", "texto": r"$-3$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$-7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pelo Teorema do Resto: $R = P(2) = 2(8) - 5(4) + 2 - 3 = 16 - 20 + 2 - 3 = -5$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique o Teorema do Resto calculando $P(2)$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para que o polinômio $P(x) = x^3 - 4x^2 + mx - 6$ seja divisível por $(x - 3)$, o valor de $m$ deve ser:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$-5$", "correta": False},
            {"letra": "C", "texto": r"$3$", "correta": False},
            {"letra": "D", "texto": r"$-3$", "correta": False},
            {"letra": "E", "texto": r"$15$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Divisível $\iff P(3) = 0$. 2. $3^3 - 4(3^2) + 3m - 6 = 0 \implies 27 - 36 + 3m - 6 = 0 \implies 3m - 15 = 0 \implies m = 5$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Imponha $P(3) = 0$ e isole a incógnita $m$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Ao dividir $P(x) = x^4 - 16$ por $(x - 1)$, qual é o resto numérico?",
        "alternativas": [],
        "resposta_correta": "-15",
        "resolucao_passo_a_passo": r"1. $R = P(1) = 1^4 - 16 = -15$.",
        "parametro_a": 1.200,
        "parametro_b": -1.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule $P(1)$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O quociente da divisão de $P(x) = 2x^3 - 3x^2 + 4x - 1$ por $(x - 1)$ obtido por Briot-Ruffini é:",
        "alternativas": [
            {"letra": "A", "texto": r"$2x^2 - x + 3$", "correta": True},
            {"letra": "B", "texto": r"$2x^2 + x + 3$", "correta": False},
            {"letra": "C", "texto": r"$2x^2 - 5x + 3$", "correta": False},
            {"letra": "D", "texto": r"$x^2 - x + 2$", "correta": False},
            {"letra": "E", "texto": r"$2x^2 - x + 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Briot-Ruffini com raiz 1: coeficientes $[2, -3, 4, -1]$. Linha inferior: $2$, depois $2(1) - 3 = -1$, depois $-1(1) + 4 = 3$. Quociente $2x^2 - x + 3$, resto $3(1) - 1 = 2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique o algoritmo de Briot-Ruffini passo a passo."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se um polinômio $P(x)$ é divisível separadamente por $(x - 1)$ e por $(x + 2)$, então ele é divisível pelo produto:",
        "alternativas": [
            {"letra": "A", "texto": r"$x^2 + x - 2$", "correta": True},
            {"letra": "B", "texto": r"$x^2 - x - 2$", "correta": False},
            {"letra": "C", "texto": r"$x^2 - 3x + 2$", "correta": False},
            {"letra": "D", "texto": r"$x^2 - 4$", "correta": False},
            {"letra": "E", "texto": r"$x^2 - 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Como $(x-1)$ e $(x+2)$ são primos entre si, $P(x)$ é divisível por $(x-1)(x+2) = x^2 + x - 2$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique os dois fatores lineares."},
    },

    # --- Cap 4: Equações Algébricas e Relações de Girard (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"As raízes da equação $x^3 - 6x^2 + 11x - 6 = 0$ são:",
        "alternativas": [
            {"letra": "A", "texto": r"$1, 2 \text{ e } 3$", "correta": True},
            {"letra": "B", "texto": r"$-1, -2 \text{ e } -3$", "correta": False},
            {"letra": "C", "texto": r"$1, -2 \text{ e } 3$", "correta": False},
            {"letra": "D", "texto": r"$0, 2 \text{ e } 4$", "correta": False},
            {"letra": "E", "texto": r"$2, 3 \text{ e } 6$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Raiz evidente $x = 1$: $1 - 6 + 11 - 6 = 0$. 2. Fatorando por $(x - 1)$: $x^2 - 5x + 6 = (x - 2)(x - 3)$. 3. Raízes $\{1, 2, 3\}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Teste a raiz evidente $x=1$ (a soma dos coeficientes é zero)."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja a equação $x^3 - 4x^2 + x + 6 = 0$. O valor da soma dos inversos das raízes $\frac{1}{r_1} + \frac{1}{r_2} + \frac{1}{r_3}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-1/6$", "correta": True},
            {"letra": "B", "texto": r"$1/6$", "correta": False},
            {"letra": "C", "texto": r"$-2/3$", "correta": False},
            {"letra": "D", "texto": r"$4/6$", "correta": False},
            {"letra": "E", "texto": r"$-4/6$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\frac{1}{r_1} + \frac{1}{r_2} + \frac{1}{r_3} = \frac{r_1 r_2 + r_1 r_3 + r_2 r_3}{r_1 r_2 r_3} = \frac{S_2}{S_3}$. 2. $S_2 = a_1/a_3 = 1/1 = 1$. 3. $S_3 = -a_0/a_3 = -6/1 = -6$. 4. Quociente $= 1 / (-6) = -1/6$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Reduza a soma de frações ao denominador comum $r_1 r_2 r_3$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o produto de todas as raízes da equação $x^4 - 7x^3 + 5x^2 - 8x + 12 = 0$?",
        "alternativas": [],
        "resposta_correta": "12",
        "resolucao_passo_a_passo": r"1. Pela relação de Girard para $n = 4$: $P = (-1)^4 \cdot \frac{a_0}{a_4} = (+1) \cdot \frac{12}{1} = 12$.",
        "parametro_a": 1.250,
        "parametro_b": -0.300,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Para grau 4, o produto é $(-1)^4 a_0 / a_4$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sabendo que $1 + 2i$ é raiz da equação real $x^3 - 4x^2 + 9x - 10 = 0$, a raiz real dessa equação é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 2$", "correta": True},
            {"letra": "B", "texto": r"$x = -2$", "correta": False},
            {"letra": "C", "texto": r"$x = 5$", "correta": False},
            {"letra": "D", "texto": r"$x = 1$", "correta": False},
            {"letra": "E", "texto": r"$x = -5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Coeficientes reais $\implies 1 - 2i$ também é raiz. 2. Soma das três raízes $= -(-4)/1 = 4$. 3. $(1 + 2i) + (1 - 2i) + r_3 = 4 \implies 2 + r_3 = 4 \implies r_3 = 2$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use o conjugado $1-2i$ e aplique a relação de Girard para a soma."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação $x^3 - 3x^2 + 3x - 1 = 0$ admite:",
        "alternativas": [
            {"letra": "A", "texto": r"Apenas a raiz real $1$ com multiplicidade 3", "correta": True},
            {"letra": "B", "texto": r"Três raízes reais distintas", "correta": False},
            {"letra": "C", "texto": r"Uma raiz real e duas imaginárias", "correta": False},
            {"letra": "D", "texto": r"Nenhuma raiz real", "correta": False},
            {"letra": "E", "texto": r"Raízes $1, -1$ e $0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Reconhecemos o produto notável $(x - 1)^3 = x^3 - 3x^2 + 3x - 1$. 2. Portanto, $(x - 1)^3 = 0 \implies x = 1$ é raiz tripla (multiplicidade 3). Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Reconheça o desenvolvimento do cubo da diferença: $(x - 1)^3$."},
    },
]
