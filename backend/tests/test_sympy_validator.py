"""
Testes unitários para o SympyMathValidator (Sandbox, Timeout e Equivalência Simbólica).
"""
import pytest
from app.sympy_engine.validator import SympyMathValidator


def test_sanitizacao_expressao_valida():
    expr = SympyMathValidator.sanitizar_expressao("2*x + 4")
    assert expr is not None
    assert str(expr) == "2*x + 4"


def test_bloqueio_padroes_maliciosos():
    assert SympyMathValidator.sanitizar_expressao("__import__('os').system('ls')") is None
    assert SympyMathValidator.sanitizar_expressao("eval('1+1')") is None
    assert SympyMathValidator.sanitizar_expressao("open('/etc/passwd')") is None
    assert SympyMathValidator.sanitizar_expressao("os.listdir('.')") is None
    assert SympyMathValidator.sanitizar_expressao("sys.path") is None
    assert SympyMathValidator.sanitizar_expressao("subprocess.Popen(['ls'])") is None


def test_funcoes_trigonometricas_nao_bloqueadas():
    """Regressão: 'os'/'sys' como substring não podem bloquear funções matemáticas legítimas."""
    assert SympyMathValidator.sanitizar_expressao("cos(x)") is not None
    assert SympyMathValidator.sanitizar_expressao("cosh(x)") is not None
    assert SympyMathValidator.sanitizar_expressao("2*cos(x) + 1") is not None
    assert SympyMathValidator.validar_equivalencia("cos(0)", "1") is True
    assert SympyMathValidator.validar_equivalencia("sin(pi/2)", "1") is True


def test_limite_tamanho_caracteres():
    expressao_gigante = "x + " * 100
    assert len(expressao_gigante) > SympyMathValidator.MAX_CARACTERES
    assert SympyMathValidator.sanitizar_expressao(expressao_gigante) is None


def test_equivalencia_algebrica_exata():
    assert SympyMathValidator.validar_equivalencia("x^2 - 4", "(x - 2)*(x + 2)") is True
    assert SympyMathValidator.validar_equivalencia("2*(x + 3)", "2*x + 6") is True
    assert SympyMathValidator.validar_equivalencia("x/2 + x/2", "x") is True


def test_equivalencia_algebrica_incorreta():
    assert SympyMathValidator.validar_equivalencia("x + 1", "x + 2") is False
    assert SympyMathValidator.validar_equivalencia("x^2", "x^3") is False


def test_equivalencia_numerica_com_tolerancia():
    # Tolerância aceita de +-0.01
    assert SympyMathValidator.validar_equivalencia("3.141", "3.14") is True
    assert SympyMathValidator.validar_equivalencia("5.005", "5.0") is True
    assert SympyMathValidator.validar_equivalencia("5.05", "5.0") is False  # Delta 0.05 > 0.01


def test_geracao_questao_gemea_quadratica():
    gemea = SympyMathValidator.gerar_questao_gemea_quadratica(r1_original=2, r2_original=3)

    assert "enunciado_katex" in gemea
    assert "alternativas" in gemea
    assert "resposta_correta" in gemea
    assert "resolucao_passo_a_passo" in gemea
    assert gemea["validado_sympy"] is True

    # Valida estrutura das 5 alternativas
    alternativas = gemea["alternativas"]
    assert len(alternativas) == 5
    letras = [alt["letra"] for alt in alternativas]
    assert letras == ["A", "B", "C", "D", "E"]

    # Deve haver exatamente uma alternativa correta
    corretas = [alt for alt in alternativas if alt["correta"] is True]
    assert len(corretas) == 1
    assert corretas[0]["letra"] == gemea["resposta_correta"]

    # Raízes devem ser inteiras diferentes de 0
    raizes = gemea["metadados_sympy"]["raizes"]
    assert len(raizes) == 2
    assert 0 not in raizes
