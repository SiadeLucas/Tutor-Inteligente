"""
Módulo Canônico de Dados Didáticos — Volume 1: Conjuntos e Funções
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (8 caps), FIXACAO_DATA (24 questões), RAG_DATA (10 fragmentos), TRI_DATA (40 itens).
"""

VOLUME_INFO = {
    "numero": 1,
    "titulo": "Conjuntos e Funções",
    "grande_area": "algebra_funcoes",
    "ordem": 1,
    "capitulos": [
        {"num": 1, "titulo": "Noções de Lógica e Proposições", "tempo": 50},
        {"num": 2, "titulo": "Conjuntos e Operações Fundamentais", "tempo": 50},
        {"num": 3, "titulo": "Relações Binárias e Pares Ordenados", "tempo": 50},
        {"num": 4, "titulo": "Conceito Geral de Função e Gráficos", "tempo": 50},
        {"num": 5, "titulo": "Função Afim (1º Grau) e Variação", "tempo": 50},
        {"num": 6, "titulo": "Função Quadrática (2º Grau) e Vértice da Parábola", "tempo": 50},
        {"num": 7, "titulo": "Função Modular e Equações", "tempo": 50},
        {"num": 8, "titulo": "Função Inversa e Composição", "tempo": 50},
    ],
}

AULAS_DATA = {
    1: {
        "teoria": r"""# Noções de Lógica e Proposições

A lógica matemática estabelece as regras formais do raciocínio dedutivo, fundamentando toda a teoria dos conjuntos e funções desenvolvida por Gelson Iezzi.

### 1. Proposição e Princípios Fundamentais
Uma **proposição** é toda oração declarativa que exprime um pensamento de sentido completo e à qual se pode atribuir um, e somente um, valor lógico: **Verdadeiro ($V$)** ou **Falso ($F$)**.

Toda a lógica clássica se baseia em dois axiomas pétreos:
1. **Princípio do Terceiro Excluído**: Toda proposição ou é verdadeira ou é falsa; não há terceiro caso.
$$\forall p, \quad (p \lor \neg p) \equiv V$$
2. **Princípio da Não-Contradição**: Nenhuma proposição pode ser simultaneamente verdadeira e falsa.
$$\forall p, \quad \neg(p \land \neg p) \equiv V$$

---

### 2. Conectivos Lógicos Fundamentais
Dadas duas proposições simples $p$ e $q$:

- **Conjunção ($p \land q$)**: É verdadeira se e somente se **ambas** forem verdadeiras.
$$v(p \land q) = V \iff v(p) = V \text{ e } v(q) = V$$

- **Disjunção Inclusiva ($p \lor q$)**: É verdadeira se ao menos uma das proposições for verdadeira.
$$v(p \lor q) = F \iff v(p) = F \text{ e } v(q) = F$$

- **Condicional ($p \to q$)**: "Se $p$, então $q$". É falsa **exclusivamente** quando o antecedente $p$ é verdadeiro e o consequente $q$ é falso ($V \to F \equiv F$).
$$p \to q \equiv \neg p \lor q$$

- **Bicondicional ($p \leftrightarrow q$)**: "Se e somente se". É verdadeira quando ambas possuem o mesmo valor lógico.
$$p \leftrightarrow q \equiv (p \to q) \land (q \to p)$$

---

### 3. Leis de De Morgan
As negações de conjunções e disjunções seguem identidades essenciais:
$$\neg(p \land q) \equiv \neg p \lor \neg q$$
$$\neg(p \lor q) \equiv \neg p \land \neg q$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Negação de uma Condicional
**Enunciado:** Determine a negação lógica formal da seguinte afirmação matemática:  
*"Se um número inteiro $n$ é par, então $n^2$ é divisível por $4$."*

**Resolução Passo a Passo:**
1. Identificamos as proposições componentes:
   - $p$: "$n$ é par"
   - $q$: "$n^2$ é divisível por $4$"
2. A afirmação tem a forma de uma condicional: $p \to q$.
3. Aplicamos a regra de equivalência da negação da condicional:
   $$\neg(p \to q) \equiv p \land \neg q$$
4. Portanto, a negação é:
   *"$n$ é par **e** $n^2$ **não** é divisível por $4$."*

---

### Exemplo 2: Tabela-Verdade e Tautologia
**Enunciado:** Demonstre que a proposição $((p \to q) \land p) \to q$ (Modus Ponens) é uma **tautologia**.

**Demonstração:**
Construímos os passos da tabela-verdade:
| $p$ | $q$ | $p \to q$ | $(p \to q) \land p$ | $((p \to q) \land p) \to q$ |
|:---:|:---:|:---------:|:-------------------:|:---------------------------:|
| $V$ | $V$ |    $V$    |         $V$         |             $V$             |
| $V$ | $F$ |    $F$    |         $F$         |             $V$             |
| $F$ | $V$ |    $V$    |         $F$         |             $V$             |
| $F$ | $F$ |    $V$    |         $F$         |             $V$             |

Como a última coluna resulta em $V$ para todas as valorações possíveis, a fórmula é uma **tautologia** comprovada.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Pegadinha Fatal da Condicional ($p \to q$):**
> O erro mais comum em provas é assumir que a negação de "Se chover, levo guarda-chuva" seria "Se chover, não levo guarda-chuva". Isso está **ERRADO**! A negação de uma condicional **NÃO é outra condicional**, e sim uma conjunção:  
> $\neg(p \to q) \equiv p \land \neg q$ ("Chove e não levo guarda-chuva").

> [!TIP]
> **Contrapositiva vs Recíproca:**
> - A condicional $p \to q$ é estritamente equivalente à sua **contrapositiva**:  
>   $$p \to q \iff \neg q \to \neg p$$
>   *Use isso frequentemente em demonstrações por absurdo na Geometria e Teoria dos Números!*
> - A **recíproca** ($q \to p$) **NÃO** é logicamente equivalente a $p \to q$.
""",
    },
    2: {
        "teoria": r"""# Conjuntos e Operações Fundamentais

A teoria dos conjuntos constitui a linguagem universal da Matemática contemporânea, servindo de base formal para o estudo de relações e funções.

### 1. Pertinência e Inclusão
- **Relação de Pertinência ($\in$)**: Vincula um **elemento** a um **conjunto**.
  $$x \in A \quad (\text{elemento } x \text{ pertence ao conjunto } A)$$
- **Relação de Inclusão ($\subset$)**: Vincula **dois conjuntos**.
  $$A \subset B \iff (\forall x, \, x \in A \implies x \in B)$$

> [!IMPORTANT]
> Nunca utilize $\in$ entre dois conjuntos a menos que um deles seja expressamente elemento do conjunto das partes!

---

### 2. Operações Fundamentais
Dados os conjuntos $A$ e $B$ em um universo $U$:

1. **União ($A \cup B$)**:
   $$A \cup B = \{x \in U \mid x \in A \lor x \in B\}$$

2. **Interseção ($A \cap B$)**:
   $$A \cap B = \{x \in U \mid x \in A \land x \in B\}$$
   Se $A \cap B = \emptyset$, dizemos que $A$ e $B$ são **disjuntos**.

3. **Diferença ($A \setminus B$ ou $A - B$)**:
   $$A - B = \{x \in U \mid x \in A \land x \notin B\}$$

4. **Complementar ($\complement_U A$)**:
   $$\complement_U A = U - A = \{x \in U \mid x \notin A\}$$

---

### 3. Princípio da Inclusão-Exclusão
Para o número de elementos de dois conjuntos finitos:
$$n(A \cup B) = n(A) + n(B) - n(A \cap B)$$
Para três conjuntos:
$$n(A \cup B \cup C) = n(A) + n(B) + n(C) - n(A \cap B) - n(A \cap C) - n(B \cap C) + n(A \cap B \cap C)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Conjunto das Partes ($\mathcal{P}(A)$)
**Enunciado:** Dado o conjunto $A = \{1, 2, 3\}$, determine $\mathcal{P}(A)$ e verifique o número de subconjuntos.

**Resolução:**
1. O conjunto das partes reúne todos os subconjuntos possíveis de $A$:
   $$\mathcal{P}(A) = \{\emptyset, \{1\}, \{2\}, \{3\}, \{1, 2\}, \{1, 3\}, \{2, 3\}, \{1, 2, 3\}\}$$
2. Pelo teorema fundamental dos subconjuntos:
   $$n(\mathcal{P}(A)) = 2^{n(A)} = 2^3 = 8 \text{ elementos}$$

---

### Exemplo 2: Aplicação do Princípio da Inclusão-Exclusão
**Enunciado:** Em uma turma de 100 alunos, 60 estudam Álgebra, 50 estudam Geometria e 20 estudam ambas as matérias. Quantos alunos não estudam nenhuma dessas matérias?

**Resolução:**
1. Seja $A$ o conjunto dos estudantes de Álgebra e $G$ de Geometria:
   $$n(A) = 60, \quad n(G) = 50, \quad n(A \cap G) = 20$$
2. Calculamos o total de estudantes que cursam ao menos uma:
   $$n(A \cup G) = n(A) + n(G) - n(A \cap G) = 60 + 50 - 20 = 90$$
3. O número de alunos fora de ambas é o complementar em relação ao universo:
   $$n(\text{Nenhum}) = 100 - n(A \cup G) = 100 - 90 = 10 \text{ alunos}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Diferença entre $\emptyset$ e $\{\emptyset\}$:**
> - $\emptyset$ é o conjunto vazio ($n(\emptyset) = 0$).
> - $\{\emptyset\}$ é um conjunto unitário cujo único elemento é o conjunto vazio ($n(\{\emptyset\}) = 1$).
> - Logo: $\emptyset \in \{\emptyset\}$ é **Verdadeiro**, e $\emptyset \subset \{\emptyset\}$ também é **Verdadeiro**!

> [!TIP]
> **Subconjuntos Próprios:**
> Se uma questão pedir o número de subconjuntos *próprios* de $A$, lembre-se de subtrair o próprio conjunto $A$:
> $$\text{Subconjuntos próprios} = 2^n - 1$$
""",
    },
    3: {
        "teoria": r"""# Relações Binárias e Pares Ordenados

O conceito de relação binária é a ponte matemática formal entre a teoria dos conjuntos puros e a definição rigorosa de funções.

### 1. Par Ordenado e Produto Cartesiano
- **Par Ordenado**: Denotado por $(a, b)$, distingue rigorosamente a primeira coordenada $a$ da segunda coordenada $b$:
  $$(a, b) = (c, d) \iff a = c \text{ e } b = d$$
- **Produto Cartesiano ($A \times B$)**: É o conjunto de todos os pares ordenados cuja primeira coordenada pertence a $A$ e a segunda a $B$:
  $$A \times B = \{(x, y) \mid x \in A \land y \in B\}$$
  $$n(A \times B) = n(A) \cdot n(B)$$

---

### 2. Definição de Relação Binária
Dados dois conjuntos $A$ e $B$, chama-se **relação binária** de $A$ em $B$ a qualquer subconjunto $R \subset A \times B$.
- **Domínio ($D(R)$)**: $\{x \in A \mid \exists y \in B, (x, y) \in R\}$.
- **Imagem ($\text{Im}(R)$)**: $\{y \in B \mid \exists x \in A, (x, y) \in R\}$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação Algébrica de Domínio e Imagem
**Enunciado:** Sejam $A = \{1, 2, 3, 4\}$ e $B = \{1, 2, 3, 4, 5, 6\}$. Seja $R = \{(x, y) \in A \times B \mid y = 2x - 1\}$. Determine os pares de $R$.

**Resolução:**
- $x = 1 \implies y = 1 \in B \implies (1, 1) \in R$
- $x = 2 \implies y = 3 \in B \implies (2, 3) \in R$
- $x = 3 \implies y = 5 \in B \implies (3, 5) \in R$
- $x = 4 \implies y = 7 \notin B \implies (4, 7) \notin R$
Logo, $R = \{(1, 1), (2, 3), (3, 5)\}$, $D(R) = \{1, 2, 3\}$, $\text{Im}(R) = \{1, 3, 5\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> $(a, b) \neq (b, a)$ se $a \neq b$. No par ordenado a ordem é posicional e fundamental.

> [!TIP]
> O número total de relações distintas de $A$ em $B$ é $2^{n(A) \cdot n(B)}$.
""",
    },
    4: {
        "teoria": r"""# Conceito Geral de Função e Gráficos

Uma relação $f: A \to B$ é dita **função** se, e somente se, para todo $x \in A$ existe um único $y \in B$ com $y = f(x)$.

### Condições Inegociáveis:
1. **Existência**: $D(f) = A$ (nenhum elemento de $A$ fica sem correspondente).
2. **Unicidade**: Cada $x$ conecta-se a um único $y$.

### Teste da Reta Vertical:
Uma curva no plano representa uma função $y = f(x)$ se nenhuma reta vertical corta a curva em mais de um ponto.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Domínio com Dupla Restrição
**Enunciado:** Determine o domínio de $f(x) = \frac{\sqrt{2x - 6}}{x - 7}$.

**Resolução:**
1. Radicando par: $2x - 6 \ge 0 \implies x \ge 3$.
2. Denominador: $x - 7 \neq 0 \implies x \neq 7$.
3. Domínio: $D(f) = [3, 7) \cup (7, +\infty)$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Contradomínio ($B$) não é necessariamente igual à Imagem ($\text{Im}(f)$). A Imagem é o subconjunto dos valores efetivamente atingidos.
""",
    },
    5: {
        "teoria": r"""# Função Afim (1º Grau) e Variação

Uma função $f: \mathbb{R} \to \mathbb{R}$ chama-se **afim** se $f(x) = ax + b$ ($a \neq 0$).
- $a$: Coeficiente angular ($a = \frac{\Delta y}{\Delta x}$). Se $a > 0$, crescente; se $a < 0$, decrescente.
- $b$: Coeficiente linear (interseção com o eixo $y$ em $(0, b)$).
- Raiz: $f(x) = 0 \iff x = -\frac{b}{a}$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação da Lei por Dois Pontos
**Enunciado:** Determine $f(x) = ax + b$ contendo $A(2, 7)$ e $B(5, 16)$.

**Resolução:**
1. $a = \frac{16 - 7}{5 - 2} = \frac{9}{3} = 3$.
2. $7 = 3(2) + b \implies b = 1$.
3. $f(x) = 3x + 1$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Uma função afim é linear se, e somente se, $b = 0$, passando pela origem $(0, 0)$.
""",
    },
    6: {
        "teoria": r"""# Função Quadrática (2º Grau) e Parábola

Uma função quadrática é dada por $f(x) = ax^2 + bx + c$ ($a \neq 0$).
- Gráfico: Parábola com vértice $V(x_v, y_v)$ onde:
  $$x_v = -\frac{b}{2a}, \quad y_v = -\frac{\Delta}{4a}$$
- Concavidade: $a > 0$ (para cima, vértice é mínimo); $a < 0$ (para baixo, vértice é máximo).
- Raízes: $x = \frac{-b \pm \sqrt{\Delta}}{2a}$, $\Delta = b^2 - 4ac$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Maximização de Lucro
**Enunciado:** $L(x) = -x^2 + 10x - 9$. Quantidade ótima e lucro máximo.

**Resolução:**
1. $x_v = -\frac{10}{2(-1)} = 5$ unidades.
2. $y_v = L(5) = -25 + 50 - 9 = 16$ mil reais.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> "Quando" o lucro é máximo refere-se a $x_v$. "Quanto" é o lucro máximo refere-se a $y_v$.
""",
    },
    7: {
        "teoria": r"""# Função Modular e Equações

O valor absoluto de $x \in \mathbb{R}$ é:
$$|x| = \begin{cases} x, & \text{se } x \ge 0 \\ -x, & \text{se } x < 0 \end{cases}$$
Propriedades: $|x| \ge 0$, $\sqrt{x^2} = |x|$, $|x \cdot y| = |x| \cdot |y|$.
Equações: $|f(x)| = k$ ($k \ge 0$) $\iff f(x) = k$ ou $f(x) = -k$.
Inequações: $|f(x)| \le a \iff -a \le f(x) \le a$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Equação Modular
**Enunciado:** Resolva $|2x - 3| = x + 1$.

**Resolução:**
1. Condição: $x + 1 \ge 0 \implies x \ge -1$.
2. $2x - 3 = x + 1 \implies x = 4$.
3. $2x - 3 = -(x + 1) \implies 3x = 2 \implies x = 2/3$.
Ambas satisfazem $x \ge -1$. $S = \{2/3, 4\}$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> Nunca esqueça da condição de existência no segundo membro algébrico de $|f(x)| = g(x)$: deve-se ter $g(x) \ge 0$.
""",
    },
    8: {
        "teoria": r"""# Função Inversa e Composição

- **Composta ($g \circ f$)**: $(g \circ f)(x) = g(f(x))$, exigindo $\text{Im}(f) \subseteq D(g)$.
- **Tipos de Função**:
  - Injetora: $x_1 \neq x_2 \implies f(x_1) \neq f(x_2)$.
  - Sobrejetora: $\text{Im}(f) = CD(f)$.
  - Bijetora: Injetora e sobrejetora simultaneamente.
- **Inversa ($f^{-1}$)**: Existe se e somente se $f$ for bijetora.
  $$f(x) = y \iff f^{-1}(y) = x$$
  Gráficos de $f$ e $f^{-1}$ são simétricos em relação à reta $y = x$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Inversa Homográfica
**Enunciado:** Determine a inversa de $f(x) = \frac{3x + 1}{x - 2}$ ($x \neq 2$).

**Resolução:**
1. $x = \frac{3y + 1}{y - 2} \implies x(y - 2) = 3y + 1$.
2. $xy - 3y = 2x + 1 \implies y(x - 3) = 2x + 1$.
3. $f^{-1}(x) = \frac{2x + 1}{x - 3}$ ($x \neq 3$).
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> $f^{-1}(x) \neq \frac{1}{f(x)}$. O expoente $-1$ indica a função inversa sob composição, não inverso multiplicativo.
""",
    },
}

FIXACAO_DATA = {
    1: [
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
    2: [
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
    3: [
        {
            "numero": 1,
            "enunciado": r"Se $A = \{1, 2, 3\}$ e $B = \{a, b\}$, quantos elementos possui o produto cartesiano $A \times B$?",
            "alternativas": [r"$5$", r"$6$", r"$8$", r"$9$"],
            "indice_correto": 1,
        },
        {
            "numero": 2,
            "enunciado": r"Seja $A = \{1, 2, 3\}$ e a relação $R = \{(x, y) \in A \times A \mid y = x + 1\}$. O conjunto imagem $\text{Im}(R)$ é:",
            "alternativas": [r"$\{1, 2\}$", r"$\{2, 3\}$", r"$\{1, 2, 3\}$", r"$\{3\}$"],
            "indice_correto": 1,
        },
        {
            "numero": 3,
            "enunciado": r"Sobre a igualdade de pares ordenados $(2x - 1, 5) = (7, y + 2)$, os valores de $x$ e $y$ são:",
            "alternativas": [
                r"$x = 4 \text{ e } y = 3$",
                r"$x = 3 \text{ e } y = 4$",
                r"$x = 4 \text{ e } y = 7$",
                r"$x = 3 \text{ e } y = 7$",
            ],
            "indice_correto": 0,
        },
    ],
    4: [
        {
            "numero": 1,
            "enunciado": r"Uma relação binária $f: A \to B$ define uma função se, e somente se:",
            "alternativas": [
                r"Todo elemento de $A$ se relaciona com pelo menos um elemento de $B$",
                r"Todo elemento de $A$ se relaciona com um único elemento de $B$",
                r"Todo elemento de $B$ recebe flecha de exatamente um elemento de $A$",
                r"O número de elementos de $A$ é igual ao de $B$",
            ],
            "indice_correto": 1,
        },
        {
            "numero": 2,
            "enunciado": r"O domínio mais amplo da função real $f(x) = \frac{\sqrt{x - 2}}{x - 6}$ em $\mathbb{R}$ é:",
            "alternativas": [
                r"$[2, +\infty[$",
                r"$[2, 6) \cup (6, +\infty)$",
                r"$]2, 6[$",
                r"$\mathbb{R} \setminus \{6\}$",
            ],
            "indice_correto": 1,
        },
        {
            "numero": 3,
            "enunciado": r"Pelo Teste da Reta Vertical no plano cartesiano, uma curva representa uma função $y = f(x)$ quando:",
            "alternativas": [
                r"Toda reta horizontal corta a curva no máximo uma vez",
                r"Toda reta vertical corta a curva em no máximo um ponto",
                r"A curva intercepta ambos os eixos coordenados",
                r"A curva passa pela origem $(0, 0)$",
            ],
            "indice_correto": 1,
        },
    ],
    5: [
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
    6: [
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
    7: [
        {
            "numero": 1,
            "enunciado": r"O conjunto solução da equação modular $|3x - 6| = 9$ em $\mathbb{R}$ é:",
            "alternativas": [r"$S = \{5\}$", r"$S = \{-1, 5\}$", r"$S = \{1, 5\}$", r"$S = \{-5, 1\}$"],
            "indice_correto": 1,
        },
        {
            "numero": 2,
            "enunciado": r"A identidade matemática verdadeira para qualquer número real $x$ é:",
            "alternativas": [r"$\sqrt{x^2} = x$", r"$\sqrt{x^2} = |x|$", r"$|-x| = -x$", r"$|x|^2 = -x^2$"],
            "indice_correto": 1,
        },
        {
            "numero": 3,
            "enunciado": r"O conjunto de todos os números reais que satisfazem a inequação $|x - 4| \le 3$ é o intervalo:",
            "alternativas": [r"$[1, 7]$", r"$[-1, 7]$", r"$[1, 4]$", r"$]-\infty, 7]$"],
            "indice_correto": 0,
        },
    ],
    8: [
        {
            "numero": 1,
            "enunciado": r"Uma função real $f: A \to B$ admite função inversa $f^{-1}$ se, e somente se, $f$ for:",
            "alternativas": [
                r"Apenas injetora",
                r"Apenas sobrejetora",
                r"Bijetora (injetora e sobrejetora)",
                r"Estritamente constante",
            ],
            "indice_correto": 2,
        },
        {
            "numero": 2,
            "enunciado": r"Dada a função bijetora $f(x) = 4x - 8$, a sua inversa $f^{-1}(x)$ é:",
            "alternativas": [
                r"$f^{-1}(x) = \frac{x + 8}{4}$",
                r"$f^{-1}(x) = \frac{x - 8}{4}$",
                r"$f^{-1}(x) = 4x + 8$",
                r"$f^{-1}(x) = \frac{1}{4x - 8}$",
            ],
            "indice_correto": 0,
        },
        {
            "numero": 3,
            "enunciado": r"Dadas $f(x) = 2x + 1$ e $g(x) = x^2$, o valor da composta $(g \circ f)(2)$ vale:",
            "alternativas": [r"$9$", r"$25$", r"$17$", r"$10$"],
            "indice_correto": 1,
        },
    ],
}

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "pagina": 5,
        "teorema": "Conceito de Proposição e Princípios Fundamentais",
        "texto": (
            "Chama-se proposição ou sentença toda oração declarativa que exprime um pensamento "
            "de sentido completo e à qual se pode atribuir um, e somente um, dos dois valores lógicos: "
            "verdadeiro (V) ou falso (F). A lógica matemática clássica baseia-se em dois princípios "
            "fundamentais inegociáveis: 1) Princípio do Terceiro Excluído: toda proposição ou é verdadeira "
            "ou é falsa, não havendo outro valor lógico possível; 2) Princípio da Não-Contradição: nenhuma "
            "proposição pode ser simultaneamente verdadeira e falsa sob as mesmas condições."
        ),
    },
    {
        "numero_capitulo": 1,
        "pagina": 12,
        "teorema": "Conectivos Lógicos: Negação, Conjunção e Disjunção",
        "texto": (
            "Dadas duas proposições $p$ e $q$, os operadores fundamentais combinam seus valores lógicos: "
            "1) Negação (~p ou ¬p): inverte o valor de p. Se p é V, ~p é F; "
            "2) Conjunção (p ∧ q): proposição 'p e q' é verdadeira apenas quando ambos p e q "
            "são simultaneamente verdadeiros. Se ao menos um for falso, a conjunção é falsa; "
            "3) Disjunção inclusiva (p ∨ q): proposição 'p ou q' é verdadeira se pelo menos um dos "
            "dois componentes for verdadeiro, sendo falsa unicamente se ambos forem simultaneamente falsos."
        ),
    },
    {
        "numero_capitulo": 1,
        "pagina": 18,
        "teorema": "Condicional e Negação da Implicação",
        "texto": (
            "A condicional p → q afirma que a ocorrência de p implica necessariamente a ocorrência de q. "
            "A condicional só é FALSA no caso em que o antecedente é verdadeiro e o consequente é falso: V → F ≡ F. "
            "Crucialmente, a negação de uma condicional não é outra condicional, mas sim a conjunção do antecedente "
            "com a negação do consequente: ~(p → q) ≡ p ∧ ~q."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 32,
        "teorema": "Definição de Conjunto e Relação de Pertinência",
        "texto": (
            "Na teoria ingênua dos conjuntos, conjunto e elemento são noções primitivas aceitas sem definição formal. "
            "A relação de pertinência (x ∈ A) vincula um elemento ao conjunto. "
            "Um conjunto A é subconjunto de B se todo elemento pertencente a A também pertence a B: A ⊂ B."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 40,
        "teorema": "Operações Fundamentais com Conjuntos",
        "texto": (
            "Sejam A e B conjuntos contidos num universo U: "
            "1) União: A ∪ B; 2) Interseção: A ∩ B; 3) Diferença: A - B; 4) Complementar. "
            "As Leis de De Morgan estabelecem as negações das uniões e interseções."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 68,
        "teorema": "Definição Rigorosa de Função",
        "texto": (
            "Dados dois conjuntos não-vazios A e B, uma relação binária f de A em B é uma função se, "
            "e somente se, para TODO elemento x ∈ A existe um ÚNICO elemento y ∈ B tal que y = f(x). "
            "O conjunto A é o domínio D(f) e B é o contradomínio CD(f)."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 84,
        "teorema": "Domínio e Imagem de Funções Reais",
        "texto": (
            "Quando consideramos funções reais de variável real, subentende-se que D(f) é o maior subconjunto "
            "de R onde as operações são possíveis: denominadores não nulos e radicandos de índice par não-negativos."
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 115,
        "teorema": "Função Afim e Taxa Média de Variação",
        "texto": (
            "Uma função f: R → R chama-se afim se f(x) = ax + b (a ≠ 0). O coeficiente a é a taxa de variação "
            "constante Δy/Δx. O coeficiente b é o coeficiente linear no ponto (0, b)."
        ),
    },
    {
        "numero_capitulo": 6,
        "pagina": 150,
        "teorema": "Função Quadrática, Raízes e Vértice da Parábola",
        "texto": (
            "A função quadrática f(x) = ax² + bx + c tem como gráfico uma parábola de vértice V(-b/2a, -Δ/4a). "
            "As raízes reais são dadas pela fórmula de Bhaskara. Se a > 0 o vértice é ponto de mínimo; se a < 0, de máximo."
        ),
    },
    {
        "numero_capitulo": 7,
        "pagina": 185,
        "teorema": "Definição de Função Modular e Equações",
        "texto": (
            "Para todo número real x, |x| = x se x ≥ 0 e |x| = -x se x < 0. Vale sempre que √(x²) = |x|. "
            "Equações |f(x)| = k equivalem a f(x) = k ou f(x) = -k (para k ≥ 0)."
        ),
    },
]

TRI_DATA = [
    # --- Cap 1: Noções de Lógica e Proposições (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A negação lógica da proposição condicional $p \to q$ é logicamente equivalente a:",
        "alternativas": [
            {"letra": "A", "texto": r"$p \land \neg q$", "correta": True},
            {"letra": "B", "texto": r"$\neg p \lor q$", "correta": False},
            {"letra": "C", "texto": r"$\neg p \land \neg q$", "correta": False},
            {"letra": "D", "texto": r"$q \to p$", "correta": False},
            {"letra": "E", "texto": r"$\neg p \to \neg q$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A condicional $p \to q$ equivale a $\neg p \lor q$. 2. Pela Lei de De Morgan: $\neg(\neg p \lor q) \equiv p \land \neg q$. 3. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A negação de 'Se P então Q' é 'P e não Q'."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Considere $p$: 'O número $7$ é primo' e $q$: 'O número $8$ é ímpar'. Os valores lógicos de $p \land q$ e $p \lor q$ são respectivamente:",
        "alternativas": [
            {"letra": "A", "texto": r"$F$ e $V$", "correta": True},
            {"letra": "B", "texto": r"$V$ e $F$", "correta": False},
            {"letra": "C", "texto": r"$V$ e $V$", "correta": False},
            {"letra": "D", "texto": r"$F$ e $F$", "correta": False},
            {"letra": "E", "texto": r"Indeterminado", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $v(p) = V$ e $v(q) = F$. 2. $V \land F = F$. 3. $V \lor F = V$. 4. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A conjunção exige ambas V; a disjunção inclusiva basta uma V."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A contrapositiva da condicional 'Se chove, então a rua fica molhada' ($p \to q$) é:",
        "alternativas": [
            {"letra": "A", "texto": r"Se a rua não fica molhada, então não chove", "correta": True},
            {"letra": "B", "texto": r"Se não chove, então a rua não fica molhada", "correta": False},
            {"letra": "C", "texto": r"Se a rua fica molhada, então chove", "correta": False},
            {"letra": "D", "texto": r"Chove e a rua não fica molhada", "correta": False},
            {"letra": "E", "texto": r"Não chove ou a rua não fica molhada", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A contrapositiva de $p \to q$ é $\neg q \to \neg p$. 2. 'Se a rua não fica molhada, então não chove'. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Inverta a ordem e negue ambas as proposições."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantas linhas possui a tabela-verdade completa associada a uma proposição com $4$ variáveis simples independentes?",
        "alternativas": [
            {"letra": "A", "texto": r"$16$", "correta": True},
            {"letra": "B", "texto": r"$8$", "correta": False},
            {"letra": "C", "texto": r"$4$", "correta": False},
            {"letra": "D", "texto": r"$32$", "correta": False},
            {"letra": "E", "texto": r"$64$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O número de linhas com $n$ proposições é $2^n$. 2. $2^4 = 16$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Aplique $2^n$ para $n=4$ variáveis independentes."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A negação da disjunção inclusiva $\neg(p \lor q)$ pelas Leis de De Morgan é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\neg p \land \neg q$", "correta": True},
            {"letra": "B", "texto": r"$\neg p \lor \neg q$", "correta": False},
            {"letra": "C", "texto": r"$p \land q$", "correta": False},
            {"letra": "D", "texto": r"$\neg p \to q$", "correta": False},
            {"letra": "E", "texto": r"$p \lor \neg q$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Primeira Lei de De Morgan: $\neg(p \lor q) \equiv \neg p \land \neg q$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Negue ambas as proposições e troque o conectivo OU pelo E."},
    },

    # --- Cap 2: Conjuntos e Operações Fundamentais (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sejam $A = \{1, 2, 3, 4, 5\}$ e $B = \{3, 4, 5, 6, 7\}$. O número de elementos de $(A \cup B) - (A \cap B)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$4$", "correta": True},
            {"letra": "B", "texto": r"$7$", "correta": False},
            {"letra": "C", "texto": r"$3$", "correta": False},
            {"letra": "D", "texto": r"$2$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A \cup B = \{1, 2, 3, 4, 5, 6, 7\}$. 2. $A \cap B = \{3, 4, 5\}$. 3. Diferença = $\{1, 2, 6, 7\}$, 4 elementos. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Diferença simétrica reúne elementos que pertencem exclusivamente a um dos conjuntos."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dado o conjunto $A = \{a, b, c, d, e\}$, o total de subconjuntos de $\mathcal{P}(A)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$32$", "correta": True},
            {"letra": "B", "texto": r"$16$", "correta": False},
            {"letra": "C", "texto": r"$25$", "correta": False},
            {"letra": "D", "texto": r"$10$", "correta": False},
            {"letra": "E", "texto": r"$64$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $n(\mathcal{P}(A)) = 2^n = 2^5 = 32$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Subconjuntos das partes é $2^n$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Num grupo de $100$ alunos, $65$ gostam de Matemática, $45$ de Física e $20$ de ambas. Quantos não gostam de nenhuma?",
        "alternativas": [
            {"letra": "A", "texto": r"$10$", "correta": True},
            {"letra": "B", "texto": r"$20$", "correta": False},
            {"letra": "C", "texto": r"$15$", "correta": False},
            {"letra": "D", "texto": r"$30$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $n(M \cup F) = 65 + 45 - 20 = 90$. 2. Nenhum = $100 - 90 = 10$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Inclusão-Exclusão: $n(A \cup B) = n(A) + n(B) - n(A \cap B)$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sejam os intervalos $A = [-3, 4[$ e $B = [1, 7]$. A interseção $A \cap B$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$[1, 4[$", "correta": True},
            {"letra": "B", "texto": r"$[-3, 7]$", "correta": False},
            {"letra": "C", "texto": r"$]1, 4]$", "correta": False},
            {"letra": "D", "texto": r"$[1, 7]$", "correta": False},
            {"letra": "E", "texto": r"$]-3, 1[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Faixa comum: $\max(-3, 1) = 1$ (fechado) e $\min(4, 7) = 4$ (aberto). 2. $[1, 4[$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Verifique a pertinência das extremidades na reta real."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos subconjuntos próprios possui um conjunto com $6$ elementos?",
        "alternativas": [
            {"letra": "A", "texto": r"$63$", "correta": True},
            {"letra": "B", "texto": r"$64$", "correta": False},
            {"letra": "C", "texto": r"$32$", "correta": False},
            {"letra": "D", "texto": r"$31$", "correta": False},
            {"letra": "E", "texto": r"$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Subconjuntos totais = $2^6 = 64$. 2. Subconjuntos próprios = $2^n - 1 = 64 - 1 = 63$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Subconjuntos próprios excluem o próprio conjunto."},
    },

    # --- Cap 3: Relações Binárias e Pares Ordenados (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sejam $A = \{1, 2, 3\}$ e $B = \{2, 4\}$. O total de pares do produto cartesiano $A \times B$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": False},
            {"letra": "B", "texto": r"$6$", "correta": True},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$9$", "correta": False},
            {"letra": "E", "texto": r"$4$", "correta": False},
        ],
        "resposta_correta": "B",
        "resolucao_passo_a_passo": r"1. $n(A \times B) = n(A) \cdot n(B) = 3 \cdot 2 = 6$. Alternativa B.",
        "parametro_a": 1.100,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique as cardinalidades dos conjuntos."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dada a igualdade $(3x - 5, 8) = (7, 2y + 4)$, os valores reais de $x$ e $y$ valem respectivamente:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 4 \text{ e } y = 2$", "correta": True},
            {"letra": "B", "texto": r"$x = 2 \text{ e } y = 4$", "correta": False},
            {"letra": "C", "texto": r"$x = 4 \text{ e } y = 6$", "correta": False},
            {"letra": "D", "texto": r"$x = -4 \text{ e } y = 2$", "correta": False},
            {"letra": "E", "texto": r"$x = 12 \text{ e } y = 4$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3x - 5 = 7 \implies 3x = 12 \implies x = 4$. 2. $2y + 4 = 8 \implies 2y = 4 \implies y = 2$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Iguale as primeiras coordenadas e depois as segundas."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $A = \{1, 2, 3, 4, 5\}$ e $R = \{(x, y) \in A \times A \mid y = 2x - 1\}$. A quantidade de pares de $R$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$1$", "correta": False},
            {"letra": "B", "texto": r"$2$", "correta": False},
            {"letra": "C", "texto": r"$3$", "correta": True},
            {"letra": "D", "texto": r"$4$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "C",
        "resolucao_passo_a_passo": r"1. $(1,1), (2,3), (3,5)$ estão em $A \times A$. Para $x \ge 4$, $y \ge 7 \notin A$. Total 3 pares. Alternativa C.",
        "parametro_a": 1.300,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Verifique se o $y$ calculado pertence ao conjunto $A$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Sejam os intervalos $A = [2, 6]$ e $B = [1, 5]$. A área da região retangular plana formada pelo produto cartesiano $A \times B$ vale:",
        "alternativas": [],
        "resposta_correta": "16",
        "resolucao_passo_a_passo": r"1. $\Delta x = 6 - 2 = 4$. 2. $\Delta y = 5 - 1 = 4$. 3. Área = $4 \times 4 = 16$.",
        "parametro_a": 1.400,
        "parametro_b": 0.800,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique os comprimentos dos dois intervalos."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $A = \{1, 2\}$ e $B = \{3, 4, 5\}$, o número total de relações binárias possíveis de $A$ em $B$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$64$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$32$", "correta": False},
            {"letra": "D", "texto": r"$12$", "correta": False},
            {"letra": "E", "texto": r"$128$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $n(A \times B) = 2 \times 3 = 6$. 2. Total de relações = $2^{n(A \times B)} = 2^6 = 64$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Qualquer subconjunto do produto cartesiano é uma relação: $2^{n(A \times B)}$."},
    },

    # --- Cap 4: Conceito Geral de Função e Gráficos (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O domínio da função real $f(x) = \frac{7}{x - 4}$ em $\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$D(f) = \mathbb{R} \setminus \{4\}$", "correta": True},
            {"letra": "B", "texto": r"$D(f) = \mathbb{R} \setminus \{0\}$", "correta": False},
            {"letra": "C", "texto": r"$D(f) = [4, +\infty[$", "correta": False},
            {"letra": "D", "texto": r"$D(f) = \mathbb{R}$", "correta": False},
            {"letra": "E", "texto": r"$D(f) = \{4\}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Denominador não nulo: $x - 4 \neq 0 \implies x \neq 4$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "O denominador de uma fração não pode ser zero."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o domínio da função real $f(x) = \sqrt{3x - 12}$ em $\mathbb{R}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$D(f) = [4, +\infty[$", "correta": True},
            {"letra": "B", "texto": r"$D(f) = ]4, +\infty[$", "correta": False},
            {"letra": "C", "texto": r"$D(f) = ]-\infty, 4]$", "correta": False},
            {"letra": "D", "texto": r"$D(f) = \mathbb{R} \setminus \{4\}$", "correta": False},
            {"letra": "E", "texto": r"$D(f) = [12, +\infty[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3x - 12 \ge 0 \implies 3x \ge 12 \implies x \ge 4$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Radicando de raiz quadrada deve ser maior ou igual a zero."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $f: \mathbb{R} \to \mathbb{R}$ dada por $f(x) = 2x + 1$ e $g(x) = x^2$. O valor de $(f \circ g)(3)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$19$", "correta": True},
            {"letra": "B", "texto": r"$49$", "correta": False},
            {"letra": "C", "texto": r"$7$", "correta": False},
            {"letra": "D", "texto": r"$18$", "correta": False},
            {"letra": "E", "texto": r"$37$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $g(3) = 3^2 = 9$. 2. $f(9) = 2(9) + 1 = 19$. Alternativa A.",
        "parametro_a": 1.600,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule primeiro $g(3)$ e aplique o resultado em $f$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Pelo Teste da Reta Vertical, uma relação $y = f(x)$ é função quando:",
        "alternativas": [
            {"letra": "A", "texto": r"Nenhuma reta vertical intersecta o gráfico mais de uma vez", "correta": True},
            {"letra": "B", "texto": r"Toda reta horizontal corta o gráfico exatamente uma vez", "correta": False},
            {"letra": "C", "texto": r"O gráfico cruza a origem $(0, 0)$", "correta": False},
            {"letra": "D", "texto": r"O gráfico é uma reta inclinada", "correta": False},
            {"letra": "E", "texto": r"A imagem é igual aos reais", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cada $x$ deve ter no máximo um $y$, logo nenhuma reta vertical pode cruzar mais de uma vez. Alternativa A.",
        "parametro_a": 1.100,
        "parametro_b": -1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A reta vertical fixa o valor de $x$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o domínio da função real $f(x) = \frac{1}{\sqrt{x - 5}}$ em $\mathbb{R}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$]5, +\infty[$", "correta": True},
            {"letra": "B", "texto": r"$[5, +\infty[$", "correta": False},
            {"letra": "C", "texto": r"$\mathbb{R} \setminus \{5\}$", "correta": False},
            {"letra": "D", "texto": r"$]-\infty, 5[$", "correta": False},
            {"letra": "E", "texto": r"$[0, +\infty[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Como o radical está no denominador, deve ser estritamente positivo: $x - 5 > 0 \implies x > 5$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Denominador não pode ser nulo, logo use $> 0$ em vez de $\ge 0$."},
    },

    # --- Cap 5: Função Afim (1º Grau) e Variação (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $f(x) = 3x - 12$. O zero (raiz) da função afim é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 4$", "correta": True},
            {"letra": "B", "texto": r"$x = -4$", "correta": False},
            {"letra": "C", "texto": r"$x = 12$", "correta": False},
            {"letra": "D", "texto": r"$x = 3$", "correta": False},
            {"letra": "E", "texto": r"$x = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $3x - 12 = 0 \implies 3x = 12 \implies x = 4$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Faça $f(x) = 0$ e isole $x$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma reta passa por $A(1, 3)$ e $B(3, 7)$. O coeficiente angular $m$ dessa reta é:",
        "alternativas": [
            {"letra": "A", "texto": r"$m = 1$", "correta": False},
            {"letra": "B", "texto": r"$m = 2$", "correta": True},
            {"letra": "C", "texto": r"$m = 3$", "correta": False},
            {"letra": "D", "texto": r"$m = 4$", "correta": False},
            {"letra": "E", "texto": r"$m = 1/2$", "correta": False},
        ],
        "resposta_correta": "B",
        "resolucao_passo_a_passo": r"1. $m = \frac{7 - 3}{3 - 1} = \frac{4}{2} = 2$. Alternativa B.",
        "parametro_a": 1.100,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use $\Delta y / \Delta x$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para quais valores reais de $x$ temos a inequação produto $(2x - 5)(-x + 4) \ge 0$ satisfeita?",
        "alternativas": [
            {"letra": "A", "texto": r"$5/2 \le x \le 4$", "correta": True},
            {"letra": "B", "texto": r"$x \le 5/2 \text{ ou } x \ge 4$", "correta": False},
            {"letra": "C", "texto": r"$-4 \le x \le 5/2$", "correta": False},
            {"letra": "D", "texto": r"$\mathbb{R}$", "correta": False},
            {"letra": "E", "texto": r"$\emptyset$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Raízes: $5/2$ e $4$. Coeficiente quadrático $a = -2 < 0$. O produto é positivo entre as raízes: $[5/2, 4]$. Alternativa A.",
        "parametro_a": 1.700,
        "parametro_b": 1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Faça o estudo do sinal do produto dos dois fatores lineares."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A função $f(x) = -4x + 12$ é estritamente decrescente porque:",
        "alternativas": [
            {"letra": "A", "texto": r"O coeficiente angular é negativo ($a = -4 < 0$)", "correta": True},
            {"letra": "B", "texto": r"O coeficiente linear é positivo ($b = 12 > 0$)", "correta": False},
            {"letra": "C", "texto": r"A sua raiz é positiva ($x = 3$)", "correta": False},
            {"letra": "D", "texto": r"Ela não passa pela origem", "correta": False},
            {"letra": "E", "texto": r"O discriminante é menor que zero", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O crescimento de uma função afim depende exclusivamente do sinal do coeficiente angular $a$. Como $a = -4 < 0$, é decrescente. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "O sinal de $a$ define se a reta sobe ou desce."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um plano de telefonia cobra taxa fixa de $R\$\,30{,}00$ mais $R\$\,0{,}50$ por minuto. Qual o valor total em reais para $80$ minutos de ligação?",
        "alternativas": [],
        "resposta_correta": "70",
        "resolucao_passo_a_passo": r"1. $C(x) = 0{,}50x + 30$. 2. $C(80) = 0{,}50(80) + 30 = 40 + 30 = 70$.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Multiplique os minutos pelo custo por minuto e some a taxa fixa."},
    },

    # --- Cap 6: Função Quadrática (2º Grau) e Parábola (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dada a função quadrática $f(x) = x^2 - 6x + 8$, as coordenadas do vértice $V(x_v, y_v)$ são:",
        "alternativas": [
            {"letra": "A", "texto": r"$V(3, -1)$", "correta": True},
            {"letra": "B", "texto": r"$V(3, 1)$", "correta": False},
            {"letra": "C", "texto": r"$V(-3, -1)$", "correta": False},
            {"letra": "D", "texto": r"$V(6, 8)$", "correta": False},
            {"letra": "E", "texto": r"$V(2, 4)$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x_v = -(-6)/2 = 3$. 2. $y_v = 3^2 - 6(3) + 8 = 9 - 18 + 8 = -1$. Vértice $(3, -1)$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use $x_v = -b/(2a)$ e calcule $f(x_v)$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o valor máximo assumido pela função real $g(x) = -2x^2 + 8x - 3$?",
        "alternativas": [
            {"letra": "A", "texto": r"$g_{\max} = 5$", "correta": True},
            {"letra": "B", "texto": r"$g_{\max} = 2$", "correta": False},
            {"letra": "C", "texto": r"$g_{\max} = 8$", "correta": False},
            {"letra": "D", "texto": r"$g_{\max} = -3$", "correta": False},
            {"letra": "E", "texto": r"$g_{\max} = 10$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x_v = -8/(2(-2)) = 2$. 2. $g(2) = -2(4) + 8(2) - 3 = -8 + 16 - 3 = 5$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Para $a < 0$, o valor máximo é $y_v = g(x_v)$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine a soma das raízes da equação quadrática $2x^2 - 10x + 12 = 0$.",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": r"1. Pelas relações de Girard: $S = -b/a = -(-10)/2 = 5$.",
        "parametro_a": 1.300,
        "parametro_b": 0.200,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_funcoes", "dica_estagio_2": "Soma de Girard: $S = -b/a$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para quais valores reais de $k$ a equação $x^2 - 2(k - 1)x + (k^2 - 2k) = 0$ tem duas raízes reais e distintas?",
        "alternativas": [
            {"letra": "A", "texto": r"Para todo $k \in \mathbb{R}$", "correta": True},
            {"letra": "B", "texto": r"$k > 1$", "correta": False},
            {"letra": "C", "texto": r"$k < 0$", "correta": False},
            {"letra": "D", "texto": r"$k = 2$", "correta": False},
            {"letra": "E", "texto": r"Nenhum valor real de $k$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\Delta = [-2(k-1)]^2 - 4(k^2 - 2k) = 4(k^2 - 2k + 1) - 4k^2 + 8k = 4 > 0$ para todo $k$. Alternativa A.",
        "parametro_a": 1.800,
        "parametro_b": 1.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule $\Delta$ e observe que os termos com $k$ se cancelam."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o conjunto imagem da função real $f(x) = x^2 - 4x + 7$?",
        "alternativas": [
            {"letra": "A", "texto": r"$[3, +\infty[$", "correta": True},
            {"letra": "B", "texto": r"$]-\infty, 3]$", "correta": False},
            {"letra": "C", "texto": r"$[7, +\infty[$", "correta": False},
            {"letra": "D", "texto": r"$\mathbb{R}$", "correta": False},
            {"letra": "E", "texto": r"$[2, +\infty[$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a = 1 > 0$ (mínimo). $x_v = 4/2 = 2$. $y_v = 4 - 8 + 7 = 3$. Logo $\text{Im}(f) = [3, +\infty[$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "A imagem de uma parábola voltada para cima é $[y_v, +\infty[$."},
    },

    # --- Cap 7: Função Modular e Equações (5 itens) ---
    {
        "numero_capitulo": 7,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O conjunto solução da equação modular $|2x - 6| = 8$ em $\mathbb{R}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$S = \{-1, 7\}$", "correta": True},
            {"letra": "B", "texto": r"$S = \{1, 7\}$", "correta": False},
            {"letra": "C", "texto": r"$S = \{-7, 1\}$", "correta": False},
            {"letra": "D", "texto": r"$S = \{7\}$", "correta": False},
            {"letra": "E", "texto": r"$S = \emptyset$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $2x - 6 = 8 \implies x = 7$. 2. $2x - 6 = -8 \implies x = -1$. $S = \{-1, 7\}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Abra nos casos positivo e negativo: $2x-6 = 8$ e $2x-6 = -8$."},
    },
    {
        "numero_capitulo": 7,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o conjunto solução da inequação modular $|x - 5| \le 3$ em $\mathbb{R}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$S = [2, 8]$", "correta": True},
            {"letra": "B", "texto": r"$S = ]-\infty, 2] \cup [8, +\infty[$", "correta": False},
            {"letra": "C", "texto": r"$S = [3, 5]$", "correta": False},
            {"letra": "D", "texto": r"$S = [-2, 8]$", "correta": False},
            {"letra": "E", "texto": r"$S = [0, 8]$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $-3 \le x - 5 \le 3 \implies 2 \le x \le 8$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Use a vizinhança: $-3 \le x - 5 \le 3$ e some 5."},
    },
    {
        "numero_capitulo": 7,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Calcule o valor numérico de $E = |-9 + 4| - |-6| + |3 \cdot (-2)|$:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$-5$", "correta": False},
            {"letra": "C", "texto": r"$17$", "correta": False},
            {"letra": "D", "texto": r"$1$", "correta": False},
            {"letra": "E", "texto": r"$-7$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $|-5| = 5$. 2. $|-6| = 6$. 3. $|-6| = 6$. 4. $E = 5 - 6 + 6 = 5$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Calcule cada termo modular individualmente."},
    },
    {
        "numero_capitulo": 7,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantas raízes reais distintas possui a equação $|x^2 - 5| = 4$?",
        "alternativas": [
            {"letra": "A", "texto": r"$4$ raízes distintas", "correta": True},
            {"letra": "B", "texto": r"$2$ raízes distintas", "correta": False},
            {"letra": "C", "texto": r"$3$ raízes distintas", "correta": False},
            {"letra": "D", "texto": r"$1$ raiz", "correta": False},
            {"letra": "E", "texto": r"Nenhuma raiz real", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x^2 - 5 = 4 \implies x^2 = 9 \implies x = \pm 3$. 2. $x^2 - 5 = -4 \implies x^2 = 1 \implies x = \pm 1$. Total 4 raízes. Alternativa A.",
        "parametro_a": 1.600,
        "parametro_b": 1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Abra em $x^2 - 5 = 4$ e $x^2 - 5 = -4$."},
    },
    {
        "numero_capitulo": 7,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A inequação modular $|2x - 1| > 5$ tem como conjunto solução:",
        "alternativas": [
            {"letra": "A", "texto": r"$]-\infty, -2[ \cup ]3, +\infty[$", "correta": True},
            {"letra": "B", "texto": r"$]-2, 3[$", "correta": False},
            {"letra": "C", "texto": r"$[3, +\infty[$", "correta": False},
            {"letra": "D", "texto": r"$]-\infty, -2]$", "correta": False},
            {"letra": "E", "texto": r"$\mathbb{R}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $2x - 1 > 5 \implies 2x > 6 \implies x > 3$. 2. $2x - 1 < -5 \implies 2x < -4 \implies x < -2$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Inequação com maior abre em OU: $u > a$ ou $u < -a$."},
    },

    # --- Cap 8: Função Inversa e Composição (5 itens) ---
    {
        "numero_capitulo": 8,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A lei da função inversa $f^{-1}(x)$ da função bijetora $f(x) = 5x - 3$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$f^{-1}(x) = \frac{x + 3}{5}$", "correta": True},
            {"letra": "B", "texto": r"$f^{-1}(x) = \frac{x - 3}{5}$", "correta": False},
            {"letra": "C", "texto": r"$f^{-1}(x) = 5x + 3$", "correta": False},
            {"letra": "D", "texto": r"$f^{-1}(x) = \frac{5}{x + 3}$", "correta": False},
            {"letra": "E", "texto": r"$f^{-1}(x) = 3x - 5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $x = 5y - 3 \implies 5y = x + 3 \implies y = (x + 3)/5$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Troque $x$ por $y$ e isole $y$."},
    },
    {
        "numero_capitulo": 8,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dadas $f(x) = 3x + 2$ e $g(x) = 2x - 1$, a lei de $(f \circ g)(x)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6x - 1$", "correta": True},
            {"letra": "B", "texto": r"$6x + 3$", "correta": False},
            {"letra": "C", "texto": r"$6x + 1$", "correta": False},
            {"letra": "D", "texto": r"$5x + 1$", "correta": False},
            {"letra": "E", "texto": r"$6x - 2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f(g(x)) = 3(2x - 1) + 2 = 6x - 3 + 2 = 6x - 1$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Substitua a expressão de $g(x)$ na variável de $f(x)$."},
    },
    {
        "numero_capitulo": 8,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja a função bijetora $f(x) = \frac{6}{x}$ ($x \neq 0$). O valor de $f^{-1}(2)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3$", "correta": True},
            {"letra": "B", "texto": r"$1/3$", "correta": False},
            {"letra": "C", "texto": r"$12$", "correta": False},
            {"letra": "D", "texto": r"$6$", "correta": False},
            {"letra": "E", "texto": r"$1/2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $f(k) = 2 \implies 6/k = 2 \implies k = 3$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Encontre qual valor de $x$ resulta em $2$."},
    },
    {
        "numero_capitulo": 8,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dadas $f(x) = x^2 + 3$ e $g(x) = \sqrt{x - 1}$ ($x \ge 1$), a lei simplificada de $(f \circ g)(x)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$x + 2$", "correta": True},
            {"letra": "B", "texto": r"$x + 4$", "correta": False},
            {"letra": "C", "texto": r"$x^2 + 2$", "correta": False},
            {"letra": "D", "texto": r"$\sqrt{x^2 + 2}$", "correta": False},
            {"letra": "E", "texto": r"$x - 2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $(\sqrt{x-1})^2 + 3 = x - 1 + 3 = x + 2$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Eleve a raiz ao quadrado e some a constante."},
    },
    {
        "numero_capitulo": 8,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se os gráficos de $f$ e sua inversa $f^{-1}$ se intersectam na reta $y = x$ no ponto $(a, b)$, então necessariamente:",
        "alternativas": [
            {"letra": "A", "texto": r"$a = b$", "correta": True},
            {"letra": "B", "texto": r"$a = -b$", "correta": False},
            {"letra": "C", "texto": r"$a \cdot b = 1$", "correta": False},
            {"letra": "D", "texto": r"$a = 0$", "correta": False},
            {"letra": "E", "texto": r"$b = 1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A reta bissetriz dos quadrantes ímpares é definida pela equação $y = x$. Todo ponto sobre ela satisfaz $a = b$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_funcoes", "dica_estagio_2": "Os pontos na reta $y=x$ possuem abscissa igual à ordenada."},
    },
]
