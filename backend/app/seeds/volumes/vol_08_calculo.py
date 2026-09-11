"""
Módulo Canônico de Dados Didáticos — Volume 8: Limites, Derivadas e Noções de Integral
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
    "numero": 8,
    "titulo": "Limites, Derivadas e Noções de Integral",
    "grande_area": "algebra_funcoes",
    "ordem": 8,
    "capitulos": [
        {"num": 1, "titulo": "Conceito Intuitivo e Definição Formal de Limite", "tempo": 50},
        {"num": 2, "titulo": "Propriedades Operatórias e Limites Fundamentais", "tempo": 50},
        {"num": 3, "titulo": "Continuidade de Funções e Teoremas Centrais", "tempo": 50},
        {"num": 4, "titulo": "A Noção de Derivada e Regras de Derivação", "tempo": 50},
        {"num": 5, "titulo": "Estudo dos Máximos, Mínimos e Reta Tangente", "tempo": 50},
        {"num": 6, "titulo": "Noções Iniciais de Integral Indefinida", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Conceito Intuitivo e Definição Formal de Limite

O Cálculo Diferencial e Integral fundamenta-se na ideia de aproximação local contínua e no comportamento assintótico de funções.

### 1. Noção Intuitiva de Limite
Dizemos que o limite de $f(x)$ quando $x$ tende a $p$ é igual a $L$, e escrevemos:
$$\lim_{x \to p} f(x) = L$$
quando podemos tornar os valores de $f(x)$ arbitrariamente próximos de $L$, bastando tomar $x$ suficientemente próximo de $p$, com $x \neq p$.
> [!NOTE]
> O valor da função exatamente no ponto $x = p$, isto é $f(p)$, é irrelevante para a existência e o valor de $\lim_{x \to p} f(x)$.

---

### 2. Definição Formal $(\varepsilon, \delta)$ de Cauchy-Weierstrass
Diz-se que $\lim_{x \to p} f(x) = L$ se, e somente se:
$$\forall \varepsilon > 0, \quad \exists \delta > 0 \quad \text{tal que} \quad 0 < |x - p| < \delta \implies |f(x) - L| < \varepsilon$$

---

### 3. Limites Laterais e Teorema da Existência
O limite bilateral existe se, e somente se, ambos os limites laterais existirem e forem iguais:
$$\lim_{x \to p} f(x) = L \iff \lim_{x \to p^+} f(x) = \lim_{x \to p^-} f(x) = L$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Indeterminação do Tipo $\frac{0}{0}$
**Enunciado:** Calcule $\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$.

**Resolução:**
1. Fatoramos $x^2 - 9 = (x - 3)(x + 3)$.
2. Como $x \neq 3$, simplificamos:
   $$\lim_{x \to 3} (x + 3) = 3 + 3 = 6$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> $\frac{0}{0}$ é uma indeterminação matemática. Fatore ou racionalize antes de concluir o limite.
""",
    },
    2: {
        "teoria": r"""# Propriedades Operatórias e Limites Fundamentais

### 1. Limites Fundamentais
1. **Limite Trigonométrico Fundamental**:
   $$\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad (x \text{ em radianos})$$
2. **Limite Exponencial Fundamental**:
   $$\lim_{x \to +\infty} \left(1 + \frac{1}{x}\right)^x = e \approx 2{,}71828$$
   $$\lim_{x \to 0} \frac{e^x - 1}{x} = 1$$

---

### 2. Teorema do Confronto (Sanduíche)
Se $g(x) \le f(x) \le h(x)$ e $\lim g(x) = \lim h(x) = L$, então $\lim f(x) = L$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Limite Trigonométrico
**Enunciado:** Calcule $\lim_{x \to 0} \frac{\sin(5x)}{2x}$.

**Resolução:**
$$\lim_{x \to 0} \frac{5}{2} \cdot \frac{\sin(5x)}{5x} = \frac{5}{2} \cdot 1 = \frac{5}{2}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> O limite trigonométrico fundamental exige arcos em radianos.
""",
    },
    3: {
        "teoria": r"""# Continuidade de Funções e Teoremas Centrais

Uma função $f$ é contínua em $x = p$ se:
1. $p \in D(f)$
2. $\lim_{x \to p} f(x)$ existe
3. $\lim_{x \to p} f(x) = f(p)$

### Teorema de Bolzano (Valor Intermediário):
Se $f$ é contínua em $[a, b]$ e $f(a) \cdot f(b) < 0$, então existe $c \in ]a, b[$ tal que $f(c) = 0$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Existência de Raiz Real
**Enunciado:** Mostre que $P(x) = x^3 - 3x - 1$ tem raiz em $[1, 2]$.

**Resolução:**
$P(1) = -3 < 0$ e $P(2) = 1 > 0$. Por Bolzano, existe $c \in ]1, 2[$ com $P(c) = 0$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> A continuidade no intervalo fechado é hipótese necessária de Bolzano.
""",
    },
    4: {
        "teoria": r"""# A Noção de Derivada e Regras de Derivação

A derivada representa a taxa instantânea de variação:
$$f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}$$

### Regras Operatórias:
- Potência: $(x^n)' = n x^{n-1}$
- Produto: $(uv)' = u'v + uv'$
- Quociente: $(u/v)' = \frac{u'v - uv'}{v^2}$
- Cadeia: $[f(g(x))]' = f'(g(x)) \cdot g'(x)$
- Fundamentais: $(\sin x)' = \cos x$, $(\cos x)' = -\sin x$, $(e^x)' = e^x$, $(\ln x)' = 1/x$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Regra da Cadeia
**Enunciado:** Derive $f(x) = (3x^2 - 5x + 2)^4$.

**Resolução:**
$$f'(x) = 4(3x^2 - 5x + 2)^3 \cdot (6x - 5)$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Cuidado com o sinal na regra do quociente: o sinal de menos antecede $uv'$.
""",
    },
    5: {
        "teoria": r"""# Estudo dos Máximos, Mínimos e Reta Tangente

- **Reta Tangente**: $y - f(x_0) = f'(x_0)(x - x_0)$
- **Crescimento**: $f'(x) > 0 \implies$ crescente; $f'(x) < 0 \implies$ decrescente.
- **Pontos Críticos**: $f'(x) = 0$.
- **Teste da 2ª Derivada**: Se $f'(c) = 0$:
  - $f''(c) < 0 \implies$ máximo local
  - $f''(c) > 0 \implies$ mínimo local
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Reta Tangente
**Enunciado:** Reta tangente a $y = x^3 - 2x + 1$ em $x = 2$.

**Resolução:**
Ponto $(2, 5)$. $f'(x) = 3x^2 - 2 \implies m = f'(2) = 10$.
$y - 5 = 10(x - 2) \implies y = 10x - 15$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> $f'(x_0) = 0$ não garante máximo nem mínimo (pode ser inflexão, como $y = x^3$ em 0).
""",
    },
    6: {
        "teoria": r"""# Noções Iniciais de Integral Indefinida

A integral indefinida é a antiderivada geral:
$$\int f(x)\,dx = F(x) + C, \quad \text{onde } F'(x) = f(x)$$

### Integrais Imediatas:
- $\int x^n\,dx = \frac{x^{n+1}}{n+1} + C \quad (n \neq -1)$
- $\int \frac{1}{x}\,dx = \ln|x| + C$
- $\int e^x\,dx = e^x + C$
- $\int \cos x\,dx = \sin x + C$
- $\int \sin x\,dx = -\cos x + C$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Método da Substituição
**Enunciado:** Calcule $\int 2x \cos(x^2)\,dx$.

**Resolução:**
$u = x^2 \implies du = 2x\,dx$. $\int \cos u\,du = \sin u + C = \sin(x^2) + C$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Sempre adicione a constante de integração $+ C$ em integrais indefinidas.
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"O valor do limite $\lim_{x \to 2} \frac{x^2 - 4}{x - 2}$ é:",
            "alternativas": [r"$4$", r"$2$", r"$0$", r"Não existe"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O limite lateral à direita $\lim_{x \to 0^+} \frac{|x|}{x}$ vale:",
            "alternativas": [r"$1$", r"$-1$", r"$0$", r"Infinito"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Para que o limite bilateral $\lim_{x \to p} f(x)$ exista, é necessário e suficiente que:",
            "alternativas": [
                r"Os limites laterais existam e sejam iguais entre si",
                r"A função esteja definida no ponto $p$",
                r"A derivada exista no ponto $p$",
                r"A função seja estritamente crescente",
            ],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"O valor do limite trigonométrico fundamental $\lim_{x \to 0} \frac{\sin(3x)}{x}$ é:",
            "alternativas": [r"$3$", r"$1$", r"$1/3$", r"$0$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O limite fundamental $\lim_{x \to +\infty} (1 + 1/x)^x$ resulta no número:",
            "alternativas": [r"$e$", r"$1$", r"$0$", r"$+\infty$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O limite $\lim_{x \to 0} \frac{1 - \cos x}{x^2}$ é igual a:",
            "alternativas": [r"$1/2$", r"$1$", r"$0$", r"$2$"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"Uma função $f$ é dita contínua em $x = p$ quando:",
            "alternativas": [
                r"$\lim_{x \to p} f(x) = f(p)$",
                r"$f'(p) > 0$",
                r"$\lim_{x \to p} f(x) = 0$",
                r"$f(p) = 0$",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O Teorema de Bolzano garante a existência de pelo menos uma raiz de $f(x) = 0$ em $[a, b]$ se $f$ for contínua e:",
            "alternativas": [
                r"$f(a) \cdot f(b) < 0$",
                r"$f(a) \cdot f(b) > 0$",
                r"$f(a) = f(b)$",
                r"$f'(a) = 0$",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Qual das funções a seguir apresenta uma descontinuidade no ponto $x = 0$?",
            "alternativas": [r"$f(x) = \frac{1}{x}$", r"$f(x) = x^2$", r"$f(x) = \sin x$", r"$f(x) = e^x$"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"A derivada da função $f(x) = 5x^3 - 4x^2 + 7x - 1$ é:",
            "alternativas": [
                r"$15x^2 - 8x + 7$",
                r"$15x^2 - 8x$",
                r"$5x^2 - 4x + 7$",
                r"$15x^3 - 8x^2 + 7$",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A derivada de $f(x) = e^{3x}$ pela regra da cadeia é:",
            "alternativas": [r"$3e^{3x}$", r"$e^{3x}$", r"$3e^x$", r"$\frac{e^{3x}}{3}$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A derivada da função trigonométrica $f(x) = \sin x$ é igual a:",
            "alternativas": [r"$\cos x$", r"$-\cos x$", r"$\tan x$", r"$-\sin x$"],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"O coeficiente angular da reta tangente a $y = x^2$ no ponto $(3, 9)$ vale:",
            "alternativas": [r"$6$", r"$3$", r"$9$", r"$2$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Se $f'(c) = 0$ e $f''(c) > 0$, o ponto $c$ é classificado como:",
            "alternativas": [
                r"Ponto de mínimo local",
                r"Ponto de máximo local",
                r"Ponto de inflexão",
                r"Assíntota vertical",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O ponto crítico da função quadrática $f(x) = x^2 - 6x + 5$ ocorre em:",
            "alternativas": [r"$x = 3$", r"$x = 6$", r"$x = -3$", r"$x = 5$"],
            "indice_correto": 0,
        },
    ],
    6: [
        {
            "numero": 1,
            "enunciado": r"A integral indefinida imediata $\int (3x^2 + 4x)\,dx$ é igual a:",
            "alternativas": [
                r"$x^3 + 2x^2 + C$",
                r"$6x + 4 + C$",
                r"$3x^3 + 4x^2 + C$",
                r"$x^3 + 4x^2 + C$",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A integral de $\frac{1}{x}\,dx$ para $x > 0$ é dada por:",
            "alternativas": [r"$\ln x + C$", r"$-\frac{1}{x^2} + C$", r"$e^x + C$", r"$x + C$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A integral indefinida de $\cos x\,dx$ é igual a:",
            "alternativas": [r"$\sin x + C$", r"$-\sin x + C$", r"$\cos x + C$", r"$\sec x + C$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 25,
        "teorema": "Definição de Limite e Limites Laterais",
        "texto": (
            "O limite lim_(x->p) f(x) = L formaliza a aproximação local contínua. "
            "O limite bilateral existe se, e somente se, os limites laterais pela direita e pela esquerda "
            "forem ambos existentes e iguais."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 60,
        "teorema": "Limites Fundamentais",
        "texto": (
            "O limite trigonométrico fundamental estabelece que lim_(x->0) (sin x)/x = 1 (em radianos). "
            "O limite exponencial fundamental define a base neperiana: lim_(x->∞) (1 + 1/x)^x = e."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 90,
        "teorema": "Continuidade e Teorema de Bolzano",
        "texto": (
            "Uma função é contínua em p se lim_(x->p) f(x) = f(p). O Teorema de Bolzano garante "
            "que uma função contínua em [a, b] com f(a) · f(b) < 0 possui ao menos uma raiz real em ]a, b[."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 125,
        "teorema": "Derivadas e Regras Algébricas",
        "texto": (
            "A derivada f'(x) é a taxa instantânea de variação e a inclinação da reta tangente. "
            "As regras incluem produto (uv)' = u'v + uv', quociente (u/v)' = (u'v - uv')/v² e regra da cadeia."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 165,
        "teorema": "Extremos e Reta Tangente",
        "texto": (
            "Pontos críticos ocorrem onde f'(x) = 0. Se f''(c) < 0 o ponto é de máximo local; se f''(c) > 0 é de mínimo local. "
            "A reta tangente em x0 é y - f(x0) = f'(x0)(x - x0)."
        ),
    },
    {
        "numero_capitulo": 6,
        "pagina": 200,
        "teorema": "Integral Indefinida e Antiderivada",
        "texto": (
            "A integral indefinida ∫ f(x) dx = F(x) + C é a antiderivada geral de f(x). "
            "O método da substituição u = g(x) inverte a regra da cadeia na integração."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Conceito de Limite (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\lim_{x \to 4} \frac{\sqrt{x} - 2}{x - 4}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$1/4$", "correta": True},
            {"letra": "B", "texto": r"$1/2$", "correta": False},
            {"letra": "C", "texto": r"$1/8$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$4$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Multiplica-se por $(\sqrt{x}+2)$: $\frac{x-4}{(x-4)(\sqrt{x}+2)} = \frac{1}{\sqrt{x}+2}$. 2. Limite = $1/4$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Racionalize o numerador."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O limite $\lim_{x \to 2} \frac{x^3 - 8}{x - 2}$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$12$", "correta": True},
            {"letra": "B", "texto": r"$8$", "correta": False},
            {"letra": "C", "texto": r"$4$", "correta": False},
            {"letra": "D", "texto": r"$6$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x^3 - 8 = (x - 2)(x^2 + 2x + 4)$. 2. $\lim (x^2 + 2x + 4) = 4 + 4 + 4 = 12$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Fatore a diferença de cubos."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule o valor de $\lim_{x \to 1} \frac{x^2 + 3x - 4}{x - 1}$.",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": r"1. Fatorando: $(x - 1)(x + 4) / (x - 1) = x + 4$. 2. $1 + 4 = 5$.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Fatore o numerador simplificando $(x - 1)$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O limite $\lim_{x \to +\infty} \frac{4x^2 - 3x + 1}{2x^2 + 5}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$2$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$0$", "correta": False},
            {"letra": "D", "texto": r"$+\infty$", "correta": False},
            {"letra": "E", "texto": r"$1/2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Razão dos coeficientes de maior grau: $4/2 = 2$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Divida os coeficientes dos termos em $x^2$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O limite lateral $\lim_{x \to 3^-} \frac{1}{x - 3}$ resulta em:",
        "alternativas": [
            {"letra": "A", "texto": r"$-\infty$", "correta": True},
            {"letra": "B", "texto": r"$+\infty$", "correta": False},
            {"letra": "C", "texto": r"$0$", "correta": False},
            {"letra": "D", "texto": r"$-1$", "correta": False},
            {"letra": "E", "texto": r"$1/3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x \to 3^- \implies x - 3 < 0$. $1/(0^-) = -\infty$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Analise o sinal do denominador à esquerda de 3."},
    },

    # --- Cap 2: Propriedades e Limites Fundamentais (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\lim_{x \to 0} \frac{\sin(4x)}{\sin(2x)}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$2$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$1/2$", "correta": False},
            {"letra": "D", "texto": r"$4$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\frac{\sin(4x)/x}{\sin(2x)/x} \to \frac{4}{2} = 2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Divida por $x$ e use o limite fundamental do seno."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\lim_{x \to +\infty} \left(1 + \frac{2}{x}\right)^x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$e^2$", "correta": True},
            {"letra": "B", "texto": r"$e$", "correta": False},
            {"letra": "C", "texto": r"$2e$", "correta": False},
            {"letra": "D", "texto": r"$e^{1/2}$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela propriedade do número de Euler: $\lim (1 + k/x)^x = e^k = e^2$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use a propriedade $\lim (1 + k/x)^x = e^k$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O limite $\lim_{x \to 0} x^2 \sin(1/x)$ pelo Teorema do Confronto vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$0$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"Não existe", "correta": False},
            {"letra": "D", "texto": r"$-1$", "correta": False},
            {"letra": "E", "texto": r"$+\infty$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $-x^2 \le x^2\sin(1/x) \le x^2$. Como $\pm x^2 \to 0$, limite é $0$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Função limitada vezes termo que tende a zero dá zero."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule o valor do limite $\lim_{x \to 0} \frac{\tan(5x)}{x}$.",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": r"1. $\frac{\sin(5x)}{x} \cdot \frac{1}{\cos(5x)} \to 5 \cdot 1 = 5$.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Abra a tangente em seno sobre cosseno."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\lim_{x \to 0} \frac{e^{2x} - 1}{x}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$2$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$e$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$1/2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Multiplicando por 2: $2 \cdot \frac{e^{2x}-1}{2x} \to 2 \cdot 1 = 2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Ajuste o denominador para $2x$ multiplicando por 2."},
    },

    # --- Cap 3: Continuidade (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para qual valor de $k$ a função $f(x) = \begin{cases} x^2 + 1, & x \ge 2 \\ 2x + k, & x < 2 \end{cases}$ é contínua em $x = 2$?",
        "alternativas": [
            {"letra": "A", "texto": r"$k = 1$", "correta": True},
            {"letra": "B", "texto": r"$k = 2$", "correta": False},
            {"letra": "C", "texto": r"$k = 0$", "correta": False},
            {"letra": "D", "texto": r"$k = -1$", "correta": False},
            {"letra": "E", "texto": r"$k = 5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f(2) = 5$. 2. $4 + k = 5 \implies k = 1$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Iguale os limites laterais no ponto $x=2$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O Teorema de Weierstrass garante máximo e mínimo absolutos para funções contínuas em:",
        "alternativas": [
            {"letra": "A", "texto": r"Intervalos fechados e limitados $[a, b]$", "correta": True},
            {"letra": "B", "texto": r"Intervalos abertos $]a, b[$", "correta": False},
            {"letra": "C", "texto": r"Toda a reta real $\mathbb{R}$", "correta": False},
            {"letra": "D", "texto": r"Intervalos semiabertos $[a, b[$", "correta": False},
            {"letra": "E", "texto": r"Conjuntos discretos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A hipótese é continuidade em conjunto fechado e limitado (compacto). Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "O intervalo deve ser fechado e limitado."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A equação $x^3 + 2x - 5 = 0$ possui raiz real no intervalo:",
        "alternativas": [
            {"letra": "A", "texto": r"$]1, 2[$", "correta": True},
            {"letra": "B", "texto": r"$]0, 1[$", "correta": False},
            {"letra": "C", "texto": r"$]2, 3[$", "correta": False},
            {"letra": "D", "texto": r"$]-1, 0[$", "correta": False},
            {"letra": "E", "texto": r"$]-2, -1[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f(1) = -2 < 0$ e $f(2) = 7 > 0$. Por Bolzano, raiz em $]1, 2[$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Verifique a troca de sinal: $f(a) \cdot f(b) < 0$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $f(x) = \frac{x^2 - 1}{x - 1}$ para $x \neq 1$, para ser contínua em $x = 1$ deve-se definir $f(1) =$:",
        "alternativas": [
            {"letra": "A", "texto": r"$2$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$0$", "correta": False},
            {"letra": "D", "texto": r"$-1$", "correta": False},
            {"letra": "E", "texto": r"Não é possível", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\lim_{x \to 1} (x + 1) = 2$. Logo $f(1) = 2$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Defina $f(1)$ igual ao limite naquele ponto."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A função maior inteiro $\lfloor x \rfloor$ possui descontinuidade em:",
        "alternativas": [
            {"letra": "A", "texto": r"Todos os números inteiros", "correta": True},
            {"letra": "B", "texto": r"Apenas em $x = 0$", "correta": False},
            {"letra": "C", "texto": r"Todos os irracionais", "correta": False},
            {"letra": "D", "texto": r"Em nenhum ponto", "correta": False},
            {"letra": "E", "texto": r"Apenas nos negativos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Há saltos unitários em cada valor inteiro. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Nos inteiros os limites laterais diferem por 1."},
    },

    # --- Cap 4: Derivadas (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A derivada de $f(x) = x^2 \sin x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$2x\sin x + x^2\cos x$", "correta": True},
            {"letra": "B", "texto": r"$2x\cos x$", "correta": False},
            {"letra": "C", "texto": r"$x^2\cos x - 2x\sin x$", "correta": False},
            {"letra": "D", "texto": r"$2x\sin x$", "correta": False},
            {"letra": "E", "texto": r"$2x + \cos x$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $(uv)' = u'v + uv' = 2x\sin x + x^2\cos x$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Regra do produto: $(uv)' = u'v + uv'$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A derivada de $f(x) = \frac{x}{x + 1}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{(x + 1)^2}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{2x + 1}{(x + 1)^2}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{-1}{(x + 1)^2}$", "correta": False},
            {"letra": "D", "texto": r"$1$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{x + 1}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $(1(x+1) - x(1))/(x+1)^2 = 1/(x+1)^2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Regra do quociente."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Para $f(x) = 2x^3 - 5x + 4$, qual é o valor da derivada em $x = 2$?",
        "alternativas": [],
        "resposta_correta": "19",
        "resolucao_passo_a_passo": r"1. $f'(x) = 6x^2 - 5$. 2. $f'(2) = 6(4) - 5 = 19$.",
        "parametro_a": 1.250,
        "parametro_b": -0.800,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Derive e calcule $f'(2)$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A derivada de $f(x) = \ln(x^2 + 1)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{2x}{x^2 + 1}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{x^2 + 1}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{x}{x^2 + 1}$", "correta": False},
            {"letra": "D", "texto": r"$2x\ln(x^2 + 1)$", "correta": False},
            {"letra": "E", "texto": r"$\frac{2}{x}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $(\ln u)' = u'/u = \frac{2x}{x^2+1}$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use a regra da cadeia no logaritmo natural."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A segunda derivada de $f(x) = x^4 - 3x^2$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$12x^2 - 6$", "correta": True},
            {"letra": "B", "texto": r"$4x^3 - 6x$", "correta": False},
            {"letra": "C", "texto": r"$12x - 6$", "correta": False},
            {"letra": "D", "texto": r"$24x$", "correta": False},
            {"letra": "E", "texto": r"$12x^2 - 3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f'(x) = 4x^3 - 6x \implies f''(x) = 12x^2 - 6$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Derive duas vezes consecutivas."},
    },

    # --- Cap 5: Extremos e Reta Tangente (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A reta tangente a $f(x) = x^2 + 3x$ em $x_0 = 1$ tem equação:",
        "alternativas": [
            {"letra": "A", "texto": r"$y = 5x - 1$", "correta": True},
            {"letra": "B", "texto": r"$y = 5x + 4$", "correta": False},
            {"letra": "C", "texto": r"$y = 2x + 2$", "correta": False},
            {"letra": "D", "texto": r"$y = 5x + 1$", "correta": False},
            {"letra": "E", "texto": r"$y = x + 3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Ponto $(1, 4)$. $f'(x) = 2x + 3 \implies m = 5$. 2. $y - 4 = 5(x - 1) \implies y = 5x - 1$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use $y - y_0 = m(x - x_0)$ com $m = f'(x_0)$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Os pontos críticos de $f(x) = x^3 - 3x$ ocorrem em:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 1 \text{ e } x = -1$", "correta": True},
            {"letra": "B", "texto": r"$x = 0 \text{ e } x = 3$", "correta": False},
            {"letra": "C", "texto": r"$x = \sqrt{3}$", "correta": False},
            {"letra": "D", "texto": r"$x = 3 \text{ e } x = -3$", "correta": False},
            {"letra": "E", "texto": r"$x = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3x^2 - 3 = 0 \implies x^2 = 1 \implies x = \pm 1$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Iguale a primeira derivada a zero."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para $f(x) = x^3 - 3x$, o ponto $x = -1$ é classificado como:",
        "alternativas": [
            {"letra": "A", "texto": r"Ponto de máximo local", "correta": True},
            {"letra": "B", "texto": r"Ponto de mínimo local", "correta": False},
            {"letra": "C", "texto": r"Ponto de inflexão", "correta": False},
            {"letra": "D", "texto": r"Extremo global apenas", "correta": False},
            {"letra": "E", "texto": r"Descontinuidade", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f''(x) = 6x \implies f''(-1) = -6 < 0 \implies$ máximo local. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use o teste da 2ª derivada."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é o valor mínimo absoluto de $f(x) = x^2 - 4x + 7$ em $\mathbb{R}$?",
        "alternativas": [],
        "resposta_correta": "3",
        "resolucao_passo_a_passo": r"1. $2x - 4 = 0 \implies x = 2$. 2. $f(2) = 4 - 8 + 7 = 3$.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Encontre o ponto crítico e calcule a imagem."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A função $f(x) = 2x^3 - 6x$ é estritamente decrescente no intervalo:",
        "alternativas": [
            {"letra": "A", "texto": r"$]-1, 1[$", "correta": True},
            {"letra": "B", "texto": r"$]1, +\infty[$", "correta": False},
            {"letra": "C", "texto": r"$]-\infty, -1[$", "correta": False},
            {"letra": "D", "texto": r"$[0, 2]$", "correta": False},
            {"letra": "E", "texto": r"$\mathbb{R}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $6x^2 - 6 < 0 \implies x^2 < 1 \implies -1 < x < 1$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Encontre onde a derivada é negativa."},
    },

    # --- Cap 6: Integrais Indefinidas (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A integral $\int (6x^2 - 4x + 5)\,dx$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$2x^3 - 2x^2 + 5x + C$", "correta": True},
            {"letra": "B", "texto": r"$6x^3 - 4x^2 + 5x + C$", "correta": False},
            {"letra": "C", "texto": r"$2x^3 - 4x^2 + 5 + C$", "correta": False},
            {"letra": "D", "texto": r"$3x^3 - 2x^2 + 5x + C$", "correta": False},
            {"letra": "E", "texto": r"$12x - 4 + C$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Integrando termo a termo: $2x^3 - 2x^2 + 5x + C$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique a regra da potência."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A integral $\int 2x(x^2 + 1)^4\,dx$ resulta em:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{(x^2 + 1)^5}{5} + C$", "correta": True},
            {"letra": "B", "texto": r"$(x^2 + 1)^5 + C$", "correta": False},
            {"letra": "C", "texto": r"$\frac{2(x^2 + 1)^5}{5} + C$", "correta": False},
            {"letra": "D", "texto": r"$\frac{(x^2 + 1)^4}{4} + C$", "correta": False},
            {"letra": "E", "texto": r"$\frac{x^2(x^2 + 1)^5}{5} + C$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $u = x^2 + 1 \implies du = 2x\,dx$. $\int u^4\,du = \frac{(x^2+1)^5}{5} + C$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Substituição $u = x^2 + 1$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A primitiva de $f(x) = 3x^2$ com $F(1) = 5$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$F(x) = x^3 + 4$", "correta": True},
            {"letra": "B", "texto": r"$F(x) = x^3 + 5$", "correta": False},
            {"letra": "C", "texto": r"$F(x) = x^3 - 4$", "correta": False},
            {"letra": "D", "texto": r"$F(x) = 3x^3 + 2$", "correta": False},
            {"letra": "E", "texto": r"$F(x) = x^3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $F(x) = x^3 + C$. $F(1) = 1 + C = 5 \implies C = 4$. $F(x) = x^3 + 4$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use a condição $F(1) = 5$ para achar $C$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual o coeficiente de $e^{2x}$ na integral $\int 6e^{2x}\,dx$?",
        "alternativas": [],
        "resposta_correta": "3",
        "resolucao_passo_a_passo": r"1. $\int 6e^{2x}\,dx = 6 \cdot \frac{e^{2x}}{2} = 3e^{2x}$. Coeficiente é 3.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Divida 6 por 2."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A integral $\int \frac{1}{2x + 1}\,dx$ para $2x + 1 > 0$ resulta em:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{2}\ln(2x + 1) + C$", "correta": True},
            {"letra": "B", "texto": r"$\ln(2x + 1) + C$", "correta": False},
            {"letra": "C", "texto": r"$2\ln(2x + 1) + C$", "correta": False},
            {"letra": "D", "texto": r"$\frac{1}{(2x + 1)^2} + C$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{2(2x + 1)} + C$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $u = 2x + 1 \implies du = 2\,dx \implies \frac{1}{2}\ln(2x + 1) + C$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Lembre-se do fator $1/2$ ao substituir $dx$."},
    },
]
