"""
Testes unitários para o Motor Psicométrico CAT (TRI 3PL e Estimador EAP Bayesiano).
"""
import pytest
from app.cat_engine.cat_service import CatEngine, ItemTRI


@pytest.fixture
def engine():
    return CatEngine(pontos_quadratura=61)


@pytest.fixture
def item_padrao():
    return ItemTRI(id="item-1", a=1.5, b=0.0, c=0.20, grande_area="algebra_funcoes")


def test_probabilidade_acerto_3pl(engine, item_padrao):
    # No ponto de inflexão theta = b = 0.0: P = c + (1 - c)/2 = 0.2 + 0.4 = 0.6
    p_b = engine.probabilidade_acerto(0.0, item_padrao)
    assert pytest.approx(p_b, rel=1e-3) == 0.6

    # Monotonicidade: P(theta) deve crescer com theta
    p_baixo = engine.probabilidade_acerto(-2.0, item_padrao)
    p_alto = engine.probabilidade_acerto(2.0, item_padrao)
    assert p_baixo < p_b < p_alto

    # Limites assintóticos
    p_muito_baixo = engine.probabilidade_acerto(-10.0, item_padrao)
    assert p_muito_baixo >= item_padrao.c  # Nunca menor que o chute
    p_muito_alto = engine.probabilidade_acerto(10.0, item_padrao)
    assert p_muito_alto <= 1.0


def test_informacao_fisher(engine):
    # Itens com maior discriminacao (a) geram mais informacao
    item_fraco = ItemTRI(id="1", a=0.8, b=0.0, c=0.2)
    item_forte = ItemTRI(id="2", a=2.0, b=0.0, c=0.2)

    info_fraco = engine.informacao_fisher(0.0, item_fraco)
    info_forte = engine.informacao_fisher(0.0, item_forte)
    assert info_forte > info_fraco


def test_selecao_mfi(engine):
    itens = [
        ItemTRI(id="facil", a=1.5, b=-2.0, c=0.2),
        ItemTRI(id="medio", a=1.5, b=0.0, c=0.2),
        ItemTRI(id="dificil", a=1.5, b=2.0, c=0.2),
    ]

    # Para um aluno com theta = 1.9, deve selecionar o item "dificil"
    melhor_para_avancado = engine.selecionar_proximo_item(1.9, itens, [])
    assert melhor_para_avancado.id == "dificil"

    # Para um aluno com theta = -1.9, deve selecionar o item "facil"
    melhor_para_iniciante = engine.selecionar_proximo_item(-1.9, itens, [])
    assert melhor_para_iniciante.id == "facil"


def test_estimador_eap_convergencia(engine):
    itens = [
        ItemTRI(id=f"item-{i}", a=1.5, b=-1.5 + i * 0.3, c=0.2)
        for i in range(10)
    ]

    # Caso 1: Aluno acerta todas as questões sequencialmente
    respostas_acertos = [(itens[i], 1) for i in range(10)]
    theta_acerto, se_acerto = engine.estimar_theta_eap(respostas_acertos)

    # Caso 2: Aluno erra todas as questões
    respostas_erros = [(itens[i], 0) for i in range(10)]
    theta_erro, se_erro = engine.estimar_theta_eap(respostas_erros)

    assert theta_acerto > 0.0
    assert theta_erro < 0.0
    # Com 10 respostas, o erro padrão deve ter reduzido consideravelmente em relação ao prior 1.0
    assert se_acerto < 0.8
    assert se_erro < 0.8


def test_selecao_area_alvo_cobertura_balanceada(engine):
    """RN-EXE-006: enquanto uma área canônica tiver < 2 respostas, ela é a alvo."""
    it_alg = ItemTRI(id="a1", a=1.5, b=0.0, c=0.2, grande_area="algebra_funcoes")
    it_geo = ItemTRI(id="g1", a=1.5, b=0.0, c=0.2, grande_area="geometria")

    # Sem respostas: a 1ª área canônica (algebra_funcoes) é a alvo
    assert engine.selecionar_area_alvo([]) == "algebra_funcoes"

    # 2 respondidas em algebra_funcoes: alvo passa a ser geometria
    assert engine.selecionar_area_alvo([(it_alg, 1), (it_alg, 0)]) == "geometria"

    # Todas as áreas com >= 2: sem alvo (MFI global)
    respostas = [(it_alg, 1), (it_alg, 1), (it_geo, 0), (it_geo, 0)]
    # Completa as outras 2 áreas com itens hipotéticos
    it_lin = ItemTRI(id="l1", a=1.5, b=0.0, c=0.2, grande_area="algebra_linear")
    it_apl = ItemTRI(id="p1", a=1.5, b=0.0, c=0.2, grande_area="aplicada")
    respostas += [(it_lin, 1), (it_lin, 0), (it_apl, 1), (it_apl, 1)]
    assert engine.selecionar_area_alvo(respostas) is None


def test_mfi_com_area_alvo_e_fallback(engine):
    itens = [
        ItemTRI(id="alg", a=2.0, b=0.0, c=0.2, grande_area="algebra_funcoes"),
        ItemTRI(id="geo", a=2.0, b=0.0, c=0.2, grande_area="geometria"),
    ]

    # Com área alvo, seleciona apenas da área pedida
    escolhido = engine.selecionar_proximo_item(0.0, itens, [], area_alvo="geometria")
    assert escolhido.id == "geo"

    # Fallback: área sem itens disponíveis -> busca em qualquer área
    escolhido_fb = engine.selecionar_proximo_item(
        0.0, itens, ["geo"], area_alvo="geometria"
    )
    assert escolhido_fb.id == "alg"


def test_scores_radar_multiplas_areas(engine):
    """Radar com 4 eixos: área com 2+ respostas tem EAP próprio; demais herdam theta geral."""
    itens_alg = [ItemTRI(id=f"a{i}", a=1.5, b=-1.0 + i, c=0.2, grande_area="algebra_funcoes") for i in range(3)]
    itens_geo = [ItemTRI(id=f"g{i}", a=1.5, b=1.0, c=0.2, grande_area="geometria") for i in range(2)]

    respostas = [(itens_alg[0], 1), (itens_alg[1], 1), (itens_alg[2], 1),
                 (itens_geo[0], 0), (itens_geo[1], 0)]

    theta_geral, _ = engine.estimar_theta_eap(respostas)
    scores = engine.calcular_scores_grandes_areas(respostas, theta_geral)

    # As 4 áreas canônicas sempre presentes
    assert set(scores.keys()) == {"algebra_funcoes", "geometria", "algebra_linear", "aplicada"}

    # algebra_funcoes (3 acertos) > theta_geral; geometria (2 erros) < theta_geral
    assert scores["algebra_funcoes"] > theta_geral
    assert scores["geometria"] < theta_geral

    # Áreas sem respostas herdam exatamente o theta geral
    assert scores["algebra_linear"] == round(float(theta_geral), 3)
    assert scores["aplicada"] == round(float(theta_geral), 3)


def test_criterio_parada(engine):
    # Menos de 12 itens nunca encerra
    assert engine.deve_encerrar_teste(total_itens_aplicados=11, erro_padrao=0.25) is False

    # 12 itens com SE <= 0.30 encerra
    assert engine.deve_encerrar_teste(total_itens_aplicados=12, erro_padrao=0.29) is True

    # 12 itens com SE > 0.30 continua
    assert engine.deve_encerrar_teste(total_itens_aplicados=12, erro_padrao=0.35) is False

    # 20 itens atinge o teto maximo e encerra mesmo com SE > 0.30
    assert engine.deve_encerrar_teste(total_itens_aplicados=20, erro_padrao=0.35) is True
