"""
Máquina de Estados Finita (FSM) da Mediação Socrática.
Conforme especificação em docs-site/docs/modules/conteudo/prototype/socratic-tutor.md.
"""
import re
from typing import Optional


class SocraticStateManager:
    """Gerencia a progressão e reset do nível socrático pedagógico por tópico/mensagem."""

    GATILHOS_PEDIDO_DICA = re.compile(
        r"(não entendi|como assim|dica|mais|ajuda|não sei|passo|explica|continua|travei|socorro|qual fórmula|como faz|perdi)",
        re.IGNORECASE
    )

    @classmethod
    def determinar_proximo_estagio(
        cls,
        estagio_atual: int,
        topico_atual: Optional[str] = None,
        ultimo_topico_registrado: Optional[str] = None,
        mensagem_aluno: str = ""
    ) -> int:
        """
        Calcula o estágio socrático adequado (1 a 3):
        - Se houve mudança de tópico/fórmula selecionada: Reseta para Estágio 1 (Reflexão).
        - Se o aluno expressou dificuldade ou pediu dica explícita no mesmo tópico: Avança estágio (máx 3).
        - Se já está no Estágio 0 ou negativo: Inicializa em 1.
        - Caso contrário: Mantém o estágio atual para consolidação.
        """
        # Se houve mudança de tópico ou seleção de nova fórmula, reinicia o ciclo pedagógico
        if topico_atual and ultimo_topico_registrado and topico_atual.strip() != ultimo_topico_registrado.strip():
            return 1

        # Inicialização
        if estagio_atual < 1:
            return 1

        # Se o aluno solicita explicitamente mais ajuda no mesmo assunto
        if cls.GATILHOS_PEDIDO_DICA.search(mensagem_aluno):
            return min(3, estagio_atual + 1)

        return min(3, max(1, estagio_atual))
