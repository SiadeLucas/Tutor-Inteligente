"""
Suíte de Testes Automatizados para Conversão de Raiz em Exponencial (RN-EXE-017).
Garante que todas as raízes (\\sqrt e \\sqrt[n]) sejam convertidas na representação
exponencial fracionária equivalente, tanto em expressões isoladas quanto em modelos Pydantic
e na geração de questões gêmeas.
"""
from pathlib import Path
import sys
import uuid

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

try:
    import pytest
except ImportError:
    pytest = None

from app.modules.exercises.formatters import converter_raiz_em_exponencial

try:
    from app.modules.exercises.schemas import AlternativaItem, ItemExercicioResponse, SubmissaoExercicioResponse
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

try:
    from app.sympy_engine.validator import SympyMathValidator
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False



class TestSqrtConverter:
    """Testes unitários da função converter_raiz_em_exponencial."""

    def test_raiz_quadrada_simples(self):
        assert converter_raiz_em_exponencial(r"\sqrt{2}") == r"2^{1/2}"
        assert converter_raiz_em_exponencial(r"\sqrt{5}") == r"5^{1/2}"
        assert converter_raiz_em_exponencial(r"\sqrt{x}") == r"x^{1/2}"

    def test_coeficiente_numerico_justaposto(self):
        # Deve inserir multiplicação explícita \cdot para não fundir números
        assert converter_raiz_em_exponencial(r"4\sqrt{2}") == r"4 \cdot 2^{1/2}"
        assert converter_raiz_em_exponencial(r"10\sqrt{3}") == r"10 \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"216\sqrt{2}") == r"216 \cdot 2^{1/2}"

    def test_coeficiente_numerico_com_espaco(self):
        assert converter_raiz_em_exponencial(r"4 \sqrt{2}") == r"4 \cdot 2^{1/2}"
        assert converter_raiz_em_exponencial(r"10 \sqrt{3}") == r"10 \cdot 3^{1/2}"

    def test_variavel_ou_simbolo_justaposto(self):
        assert converter_raiz_em_exponencial(r"l\sqrt{3}") == r"l \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"a\sqrt{3}") == r"a \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"R\sqrt{3}") == r"R \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"i\sqrt{3}") == r"i \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"2i\sqrt{3}") == r"2i \cdot 3^{1/2}"

    def test_potencia_justaposta(self):
        assert converter_raiz_em_exponencial(r"l^2\sqrt{3}") == r"l^2 \cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"6^2\sqrt{3}") == r"6^2 \cdot 3^{1/2}"

    def test_fracoes_e_delimitadores(self):
        assert converter_raiz_em_exponencial(r"\frac{\sqrt{3}}{2}") == r"\frac{3^{1/2}}{2}"
        assert converter_raiz_em_exponencial(r"\frac{1}{\sqrt{x}}") == r"\frac{1}{x^{1/2}}"
        assert converter_raiz_em_exponencial(r"\frac{l^2\sqrt{3}}{4}") == r"\frac{l^2 \cdot 3^{1/2}}{4}"

    def test_comandos_latex_anteriores(self):
        assert converter_raiz_em_exponencial(r"\pm \sqrt{\Delta}") == r"\pm \Delta^{1/2}"
        assert converter_raiz_em_exponencial(r"\pm\sqrt{\Delta}") == r"\pm \Delta^{1/2}"
        assert converter_raiz_em_exponencial(r"\cdot \sqrt{3}") == r"\cdot 3^{1/2}"
        assert converter_raiz_em_exponencial(r"\cdot\sqrt{3}") == r"\cdot 3^{1/2}"

    def test_radicando_composto_com_parenteses(self):
        assert converter_raiz_em_exponencial(r"\sqrt{3x - 12}") == r"(3x - 12)^{1/2}"
        assert converter_raiz_em_exponencial(r"\sqrt{1 - 0{,}64}") == r"(1 - 0{,}64)^{1/2}"
        assert converter_raiz_em_exponencial(r"\sqrt{a^2 + b^2}") == r"(a^2 + b^2)^{1/2}"
        assert converter_raiz_em_exponencial(r"\sqrt{a^2 + b^2 + c^2}") == r"(a^2 + b^2 + c^2)^{1/2}"

    def test_raiz_de_ordem_n(self):
        assert converter_raiz_em_exponencial(r"\sqrt[3]{8}") == r"8^{1/3}"
        assert converter_raiz_em_exponencial(r"\sqrt[n]{\rho}") == r"\rho^{1/n}"
        assert converter_raiz_em_exponencial(r"\sqrt[4]{x + 1}") == r"(x + 1)^{1/4}"

    def test_raizes_aninhadas(self):
        entrada = r"\sqrt{(-2)^2 + (2\sqrt{3})^2}"
        esperado = r"((-2)^2 + (2 \cdot 3^{1/2})^2)^{1/2}"
        assert converter_raiz_em_exponencial(entrada) == esperado

    def test_texto_completo_com_varias_raizes(self):
        texto = r"O valor simplificado de $\sqrt{50} - \sqrt{18} + \sqrt{8}$ é:"
        esperado = r"O valor simplificado de $50^{1/2} - 18^{1/2} + 8^{1/2}$ é:"
        assert converter_raiz_em_exponencial(texto) == esperado


class TestSchemasSanitization:
    """Valida a sanitização automática nos schemas Pydantic v2."""

    def test_alternativa_item_sanitizacao(self):
        if not HAS_PYDANTIC:
            print("    [SKIP] Pydantic não disponível no ambiente host (executado no container).")
            return
        alt = AlternativaItem(letra="B", texto_katex=r"$4\sqrt{2}\text{ cm}$")
        assert alt.texto_katex == r"$4 \cdot 2^{1/2}\text{ cm}$"

    def test_item_exercicio_response_sanitizacao(self):
        if not HAS_PYDANTIC:
            print("    [SKIP] Pydantic não disponível no ambiente host (executado no container).")
            return
        item = ItemExercicioResponse(
            id=uuid.uuid4(),
            capitulo_id=uuid.uuid4(),
            enunciado_katex=r"Calcule o valor de $f(x) = \frac{\sqrt{2x - 6}}{x - 7}$.",
            alternativas=[
                AlternativaItem(letra="A", texto_katex=r"$\sqrt{2}$"),
                AlternativaItem(letra="B", texto_katex=r"$3\sqrt{5}$"),
            ],
        )
        assert item.enunciado_katex == r"Calcule o valor de $f(x) = \frac{(2x - 6)^{1/2}}{x - 7}$."
        assert item.alternativas[0].texto_katex == r"$2^{1/2}$"
        assert item.alternativas[1].texto_katex == r"$3 \cdot 5^{1/2}$"

    def test_submissao_exercicio_response_sanitizacao(self):
        if not HAS_PYDANTIC:
            print("    [SKIP] Pydantic não disponível no ambiente host (executado no container).")
            return
        res = SubmissaoExercicioResponse(
            acertou=True,
            pontuacao_obtida=1.0,
            permite_segunda_chance=False,
            resolucao_completa_katex=r"Aplicando Bhaskara: $x = \frac{-b \pm \sqrt{\Delta}}{2a}$.",
        )
        assert res.resolucao_completa_katex == r"Aplicando Bhaskara: $x = \frac{-b \pm \Delta^{1/2}}{2a}$."


class TestTwinQuestionNoSqrt:
    """Garante que a geração de questões gêmeas nunca produza \\sqrt."""

    def test_questao_gemea_quadratica_sem_sqrt(self):
        if not HAS_SYMPY:
            print("    [SKIP] SymPy não disponível no ambiente host (executado no container).")
            return
        gemea = SympyMathValidator.gerar_questao_gemea_quadratica(r1_original=2, r2_original=3)
        assert r"\sqrt" not in gemea["resolucao_passo_a_passo"]
        assert r"\Delta^{1/2}" in gemea["resolucao_passo_a_passo"]



if __name__ == "__main__":
    import sys
    test_classes = [TestSqrtConverter, TestSchemasSanitization, TestTwinQuestionNoSqrt]
    total_passed = 0
    total_failed = 0

    print("=" * 60)
    print("Iniciando Bateria de Testes: Conversor de Raiz em Exponencial")
    print("=" * 60)

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_") and callable(getattr(instance, m))]
        for method_name in methods:
            try:
                getattr(instance, method_name)()
                print(f"  [PASS] {cls.__name__}.{method_name}")
                total_passed += 1
            except Exception as e:
                print(f"  [FAIL] {cls.__name__}.{method_name}: {e}")
                total_failed += 1

    print("=" * 60)
    print(f"Resultado Final: {total_passed} passaram, {total_failed} falharam.")
    print("=" * 60)

    if total_failed > 0:
        sys.exit(1)

