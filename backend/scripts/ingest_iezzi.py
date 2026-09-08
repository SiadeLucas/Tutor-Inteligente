"""
Script Canônico de Ingestão de Fragmentos do Iezzi (RAG - pgvector 768d).
Conforme especificação em docs-site/docs/implementation/etapa-06-ia-rag.md (Seção 6.3)
e docs-site/docs/knowledge/database/10-documentos-vetoriais-rag.md.
"""
import asyncio
import sys
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, delete

from app.core.config import settings
from app.models.content import VolumeDidatico, Capitulo, DocumentoVetorialRAG
from app.ai.llm_factory import LLMFactory


FRAGMENTOS_IEZZI_VOLUME_1 = [
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
            "1) Negação ($\\sim p$ ou $\\neg p$): inverte o valor de $p$. Se $p$ é V, $\\sim p$ é F; "
            "2) Conjunção ($p \\land q$): proposição 'p e q' é verdadeira apenas quando ambos $p$ e $q$ "
            "são simultaneamente verdadeiros. Se ao menos um for falso, a conjunção é falsa; "
            "3) Disjunção inclusiva ($p \\lor q$): proposição 'p ou q' é verdadeira se pelo menos um dos "
            "dois componentes for verdadeiro, sendo falsa unicamente se ambos forem simultaneamente falsos."
        ),
    },
    {
        "numero_capitulo": 1,
        "pagina": 18,
        "teorema": "Condicional e Negação da Implicação",
        "texto": (
            "A condicional $p \\to q$ (lê-se 'se p, então q') afirma que a ocorrência de $p$ (antecedente) "
            "implica necessariamente a ocorrência de $q$ (consequente). A condicional só é FALSA no caso "
            "em que o antecedente é verdadeiro e o consequente é falso: $V \\to F \\equiv F$. Em todos "
            "os demais casos, a condicional é logicamente verdadeira. Crucialmente, a negação de uma "
            "condicional não é outra condicional, mas sim a conjunção do antecedente com a negação do "
            "consequente: $\\sim (p \\to q) \\equiv p \\land \\sim q$."
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 32,
        "teorema": "Definição de Conjunto e Relação de Pertinência",
        "texto": (
            "Na teoria ingênua dos conjuntos, conjunto e elemento são noções primitivas aceitas sem definição formal. "
            "A relação de pertinência ($x \\in A$) vincula um elemento $x$ ao conjunto $A$. Se $x$ não pertence a $A$, "
            "escrevemos $x \\notin A$. O conjunto que não possui nenhum elemento é o conjunto vazio, denotado por $\\emptyset$ "
            "ou $\\{\\}$. Um conjunto $A$ é subconjunto de $B$ (escreve-se $A \\subset B$, ou $A$ está contido em $B$) "
            "se, e somente se, todo elemento pertencente a $A$ também pertence a $B$: "
            "$$A \\subset B \\iff (\\forall x)(x \\in A \\implies x \\in B)$$"
        ),
    },
    {
        "numero_capitulo": 2,
        "pagina": 40,
        "teorema": "Operações Fundamentais com Conjuntos",
        "texto": (
            "Sejam $A$ e $B$ conjuntos contidos num universo $U$: "
            "1) União: $A \\cup B = \\{x \\in U \\mid x \\in A \\lor x \\in B\\}$; "
            "2) Interseção: $A \\cap B = \\{x \\in U \\mid x \\in A \\land x \\in B\\}$. Quando $A \\cap B = \\emptyset$, dizemos que $A$ e $B$ são disjuntos; "
            "3) Diferença: $A - B = \\{x \\in U \\mid x \\in A \\land x \\notin B\\}$; "
            "4) Complementar: se $B \\subset A$, o complementar de $B$ em relação a $A$ é $C_A B = A - B$. "
            "As Leis de De Morgan estabelecem: $\\overline{A \\cup B} = \\overline{A} \\cap \\overline{B}$ e "
            "$\\overline{A \\cap B} = \\overline{A} \\cup \\overline{B}$."
        ),
    },
    {
        "numero_capitulo": 3,
        "pagina": 68,
        "teorema": "Definição Rigorosa de Função",
        "texto": (
            "Dados dois conjuntos não-vazios $A$ e $B$, uma relação binária $f$ de $A$ em $B$ é uma função (ou aplicação) "
            "se, e somente se, para TODO elemento $x \\in A$ existe um ÚNICO elemento $y \\in B$ tal que o par ordenado "
            "$(x, y) \\in f$. Formalmente: "
            "$$f: A \\to B \\iff (\\forall x \\in A)(\\exists! y \\in B)(y = f(x))$$"
            "O conjunto $A$ é denominado domínio da função ($D(f) = A$) e o conjunto $B$ é denominado contradomínio ($CD(f) = B$). "
            "Geometricamente no plano cartesiano, uma curva representa o gráfico de uma função se nenhuma reta vertical intersecta o gráfico em mais de um ponto."
        ),
    },
    {
        "numero_capitulo": 4,
        "pagina": 84,
        "teorema": "Domínio e Imagem de Funções Reais",
        "texto": (
            "Quando consideramos funções reais de variável real ($f: D \\subset \\mathbb{R} \\to \\mathbb{R}$), se o domínio não "
            "for explicitado, subentende-se que $D(f)$ é o conjunto de todos os números reais $x$ para os quais as operações indicadas "
            "em $f(x)$ são matematicamente possíveis e produzem um número real. As duas restrições fundamentais são: "
            "1) Denominadores não podem ser nulos: se $f(x) = \\frac{g(x)}{h(x)}$, deve-se impor $h(x) \\neq 0$; "
            "2) Radicandos de raízes de índice par devem ser não-negativos: se $f(x) = \\sqrt[2k]{g(x)}$, impõe-se $g(x) \\ge 0$. "
            "O conjunto imagem $\\text{Im}(f)$ é o subconjunto do contradomínio formado pelos valores reais atingidos por $f$: "
            "$$\\text{Im}(f) = \\{y \\in \\mathbb{R} \\mid \\exists x \\in D(f) \\text{ tal que } f(x) = y\\}$$"
        ),
    },
    {
        "numero_capitulo": 5,
        "pagina": 115,
        "teorema": "Função Afim e Taxa Média de Variação",
        "texto": (
            "Uma função $f: \\mathbb{R} \\to \\mathbb{R}$ chama-se função afim se existem constantes reais $a$ e $b$ tais que "
            "$f(x) = ax + b$, com $a \\neq 0$. O coeficiente $a$ é o coeficiente angular ou taxa de variação: "
            "$$a = \\frac{f(x_2) - f(x_1)}{x_2 - x_1} = \\frac{\\Delta y}{\\Delta x}$$"
            "O coeficiente $b$ é o coeficiente linear, indicando a ordenada do ponto onde a reta corta o eixo das ordenadas $(0, b)$. "
            "A raiz ou zero da função afim é o valor de $x$ tal que $f(x) = 0$, dado por $x = -\\frac{b}{a}$. "
            "Se $a > 0$, a função é estritamente crescente em $\\mathbb{R}$; se $a < 0$, a função é estritamente decrescente."
        ),
    },
    {
        "numero_capitulo": 6,
        "pagina": 150,
        "teorema": "Função Quadrática, Raízes e Vértice da Parábola",
        "texto": (
            "A função quadrática $f(x) = ax^2 + bx + c$ ($a \\neq 0$) tem como gráfico uma parábola de eixo vertical com concavidade voltada "
            "para cima se $a > 0$ e para baixo se $a < 0$. As raízes reais são obtidas pela fórmula resolutiva de Bhaskara: "
            "$$x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}, \\quad \\text{onde } \\Delta = b^2 - 4ac$$"
            "- Se $\\Delta > 0$, a função possui duas raízes reais distintas e corta o eixo $Ox$ em dois pontos; "
            "- Se $\\Delta = 0$, a parábola tangencia o eixo $Ox$ no ponto da raiz dupla; "
            "- Se $\\Delta < 0$, a função não possui raízes reais e a parábola não toca o eixo $Ox$. "
            "O vértice da parábola representa o ponto de mínimo (se $a > 0$) ou de máximo (se $a < 0$), dado por: "
            "$$V = \\left(-\\frac{b}{2a}, -\\frac{\\Delta}{4a}\\right)$$"
        ),
    },
]


async def run_ingestion():
    print("Iniciando processo de ingestão RAG da coleção Iezzi...")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    provedor = LLMFactory.obter_provedor()

    async with async_session() as session:
        # 1. Localiza o Volume 1 (Conjuntos e Funções)
        res_vol = await session.execute(
            select(VolumeDidatico).where(VolumeDidatico.numero_volume == 1)
        )
        volume_1 = res_vol.scalar_one_or_none()
        if not volume_1:
            print("ERRO: Volume 1 não encontrado no banco de dados. Execute o seed prévio da Etapa 5.")
            sys.exit(1)

        print(f"Volume localizado: Vol. {volume_1.numero_volume} - '{volume_1.titulo}' (ID: {volume_1.id})")

        # 2. Carrega capítulos do Volume 1 para associação de ID
        res_caps = await session.execute(
            select(Capitulo).where(Capitulo.volume_id == volume_1.id)
        )
        capitulos_map = {cap.numero_capitulo: cap.id for cap in res_caps.scalars().all()}

        # 3. Limpa fragmentos pré-existentes deste volume para reingestão limpa
        await session.execute(
            delete(DocumentoVetorialRAG).where(DocumentoVetorialRAG.volume_id == volume_1.id)
        )
        await session.commit()
        print("Fragmentos anteriores do Volume 1 removidos para nova indexação.")

        # 4. Processa cada fragmento gerando embeddings reais via LLMFactory.
        # Resiliência: cada fragmento tenta até 3 vezes (backoff exponencial);
        # falha definitiva em um fragmento NÃO aborta a ingestão dos demais.
        MAX_TENTATIVAS = 3
        sucessos = 0
        falhas = []
        for i, frag in enumerate(FRAGMENTOS_IEZZI_VOLUME_1, start=1):
            num_cap = frag["numero_capitulo"]
            cap_id = capitulos_map.get(num_cap)
            texto = frag["texto"]
            teorema = frag["teorema"]
            pagina = frag["pagina"]

            print(f"[{i}/{len(FRAGMENTOS_IEZZI_VOLUME_1)}] Gerando embedding para: '{teorema}' (Cap. {num_cap}, p. {pagina})...")

            embedding = None
            for tentativa in range(1, MAX_TENTATIVAS + 1):
                try:
                    # task_type='retrieval_document': vetores de INDEXAÇÃO devem
                    # usar o mesmo espaço semântico das futuras consultas RAG.
                    embedding = await provedor.gerar_embedding(texto, task_type="retrieval_document")
                    break
                except Exception as err:
                    print(f"  Tentativa {tentativa}/{MAX_TENTATIVAS} falhou: {err}")
                    if tentativa < MAX_TENTATIVAS:
                        await asyncio.sleep(2 ** tentativa)

            if embedding is None:
                print(f"  [ERRO] Fragmento '{teorema}' não indexado após {MAX_TENTATIVAS} tentativas.")
                falhas.append(teorema)
                continue

            if len(embedding) != 768:
                print(f"AVISO: Dimensão do vetor gerado ({len(embedding)}) ajustada para 768.")
                embedding = embedding[:768] if len(embedding) > 768 else embedding + [0.0] * (768 - len(embedding))

            doc = DocumentoVetorialRAG(
                id=uuid4(),
                volume_id=volume_1.id,
                capitulo_id=cap_id,
                trecho_conteudo=texto,
                metadados={
                    "pagina": pagina,
                    "teorema": teorema,
                    "numero_capitulo": num_cap,
                    "fonte": "Fundamentos de Matemática Elementar - Gelson Iezzi, Vol. 1",
                },
                embedding=embedding,
            )
            session.add(doc)
            sucessos += 1

        await session.commit()
        print(f"\nIngestão concluída! {sucessos}/{len(FRAGMENTOS_IEZZI_VOLUME_1)} fragmentos indexados no pgvector (HNSW) para o Volume 1.")
        if falhas:
            print(f"Fragmentos com falha (reexecute o script para tentar novamente): {falhas}")
            sys.exit(2)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_ingestion())
