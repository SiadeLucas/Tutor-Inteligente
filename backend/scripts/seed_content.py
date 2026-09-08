"""
Script de População Canônica de Conteúdo Didático — Tutor Inteligente
Popula a disciplina de Matemática, os 11 volumes da Coleção Iezzi,
todos os capítulos canônicos e aulas ricas em KaTeX para o Volume 1.
"""
import asyncio
import uuid
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.content import Disciplina, VolumeDidatico, Capitulo, Aula


VOLUMES_DATA = [
    {
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
    },
    {
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
    },
    {
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
    },
    {
        "numero": 4,
        "titulo": "Sequências, Matrizes, Determinantes e Sistemas",
        "grande_area": "algebra_linear",
        "ordem": 4,
        "capitulos": [
            {"num": 1, "titulo": "Sequências Numéricas e Lei de Formação", "tempo": 50},
            {"num": 2, "titulo": "Progressão Aritmética (PA)", "tempo": 50},
            {"num": 3, "titulo": "Progressão Geométrica (PG)", "tempo": 50},
            {"num": 4, "titulo": "Teoria das Matrizes e Álgebra Matricial", "tempo": 50},
            {"num": 5, "titulo": "Determinantes e Teorema de Laplace", "tempo": 50},
            {"num": 6, "titulo": "Sistemas Lineares e Escalonamento Gaussiano", "tempo": 50},
        ],
    },
    {
        "numero": 5,
        "titulo": "Combinatória e Probabilidade",
        "grande_area": "aplicada",
        "ordem": 5,
        "capitulos": [
            {"num": 1, "titulo": "Princípio Fundamental da Contagem (PFC)", "tempo": 50},
            {"num": 2, "titulo": "Arranjos e Permutações Simples e com Repetição", "tempo": 50},
            {"num": 3, "titulo": "Combinações Simples e Problemas de Escolha", "tempo": 50},
            {"num": 4, "titulo": "Binômio de Newton e Triângulo de Pascal", "tempo": 50},
            {"num": 5, "titulo": "Conceito de Probabilidade e Espaço Amostral", "tempo": 50},
            {"num": 6, "titulo": "Probabilidade Condicional e Eventos Independentes", "tempo": 50},
        ],
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
        "numero": 11,
        "titulo": "Matemática Financeira e Estatística Descritiva",
        "grande_area": "aplicada",
        "ordem": 11,
        "capitulos": [
            {"num": 1, "titulo": "Razão, Proporção e Grandezas Proporcionais", "tempo": 50},
            {"num": 2, "titulo": "Porcentagem, Lucro e Prejuízo Comercial", "tempo": 50},
            {"num": 3, "titulo": "Regime de Juros Simples e Compostos", "tempo": 50},
            {"num": 4, "titulo": "Fluxos de Caixa e Equivalência de Capitais", "tempo": 50},
            {"num": 5, "titulo": "Estatística Descritiva: Tabelas, Média, Mediana e Moda", "tempo": 50},
            {"num": 6, "titulo": "Medidas de Dispersão: Variância e Desvio Padrão", "tempo": 50},
        ],
    },
]


# ============================================================================
# Conteúdo Didático Completo para Aulas do Volume 1 (Conjuntos e Funções)
# ============================================================================

AULAS_VOLUME_1 = {
    1: {  # Capítulo 1: Noções de Lógica e Proposições
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
    2: {  # Capítulo 2: Conjuntos e Operações Fundamentais
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
    5: {  # Capítulo 5: Função Afim (1º Grau)
        "teoria": r"""# Função Afim (1º Grau) e Variação Linear

A função afim é o modelo matemático canônico para fenômenos com taxa de variação constante.

### 1. Definição Formal
Uma função $f: \mathbb{R} \to \mathbb{R}$ chama-se **função afim** quando existem constantes reais $a, b \in \mathbb{R}$ (com $a \neq 0$) tais que:
$$f(x) = ax + b$$

- $a$: **Coeficiente angular** ou **taxa de variação** da função:
  $$a = \frac{\Delta y}{\Delta x} = \frac{f(x_2) - f(x_1)}{x_2 - x_1}$$
- $b$: **Coeficiente linear**, correspondente à ordenada do ponto onde o gráfico intercepta o eixo $y$ no par ordenado $(0, b)$.

---

### 2. Classificação quanto ao Crescimento
O sinal do coeficiente angular $a$ determina a monotonicidade:
- Se $a > 0$: Função **estritamente crescente**.
  $$\forall x_1 < x_2 \implies f(x_1) < f(x_2)$$
- Se $a < 0$: Função **estritamente decrescente**.
  $$\forall x_1 < x_2 \implies f(x_1) > f(x_2)$$

---

### 3. Raiz ou Zero da Função Afim
A raiz de $f(x) = ax + b$ é o valor de $x$ para o qual $f(x) = 0$:
$$ax + b = 0 \iff x = -\frac{b}{a}$$
Geometricamente, representa o ponto $(-\frac{b}{a}, 0)$ onde a reta corta o eixo das abscissas ($x$).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação da Lei da Função Afim por Dois Pontos
**Enunciado:** Determine a lei da função afim $f(x) = ax + b$ cujo gráfico cartesiano contém os pontos $A(2, 7)$ e $B(5, 16)$.

**Resolução:**
1. Calculamos primeiro o coeficiente angular $a$:
   $$a = \frac{y_2 - y_1}{x_2 - x_1} = \frac{16 - 7}{5 - 2} = \frac{9}{3} = 3$$
2. Substituímos $a = 3$ e as coordenadas do ponto $A(2, 7)$ na equação fundamental:
   $$f(x) = 3x + b \implies 7 = 3(2) + b \implies 7 = 6 + b \implies b = 1$$
3. Portanto, a lei procurada é:
   $$f(x) = 3x + 1$$

---

### Exemplo 2: Estudo dos Sinais de $f(x) = ax + b$
**Enunciado:** Faça o estudo dos sinais da função $f(x) = -2x + 6$.

**Resolução:**
1. Encontramos a raiz da função:
   $$-2x + 6 = 0 \implies -2x = -6 \implies x = 3$$
2. Analisamos o coeficiente angular: $a = -2 < 0$ (função decrescente).
3. Conclusão do estudo de sinais:
   - Para $x < 3$: $f(x) > 0$ (positivo)
   - Para $x = 3$: $f(x) = 0$ (nulo)
   - Para $x > 3$: $f(x) < 0$ (negativo)
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Função Linear vs Função Afim:**
> - Toda função afim tem a forma $f(x) = ax + b$.
> - Uma função afim é dita **linear** estritamente quando $b = 0$, ou seja, $f(x) = ax$. Neste caso, e somente neste caso, o gráfico passa pela **origem $(0, 0)$** e satisfaz a proporcionalidade direta:  
>   $$f(k \cdot x) = k \cdot f(x)$$

> [!TIP]
> **Interpretação Econômica (Custo Total):**
> Em problemas aplicados (ENEM e vestibulares):
> $$C(x) = C_{\text{variável}} \cdot x + C_{\text{fixo}}$$
> O custo fixo é sempre o coeficiente linear $b$, e o custo unitário variável é o coeficiente angular $a$.
""",
    },
    6: {  # Capítulo 6: Função Quadrática (2º Grau) e Parábola
        "teoria": r"""# Função Quadrática (2º Grau) e a Parábola

A função quadrática é a representação matemática do movimento com aceleração constante e da otimização de áreas e custos.

### 1. Definição Formal
Uma função $f: \mathbb{R} \to \mathbb{R}$ chama-se **quadrática** quando existem reais $a, b, c$ com $a \neq 0$ tais que:
$$f(x) = ax^2 + bx + c$$

Seu gráfico cartesiano é uma curva plana denominada **parábola** com eixo de simetria vertical paralelo ao eixo $y$.

---

### 2. Concavidade e Zeros da Função
- **Concavidade**:
  - $a > 0$: Concavidade voltada para **cima** ($\cup$), possuindo ponto de **mínimo**.
  - $a < 0$: Concavidade voltada para **baixo** ($\cap$), possuindo ponto de **máximo**.

- **Fórmula Resolutiva de Bhaskara**:
  $$\Delta = b^2 - 4ac$$
  $$x = \frac{-b \pm \sqrt{\Delta}}{2a}$$
  - $\Delta > 0$: Duas raízes reais e distintas ($x_1 \neq x_2$).
  - $\Delta = 0$: Uma raiz real dupla ($x_1 = x_2 = -\frac{b}{2a}$).
  - $\Delta < 0$: Nenhuma raiz real (a parábola não intercepta o eixo $x$).

---

### 3. Vértice da Parábola e Otimização
O vértice $V(x_v, y_v)$ é o ponto extremo da função:
$$x_v = -\frac{b}{2a}$$
$$y_v = -\frac{\Delta}{4a} = f(x_v)$$

- Se $a > 0$: $y_v$ é o **valor mínimo** de $f$, e o conjunto imagem é $\text{Im}(f) = [y_v, +\infty[$.
- Se $a < 0$: $y_v$ é o **valor máximo** de $f$, e o conjunto imagem é $\text{Im}(f) = ]-\infty, y_v]$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Maximização de Lucro
**Enunciado:** O lucro $L$ (em milhares de reais) de uma pequena fábrica em função da quantidade $x$ de peças produzidas é modelado por:
$$L(x) = -x^2 + 10x - 9$$
Determine a quantidade de peças que maximiza o lucro e o valor do lucro máximo.

**Resolução:**
1. Como $a = -1 < 0$, a parábola possui concavidade voltada para baixo, admitindo ponto de máximo.
2. A quantidade que maximiza o lucro é a abscissa do vértice $x_v$:
   $$x_v = -\frac{b}{2a} = -\frac{10}{2(-1)} = \frac{-10}{-2} = 5 \text{ peças}$$
3. O lucro máximo obtido é o valor da função no vértice $L(x_v)$:
   $$L(5) = -(5)^2 + 10(5) - 9 = -25 + 50 - 9 = 16 \text{ mil reais}$$
   *(Pela fórmula direta: $\Delta = 10^2 - 4(-1)(-9) = 100 - 36 = 64 \implies y_v = -\frac{64}{4(-1)} = 16$)*

---

### Exemplo 2: Forma Fatorada da Parábola
**Enunciado:** Escreva a função quadrática com raízes $x_1 = 1$ e $x_2 = 4$ cujo gráfico passa pelo ponto $(0, 8)$.

**Resolução:**
1. Usamos a forma fatorada: $f(x) = a(x - x_1)(x - x_2) = a(x - 1)(x - 4)$.
2. Substituímos o ponto $(0, 8)$:
   $$8 = a(0 - 1)(0 - 4) \implies 8 = 4a \implies a = 2$$
3. Expandimos para a forma canônica:
   $$f(x) = 2(x^2 - 5x + 4) = 2x^2 - 10x + 8$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **"Quando" vs "Quanto" no Vértice:**
> - Se a questão perguntar **quando** o lucro é máximo, ou a quantidade necessária, a resposta é $x_v = -\frac{b}{2a}$.
> - Se perguntar **qual** o lucro máximo ou o valor extremo atingido, a resposta é $y_v = -\frac{\Delta}{4a}$.

> [!TIP]
> **Forma Canônica da Função Quadrática:**
> Qualquer função quadrática pode ser reescrita sem Bhaskara através do completamento de quadrados:
> $$f(x) = a(x - x_v)^2 + y_v$$
> Essa forma revela o vértice instantaneamente sem calcular $\Delta$!
""",
    },
}


async def seed():
    print("=== Tutor Inteligente: Iniciando Seed Canônico de Conteúdo Didático ===")
    async with AsyncSessionLocal() as db:
        # 1. Disciplina de Matemática
        disc_res = await db.execute(select(Disciplina).where(Disciplina.slug == "matematica"))
        disciplina = disc_res.scalar_one_or_none()

        if not disciplina:
            disciplina = Disciplina(
                slug="matematica",
                nome="Matemática",
                nivel_ensino="ensino_medio",
                icone="calculate",
                cor_tema="#F57C00",
                ordem=1,
                ativo=True
            )
            db.add(disciplina)
            await db.flush()
            print(f"[OK] Disciplina cadastrada: {disciplina.nome} ({disciplina.slug})")
        else:
            print(f"[OK] Disciplina já existente: {disciplina.nome}")

        # 2. Volumes e Capítulos
        total_caps = 0
        total_aulas = 0

        for vol_info in VOLUMES_DATA:
            vol_res = await db.execute(
                select(VolumeDidatico).where(
                    VolumeDidatico.disciplina_id == disciplina.id,
                    VolumeDidatico.numero_volume == vol_info["numero"]
                )
            )
            volume = vol_res.scalar_one_or_none()

            if not volume:
                volume = VolumeDidatico(
                    disciplina_id=disciplina.id,
                    nome_colecao="Fundamentos de Matemática Elementar - Gelson Iezzi",
                    numero_volume=vol_info["numero"],
                    titulo=vol_info["titulo"],
                    grande_area=vol_info["grande_area"],
                    ordem_exibicao=vol_info["ordem"],
                    preco_padrao=49.90,
                    ativo=True
                )
                db.add(volume)
                await db.flush()
                print(f"  [+] Volume {volume.numero_volume:02d}: {volume.titulo} ({volume.grande_area})")
            else:
                print(f"  [OK] Volume {volume.numero_volume:02d} existente: {volume.titulo}")

            # Capítulos do Volume
            for cap_idx, cap_info in enumerate(vol_info["capitulos"], start=1):
                cap_res = await db.execute(
                    select(Capitulo).where(
                        Capitulo.volume_id == volume.id,
                        Capitulo.numero_capitulo == cap_info["num"]
                    )
                )
                capitulo = cap_res.scalar_one_or_none()

                if not capitulo:
                    capitulo = Capitulo(
                        volume_id=volume.id,
                        numero_capitulo=cap_info["num"],
                        titulo=cap_info["titulo"],
                        tempo_estimado_min=cap_info["tempo"],
                        preco_avulso=9.90,
                        pre_requisitos_ids=[],
                        ordem=cap_idx
                    )
                    db.add(capitulo)
                    await db.flush()
                total_caps += 1

                # Se for Volume 1 e tiver aula completa mapeada, criar/atualizar aula
                if vol_info["numero"] == 1 and cap_info["num"] in AULAS_VOLUME_1:
                    aula_data = AULAS_VOLUME_1[cap_info["num"]]
                    aula_res = await db.execute(select(Aula).where(Aula.capitulo_id == capitulo.id))
                    aula = aula_res.scalar_one_or_none()

                    if not aula:
                        aula = Aula(
                            capitulo_id=capitulo.id,
                            bloco1_teoria_katex=aula_data["teoria"],
                            bloco2_exemplos_katex=aula_data["exemplos"],
                            bloco3_dicas_ia=aula_data["dicas"],
                            publicado=True
                        )
                        db.add(aula)
                        await db.flush()
                        total_aulas += 1
                        print(f"      [*] Aula estruturada criada para Cap. {capitulo.numero_capitulo}: {capitulo.titulo}")

        await db.commit()
        print(f"\nSeed concluído com sucesso!")
        print(f"Total: 1 Disciplina | 11 Volumes | {total_caps} Capítulos cadastrados | {total_aulas} Aulas completas com KaTeX.")


if __name__ == "__main__":
    asyncio.run(seed())
