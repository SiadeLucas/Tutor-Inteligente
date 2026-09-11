"""
Módulo Canônico de Dados Didáticos — Volume 5: Combinatória e Probabilidade
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
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
}

# ============================================================================
# 1. CONTEÚDO DIDÁTICO DAS AULAS (AULAS_DATA)
# ============================================================================

AULAS_DATA = {
    1: {
        "teoria": r"""# Princípio Fundamental da Contagem (PFC)

A Análise Combinatória é o ramo da Matemática que desenvolve métodos sistemáticos para quantificar agrupamentos e configurações finitas sem a necessidade de enumerá-los exaustivamente um a um.

### 1. Princípio Aditivo
Se uma decisão $A$ pode ser tomada de $m$ maneiras e uma decisão $B$ pode ser tomada de $n$ maneiras, e essas decisões são mutuamente exclusivas ($A \cap B = \emptyset$), então a decisão "tomar $A$ **ou** $B$" pode ser realizada de:
$$m + n \quad \text{maneiras}$$

---

### 2. Princípio Multiplicativo (PFC)
Se uma ação é composta por $k$ etapas sucessivas e independentes, onde:
- A 1ª etapa pode ser tomada de $n_1$ maneiras;
- A 2ª etapa pode ser tomada de $n_2$ maneiras;
- $\dots$
- A $k$-ésima etapa pode ser tomada de $n_k$ maneiras;

então o número total de possibilidades para realizar o evento completo é o produto:
$$N = n_1 \cdot n_2 \cdot n_3 \cdots n_k$$

---

### 3. Diagrama de Árvore e Restrições
- **Árvore de Possibilidades**: representação gráfica onde cada ramificação ilustra as escolhas disponíveis em uma etapa subsequente.
- **Técnica de Resolução com Restrições**: quando um problema apresentar restrições especiais (ex: números pares, algarismos distintos, posições fixas), **comece sempre preenchendo as etapas mais restritivas**.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Montagem de Vestuário
**Enunciado:** Um estudante dispõe de 4 calças distintas, 5 camisas e 2 pares de sapatos. De quantas formas distintas ele pode se vestir escolhendo uma calça, uma camisa e um par de sapatos?

**Resolução Passo a Passo:**
1. A escolha é feita em 3 etapas sucessivas e independentes:
   - Etapa 1 (Calça): 4 opções.
   - Etapa 2 (Camisa): 5 opções.
   - Etapa 3 (Sapato): 2 opções.
2. Pelo Princípio Multiplicativo da Contagem:
   $$N = 4 \cdot 5 \cdot 2 = 40 \text{ maneiras distintas}$$

---

### Exemplo 2: Formação de Códigos com Restrições
**Enunciado:** Quantos números pares de 3 algarismos distintos podem ser formados utilizando apenas os algarismos $\{1, 2, 3, 4, 5, 6\}$?

**Resolução:**
1. Para o número ser par, o algarismo das unidades deve ser par: opções $\{2, 4, 6\}$ (3 possibilidades).
2. Preenchemos primeiro a restrição (unidades): 3 modos.
3. Preenchemos as centenas com os 5 algarismos restantes: 5 modos.
4. Preenchemos as dezenas com os 4 algarismos restantes: 4 modos.
5. Aplicando o PFC:
   $$N = 5 \cdot 4 \cdot 3 = 60 \text{ números pares distintos}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Prioridade das Restrições:**
> Nunca preencha as posições da esquerda para a direita se a restrição estiver na ponta direita (como paridade ou divisibilidade por 5). Atenda primeiro à casa das unidades para não gerar contagens ambíguas!

> [!TIP]
> A conjunção **"OU"** indica soma (Princípio Aditivo: eventos disjuntos). A conjunção **"E"** indica multiplicação (Princípio Multiplicativo: etapas encadeadas).
""",
    },
    2: {
        "teoria": r"""# Arranjos e Permutações Simples e com Repetição

Quando a ordem dos elementos altera o agrupamento formado, estamos lidando com problemas de **Arranjo** ou **Permutação**.

### 1. Fatorial de um Número Natural
Para $n \in \mathbb{N}$, define-se:
$$n! = \begin{cases} 1, & \text{se } n = 0 \text{ ou } n = 1 \\ n \cdot (n-1) \cdot (n-2) \cdots 2 \cdot 1, & \text{se } n \ge 2 \end{cases}$$

---

### 2. Arranjos Simples ($A_{n, p}$)
Agrupamentos ordenados de $p$ elementos escolhidos dentre $n$ elementos distintos ($p \le n$):
$$A_{n, p} = \frac{n!}{(n - p)!} = n(n - 1)(n - 2)\cdots(n - p + 1)$$
A ordem importa: $(A, B) \neq (B, A)$.

---

### 3. Permutações Simples ($P_n$)
Caso particular do arranjo onde todos os $n$ elementos disponíveis são utilizados ($p = n$):
$$P_n = A_{n, n} = n!$$
- **Anagramas**: permutações das letras de uma palavra.

---

### 4. Permutações com Elementos Repetidos ($P_n^{\alpha, \beta, \dots}$)
Quando entre os $n$ elementos existem elementos repetidos com frequências $\alpha, \beta, \dots$:
$$P_n^{\alpha, \beta, \dots} = \frac{n!}{\alpha! \cdot \beta! \cdots}$$

---

### 5. Permutações Circulares ($PC_n$)
Disposição de $n$ elementos em torno de um círculo fechado, onde rotações não produzem configurações novas:
$$PC_n = \frac{n!}{n} = (n - 1)!$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Anagramas com Letras Repetidas
**Enunciado:** Quantos anagramas distintos possui a palavra **BATATA**?

**Resolução Passo a Passo:**
1. A palavra BATATA possui 6 letras no total ($n = 6$).
2. Contamos as repetições:
   - Letra A: repete 3 vezes ($\alpha = 3$).
   - Letra T: repete 2 vezes ($\beta = 2$).
   - Letra B: ocorre 1 vez.
3. Aplicamos a fórmula da permutação com repetição:
   $$P_6^{3, 2} = \frac{6!}{3! \cdot 2!} = \frac{720}{6 \cdot 2} = \frac{720}{12} = 60$$
Portanto, existem 60 anagramas distintos.

---

### Exemplo 2: Arranjo Simples em Pódio
**Enunciado:** Oito atletas disputam a final dos 100m rasos. De quantas maneiras distintas podem ser preenchidas as medalhas de Ouro, Prata e Bronze?

**Resolução:**
1. Temos $n = 8$ atletas e $p = 3$ posições onde a ordem faz toda a diferença (Ouro $\neq$ Prata $\neq$ Bronze).
2. Trata-se de um Arranjo Simples:
   $$A_{8, 3} = \frac{8!}{(8 - 3)!} = 8 \cdot 7 \cdot 6 = 336 \text{ maneiras}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Permutações Circulares vs Lineares:**
> Em torno de uma mesa redonda, fixar um elemento elimina o grau de liberdade rotacional, gerando $(n-1)!$. Se a mesa for numerada ou as cadeiras forem etiquetadas, o problema volta a ser permutação linear comum ($n!$)!

> [!TIP]
> Quando elementos devem ficar "sempre juntos" em uma fila, trate o grupo como um único **superbloco**, permute os elementos externos e lembre-se de multiplicar pelas permutações internas dentro do bloco.
""",
    },
    3: {
        "teoria": r"""# Combinações Simples e Problemas de Escolha

Em muitos problemas práticos, a ordem de escolha dos elementos **não diferencia** o agrupamento resultante (ex: formar comissões, sortear equipes, selecionar ingredientes, desenhar triângulos ligando vértices).

### 1. Definição Formal de Combinação Simples
Uma **combinação simples** de $n$ elementos tomados $p$ a $p$ ($0 \le p \le n$) é qualquer subconjunto com $p$ elementos formado a partir de um conjunto de $n$ elementos distintos:
$$C_{n, p} = \binom{n}{p} = \frac{n!}{p! \cdot (n - p)!}$$
Relação fundamental com o Arranjo:
$$C_{n, p} = \frac{A_{n, p}}{p!}$$
onde a divisão por $p!$ elimina a redundância provocada pelas diferentes ordenações dos mesmos $p$ elementos.

---

### 2. Propriedades Canônicas dos Números Binomiais
1. **Extremos**: $\binom{n}{0} = 1$ e $\binom{n}{n} = 1$.
2. **Binomiais Complementares**:
   $$\binom{n}{p} = \binom{n}{n - p}$$
3. **Relação de Stifel**:
   $$\binom{n-1}{p-1} + \binom{n-1}{p} = \binom{n}{p}$$
4. **Teorema das Linhas do Triângulo de Pascal**:
   $$\sum_{p=0}^n \binom{n}{p} = \binom{n}{0} + \binom{n}{1} + \dots + \binom{n}{n} = 2^n$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Formação de Comissões Mistas
**Enunciado:** Em uma turma com 6 rapazes e 5 moças, de quantas maneiras podemos formar uma comissão de 4 pessoas contendo exatamente 2 rapazes e 2 moças?

**Resolução Passo a Passo:**
1. Como a ordem na comissão não importa, utilizamos combinações simples.
2. Escolha dos rapazes: dentre 6, escolhemos 2:
   $$C_{6, 2} = \frac{6 \cdot 5}{2 \cdot 1} = 15$$
3. Escolha das moças: dentre 5, escolhemos 2:
   $$C_{5, 2} = \frac{5 \cdot 4}{2 \cdot 1} = 10$$
4. Pelo PFC, multiplicamos as escolhas:
   $$N = C_{6, 2} \cdot C_{5, 2} = 15 \cdot 10 = 150 \text{ comissões}$$

---

### Exemplo 2: Geometria Combinatória
**Enunciado:** Quantos triângulos distintos podem ser formados tendo como vértices os vértices de um octógono regular convexo?

**Resolução:**
1. O octógono possui 8 vértices. Como nenhum conjunto de 3 vértices é colinear em um polígono regular convexo, quaisquer 3 vértices determinam um triângulo.
2. A ordem de escolha dos vértices não altera o triângulo ($\triangle ABC = \triangle BCA$).
3. Aplicamos a combinação:
   $$C_{8, 3} = \frac{8 \cdot 7 \cdot 6}{3 \cdot 2 \cdot 1} = \frac{336}{6} = 56 \text{ triângulos}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Arranjo ou Combinação? A Pergunta Chave:**
> Troque a ordem de dois elementos da amostra. O resultado mudou de identidade?
> - **SIM** (ex: senha de banco, pódio, presidente e vice) $\implies$ **Arranjo**.
> - **NÃO** (ex: comissão de trabalho, salada de frutas, cartas na mão) $\implies$ **Combinação**.

> [!TIP]
> Para problemas com a cláusula "pelo menos um", é quase sempre mais rápido calcular o **total irrestrito** e subtrair o **caso indesejado (nenhum)**.
""",
    },
    4: {
        "teoria": r"""# Binômio de Newton e Triângulo de Pascal

O Teorema do Binômio de Newton fornece a fórmula explícita para desenvolver algebricamente a potência inteira de um binômio $(x + a)^n$, onde $n \in \mathbb{N}$.

### 1. Triângulo de Pascal
Tabela triangular formada pelos coeficientes binomiais $\binom{n}{p}$, onde a linha representa $n$ ($n \ge 0$) e a coluna representa $p$ ($0 \le p \le n$):
```
n=0: 1
n=1: 1  1
n=2: 1  2  1
n=3: 1  3  3  1
n=4: 1  4  6  4  1
```
- **Relação de Stifel**: a soma de dois elementos consecutivos de uma mesma linha resulta no elemento imediatamente abaixo do segundo:
  $$\binom{n}{p} + \binom{n}{p+1} = \binom{n+1}{p+1}$$

---

### 2. Fórmula do Binômio de Newton
Para $x, a \in \mathbb{R}$ e $n \in \mathbb{N}$:
$$(x + a)^n = \sum_{p=0}^n \binom{n}{p} x^{n-p} a^p = \binom{n}{0} x^n + \binom{n}{1} x^{n-1} a + \dots + \binom{n}{n} a^n$$
- O desenvolvimento completo de $(x + a)^n$ possui exatamente **$n + 1$ termos**.

---

### 3. Fórmula do Termo Geral
O $(p+1)$-ésimo termo do desenvolvimento (denotado por $T_{p+1}$, com $0 \le p \le n$) é dado por:
$$T_{p+1} = \binom{n}{p} \cdot x^{n - p} \cdot a^p$$
- **Termo Independente de $x$**: termo no qual o expoente final de $x$ é igual a zero ($x^0$).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação do Termo Médio
**Enunciado:** Desenvolva o termo geral e determine o 4º termo de $(x + 2)^5$.

**Resolução Passo a Passo:**
1. Para o 4º termo, temos $p + 1 = 4 \implies p = 3$.
2. Na fórmula $T_{p+1} = \binom{n}{p} x^{n-p} a^p$, com $n = 5$, $a = 2$ e $p = 3$:
   $$T_4 = \binom{5}{3} x^{5-3} \cdot 2^3$$
3. Calculamos o binomial $\binom{5}{3} = \frac{5 \cdot 4}{2 \cdot 1} = 10$.
4. Substituindo:
   $$T_4 = 10 \cdot x^2 \cdot 8 = 80x^2$$

---

### Exemplo 2: Termo Independente de $x$
**Enunciado:** Calcule o termo independente de $x$ no desenvolvimento de $\left(x^2 + \frac{1}{x}\right)^6$.

**Resolução:**
1. Escrevemos o termo geral com $n = 6$:
   $$T_{p+1} = \binom{6}{p} (x^2)^{6-p} \left(\frac{1}{x}\right)^p = \binom{6}{p} x^{12 - 2p} \cdot x^{-p} = \binom{6}{p} x^{12 - 3p}$$
2. Para ser independente de $x$, o expoente de $x$ deve ser nulo:
   $$12 - 3p = 0 \implies 3p = 12 \implies p = 4$$
3. Calculamos o termo para $p = 4$:
   $$T_5 = \binom{6}{4} x^0 = \frac{6 \cdot 5}{2 \cdot 1} = 15$$
O termo independente é 15.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **O índice $p$ vs a ordem do termo:**
> O primeiro termo é $T_1$ (onde $p = 0$). Logo, no $k$-ésimo termo, **$p = k - 1$**! Não use $p = k$, pois isso apontará para o termo seguinte.

> [!TIP]
> Para encontrar a **soma de todos os coeficientes** de um polinômio binomial $(a x + b y)^n$, basta substituir todas as variáveis por $1$: $\text{Soma} = (a(1) + b(1))^n = (a + b)^n$.
""",
    },
    5: {
        "teoria": r"""# Conceito de Probabilidade e Espaço Amostral

A teoria das probabilidades quantifica a incerteza associada a experimentos aleatórios, fornecendo um modelo numérico formal entre 0 (impossível) e 1 (evento certo).

### 1. Conceitos Primitivos
- **Experimento Aleatório**: fenômeno que, mesmo repetido sob idênticas condições, pode apresentar resultados imprevisíveis (ex: lançar um dado, sortear uma carta).
- **Espaço Amostral ($\Omega$)**: conjunto de todos os resultados possíveis do experimento.
- **Evento ($E$)**: qualquer subconjunto do espaço amostral ($E \subseteq \Omega$).
  - Evento Impossível: $E = \emptyset \implies P(E) = 0$.
  - Evento Certo: $E = \Omega \implies P(E) = 1$.

---

### 2. Definição Clássica de Laplace (Espaços Equiprováveis)
Se o espaço amostral $\Omega$ é finito e todos os seus elementos têm a mesma chance de ocorrer (equiprováveis):
$$P(E) = \frac{n(E)}{n(\Omega)} = \frac{\text{número de casos favoráveis}}{\text{número de casos possíveis}}$$
Propriedade fundamental:
$$0 \le P(E) \le 1 \quad (0\% \le P(E) \le 100\%)$$

---

### 3. Probabilidade da União e do Evento Complementar
1. **Evento Complementar ($\bar{E}$ ou $E^c$)**: a não ocorrência de $E$.
   $$P(\bar{E}) = 1 - P(E)$$
2. **Teorema da Adição (União de Eventos)**:
   $$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
   Se os eventos forem mutuamente exclusivos ($A \cap B = \emptyset$):
   $$P(A \cup B) = P(A) + P(B)$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Lançamento de Dois Dados Honestos
**Enunciado:** Lançando-se dois dados honestos de 6 faces simultaneamente, qual é a probabilidade de a soma das faces ser igual a 7?

**Resolução Passo a Passo:**
1. O espaço amostral $\Omega$ é composto por pares ordenados $(d_1, d_2)$ com $n(\Omega) = 6 \times 6 = 36$ resultados equiprováveis.
2. O evento $E$ (soma igual a 7) consiste nos pares:
   $$E = \{(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)\}$$
   Temos $n(E) = 6$ casos favoráveis.
3. Aplicamos a probabilidade de Laplace:
   $$P(E) = \frac{n(E)}{n(\Omega)} = \frac{6}{36} = \frac{1}{6} \approx 16{,}67\%$$

---

### Exemplo 2: Probabilidade com Baralho
**Enunciado:** Retirando-se ao acaso uma carta de um baralho tradicional de 52 cartas, qual é a probabilidade de ela ser um Ás ou uma carta de Copas?

**Resolução:**
1. Total de cartas: $n(\Omega) = 52$.
2. Evento $A$ (Ás): existem 4 ases no baralho $\implies P(A) = 4/52$.
3. Evento $B$ (Copas): existem 13 cartas de copas $\implies P(B) = 13/52$.
4. Interseção $A \cap B$ (Ás de Copas): existe 1 carta $\implies P(A \cap B) = 1/52$.
5. Pelo teorema da adição:
   $$P(A \cup B) = \frac{4}{52} + \frac{13}{52} - \frac{1}{52} = \frac{16}{52} = \frac{4}{13}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Subtrair a Interseção:**
> Ao calcular a probabilidade da união de dois eventos ("Ás OU Copas"), sempre subtraia a probabilidade da interseção ("Ás DE Copas") para não contar o mesmo caso duas vezes!

> [!TIP]
> Em problemas com cartas ou bolas, certifique-se de identificar se a retirada é **com reposição** (espaço amostral permanece constante) ou **sem reposição** (o espaço amostral diminui a cada etapa).
""",
    },
    6: {
        "teoria": r"""# Probabilidade Condicional e Eventos Independentes

A probabilidade condicional modela como a ocorrência prévia de um determinado evento altera a probabilidade de outro evento, ao restringir o espaço amostral original.

### 1. Definição Formal de Probabilidade Condicional
A probabilidade de ocorrer o evento $A$, dado que o evento $B$ já ocorreu (com $P(B) > 0$), é indicada por $P(A \mid B)$ e calculada por:
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{n(A \cap B)}{n(B)}$$
O evento condicionante $B$ atua como o novo **espaço amostral reduzido**.

---

### 2. Teorema da Multiplicação
Isolando a interseção na definição de probabilidade condicional:
$$P(A \cap B) = P(B) \cdot P(A \mid B) = P(A) \cdot P(B \mid A)$$

---

### 3. Eventos Independentes
Dois eventos $A$ e $B$ são estritamente **independentes** se a ocorrência de um não afeta a probabilidade de ocorrência do outro:
$$P(A \mid B) = P(A) \quad \text{e} \quad P(B \mid A) = P(B)$$
- **Regra do Produto para Eventos Independentes**:
  $$P(A \cap B) = P(A) \cdot P(B)$$

---

### 4. Teorema da Probabilidade Total e Teorema de Bayes
Se $B_1, B_2, \dots, B_k$ formam uma partição do espaço amostral $\Omega$:
$$P(A) = \sum_{i=1}^k P(B_i) \cdot P(A \mid B_i)$$
- **Fórmula de Bayes**:
  $$P(B_j \mid A) = \frac{P(B_j) \cdot P(A \mid B_j)}{\sum_{i=1}^k P(B_i) \cdot P(A \mid B_i)}$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Probabilidade Condicional em Dados
**Enunciado:** Um dado honesto de 6 faces é lançado. Sabendo-se que o resultado obtido foi um número par, qual é a probabilidade de ter saído o número 6?

**Resolução Passo a Passo:**
1. Evento $B$ (o resultado foi par): $B = \{2, 4, 6\} \implies n(B) = 3$.
2. Evento $A$ (resultado igual a 6): $A = \{6\}$.
3. A interseção é $A \cap B = \{6\} \implies n(A \cap B) = 1$.
4. Como já sabemos que o resultado é par, o espaço amostral fica reduzido a $\{2, 4, 6\}$:
   $$P(A \mid B) = \frac{n(A \cap B)}{n(B)} = \frac{1}{3}$$

---

### Exemplo 2: Eventos Independentes em Moedas
**Enunciado:** Uma moeda honesta é lançada 3 vezes consecutivas. Qual é a probabilidade de obter coroa em todos os 3 lançamentos?

**Resolução:**
1. Cada lançamento é um evento independente dos anteriores, com $P(\text{Coroa}) = \frac{1}{2}$.
2. Pela regra do produto para eventos independentes:
   $$P(C_1 \cap C_2 \cap C_3) = P(C_1) \cdot P(C_2) \cdot P(C_3) = \frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{8}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Mutuamente Exclusivo $\neq$ Independente:**
> Eventos mutuamente exclusivos com probabilidades positivas **nunca** são independentes! Se $A \cap B = \emptyset$, saber que $B$ ocorreu garante que $A$ não ocorreu ($P(A \mid B) = 0 \neq P(A)$).

> [!TIP]
> Em problemas de probabilidade condicional descritos em tabelas de contingência, localize diretamente a linha ou coluna da condição dada e calcule a fração apenas dentro dessa fatia.
""",
    },
}

# ============================================================================
# 2. BATERIAS DE FIXAÇÃO (FIXACAO_DATA — 3 questões por capítulo)
# ============================================================================

FIXACAO_DATA = {
    1: [
        {
            "enunciado_katex": r"Um restaurante oferece um cardápio com 3 opções de entrada, 4 de prato principal e 2 de sobremesa. Quantas refeições completas distintas podem ser montadas escolhendo uma opção de cada tipo?",
            "alternativas": [
                {"letra": "A", "texto": r"$24$", "correta": True},
                {"letra": "B", "texto": r"$9$", "correta": False},
                {"letra": "C", "texto": r"$12$", "correta": False},
                {"letra": "D", "texto": r"$18$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Pelo Princípio Fundamental da Contagem: $3 \times 4 \times 2 = 24$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Quantos números de telefone celular de 2 dígitos podem ser formados utilizando apenas os algarismos $\{1, 2, 3, 4, 5\}$, se os algarismos puderem se repetir?",
            "alternativas": [
                {"letra": "A", "texto": r"$25$", "correta": True},
                {"letra": "B", "texto": r"$20$", "correta": False},
                {"letra": "C", "texto": r"$10$", "correta": False},
                {"letra": "D", "texto": r"$30$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Como pode repetir: $5 \times 5 = 25$ números. Alternativa A.",
        },
        {
            "enunciado_katex": r"Para acessar um cofre, deve-se digitar uma senha de 3 letras distintas escolhidas dentre as vogais $\{A, E, I, O, U\}$. Quantas senhas possíveis existem?",
            "alternativas": [
                {"letra": "A", "texto": r"$60$", "correta": True},
                {"letra": "B", "texto": r"$125$", "correta": False},
                {"letra": "C", "texto": r"$15$", "correta": False},
                {"letra": "D", "texto": r"$20$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Como as letras são distintas: $5 \times 4 \times 3 = 60$ senhas. Alternativa A.",
        },
    ],
    2: [
        {
            "enunciado_katex": r"De quantas maneiras 4 amigos podem se sentar em 4 cadeiras enfileiradas em um cinema?",
            "alternativas": [
                {"letra": "A", "texto": r"$24$", "correta": True},
                {"letra": "B", "texto": r"$16$", "correta": False},
                {"letra": "C", "texto": r"$12$", "correta": False},
                {"letra": "D", "texto": r"$8$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Permutação simples de 4 elementos: $P_4 = 4! = 4 \times 3 \times 2 \times 1 = 24$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Quantos anagramas distintos possui a palavra **MESA**?",
            "alternativas": [
                {"letra": "A", "texto": r"$24$", "correta": True},
                {"letra": "B", "texto": r"$12$", "correta": False},
                {"letra": "C", "texto": r"$4$", "correta": False},
                {"letra": "D", "texto": r"$48$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"A palavra MESA tem 4 letras distintas: $P_4 = 4! = 24$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Quantos anagramas distintos possui a palavra **BOLA** se as letras B e O devem permanecer sempre juntas nessa ordem?",
            "alternativas": [
                {"letra": "A", "texto": r"$6$", "correta": True},
                {"letra": "B", "texto": r"$12$", "correta": False},
                {"letra": "C", "texto": r"$24$", "correta": False},
                {"letra": "D", "texto": r"$2$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Tratando (BO) como um bloco único fixo, permutamos 3 blocos: (BO), L, A $\implies P_3 = 3! = 6$. Alternativa A.",
        },
    ],
    3: [
        {
            "enunciado_katex": r"De quantas maneiras podemos escolher uma comissão de 2 representantes a partir de um grupo de 6 estudantes?",
            "alternativas": [
                {"letra": "A", "texto": r"$15$", "correta": True},
                {"letra": "B", "texto": r"$30$", "correta": False},
                {"letra": "C", "texto": r"$12$", "correta": False},
                {"letra": "D", "texto": r"$36$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"A ordem na comissão não importa: $C_{6, 2} = \frac{6 \times 5}{2 \times 1} = 15$. Alternativa A.",
        },
        {
            "enunciado_katex": r"O valor do número binomial $\binom{7}{2}$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$21$", "correta": True},
                {"letra": "B", "texto": r"$42$", "correta": False},
                {"letra": "C", "texto": r"$14$", "correta": False},
                {"letra": "D", "texto": r"$35$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$\binom{7}{2} = \frac{7 \times 6}{2 \times 1} = 21$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Quantas diagonais possui um polígono regular convexo de 6 lados (hexágono)?",
            "alternativas": [
                {"letra": "A", "texto": r"$9$", "correta": True},
                {"letra": "B", "texto": r"$15$", "correta": False},
                {"letra": "C", "texto": r"$12$", "correta": False},
                {"letra": "D", "texto": r"$6$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Total de segmentos entre os 6 vértices é $C_{6,2} = 15$. Subtraindo os 6 lados: $15 - 6 = 9$ diagonais. Alternativa A.",
        },
    ],
    4: [
        {
            "enunciado_katex": r"Quantos termos possui o desenvolvimento completo do binômio $(x + y)^7$?",
            "alternativas": [
                {"letra": "A", "texto": r"$8$", "correta": True},
                {"letra": "B", "texto": r"$7$", "correta": False},
                {"letra": "C", "texto": r"$6$", "correta": False},
                {"letra": "D", "texto": r"$14$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"O número de termos no desenvolvimento de $(x + a)^n$ é sempre $n + 1$. Para $n = 7$, são $7 + 1 = 8$ termos. Alternativa A.",
        },
        {
            "enunciado_katex": r"A soma de todos os coeficientes do desenvolvimento de $(2x - 1)^5$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$1$", "correta": True},
                {"letra": "B", "texto": r"$32$", "correta": False},
                {"letra": "C", "texto": r"$243$", "correta": False},
                {"letra": "D", "texto": r"$0$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Basta fazer $x = 1$: $(2(1) - 1)^5 = 1^5 = 1$. Alternativa A.",
        },
        {
            "enunciado_katex": r"No Triângulo de Pascal, a soma de todos os elementos da linha $n = 4$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$16$", "correta": True},
                {"letra": "B", "texto": r"$32$", "correta": False},
                {"letra": "C", "texto": r"$8$", "correta": False},
                {"letra": "D", "texto": r"$15$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"A soma dos elementos da linha $n$ do Triângulo de Pascal é $2^n$. Para $n = 4$: $2^4 = 16$. Alternativa A.",
        },
    ],
    5: [
        {
            "enunciado_katex": r"No lançamento de um dado perfeito de 6 faces, a probabilidade de obter um número par é:",
            "alternativas": [
                {"letra": "A", "texto": r"$\frac{1}{2}$", "correta": True},
                {"letra": "B", "texto": r"$\frac{1}{3}$", "correta": False},
                {"letra": "C", "texto": r"$\frac{1}{6}$", "correta": False},
                {"letra": "D", "texto": r"$\frac{2}{3}$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Os números pares são $\{2, 4, 6\}$ (3 casos favoráveis entre 6 possíveis): $\frac{3}{6} = \frac{1}{2}$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Uma urna contém 3 bolas brancas e 7 bolas pretas. Retirando-se uma bola ao acaso, a probabilidade de ela ser branca é:",
            "alternativas": [
                {"letra": "A", "texto": r"$30\%$", "correta": True},
                {"letra": "B", "texto": r"$70\%$", "correta": False},
                {"letra": "C", "texto": r"$3\%$", "correta": False},
                {"letra": "D", "texto": r"$40\%$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Total de bolas: $3 + 7 = 10$. Probabilidade: $\frac{3}{10} = 30\%$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se a probabilidade de chover amanhã é de $0{,}35$, qual é a probabilidade do evento complementar (não chover)?",
            "alternativas": [
                {"letra": "A", "texto": r"$0{,}65$", "correta": True},
                {"letra": "B", "texto": r"$0{,}35$", "correta": False},
                {"letra": "C", "texto": r"$0{,}75$", "correta": False},
                {"letra": "D", "texto": r"$1{,}35$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$P(\bar{E}) = 1 - P(E) = 1 - 0{,}35 = 0{,}65$. Alternativa A.",
        },
    ],
    6: [
        {
            "enunciado_katex": r"Dois dados honestos são lançados. Sabendo que os dois números obtidos são iguais, qual é a probabilidade de que a soma deles seja 8?",
            "alternativas": [
                {"letra": "A", "texto": r"$\frac{1}{6}$", "correta": True},
                {"letra": "B", "texto": r"$\frac{1}{36}$", "correta": False},
                {"letra": "C", "texto": r"$\frac{1}{18}$", "correta": False},
                {"letra": "D", "texto": r"$\frac{1}{12}$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Condição dada: pares iguais $\{(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)\}$ (6 casos). Desses, apenas $(4,4)$ tem soma 8. Logo, $\frac{1}{6}$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se $A$ e $B$ são eventos independentes com $P(A) = 0{,}4$ e $P(B) = 0{,}5$, então $P(A \cap B)$ vale:",
            "alternativas": [
                {"letra": "A", "texto": r"$0{,}20$", "correta": True},
                {"letra": "B", "texto": r"$0{,}90$", "correta": False},
                {"letra": "C", "texto": r"$0{,}10$", "correta": False},
                {"letra": "D", "texto": r"$0{,}45$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Para eventos independentes: $P(A \cap B) = P(A) \cdot P(B) = 0{,}4 \times 0{,}5 = 0{,}20$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Em um grupo de 100 pessoas, 60 leem o jornal A, 40 leem o jornal B e 20 leem ambos. Escolhendo ao acaso um leitor do jornal A, a probabilidade de ele também ler o jornal B é:",
            "alternativas": [
                {"letra": "A", "texto": r"$\frac{1}{3}$", "correta": True},
                {"letra": "B", "texto": r"$\frac{1}{2}$", "correta": False},
                {"letra": "C", "texto": r"$\frac{1}{5}$", "correta": False},
                {"letra": "D", "texto": r"$\frac{2}{3}$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Espaço reduzido: leitores de A (60 pessoas). Casos favoráveis (leem B e A): 20 pessoas. Probabilidade condicional: $\frac{20}{60} = \frac{1}{3}$. Alternativa A.",
        },
    ],
}

# ============================================================================
# 3. FRAGMENTOS CANÔNICOS PARA O RAG (RAG_DATA — 1 por capítulo)
# ============================================================================

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "titulo": "Princípio Fundamental da Contagem (Multiplicativo e Aditivo)",
        "conteudo_markdown": r"""O Princípio Fundamental da Contagem (PFC) estabelece que uma ação composta por decisões sequenciais independentes com $n_1, n_2, \dots, n_k$ alternativas tem $n_1 \cdot n_2 \cdots n_k$ maneiras de ocorrer. Decisões mutuamente exclusivas obedecem ao princípio aditivo, somando as alternativas disponíveis.""",
    },
    {
        "numero_capitulo": 2,
        "titulo": "Permutações Simples, Circulares e com Repetição",
        "conteudo_markdown": r"""O número de ordenações lineares de $n$ elementos distintos é $P_n = n!$. Se houver repetições de elementos com frequências $\alpha, \beta$, o total reduz para $\frac{n!}{\alpha! \beta!}$. Em arranjos circulares sem pontos fixos de referência, a rotação gera $(n-1)!$ configurações distintas.""",
    },
    {
        "numero_capitulo": 3,
        "titulo": "Combinações Simples e Relações Binomiais",
        "conteudo_markdown": r"""Combinação simples quantifica subconjuntos de $p$ elementos a partir de $n$ elementos disponíveis sem distinção de ordem interna: $C_{n,p} = \binom{n}{p} = \frac{n!}{p!(n-p)!}$. Satisfaz a simetria complementar $\binom{n}{p} = \binom{n}{n-p}$ e a relação recursiva de Stifel $\binom{n-1}{p-1} + \binom{n-1}{p} = \binom{n}{p}$.""",
    },
    {
        "numero_capitulo": 4,
        "titulo": "Teorema do Binômio de Newton e Fórmula do Termo Geral",
        "conteudo_markdown": r"""O desenvolvimento de $(x + a)^n$ é expresso por $\sum_{p=0}^n \binom{n}{p} x^{n-p} a^p$. O $(p+1)$-ésimo termo é dado explicitamente por $T_{p+1} = \binom{n}{p} x^{n-p} a^p$. A soma de todos os coeficientes binomiais de ordem $n$ no Triângulo de Pascal equivale a $2^n$.""",
    },
    {
        "numero_capitulo": 5,
        "titulo": "Probabilidade Clássica de Laplace e Teorema da Adição",
        "conteudo_markdown": r"""Em espaços amostrais finitos e equiprováveis $\Omega$, a probabilidade de um evento $E$ é a razão entre a cardinalidade dos casos favoráveis e a cardinalidade total: $P(E) = \frac{n(E)}{n(\Omega)}$. Para dois eventos quaisquer, vale $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.""",
    },
    {
        "numero_capitulo": 6,
        "titulo": "Probabilidade Condicional e Critério de Independência",
        "conteudo_markdown": r"""A probabilidade de $A$ condicionada à ocorrência prévia de $B$ é $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$. Dois eventos são estritamente independentes se, e somente se, a probabilidade conjunta fatoriza no produto das probabilidades marginais: $P(A \cap B) = P(A) \cdot P(B)$.""",
    },
]

# ============================================================================
# 4. ITENS CALIBRADOS TRI (TRI_DATA — 5 itens por capítulo = 30 itens)
# ============================================================================

TRI_DATA = [
    # --- Cap 1: Princípio Fundamental da Contagem (PFC) (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma pessoa possui $4$ camisetas e $3$ calças distintas. De quantas maneiras diferentes ela pode se vestir escolhendo uma camiseta e uma calça?",
        "alternativas": [
            {"letra": "A", "texto": r"$12$", "correta": True},
            {"letra": "B", "texto": r"$7$", "correta": False},
            {"letra": "C", "texto": r"$24$", "correta": False},
            {"letra": "D", "texto": r"$10$", "correta": False},
            {"letra": "E", "texto": r"$34$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pelo Princípio Fundamental da Contagem, escolhas sucessivas se multiplicam. 2. Total $= 4 \times 3 = 12$ maneiras. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O PFC diz que decisões independentes em sequência se multiplicam: multiplique as opções de cada escolha."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos números naturais de 3 algarismos distintos podemos formar utilizando os algarismos do conjunto $\{1, 2, 3, 4, 5\}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$60$", "correta": True},
            {"letra": "B", "texto": r"$125$", "correta": False},
            {"letra": "C", "texto": r"$120$", "correta": False},
            {"letra": "D", "texto": r"$15$", "correta": False},
            {"letra": "E", "texto": r"$20$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. 1º algarismo: 5 opções. 2. 2º algarismo: 4 opções. 3. 3º algarismo: 3 opções. 4. Total: $5 \times 4 \times 3 = 60$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Como os algarismos são distintos, a cada casa decimal temos uma opção a menos."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos números pares de 3 algarismos distintos podem ser formados utilizando apenas os algarismos $\{1, 2, 3, 4, 6, 7\}$?",
        "alternativas": [
            {"letra": "A", "texto": r"$60$", "correta": True},
            {"letra": "B", "texto": r"$36$", "correta": False},
            {"letra": "C", "texto": r"$72$", "correta": False},
            {"letra": "D", "texto": r"$120$", "correta": False},
            {"letra": "E", "texto": r"$48$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Unidades: deve ser par $\{2, 4, 6\}$ (3 possibilidades). 2. Centenas: sobram 5 algarismos. 3. Dezenas: sobram 4 algarismos. 4. Total: $3 \times 5 \times 4 = 60$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Preencha primeiro a casa das unidades com as opções pares."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Em uma prova com 5 questões de verdadeiro ou falso, quantas folhas de resposta distintas são possíveis?",
        "alternativas": [],
        "resposta_correta": "32",
        "resolucao_passo_a_passo": r"1. Cada questão possui 2 opções (V ou F). 2. Total de gabaritos possíveis: $2^5 = 32$.",
        "parametro_a": 1.300,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Calcule $2$ elevado ao número de questões."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos números de 4 algarismos (não necessariamente distintos) existem no sistema de numeração decimal?",
        "alternativas": [
            {"letra": "A", "texto": r"$9.000$", "correta": True},
            {"letra": "B", "texto": r"$10.000$", "correta": False},
            {"letra": "C", "texto": r"$4.536$", "correta": False},
            {"letra": "D", "texto": r"$8.999$", "correta": False},
            {"letra": "E", "texto": r"$9.999$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. 1º algarismo (milhar): não pode ser zero $\implies 9$ opções $\{1, \dots, 9\}$. 2. 2º, 3º e 4º algarismos: 10 opções cada. 3. Total: $9 \times 10 \times 10 \times 10 = 9.000$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O primeiro algarismo não pode ser zero; as demais casas têm 10 escolhas possíveis."},
    },

    # --- Cap 2: Arranjos e Permutações Simples e com Repetição (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"De quantas maneiras distintas $5$ pessoas podem se posicionar em uma fila indiana?",
        "alternativas": [
            {"letra": "A", "texto": r"$120$", "correta": True},
            {"letra": "B", "texto": r"$25$", "correta": False},
            {"letra": "C", "texto": r"$60$", "correta": False},
            {"letra": "D", "texto": r"$24$", "correta": False},
            {"letra": "E", "texto": r"$720$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O número de permutações de $n$ elementos distintos é $P_n = n!$. 2. Para $n = 5$: $P_5 = 5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Permutação simples de $n$ pessoas em fila é $n!$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O número de anagramas distintos da palavra **ARARA** é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$10$", "correta": True},
            {"letra": "B", "texto": r"$120$", "correta": False},
            {"letra": "C", "texto": r"$20$", "correta": False},
            {"letra": "D", "texto": r"$30$", "correta": False},
            {"letra": "E", "texto": r"$5$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A palavra tem 5 letras: 3 A's e 2 R's. 2. Permutação com repetição: $P_5^{3, 2} = \frac{5!}{3! \cdot 2!} = \frac{120}{6 \cdot 2} = \frac{120}{12} = 10$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Divida o fatorial do total de letras pelo produto dos fatoriais das repetições."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma corrida com 10 participantes, de quantas maneiras distintas podem ser distribuídas as medalhas de 1º, 2º e 3º lugares?",
        "alternativas": [
            {"letra": "A", "texto": r"$720$", "correta": True},
            {"letra": "B", "texto": r"$120$", "correta": False},
            {"letra": "C", "texto": r"$1.000$", "correta": False},
            {"letra": "D", "texto": r"$504$", "correta": False},
            {"letra": "E", "texto": r"$240$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A ordem importa (pódio). 2. $A_{10, 3} = \frac{10!}{(10 - 3)!} = 10 \times 9 \times 8 = 720$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Como a ordem dos três primeiros colocados importa, utilize arranjo simples: $10 \\times 9 \\times 8$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"De quantas maneiras 5 pessoas podem se sentar ao redor de uma mesa circular (permutação circular)?",
        "alternativas": [],
        "resposta_correta": "24",
        "resolucao_passo_a_passo": r"1. Em torno de uma mesa circular, $PC_n = (n - 1)!$. 2. Para $n = 5$: $PC_5 = (5 - 1)! = 4! = 24$.",
        "parametro_a": 1.400,
        "parametro_b": 0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Para permutações circulares, use a fórmula $(n-1)!$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos anagramas da palavra **LIVRO** começam e terminam por consoante?",
        "alternativas": [
            {"letra": "A", "texto": r"$36$", "correta": True},
            {"letra": "B", "texto": r"$72$", "correta": False},
            {"letra": "C", "texto": r"$24$", "correta": False},
            {"letra": "D", "texto": r"$48$", "correta": False},
            {"letra": "E", "texto": r"$18$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Consoantes: L, V, R (3 opções); Vogais: I, O (2 opções). 2. 1ª letra (consoante): 3 opções. 3. Última letra (outra consoante): 2 opções. 4. As 3 letras do meio permutam livremente: $3! = 6$. 5. Total: $3 \times 2 \times 6 = 36$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Fixe as consoantes nos extremos e permute as 3 letras restantes no centro."},
    },

    # --- Cap 3: Combinações Simples e Problemas de Escolha (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantas comissões distintas de $3$ pessoas podem ser formadas a partir de um grupo de $10$ pessoas?",
        "alternativas": [
            {"letra": "A", "texto": r"$120$", "correta": True},
            {"letra": "B", "texto": r"$720$", "correta": False},
            {"letra": "C", "texto": r"$30$", "correta": False},
            {"letra": "D", "texto": r"$1000$", "correta": False},
            {"letra": "E", "texto": r"$360$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Como a ordem não importa (comissão), usamos combinação: $C_{10,3} = \frac{10!}{3!\,7!}$. 2. $C_{10,3} = \frac{10 \times 9 \times 8}{3 \times 2 \times 1} = \frac{720}{6} = 120$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Se a ordem não importa (formar grupo), use $C_{n,p} = \\frac{n!}{p!(n-p)!}$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantas retas distintas ficam determinadas por 7 pontos no plano, sabendo que não há 3 pontos colineares?",
        "alternativas": [
            {"letra": "A", "texto": r"$21$", "correta": True},
            {"letra": "B", "texto": r"$42$", "correta": False},
            {"letra": "C", "texto": r"$14$", "correta": False},
            {"letra": "D", "texto": r"$35$", "correta": False},
            {"letra": "E", "texto": r"$28$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cada reta é determinada por um par de pontos ($n = 7, p = 2$). 2. $C_{7, 2} = \frac{7 \times 6}{2 \times 1} = 21$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Dois pontos determinam uma reta única: calcule a combinação dos pontos tomados 2 a 2."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma sala há 5 homens e 4 mulheres. De quantas maneiras podemos formar uma comissão de 3 pessoas contendo pelo menos 1 mulher?",
        "alternativas": [
            {"letra": "A", "texto": r"$74$", "correta": True},
            {"letra": "B", "texto": r"$84$", "correta": False},
            {"letra": "C", "texto": r"$64$", "correta": False},
            {"letra": "D", "texto": r"$50$", "correta": False},
            {"letra": "E", "texto": r"$70$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Total de pessoas: $5 + 4 = 9$. Comissões totais de 3 pessoas: $C_{9, 3} = \frac{9 \times 8 \times 7}{6} = 84$. 2. Comissões sem nenhuma mulher (só homens): $C_{5, 3} = \frac{5 \times 4}{2} = 10$. 3. Comissões com pelo menos 1 mulher: $84 - 10 = 74$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Técnica do complementar: subtraia do total de comissões aquelas formadas exclusivamente por homens."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine o número de apertos de mão trocados em uma reunião com 8 pessoas, sabendo que todas se cumprimentaram exatamente uma vez.",
        "alternativas": [],
        "resposta_correta": "28",
        "resolucao_passo_a_passo": r"1. Cada aperto de mão é uma escolha não-ordenada de 2 pessoas entre 8. 2. $C_{8, 2} = \frac{8 \times 7}{2 \times 1} = 28$.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Cada aperto de mão envolve uma dupla: use $C_{8, 2}$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Quantos jogos ocorrem em um torneio de xadrez com 12 competidores, se cada jogador enfrenta todos os outros uma única vez?",
        "alternativas": [
            {"letra": "A", "texto": r"$66$", "correta": True},
            {"letra": "B", "texto": r"$132$", "correta": False},
            {"letra": "C", "texto": r"$72$", "correta": False},
            {"letra": "D", "texto": r"$144$", "correta": False},
            {"letra": "E", "texto": r"$55$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Cada partida reúne 2 jogadores entre os 12. 2. $C_{12, 2} = \frac{12 \times 11}{2 \times 1} = 66$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule a combinação de 12 jogadores tomados 2 a 2."},
    },

    # --- Cap 4: Binômio de Newton e Triângulo de Pascal (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O coeficiente do termo em $x^2$ no desenvolvimento de $(x + 2)^4$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$24$", "correta": True},
            {"letra": "B", "texto": r"$16$", "correta": False},
            {"letra": "C", "texto": r"$12$", "correta": False},
            {"letra": "D", "texto": r"$6$", "correta": False},
            {"letra": "E", "texto": r"$32$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Termo geral: $T_{p+1} = \binom{4}{p} x^{4-p} 2^p$. 2. Para $x^2$, fazemos $4 - p = 2 \implies p = 2$. 3. $T_3 = \binom{4}{2} x^2 \cdot 2^2 = 6 \cdot x^2 \cdot 4 = 24x^2$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Aplique a fórmula do termo geral do binômio para encontrar o coeficiente de $x^2$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A soma de todos os coeficientes do desenvolvimento de $(3x - 2y)^6$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$1$", "correta": True},
            {"letra": "B", "texto": r"$64$", "correta": False},
            {"letra": "C", "texto": r"$729$", "correta": False},
            {"letra": "D", "texto": r"$0$", "correta": False},
            {"letra": "E", "texto": r"$15.625$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A soma dos coeficientes é obtida atribuindo valor 1 às variáveis: $x = 1$ e $y = 1$. 2. $(3(1) - 2(1))^6 = (3 - 2)^6 = 1^6 = 1$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Para encontrar a soma dos coeficientes de qualquer binômio, faça as variáveis iguais a 1."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Quantos termos possui o desenvolvimento do binômio $(2x + 5y)^9$?",
        "alternativas": [],
        "resposta_correta": "10",
        "resolucao_passo_a_passo": r"1. O número de termos de $(a + b)^n$ é dado por $n + 1$. 2. Para $n = 9$: $9 + 1 = 10$.",
        "parametro_a": 1.150,
        "parametro_b": -1.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "O número de termos é sempre uma unidade a mais que o expoente."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"No Triângulo de Pascal, a soma $\binom{8}{3} + \binom{8}{4}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$\binom{9}{4}$", "correta": True},
            {"letra": "B", "texto": r"$\binom{8}{7}$", "correta": False},
            {"letra": "C", "texto": r"$\binom{9}{3}$", "correta": False},
            {"letra": "D", "texto": r"$\binom{16}{7}$", "correta": False},
            {"letra": "E", "texto": r"$\binom{9}{5}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela Relação de Stifel: $\binom{n}{p} + \binom{n}{p+1} = \binom{n+1}{p+1}$. 2. Para $n = 8$ e $p = 3$: $\binom{8}{3} + \binom{8}{4} = \binom{9}{4}$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Aplique diretamente a identidade de Stifel."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O termo independente de $x$ no desenvolvimento de $\left(x + \frac{1}{x}\right)^4$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$1$", "correta": False},
            {"letra": "D", "texto": r"$8$", "correta": False},
            {"letra": "E", "texto": r"$12$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $T_{p+1} = \binom{4}{p} x^{4-p} (x^{-1})^p = \binom{4}{p} x^{4 - 2p}$. 2. Independente de $x \implies 4 - 2p = 0 \implies p = 2$. 3. $T_3 = \binom{4}{2} = 6$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Iguale o expoente de x a zero para encontrar o valor de p correspondente."},
    },

    # --- Cap 5: Conceito de Probabilidade e Espaço Amostral (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Lançando-se simultaneamente dois dados honestos de $6$ faces, a probabilidade de a soma dos resultados ser igual a $7$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{6}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{12}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{7}{36}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{1}{9}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{5}{36}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O espaço amostral tem $6 \times 6 = 36$ resultados equiprováveis. 2. Os pares com soma $7$ são: $(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)$ — $6$ casos favoráveis. 3. $P = \frac{6}{36} = \frac{1}{6}$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 1.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Conte o espaço amostral ($36$ pares) e liste os casos favoráveis à soma $7$: são $6$ pares distintos."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma urna contém 4 bolas azuis e 6 bolas vermelhas. Sorteando-se uma bola ao acaso, qual é a probabilidade de ela ser azul?",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{2}{5}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{3}{5}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{1}{4}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{2}{3}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{2}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Total de bolas: $4 + 6 = 10$. 2. Bolas azuis: 4. 3. $P = \frac{4}{10} = \frac{2}{5} = 40\%$. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.000,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Divida a quantidade de bolas azuis pelo total de bolas na urna."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um número de 1 a 20 é escolhido aleatoriamente. Qual é a probabilidade percentual (de 0 a 100) de ser escolhido um múltiplo de 5?",
        "alternativas": [],
        "resposta_correta": "20",
        "resolucao_passo_a_passo": r"1. Os múltiplos de 5 entre 1 e 20 são $\{5, 10, 15, 20\}$ (4 números). 2. Probabilidade: $\frac{4}{20} = \frac{1}{5} = 20\%$.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Identifique quantos múltiplos de 5 existem de 1 a 20 e calcule a porcentagem em relação a 20."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Lançando-se uma moeda honesta 3 vezes consecutivas, a probabilidade de obter exatamente duas coroas é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{3}{8}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{8}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{1}{2}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{1}{4}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{5}{8}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Espaço amostral: $2^3 = 8$ sequências. 2. Casos com 2 coroas e 1 cara: $(C, C, K), (C, K, C), (K, C, C)$ — 3 casos. 3. $P = \frac{3}{8}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O espaço amostral tem 8 sequências equiprováveis; liste as que contêm exatamente 2 coroas."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma roleta com números de 1 a 36, a probabilidade de sortear um número primo menor que 10 é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{9}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{5}{36}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{1}{6}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{1}{12}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{18}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Os números primos menores que 10 são $\{2, 3, 5, 7\}$ (4 casos). 2. $P = \frac{4}{36} = \frac{1}{9}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Lembre-se de que 1 não é primo; os primos menores que 10 são 2, 3, 5 e 7."},
    },

    # --- Cap 6: Probabilidade Condicional e Eventos Independentes (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Lança-se um dado honesto de 6 faces. Sabendo que o número obtido foi maior que 2, a probabilidade de que ele seja primo é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{1}{2}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{3}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{2}{3}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{3}{4}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{4}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Espaço amostral reduzido (maior que 2): $\{3, 4, 5, 6\}$ (4 elementos). 2. Números primos desse conjunto: $\{3, 5\}$ (2 elementos). 3. Probabilidade condicional: $P = \frac{2}{4} = \frac{1}{2}$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Restrinja o espaço aos números maiores que 2 e conte os primos existentes nessa lista."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Dois eventos $A$ e $B$ são independentes tais que $P(A) = 0{,}30$ e $P(B) = 0{,}60$. O valor de $P(A \cup B)$ é:",
        "alternativas": [
            {"letra": "A", "texto": r"$0{,}72$", "correta": True},
            {"letra": "B", "texto": r"$0{,}90$", "correta": False},
            {"letra": "C", "texto": r"$0{,}18$", "correta": False},
            {"letra": "D", "texto": r"$0{,}60$", "correta": False},
            {"letra": "E", "texto": r"$0{,}82$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Como são independentes, $P(A \cap B) = P(A) \cdot P(B) = 0{,}30 \times 0{,}60 = 0{,}18$. 2. Teorema da adição: $P(A \cup B) = P(A) + P(B) - P(A \cap B) = 0{,}30 + 0{,}60 - 0{,}18 = 0{,}72$. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule a interseção pelo produto e aplique $P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma urna tem 5 bolas vermelhas e 5 bolas pretas. Retiram-se duas bolas sucessivamente e sem reposição. A probabilidade de ambas serem vermelhas é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{2}{9}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{1}{4}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{1}{2}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{5}{18}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{9}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. 1ª retirada: $P(V_1) = \frac{5}{10} = \frac{1}{2}$. 2. 2ª retirada (sem reposição): sobram 9 bolas, sendo 4 vermelhas $\implies P(V_2 \mid V_1) = \frac{4}{9}$. 3. $P = \frac{1}{2} \times \frac{4}{9} = \frac{2}{9}$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Atenção: como não há reposição, a segunda retirada tem 4 favoráveis em 9 possíveis."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Dois atiradores disparam simultaneamente contra um alvo. A probabilidade de o primeiro acertar é $0{,}8$ e a do segundo é $0{,}7$. Sendo os disparos independentes, determine a probabilidade percentual (de 0 a 100) de que ambos acertem o alvo.",
        "alternativas": [],
        "resposta_correta": "56",
        "resolucao_passo_a_passo": r"1. Para eventos independentes: $P(A \cap B) = P(A) \cdot P(B)$. 2. $P = 0{,}8 \times 0{,}7 = 0{,}56 = 56\%$.",
        "parametro_a": 1.300,
        "parametro_b": 0.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Multiplique as probabilidades individuais dos dois atiradores."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma moeda viciada tem probabilidade de dar cara igual a $\frac{2}{3}$. Lançando essa moeda 2 vezes de forma independente, a probabilidade de sair cara exatamente uma vez é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{4}{9}$", "correta": True},
            {"letra": "B", "texto": r"$\frac{2}{9}$", "correta": False},
            {"letra": "C", "texto": r"$\frac{1}{3}$", "correta": False},
            {"letra": "D", "texto": r"$\frac{5}{9}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{1}{2}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $P(\text{Cara}) = 2/3$, $P(\text{Coroa}) = 1/3$. 2. As ordens possíveis para exatamente uma cara são (Cara, Coroa) e (Coroa, Cara). 3. $P = 2 \times \left(\frac{2}{3} \times \frac{1}{3}\right) = 2 \times \frac{2}{9} = \frac{4}{9}$. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.850,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Lembre-se de considerar as duas ordens possíveis: (Cara, Coroa) e (Coroa, Cara)."},
    },
]
