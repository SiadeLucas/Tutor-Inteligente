---
title: Exercícios - Algoritmo Psicométrico do CAT (TRI)
type: module
status: draft
related:
  - modules/exercicios/prototype/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 2. Motor Psicométrico CAT (Python, NumPy & SciPy)

Implementação executável do **Teste Adaptativo Computadorizado (CAT)** fundamentado na **Teoria da Resposta ao Item (TRI)** sob os modelos logísticos de 2 e 3 parâmetros (2PL e 3PL).

---

## Código Fonte (`backend/app/cat_engine/cat_service.py`)

```python
import numpy as np
from typing import List, Dict, Tuple, Optional


class ItemTRI:
    """Representa um item calibrado no banco de questões."""
    def __init__(self, id: str, a: float, b: float, c: float = 0.2, grande_area: str = "algebra_funcoes"):
        self.id = id
        self.a = float(a)          # Parâmetro de discriminação (a > 0)
        self.b = float(b)          # Parâmetro de dificuldade (-3.0 a +3.0)
        self.c = float(c)          # Parâmetro de acerto casual / chute (típico: 0.20 para 5 opções)
        self.grande_area = grande_area


class CatEngine:
    """Motor de cálculo adaptativo em circuito fechado."""
    
    CONSTANTE_D = 1.7  # Fator de escala para aproximação com a ogiva normal
    
    def __init__(self, pontos_quadratura: int = 61):
        # Grade de quadratura numérica de -3.0 a +3.0 (passo 0.1)
        self.thetas = np.linspace(-3.0, 3.0, pontos_quadratura)
        # Prior padrão: Normal padrão N(0, 1)
        self.prior = (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * self.thetas**2)
        self.prior /= np.sum(self.prior)

    def probabilidade_acerto(self, theta: float, item: ItemTRI) -> float:
        """Calcula P_i(theta) segundo o modelo 3PL."""
        expoente = -self.CONSTANTE_D * item.a * (theta - item.b)
        # Proteção contra overflow numérico
        expoente = np.clip(expoente, -30.0, 30.0)
        prob_logistica = 1.0 / (1.0 + np.exp(expoente))
        return item.c + (1.0 - item.c) * prob_logistica

    def informacao_fisher(self, theta: float, item: ItemTRI) -> float:
        """Calcula a Função de Informação de Fisher I_i(theta)."""
        P = self.probabilidade_acerto(theta, item)
        Q = 1.0 - P
        expoente = -self.CONSTANTE_D * item.a * (theta - item.b)
        expoente = np.clip(expoente, -30.0, 30.0)
        
        # Derivada P'_i(theta)
        derivada_P = (self.CONSTANTE_D * item.a * (1.0 - item.c) * np.exp(expoente)) / ((1.0 + np.exp(expoente))**2)
        
        if P * Q == 0:
            return 0.0
        return (derivada_P**2) / (P * Q)

    def selecionar_proximo_item(
        self, 
        theta_atual: float, 
        banco_disponivel: List[ItemTRI], 
        itens_ja_aplicados_ids: List[str],
        area_alvo: Optional[str] = None
    ) -> Optional[ItemTRI]:
        """
        Critério de Seleção por Máxima Informação de Fisher (MFI).
        Seleciona o item disponível que maximiza I_i(theta_atual).
        """
        candidatos = [
            item for item in banco_disponivel 
            if item.id not in itens_ja_aplicados_ids
            and (area_alvo is None or item.grande_area == area_alvo)
        ]
        
        if not candidatos:
            return None
            
        melhor_item = max(
            candidatos, 
            key=lambda it: self.informacao_fisher(theta_atual, it)
        )
        return melhor_item

    def estimar_theta_eap(
        self, 
        respostas: List[Tuple[ItemTRI, int]]
    ) -> Tuple[float, float]:
        """
        Estimador Bayesiano EAP (Expected A Posteriori).
        Retorna: (theta_estimado, erro_padrao_se)
        """
        if not respostas:
            return 0.0, 1.0  # Sem respostas: prior puro theta=0.0, SE=1.0

        # Calcula a função de verossimilhança L(X | theta) na grade
        verossimilhanca = np.ones_like(self.thetas)
        
        for item, acertou in respostas:
            P_grid = np.array([self.probabilidade_acerto(th, item) for th in self.thetas])
            if acertou == 1:
                verossimilhanca *= P_grid
            else:
                verossimilhanca *= (1.0 - P_grid)

        # Distribuição a posteriori
        posterior = verossimilhanca * self.prior
        soma_posterior = np.sum(posterior)
        
        if soma_posterior == 0:
            # Degeneração numérica extrema: fallback
            return 0.0, 1.0

        posterior /= soma_posterior

        # Média a posteriori (Theta)
        theta_eap = float(np.sum(self.thetas * posterior))
        
        # Variância a posteriori e Erro Padrão (SE)
        variancia = float(np.sum(((self.thetas - theta_eap)**2) * posterior))
        erro_padrao = float(np.sqrt(variancia))

        return theta_eap, erro_padrao

    def deve_encerrar_teste(self, total_itens_aplicados: int, erro_padrao: float) -> bool:
        """
        Critério de Parada Híbrido:
        1. Erro padrão de mensuração SE < 0.30 (precisão excelente), OU
        2. Limite máximo de 20 questões atingido, respeitando o mínimo de 12 questões.
        """
        if total_itens_aplicados < 12:
            return False
        if erro_padrao < 0.30 or total_itens_aplicados >= 20:
            return True
        return False
```
