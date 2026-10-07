"""
Bateria de Testes Automatizados — Randomizador de Alternativas (Prova CAT e Seeds TRI).
Valida:
1. Integridade do embaralhamento (nenhum distrator perdido, marcação de correta).
2. Posicionamento determinístico por letra alvo.
3. Atualização semântica e didática das resoluções KaTeX.
4. Distribuição perfeitamente equilibrada (~20% para cada letra: A, B, C, D, E).
5. Determinismo e isolamento por sessão na Prova Adaptativa CAT (runtime).
6. Preservação estrita de itens numéricos.
"""

from collections import Counter
try:
    import pytest
    fixture = pytest.fixture
except ImportError:
    def fixture(fn):
        return fn
from app.modules.exercises.randomizer import (
    LETRAS_PADRAO,
    embaralhar_alternativas,
    atualizar_texto_resolucao,
    randomizar_item_exercicio,
    balancear_itens,
    obter_alternativas_randomizadas_cat,
)


@fixture
def alternativas_exemplo():
    return [
        {"letra": "A", "texto": r"$x = 2$", "correta": True},
        {"letra": "B", "texto": r"$x = -2$", "correta": False},
        {"letra": "C", "texto": r"$x = 0$", "correta": False},
        {"letra": "D", "texto": r"$x = 4$", "correta": False},
        {"letra": "E", "texto": r"$x = \emptyset$", "correta": False},
    ]


def test_embaralhar_alternativas_integridade(alternativas_exemplo):
    """Garante que todas as 5 alternativas continuam presentes e apenas uma é correta."""
    novas, nova_letra, letra_antiga = embaralhar_alternativas(
        alternativas=alternativas_exemplo,
        resposta_correta="A",
    )

    assert letra_antiga == "A"
    assert nova_letra in LETRAS_PADRAO
    assert len(novas) == 5

    # Letras devem ser sequenciais A, B, C, D, E
    assert [alt["letra"] for alt in novas] == LETRAS_PADRAO

    # Exatamente uma alternativa deve ser marcada como correta
    corretas = [alt for alt in novas if alt["correta"]]
    assert len(corretas) == 1
    assert corretas[0]["letra"] == nova_letra
    assert corretas[0]["texto"] == r"$x = 2$"

    # Todos os textos originais devem estar presentes
    textos_originais = {alt["texto"] for alt in alternativas_exemplo}
    textos_novos = {alt["texto"] for alt in novas}
    assert textos_originais == textos_novos


def test_embaralhar_com_letra_alvo_especifica(alternativas_exemplo):
    """Garante que a alternativa correta é alocada na letra alvo solicitada."""
    for letra_esperada in ["A", "B", "C", "D", "E"]:
        novas, nova_letra, _ = embaralhar_alternativas(
            alternativas=alternativas_exemplo,
            resposta_correta="A",
            letra_alvo=letra_esperada,
        )
        assert nova_letra == letra_esperada
        alt_correta = next(alt for alt in novas if alt["letra"] == letra_esperada)
        assert alt_correta["correta"] is True
        assert alt_correta["texto"] == r"$x = 2$"


def test_atualizar_texto_resolucao():
    """Valida a atualização da letra correta na explicação pedagógica passo a passo."""
    # Caso 1: Substituição direta de 'Alternativa A.'
    res1 = "1. Calculamos as raízes. 2. Alternativa A."
    assert atualizar_texto_resolucao(res1, "A", "C") == "1. Calculamos as raízes. 2. Alternativa C."

    # Caso 2: Substituição de 'Alternativa A' sem ponto
    res2 = "Portanto temos Alternativa A como resposta final"
    assert atualizar_texto_resolucao(res2, "A", "E") == "Portanto temos Alternativa E como resposta final"

    # Caso 3: Substituição de 'Letra A'
    res3 = "Conforme demonstrado na Letra A."
    assert atualizar_texto_resolucao(res3, "A", "B") == "Conforme demonstrado na Letra B."

    # Caso 4: Texto sem menção a Alternativa (anexa com clareza ao final)
    res4 = "O valor encontrado para x é 10."
    assert atualizar_texto_resolucao(res4, "A", "D") == "O valor encontrado para x é 10. Alternativa D."


def test_balancear_itens_distribuicao_uniforme(alternativas_exemplo):
    """Garante que em um lote de 50 itens a distribuição seja exatamente 10 para cada letra (20%)."""
    itens = [
        {
            "numero_capitulo": 1,
            "tipo_item": "multiple_choice",
            "enunciado_katex": f"Questão {i}",
            "alternativas": list(alternativas_exemplo),
            "resposta_correta": "A",
            "resolucao_passo_a_passo": "Alternativa A.",
        }
        for i in range(50)
    ]

    balanceados = balancear_itens(itens, seed=99)
    dist = Counter(it["resposta_correta"] for it in balanceados)

    assert dist["A"] == 10
    assert dist["B"] == 10
    assert dist["C"] == 10
    assert dist["D"] == 10
    assert dist["E"] == 10

    # Verifica também a consistência interna de cada item balanceado
    for it in balanceados:
        letra_gabarito = it["resposta_correta"]
        alt_correta = next(a for a in it["alternativas"] if a["letra"] == letra_gabarito)
        assert alt_correta["correta"] is True
        assert f"Alternativa {letra_gabarito}" in it["resolucao_passo_a_passo"]


def test_runtime_cat_determinismo_e_variacao(alternativas_exemplo):
    """Valida que o randomizador CAT por sessão é determinístico por item/sessão e varia entre sessões."""
    sessao_1 = "sessao-cat-aluno-1"
    sessao_2 = "sessao-cat-aluno-2"
    item_id = "item-matematica-101"

    # Duas chamadas para a mesma sessão e mesmo item (ex: F5 / recarregamento de página)
    alts_1a, gab_1a = obter_alternativas_randomizadas_cat(
        alternativas_exemplo, "A", sessao_1, item_id
    )
    alts_1b, gab_1b = obter_alternativas_randomizadas_cat(
        alternativas_exemplo, "A", sessao_1, item_id
    )

    assert gab_1a == gab_1b
    assert [a["letra"] + a["texto"] for a in alts_1a] == [a["letra"] + a["texto"] for a in alts_1b]

    # Chamada para outra sessão (outro aluno realizando a mesma questão)
    # Testa múltiplas sessões para verificar que o gabarito não é estático
    gabaritos_outros = set()
    for i in range(10):
        _, gab_outro = obter_alternativas_randomizadas_cat(
            alternativas_exemplo, "A", f"sessao-{i}", item_id
        )
        gabaritos_outros.add(gab_outro)

    # Com 10 sessões aleatórias, deve haver variação de gabaritos (não apenas uma letra)
    assert len(gabaritos_outros) > 1


def test_itens_numericos_preservados():
    """Garante que itens sem alternativas ou numéricos não sofrem mutação."""
    item_num = {
        "tipo_item": "numeric_input",
        "enunciado_katex": "Calcule $2 + 2$",
        "alternativas": [],
        "resposta_correta": "4",
        "resolucao_passo_a_passo": "$2 + 2 = 4$.",
    }
    resultado = randomizar_item_exercicio(dict(item_num))
    assert resultado["resposta_correta"] == "4"
    assert resultado["alternativas"] == []
    assert resultado["resolucao_passo_a_passo"] == "$2 + 2 = 4$."
