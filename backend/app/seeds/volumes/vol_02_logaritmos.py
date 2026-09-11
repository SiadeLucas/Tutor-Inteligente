"""
Módulo Canônico de Dados Didáticos — Volume 2: Logaritmos
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (5 caps), FIXACAO_DATA (15 questões), RAG_DATA (6 fragmentos), TRI_DATA (25 itens).
"""

VOLUME_INFO = {
    "numero": 2,
    "titulo": "Logaritmos",
    "grande_area": "algebra_funcoes",
    "ordem": 2,
    "capitulos": [
        {"num": 1, "titulo": "Potências e Raízes Aritméticas", "tempo": 50},
        {"num": 2, "titulo": "Função Exponencial e Equações", "tempo": 50},
        {"num": 3, "titulo": "Conceito e Propriedades dos Logaritmos", "tempo": 50},
        {"num": 4, "titulo": "Função Logarítmica e Gráficos", "tempo": 50},
        {"num": 5, "titulo": "Equações e Inequações Logarítmicas", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Potências e Raízes Aritméticas

A teoria dos expoentes reais estende a multiplicação repetida para expoentes fracionários e irracionais, constituindo o alicerce formal para o estudo das funções exponenciais e logarítmicas.

### 1. Definição e Expoentes Inteiros
Para $a \in \mathbb{R}$ e $n \in \mathbb{N}^*$:
$$a^1 = a, \quad a^n = \underbrace{a \cdot a \cdots a}_{n \text{ fatores}}$$
- Expoente nulo: Para $a \neq 0$, define-se $a^0 = 1$.
- Expoente negativo: Para $a \neq 0$ e $n \in \mathbb{N}^*$, $a^{-n} = \frac{1}{a^n} = \left(\frac{1}{a}\right)^n$.

---

### 2. Propriedades Operatórias das Potências
Para bases reais não-nulas $a, b$ e expoentes $m, n \in \mathbb{R}$:
1. **Produto de mesma base**: $a^m \cdot a^n = a^{m+n}$
2. **Quociente de mesma base**: $\frac{a^m}{a^n} = a^{m-n}$
3. **Potência de potência**: $(a^m)^n = a^{m \cdot n}$
4. **Potência de produto e quociente**: $(a \cdot b)^n = a^n \cdot b^n \quad \text{e} \quad \left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}$

---

### 3. Raízes Aritméticas e Expoentes Fracionários
Para $a \ge 0$ e $n \in \mathbb{N}, n \ge 2$, a raiz $n$-ésima aritmética $\sqrt[n]{a}$ é o único número real não-negativo $b$ tal que $b^n = a$.
- **Expoente Racional Fracionário**:
$$a^{m/n} = \sqrt[n]{a^m} = (\sqrt[n]{a})^m \quad (a > 0, m \in \mathbb{Z}, n \in \mathbb{N}^*)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Simplificação com Expoentes Fracionários
**Enunciado:** Calcule o valor numérico de $E = 8^{2/3} + 16^{-3/4} - 27^{1/3}$.

**Resolução Passo a Passo:**
1. Escrevemos cada base na forma fatorada prima:
   - $8^{2/3} = (2^3)^{2/3} = 2^{3 \cdot (2/3)} = 2^2 = 4$
   - $16^{-3/4} = (2^4)^{-3/4} = 2^{4 \cdot (-3/4)} = 2^{-3} = \frac{1}{2^3} = \frac{1}{8}$
   - $27^{1/3} = (3^3)^{1/3} = 3^1 = 3$
2. Efetuamos as operações:
   $$E = 4 + \frac{1}{8} - 3 = 1 + \frac{1}{8} = \frac{9}{8}$$

---

### Exemplo 2: Racionalização de Denominadores
**Enunciado:** Racionalize a fração $\frac{6}{\sqrt{5} - \sqrt{2}}$.

**Resolução:**
1. Multiplicamos numerador e denominador pelo conjugado $(\sqrt{5} + \sqrt{2})$:
   $$\frac{6(\sqrt{5} + \sqrt{2})}{(\sqrt{5} - \sqrt{2})(\sqrt{5} + \sqrt{2})} = \frac{6(\sqrt{5} + \sqrt{2})}{(\sqrt{5})^2 - (\sqrt{2})^2} = \frac{6(\sqrt{5} + \sqrt{2})}{5 - 2} = \frac{6(\sqrt{5} + \sqrt{2})}{3}$$
2. Simplificando a fração por 3:
   $$2(\sqrt{5} + \sqrt{2}) = 2\sqrt{5} + 2\sqrt{2}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Base Negativa com Expoente Racional:**
> A identidade $a^{m/n} = \sqrt[n]{a^m}$ é rigorosamente restrita a $a > 0$. Para bases negativas, $(-8)^{2/6} \neq (-8)^{1/3}$ no campo real, pois $(-8)^{2/6} = \sqrt[6]{(-8)^2} = \sqrt[6]{64} = 2$, enquanto $(-8)^{1/3} = -2$!

> [!TIP]
> Em potências de potências, lembre-se da hierarquia: $(a^m)^n = a^{m \cdot n}$, mas $a^{m^n} = a^{(m^n)}$.
""",
    },
    2: {
        "teoria": r"""# Função Exponencial e Equações

A função exponencial é o modelo universal de crescimento e decaimento irrestrito em Física, Biologia e Finanças.

### 1. Definição Formal
Dado um número real $a > 0$ com $a \neq 1$, a função $f: \mathbb{R} \to \mathbb{R}^*_+$ definida por:
$$f(x) = a^x$$
chama-se **função exponencial** de base $a$.
- **Domínio**: $D(f) = \mathbb{R}$
- **Conjunto Imagem**: $\text{Im}(f) = \mathbb{R}^*_+ = ]0, +\infty[$
- Ponto fixo: O gráfico sempre corta o eixo das ordenadas em $(0, 1)$, pois $a^0 = 1$.

---

### 2. Comportamento e Crescimento
- Se $a > 1$: A função é **estritamente crescente**.
  $$x_1 < x_2 \iff a^{x_1} < a^{x_2}$$
- Se $0 < a < 1$: A função é **estritamente decrescente**.
  $$x_1 < x_2 \iff a^{x_1} > a^{x_2}$$
- **Assíntota Horizontal**: O eixo das abscissas ($y = 0$) é uma assíntota horizontal da curva.

---

### 3. Equações Exponenciais
Equações nas quais a incógnita figura no expoente são resolvidas reduzindo ambos os membros à mesma base:
$$a^{f(x)} = a^{g(x)} \iff f(x) = g(x) \quad (a > 0, a \neq 1)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Equação com Mudança de Variável
**Enunciado:** Resolva em $\mathbb{R}$ a equação exponencial $4^x - 5 \cdot 2^x + 4 = 0$.

**Resolução:**
1. Observamos que $4^x = (2^2)^x = (2^x)^2$.
2. Fazemos a substituição de variável $y = 2^x$ (com a restrição $y > 0$):
   $$y^2 - 5y + 4 = 0$$
3. Fatorando ou aplicando Bhaskara:
   $$(y - 1)(y - 4) = 0 \implies y = 1 \quad \text{ou} \quad y = 4$$
4. Retornamos à variável original $x$:
   - $2^x = 1 = 2^0 \implies x_1 = 0$
   - $2^x = 4 = 2^2 \implies x_2 = 2$
5. Conjunto Solução: $S = \{0, 2\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Nunca aceite soluções onde a substituição de variável $y = a^x$ resulte em valor negativo ou nulo ($y \le 0$), pois $a^x > 0$ para todo $x \in \mathbb{R}$.

> [!TIP]
> Em inequações exponenciais com base entre 0 e 1 ($0 < a < 1$), lembre-se de **inverter o sentido da desigualdade** ao comparar os expoentes!
""",
    },
    3: {
        "teoria": r"""# Conceito e Propriedades dos Logaritmos

O logaritmo desfaz a exponenciação, permitindo determinar a que expoente uma dada base deve ser elevada para atingir determinado valor.

### 1. Definição Formal
Dados $a, b \in \mathbb{R}$ com $a > 0, a \neq 1$ e $b > 0$, chama-se **logaritmo de $b$ na base $a$** o expoente $x$ ao qual se deve elevar a base $a$ para obter o logaritmando $b$:
$$\log_a b = x \iff a^x = b$$
- $a$: base do logaritmo ($a > 0$ e $a \neq 1$)
- $b$: logaritmando ($b > 0$)
- $x$: logaritmo

---

### 2. Consequências Imediatas
1. $\log_a 1 = 0$ (pois $a^0 = 1$)
2. $\log_a a = 1$ (pois $a^1 = a$)
3. $\log_a (a^k) = k$
4. **Identidade Fundamental**: $a^{\log_a b} = b$

---

### 3. Propriedades Operatórias Fundamentais
Para $a > 0, a \neq 1$ e $x, y > 0$:
1. **Logaritmo do Produto**: $\log_a (x \cdot y) = \log_a x + \log_a y$
2. **Logaritmo do Quociente**: $\log_a \left(\frac{x}{y}\right) = \log_a x - \log_a y$
3. **Logaritmo da Potência**: $\log_a (x^k) = k \cdot \log_a x$
4. **Mudança de Base**: Para qualquer base $c > 0, c \neq 1$:
   $$\log_a b = \frac{\log_c b}{\log_c a}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Aplicação das Propriedades Operatórias
**Enunciado:** Sabendo que $\log_{10} 2 \approx 0{,}301$ e $\log_{10} 3 \approx 0{,}477$, determine o valor aproximado de $\log_{10} 12$ e de $\log_{10} 5$.

**Resolução:**
1. Fatoramos $12 = 2^2 \cdot 3$:
   $$\log_{10} 12 = \log_{10} (2^2 \cdot 3) = \log_{10} (2^2) + \log_{10} 3 = 2\log_{10} 2 + \log_{10} 3$$
   $$\log_{10} 12 \approx 2(0{,}301) + 0{,}477 = 0{,}602 + 0{,}477 = 1{,}079$$
2. Para $\log_{10} 5$, usamos o artifício $5 = \frac{10}{2}$:
   $$\log_{10} 5 = \log_{10} \left(\frac{10}{2}\right) = \log_{10} 10 - \log_{10} 2 = 1 - 0{,}301 = 0{,}699$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Erro Mais Comum da Álgebra:**
> $\log(x + y) \neq \log x + \log y$ e $\frac{\log x}{\log y} \neq \log(x - y)$!
> O logaritmo transforma produto em soma de logaritmos, e não a soma em produto.

> [!TIP]
> O artifício $\log_{10} 5 = 1 - \log_{10} 2$ é cobrado em praticamente todos os vestibulares e no ENEM!
""",
    },
    4: {
        "teoria": r"""# Função Logarítmica e Gráficos

A função logarítmica é a inversa bijetora da função exponencial, desempenhando papel crucial em escalas físicas sensoriais (Decibel, Richter, pH).

### 1. Definição Formal
Seja $a > 0$ com $a \neq 1$. A função $f: \mathbb{R}^*_+ \to \mathbb{R}$ definida por:
$$f(x) = \log_a x$$
chama-se **função logarítmica** de base $a$.
- **Domínio**: $D(f) = \mathbb{R}^*_+ = ]0, +\infty[$
- **Conjunto Imagem**: $\text{Im}(f) = \mathbb{R}$
- Ponto fixo: Corta o eixo das abscissas em $(1, 0)$, pois $\log_a 1 = 0$.

---

### 2. Monotonicidade e Assíntota
- Se $a > 1$: Função **estritamente crescente**.
  $$x_1 < x_2 \iff \log_a x_1 < \log_a x_2$$
- Se $0 < a < 1$: Função **estritamente decrescente**.
  $$x_1 < x_2 \iff \log_a x_1 > \log_a x_2$$
- **Assíntota Vertical**: O eixo das ordenadas ($x = 0$) é uma assíntota vertical do gráfico.
- **Simetria**: O gráfico de $y = \log_a x$ é simétrico ao de $y = a^x$ em relação à reta bissetriz $y = x$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Domínio de Função Logarítmica
**Enunciado:** Determine o domínio real da função $f(x) = \log_3 \left(\frac{x - 2}{5 - x}\right)$.

**Resolução:**
1. A condição de existência exige logaritmando estritamente positivo:
   $$\frac{x - 2}{5 - x} > 0$$
2. Fazemos o quadro de sinais para o quociente:
   - Numerador $x - 2 = 0 \implies x = 2$ (positivo para $x > 2$)
   - Denominador $5 - x = 0 \implies x = 5$ (positivo para $x < 5$)
3. O quociente é positivo estritamente no intervalo entre 2 e 5:
   $$D(f) = ]2, 5[$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> O logaritmando deve ser **estritamente positivo** ($> 0$). Não confunda com a condição de radicandos reais que aceitam zero ($\ge 0$). Logaritmo de zero não existe!
""",
    },
    5: {
        "teoria": r"""# Equações e Inequações Logarítmicas

A resolução de equações e inequações com logaritmos requer controle rigoroso das Condições de Existência (C.E.) antes de qualquer transformação algébrica.

### 1. Condições de Existência (C.E.)
Para $\log_{g(x)} f(x)$:
$$\begin{cases} f(x) > 0 & \text{(logaritmando positivo)} \\ g(x) > 0 \text{ e } g(x) \neq 1 & \text{(base positiva e diferente de 1)} \end{cases}$$

---

### 2. Resolução de Equações
1. **Tipo $\log_a f(x) = \log_a g(x)$**:
   $$f(x) = g(x), \quad \text{com } f(x) > 0 \text{ e } g(x) > 0$$
2. **Tipo $\log_a f(x) = k$**:
   $$f(x) = a^k, \quad \text{com } f(x) > 0$$

---

### 3. Inequações Logarítmicas
- **Base maior que 1 ($a > 1$)**: Mantém-se o sinal da desigualdade:
  $$\log_a f(x) < \log_a g(x) \iff 0 < f(x) < g(x)$$
- **Base entre 0 e 1 ($0 < a < 1$)**: **Inverte-se** o sinal da desigualdade:
  $$\log_a f(x) < \log_a g(x) \iff f(x) > g(x) > 0$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Equação com Propriedade da Soma
**Enunciado:** Resolva em $\mathbb{R}$ a equação $\log_2 (x - 1) + \log_2 (x + 1) = 3$.

**Resolução:**
1. **Condições de Existência (C.E.):**
   $$x - 1 > 0 \implies x > 1 \quad \text{e} \quad x + 1 > 0 \implies x > -1 \implies x > 1$$
2. Aplicamos a propriedade da soma de logaritmos:
   $$\log_2 ((x - 1)(x + 1)) = 3 \implies \log_2 (x^2 - 1) = 3$$
3. Pela definição:
   $$x^2 - 1 = 2^3 = 8 \implies x^2 = 9 \implies x = 3 \quad \text{ou} \quad x = -3$$
4. Verificação com a C.E. ($x > 1$):
   - $x = 3 > 1$ (Válido!)
   - $x = -3 < 1$ (Rejeitado!)
5. Solução: $S = \{3\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Esquecer a Condição de Existência (C.E.):**
> É a causa de 90% dos erros em vestibulares. Sempre estabeleça a C.E. na primeira linha da resolução, antes de condensar somas em produtos. Se condensar antes, $(-3)^2 - 1 = 8$ pareceria válida, mas $\log_2(-4)$ não existe em $\mathbb{R}$!
""",
    },
}

FIXACAO_DATA = {
    1: [
        {
            "numero": 1,
            "enunciado": r"O valor numérico da expressão $E = 27^{2/3} + 16^{3/4}$ é:",
            "alternativas": [r"$17$", r"$15$", r"$25$", r"$13$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Para $a > 0$, a expressão simplificada de $\frac{a^3 \cdot a^{-5}}{a^{-4}}$ é:",
            "alternativas": [r"$a^2$", r"$a^{-6}$", r"$a^6$", r"$a^{-2}$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A fração racionalizada correspondente a $\frac{10}{\sqrt{5}}$ vale:",
            "alternativas": [r"$2\sqrt{5}$", r"$5\sqrt{2}$", r"$\sqrt{5}$", r"$10\sqrt{5}$"],
            "indice_correto": 0,
        },
    ],
    2: [
        {
            "numero": 1,
            "enunciado": r"A solução real da equação exponencial $3^{2x - 1} = 27$ é:",
            "alternativas": [r"$x = 2$", r"$x = 1$", r"$x = 3$", r"$x = 4$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Se a base de uma função exponencial $f(x) = a^x$ é $a = 1/3$, a função é:",
            "alternativas": [
                r"Estritamente decrescente em todo o domínio",
                r"Estritamente crescente em todo o domínio",
                r"Constante e igual a zero",
                r"Não definida para reais negativos",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"O conjunto imagem da função exponencial real $f(x) = 2^x + 5$ é:",
            "alternativas": [r"$]5, +\infty[$", r"$[5, +\infty[$", r"$]0, +\infty[$", r"$\mathbb{R}$"],
            "indice_correto": 0,
        },
    ],
    3: [
        {
            "numero": 1,
            "enunciado": r"O valor do logaritmo $\log_3 81$ é igual a:",
            "alternativas": [r"$4$", r"$3$", r"$27$", r"$9$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Se $\log_{10} 2 = 0{,}30$, então o valor de $\log_{10} 5$ é:",
            "alternativas": [r"$0{,}70$", r"$0{,}60$", r"$0{,}50$", r"$1{,}30$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A propriedade correta do logaritmo da potência é expressa por:",
            "alternativas": [
                r"$\log_a (x^k) = k \cdot \log_a x$",
                r"$\log_a (x^k) = (\log_a x)^k$",
                r"$\log_a (x^k) = \log_a (k \cdot x)$",
                r"$\log_a (x^k) = k + \log_a x$",
            ],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"O domínio da função real $f(x) = \log_5 (2x - 8)$ em $\mathbb{R}$ é:",
            "alternativas": [r"$]4, +\infty[$", r"$[4, +\infty[$", r"$]-\infty, 4[$", r"$\mathbb{R} \setminus \{4\}$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"O gráfico de $y = \log_a x$ sempre intersecta o eixo das abscissas no ponto:",
            "alternativas": [r"$(1, 0)$", r"$(0, 1)$", r"$(a, 0)$", r"$(0, 0)$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"A função logarítmica $f(x) = \log_{0{,}5} x$ é:",
            "alternativas": [
                r"Estritamente decrescente",
                r"Estritamente crescente",
                r"Limitada superiormente",
                r"Periódica de período 1",
            ],
            "indice_correto": 0,
        },
    ],
    5: [
        {
            "numero": 1,
            "enunciado": r"O conjunto solução da equação $\log_3 (x - 2) = 2$ em $\mathbb{R}$ é:",
            "alternativas": [r"$S = \{11\}$", r"$S = \{8\}$", r"$S = \{7\}$", r"$S = \{9\}$"],
            "indice_correto": 0,
        },
        {
            "numero": 2,
            "enunciado": r"Na inequação $\log_{1/2} x > \log_{1/2} 4$, a solução é o intervalo:",
            "alternativas": [r"$]0, 4[$", r"$]4, +\infty[$", r"$[0, 4[$", r"$]-\infty, 4[$"],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Qual o valor de $x$ que satisfaz $\log_2 x + \log_2 (x - 2) = 3$?",
            "alternativas": [r"$x = 4$", r"$x = -2$", r"$x = 2$", r"$x = 6$"],
            "indice_correto": 0,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 15,
        "teorema": "Propriedades Operatórias de Potências e Radicais",
        "texto": (
            "Para base real positiva a e expoentes reais quaisquer, valem as identidades fundamentais: "
            "a^m · a^n = a^(m+n), a^m / a^n = a^(m-n) e (a^m)^n = a^(m·n). O expoente racional a^(m/n) = √(a^m) "
            "unifica a teoria dos radicais com a álgebra das potências."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 48,
        "teorema": "Definição e Comportamento da Função Exponencial",
        "texto": (
            "A função f(x) = a^x com a > 0 e a ≠ 1 possui domínio R e imagem R*+. Se a > 1 a função é estritamente "
            "crescente; se 0 < a < 1 a função é estritamente decrescente. O eixo Ox é assíntota horizontal."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 82,
        "teorema": "Definição Rigorosa de Logaritmo e Mudança de Base",
        "texto": (
            "Para a > 0, a ≠ 1 e b > 0, define-se log_a(b) = x ⇔ a^x = b. As propriedades operatórias fundamentais "
            "são: log_a(xy) = log_a(x) + log_a(y), log_a(x/y) = log_a(x) - log_a(y) e log_a(x^k) = k · log_a(x). "
            "A fórmula de mudança de base estabelece: log_a(b) = log_c(b) / log_c(a)."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 110,
        "teorema": "A Função Logarítmica como Inversa da Exponencial",
        "texto": (
            "A função f(x) = log_a(x) é a inversa bijetora de g(x) = a^x. Seu domínio é R*+ e imagem R. "
            "O gráfico corta o eixo das abscissas em (1, 0) e possui o eixo Oy como assíntota vertical."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 138,
        "teorema": "Resolução de Equações e Inequações Logarítmicas",
        "texto": (
            "Toda equação ou inequação logarítmica exige a verificação prévia das Condições de Existência (C.E.): "
            "logaritmando estritamente positivo e base positiva e diferente de 1. Em inequações, se a base estiver "
            "entre 0 e 1, deve-se inverter o sentido da desigualdade entre os logaritmandos."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Potências e Raízes Aritméticas (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor numérico da expressão $E = 8^{2/3} + 16^{-3/4}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$33/8$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$35/8$", "correta": False},
            {"letra": "D", "texto": r"$17/4$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $8^{2/3} = (2^3)^{2/3} = 2^2 = 4$. 2. $16^{-3/4} = (2^4)^{-3/4} = 2^{-3} = 1/8$. 3. $4 + 1/8 = 33/8$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Fatore as bases em potências de 2 e multiplique os expoentes."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Simplificando a expressão com radicais $\sqrt{50} - \sqrt{18} + \sqrt{8}$, obtém-se:",
        "alternativas": [
            {"letra": "A", "texto": r"$4\sqrt{2}$", "correta": True},
            {"letra": "B", "texto": r"$3\sqrt{2}$", "correta": False},
            {"letra": "C", "texto": r"$5\sqrt{2}$", "correta": False},
            {"letra": "D", "texto": r"$2\sqrt{2}$", "correta": False},
            {"letra": "E", "texto": r"$\sqrt{40}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\sqrt{50} = 5\sqrt{2}$. 2. $\sqrt{18} = 3\sqrt{2}$. 3. $\sqrt{8} = 2\sqrt{2}$. 4. $5\sqrt{2} - 3\sqrt{2} + 2\sqrt{2} = 4\sqrt{2}$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Fatore os números sob o radical em fatores quadrados perfeitos."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Racionalizando o denominador da fração $\frac{6}{\sqrt{5} - \sqrt{2}}$, obtém-se:",
        "alternativas": [
            {"letra": "A", "texto": r"$2(\sqrt{5} + \sqrt{2})$", "correta": True},
            {"letra": "B", "texto": r"$3(\sqrt{5} + \sqrt{2})$", "correta": False},
            {"letra": "C", "texto": r"$\sqrt{5} + \sqrt{2}$", "correta": False},
            {"letra": "D", "texto": r"$2(\sqrt{5} - \sqrt{2})$", "correta": False},
            {"letra": "E", "texto": r"$6(\sqrt{5} + \sqrt{2})$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Multiplica-se pelo conjugado: $\frac{6(\sqrt{5}+\sqrt{2})}{5 - 2} = \frac{6(\sqrt{5}+\sqrt{2})}{3} = 2(\sqrt{5}+\sqrt{2})$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique numerador e denominador pelo conjugado."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule o valor de $(0{,}25)^{-3/2}$.",
        "alternativas": [],
        "resposta_correta": "8",
        "resolucao_passo_a_passo": r"1. $0{,}25 = 1/4 = 2^{-2}$. 2. $(2^{-2})^{-3/2} = 2^{(-2) \cdot (-3/2)} = 2^3 = 8$.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Converta o decimal 0,25 na fração 1/4 e escreva como potência de 2."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $x = 2^{60}$, $y = 3^{40}$ e $z = 5^{20}$, a relação de ordem correta entre esses números é:",
        "alternativas": [
            {"letra": "A", "texto": r"$z < x < y$", "correta": True},
            {"letra": "B", "texto": r"$x < y < z$", "correta": False},
            {"letra": "C", "texto": r"$y < x < z$", "correta": False},
            {"letra": "D", "texto": r"$z < y < x$", "correta": False},
            {"letra": "E", "texto": r"$x < z < y$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Expoente comum $20$: $x = (2^3)^{20} = 8^{20}$; $y = (3^2)^{20} = 9^{20}$; $z = 5^{20}$. 2. Como $5 < 8 < 9$, temos $z < x < y$. Alternativa A.",
        "parametro_a": 1.650,
        "parametro_b": 1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Reduza todos os números ao mesmo expoente pelo MDC dos expoentes (20)."},
    },

    # --- Cap 2: Função Exponencial e Equações (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma das raízes da equação exponencial $4^x - 5 \cdot 2^x + 4 = 0$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$2$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$5$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $y = 2^x \implies y^2 - 5y + 4 = 0 \implies y = 1$ ou $y = 4$. 2. $2^x = 1 \implies x = 0$; $2^x = 4 \implies x = 2$. 3. Soma = $0 + 2 = 2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Faça a mudança de variável $y = 2^x$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Resolvendo em $\mathbb{R}$ a inequação exponencial $(1/2)^{3x - 1} \le (1/2)^{x + 5}$, obtemos:",
        "alternativas": [
            {"letra": "A", "texto": r"$x \ge 3$", "correta": True},
            {"letra": "B", "texto": r"$x \le 3$", "correta": False},
            {"letra": "C", "texto": r"$x \ge 2$", "correta": False},
            {"letra": "D", "texto": r"$x \le 2$", "correta": False},
            {"letra": "E", "texto": r"$x \ge -3$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Base $1/2 < 1$, inverte o sinal: $3x - 1 \ge x + 5 \implies 2x \ge 6 \implies x \ge 3$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Atenção: base menor que 1 inverte a desigualdade dos expoentes."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A solução da equação $9^{x + 1} = 27^{x - 1}$ em $\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 5$", "correta": True},
            {"letra": "B", "texto": r"$x = 3$", "correta": False},
            {"letra": "C", "texto": r"$x = 4$", "correta": False},
            {"letra": "D", "texto": r"$x = 2$", "correta": False},
            {"letra": "E", "texto": r"$x = 6$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Base 3: $(3^2)^{x+1} = (3^3)^{x-1} \implies 2x + 2 = 3x - 3 \implies x = 5$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Passe ambas as potências para a base 3."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma população bacteriana dobra a cada $3$ horas. Inicialmente com $500$ bactérias, após $12$ horas o total será de:",
        "alternativas": [
            {"letra": "A", "texto": r"$8.000$ bactérias", "correta": True},
            {"letra": "B", "texto": r"$4.000$ bactérias", "correta": False},
            {"letra": "C", "texto": r"$6.000$ bactérias", "correta": False},
            {"letra": "D", "texto": r"$16.000$ bactérias", "correta": False},
            {"letra": "E", "texto": r"$2.000$ bactérias", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Em 12 horas ocorrem $12/3 = 4$ ciclos de duplicação. 2. $P = 500 \cdot 2^4 = 500 \cdot 16 = 8.000$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule a quantidade de períodos e aplique $P_0 \cdot 2^k$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine o valor de $x$ que satisfaz $2^{x + 3} + 2^{x} = 72$.",
        "alternativas": [],
        "resposta_correta": "3",
        "resolucao_passo_a_passo": r"1. $2^x \cdot 2^3 + 2^x = 72 \implies 8 \cdot 2^x + 2^x = 72 \implies 9 \cdot 2^x = 72$. 2. $2^x = 8 = 2^3 \implies x = 3$.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Coloque o termo $2^x$ em evidência."},
    },

    # --- Cap 3: Conceito e Propriedades dos Logaritmos (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor da expressão $E = \log_2 32 - \log_3 (1/27) + \log_{10} 0{,}01$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$10$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\log_2 32 = 5$. 2. $\log_3 (3^{-3}) = -3$. 3. $\log_{10} 10^{-2} = -2$. 4. $E = 5 - (-3) + (-2) = 5 + 3 - 2 = 6$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule cada logaritmo usando a definição de potência."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sabendo que $\log_{10} 2 = a$ e $\log_{10} 3 = b$, o valor de $\log_{10} 72$ expresso em termos de $a$ e $b$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3a + 2b$", "correta": True},
            {"letra": "B", "texto": r"$2a + 3b$", "correta": False},
            {"letra": "C", "texto": r"$6ab$", "correta": False},
            {"letra": "D", "texto": r"$3a - 2b$", "correta": False},
            {"letra": "E", "texto": r"$a^3 \cdot b^2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $72 = 2^3 \cdot 3^2$. 2. $\log_{10} (2^3 \cdot 3^2) = 3\log_{10} 2 + 2\log_{10} 3 = 3a + 2b$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Decomponha 72 em fatores primos."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor da expressão $5^{\log_5 12} + 3^{\log_3 7}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$19$", "correta": True},
            {"letra": "B", "texto": r"$84$", "correta": False},
            {"letra": "C", "texto": r"$15$", "correta": False},
            {"letra": "D", "texto": r"$23$", "correta": False},
            {"letra": "E", "texto": r"$35$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela identidade fundamental $a^{\log_a b} = b$: $5^{\log_5 12} = 12$ e $3^{\log_3 7} = 7$. 2. $12 + 7 = 19$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Lembre-se da identidade fundamental: $a^{\log_a b} = b$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $\log_2 3 = k$, então $\log_3 16$ vale:",
        "alternativas": [
            {"letra": "A", "texto": r"$4/k$", "correta": True},
            {"letra": "B", "texto": r"$4k$", "correta": False},
            {"letra": "C", "texto": r"$k/4$", "correta": False},
            {"letra": "D", "texto": r"$k^4$", "correta": False},
            {"letra": "E", "texto": r"$16/k$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Mudança de base para 2: $\log_3 16 = \frac{\log_2 16}{\log_2 3} = \frac{4}{k}$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique a fórmula de mudança de base."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Sabendo que $\log_{10} 2 = 0{,}30$, calcule o valor de $\log_{10} 200$.",
        "alternativas": [],
        "resposta_correta": "2.3",
        "resolucao_passo_a_passo": r"1. $200 = 2 \cdot 100 = 2 \cdot 10^2$. 2. $\log_{10} 200 = \log_{10} 2 + \log_{10} 10^2 = 0{,}30 + 2 = 2{,}30$.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Escreva $200$ como $2 \cdot 10^2$."},
    },

    # --- Cap 4: Função Logarítmica e Gráficos (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O domínio da função real $f(x) = \log_4 (x^2 - 9)$ em $\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$]-\infty, -3[ \cup ]3, +\infty[$", "correta": True},
            {"letra": "B", "texto": r"$]-3, 3[$", "correta": False},
            {"letra": "C", "texto": r"$[3, +\infty[$", "correta": False},
            {"letra": "D", "texto": r"$\mathbb{R} \setminus \{-3, 3\}$", "correta": False},
            {"letra": "E", "texto": r"$]0, +\infty[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. C.E.: $x^2 - 9 > 0$. 2. As raízes são $\pm 3$. Como a parábola tem $a > 0$, é positiva fora das raízes: $x < -3$ ou $x > 3$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Estude o sinal da função quadrática no logaritmando."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A função inversa de $f(x) = \log_3 (x - 1)$ para $x > 1$ é dada por:",
        "alternativas": [
            {"letra": "A", "texto": r"$f^{-1}(x) = 3^x + 1$", "correta": True},
            {"letra": "B", "texto": r"$f^{-1}(x) = 3^x - 1$", "correta": False},
            {"letra": "C", "texto": r"$f^{-1}(x) = 3^{x + 1}$", "correta": False},
            {"letra": "D", "texto": r"$f^{-1}(x) = \log_3 (x + 1)$", "correta": False},
            {"letra": "E", "texto": r"$f^{-1}(x) = \frac{1}{\log_3 (x - 1)}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $y = \log_3 (x - 1) \implies x - 1 = 3^y \implies x = 3^y + 1$. 2. $f^{-1}(x) = 3^x + 1$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Isole $x$ usando a definição de logaritmo como exponencial."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual das retas a seguir é a assíntota vertical do gráfico de $f(x) = \log_2 (x - 5)$?",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 5$", "correta": True},
            {"letra": "B", "texto": r"$y = 5$", "correta": False},
            {"letra": "C", "texto": r"$x = 0$", "correta": False},
            {"letra": "D", "texto": r"$y = 0$", "correta": False},
            {"letra": "E", "texto": r"$x = -5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A assíntota vertical ocorre onde o logaritmando se anula: $x - 5 = 0 \implies x = 5$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A assíntota vertical localiza-se na fronteira do domínio."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para qual valor de $x$ a função $f(x) = \log_5 (3x + 1)$ assume o valor $2$?",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 8$", "correta": True},
            {"letra": "B", "texto": r"$x = 5$", "correta": False},
            {"letra": "C", "texto": r"$x = 10$", "correta": False},
            {"letra": "D", "texto": r"$x = 7$", "correta": False},
            {"letra": "E", "texto": r"$x = 9$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\log_5 (3x + 1) = 2 \implies 3x + 1 = 5^2 = 25 \implies 3x = 24 \implies x = 8$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique a definição de logaritmo e resolva a equação de 1º grau."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O ponto de interseção do gráfico de $f(x) = \log_3 (x + 2) - 1$ com o eixo das abscissas é:",
        "alternativas": [
            {"letra": "A", "texto": r"$(1, 0)$", "correta": True},
            {"letra": "B", "texto": r"$(0, 0)$", "correta": False},
            {"letra": "C", "texto": r"$(3, 0)$", "correta": False},
            {"letra": "D", "texto": r"$(2, 0)$", "correta": False},
            {"letra": "E", "texto": r"$(-1, 0)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f(x) = 0 \implies \log_3 (x + 2) = 1 \implies x + 2 = 3^1 = 3 \implies x = 1$. Ponto $(1, 0)$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Iguale a função a zero para encontrar o corte com o eixo x."},
    },

    # --- Cap 5: Equações e Inequações Logarítmicas (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O conjunto solução da equação $\log_2 (x - 1) + \log_2 (x + 1) = 3$ em $\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$S = \{3\}$", "correta": True},
            {"letra": "B", "texto": r"$S = \{-3, 3\}$", "correta": False},
            {"letra": "C", "texto": r"$S = \{4\}$", "correta": False},
            {"letra": "D", "texto": r"$S = \{2\}$", "correta": False},
            {"letra": "E", "texto": r"$S = \emptyset$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. C.E.: $x > 1$. 2. $\log_2 (x^2 - 1) = 3 \implies x^2 - 1 = 8 \implies x = \pm 3$. 3. Pela C.E., apenas $x = 3$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Lembre-se de descartar raízes que não atendem à Condição de Existência."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o conjunto solução da inequação $\log_{1/3} (2x - 5) > -2$ em $\mathbb{R}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$]5/2, 7[$", "correta": True},
            {"letra": "B", "texto": r"$]7, +\infty[$", "correta": False},
            {"letra": "C", "texto": r"$]-\infty, 7[$", "correta": False},
            {"letra": "D", "texto": r"$[5/2, 7]$", "correta": False},
            {"letra": "E", "texto": r"$]0, 7[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. C.E.: $2x - 5 > 0 \implies x > 5/2$. 2. Base $1/3 < 1$, inverte sinal: $2x - 5 < (1/3)^{-2} = 9 \implies 2x < 14 \implies x < 7$. 3. $]5/2, 7[$. Alternativa A.",
        "parametro_a": 1.550,
        "parametro_b": 1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Combine a C.E. do logaritmando com a inversão da desigualdade."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Resolvendo a equação $(\log_2 x)^2 - 4\log_2 x + 3 = 0$, o produto das raízes reais é:",
        "alternativas": [
            {"letra": "A", "texto": r"$16$", "correta": True},
            {"letra": "B", "texto": r"$8$", "correta": False},
            {"letra": "C", "texto": r"$4$", "correta": False},
            {"letra": "D", "texto": r"$10$", "correta": False},
            {"letra": "E", "texto": r"$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $y = \log_2 x \implies y^2 - 4y + 3 = 0 \implies y = 1$ ou $y = 3$. 2. $\log_2 x = 1 \implies x_1 = 2$; $\log_2 x = 3 \implies x_2 = 8$. 3. Produto $2 \cdot 8 = 16$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Substitua $y = \log_2 x$ e ache as soluções de $x$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine o valor de $x$ que satisfaz $\log_{10} (x + 9) - \log_{10} x = 1$.",
        "alternativas": [],
        "resposta_correta": "1",
        "resolucao_passo_a_passo": r"1. C.E.: $x > 0$. 2. $\log_{10} \frac{x+9}{x} = 1 \implies \frac{x+9}{x} = 10 \implies x + 9 = 10x \implies 9x = 9 \implies x = 1$.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Junte a diferença em quociente: $\log((x+9)/x) = 1$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantas soluções inteiras possui a inequação $\log_2 (x - 3) \le 3$?",
        "alternativas": [
            {"letra": "A", "texto": r"$8$ soluções inteiras", "correta": True},
            {"letra": "B", "texto": r"$7$ soluções inteiras", "correta": False},
            {"letra": "C", "texto": r"$9$ soluções inteiras", "correta": False},
            {"letra": "D", "texto": r"$5$ soluções inteiras", "correta": False},
            {"letra": "E", "texto": r"Infinitas soluções", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. C.E.: $x - 3 > 0 \implies x > 3$. 2. $x - 3 \le 2^3 = 8 \implies x \le 11$. 3. $3 < x \le 11$. Os inteiros são $\{4, 5, 6, 7, 8, 9, 10, 11\}$ — total 8. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Conte os inteiros estritamente maiores que 3 e menores ou iguais a 11."},
    },
]
