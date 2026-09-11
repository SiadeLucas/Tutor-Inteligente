"""
Módulo Canônico de Dados Didáticos — Volume 11: Matemática Financeira e Estatística Descritiva
Coleção: Fundamentos de Matemática Elementar (Gelson Iezzi)
Contém: AULAS_DATA (6 caps), FIXACAO_DATA (18 questões), RAG_DATA (6 fragmentos), TRI_DATA (30 itens).
"""

VOLUME_INFO = {
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
}

# ============================================================================
# 1. CONTEÚDO DIDÁTICO DAS AULAS (AULAS_DATA)
# ============================================================================

AULAS_DATA = {
    1: {
        "teoria": r"""# Razão, Proporção e Grandezas Proporcionais

A teoria das grandezas proporcionais é a espinha dorsal quantitativa de aplicações em Física, Engenharia, Economia e Ciências Sociais.

### 1. Razão e Proporção Numérica
- **Razão**: Dados dois números reais $a$ e $b$ ($b \neq 0$), a razão entre $a$ e $b$ é o quociente:
  $$r = \frac{a}{b}$$
  onde $a$ é o antecedente e $b$ o consequente.
- **Proporção**: É a igualdade entre duas razões:
  $$\frac{a}{b} = \frac{c}{d} \quad (b, d \neq 0)$$
  - **Propriedade Fundamental das Proporções**: O produto dos extremos é igual ao produto dos meios:
    $$a \cdot d = b \cdot c$$

---

### 2. Grandezas Diretamente e Inversamente Proporcionais
- **Diretamente Proporcionais**: Duas grandezas $X$ e $Y$ são diretamente proporcionais quando a razão entre valores correspondentes é constante:
  $$\frac{y}{x} = k \iff y = k \cdot x \quad (k > 0)$$
  Se $x$ dobra, $y$ também dobra. O gráfico de $y$ em função de $x$ é uma reta que passa pela origem.
- **Inversamente Proporcionais**: Duas grandezas $X$ e $Y$ são inversamente proporcionais quando o produto de valores correspondentes é constante:
  $$x \cdot y = k \iff y = \frac{k}{x} \quad (k > 0)$$
  Se $x$ dobra, $y$ cai pela metade. O gráfico de $y$ em função de $x$ é uma hipérbole equilátera.

---

### 3. Regra de Três Simples e Composta
A regra de três composta articula três ou mais grandezas simultâneas.
- **Método das Razões**:
  1. Fixa-se a grandeza que contém a incógnita como referência.
  2. Compara-se individualmente cada uma das outras grandezas com a referência para identificar se são direta ou inversamente proporcionais.
  3. Iguala-se a razão da incógnita ao produto das demais razões (invertendo as grandezas inversas).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Divisão em Partes Proporcionais
**Enunciado:** Uma quantia de $R\$\,1.800{,}00$ deve ser dividida entre duas pessoas em partes diretamente proporcionais às suas idades, que são 12 e 18 anos. Quanto receberá a pessoa mais velha?

**Resolução Passo a Passo:**
1. Sejam $x$ e $y$ os valores recebidos, proporcionais a 12 e 18:
   $$\frac{x}{12} = \frac{y}{18} = k \implies x = 12k, \; y = 18k$$
2. A soma total deve ser 1.800:
   $$12k + 18k = 1.800 \implies 30k = 1.800 \implies k = 60$$
3. Calculamos o valor da pessoa mais velha ($y$):
   $$y = 18 \cdot 60 = 1.080$$
A pessoa mais velha receberá $R\$\,1.080{,}00$.

---

### Exemplo 2: Regra de Três Composta
**Enunciado:** Se 6 operários constroem 120 metros de muro em 8 dias, quantos operários de mesma capacidade seriam necessários para construir 300 metros de muro em 10 dias?

**Resolução:**
1. Grandezas: Operários ($O$), Muro ($M$), Dias ($D$).
   - $O_1 = 6, M_1 = 120, D_1 = 8$
   - $O_2 = x, M_2 = 300, D_2 = 10$
2. Analisando a relação em relação a Operários:
   - Mais muro $\implies$ mais operários necessários (**Direta**).
   - Mais dias disponíveis $\implies$ menos operários necessários (**Inversa**).
3. Montamos a equação:
   $$\frac{6}{x} = \frac{120}{300} \cdot \frac{10}{8}$$
4. Simplificando as frações:
   $$\frac{120}{300} = \frac{2}{5}, \quad \frac{10}{8} = \frac{5}{4} \implies \frac{6}{x} = \frac{2}{5} \cdot \frac{5}{4} = \frac{2}{4} = \frac{1}{2}$$
5. Logo:
   $$x = 6 \cdot 2 = 12 \text{ operários}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Inversão de Grandezas:**
> Na regra de três, grandezas como velocidade, tempo, número de trabalhadores para a mesma tarefa ou vazão de torneiras são frequentemente **inversamente proporcionais**. Lembre-se sempre de inverter essas frações antes de multiplicar!

> [!TIP]
> Em divisão em partes inversamente proporcionais a $a, b, c$, divida em partes diretamente proporcionais aos inversos $\frac{1}{a}, \frac{1}{b}, \frac{1}{c}$.
""",
    },
    2: {
        "teoria": r"""# Porcentagem, Lucro e Prejuízo Comercial

A porcentagem expressa frações com denominador 100, servindo como a métrica universal de comparação relativa nos mercados financeiros e comerciais.

### 1. Definição e Fatores de Atualização
- **Definição**: $p\% = \frac{p}{100}$.
- **Fator de Aumento Multiplicativo ($F_a$)**:
  Ao aumentar um valor em $i\%$ ($i$ na forma unitária):
  $$V_f = V_0 \cdot (1 + i)$$
  Exemplo: aumento de $20\% \implies F_a = 1 + 0{,}20 = 1{,}20$.
- **Fator de Redução / Desconto ($F_d$)**:
  Ao reduzir um valor em $i\%$:
  $$V_f = V_0 \cdot (1 - i)$$
  Exemplo: desconto de $15\% \implies F_d = 1 - 0{,}15 = 0{,}85$.

---

### 2. Aumentos e Descontos Sucessivos
Se um produto sofre sucessivos aumentos $i_1, i_2$ ou descontos $d_1, d_2$, o fator acumulado total é o **produto dos fatores individuais**:
$$F_{\text{total}} = F_1 \cdot F_2 \cdots F_n$$
> [!NOTE]
> Um aumento de $10\%$ seguido de outro aumento de $10\%$ **não** equivale a $20\%$:
> $F_{\text{total}} = 1{,}10 \times 1{,}10 = 1{,}21 \implies \text{aumento real de } 21\%$.

---

### 3. Matemática Comercial: Lucro sobre Custo vs Lucro sobre Venda
- **Equação Fundamental da Venda**:
  $$P_v = P_c + L$$
  onde $P_v$ é o preço de venda, $P_c$ o preço de custo e $L$ o lucro líquido.
  - **Lucro sobre o Custo**: $L = i_c \cdot P_c \implies P_v = P_c (1 + i_c)$.
  - **Lucro sobre a Venda**: $L = i_v \cdot P_v \implies P_v = \frac{P_c}{1 - i_v}$.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Descontos Sucessivos
**Enunciado:** Uma loja oferece uma liquidação com desconto inicial de $20\%$ e, para pagamentos à vista no PIX, um desconto adicional de $10\%$ sobre o valor já com desconto. Qual é a taxa percentual de desconto total sobre o valor original?

**Resolução Passo a Passo:**
1. Fator do primeiro desconto ($20\%$): $F_1 = 1 - 0{,}20 = 0{,}80$.
2. Fator do segundo desconto ($10\%$): $F_2 = 1 - 0{,}10 = 0{,}90$.
3. Fator acumulado total:
   $$F_{\text{total}} = 0{,}80 \times 0{,}90 = 0{,}72$$
4. O cliente pagará $72\%$ do valor original.
5. Taxa de desconto real:
   $$D_{\text{total}} = 1 - 0{,}72 = 0{,}28 = 28\%$$
(Note que $20\% + 10\% = 30\%$, mas o desconto real é de $28\%$).

---

### Exemplo 2: Lucro sobre o Preço de Venda
**Enunciado:** Um comerciante adquire uma mercadoria por $R\$\,240{,}00$. Por qual preço ele deve vendê-la para obter um lucro de $20\%$ sobre o preço de venda?

**Resolução:**
1. Identificamos: $P_c = 240$ e $L = 0{,}20 \cdot P_v$.
2. Pela equação fundamental $P_v = P_c + L$:
   $$P_v = 240 + 0{,}20 \cdot P_v$$
3. Isolando $P_v$:
   $$P_v - 0{,}20 \cdot P_v = 240 \implies 0{,}80 \cdot P_v = 240$$
4. Dividindo:
   $$P_v = \frac{240}{0{,}80} = 300$$
O preço de venda deve ser $R\$\,300{,}00$.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Base de Cálculo do Lucro:**
> Em provas e concursos, verifique com atenção se o lucro está definido sobre o **custo** ou sobre o **preço de venda**. O lucro sobre a venda tem como base $P_v$, logo a fórmula é $P_v = \frac{P_c}{1 - i}$.

> [!TIP]
> Nunca some taxas de aumentos sucessivos: multiplique sempre os fatores multiplicativos correspondentes.
""",
    },
    3: {
        "teoria": r"""# Regime de Juros Simples e Compostos

O juro é a remuneração paga pelo uso temporário de um capital $C$ ao longo do tempo $t$ a uma taxa de juros $i$.

### 1. Regime de Juros Simples (Crescimento Linear)
No regime simples, os juros de cada período são calculados exclusivamente sobre o capital inicial $C$. Não há juros sobre juros.
- **Juro Acumulado**:
  $$J = C \cdot i \cdot t$$
- **Montante Final ($M$)**:
  $$M = C + J = C(1 + i \cdot t)$$
O montante cresce em **Progressão Aritmética (PA)** de razão $C \cdot i$.

---

### 2. Regime de Juros Compostos (Crescimento Exponencial)
No regime composto (usado universalmente no sistema financeiro), os juros gerados ao fim de cada período são incorporados ao capital, passando a render juros no período subsequente (capitalização contínua/periódica).
- **Montante Final ($M$)**:
  $$M = C \cdot (1 + i)^t$$
- **Juro Acumulado**:
  $$J = M - C = C \cdot [(1 + i)^t - 1]$$
O montante cresce em **Progressão Geométrica (PG)** de razão $(1 + i)$.

---

### 3. Comparação de Curvas de Crescimento
- Para $t = 0$: $M_{\text{simples}} = M_{\text{composto}} = C$.
- Para $0 < t < 1$: $M_{\text{simples}} > M_{\text{composto}}$ (curva exponencial fica abaixo da reta no início).
- Para $t = 1$: $M_{\text{simples}} = M_{\text{composto}} = C(1 + i)$.
- Para $t > 1$: $M_{\text{composto}} > M_{\text{simples}}$ (o crescimento exponencial supera e se distancia rapidamente do linear).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Juros Simples
**Enunciado:** Um investidor aplica $R\$\,2.500{,}00$ a uma taxa de juros simples de $1{,}5\%$ ao mês por um período de 8 meses. Qual é o montante acumulado ao final do prazo?

**Resolução Passo a Passo:**
1. Identificamos os parâmetros: $C = 2.500$, $i = 0{,}015$ a.m., $t = 8$ meses.
2. Calculamos os juros simples:
   $$J = C \cdot i \cdot t = 2.500 \cdot 0{,}015 \cdot 8 = 300$$
3. Calculamos o montante:
   $$M = C + J = 2.500 + 300 = 2.800$$
O montante é $R\$\,2.800{,}00$.

---

### Exemplo 2: Juros Compostos
**Enunciado:** Qual o montante gerado por um capital de $R\$\,5.000{,}00$ aplicado a juros compostos com taxa de $10\%$ ao ano durante 3 anos?

**Resolução:**
1. Identificamos: $C = 5.000$, $i = 0{,}10$ a.a., $t = 3$ anos.
2. Aplicamos a fórmula $M = C(1 + i)^t$:
   $$M = 5.000 \cdot (1 + 0{,}10)^3 = 5.000 \cdot (1{,}10)^3$$
3. Calculamos $(1{,}1)^3 = 1{,}331$:
   $$M = 5.000 \cdot 1{,}331 = 6.655$$
O montante final é $R\$\,6.655{,}00$, tendo gerado $R\$\,1.655{,}00$ de juros.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Compatibilidade de Unidades de Tempo:**
> A taxa de juros $i$ e o tempo $t$ **devem obrigatoriamente estar expressos na mesma unidade temporal** (ambos em meses, ou ambos em anos). Se a taxa for mensal e o prazo em anos, converta o prazo para meses antes de aplicar a fórmula!

> [!TIP]
> Em juros compostos com taxas pequenas, a "Regra dos 72" permite estimar em quanto tempo o capital dobra: $t \approx \frac{72}{i\%}$.
""",
    },
    4: {
        "teoria": r"""# Fluxos de Caixa e Equivalência de Capitais

No cálculo financeiro avançado, o dinheiro possui um valor temporal: uma quantia disponível hoje não equivale à mesma quantia em uma data futura, pois o capital pode ser rentabilizado à taxa de oportunidade do mercado.

### 1. Valor Presente ($VP$) e Valor Futuro ($VF$)
A relação fundamental de equivalência temporal sob juros compostos a uma taxa de desconto $i$ por período é:
$$VF = VP \cdot (1 + i)^t \iff VP = \frac{VF}{(1 + i)^t} = VF \cdot (1 + i)^{-t}$$
onde:
- $VP$ (ou $PV$ - *Present Value*): valor atual descontado.
- $VF$ (ou $FV$ - *Future Value*): montante na data futura.

---

### 2. Diagrama de Fluxo de Caixa
Representação gráfica em uma linha do tempo horizontal:
- **Entradas de Caixa (Recebimentos)**: representadas por setas verticais para cima ($+$).
- **Saídas de Caixa (Desembolsos/Pagamentos)**: representadas por setas verticais para baixo ($-$).

---

### 3. Equivalência de Capitais e Data Focal
Dois conjuntos de fluxos de caixa são **financeiramente equivalentes** a uma taxa de juros $i$ se a soma de seus valores atuais, transportados para uma mesma data de referência (**data focal**), for rigorosamente igual.

---

### 4. Sistemas Tradicionais de Amortização
- **Sistema Francês (Tabela Price)**: as prestações periódicas $P$ são **constantes**. Os juros decrescem com o tempo e a parcela de amortização cresce a cada período.
  $$P = C \cdot \left[ \frac{i \cdot (1+i)^n}{(1+i)^n - 1} \right]$$
- **Sistema de Amortização Constante (SAC)**: a parcela de amortização do saldo devedor é estritamente **fixa** em todos os períodos ($A = \frac{C}{n}$). Como consequência, as parcelas mensais são decrescentes ao longo do tempo.
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Cálculo de Valor Presente
**Enunciado:** Uma duplicata com valor nominal de $R\$\,1.210{,}00$ tem vencimento para daqui a 2 anos. Sabendo que a taxa de juros do mercado é de $10\%$ ao ano no regime composto, qual é o valor presente desse título hoje?

**Resolução Passo a Passo:**
1. Temos $VF = 1.210$, $i = 0{,}10$ e $t = 2$.
2. Aplicamos a fórmula do Valor Presente:
   $$VP = \frac{VF}{(1 + i)^t} = \frac{1.210}{(1 + 0{,}10)^2} = \frac{1.210}{(1{,}10)^2} = \frac{1.210}{1{,}21} = 1.000$$
O valor presente é $R\$\,1.000{,}00$.

---

### Exemplo 2: Comparação de Planos de Financiamento
**Enunciado:** Um produto custa $R\$\,1.000{,}00$ à vista ou pode ser pago em duas parcelas mensais: uma entrada de $R\$\,500{,}00$ no ato e uma parcela de $R\$\,550{,}00$ após 1 mês. Qual é a taxa mensal de juros embutida nesse parcelamento?

**Resolução:**
1. A entrada de $R\$\,500{,}00$ é paga na hora, restando um saldo financiado de:
   $$S_0 = 1.000 - 500 = 500$$
2. O cliente paga $R\$\,550{,}00$ após 1 mês para quitar o saldo devedor de $500$.
3. O juro cobrado é de $550 - 500 = 50$.
4. A taxa de juros do financiamento é calculada sobre o saldo financiado:
   $$i = \frac{50}{500} = \frac{1}{10} = 0{,}10 = 10\% \text{ ao mês}$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **A Pegadinha da Entrada no Parcelamento:**
> Em vendas parceladas com entrada ("1 + 1"), a entrada não é financiada! O juro é cobrado unicamente sobre a diferença entre o preço à vista e a entrada. Calcular a taxa sobre o total de 1.000 resulta em um erro crasso de subestimação do juro.

> [!TIP]
> No Sistema SAC, o cálculo da prestação do mês $k$ é simplificado: a amortização é $A = C/n$ e os juros do mês incidem sobre o saldo devedor anterior: $J_k = S_{k-1} \cdot i$.
""",
    },
    5: {
        "teoria": r"""# Estatística Descritiva: Tabelas, Média, Mediana e Moda

A Estatística Descritiva reúne técnicas analíticas para coletar, organizar, tabular e resumir conjuntos de dados numéricos por meio de medidas de tendência central e representações gráficas.

### 1. Tipos de Variáveis
- **Qualitativas**: expressam atributos ou categorias (Nominais: cor dos olhos; Ordinais: nível de escolaridade).
- **Quantitativas**: expressam valores numéricos resultantes de contagem ou mensuração (Discretas: número de filhos; Contínuas: altura, massa, tempo).

---

### 2. Medidas de Tendência Central
1. **Média Aritmética Simples ($\bar{x}$)**:
   $$\bar{x} = \frac{\sum_{i=1}^n x_i}{n} = \frac{x_1 + x_2 + \dots + x_n}{n}$$
2. **Média Aritmética Ponderada ($\bar{x}_p$)**:
   Quando cada valor $x_i$ possui um peso $w_i$:
   $$\bar{x}_p = \frac{\sum_{i=1}^k x_i \cdot w_i}{\sum_{i=1}^k w_i}$$
3. **Moda ($Mo$)**:
   É o valor que ocorre com a **maior frequência absoluta** no conjunto de dados. Pode ser amodal (nenhum se repete), unimodal (um único pico) ou multimodal (dois ou mais valores com frequência máxima empatada).
4. **Mediana ($Md$)**:
   É o elemento que ocupa exatamente a posição central dos dados dispostos em **ordem crescente ou decrescente (rol)**:
   - Se o número de observações $n$ for **ímpar**: $Md = x_{\frac{n+1}{2}}$.
   - Se $n$ for **par**: $Md = \frac{x_{n/2} + x_{(n/2)+1}}{2}$ (a média dos dois centrais).
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Determinação de Média, Mediana e Moda
**Enunciado:** Um grupo de 7 estudantes obteve as seguintes notas em um exame: $\{4, 8, 5, 8, 9, 7, 8\}$. Determine a média, a mediana e a moda desse conjunto.

**Resolução Passo a Passo:**
1. **Ordenação dos dados (Rol)**:
   $$\{4, 5, 7, 8, 8, 8, 9\}$$
2. **Média Aritmética**:
   $$\bar{x} = \frac{4 + 5 + 7 + 8 + 8 + 8 + 9}{7} = \frac{49}{7} = 7{,}0$$
3. **Mediana**:
   Como $n = 7$ (ímpar), a mediana é o 4º termo:
   $$Md = x_4 = 8{,}0$$
4. **Moda**:
   A nota 8 aparece 3 vezes (maior frequência):
   $$Mo = 8{,}0$$

---

### Exemplo 2: Média Ponderada
**Enunciado:** Um processo seletivo avalia três provas com pesos distintos: Matemática (peso 3), Redação (peso 2) e Conhecimentos Gerais (peso 1). Um candidato obteve notas 8,0 em Matemática, 9,0 em Redação e 6,0 em Conhecimentos Gerais. Qual foi sua nota final ponderada?

**Resolução:**
1. Multiplicamos cada nota pelo respectivo peso e somamos:
   $$\sum (x_i \cdot w_i) = 8{,}0 \cdot 3 + 9{,}0 \cdot 2 + 6{,}0 \cdot 1 = 24 + 18 + 6 = 48$$
2. Somamos os pesos:
   $$\sum w_i = 3 + 2 + 1 = 6$$
3. Média ponderada:
   $$\bar{x}_p = \frac{48}{6} = 8{,}0$$
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Nunca calcule a Mediana sem Ordenar:**
> O erro mais comum em estatística elementar é pegar o elemento central da lista na ordem em que ela foi dada no enunciado. A mediana exige obrigatoriamente a construção prévia do **ROL ordenado**!

> [!TIP]
> A média é altamente sensível a valores discrepantes (*outliers*), enquanto a mediana é uma medida robusta e não é distorcida por valores extremos.
""",
    },
    6: {
        "teoria": r"""# Medidas de Dispersão: Variância e Desvio Padrão

As medidas de tendência central (como a média) são insuficientes para caracterizar uma distribuição, pois dois conjuntos com idêntica média podem apresentar distribuições completamente distintas em termos de homogeneidade e espalhamento.

### 1. Amplitude Total ($AT$)
É a diferença entre o maior e o menor valor observado no conjunto de dados:
$$AT = x_{\max} - x_{\min}$$

---

### 2. Variância Populacional e Amostral ($\sigma^2$ e $s^2$)
A variância mede a média dos quadrados dos desvios de cada elemento em relação à média aritmética:
- **Variância Populacional ($\sigma^2$)**:
  $$\sigma^2 = \frac{\sum_{i=1}^N (x_i - \mu)^2}{N}$$
- **Variância Amostral ($s^2$)** (com correção de Bessel para estimador não-tendencioso):
  $$s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1}$$

---

### 3. Desvio Padrão ($\sigma$ ou $s$)
Como a variância expressa unidades ao quadrado (ex: $\text{m}^2$, $\text{kg}^2$), o **desvio padrão** é definido como a raiz quadrada positiva da variância, resgatando a mesma unidade de medida dos dados originais:
$$\sigma = \sqrt{\sigma^2} = \sqrt{\frac{\sum_{i=1}^N (x_i - \mu)^2}{N}}$$
- **Interpretação**: Quanto menor o desvio padrão, mais homogêneo e regular é o conjunto de dados (valores concentrados em torno da média).

---

### 4. Coeficiente de Variação ($CV$)
Mede a dispersão relativa percentual, permitindo comparar a homogeneidade entre distribuições com grandezas ou médias distintas:
$$CV = \frac{\sigma}{\mu} \times 100\%$$
""",
        "exemplos": r"""# Exemplos Resolvidos Passo a Passo

### Exemplo 1: Cálculo Completo de Variância e Desvio Padrão
**Enunciado:** Calcule a variância populacional e o desvio padrão do conjunto de dados $\{2, 4, 4, 4, 5, 5, 7, 9\}$.

**Resolução Passo a Passo:**
1. Calculamos o número de elementos e a média:
   $$N = 8, \quad \mu = \frac{2 + 4 + 4 + 4 + 5 + 5 + 7 + 9}{8} = \frac{40}{8} = 5$$
2. Calculamos os quadrados dos desvios $(x_i - \mu)^2$:
   - $(2 - 5)^2 = (-3)^2 = 9$
   - $(4 - 5)^2 = (-1)^2 = 1$ (ocorre 3 vezes $\implies 3 \times 1 = 3$)
   - $(5 - 5)^2 = 0^2 = 0$ (ocorre 2 vezes $\implies 0$)
   - $(7 - 5)^2 = 2^2 = 4$
   - $(9 - 5)^2 = 4^2 = 16$
3. Somamos todos os desvios quadráticos:
   $$\sum (x_i - \mu)^2 = 9 + 3 + 0 + 4 + 16 = 32$$
4. Calculamos a variância populacional:
   $$\sigma^2 = \frac{32}{8} = 4$$
5. Calculamos o desvio padrão:
   $$\sigma = \sqrt{4} = 2$$

---

### Exemplo 2: Comparação de Regularidade entre Atletas
**Enunciado:** Dois atiradores, A e B, obtiveram a mesma média de 80 pontos em 5 rodadas. O desvio padrão do atirador A foi de 2 pontos e o do atirador B foi de 10 pontos. Qual atleta foi mais regular e consistente?

**Resolução:**
1. A regularidade em estatística é inversamente proporcional ao desvio padrão.
2. Como $\sigma_A = 2 < \sigma_B = 10$, as pontuações do atirador A oscilaram muito menos em torno da média de 80.
3. Portanto, o atirador A foi mais homogêneo, regular e consistente.
""",
        "dicas": r"""# Dicas do Tutor IA & Pegadinhas Clássicas

> [!WARNING]
> **Propriedade da Soma de Constante:**
> Se adicionarmos ou subtrairmos uma constante $c$ a todos os valores de uma amostra, a média é alterada por $c$, mas **a variância e o desvio padrão permanecem rigorosamente idênticos**, pois a dispersão mútua não muda!

> [!TIP]
> Se multiplicarmos todos os valores de uma amostra por uma constante $k > 0$, o novo desvio padrão fica multiplicado por $k$, e a nova variância fica multiplicada por $k^2$.
""",
    },
}

# ============================================================================
# 2. BATERIAS DE FIXAÇÃO (FIXACAO_DATA — 3 questões por capítulo)
# ============================================================================

FIXACAO_DATA = {
    1: [
        {
            "enunciado_katex": r"Se a razão entre dois números é $\frac{3}{5}$ e a soma deles é 64, o maior desses números vale:",
            "alternativas": [
                {"letra": "A", "texto": r"$40$", "correta": True},
                {"letra": "B", "texto": r"$24$", "correta": False},
                {"letra": "C", "texto": r"$48$", "correta": False},
                {"letra": "D", "texto": r"$32$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Seja $3k + 5k = 64 \implies 8k = 64 \implies k = 8$. O maior é $5k = 5(8) = 40$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Duas grandezas $x$ e $y$ são inversamente proporcionais. Quando $x = 4$, tem-se $y = 15$. Qual é o valor de $y$ quando $x = 6$?",
            "alternativas": [
                {"letra": "A", "texto": r"$10$", "correta": True},
                {"letra": "B", "texto": r"$22{,}5$", "correta": False},
                {"letra": "C", "texto": r"$12$", "correta": False},
                {"letra": "D", "texto": r"$8$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Como são inversamente proporcionais, o produto é constante: $x \cdot y = 4 \times 15 = 60$. Para $x = 6$: $y = \frac{60}{6} = 10$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Um carro percorre 240 km com 20 litros de combustível. Quantos litros serão necessários para percorrer 360 km sob as mesmas condições?",
            "alternativas": [
                {"letra": "A", "texto": r"$30$ litros", "correta": True},
                {"letra": "B", "texto": r"$25$ litros", "correta": False},
                {"letra": "C", "texto": r"$32$ litros", "correta": False},
                {"letra": "D", "texto": r"$28$ litros", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Consumo: $\frac{240}{20} = 12$ km/l. Litros necessários: $\frac{360}{12} = 30$ litros. Alternativa A.",
        },
    ],
    2: [
        {
            "enunciado_katex": r"Um produto que custava $R\$\,80{,}00$ sofreu um aumento de $25\%$. Seu novo preço é:",
            "alternativas": [
                {"letra": "A", "texto": r"$R\$\,100{,}00$", "correta": True},
                {"letra": "B", "texto": r"$R\$\,105{,}00$", "correta": False},
                {"letra": "C", "texto": r"$R\$\,95{,}00$", "correta": False},
                {"letra": "D", "texto": r"$R\$\,120{,}00$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$80 \times 1{,}25 = 100$, ou seja, $R\$\,100{,}00$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Um comerciante comprou um item por $R\$\,150{,}00$ e o vendeu por $R\$\,180{,}00$. A taxa percentual de lucro sobre o preço de custo foi de:",
            "alternativas": [
                {"letra": "A", "texto": r"$20\%$", "correta": True},
                {"letra": "B", "texto": r"$16{,}67\%$", "correta": False},
                {"letra": "C", "texto": r"$30\%$", "correta": False},
                {"letra": "D", "texto": r"$25\%$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Lucro: $180 - 150 = 30$. Taxa sobre o custo: $\frac{30}{150} = 0{,}20 = 20\%$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Dois aumentos sucessivos de $10\%$ sobre o valor de uma mercadoria equivalem a um único aumento de:",
            "alternativas": [
                {"letra": "A", "texto": r"$21\%$", "correta": True},
                {"letra": "B", "texto": r"$20\%$", "correta": False},
                {"letra": "C", "texto": r"$22\%$", "correta": False},
                {"letra": "D", "texto": r"$19\%$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Fator acumulado: $1{,}10 \times 1{,}10 = 1{,}21 \implies 21\%$ de aumento total. Alternativa A.",
        },
    ],
    3: [
        {
            "enunciado_katex": r"Um capital de $R\$\,600{,}00$ é aplicado a juros simples com taxa de $3\%$ ao mês durante 5 meses. O valor total dos juros produzidos é:",
            "alternativas": [
                {"letra": "A", "texto": r"$R\$\,90{,}00$", "correta": True},
                {"letra": "B", "texto": r"$R\$\,690{,}00$", "correta": False},
                {"letra": "C", "texto": r"$R\$\,80{,}00$", "correta": False},
                {"letra": "D", "texto": r"$R\$\,100{,}00$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$J = C \cdot i \cdot t = 600 \times 0{,}03 \times 5 = 90$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Qual é o montante acumulado por um capital de $R\$\,2.000{,}00$ aplicado a juros compostos de $5\%$ ao mês durante 2 meses?",
            "alternativas": [
                {"letra": "A", "texto": r"$R\$\,2.205{,}00$", "correta": True},
                {"letra": "B", "texto": r"$R\$\,2.200{,}00$", "correta": False},
                {"letra": "C", "texto": r"$R\$\,2.100{,}00$", "correta": False},
                {"letra": "D", "texto": r"$R\$\,2.250{,}00$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$M = 2.000 \times (1{,}05)^2 = 2.000 \times 1{,}1025 = 2.205$, ou seja, $R\$\,2.205{,}00$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Em qual regime de capitalização o crescimento do montante ao longo do tempo é representado graficamente por uma linha reta?",
            "alternativas": [
                {"letra": "A", "texto": r"Juros Simples", "correta": True},
                {"letra": "B", "texto": r"Juros Compostos", "correta": False},
                {"letra": "C", "texto": r"Desconto Racional Composto", "correta": False},
                {"letra": "D", "texto": r"Capitalização Contínua", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Em juros simples a fórmula é afim ($M(t) = C + (C \cdot i) \cdot t$), cujo gráfico é linear. Alternativa A.",
        },
    ],
    4: [
        {
            "enunciado_katex": r"O valor presente de um pagamento futuro de $R\$\,1.331{,}00$ com vencimento para daqui a 3 anos, a uma taxa de juros compostos de $10\%$ ao ano, é:",
            "alternativas": [
                {"letra": "A", "texto": r"$R\$\,1.000{,}00$", "correta": True},
                {"letra": "B", "texto": r"$R\$\,1.100{,}00$", "correta": False},
                {"letra": "C", "texto": r"$R\$\,1.200{,}00$", "correta": False},
                {"letra": "D", "texto": r"$R\$\,900{,}00$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$VP = \frac{1.331}{(1{,}10)^3} = \frac{1.331}{1{,}331} = 1.000$, ou seja, $R\$\,1.000{,}00$. Alternativa A.",
        },
        {
            "enunciado_katex": r"No Sistema de Amortização Constante (SAC), o que ocorre com o valor das prestações periódicas pagas ao longo do tempo?",
            "alternativas": [
                {"letra": "A", "texto": r"Decrescem a cada período", "correta": True},
                {"letra": "B", "texto": r"Permanecem estritamente constantes", "correta": False},
                {"letra": "C", "texto": r"Crescem a cada período", "correta": False},
                {"letra": "D", "texto": r"Oscilam conforme a inflação", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"No SAC a amortização é fixa, mas como o saldo devedor diminui, a parcela de juros decresce, reduzindo o valor total da prestação. Alternativa A.",
        },
        {
            "enunciado_katex": r"Na Tabela Price (Sistema Francês), as prestações mensais são:",
            "alternativas": [
                {"letra": "A", "texto": r"Iguais e constantes ao longo de todo o prazo", "correta": True},
                {"letra": "B", "texto": r"Decrescentes com amortização fixa", "correta": False},
                {"letra": "C", "texto": r"Crescentes em progressão geométrica", "correta": False},
                {"letra": "D", "texto": r"Calculadas unicamente por juros simples", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"A característica definidora da Tabela Price é manter as parcelas periódicas uniformes (constantes). Alternativa A.",
        },
    ],
    5: [
        {
            "enunciado_katex": r"A média aritmética dos números $\{6, 8, 12, 14\}$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$10$", "correta": True},
                {"letra": "B", "texto": r"$9$", "correta": False},
                {"letra": "C", "texto": r"$11$", "correta": False},
                {"letra": "D", "texto": r"$8$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$\bar{x} = \frac{6 + 8 + 12 + 14}{4} = \frac{40}{4} = 10$. Alternativa A.",
        },
        {
            "enunciado_katex": r"A mediana do conjunto de dados $\{3, 9, 2, 7, 5\}$ é:",
            "alternativas": [
                {"letra": "A", "texto": r"$5$", "correta": True},
                {"letra": "B", "texto": r"$2$", "correta": False},
                {"letra": "C", "texto": r"$7$", "correta": False},
                {"letra": "D", "texto": r"$5{,}2$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Ordenando os dados (Rol): $\{2, 3, 5, 7, 9\}$. O elemento central é $5$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Em uma pesquisa sobre número de irmãos, as respostas foram: $\{1, 2, 2, 3, 2, 4, 1, 5\}$. A moda dessa distribuição é:",
            "alternativas": [
                {"letra": "A", "texto": r"$2$", "correta": True},
                {"letra": "B", "texto": r"$1$", "correta": False},
                {"letra": "C", "texto": r"$2{,}5$", "correta": False},
                {"letra": "D", "texto": r"$3$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"O valor $2$ se repete 3 vezes (maior frequência absoluta). Portanto, $Mo = 2$. Alternativa A.",
        },
    ],
    6: [
        {
            "enunciado_katex": r"A amplitude total do conjunto de dados $\{12, 18, 5, 23, 9\}$ é igual a:",
            "alternativas": [
                {"letra": "A", "texto": r"$18$", "correta": True},
                {"letra": "B", "texto": r"$23$", "correta": False},
                {"letra": "C", "texto": r"$14$", "correta": False},
                {"letra": "D", "texto": r"$16$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"$AT = x_{\max} - x_{\min} = 23 - 5 = 18$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se a variância de uma distribuição é igual a 16, o desvio padrão correspondente é:",
            "alternativas": [
                {"letra": "A", "texto": r"$4$", "correta": True},
                {"letra": "B", "texto": r"$256$", "correta": False},
                {"letra": "C", "texto": r"$8$", "correta": False},
                {"letra": "D", "texto": r"$2$", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"O desvio padrão é a raiz quadrada da variância: $\sigma = \sqrt{16} = 4$. Alternativa A.",
        },
        {
            "enunciado_katex": r"Se todos os elementos de um conjunto de dados forem somados ao número 10, o que ocorre com o desvio padrão?",
            "alternativas": [
                {"letra": "A", "texto": r"Permanece inalterado", "correta": True},
                {"letra": "B", "texto": r"Aumenta em 10 unidades", "correta": False},
                {"letra": "C", "texto": r"Fica multiplicado por 10", "correta": False},
                {"letra": "D", "texto": r"Aumenta em 100 unidades", "correta": False},
            ],
            "resposta_correta": "A",
            "explicacao_katex": r"Adicionar uma constante a todos os valores translada os dados, sem alterar o espalhamento relativo. O desvio padrão permanece o mesmo. Alternativa A.",
        },
    ],
}

# ============================================================================
# 3. FRAGMENTOS CANÔNICOS PARA O RAG (RAG_DATA — 1 por capítulo)
# ============================================================================

RAG_DATA = [
    {
        "numero_capitulo": 1,
        "titulo": "Grandezas Diretamente e Inversamente Proporcionais",
        "conteudo_markdown": r"""Duas grandezas são diretamente proporcionais quando a razão $\frac{y}{x} = k$ é constante, gerando retas que cruzam a origem. São inversamente proporcionais quando o produto $x \cdot y = k$ permanece invariante, formando uma hipérbole equilátera.""",
    },
    {
        "numero_capitulo": 2,
        "titulo": "Fatores Multiplicativos e Matemática Comercial",
        "conteudo_markdown": r"""Aumentos e descontos sucessivos operam por multiplicação de seus fatores: $F_{\text{total}} = \prod (1 \pm i_k)$. Na matemática comercial, o lucro sobre o custo é $L = i_c P_c$, enquanto o lucro sobre o preço de venda é $L = i_v P_v \implies P_v = \frac{P_c}{1 - i_v}$.""",
    },
    {
        "numero_capitulo": 3,
        "titulo": "Regimes de Capitalização Simples e Composta",
        "conteudo_markdown": r"""No regime simples, os juros incidem apenas sobre o capital inicial linearmente ($M = C(1 + it)$). No regime composto, os rendimentos integram a base a cada período ($M = C(1 + i)^t$), caracterizando crescimento exponencial e modelando o sistema bancário.""",
    },
    {
        "numero_capitulo": 4,
        "titulo": "Equivalência de Capitais e Modelos SAC e Price",
        "conteudo_markdown": r"""O valor presente desconta fluxos futuros a valor de hoje: $VP = VF(1+i)^{-t}$. No Sistema de Amortização Constante (SAC), a cota de amortização é fixa e as prestações decrescem; na Tabela Price, os desembolsos periódicos são uniformes.""",
    },
    {
        "numero_capitulo": 5,
        "titulo": "Estatística Descritiva e Medidas de Tendência Central",
        "conteudo_markdown": r"""A média aritmética simples ou ponderada expressa o centro de massa da distribuição. A mediana divide a amostra ordenada (rol) em duas metades com igual número de elementos. A moda expressa o valor de frequência absoluta máxima.""",
    },
    {
        "numero_capitulo": 6,
        "titulo": "Medidas de Dispersão, Variância e Desvio Padrão",
        "conteudo_markdown": r"""A variância afere a média dos quadrados dos desvios em relação à média: $\sigma^2 = \frac{\sum (x_i - \mu)^2}{N}$. O desvio padrão $\sigma = \sqrt{\sigma^2}$ reestabelece a unidade de medida das variáveis originais, mensurando o grau de regularidade da distribuição.""",
    },
]

# ============================================================================
# 4. ITENS CALIBRADOS TRI (TRI_DATA — 5 itens por capítulo = 30 itens)
# ============================================================================

TRI_DATA = [
    # --- Cap 1: Razão, Proporção e Grandezas Proporcionais (5 itens) ---
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A razão entre a idade de um filho e a de seu pai é de $\frac{2}{5}$. Se o pai tem $45$ anos, qual é a idade do filho?",
        "alternativas": [
            {"letra": "A", "texto": r"$18$ anos", "correta": True},
            {"letra": "B", "texto": r"$15$ anos", "correta": False},
            {"letra": "C", "texto": r"$20$ anos", "correta": False},
            {"letra": "D", "texto": r"$22$ anos", "correta": False},
            {"letra": "E", "texto": r"$16$ anos", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $\frac{F}{P} = \frac{2}{5} \implies \frac{F}{45} = \frac{2}{5}$. 2. $5F = 90 \implies F = 18$ anos. Alternativa A.",
        "parametro_a": 1.150,
        "parametro_b": -1.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Monte a proporção direta entre a idade do filho e a do pai."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Três pedreiros constroem um muro em 12 dias. Trabalhando no mesmo ritmo, em quantos dias 4 pedreiros construiriam esse mesmo muro?",
        "alternativas": [
            {"letra": "A", "texto": r"$9$ dias", "correta": True},
            {"letra": "B", "texto": r"$16$ dias", "correta": False},
            {"letra": "C", "texto": r"$8$ dias", "correta": False},
            {"letra": "D", "texto": r"$10$ dias", "correta": False},
            {"letra": "E", "texto": r"$15$ dias", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pedreiros e dias são grandezas inversamente proporcionais: $3 \times 12 = 4 \times x$. 2. $36 = 4x \implies x = 9$ dias. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Mais pedreiros exigem menos dias: grandezas inversamente proporcionais têm produto constante."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Dividindo o número 120 em partes diretamente proporcionais a 2, 3 e 5, determine o valor da maior parte.",
        "alternativas": [],
        "resposta_correta": "60",
        "resolucao_passo_a_passo": r"1. $2k + 3k + 5k = 120 \implies 10k = 120 \implies k = 12$. 2. A maior parte é $5k = 5(12) = 60$.",
        "parametro_a": 1.200,
        "parametro_b": -0.800,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Some os fatores de proporção ($2+3+5=10$) e divida 120 por 10 para achar a constante k."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um mapa foi desenhado na escala $1 : 500.000$. A distância no mapa entre duas cidades é de $6\text{ cm}$. A distância real em linha reta entre essas cidades é de:",
        "alternativas": [
            {"letra": "A", "texto": r"$30\text{ km}$", "correta": True},
            {"letra": "B", "texto": r"$300\text{ km}$", "correta": False},
            {"letra": "C", "texto": r"$3\text{ km}$", "correta": False},
            {"letra": "D", "texto": r"$12\text{ km}$", "correta": False},
            {"letra": "E", "texto": r"$60\text{ km}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Distância real $= 6 \times 500.000\text{ cm} = 3.000.000\text{ cm}$. 2. Convertendo para metros: $30.000\text{ m}$. 3. Convertendo para quilômetros: $30\text{ km}$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Multiplique a medida do mapa pela escala e converta centímetros para quilômetros dividindo por $100.000$."},
    },
    {
        "numero_capitulo": 1,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Cinco máquinas idênticas produzem 400 peças em 4 horas. Quantas peças 8 dessas mesmas máquinas produziriam em 6 horas de trabalho?",
        "alternativas": [
            {"letra": "A", "texto": r"$960$", "correta": True},
            {"letra": "B", "texto": r"$800$", "correta": False},
            {"letra": "C", "texto": r"$1.200$", "correta": False},
            {"letra": "D", "texto": r"$640$", "correta": False},
            {"letra": "E", "texto": r"$720$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Capacidade por máquina-hora: $\frac{400}{5 \times 4} = \frac{400}{20} = 20$ peças por hora. 2. Produção nova: $8 \times 6 \times 20 = 48 \times 20 = 960$ peças. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule a produção de uma única máquina por hora e multiplique pela nova quantidade de máquinas e horas."},
    },

    # --- Cap 2: Porcentagem, Lucro e Prejuízo Comercial (5 itens) ---
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um produto com preço de tabela de $R\$\,200{,}00$ recebe um desconto de $15\%$. O preço final a ser pago é:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,170{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,180{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,165{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,150{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,175{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O desconto equivale a $15\%$ de $200$: $0{,}15 \times 200 = 30$. 2. Preço final: $200 - 30 = 170$, ou seja, $R\$\,170{,}00$. Alternativa A.",
        "parametro_a": 1.200,
        "parametro_b": -1.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule o desconto ($15\%$ de $200$) e subtraia do preço de tabela."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Após um reajuste salarial de $8\%$, o salário de um trabalhador passou a ser de $R\$\,2.700{,}00$. O valor do salário antes do reajuste era de:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,2.500{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,2.484{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,2.600{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,2.450{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,2.520{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $S_0 \cdot 1{,}08 = 2.700 \implies S_0 = \frac{2.700}{1{,}08} = 2.500$, ou seja, $R\$\,2.500{,}00$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Divida o salário novo pelo fator de aumento $1 + 0{,}08 = 1{,}08$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um investidor compra uma ação por $R\$\,50{,}00$. Ela sofre uma valorização de $20\%$ no primeiro mês e, no segundo mês, uma queda de $20\%$ sobre o novo valor. Ao final dos dois meses, o valor da ação é de:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,48{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,50{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,46{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,52{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,45{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Fator composto: $F = (1 + 0{,}20) \times (1 - 0{,}20) = 1{,}20 \times 0{,}80 = 0{,}96$. 2. Valor final: $50 \times 0{,}96 = 48$, ou seja, $R\$\,48{,}00$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Multiplique os dois fatores: $1{,}20 \\times 0{,}80 = 0{,}96$, indicando perda líquida de $4\%$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um comerciante deseja obter um lucro de 25% sobre o preço de custo de um produto que lhe custou R$ 80,00. Por quantos reais ele deve vender o produto?",
        "alternativas": [],
        "resposta_correta": "100",
        "resolucao_passo_a_passo": r"1. Lucro sobre o custo: $L = 0{,}25 \times 80 = 20$. 2. Preço de venda: $80 + 20 = 100$.",
        "parametro_a": 1.250,
        "parametro_b": -0.700,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Calcule $80 \\times 1{,}25$."},
    },
    {
        "numero_capitulo": 2,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma loja vende um eletrodoméstico por $R\$\,400{,}00$, obtendo um lucro de $20\%$ sobre o preço de venda. Qual foi o preço de custo desse aparelho para a loja?",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,320{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,333{,}33$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,300{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,350{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,310{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O lucro é $20\%$ da venda: $L = 0{,}20 \times 400 = 80$. 2. Custo: $P_c = P_v - L = 400 - 80 = 320$, ou seja, $R\$\,320{,}00$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O lucro é calculado sobre $400$ ($20\%$ de $400$); subtraia esse valor da venda para obter o custo."},
    },

    # --- Cap 3: Regime de Juros Simples e Compostos (5 itens) ---
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um capital de $R\$\,1.000{,}00$ é aplicado a juros simples de $2\%$ ao mês durante $6$ meses. Os juros produzidos totalizam:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,120{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,126{,}16$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,60{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,200{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,102{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Em juros simples: $J = C \cdot i \cdot t$. 2. $J = 1000 \cdot 0{,}02 \cdot 6 = 120$, ou seja, $R\$\,120{,}00$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Juros simples não capitalizam: $J = C \\cdot i \\cdot t$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Aplicando-se $R\$\,1.000{,}00$ a juros compostos de $10\%$ ao ano, o montante após $2$ anos será de:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,1.210{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,1.200{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,1.100{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,1.220{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,1.331{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Em juros compostos: $M = C(1+i)^t$. 2. $M = 1000 \cdot (1{,}10)^2 = 1000 \cdot 1{,}21 = 1210$, ou seja, $R\$\,1.210{,}00$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Juros compostos capitalizam período a período: $M = C(1+i)^t$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Durante quantos meses um capital de R$ 500,00 deve ficar aplicado a juros simples com taxa de 4% ao mês para render R$ 100,00 de juros?",
        "alternativas": [],
        "resposta_correta": "5",
        "resolucao_passo_a_passo": r"1. $J = C \cdot i \cdot t \implies 100 = 500 \cdot 0{,}04 \cdot t \implies 100 = 20t \implies t = 5$ meses.",
        "parametro_a": 1.250,
        "parametro_b": -0.600,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Isole t na equação dos juros simples: $t = J / (C \\cdot i)$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é a taxa anual equivalente a uma taxa de juros compostos de $20\%$ ao semestre?",
        "alternativas": [
            {"letra": "A", "texto": r"$44\%$ a.a.", "correta": True},
            {"letra": "B", "texto": r"$40\%$ a.a.", "correta": False},
            {"letra": "C", "texto": r"$42\%$ a.a.", "correta": False},
            {"letra": "D", "texto": r"$48\%$ a.a.", "correta": False},
            {"letra": "E", "texto": r"$36\%$ a.a.", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Um ano tem 2 semestres. 2. $1 + i_a = (1 + i_s)^2 = (1{,}20)^2 = 1{,}44$. 3. $i_a = 0{,}44 = 44\%$ a.a. Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.800,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Em juros compostos, a taxa anual para 2 semestres é dada por $(1 + i_s)^2 - 1$."},
    },
    {
        "numero_capitulo": 3,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um investidor aplicou $R\$\,8.000{,}00$ a juros compostos com taxa de $5\%$ ao ano. Ao final de 2 anos, o total de juros obtidos foi de:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,820{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,800{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,840{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,900{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,400{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $M = 8000 \cdot (1{,}05)^2 = 8000 \cdot 1{,}1025 = 8.820$. 2. Juros: $8.820 - 8.000 = 820$, ou seja, $R\$\,820{,}00$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule o montante final e subtraia o capital inicial para encontrar os juros."},
    },

    # --- Cap 4: Fluxos de Caixa e Equivalência de Capitais (5 itens) ---
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"O valor presente de um capital de $R\$\,2.420{,}00$ a ser resgatado daqui a 2 meses, considerando uma taxa de desconto composto de $10\%$ ao mês, é:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,2.000{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,2.200{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,1.936{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,2.100{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,1.800{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $VP = \frac{VF}{(1+i)^t} = \frac{2420}{(1{,}10)^2} = \frac{2420}{1{,}21} = 2.000$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Divida o valor futuro por $(1 + i)^2$."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um financiamento de $R\$\,12.000{,}00$ será pago em 12 parcelas mensais pelo Sistema SAC a uma taxa de juros de $1\%$ ao mês. A cota de amortização mensal constante é:",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,1.000{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,1.120{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,1.010{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,900{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,1.050{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. No SAC, a amortização mensal é estritamente constante: $A = \frac{C}{n}$. 2. $A = \frac{12.000}{12} = 1.000$, ou seja, $R\$\,1.000{,}00$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "No SAC, a amortização é obtida dividindo o valor total financiado pelo número de parcelas."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual é o valor dos juros da primeira parcela no financiamento de $R\$\,10.000{,}00$ com juros de $2\%$ ao mês?",
        "alternativas": [
            {"letra": "A", "texto": r"$R\$\,200{,}00$", "correta": True},
            {"letra": "B", "texto": r"$R\$\,100{,}00$", "correta": False},
            {"letra": "C", "texto": r"$R\$\,400{,}00$", "correta": False},
            {"letra": "D", "texto": r"$R\$\,20{,}00$", "correta": False},
            {"letra": "E", "texto": r"$R\$\,500{,}00$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. No primeiro mês, os juros incidem sobre todo o saldo devedor inicial de 10.000. 2. $J_1 = 10.000 \times 0{,}02 = 200$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Multiplique o saldo devedor inicial pela taxa mensal."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Um smartphone de R$ 2.000,00 pode ser comprado com entrada de R$ 800,00 e uma parcela de R$ 1.320,00 após 1 mês. Qual é a taxa percentual de juros mensal cobrada no parcelamento?",
        "alternativas": [],
        "resposta_correta": "10",
        "resolucao_passo_a_passo": r"1. Saldo financiado: $2.000 - 800 = 1.200$. 2. Parcela paga: $1.320$. Juros: $1.320 - 1.200 = 120$. 3. Taxa: $\frac{120}{1.200} = 0{,}10 = 10\%$.",
        "parametro_a": 1.450,
        "parametro_b": 0.600,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Calcule a taxa sobre o saldo devedor financiado (R$ 1.200), e não sobre o preço total à vista."},
    },
    {
        "numero_capitulo": 4,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em relação aos sistemas Price e SAC, é correto afirmar que, para um mesmo prazo e taxa:",
        "alternativas": [
            {"letra": "A", "texto": r"O total de juros pagos no SAC é menor do que no Price", "correta": True},
            {"letra": "B", "texto": r"O total de juros pagos no Price é menor do que no SAC", "correta": False},
            {"letra": "C", "texto": r"Ambos os sistemas pagam rigorosamente o mesmo total de juros", "correta": False},
            {"letra": "D", "texto": r"No SAC a primeira parcela é sempre menor do que no Price", "correta": False},
            {"letra": "E", "texto": r"No Price a amortização é constante", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. No SAC o saldo devedor decresce mais rapidamente desde o início, gerando uma base de cálculo de juros menor a cada mês. 2. Logo, o montante total de juros pagos no SAC é inferior ao da Tabela Price. Alternativa A.",
        "parametro_a": 1.500,
        "parametro_b": 0.900,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Como a amortização no SAC é maior no início, o saldo devedor cai mais rápido e reduz o juro total pago."},
    },

    # --- Cap 5: Estatística Descritiva: Tabelas, Média, Mediana e Moda (5 itens) ---
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Um aluno obteve as notas $8$ (com peso $2$) e $6$ (com peso $3$). Sua média ponderada final é:",
        "alternativas": [
            {"letra": "A", "texto": r"$6{,}8$", "correta": True},
            {"letra": "B", "texto": r"$7{,}0$", "correta": False},
            {"letra": "C", "texto": r"$6{,}5$", "correta": False},
            {"letra": "D", "texto": r"$7{,}2$", "correta": False},
            {"letra": "E", "texto": r"$6{,}0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Média ponderada: $\bar{x} = \frac{\sum (x_i \cdot p_i)}{\sum p_i}$. 2. $\bar{x} = \frac{8 \cdot 2 + 6 \cdot 3}{2 + 3} = \frac{16 + 18}{5} = \frac{34}{5} = 6{,}8$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 1.300,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Na média ponderada, multiplique cada nota pelo seu peso, some tudo e divida pela soma dos pesos."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"A mediana do conjunto ordenado de observações $\{4, 7, 9, 12, 15, 18\}$ é igual a:",
        "alternativas": [
            {"letra": "A", "texto": r"$10{,}5$", "correta": True},
            {"letra": "B", "texto": r"$10{,}0$", "correta": False},
            {"letra": "C", "texto": r"$11{,}0$", "correta": False},
            {"letra": "D", "texto": r"$9{,}0$", "correta": False},
            {"letra": "E", "texto": r"$12{,}0$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. O número de termos é $n = 6$ (par). 2. Os dois termos centrais são o 3º ($9$) e o 4º ($12$). 3. $Md = \frac{9 + 12}{2} = \frac{21}{2} = 10{,}5$. Alternativa A.",
        "parametro_a": 1.250,
        "parametro_b": -0.400,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Como a quantidade de elementos é par, a mediana é a média aritmética dos dois valores centrais."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Calcule a média aritmética simples dos números 14, 18, 22 e 26.",
        "alternativas": [],
        "resposta_correta": "20",
        "resolucao_passo_a_passo": r"1. Soma: $14 + 18 + 22 + 26 = 80$. 2. Média: $\frac{80}{4} = 20$.",
        "parametro_a": 1.150,
        "parametro_b": -1.000,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Some os 4 números e divida por 4."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma turma de 10 alunos, 4 tiraram nota 6, 4 tiraram nota 8 e 2 tiraram nota 10. A média da turma foi:",
        "alternativas": [
            {"letra": "A", "texto": r"$7{,}6$", "correta": True},
            {"letra": "B", "texto": r"$8{,}0$", "correta": False},
            {"letra": "C", "texto": r"$7{,}2$", "correta": False},
            {"letra": "D", "texto": r"$7{,}8$", "correta": False},
            {"letra": "E", "texto": r"$8{,}2$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Soma das notas: $4 \times 6 + 4 \times 8 + 2 \times 10 = 24 + 32 + 20 = 76$. 2. Média: $\frac{76}{10} = 7{,}6$. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Multiplique cada nota pela sua frequência, some os produtos e divida pelo total de 10 alunos."},
    },
    {
        "numero_capitulo": 5,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Qual das seguintes medidas estatísticas NÃO é afetada pela presença de um único valor extremo discrepante (outlier)?",
        "alternativas": [
            {"letra": "A", "texto": r"Mediana", "correta": True},
            {"letra": "B", "texto": r"Média aritmética", "correta": False},
            {"letra": "C", "texto": r"Desvio padrão", "correta": False},
            {"letra": "D", "texto": r"Variância", "correta": False},
            {"letra": "E", "texto": r"Amplitude total", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. A mediana é uma medida de posição separatriz robusta que depende apenas da ordem central dos elementos, ao passo que a média, desvio padrão e amplitude são diretamente alterados por outliers. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "A mediana é resistente a extremos porque olha para o centro da ordenação."},
    },

    # --- Cap 6: Medidas de Dispersão: Variância e Desvio Padrão (5 itens) ---
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Considere o conjunto de dados $\{3, 5, 7\}$. A variância populacional desse conjunto é:",
        "alternativas": [
            {"letra": "A", "texto": r"$\frac{8}{3}$", "correta": True},
            {"letra": "B", "texto": r"$4$", "correta": False},
            {"letra": "C", "texto": r"$2$", "correta": False},
            {"letra": "D", "texto": r"$\frac{4}{3}$", "correta": False},
            {"letra": "E", "texto": r"$\frac{16}{3}$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Média: $\mu = \frac{3 + 5 + 7}{3} = \frac{15}{3} = 5$. 2. Desvios quadráticos: $(3-5)^2 = 4$; $(5-5)^2 = 0$; $(7-5)^2 = 4$. 3. $\sigma^2 = \frac{4 + 0 + 4}{3} = \frac{8}{3}$. Alternativa A.",
        "parametro_a": 1.400,
        "parametro_b": 0.500,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Calcule a média (5) e tire a média dos quadrados das distâncias de cada valor até a média."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Se todos os elementos de uma amostra forem multiplicados pelo número positivo 3, o novo desvio padrão:",
        "alternativas": [
            {"letra": "A", "texto": r"Fica multiplicado por 3", "correta": True},
            {"letra": "B", "texto": r"Fica multiplicado por 9", "correta": False},
            {"letra": "C", "texto": r"Permanece inalterado", "correta": False},
            {"letra": "D", "texto": r"Aumenta em 3 unidades", "correta": False},
            {"letra": "E", "texto": r"Fica dividido por 3", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Pela propriedade de escala das medidas de dispersão: $\sigma(k X) = |k| \cdot \sigma(X)$. Para $k = 3$, o desvio padrão é multiplicado por 3 (enquanto a variância seria multiplicada por $3^2 = 9$). Alternativa A.",
        "parametro_a": 1.450,
        "parametro_b": 0.700,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O desvio padrão tem a mesma dimensão dos dados originais: multiplica-se pelo próprio fator $k$."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "numeric_input",
        "enunciado_katex": r"Determine o desvio padrão de uma amostra composta por 5 valores idênticos a 8.",
        "alternativas": [],
        "resposta_correta": "0",
        "resolucao_passo_a_passo": r"1. Como todos os valores são iguais a 8, não há dispersão ou afastamento em relação à média ($8 - 8 = 0$). Logo, o desvio padrão é 0.",
        "parametro_a": 1.200,
        "parametro_b": -1.100,
        "parametro_c": 0.000,
        "metadados_sympy": {"tipo_item": "numeric_input", "grande_area": "aplicada", "dica_estagio_2": "Quando todos os dados são rigorosamente iguais, a dispersão é nula."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Uma distribuição possui média igual a $50$ e desvio padrão igual a $5$. O coeficiente de variação percentual dessa distribuição é:",
        "alternativas": [
            {"letra": "A", "texto": r"$10\%$", "correta": True},
            {"letra": "B", "texto": r"$5\%$", "correta": False},
            {"letra": "C", "texto": r"$20\%$", "correta": False},
            {"letra": "D", "texto": r"$25\%$", "correta": False},
            {"letra": "E", "texto": r"$2{,}5\%$", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. $CV = \frac{\sigma}{\mu} \times 100\% = \frac{5}{50} \times 100\% = 0{,}10 \times 100\% = 10\%$. Alternativa A.",
        "parametro_a": 1.350,
        "parametro_b": 0.100,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "O coeficiente de variação é a razão entre o desvio padrão e a média vezes 100%."},
    },
    {
        "numero_capitulo": 6,
        "tipo_origem": "iezzi_original",
        "tipo_item": "multiple_choice",
        "enunciado_katex": r"Em uma competição de salto em altura, o atleta X teve saltos com média de 2,0 m e desvio padrão de 0,05 m. O atleta Y teve média de 2,0 m e desvio padrão de 0,20 m. Pode-se concluir que:",
        "alternativas": [
            {"letra": "A", "texto": r"O atleta X é mais regular e consistente que o atleta Y", "correta": True},
            {"letra": "B", "texto": r"O atleta Y é mais regular e consistente que o atleta X", "correta": False},
            {"letra": "C", "texto": r"Ambos os atletas apresentaram exatamente o mesmo desempenho", "correta": False},
            {"letra": "D", "texto": r"O atleta Y saltou mais alto em média do que o atleta X", "correta": False},
            {"letra": "E", "texto": r"Não é possível comparar a regularidade dos atletas", "correta": False},
        ],
        "resposta_correta": "A",
        "resolucao_passo_a_passo": r"1. Com médias idênticas, a regularidade é mensurada diretamente pelo desvio padrão. 2. Quanto menor o desvio padrão, menor a oscilação dos resultados. Como $0{,}05 < 0{,}20$, o atleta X foi mais regular. Alternativa A.",
        "parametro_a": 1.300,
        "parametro_b": -0.200,
        "parametro_c": 0.200,
        "metadados_sympy": {"grande_area": "aplicada", "dica_estagio_2": "Menor desvio padrão indica menor variabilidade e maior consistência."},
    },
]
