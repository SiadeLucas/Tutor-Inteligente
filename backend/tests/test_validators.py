"""
Testes do validador de CPF (Módulo 11) — Etapa 4: Onboarding.
Referência: docs-site/docs/modules/onboarding/prototype/cpf-validator.md
"""
import pytest

from app.core.validators import CPFValidator


@pytest.mark.parametrize(
    "cpf_valido",
    [
        "529.982.247-25",   # CPF clássico válido, formatado
        "52998224725",      # Mesmo CPF, apenas dígitos
        "168.995.350-09",   # Válido com pontuação
        "798.254.489-46",   # Válido calculado pelo Módulo 11
    ],
)
def test_cpf_valido(cpf_valido: str):
    assert CPFValidator.validar(cpf_valido) is True


@pytest.mark.parametrize(
    "cpf_invalido",
    [
        "529.982.247-24",      # Dígito verificador errado
        "111.111.111-11",      # Sequência repetida (RN: rejeitado)
        "000.000.000-00",      # Sequência repetida
        "12345678900",         # Dígitos sequenciais inválidos
        "5299822472",          # 10 dígitos
        "529982247250",        # 12 dígitos
        "",                    # Vazio
        "abcdefghijk",         # Sem dígitos
        "529.982.24a",         # Parcialmente alfabético (menos de 11 dígitos)
    ],
)
def test_cpf_invalido(cpf_invalido: str):
    assert CPFValidator.validar(cpf_invalido) is False


def test_cpf_normalizar():
    assert CPFValidator.normalizar("529.982.247-25") == "52998224725"
    assert CPFValidator.normalizar("abc52998224725xyz") == "52998224725"
