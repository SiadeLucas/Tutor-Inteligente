"""
Motor Psicométrico CAT (Computerized Adaptive Testing) fundamentado na Teoria da Resposta ao Item (TRI).
Modelo logístico 3PL com estimador Bayesiano EAP (Expected A Posteriori) e seleção MFI (Maximum Fisher Information).
Conforme documentado em docs-site/docs/modules/exercicios/prototype/cat-engine.md.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional


class ItemTRI:
    """Representa um item calibrado na métrica psicométrica TRI."""

    def __init__(
        self,
        id: str,
        a: float,
        b: float,
        c: float = 0.200,
        grande_area: str = "algebra_funcoes",
    ):
        self.id = str(id)
        self.a = float(a)  # Parâmetro de discriminação (a > 0, típico: 0.5 a 2.5)
        self.b = float(b)  # Parâmetro de dificuldade (-3.0 a +3.0)
        self.c = float(c)  # Parâmetro de acerto casual (0.20 para 5 alternativas)
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
        """Calcula P_i(theta) segundo o modelo logístico 3PL."""
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

        # Derivada analítica P'_i(theta)
        derivada_P = (
            self.CONSTANTE_D
            * item.a
            * (1.0 - item.c)
            * np.exp(expoente)
        ) / ((1.0 + np.exp(expoente)) ** 2)

        if P * Q == 0:
            return 0.0
        return float((derivada_P**2) / (P * Q))

    def selecionar_proximo_item(
        self,
        theta_atual: float,
        banco_disponivel: List[ItemTRI],
        itens_ja_aplicados_ids: List[str],
        area_alvo: Optional[str] = None,
    ) -> Optional[ItemTRI]:
        """
        Critério de Seleção por Máxima Informação de Fisher (MFI).
        Seleciona o item não aplicado que maximiza a informação no theta corrente.
        """
        itens_aplicados_set = set(str(item_id) for item_id in itens_ja_aplicados_ids)
        candidatos = [
            item
            for item in banco_disponivel
            if item.id not in itens_aplicados_set
            and (area_alvo is None or item.grande_area == area_alvo)
        ]

        if not candidatos:
            # Fallback se não encontrar na área alvo: busca em qualquer área
            if area_alvo is not None:
                candidatos = [
                    item
                    for item in banco_disponivel
                    if item.id not in itens_aplicados_set
                ]
            if not candidatos:
                return None

        melhor_item = max(
            candidatos,
            key=lambda it: self.informacao_fisher(theta_atual, it),
        )
        return melhor_item

    def estimar_theta_eap(
        self,
        respostas: List[Tuple[ItemTRI, int]],
    ) -> Tuple[float, float]:
        """
        Estimador Bayesiano EAP (Expected A Posteriori).
        Calcula média a posteriori (theta) e desvio padrão a posteriori (erro padrão SE).
        """
        if not respostas:
            return 0.0, 1.0  # Sem respostas: prior N(0, 1) puro

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

        if soma_posterior <= 0 or np.isnan(soma_posterior):
            # Fallback em caso de degeneração numérica extrema
            return 0.0, 1.0

        posterior /= soma_posterior

        # Média a posteriori (Theta)
        theta_eap = float(np.sum(self.thetas * posterior))

        # Variância a posteriori e Erro Padrão (SE)
        variancia = float(np.sum(((self.thetas - theta_eap) ** 2) * posterior))
        erro_padrao = float(np.sqrt(max(variancia, 1e-6)))

        return theta_eap, erro_padrao

    # Áreas canônicas da taxonomia oficial (RN-EXE-006 / data-architecture.md)
    AREAS_PADRAO = [
        "algebra_funcoes",
        "geometria",
        "algebra_linear",
        "aplicada",
    ]

    def selecionar_area_alvo(
        self,
        respostas: List[Tuple[ItemTRI, int]],
        minimo_por_area: int = 2,
    ) -> Optional[str]:
        """
        Política de cobertura balanceada do Radar (RN-EXE-006):
        enquanto alguma Grande Área canônica tiver menos de `minimo_por_area` itens
        respondidos, retorna a área menos coberta (empates em ordem canônica) para
        direcionar a seleção MFI. Retorna None quando todas as áreas estão cobertas
        (ou quando o banco não possui itens da área faltante — nesse caso a seleção
        degrada graciosamente para o MFI global, sem bloquear a prova).
        """
        contagem = {area: 0 for area in self.AREAS_PADRAO}
        for item, _ in respostas:
            if item.grande_area in contagem:
                contagem[item.grande_area] += 1
        return next(
            (area for area in self.AREAS_PADRAO if contagem[area] < minimo_por_area),
            None,
        )

    def deve_encerrar_teste(self, total_itens_aplicados: int, erro_padrao: float) -> bool:
        """
        Critério de Parada Híbrido:
        - Mínimo de 12 questões.
        - Encerra quando SE <= 0.30 (precisão Bayesiana suficiente) ou atinge o teto de 20 questões.
        """
        if total_itens_aplicados < 12:
            return False
        if erro_padrao <= 0.30 or total_itens_aplicados >= 20:
            return True
        return False

    def calcular_scores_grandes_areas(
        self,
        respostas: List[Tuple[ItemTRI, int]],
        theta_geral: float,
    ) -> Dict[str, float]:
        """
        Calcula as pontuações estimadas para o Radar Chart agrupadas por Grande Área.
        Taxonomia canônica (docs knowledge/data-architecture.md e Tabela 07):
        'algebra_funcoes', 'geometria', 'algebra_linear', 'aplicada' (RN-EXE-006).
        """
        areas_padrao = [
            "algebra_funcoes",
            "geometria",
            "algebra_linear",
            "aplicada",
        ]

        scores: Dict[str, float] = {}

        for area in areas_padrao:
            respostas_area = [r for r in respostas if r[0].grande_area == area]
            if len(respostas_area) >= 2:
                # Se respondeu 2 ou mais questões desta área, estima o theta específico da área
                th_area, _ = self.estimar_theta_eap(respostas_area)
                scores[area] = round(float(th_area), 3)
            elif len(respostas_area) == 1:
                # Pondera com o theta geral
                acertou = respostas_area[0][1]
                delta = 0.2 if acertou == 1 else -0.2
                scores[area] = round(float(theta_geral + delta), 3)
            else:
                # Herda o theta geral com leve variação neutra
                scores[area] = round(float(theta_geral), 3)

        return scores
