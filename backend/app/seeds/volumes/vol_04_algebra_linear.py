"""
Módulo Canônico de Dados Didáticos — Volume 4: Sequências, Matrizes, Determinantes e Sistemas
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
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
}

# ============================================================================
# 1. CONTEÚDO DIDÁTICO DAS AULAS (AULAS_DATA)
# ============================================================================

AULAS_DATA = {
    1: {
        "teoria": r"""# Sequências Numéricas e Lei de Formação

Uma sequência (ou sucessão) numérica real é uma função cujo domínio é o conjunto dos números naturais não-nulos $\mathbb{N}^* = \{1, 2, 3, \dots, n, \dots\}$ e cujo contradomínio é o conjunto dos números reais $\mathbb{R}$.

### 1. Notação Canônica
Em vez da notação funcional usual $f(n)$, indicamos o elemento associado ao índice $n$ por $a_n$:
$$(a_n)_{n \in \mathbb{N}^*} = (a_1, a_2, a_3, \dots, a_n, \dots)$$
onde $a_1$ é o primeiro termo, $a_2$ o segundo termo, e $a_n$ o termo geral de ordem $n$.

---

### 2. Formas de Definição de uma Sequência
1. **Fórmula do Termo Geral**: expressa $a_n$ explicitamente em função da sua posição $n$.
   - Exemplo: $a_n = 3n - 1 \implies (2, 5, 8, 11, \dots)$.
2. **Fórmula de Recorrência**: fornece o(s) primeiro(s) termo(s) e uma regra para calcular $a_{n+1}$ a partir dos antecedentes imediatos.
   - Exemplo (Sequência de Fibonacci):
     $$\begin{cases} F_1 = 1, \; F_2 = 1 \\ F_{n} = F_{n-1} + F_{n-2}, \quad \forall n \ge 3 \end{cases}$$
3. **Propriedade dos Termos**: enunciada por uma regra descritiva textual (ex: sequência dos números primos positivos: $(2, 3, 5, 7, 11, \dots)$).

---

### 3. Monotonicidade e Limitação
- **Estritamente Crescente**: $a_{n+1} > a_n, \; \forall n \ge 1$.
- **Estritamente Decrescente**: $a_{n+1} < a_n, \; \forall n \ge 1$.
- **Constante ou Estacionária**: $a_{n+1} = a_n, \; \forall n \ge 1$.
- **Alternada ou Oscilante**: os termos alternam de sinal (ex: $a_n = (-1)^n$).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Termo Geral a partir de Recorrência
**Enunciado:** Uma sequência é definida recursivamente por $a_1 = 3$ e $a_{n+1} = 2a_n + 1$ para $n \ge 1$. Determine o valor de $a_4$.

**Resolução Passo a Passo:**
1. Calculamos $a_2$ fazendo $n = 1$:
   $$a_2 = 2a_1 + 1 = 2(3) + 1 = 6 + 1 = 7$$
2. Calculamos $a_3$ fazendo $n = 2$:
   $$a_3 = 2a_2 + 1 = 2(7) + 1 = 14 + 1 = 15$$
3. Calculamos $a_4$ fazendo $n = 3$:
   $$a_4 = 2a_3 + 1 = 2(15) + 1 = 30 + 1 = 31$$
Logo, $a_4 = 31$.

---

### Exemplo 2: Determinação da Fórmula Fechada
**Enunciado:** Determine o termo geral da sequência $(1, 4, 9, 16, 25, \dots)$ e calcule seu 12º termo.

**Resolução:**
1. Observamos que cada termo corresponde ao quadrado do respectivo índice:
   - $a_1 = 1 = 1^2$
   - $a_2 = 4 = 2^2$
   - $a_3 = 9 = 3^2$
2. Logo, a fórmula do termo geral é $a_n = n^2$.
3. Para o 12º termo ($n = 12$):
   $$a_{12} = 12^2 = 144$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Índice vs Valor do Termo:**
> Nunca confunda $n$ (a posição ou ordem do termo, sempre inteiro positivo $n \in \{1, 2, 3, \dots\}$) com $a_n$ (o valor numérico do termo, que pode ser fracionário, negativo ou irracional).

> [!TIP]
> Em sequências definidas por recorrência linear $a_{n+1} = k \cdot a_n$, se somarmos ou subtrairmos uma constante, experimente calcular os primeiros 4 termos para verificar se há uma PG oculta por translação.
""",
    },
    2: {
        "teoria": r"""# Progressão Aritmética (PA)

Uma **Progressão Aritmética (PA)** é qualquer sequência numérica em que cada termo, a partir do segundo, é igual à soma do termo anterior com uma constante fixa $r \in \mathbb{R}$, denominada **razão da PA**:
$$a_{n+1} - a_n = r, \quad \forall n \ge 1$$

### 1. Classificação da PA quanto à Razão
- **Crescente**: $r > 0 \implies a_{n+1} > a_n$.
- **Decrescente**: $r < 0 \implies a_{n+1} < a_n$.
- **Constante**: $r = 0 \implies a_1 = a_2 = \cdots = a_n$.

---

### 2. Termo Geral da PA
Por indução imediata sobre a definição recursiva:
- $a_2 = a_1 + r$
- $a_3 = a_2 + r = a_1 + 2r$
- $\dots$
- **Fórmula Geral**:
  $$a_n = a_1 + (n - 1)r$$
- **Relação entre quaisquer dois termos $a_n$ e $a_k$**:
  $$a_n = a_k + (n - k)r$$

---

### 3. Propriedades Canônicas da PA
1. **Média Aritmética dos Vizinhos**: Em qualquer PA, cada termo intermediário é a média aritmética dos seus termos equidistantes:
   $$a_k = \frac{a_{k-1} + a_{k+1}}{2}$$
2. **Soma dos Termos Equidistantes dos Extremos**:
   $$a_1 + a_n = a_2 + a_{n-1} = a_k + a_{n-k+1}$$
3. **Notação Especial para 3 Termos em PA**:
   $$(x - r, \; x, \; x + r)$$

---

### 4. Soma dos $n$ Primeiros Termos ($S_n$)
A soma histórica demonstrada por Gauss é dada por:
$$S_n = \frac{(a_1 + a_n) \cdot n}{2}$$
Substituindo $a_n = a_1 + (n-1)r$:
$$S_n = \frac{[2a_1 + (n - 1)r] \cdot n}{2}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Termo Geral e Interpolação
**Enunciado:** Numa PA com $a_1 = 7$ e razão $r = 4$, qual é a posição do termo igual a 83?

**Resolução Passo a Passo:**
1. Aplicamos a fórmula do termo geral $a_n = a_1 + (n - 1)r$:
   $$83 = 7 + (n - 1) \cdot 4$$
2. Subtraindo 7 de ambos os membros:
   $$76 = (n - 1) \cdot 4$$
3. Dividindo por 4:
   $$n - 1 = 19 \implies n = 20$$
O número 83 ocupa o 20º lugar na PA.

---

### Exemplo 2: Soma de Termos com Contexto
**Enunciado:** Calcule a soma de todos os múltiplos positivos de 3 compreendidos entre 10 e 100.

**Resolução:**
1. O primeiro múltiplo de 3 maior que 10 é $a_1 = 12$.
2. O último múltiplo de 3 menor que 100 é $a_n = 99$.
3. A razão é $r = 3$. Determinamos o número de termos $n$:
   $$99 = 12 + (n - 1) \cdot 3 \implies 87 = 3(n - 1) \implies n - 1 = 29 \implies n = 30$$
4. Calculamos a soma $S_{30}$:
   $$S_{30} = \frac{(a_1 + a_{30}) \cdot 30}{2} = \frac{(12 + 99) \cdot 30}{2} = 111 \cdot 15 = 1.665$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Atenção ao termo $(n-1)$:**
> Um erro clássico é escrever $a_n = a_1 + n \cdot r$. O primeiro termo não possui razão somada a ele; portanto, para atingir o $n$-ésimo termo avançamos exatamente $n - 1$ passos!

> [!TIP]
> Quando um problema envolver a soma de 3 termos em PA, defina-os como $(x - r, x, x + r)$. A soma deles cancela o $r$ e resulta diretamente em $3x$!
""",
    },
    3: {
        "teoria": r"""# Progressão Geométrica (PG)

Uma **Progressão Geométrica (PG)** é toda sequência numérica em que cada termo, a partir do segundo, é igual ao produto do termo anterior por uma constante $q \in \mathbb{R}$, chamada **razão da PG**:
$$\frac{a_{n+1}}{a_n} = q, \quad \forall n \ge 1 \quad (a_n \neq 0)$$

### 1. Classificação das Progressões Geométricas
- **Crescente**: $a_1 > 0$ e $q > 1$, ou $a_1 < 0$ e $0 < q < 1$.
- **Decrescente**: $a_1 > 0$ e $0 < q < 1$, ou $a_1 < 0$ e $q > 1$.
- **Oscilante ou Alternada**: $q < 0$ (os termos alternam de positivo para negativo).
- **Constante ou Singular**: $q = 1$ ou $a_1 = 0$.

---

### 2. Termo Geral da PG
Pela regra multiplicativa recursiva:
- $a_2 = a_1 \cdot q$
- $a_3 = a_2 \cdot q = a_1 \cdot q^2$
- **Fórmula Geral**:
  $$a_n = a_1 \cdot q^{n-1}$$
- **Relação entre quaisquer dois termos**:
  $$a_n = a_k \cdot q^{n-k}$$

---

### 3. Propriedades Canônicas da PG
1. **Média Geométrica**: Em termos positivos, cada termo intermediário é a média geométrica dos adjacentes:
   $$a_k^2 = a_{k-1} \cdot a_{k+1}$$
2. **Produto dos Termos Equidistantes dos Extremos**:
   $$a_1 \cdot a_n = a_2 \cdot a_{n-1} = a_k \cdot a_{n-k+1}$$

---

### 4. Fórmulas de Soma da PG
- **Soma dos $n$ Primeiros Termos (Finita)** ($q \neq 1$):
  $$S_n = \frac{a_1 (q^n - 1)}{q - 1} = \frac{a_1 (1 - q^n)}{1 - q}$$
- **Soma dos Infinitos Termos (Série Geométrica Convergente)**:
  Para razões no intervalo aberto $|q| < 1$, quando $n \to \infty$, $q^n \to 0$. A soma limite converge para:
  $$S_\infty = \lim_{n \to \infty} S_n = \frac{a_1}{1 - q}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Termo Geral da PG
**Enunciado:** Numa PG com $a_1 = 2$ e $q = 3$, calcule o sexto termo $a_6$.

**Resolução Passo a Passo:**
1. Aplicamos o termo geral $a_n = a_1 \cdot q^{n-1}$ para $n = 6$:
   $$a_6 = 2 \cdot 3^{6-1} = 2 \cdot 3^5$$
2. Calculamos $3^5 = 243$.
3. Multiplicamos:
   $$a_6 = 2 \cdot 243 = 486$$

---

### Exemplo 2: Soma de PG Infinita e Fração Geratriz
**Enunciado:** Determine a soma da série infinita $S = 4 + 2 + 1 + \frac{1}{2} + \frac{1}{4} + \cdots$.

**Resolução:**
1. Identificamos o primeiro termo e a razão:
   - $a_1 = 4$
   - $q = \frac{2}{4} = \frac{1}{2}$
2. Como $|q| = 1/2 < 1$, a série converge.
3. Aplicamos a fórmula $S_\infty = \frac{a_1}{1 - q}$:
   $$S_\infty = \frac{4}{1 - 1/2} = \frac{4}{1/2} = 4 \cdot 2 = 8$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Convergência da Soma Infinita:**
> A fórmula $S_\infty = \frac{a_1}{1 - q}$ é válida **exclusivamente** se $|q| < 1$. Se $q \ge 1$ ou $q \le -1$, a soma diverge e a fórmula não produz um número real válido!

> [!TIP]
> Para dízimas periódicas como $0{,}777\dots = \frac{7}{10} + \frac{7}{100} + \dots$, use a soma de PG infinita com $a_1 = 7/10$ e $q = 1/10 \implies S = \frac{7/10}{9/10} = \frac{7}{9}$.
""",
    },
    4: {
        "teoria": r"""# Teoria das Matrizes e Álgebra Matricial

Uma **matriz** $A$ do tipo $m \times n$ (lê-se $m$ por $n$) é uma tabela retangular de números reais dispostos em $m$ linhas e $n$ colunas:
$$A = [a_{ij}]_{m \times n} = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix}$$
onde $a_{ij}$ representa o elemento localizado na linha $i$ ($1 \le i \le m$) e coluna $j$ ($1 \le j \le n$).

### 1. Tipos Notáveis de Matrizes
- **Matriz Quadrada**: quando $m = n$ (ordem $n$). Possui diagonal principal ($i = j$) e diagonal secundária ($i + j = n + 1$).
- **Matriz Identidade ($I_n$)**: matriz quadrada onde $a_{ij} = 1$ para $i = j$ e $a_{ij} = 0$ para $i \neq j$.
- **Matriz Nula ($O_{m \times n}$)**: todos os elementos são nulos.
- **Matriz Transposta ($A^t$)**: obtida trocando ordenadamente as linhas pelas colunas ($A^t = [a_{ji}]_{n \times m}$).
- **Matriz Simétrica**: matriz quadrada tal que $A^t = A$.

---

### 2. Operações Fundamentais com Matrizes
1. **Adição e Subtração**:
   Definida apenas para matrizes de mesma dimensão $m \times n$:
   $$(A + B)_{ij} = a_{ij} + b_{ij}$$
2. **Multiplicação por Escalar**:
   $$(\alpha \cdot A)_{ij} = \alpha \cdot a_{ij}, \quad \alpha \in \mathbb{R}$$
3. **Multiplicação de Matrizes ($A \cdot B$)**:
   - **Condição de Existência**: O número de colunas de $A$ deve ser rigorosamente igual ao número de linhas de $B$:
     $$A_{m \times p} \cdot B_{p \times n} = C_{m \times n}$$
   - **Regra Linha por Coluna**:
     $$c_{ij} = \sum_{k=1}^p a_{ik} \cdot b_{kj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{ip}b_{pj}$$

---

### 3. Propriedades Críticas da Multiplicação
- **Não-comutativa em geral**: $A \cdot B \neq B \cdot A$.
- **Associativa**: $(A \cdot B) \cdot C = A \cdot (B \cdot C)$.
- **Distributiva**: $A \cdot (B + C) = A \cdot B + A \cdot C$.
- **Elemento Neutro**: $A \cdot I_n = I_m \cdot A = A$.
- **Transposta do Produto**: $(A \cdot B)^t = B^t \cdot A^t$ (a ordem dos fatores inverte!).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Multiplicação de Matrizes $2 \times 2$
**Enunciado:** Calcule o produto $A \cdot B$ das matrizes:
$$A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} 5 & 0 \\ -1 & 2 \end{bmatrix}$$

**Resolução Passo a Passo:**
1. A matriz resultante $C = A \cdot B$ é de ordem $2 \times 2$.
2. Linha 1 de $A$ com Colunas de $B$:
   - $c_{11} = 1 \cdot 5 + 2 \cdot (-1) = 5 - 2 = 3$
   - $c_{12} = 1 \cdot 0 + 2 \cdot 2 = 0 + 4 = 4$
3. Linha 2 de $A$ com Colunas de $B$:
   - $c_{21} = 3 \cdot 5 + 4 \cdot (-1) = 15 - 4 = 11$
   - $c_{22} = 3 \cdot 0 + 4 \cdot 2 = 0 + 8 = 8$
4. Montando a matriz:
   $$A \cdot B = \begin{bmatrix} 3 & 4 \\ 11 & 8 \end{bmatrix}$$

---

### Exemplo 2: Equação Matricial
**Enunciado:** Sendo $A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}$ e $I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$, determine $2A - 3I$.

**Resolução:**
1. Multiplicamos $A$ por 2:
   $$2A = \begin{bmatrix} 4 & 2 \\ 0 & 6 \end{bmatrix}$$
2. Multiplicamos $I$ por 3:
   $$3I = \begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$$
3. Subtraímos elemento a elemento:
   $$2A - 3I = \begin{bmatrix} 4 - 3 & 2 - 0 \\ 0 - 0 & 6 - 3 \end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 0 & 3 \end{bmatrix}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **$AB = 0$ não implica $A = 0$ ou $B = 0$:**
> Na álgebra de matrizes existem divisores de zero! Matrizes não-nulas multiplicadas podem resultar na matriz nula. Exemplo: $\begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$.

> [!TIP]
> Atenção às dimensões na multiplicação: $(m \times p) \times (p \times n) \to (m \times n)$. Os valores internos devem ser rigorosamente iguais.
""",
    },
    5: {
        "teoria": r"""# Determinantes e Teorema de Laplace

O determinante é uma função que associa a cada matriz quadrada $A$ de ordem $n$ com coeficientes reais um único número real, denotado por $\det(A)$ ou $|A|$.

### 1. Determinantes de Ordens 1, 2 e 3
1. **Ordem 1**: Se $A = [a_{11}]$, então $\det(A) = a_{11}$.
2. **Ordem 2**:
   $$\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$$
3. **Ordem 3 (Regra de Sarrus)**:
   $$\det \begin{bmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{bmatrix} = (a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32}) - (a_{13}a_{22}a_{31} + a_{11}a_{23}a_{32} + a_{12}a_{21}a_{33})$$

---

### 2. Teorema de Laplace e Matriz dos Cofatores
Para qualquer matriz de ordem $n \ge 2$, o determinante pode ser calculado pelo desenvolvimento ao longo de qualquer fila (linha $i$ ou coluna $j$):
$$\det(A) = \sum_{j=1}^n a_{ij} \cdot C_{ij}$$
onde o **cofator** $C_{ij}$ é dado por:
$$C_{ij} = (-1)^{i+j} \cdot \det(M_{ij})$$
sendo $M_{ij}$ a submatriz de ordem $n-1$ obtida eliminando a linha $i$ e a coluna $j$ de $A$.

---

### 3. Propriedades Canônicas dos Determinantes
1. **Fila Nula**: Se $A$ possui uma linha ou coluna inteira de zeros, $\det(A) = 0$.
2. **Filas Proporcionais ou Iguais**: Se duas linhas (ou colunas) forem iguais ou múltiplas escalares, $\det(A) = 0$.
3. **Multiplicação de Fila por Escalar**: Multiplicar uma linha de $A$ por $k$ multiplica o determinante por $k$. Consequentemente:
   $$\det(k \cdot A) = k^n \cdot \det(A) \quad (\text{para } A \text{ de ordem } n)$$
4. **Troca de Filas**: Trocar duas linhas paralelas inverte o sinal do determinante.
5. **Teorema de Binet**: O determinante do produto é o produto dos determinantes:
   $$\det(A \cdot B) = \det(A) \cdot \det(B)$$
6. **Inversa**: Uma matriz quadrada $A$ é invertível se, e somente se, $\det(A) \neq 0$. Nesse caso:
   $$\det(A^{-1}) = \frac{1}{\det(A)}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinante $2 \times 2$ e Equação
**Enunciado:** Determine o valor real de $x$ tal que $\det \begin{bmatrix} x & 3 \\ 2 & x+1 \end{bmatrix} = 0$.

**Resolução Passo a Passo:**
1. Calculamos o determinante pela diagonal principal menos secundária:
   $$\det = x(x + 1) - (3)(2) = x^2 + x - 6$$
2. Igualamos a zero:
   $$x^2 + x - 6 = 0$$
3. Aplicamos a fórmula quadrática:
   $$x = \frac{-1 \pm \sqrt{1^2 - 4(1)(-6)}}{2} = \frac{-1 \pm \sqrt{25}}{2} = \frac{-1 \pm 5}{2}$$
   - $x_1 = \frac{4}{2} = 2$
   - $x_2 = \frac{-6}{2} = -3$
Portanto, as soluções são $x \in \{-3, 2\}$.

---

### Exemplo 2: Aplicação do Teorema de Binet e Escalares
**Enunciado:** Seja $A$ uma matriz quadrada de ordem 3 tal que $\det(A) = 4$. Calcule $\det(2A)$ e $\det(A^3)$.

**Resolução:**
1. Como a ordem da matriz é $n = 3$, ao multiplicar a matriz toda pelo escalar 2:
   $$\det(2A) = 2^3 \cdot \det(A) = 8 \cdot 4 = 32$$
2. Pelo Teorema de Binet:
   $$\det(A^3) = [\det(A)]^3 = 4^3 = 64$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **$\det(k \cdot A) \neq k \cdot \det(A)$:**
> Multiplicar toda a matriz $A_{n \times n}$ por $k$ multiplica **todas as $n$ linhas** por $k$. Portanto, o escalar sai elevado à ordem da matriz: $\det(k A) = k^n \det(A)$!

> [!TIP]
> Ao aplicar o Teorema de Laplace, escolha sempre a fila (linha ou coluna) que possua o **maior número de zeros**, reduzindo drasticamente a quantidade de cofatores a serem calculados.
""",
    },
    6: {
        "teoria": r"""# Sistemas Lineares e Escalonamento Gaussiano

Um **sistema linear** de $m$ equações com $n$ incógnitas $(x_1, x_2, \dots, x_n)$ é um conjunto de equações da forma:
$$\begin{cases} a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\ a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\ \vdots \\ a_{m1}x_1 + a_{m2}x_2 + \cdots + a_{mn}x_n = b_m \end{cases}$$
Forma matricial compacta: $A \cdot X = B$.

### 1. Classificação dos Sistemas Lineares
- **SPD (Sistema Possível e Determinado)**: possui uma única solução (grau de liberdade zero).
- **SPI (Sistema Possível e Indeterminado)**: possui infinitas soluções (graus de liberdade $> 0$).
- **SI (Sistema Impossível)**: não admite nenhuma solução real (conjunto solução $S = \emptyset$).

---

### 2. Regra de Cramer (Para Sistemas $n \times n$)
Seja $D = \det(A)$ o determinante da matriz dos coeficientes.
- Se $D \neq 0$, o sistema é **SPD** e as incógnitas são dadas por:
  $$x_i = \frac{D_{x_i}}{D}$$
  onde $D_{x_i}$ é o determinante obtido substituindo a coluna dos coeficientes de $x_i$ pela coluna dos termos independentes $B$.
- Se $D = 0$, o sistema é **SPI** ou **SI** (a Regra de Cramer é inconclusiva; deve-se recorrer ao escalonamento).

---

### 3. Escalonamento Gaussiano (Eliminação de Gauss)
O método universal consiste em transformar a matriz aumentada $[A \mid B]$ em uma matriz escalonada por meio de operações elementares sobre as linhas:
1. Trocar duas linhas entre si ($L_i \leftrightarrow L_j$).
2. Multiplicar uma linha por escalar não-nulo ($L_i \leftarrow k \cdot L_i, \; k \neq 0$).
3. Somar a uma linha um múltiplo escalar de outra linha ($L_i \leftarrow L_i + k \cdot L_j$).

- **Interpretação do Escalonamento**:
  - Se surgir uma linha do tipo $[0 \; 0 \; \dots \; 0 \mid b_k]$ com $b_k \neq 0$, o sistema é **SI** ($0 = b_k$ é absurdo).
  - Se o número de equações úteis for igual ao número de incógnitas, o sistema é **SPD**.
  - Se o número de equações úteis for menor que o número de incógnitas, o sistema é **SPI**.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Resolução por Cramer
**Enunciado:** Resolva o sistema linear:
$$\begin{cases} 2x + y = 7 \\ 3x - y = 8 \end{cases}$$

**Resolução Passo a Passo:**
1. Determinante principal $D$:
   $$D = \det \begin{bmatrix} 2 & 1 \\ 3 & -1 \end{bmatrix} = 2(-1) - 1(3) = -2 - 3 = -5$$
   Como $D = -5 \neq 0$, o sistema é SPD.
2. Determinantes das incógnitas:
   $$D_x = \det \begin{bmatrix} 7 & 1 \\ 8 & -1 \end{bmatrix} = 7(-1) - 1(8) = -7 - 8 = -15$$
   $$D_y = \det \begin{bmatrix} 2 & 7 \\ 3 & 8 \end{bmatrix} = 2(8) - 7(3) = 16 - 21 = -5$$
3. Calculamos as variáveis:
   $$x = \frac{D_x}{D} = \frac{-15}{-5} = 3, \quad y = \frac{D_y}{D} = \frac{-5}{-5} = 1$$
O par ordenado solução é $(x, y) = (3, 1)$.

---

### Exemplo 2: Discussão de Sistema por Escalonamento
**Enunciado:** Para qual valor real de $k$ o sistema $\begin{cases} x + 2y = 4 \\ 2x + ky = 8 \end{cases}$ possui infinitas soluções?

**Resolução:**
1. Montamos a matriz aumentada:
   $$\begin{bmatrix} 1 & 2 & \mid & 4 \\ 2 & k & \mid & 8 \end{bmatrix}$$
2. Aplicamos a operação elementar $L_2 \leftarrow L_2 - 2L_1$:
   - $2 - 2(1) = 0$
   - $k - 2(2) = k - 4$
   - $8 - 2(4) = 0$
   Resultando em:
   $$\begin{bmatrix} 1 & 2 & \mid & 4 \\ 0 & k - 4 & \mid & 0 \end{bmatrix}$$
3. Para que o sistema seja SPI (infinitas soluções), a segunda linha deve anular-se por completo ($0y = 0$):
   $$k - 4 = 0 \implies k = 4$$
Logo, para $k = 4$ o sistema é possível e indeterminado.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **$D = 0$ em Cramer não significa necessariamente SPI:**
> Se $D = 0$ e todos os $D_{x_i} = 0$, o sistema ainda pode ser **Impossível (SI)** no caso de equações incompatíveis como planos paralelos distintos! Utilize sempre o escalonamento para garantir o diagnóstico correto.

> [!TIP]
> Em um sistema homogêneo (todos os termos independentes $b_i = 0$), a solução trivial $(0, 0, \dots, 0)$ sempre existe. Logo, um sistema homogêneo nunca é impossível: ou é SPD (somente solução nula) ou SPI (soluções próprias).
""",
    },
}

# ============================================================================
# 2. BATERIAS DE FIXAÇÃO (FIXACAO_DATA — 3 questões por capítulo)
# ============================================================================

FIXACAO_DATA = {
    1: [
        {
            "enunciado_katex": r"Dada a sequência com termo geral $a_n = 2n^2 - 3$, o valor do quarto termo ($a_4$) é:",
            "alternativas": [
                {"letra": "A", "texto": r"$29$", "correta": True},
                {"letra": "B", "texto": r"$25$", "correta": False},
                {"letra": "C", "texto": r"$31$", "correta": False},
                {"letra": "D", "texto": r"$13$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Substituindo $n = 4$: $a_4 = 2(4)^2 - 3 = 2(16) - 3 = 32 - 3 = 29$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Uma sequência é definida por $x_1 = 5$ e $x_{n+1} = x_n + 4$. Qual é o terceiro termo dessa sequência?",
            "alternativas": [
                {"letra": "A", "texto": r"$13$", "correta": True},
                {"letra": "B", "texto": r"$9$", "correta": False},
                {"letra": "C", "texto": r"$17$", "correta": False},
                {"letra": "D", "texto": r"$12$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$x_2 = 5 + 4 = 9$; $x_3 = 9 + 4 = 13$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Considere a sequência $a_n = (-1)^n \cdot \frac{1}{n}$. Pode-se afirmar que essa sequência é:",
            "alternativas": [
                {"letra": "A", "texto": r"Alternada e limitada", "correta": True},
                {"letra": "B", "texto": r"Monótona crescente", "correta": False},
                {"letra": "C", "texto": r"Monótona decrescente", "correta": False},
                {"letra": "D", "texto": r"Divergente para o infinito", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Os sinais dos termos alternam entre negativo e positivo ($-\frac{1}{1}, \frac{1}{2}, -\frac{1}{3}, \dots$), e todos os termos estão no intervalo $[-1, \frac{1}{2}]$. Alternativa A.",
        },
    ],
    2: [
        {
            "enunciado_katex": r"Em uma progressão aritmética, tem-se $a_1 = 4$ e razão $r = 5$. O 15º termo ($a_{15}$) vale:",
            "alternativas": [
                {"letra": "A", "texto": r"$74$", "correta": True},
                {"letra": "B", "texto": r"$79$", "correta": False},
                {"letra": "C", "texto": r"$70$", "correta": False},
                {"letra": "D", "texto": r"$69$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$a_{15} = a_1 + 14r = 4 + 14(5) = 4 + 70 = 74$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Qual é a soma dos 20 primeiros termos da progressão aritmética $(3, 7, 11, 15, \dots)$?",
            "alternativas": [
                {"letra": "A", "texto": r"$820$", "correta": True},
                {"letra": "B", "texto": r"$790$", "correta": False},
                {"letra": "C", "texto": r"$840$", "correta": False},
                {"letra": "D", "texto": r"$410$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$a_1 = 3, r = 4 \implies a_{20} = 3 + 19(4) = 79$. $S_{20} = \frac{(3 + 79) \cdot 20}{2} = 82 \cdot 10 = 820$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Três termos consecutivos de uma PA são dados por $(x - 1, \; 2x + 1, \; 4x - 1)$. O valor de $x$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$4$", "correta": True},
                {"letra": "B", "texto": r"$2$", "correta": False},
                {"letra": "C", "texto": r"$3$", "correta": False},
                {"letra": "D", "texto": r"$5$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Pela média aritmética: $2x + 1 = \frac{(x - 1) + (4x - 1)}{2} \implies 4x + 2 = 5x - 2 \implies x = 4$. Alternativa A.",
        },
    ],
    3: [
        {
            "enunciado_katex": r"Em uma PG, o primeiro termo é $a_1 = 3$ e a razão é $q = 2$. O oitavo termo ($a_8$) é:",
            "alternativas": [
                {"letra": "A", "texto": r"$384$", "correta": True},
                {"letra": "B", "texto": r"$768$", "correta": False},
                {"letra": "C", "texto": r"$192$", "correta": False},
                {"letra": "D", "texto": r"$256$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$a_8 = a_1 \cdot q^7 = 3 \cdot 2^7 = 3 \cdot 128 = 384$. Alternativa A.",
        },
        {
            "enunciado_katex": r"A soma dos infinitos termos da PG $(12, 6, 3, 1{,}5, \dots)$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$24$", "correta": True},
                {"letra": "B", "texto": r"$18$", "correta": False},
                {"letra": "C", "texto": r"$36$", "correta": False},
                {"letra": "D", "texto": r"$48$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$a_1 = 12$ e $q = 1/2$. Como $|q| < 1$: $S_\infty = \frac{12}{1 - 1/2} = \frac{12}{1/2} = 24$. Alternativa A.",
        },
        {
            "enunciado_katex": r"A soma dos 5 primeiros termos da PG finita $(2, 6, 18, \dots)$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$242$", "correta": True},
                {"letra": "B", "texto": r"$240$", "correta": False},
                {"letra": "C", "texto": r"$162$", "correta": False},
                {"letra": "D", "texto": r"$486$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$a_1 = 2, q = 3$. $S_5 = \frac{2(3^5 - 1)}{3 - 1} = \frac{2(243 - 1)}{2} = 242$. Alternativa A.",
        },
    ],
    4: [
        {
            "enunciado_katex": r"Dadas as matrizes $A = \begin{bmatrix} 1 & 3 \\ 2 & 4 \end{bmatrix}$ e $B = \begin{bmatrix} -1 & 2 \\ 0 & 5 \end{bmatrix}$, a soma $A + B$ resulta em:",
            "alternativas": [
                {"letra": "A", "texto": r"$\begin{bmatrix} 0 & 5 \\ 2 & 9 \end{bmatrix}$", "correta": True},
                {"letra": "B", "texto": r"$\begin{bmatrix} 2 & 1 \\ 2 & -1 \end{bmatrix}$", "correta": False},
                {"letra": "C", "texto": r"$\begin{bmatrix} 0 & 1 \\ 2 & 9 \end{bmatrix}$", "correta": False},
                {"letra": "D", "texto": r"$\begin{bmatrix} -1 & 6 \\ 0 & 20 \end{bmatrix}$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Somando elemento a elemento: $1+(-1)=0, 3+2=5, 2+0=2, 4+5=9$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se a matriz $A$ é de ordem $3 \times 4$ e a matriz $B$ é de ordem $4 \times 2$, a ordem da matriz produto $A \cdot B$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$3 \times 2$", "correta": True},
                {"letra": "B", "texto": r"$4 \times 4$", "correta": False},
                {"letra": "C", "texto": r"$2 \times 3$", "correta": False},
                {"letra": "D", "texto": r"$3 \times 4$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"O produto de uma matriz $(m \times p)$ por $(p \times n)$ resulta em $(m \times n)$. Logo, $(3 \times 4) \times (4 \times 2) = (3 \times 2)$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se $A = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}$, a transposta $A^t$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$\begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}$", "correta": True},
                {"letra": "B", "texto": r"$\begin{bmatrix} 3 & 0 \\ 1 & 2 \end{bmatrix}$", "correta": False},
                {"letra": "C", "texto": r"$\begin{bmatrix} -2 & 0 \\ -1 & -3 \end{bmatrix}$", "correta": False},
                {"letra": "D", "texto": r"$\begin{bmatrix} 0 & 2 \\ 3 & 1 \end{bmatrix}$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"A primeira linha $(2, 0)$ passa a ser a primeira coluna, e a segunda linha $(1, 3)$ passa a ser a segunda coluna. Alternativa A.",
        },
    ],
    5: [
        {
            "enunciado_katex": r"O determinante da matriz $M = \begin{bmatrix} 4 & 5 \\ 2 & 3 \end{bmatrix}$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$2$", "correta": True},
                {"letra": "B", "texto": r"$22$", "correta": False},
                {"letra": "C", "texto": r"$-2$", "correta": False},
                {"letra": "D", "texto": r"$10$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$\det(M) = 4 \cdot 3 - 5 \cdot 2 = 12 - 10 = 2$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se $A$ é uma matriz quadrada de ordem $2$ com $\det(A) = 5$, então $\det(3A)$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$45$", "correta": True},
                {"letra": "B", "texto": r"$15$", "correta": False},
                {"letra": "C", "texto": r"$30$", "correta": False},
                {"letra": "D", "texto": r"$125$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Para ordem $n = 2$: $\det(k A) = k^2 \det(A) = 3^2 \cdot 5 = 9 \cdot 5 = 45$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Uma matriz quadrada $A$ admite inversa se, e somente se:",
            "alternativas": [
                {"letra": "A", "texto": r"$\det(A) \neq 0$", "correta": True},
                {"letra": "B", "texto": r"$\det(A) = 0$", "correta": False},
                {"letra": "C", "texto": r"$\det(A) > 0$", "correta": False},
                {"letra": "D", "texto": r"Todos os elementos forem não-nulos", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Uma matriz é invertível (ou não-singular) se e somente se o seu determinante é diferente de zero. Alternativa A.",
        },
    ],
    6: [
        {
            "enunciado_katex": r"O sistema linear $\begin{cases} x + y = 10 \\ x - y = 4 \end{cases}$ possui como solução o par $(x, y)$ igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$(7, 3)$", "correta": True},
                {"letra": "B", "texto": r"$(6, 4)$", "correta": False},
                {"letra": "C", "texto": r"$(8, 2)$", "correta": False},
                {"letra": "D", "texto": r"$(5, 5)$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Somando as duas equações: $2x = 14 \implies x = 7$. Logo, $y = 10 - 7 = 3$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Um sistema linear com 3 equações e 3 incógnitas que possui determinante da matriz dos coeficientes $D = 0$ e determinante $D_x = 4$ é classificado como:",
            "alternativas": [
                {"letra": "A", "texto": r"Sistema Impossível (SI)", "correta": True},
                {"letra": "B", "texto": r"Sistema Possível e Determinado (SPD)", "correta": False},
                {"letra": "C", "texto": r"Sistema Possível e Indeterminado (SPI)", "correta": False},
                {"letra": "D", "texto": r"Sistema Homogêneo", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Se $D = 0$ e algum $D_i \neq 0$, a igualdade $0 \cdot x = 4$ não admite solução no campo real. O sistema é Impossível (SI). Alternativa A.",
        },
        {
            "enunciado_katex": r"Quantas soluções possui o sistema linear homogêneo $\begin{cases} 2x + 3y = 0 \\ 4x + 6y = 0 \end{cases}$?",
            "alternativas": [
                {"letra": "A", "texto": r"Infinitas soluções", "correta": True},
                {"letra": "B", "texto": r"Uma única solução", "correta": False},
                {"letra": "C", "texto": r"Nenhuma solução", "correta": False},
                {"letra": "D", "texto": r"Exatamente duas soluções", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"As duas equações são proporcionais ($L_2 = 2L_1$). Trata-se de um sistema homogêneo com $\det(A) = 0$, admitindo infinitas soluções (SPI). Alternativa A.",
        },
    ],
}

# ============================================================================
# 3. FRAGMENTOS CANÔNICOS PARA O RAG (RAG_DATA — 1 por capítulo)
# ============================================================================

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "titulo": "Definição de Sequência e Relações de Recorrência",
        "conteudo_markdown": r"""Uma sequência de números reais é uma função $f: \mathbb{N}^* \to \mathbb{R}$, denotada por $(a_n)_{n \ge 1}$. A especificação por recorrência requer a definição explícita do valor do primeiro termo $a_1$ e uma equação $a_{n+1} = g(a_n)$ que permite gerar unicamente cada termo posterior a partir dos termos predecessores.""",
    },
    {
        "numero_capitulo": 2,
        "titulo": "Progressão Aritmética e Teorema da Soma de Gauss",
        "conteudo_markdown": r"""Em uma PA de razão $r$, a diferença entre termos consecutivos é invariante: $a_{n+1} - a_n = r$. O termo geral é dado por $a_n = a_1 + (n-1)r$. A soma dos $n$ primeiros termos é obtida pelo produto da média dos extremos pelo número de termos: $S_n = \frac{n(a_1 + a_n)}{2}$.""",
    },
    {
        "numero_capitulo": 3,
        "titulo": "Progressão Geométrica e Série Geométrica Infinita",
        "conteudo_markdown": r"""Em uma PG de razão $q$, a taxa de variação multiplicativa é constante: $a_{n+1} = a_n \cdot q$. O termo geral é $a_n = a_1 \cdot q^{n-1}$. Para $|q| < 1$, a série infinita é absolutamente convergente e o limite da soma é $S_\infty = \frac{a_1}{1 - q}$.""",
    },
    {
        "numero_capitulo": 4,
        "titulo": "Álgebra de Matrizes e Multiplicação Matricial",
        "conteudo_markdown": r"""O produto $A_{m \times p} \cdot B_{p \times n} = C_{m \times n}$ só é definido quando a quantidade de colunas do primeiro fator coincide com a quantidade de linhas do segundo fator. O produto em geral é não-comutativo ($AB \neq BA$) e a transposição inverte a ordem: $(AB)^t = B^t A^t$.""",
    },
    {
        "numero_capitulo": 5,
        "titulo": "Propriedades dos Determinantes e Teorema de Binet",
        "conteudo_markdown": r"""Para qualquer matriz $A_{n \times n}$ e escalar $k$, tem-se $\det(k A) = k^n \det(A)$. Pelo Teorema de Binet, o determinante do produto coincide com o produto dos determinantes: $\det(AB) = \det(A)\det(B)$. Uma matriz quadrada admite inversa multiplicativa se, e somente se, $\det(A) \neq 0$, caso em que $\det(A^{-1}) = \frac{1}{\det(A)}$.""",
    },
    {
        "numero_capitulo": 6,
        "titulo": "Classificação de Sistemas Lineares e Regra de Cramer",
        "conteudo_markdown": r"""Um sistema linear $A X = B$ de ordem $n \times n$ é Possível e Determinado (SPD) se $\det(A) \neq 0$, com solução calculada por $x_i = \frac{\det(A_i)}{\det(A)}$. Se $\det(A) = 0$, o escalonamento gaussiano é obrigatório para distinguir entre infinitas soluções (SPI) e impossibilidade (SI).""",
    },
]

# ============================================================================
# 4. ITENS CALIBRADOS TRI (TRI_DATA — 5 itens por capítulo = 30 itens)
# ============================================================================

TRI_DATA = [
    # --- Cap 1: Sequências Numéricas e Lei de Formação (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dada a sequência de termo geral $a_n = 3n - 2$, a soma dos quatro primeiros termos é:",
        "alternativas": [
            {"letra": "A", "texto": r"$22$", "correta": True},
            {"letra": "B", "texto": r"$20$", "correta": False},
            {"letra": "C", "texto": r"$24$", "correta": False},
            {"letra": "D", "texto": r"$18$", "correta": False},
            {"letra": "E", "texto": r"$26$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_1 = 3(1) - 2 = 1$. 2. $a_2 = 3(2) - 2 = 4$. 3. $a_3 = 3(3) - 2 = 7$. 4. $a_4 = 3(4) - 2 = 10$. 5. Soma: $1 + 4 + 7 + 10 = 22$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Calcule cada um dos quatro termos individualmente e depois efetue a soma."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma sequência possui a lei de formação $a_1 = 2$ e $a_{n+1} = 3a_n - 1$. O valor de $a_3$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$14$", "correta": True},
            {"letra": "B", "texto": r"$15$", "correta": False},
            {"letra": "C", "texto": r"$12$", "correta": False},
            {"letra": "D", "texto": r"$17$", "correta": False},
            {"letra": "E", "texto": r"$11$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_2 = 3a_1 - 1 = 3(2) - 1 = 5$. 2. $a_3 = 3a_2 - 1 = 3(5) - 1 = 14$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Aplique a relação recursiva duas vezes consecutivas."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o 20º termo da sequência cujo termo geral é dado por $a_n = \frac{n}{n + 1}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{20}{21}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{19}{20}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{21}{22}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{20}{19}$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Fazendo $n = 20$: $a_{20} = \frac{20}{20 + 1} = \frac{20}{21}$. Alternativa A.",
        "parametro_a": 1.100,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Substitua diretamente $n = 20$ no numerador e no denominador."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Na sequência de Fibonacci onde $F_1 = 1, F_2 = 1$ e $F_n = F_{n-1} + F_{n-2}$, determine o valor de $F_7$.",
        "alternativas": [],
        "resposta_correta": "13",
        "resolucao_passo_a_passo": r"1. $F_1 = 1$. 2. $F_2 = 1$. 3. $F_3 = 2$. 4. $F_4 = 3$. 5. $F_5 = 5$. 6. $F_6 = 8$. 7. $F_7 = 5 + 8 = 13$.",
        "parametro_a": 1.300,
        "parametro_b": 0.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "Some os dois termos anteriores sucessivamente até o 7º elemento."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se a sequência $(a_n)$ satisfaz $a_n = n^2 - 10n + 9$, qual é o menor valor assumido por $a_n$ para $n \in \mathbb{N}^*$?",
        "alternativas": [
            {"letra": "A", "texto": r"$-16$", "correta": True},
            {"letra": "B", "texto": r"$-25$", "correta": False},
            {"letra": "C", "texto": r"$-15$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$-9$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A função quadrática $f(x) = x^2 - 10x + 9$ atinge vértice em $x_v = -\frac{-10}{2} = 5 \in \mathbb{N}^*$. 2. $a_5 = 5^2 - 10(5) + 9 = 25 - 50 + 9 = -16$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Encontre o vértice da parábola associada ao termo geral."},
    },

    # --- Cap 2: Progressão Aritmética (PA) (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma PA, o primeiro termo é $a_1 = 5$ e a razão é $r = 3$. O valor do décimo termo $a_{10}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$32$", "correta": True},
            {"letra": "B", "texto": r"$35$", "correta": False},
            {"letra": "C", "texto": r"$30$", "correta": False},
            {"letra": "D", "texto": r"$29$", "correta": False},
            {"letra": "E", "texto": r"$50$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Fórmula do termo geral da PA: $a_n = a_1 + (n - 1)r$. 2. $a_{10} = 5 + (10 - 1) \cdot 3 = 5 + 27 = 32$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Use o termo geral da PA: $a_n = a_1 + (n-1)r$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos termos possui a PA finita $(7, 11, 15, \dots, 83)$?",
        "alternativas": [
            {"letra": "A", "texto": r"$20$", "correta": True},
            {"letra": "B", "texto": r"$19$", "correta": False},
            {"letra": "C", "texto": r"$21$", "correta": False},
            {"letra": "D", "texto": r"$18$", "correta": False},
            {"letra": "E", "texto": r"$22$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_1 = 7, r = 4, a_n = 83$. 2. $83 = 7 + (n - 1) \cdot 4 \implies 76 = 4(n - 1) \implies n - 1 = 19 \implies n = 20$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Isole $n$ na equação do termo geral da PA."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma dos 30 primeiros termos de uma progressão aritmética cujo termo geral é $a_n = 2n + 1$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$960$", "correta": True},
            {"letra": "B", "texto": r"$930$", "correta": False},
            {"letra": "C", "texto": r"$1.860$", "correta": False},
            {"letra": "D", "texto": r"$900$", "correta": False},
            {"letra": "E", "texto": r"$990$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_1 = 2(1) + 1 = 3$. 2. $a_{30} = 2(30) + 1 = 61$. 3. $S_{30} = \frac{(3 + 61) \cdot 30}{2} = 64 \cdot 15 = 960$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Calcule $a_1$ e $a_{30}$ e aplique a fórmula da soma de Gauss."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Três números estão em PA crescente. A soma deles é 21 e o produto é 280. Determine a razão dessa PA.",
        "alternativas": [],
        "resposta_correta": "3",
        "resolucao_passo_a_passo": r"1. Seja a PA $(x-r, x, x+r)$. 2. Soma: $3x = 21 \implies x = 7$. 3. Produto: $(7-r) \cdot 7 \cdot (7+r) = 280 \implies 49 - r^2 = 40 \implies r^2 = 9$. Como a PA é crescente, $r = 3$.",
        "parametro_a": 1.500,
        "parametro_b": 0.700,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "Escreva os três termos como $(x-r, x, x+r)$ para cancelar $r$ na soma."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Interpolando-se 6 meios aritméticos entre 5 e 40, a razão da PA obtida é:",
        "alternativas": [
            {"letra": "A", "texto": r"$5$", "correta": True},
            {"letra": "B", "texto": r"$6$", "correta": False},
            {"letra": "C", "texto": r"$7$", "correta": False},
            {"letra": "D", "texto": r"$4$", "correta": False},
            {"letra": "E", "texto": r"$8$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Inserir 6 meios resulta em $n = 6 + 2 = 8$ termos. 2. $a_1 = 5$ e $a_8 = 40$. 3. $40 = 5 + (8 - 1)r \implies 35 = 7r \implies r = 5$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "O número total de termos é a quantidade de meios somada aos 2 extremos."},
    },

    # --- Cap 3: Progressão Geométrica (PG) (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma PG de razão $2$, o terceiro termo vale $12$. O quinto termo $a_5$ dessa PG é:",
        "alternativas": [
            {"letra": "A", "texto": r"$48$", "correta": True},
            {"letra": "B", "texto": r"$24$", "correta": False},
            {"letra": "C", "texto": r"$36$", "correta": False},
            {"letra": "D", "texto": r"$96$", "correta": False},
            {"letra": "E", "texto": r"$14$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_4 = a_3 \cdot q = 12 \cdot 2 = 24$. 2. $a_5 = a_4 \cdot q = 24 \cdot 2 = 48$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Multiplique duas vezes pela razão: $a_5 = a_3 \cdot q^2$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor da soma infinita $S = 9 + 3 + 1 + \frac{1}{3} + \dots$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{27}{2}$", "correta": True},
            {"letra": "B", "texto": r"$13$", "correta": False},
            {"letra": "C", "texto": r"$14$", "correta": False},
            {"letra": "D", "texto": r"$\frac{25}{2}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{9}{2}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_1 = 9$ e $q = 1/3$. 2. Como $|q| < 1$, $S_\infty = \frac{9}{1 - 1/3} = \frac{9}{2/3} = \frac{27}{2}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Aplique a fórmula $S = a_1 / (1 - q)$ com $q = 1/3$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se a sequência $(x, \; x + 3, \; 4x)$ forma uma PG com termos estritamente positivos, o valor de $x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3$", "correta": True},
            {"letra": "B", "texto": r"$1$", "correta": False},
            {"letra": "C", "texto": r"$2$", "correta": False},
            {"letra": "D", "texto": r"$4$", "correta": False},
            {"letra": "E", "texto": r"$9$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Propriedade da PG: $(x + 3)^2 = x \cdot 4x$. 2. $x^2 + 6x + 9 = 4x^2 \implies 3x^2 - 6x - 9 = 0 \implies x^2 - 2x - 3 = 0$. 3. $(x - 3)(x + 1) = 0 \implies x = 3$ (pois $x > 0$). Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Em uma PG de 3 termos, o quadrado do termo central é igual ao produto dos extremos."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule a soma dos 6 primeiros termos da PG finita $(3, 6, 12, 24, \dots)$.",
        "alternativas": [],
        "resposta_correta": "189",
        "resolucao_passo_a_passo": r"1. $a_1 = 3, q = 2$. 2. $S_6 = \frac{a_1(q^6 - 1)}{q - 1} = \frac{3(2^6 - 1)}{2 - 1} = 3(64 - 1) = 3 \cdot 63 = 189$.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "Use a fórmula da soma da PG finita: $S_n = a_1(q^n - 1)/(q - 1)$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A fração geratriz da dízima periódica simples $0{,}444\dots$ obtida via soma de PG infinita é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{4}{9}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{4}{10}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{2}{5}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{4}{99}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{44}{90}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $0{,}444\dots = \frac{4}{10} + \frac{4}{100} + \dots$, com $a_1 = 4/10$ e $q = 1/10$. 2. $S_\infty = \frac{4/10}{1 - 1/10} = \frac{4/10}{9/10} = \frac{4}{9}$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Represente a dízima como uma série de potências de 1/10."},
    },

    # --- Cap 4: Teoria das Matrizes e Álgebra Matricial (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se $A = \begin{bmatrix} 1 & 2 \\ 0 & 3 \end{bmatrix}$ e $B = \begin{bmatrix} 2 & -1 \\ 4 & 1 \end{bmatrix}$, o elemento $c_{21}$ da matriz produto $C = A \cdot B$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$12$", "correta": True},
            {"letra": "B", "texto": r"$10$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$3$", "correta": False},
            {"letra": "E", "texto": r"$0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $c_{21}$ é o produto escalar da 2ª linha de $A$ com a 1ª coluna de $B$. 2. $c_{21} = 0 \cdot 2 + 3 \cdot 4 = 0 + 12 = 12$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Multiplique os elementos da segunda linha de A pelos da primeira coluna de B e some."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dada a matriz $A = [a_{ij}]_{2 \times 2}$ com lei de formação $a_{ij} = 2i - j$, a soma de todos os elementos de $A$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$8$", "correta": False},
            {"letra": "D", "texto": r"$5$", "correta": False},
            {"letra": "E", "texto": r"$10$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $a_{11} = 2(1)-1 = 1$. $a_{12} = 2(1)-2 = 0$. 2. $a_{21} = 2(2)-1 = 3$. $a_{22} = 2(2)-2 = 2$. 3. Soma: $1 + 0 + 3 + 2 = 6$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Calcule cada um dos 4 elementos da matriz $2 \\times 2$ e some-os."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma matriz quadrada $M$ é dita simétrica se $M^t = M$. Para que a matriz $M = \begin{bmatrix} 2 & x - 1 \\ 5 & 3 \end{bmatrix}$ seja simétrica, devemos ter:",
        "alternativas": [
            {"letra": "A", "texto": r"$x = 6$", "correta": True},
            {"letra": "B", "texto": r"$x = 5$", "correta": False},
            {"letra": "C", "texto": r"$x = 4$", "correta": False},
            {"letra": "D", "texto": r"$x = -4$", "correta": False},
            {"letra": "E", "texto": r"$x = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A condição de simetria exige $a_{12} = a_{21}$. 2. $x - 1 = 5 \implies x = 6$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Iguale os elementos simétricos em relação à diagonal principal ($a_{12} = a_{21}$)."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Sejam $A$ de ordem $2 \times 3$ e $B$ de ordem $3 \times 4$. Quantos elementos possui a matriz produto $A \cdot B$?",
        "alternativas": [],
        "resposta_correta": "8",
        "resolucao_passo_a_passo": r"1. O produto $A_{2 \times 3} \cdot B_{3 \times 4}$ resulta em uma matriz $C$ de ordem $2 \times 4$. 2. Número de elementos: $2 \times 4 = 8$.",
        "parametro_a": 1.200,
        "parametro_b": -0.900,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "A dimensão resultante é $(2 \\times 4)$; multiplique o número de linhas pelo de colunas."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$. A matriz potência $A^3$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$\begin{bmatrix} 1 & 3 \\ 0 & 1 \end{bmatrix}$", "correta": True},
            {"letra": "B", "texto": r"$\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$", "correta": False},
            {"letra": "C", "texto": r"$\begin{bmatrix} 1 & 6 \\ 0 & 1 \end{bmatrix}$", "correta": False},
            {"letra": "D", "texto": r"$\begin{bmatrix} 3 & 3 \\ 0 & 3 \end{bmatrix}$", "correta": False},
            {"letra": "E", "texto": r"$\begin{bmatrix} 1 & 8 \\ 0 & 1 \end{bmatrix}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $A^2 = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$. 2. $A^3 = A^2 \cdot A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 0 & 1 \end{bmatrix}$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Calcule primeiro $A^2$ e depois multiplique o resultado por $A$."},
    },

    # --- Cap 5: Determinantes e Teorema de Laplace (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O determinante da matriz $A = \begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$10$", "correta": True},
            {"letra": "B", "texto": r"$14$", "correta": False},
            {"letra": "C", "texto": r"$-10$", "correta": False},
            {"letra": "D", "texto": r"$6$", "correta": False},
            {"letra": "E", "texto": r"$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Para matriz $2 \times 2$: $\det(A) = a_{11}a_{22} - a_{12}a_{21}$. 2. $\det(A) = 3 \cdot 4 - 2 \cdot 1 = 12 - 2 = 10$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Determinante $2\times 2$: produto da diagonal principal menos produto da diagonal secundária."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Seja $A$ uma matriz quadrada de ordem 3 tal que $\det(A) = 5$. O determinante da matriz $2A$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$40$", "correta": True},
            {"letra": "B", "texto": r"$10$", "correta": False},
            {"letra": "C", "texto": r"$30$", "correta": False},
            {"letra": "D", "texto": r"$20$", "correta": False},
            {"letra": "E", "texto": r"$80$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela propriedade de multiplicação por escalar: $\det(k A) = k^n \det(A)$. 2. Aqui $k = 2$ e a ordem é $n = 3$: $\det(2A) = 2^3 \cdot \det(A) = 8 \cdot 5 = 40$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Lembre-se de que o escalar é elevado à ordem da matriz: $k^n$."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor do determinante da matriz $M = \begin{bmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 0 & 0 & 6 \end{bmatrix}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$24$", "correta": True},
            {"letra": "B", "texto": r"$18$", "correta": False},
            {"letra": "C", "texto": r"$0$", "correta": False},
            {"letra": "D", "texto": r"$12$", "correta": False},
            {"letra": "E", "texto": r"$30$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Trata-se de uma matriz triangular superior. 2. O determinante de uma matriz triangular é o produto dos elementos da diagonal principal: $\det(M) = 1 \cdot 4 \cdot 6 = 24$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Em matrizes triangulares, o determinante é simplesmente o produto da diagonal principal."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule o determinante da matriz $A = \begin{bmatrix} 2 & 1 \\ 4 & 2 \end{bmatrix}$.",
        "alternativas": [],
        "resposta_correta": "0",
        "resolucao_passo_a_passo": r"1. $\det(A) = 2 \cdot 2 - 1 \cdot 4 = 4 - 4 = 0$. Note que a segunda linha é o dobro da primeira ($L_2 = 2L_1$).",
        "parametro_a": 1.200,
        "parametro_b": -1.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "Linhas proporcionais geram determinante nulo."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Sejam $A$ e $B$ matrizes quadradas de ordem 2 tais que $\det(A) = 3$ e $\det(B) = -2$. O valor de $\det(A \cdot B^{-1})$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-\frac{3}{2}$", "correta": True},
            {"letra": "B", "texto": r"$-6$", "correta": False},
            {"letra": "C", "texto": r"$\frac{3}{2}$", "correta": False},
            {"letra": "D", "texto": r"$6$", "correta": False},
            {"letra": "E", "texto": r"$-\frac{2}{3}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pelo Teorema de Binet: $\det(A \cdot B^{-1}) = \det(A) \cdot \det(B^{-1}) = \frac{\det(A)}{\det(B)}$. 2. $\det(A \cdot B^{-1}) = \frac{3}{-2} = -\frac{3}{2}$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Aplique $\det(B^{-1}) = 1/\det(B)$ junto ao Teorema de Binet."},
    },

    # --- Cap 6: Sistemas Lineares e Escalonamento Gaussiano (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor de $x$ na solução do sistema linear $\begin{cases} 3x + 2y = 13 \\ x - y = 1 \end{cases}$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$3$", "correta": True},
            {"letra": "B", "texto": r"$2$", "correta": False},
            {"letra": "C", "texto": r"$4$", "correta": False},
            {"letra": "D", "texto": r"$5$", "correta": False},
            {"letra": "E", "texto": r"$1$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Da 2ª equação: $y = x - 1$. 2. Substituindo na 1ª: $3x + 2(x - 1) = 13 \implies 5x - 2 = 13 \implies 5x = 15 \implies x = 3$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Isole y na segunda equação e substitua na primeira."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Para qual valor de $m$ o sistema $\begin{cases} 2x + my = 6 \\ x + 3y = 3 \end{cases}$ é impossível (SI)?",
        "alternativas": [
            {"letra": "A", "texto": r"Nenhum valor de $m$", "correta": True},
            {"letra": "B", "texto": r"$m = 6$", "correta": False},
            {"letra": "C", "texto": r"$m = 3$", "correta": False},
            {"letra": "D", "texto": r"$m = 2$", "correta": False},
            {"letra": "E", "texto": r"$m = 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $D = 2(3) - m(1) = 6 - m$. Se $m = 6$, $D = 0$. 2. Para $m = 6$: a 1ª equação fica $2x + 6y = 6$, que dividida por 2 resulta em $x + 3y = 3$, exatamente igual à 2ª equação! 3. Logo, para $m = 6$ o sistema é SPI (infinitas soluções). Para $m \neq 6$ é SPD. Portanto, não existe valor de $m$ que torne o sistema impossível. Alternativa A.",
        "parametro_a": 1.550,
        "parametro_b": 1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Cuidado: teste se para D=0 as equações se tornam idênticas (SPI) ou incompatíveis (SI)."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Considere o sistema linear escalonado $\begin{cases} x + 2y + z = 6 \\ y - 2z = 1 \\ 3z = 6 \end{cases}$. O valor da incógnita $x$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$-6$", "correta": True},
            {"letra": "B", "texto": r"$2$", "correta": False},
            {"letra": "C", "texto": r"$5$", "correta": False},
            {"letra": "D", "texto": r"$-2$", "correta": False},
            {"letra": "E", "texto": r"$4$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Da 3ª equação: $z = 2$. 2. Da 2ª: $y - 2(2) = 1 \implies y = 5$. 3. Da 1ª: $x + 2(5) + 2 = 6 \implies x + 12 = 6 \implies x = -6$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Resolva por retro-substituição: ache z na última linha, depois y e por fim x."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine a soma $x + y$ na solução do sistema $\begin{cases} 4x + 3y = 25 \\ 2x - y = 5 \end{cases}$.",
        "alternativas": [],
        "resposta_correta": "7",
        "resolucao_passo_a_passo": r"1. Multiplicamos a 2ª equação por 3: $6x - 3y = 15$. 2. Somamos com a 1ª: $10x = 40 \implies x = 4$. 3. $y = 2(4) - 5 = 3$. 4. Soma: $x + y = 4 + 3 = 7$.",
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "algebra_linear", "dica_estagio_2": "Elimine y multiplicando a segunda equação por 3 e somando as equações."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O sistema linear homogêneo $\begin{cases} x + 2y = 0 \\ 3x + ky = 0 \end{cases}$ admite solução não-trivial se, e somente se:",
        "alternativas": [
            {"letra": "A", "texto": r"$k = 6$", "correta": True},
            {"letra": "B", "texto": r"$k \neq 6$", "correta": False},
            {"letra": "C", "texto": r"$k = 0$", "correta": False},
            {"letra": "D", "texto": r"$k = 3$", "correta": False},
            {"letra": "E", "texto": r"$k \neq 0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Para admitir soluções além da trivial $(0, 0)$, o sistema homogêneo deve ser SPI ($\det(A) = 0$). 2. $\det(A) = 1 \cdot k - 2 \cdot 3 = k - 6 = 0 \implies k = 6$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "algebra_linear", "dica_estagio_2": "Sistema homogêneo admite soluções não-triviais se o determinante da matriz dos coeficientes for nulo."},
    },
]
