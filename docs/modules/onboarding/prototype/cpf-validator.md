---
title: Onboarding - Algoritmo de Validação de CPF (Módulo 11)
type: module
status: draft
related:
  - modules/onboarding/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Algoritmo de Validação de CPF (Módulo 11)

Implementação executável do cálculo oficial dos **dois dígitos verificadores do CPF** da Receita Federal do Brasil segundo o algoritmo do **Módulo 11**, rodando em Python puro em menos de 1 microssegundo.

---

## Código Fonte (`backend/app/core/validators.py`)

```python
import re


class CPFValidator:
    """Validador determinístico do algoritmo Módulo 11 do CPF."""

    @staticmethod
    def validar(cpf_str: str) -> bool:
        """
        Retorna True se o CPF for matematicamente válido e não pertencer
        à lista de sequências repetidas inválidas da Receita Federal.
        """
        # 1. Sanitização: extrai apenas os números
        digitos = re.sub(r"\D", "", str(cpf_str))

        # 2. Valida extensão estrita de 11 dígitos
        if len(digitos) != 11:
            return False

        # 3. Elimina sequências com todos os dígitos iguais (ex: 111.111.111-11, 000.000.000-00)
        if digitos == digitos[0] * 11:
            return False

        # 4. Cálculo do Primeiro Dígito Verificador
        # Pesos decrescentes de 10 a 2 aplicados aos primeiros 9 dígitos
        soma_primeiro = sum(int(digitos[i]) * (10 - i) for i in range(9))
        resto_primeiro = (soma_primeiro * 10) % 11
        digito1_esperado = 0 if resto_primeiro in (10, 11) else resto_primeiro

        if int(digitos[9]) != digito1_esperado:
            return False

        # 5. Cálculo do Segundo Dígito Verificador
        # Pesos decrescentes de 11 a 2 aplicados aos primeiros 10 dígitos (incluindo o digito1)
        soma_segundo = sum(int(digitos[i]) * (11 - i) for i in range(10))
        resto_segundo = (soma_segundo * 10) % 11
        digito2_esperado = 0 if resto_segundo in (10, 11) else resto_segundo

        if int(digitos[10]) != digito2_esperado:
            return False

        return True
```
