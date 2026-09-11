"""
Módulo Canônico de Dados Didáticos — Volume 3: Trigonometria
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (5 caps), FIXACAO_DATA (15 questões), RAG_DATA (5 fragmentos), TRI_DATA (25 itens).
"""

VOLUME_INFO = {
    "numero": 3,
    "titulo": "Trigonometria",
    "grande_area": "geometria",
    "ordem": 3,
    "capitulos": [
        {"num": 1, "titulo": "Razões Trigonométricas no Triângulo Retângulo", "tempo": 50},
        {"num": 2, "titulo": "Arcos e o Ciclo Trigonométrico", "tempo": 50},
        {"num": 3, "titulo": "Funções Circulares (Seno, Cosseno, Tangente)", "tempo": 50},
        {"num": 4, "titulo": "Transformações e Fórmulas de Adição de Arcos", "tempo": 50},
        {"num": 5, "titulo": "Equações e Inequações Trigonométricas", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Razões Trigonométricas no Triângulo Retângulo

A trigonometria fundamenta-se nas proporções geométricas invariantes entre os lados de um triângulo retângulo em relação aos seus ângulos agudos.

### 1. Definições Fundamentais
Dado um triângulo retângulo com hipotenusa $a$, catetos $b$ (oposto a $\theta$) e $c$ (adjacente a $\theta$):
- **Seno**: $\sin\theta = \frac{\text{cateto oposto}}{\text{hipotenusa}} = \frac{b}{a}$
- **Cosseno**: $\cos\theta = \frac{\text{cateto adjacente}}{\text{hipotenusa}} = \frac{c}{a}$
- **Tangente**: $\tan\theta = \frac{\text{cateto oposto}}{\text{cateto adjacente}} = \frac{b}{c} = \frac{\sin\theta}{\cos\theta}$

---

### 2. Identidade Fundamental e Ângulos Notáveis
Pelo Teorema de Pitágoras ($b^2 + c^2 = a^2$):
$$\sin^2\theta + \cos^2\theta = 1$$

Tabela dos Ângulos Notáveis:
| Razão | $30^\circ$ ($\pi/6$) | $45^\circ$ ($\pi/4$) | $60^\circ$ ($\pi/3$) |
|:---:|:---:|:---:|:---:|
| $\sin$ | $1/2$ | $\sqrt{2}/2$ | $\sqrt{3}/2$ |
| $\cos$ | $\sqrt{3}/2$ | $\sqrt{2}/2$ | $1/2$ |
| $\tan$ | $\sqrt{3}/3$ | $1$ | $\sqrt{3}$ |
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Altura de uma Torre
**Enunciado:** Um observador a $30\text{ m}$ da base de uma torre vertical avista seu topo sob um ângulo de elevação de $30^\circ$. Qual é a altura da torre?

**Resolução:**
1. A altura $h$ é o cateto oposto e a distância $30\text{ m}$ é o cateto adjacente:
   $$\tan 30^\circ = \frac{h}{30} \implies \frac{\sqrt{3}}{3} = \frac{h}{30} \implies h = \frac{30\sqrt{3}}{3} = 10\sqrt{3}\text{ m}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Ângulos complementares trocam seno com cosseno: $\sin(90^\circ - \theta) = \cos\theta$ e $\cos(90^\circ - \theta) = \sin\theta$.
""",
    },
    2: {
        "teoria": r"""# Arcos e o Ciclo Trigonométrico

O ciclo trigonométrico estende o domínio das razões angulares para arcos orientados de qualquer amplitude real em radianos.

### 1. O Ciclo Trigonométrico
É uma circunferência orientada de raio unitário ($R = 1$) centrada na origem $(0, 0)$ do plano cartesiano.
- Sentido positivo: Anti-horário.
- Ponto de partida: $A(1, 0)$.
- Relação graus-radianos: $180^\circ \equiv \pi\text{ rad}$.

---

### 2. Coordenadas dos Pontos no Ciclo
Para um arco de medida $\alpha$:
- A abscissa do ponto afixo é o **cosseno**: $x = \cos\alpha$.
- A ordenada do ponto afixo é o **seno**: $y = \sin\alpha$.

---

### 3. Redução ao Primeiro Quadrante
- 2º Quadrante ($\pi - x$): $\sin(\pi - x) = \sin x, \quad \cos(\pi - x) = -\cos x$
- 3º Quadrante ($\pi + x$): $\sin(\pi + x) = -\sin x, \quad \cos(\pi + x) = -\cos x$
- 4º Quadrante ($2\pi - x$): $\sin(2\pi - x) = -\sin x, \quad \cos(2\pi - x) = \cos x$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Redução de Arco ao 1º Quadrante
**Enunciado:** Calcule $\sin(150^\circ)$ e $\cos(240^\circ)$.

**Resolução:**
1. $150^\circ$ está no 2º quadrante: $\sin(150^\circ) = \sin(180^\circ - 150^\circ) = \sin(30^\circ) = 1/2$.
2. $240^\circ$ está no 3º quadrante: $\cos(240^\circ) = -\cos(240^\circ - 180^\circ) = -\cos(60^\circ) = -1/2$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Lembre-se dos sinais nos quadrantes: o seno é positivo nos quadrantes 1 e 2 (acima do eixo x); o cosseno é positivo nos quadrantes 1 e 4 (à direita do eixo y).
""",
    },
    3: {
        "teoria": r"""# Funções Circulares (Seno, Cosseno, Tangente)

As funções circulares modelam fenômenos ondulatórios, movimentos harmônicos simples e oscilações periódicas.

### 1. Função Seno ($f(x) = \sin x$)
- Domínio: $\mathbb{R}$
- Imagem: $[-1, 1]$
- Período: $T = 2\pi$
- Simetria: Função ímpar ($\sin(-x) = -\sin x$).

---

### 2. Função Cosseno ($f(x) = \cos x$)
- Domínio: $\mathbb{R}$
- Imagem: $[-1, 1]$
- Período: $T = 2\pi$
- Simetria: Função par ($\cos(-x) = \cos x$).

---

### 3. Função Tangente ($f(x) = \tan x$)
- Domínio: $\{x \in \mathbb{R} \mid x \neq \frac{\pi}{2} + k\pi, k \in \mathbb{Z}\}$
- Imagem: $\mathbb{R}$
- Período: $T = \pi$

- **Parâmetros da Senoide Generalizada**:
  Para $y = A + B\sin(Cx + D)$:
  $$\text{Amplitude} = |B|, \quad \text{Período} = \frac{2\pi}{|C|}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação de Período e Imagem
**Enunciado:** Determine o período e a imagem da função $f(x) = 3 - 2\cos(4x)$.

**Resolução:**
1. Período: $T = \frac{2\pi}{|C|} = \frac{2\pi}{4} = \frac{\pi}{2}$.
2. Variação do cosseno: $-1 \le \cos(4x) \le 1$.
3. Multiplicando por $-2$: $-2 \le -2\cos(4x) \le 2$.
4. Somando 3: $1 \le 3 - 2\cos(4x) \le 5 \implies \text{Im}(f) = [1, 5]$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Apenas o coeficiente $C$ altera o período da função periódica ($T = 2\pi/|C|$). Os parâmetros $A$ e $B$ afetam apenas o deslocamento vertical e a amplitude.
""",
    },
    4: {
        "teoria": r"""# Transformações e Fórmulas de Adição de Arcos

As identidades de adição e duplicação de arcos ampliam a álgebra trigonométrica para a resolução de equações complexas.

### 1. Fórmulas de Adição e Subtração
- $\cos(a \pm b) = \cos a \cos b \mp \sin a \sin b$
- $\sin(a \pm b) = \sin a \cos b \pm \sin b \cos a$
- $\tan(a \pm b) = \frac{\tan a \pm \tan b}{1 \mp \tan a \tan b}$

---

### 2. Fórmulas do Arco Duplo
- $\sin(2a) = 2\sin a \cos a$
- $\cos(2a) = \cos^2 a - \sin^2 a = 2\cos^2 a - 1 = 1 - 2\sin^2 a$
- $\tan(2a) = \frac{2\tan a}{1 - \tan^2 a}$

---

### 3. Fórmulas de Transformação em Produto (Prostaferese)
$$\sin p + \sin q = 2\sin\left(\frac{p+q}{2}\right)\cos\left(\frac{p-q}{2}\right)$$
$$\cos p + \cos q = 2\cos\left(\frac{p+q}{2}\right)\cos\left(\frac{p-q}{2}\right)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Cálculo de $\cos(15^\circ)$
**Enunciado:** Calcule o valor exato de $\cos(15^\circ)$ usando a subtração de arcos.

**Resolução:**
1. Escrevemos $15^\circ = 45^\circ - 30^\circ$.
2. $\cos(45^\circ - 30^\circ) = \cos 45^\circ \cos 30^\circ + \sin 45^\circ \sin 30^\circ$:
   $$\cos 15^\circ = \left(\frac{\sqrt{2}}{2}\right)\left(\frac{\sqrt{3}}{2}\right) + \left(\frac{\sqrt{2}}{2}\right)\left(\frac{1}{2}\right) = \frac{\sqrt{6} + \sqrt{2}}{4}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Lembre-se do sinal trocado na adição do cosseno: $\cos(a + b) = \cos a \cos b - \sin a \sin b$.
""",
    },
    5: {
        "teoria": r"""# Equações e Inequações Trigonométricas

A periodicidade das funções circulares introduz uma infinidade discreta de soluções descritas por parâmetros inteiros $k \in \mathbb{Z}$.

### 1. Equações Fundamentais
1. **$\sin x = \sin \alpha$**:
   $$x = \alpha + 2k\pi \quad \lor \quad x = (\pi - \alpha) + 2k\pi \quad (k \in \mathbb{Z})$$
2. **$\cos x = \cos \alpha$**:
   $$x = \pm \alpha + 2k\pi \quad (k \in \mathbb{Z})$$
3. **$\tan x = \tan \alpha$**:
   $$x = \alpha + k\pi \quad (k \in \mathbb{Z})$$

---

### 2. Inequações Trigonométricas
Resolvem-se representando graficamente os intervalos de arcos na circunferência trigonométrica que satisfazem a desigualdade no intervalo fundamental $[0, 2\pi[$ e somando as voltas completas $2k\pi$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Equação na Primeira Volta
**Enunciado:** Resolva $\sin x = 1/2$ para $x \in [0, 2\pi[$.

**Resolução:**
1. No ciclo trigonométrico, o seno é $1/2$ no 1º quadrante em $x_1 = \pi/6$ ($30^\circ$) e no 2º quadrante em $x_2 = \pi - \pi/6 = 5\pi/6$ ($150^\circ$).
2. Solução: $S = \{\pi/6, 5\pi/6\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Sempre verifique o intervalo solicitado no enunciado (ex: $[0, 2\pi[$ vs conjunto universo $\mathbb{R}$ com $+ 2k\pi$).
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"Num triângulo retângulo com hipotenusa 10 cm e cateto oposto a $\theta$ medindo 6 cm, o valor de $\cos\theta$ é:",
            "alternativas": [r"$4/5$", r"$3/5$", r"$3/4$", r"$1/2$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O valor numérico de $\sin(30^\circ) + \cos(60^\circ)$ é:",
            "alternativas": [r"$1$", r"$\sqrt{3}$", r"$1/2$", r"$\sqrt{2}/2$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se $\sin\theta = 3/5$ com $\theta$ agudo, então $\tan\theta$ vale:",
            "alternativas": [r"$3/4$", r"$4/3$", r"$4/5$", r"$5/3$"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"O valor de $\cos(120^\circ)$ no ciclo trigonométrico é:",
            "alternativas": [r"$-1/2$", r"$1/2$", r"$-\sqrt{3}/2$", r"$\sqrt{3}/2$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A conversão de $135^\circ$ para radianos é expressa por:",
            "alternativas": [r"$3\pi/4$", r"$2\pi/3$", r"$5\pi/6$", r"$4\pi/3$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Em qual quadrante o seno é negativo e o cosseno é positivo?",
            "alternativas": [r"4º Quadrante", r"1º Quadrante", r"2º Quadrante", r"3º Quadrante"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"O período da função periódica $f(x) = \sin(3x)$ é:",
            "alternativas": [r"$2\pi/3$", r"$6\pi$", r"$3\pi$", r"$\pi/3$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O valor máximo assumido pela função $g(x) = 4 - 3\cos x$ é:",
            "alternativas": [r"$7$", r"$4$", r"$1$", r"$3$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A função cosseno é uma função par porque satisfaz:",
            "alternativas": [r"$\cos(-x) = \cos x$", r"$\cos(-x) = -\cos x$", r"$\cos(x + \pi) = \cos x$", r"$\cos(0) = 0$"],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"A fórmula do arco duplo para o seno estabelece que $\sin(2a)$ equivale a:",
            "alternativas": [r"$2\sin a \cos a$", r"$\sin^2 a - \cos^2 a$", r"$2\sin a$", r"$\cos^2 a + \sin^2 a$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Sabendo que $\cos(2a) = \cos^2 a - \sin^2 a$, para $a = 45^\circ$ o valor de $\cos(90^\circ)$ é:",
            "alternativas": [r"$0$", r"$1$", r"$-1$", r"$1/2$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Se $\sin a = 3/5$ e $\cos a = 4/5$, o valor de $\sin(2a)$ é:",
            "alternativas": [r"$24/25$", r"$7/25$", r"$12/25$", r"$1$"],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"O conjunto solução da equação $\cos x = 1$ no intervalo $[0, 2\pi[$ é:",
            "alternativas": [r"$\{0\}$", r"$\{\pi\}$", r"$\{0, 2\pi\}$", r"$\{\pi/2\}$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"A quantidade de soluções de $\sin x = 0$ no intervalo fechado $[0, 2\pi]$ é:",
            "alternativas": [r"$3$", r"$2$", r"$1$", r"$4$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Para $x \in [0, \pi]$, a inequação $\sin x \ge 1/2$ é satisfeita no intervalo:",
            "alternativas": [r"$[\pi/6, 5\pi/6]$", r"$[0, \pi/6]$", r"$[5\pi/6, \pi]$", r"$[\pi/4, 3\pi/4]$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 15,
        "teorema": "Razões Trigonométricas e Identidade Fundamental",
        "texto": (
            "No triângulo retângulo, as razões seno, cosseno e tangente conectam os comprimentos dos catetos "
            "e da hipotenusa. A identidade fundamental sin²θ + cos²θ = 1 decorre diretamente do Teorema de Pitágoras."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 45,
        "teorema": "O Ciclo Trigonométrico e Redução ao 1º Quadrante",
        "texto": (
            "O ciclo de raio unitário define o seno como a ordenada e o cosseno como a abscissa do afixo do arco. "
            "A simetria nos quatro quadrantes permite reduzir qualquer arco côngruo ao primeiro quadrante."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 80,
        "teorema": "Funções Periódicas Circulares",
        "texto": (
            "As funções f(x) = sin x e g(x) = cos x possuem período 2π e imagem [-1, 1]. Na forma generalizada "
            "y = A + B sin(Cx + D), o período é dado por 2π/|C| e a amplitude por |B|."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 115,
        "teorema": "Fórmulas de Adição e Arco Duplo",
        "texto": (
            "As relações fundamentais de adição estabelecem: sin(a±b) = sin a cos b ± sin b cos a e "
            "cos(a±b) = cos a cos b ∓ sin a sin b. Para o arco duplo: sin(2a) = 2 sin a cos a e cos(2a) = cos²a - sin²a."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 145,
        "teorema": "Equações Trigonométricas Fundamentais",
        "texto": (
            "As soluções gerais de sin x = sin α são x = α + 2kπ ou x = (π - α) + 2kπ. Para cos x = cos α, "
            "as soluções são x = ±α + 2kπ com k inteiro."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Razões no Triângulo Retângulo (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um triângulo retângulo tem catetos medindo $6\text{ cm}$ e $8\text{ cm}$. O seno do ângulo oposto ao cateto de $6\text{ cm}$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$3/5$", "correta": True},
            {"letra": "B", "texto": r"$4/5$", "correta": False},
            {"letra": "C", "texto": r"$3/4$", "correta": False},
            {"letra": "D", "texto": r"$6/8$", "correta": False},
            {"letra": "E", "texto": r"$1/2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Hipotenusa: $\sqrt{6^2 + 8^2} = 10$. 2. $\sin\theta = 6/10 = 3/5$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Calcule a hipotenusa por Pitágoras e divida cateto oposto pela hipotenusa."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma rampa de $20\text{ m}$ de comprimento forma um ângulo de $30^\circ$ com o solo. A que altura vertical do solo ela chega?",
        "alternativas": [
            {"letra": "A", "texto": r"$10\text{ m}$", "correta": True},
            {"letra": "B", "texto": r"$10\sqrt{3}\text{ m}$", "correta": False},
            {"letra": "C", "texto": r"$5\text{ m}$", "correta": False},
            {"letra": "D", "texto": r"$15\text{ m}$", "correta": False},
            {"letra": "E", "texto": r"$20\text{ m}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $h = 20 \cdot \sin 30^\circ = 20 \cdot (1/2) = 10\text{ m}$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique $h = \text{hipotenusa} \cdot \sin\theta$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Se $\cos\theta = 0{,}8$ com $\theta$ agudo, qual é o valor numérico de $\tan\theta$?",
        "alternativas": [],
        "resposta_correta": "0.75",
        "resolucao_passo_a_passo": r"1. $\sin\theta = \sqrt{1 - 0{,}8^2} = 0{,}6$. 2. $\tan\theta = 0{,}6 / 0{,}8 = 3/4 = 0{,}75$.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Calcule o seno e faça seno dividido por cosseno."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor da expressão $\sin^2(27^\circ) + \sin^2(63^\circ)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$1$", "correta": True},
            {"letra": "B", "texto": r"$0$", "correta": False},
            {"letra": "C", "texto": r"$1/2$", "correta": False},
            {"letra": "D", "texto": r"$\sqrt{2}$", "correta": False},
            {"letra": "E", "texto": r"$2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $63^\circ = 90^\circ - 27^\circ \implies \sin(63^\circ) = \cos(27^\circ)$. 2. $\sin^2(27^\circ) + \cos^2(27^\circ) = 1$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Ângulos complementares: $\sin(90^\circ - x) = \cos x$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em um triângulo retângulo, a hipotenusa mede $12\text{ cm}$ e um dos ângulos agudos mede $45^\circ$. A área do triângulo é:",
        "alternativas": [
            {"letra": "A", "texto": r"$36\text{ cm}^2$", "correta": True},
            {"letra": "B", "texto": r"$72\text{ cm}^2$", "correta": False},
            {"letra": "C", "texto": r"$18\text{ cm}^2$", "correta": False},
            {"letra": "D", "texto": r"$24\text{ cm}^2$", "correta": False},
            {"letra": "E", "texto": r"$48\text{ cm}^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Catetos iguais: $c = 12 \cdot \cos 45^\circ = 6\sqrt{2}$. 2. Área = $(6\sqrt{2})^2 / 2 = 72 / 2 = 36\text{ cm}^2$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Calcule os catetos e use $\text{cateto}_1 \times \text{cateto}_2 / 2$."},
    },

    # --- Cap 2: Arcos e Ciclo Trigonométrico (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\sin(210^\circ)$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$-1/2$", "correta": True},
            {"letra": "B", "texto": r"$1/2$", "correta": False},
            {"letra": "C", "texto": r"$-\sqrt{3}/2$", "correta": False},
            {"letra": "D", "texto": r"$\sqrt{3}/2$", "correta": False},
            {"letra": "E", "texto": r"$-1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. 3º Quadrante: $\sin(210^\circ) = -\sin(210^\circ - 180^\circ) = -\sin(30^\circ) = -1/2$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Reduza ao 1º quadrante com sinal negativo para o seno no 3º quadrante."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A primeira determinação positiva do arco de $1140^\circ$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$60^\circ$", "correta": True},
            {"letra": "B", "texto": r"$30^\circ$", "correta": False},
            {"letra": "C", "texto": r"$120^\circ$", "correta": False},
            {"letra": "D", "texto": r"$240^\circ$", "correta": False},
            {"letra": "E", "texto": r"$300^\circ$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $1140^\circ = 3 \times 360^\circ + 60^\circ = 1080^\circ + 60^\circ$. Resto $60^\circ$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Divida 1140 por 360 e pegue o resto."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $\cos(300^\circ)$ no 4º quadrante é:",
        "alternativas": [
            {"letra": "A", "texto": r"$1/2$", "correta": True},
            {"letra": "B", "texto": r"$-1/2$", "correta": False},
            {"letra": "C", "texto": r"$\sqrt{3}/2$", "correta": False},
            {"letra": "D", "texto": r"$-\sqrt{3}/2$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\cos(300^\circ) = \cos(360^\circ - 300^\circ) = \cos(60^\circ) = 1/2$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "No 4º quadrante o cosseno é positivo: $\cos(360^\circ - x) = \cos x$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Quantos radianos equivalem exatamente a $270^\circ$ divididos por $\pi$?",
        "alternativas": [],
        "resposta_correta": "1.5",
        "resolucao_passo_a_passo": r"1. $270^\circ = 3\pi/2\text{ rad} = 1{,}5\pi\text{ rad}$. Dividido por $\pi$ resulta em $1{,}5$.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "$270^\circ = 3/2 \pi$ radianos."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em qual quadrante do ciclo trigonométrico a função tangente é estritamente negativa e o cosseno é positivo?",
        "alternativas": [
            {"letra": "A", "texto": r"4º Quadrante", "correta": True},
            {"letra": "B", "texto": r"2º Quadrante", "correta": False},
            {"letra": "C", "texto": r"3º Quadrante", "correta": False},
            {"letra": "D", "texto": r"1º Quadrante", "correta": False},
            {"letra": "E", "texto": r"Nenhum quadrante", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cosseno positivo nos quadrantes 1 e 4. Tangente negativa nos quadrantes 2 e 4. A interseção é o 4º quadrante. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Cruze os sinais do cosseno e da tangente em cada quadrante."},
    },

    # --- Cap 3: Funções Circulares (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O período da função $f(x) = 5\cos(2x - \pi/3)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\pi$", "correta": True},
            {"letra": "B", "texto": r"$2\pi$", "correta": False},
            {"letra": "C", "texto": r"$\pi/2$", "correta": False},
            {"letra": "D", "texto": r"$4\pi$", "correta": False},
            {"letra": "E", "texto": r"$5\pi$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $T = \frac{2\pi}{|C|} = \frac{2\pi}{2} = \pi$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Divida $2\pi$ pelo coeficiente de $x$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O conjunto imagem da função $f(x) = 2 - 3\sin x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$[-1, 5]$", "correta": True},
            {"letra": "B", "texto": r"$[-3, 3]$", "correta": False},
            {"letra": "C", "texto": r"$[2, 5]$", "correta": False},
            {"letra": "D", "texto": r"$[-1, 2]$", "correta": False},
            {"letra": "E", "texto": r"$\mathbb{R}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $-1 \le \sin x \le 1 \implies -3 \le -3\sin x \le 3$. 2. Somando 2: $-1 \le 2 - 3\sin x \le 5$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Avalie os extremos substituindo $\sin x = 1$ e $\sin x = -1$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Qual é a amplitude da função periódica $y = -7\cos(3x + 1)$?",
        "alternativas": [],
        "resposta_correta": "7",
        "resolucao_passo_a_passo": r"1. Amplitude é o módulo do coeficiente multiplicador: $|-7| = 7$.",
        "parametro_a": 1.200,
        "parametro_b": -0.800,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "A amplitude é sempre positiva: $|B|$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O domínio da função tangente $f(x) = \tan x$ exclui os pontos onde:",
        "alternativas": [
            {"letra": "A", "texto": r"$\cos x = 0 \iff x = \pi/2 + k\pi$", "correta": True},
            {"letra": "B", "texto": r"$\sin x = 0 \iff x = k\pi$", "correta": False},
            {"letra": "C", "texto": r"$\cos x = 1$", "correta": False},
            {"letra": "D", "texto": r"$x = 2k\pi$", "correta": False},
            {"letra": "E", "texto": r"$\sin x = 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\tan x = \frac{\sin x}{\cos x}$. O denominador anula-se em $x = \pi/2 + k\pi$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A tangente não existe onde o cosseno vale zero."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual das afirmações a seguir é correta sobre a paridade das funções circulares?",
        "alternativas": [
            {"letra": "A", "texto": r"O seno é ímpar ($\sin(-x) = -\sin x$) e o cosseno é par ($\cos(-x) = \cos x$)", "correta": True},
            {"letra": "B", "texto": r"Ambas são funções pares", "correta": False},
            {"letra": "C", "texto": r"Ambas são funções ímpares", "correta": False},
            {"letra": "D", "texto": r"O seno é par e o cosseno é ímpar", "correta": False},
            {"letra": "E", "texto": r"Nenhuma possui simetria", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\cos(-x) = \cos x$ (par) e $\sin(-x) = -\sin x$ (ímpar). Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "O cosseno 'engole' o sinal negativo; o seno 'expulsa' o sinal."},
    },

    # --- Cap 4: Transformações e Arco Duplo (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sabendo que $\sin x = 4/5$ e $x$ pertence ao 1º quadrante, o valor de $\cos(2x)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-7/25$", "correta": True},
            {"letra": "B", "texto": r"$7/25$", "correta": False},
            {"letra": "C", "texto": r"$24/25$", "correta": False},
            {"letra": "D", "texto": r"$-24/25$", "correta": False},
            {"letra": "E", "texto": r"$1/5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\cos(2x) = 1 - 2\sin^2 x = 1 - 2(16/25) = 1 - 32/25 = -7/25$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use $\cos(2x) = 1 - 2\sin^2 x$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor exato de $\sin(75^\circ)$ obtido pela adição $\sin(45^\circ + 30^\circ)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{\sqrt{6} + \sqrt{2}}{4}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{\sqrt{6} - \sqrt{2}}{4}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{\sqrt{3} + 1}{2}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{\sqrt{2} + 1}{2}$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\sin(45^\circ)\cos(30^\circ) + \sin(30^\circ)\cos(45^\circ) = \frac{\sqrt{2}}{2}\frac{\sqrt{3}}{2} + \frac{1}{2}\frac{\sqrt{2}}{2} = \frac{\sqrt{6}+\sqrt{2}}{4}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Aplique a fórmula $\sin(a+b) = \sin a \cos b + \sin b \cos a$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule o valor de $2\sin(15^\circ)\cos(15^\circ)$.",
        "alternativas": [],
        "resposta_correta": "0.5",
        "resolucao_passo_a_passo": r"1. Pela fórmula do arco duplo: $2\sin(15^\circ)\cos(15^\circ) = \sin(30^\circ) = 0{,}5$.",
        "parametro_a": 1.250,
        "parametro_b": -0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Reconheça a fórmula do arco duplo: $2\sin a \cos a = \sin(2a)$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A expressão simplificada de $\cos^4 x - \sin^4 x$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$\cos(2x)$", "correta": True},
            {"letra": "B", "texto": r"$\sin(2x)$", "correta": False},
            {"letra": "C", "texto": r"$1$", "correta": False},
            {"letra": "D", "texto": r"$\cos^2 x$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Diferença de quadrados: $(\cos^2 x - \sin^2 x)(\cos^2 x + \sin^2 x) = \cos(2x) \cdot 1 = \cos(2x)$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Fatore como produto da soma pela diferença."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $\tan a = 2$, o valor de $\tan(2a)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-4/3$", "correta": True},
            {"letra": "B", "texto": r"$4/3$", "correta": False},
            {"letra": "C", "texto": r"$4/5$", "correta": False},
            {"letra": "D", "texto": r"$-4/5$", "correta": False},
            {"letra": "E", "texto": r"$2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\tan(2a) = \frac{2\tan a}{1 - \tan^2 a} = \frac{2(2)}{1 - 4} = \frac{4}{-3} = -4/3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Use a fórmula do arco duplo da tangente."},
    },

    # --- Cap 5: Equações e Inequações (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O conjunto solução de $2\cos x - 1 = 0$ para $x \in [0, 2\pi[$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\{\pi/3, 5\pi/3\}$", "correta": True},
            {"letra": "B", "texto": r"$\{\pi/6, 11\pi/6\}$", "correta": False},
            {"letra": "C", "texto": r"$\{\pi/3, 2\pi/3\}$", "correta": False},
            {"letra": "D", "texto": r"$\{\pi/4, 7\pi/4\}$", "correta": False},
            {"letra": "E", "texto": r"$\{\pi/3\}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\cos x = 1/2$. No 1º quadrante $x = \pi/3$; no 4º quadrante $x = 2\pi - \pi/3 = 5\pi/3$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Identifique os ângulos do 1º e 4º quadrantes com cosseno 1/2."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma das raízes da equação $\sin(2x) = 0$ no intervalo $[0, \pi]$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3\pi/2$", "correta": True},
            {"letra": "B", "texto": r"$\pi$", "correta": False},
            {"letra": "C", "texto": r"$2\pi$", "correta": False},
            {"letra": "D", "texto": r"$\pi/2$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $2x = 0, \pi, 2\pi \implies x = 0, \pi/2, \pi$. 2. Soma = $0 + \pi/2 + \pi = 3\pi/2$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "Encontre todas as soluções de $2x = k\pi$ no intervalo."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A inequação $\cos x < 0$ para $x \in [0, 2\pi[$ é satisfeita no intervalo:",
        "alternativas": [
            {"letra": "A", "texto": r"$]\pi/2, 3\pi/2[$", "correta": True},
            {"letra": "B", "texto": r"$[0, \pi/2[$", "correta": False},
            {"letra": "C", "texto": r"$]3\pi/2, 2\pi[$", "correta": False},
            {"letra": "D", "texto": r"$[\pi, 2\pi]$", "correta": False},
            {"letra": "E", "texto": r"$]0, \pi[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O cosseno é negativo nos quadrantes 2 e 3, ou seja, de $\pi/2$ a $3\pi/2$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "O cosseno é negativo à esquerda do eixo vertical."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Quantas soluções distintas possui a equação $\sin^2 x - 1 = 0$ no intervalo $[0, 2\pi[$?",
        "alternativas": [],
        "resposta_correta": "2",
        "resolucao_passo_a_passo": r"1. $\sin^2 x = 1 \implies \sin x = \pm 1$. 2. $\sin x = 1 \implies x = \pi/2$; $\sin x = -1 \implies x = 3\pi/2$. Total 2 soluções.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "geometria", "dica_estagio_2": "Considere $\sin x = 1$ e $\sin x = -1$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para $x \in [0, 2\pi[$, a solução da equação $\tan x = \sqrt{3}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\{\pi/3, 4\pi/3\}$", "correta": True},
            {"letra": "B", "texto": r"$\{\pi/6, 7\pi/6\}$", "correta": False},
            {"letra": "C", "texto": r"$\{\pi/3, 2\pi/3\}$", "correta": False},
            {"letra": "D", "texto": r"$\{\pi/3\}$", "correta": False},
            {"letra": "E", "texto": r"$\{\pi/4, 5\pi/4\}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A tangente é positiva nos quadrantes 1 e 3. $x_1 = \pi/3$; $x_2 = \pi/3 + \pi = 4\pi/3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "geometria", "dica_estagio_2": "A tangente tem período $\pi$."},
    },
]
