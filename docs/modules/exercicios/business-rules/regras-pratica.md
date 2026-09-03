---
title: Exercícios - 2. Modos de Prática
type: module
status: draft
related:
  - modules/exercicios/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 2. Modos de Prática e Listas de Fixação

### 2.1 Listas de Fixação Pós-Aula

#### RN-EXE-007: Composição das Listas de Fixação
- Toda aula concluída disponibiliza imediatamente uma lista de 3 a 5 exercícios selecionados diretamente dos exercícios propostos do Iezzi correspondentes àquele capítulo.

#### RN-EXE-008: Dinâmica de 2ª Chance e Ponderação de Acertos
- Se o aluno errar a questão na primeira submissão:
  1. A questão **não** é considerada perdida imediatamente.
  2. O Tutor IA fornece uma **Pista Socrática** contextualizada.
  3. O aluno recebe permissão para uma **segunda tentativa**.
- **Ponderação Estatística**:
  - **Acerto na 1ª tentativa**: Ganho integral ($100\%$ de pontuação / valor $1.0$), refletindo domínio autônomo.
  - **Acerto na 2ª tentativa (com dica da IA)**: Ganho parcial de **50%** ($0.5$), reconhecendo o esforço orientado sem distorcer o cálculo de proficiência autônoma.
  - **Erro duplo (1ª e 2ª tentativas)**: Zero pontos ($0.0$), exibição da resolução passo a passo em KaTeX e acionamento do Ciclo de Recuperação Ativa (vide RN-EXE-008.1).

#### RN-EXE-008.1: Ciclo de Recuperação Ativa com Questão Gêmea
- Ao esgotar as 2 tentativas e visualizar a resolução completa, o sistema disponibiliza o botão: *"Tentar uma Questão Gêmea similar agora"*.
- A IA especialista do volume (com validação simbólica determinística via SymPy) gera uma nova questão com idêntica estrutura algébrica, mas valores numéricos inéditos.
- O acerto da Questão Gêmea atenua o impacto negativo no $\theta$ daquele capítulo e valida a superação da dúvida.
- A questão matriz original que gerou o erro duplo é automaticamente arquivada na **Caixa de Reforço** do aluno para futuras revisões espaçadas.

#### RN-EXE-009: Feedback Imediato em Modo Treino
- No modo fixação e treino de reforço, a confirmação de acerto/erro e a resolução comentada são exibidas logo após a resposta do aluno.

#### RN-EXE-010: Ausência de Feedback Intermediário no CAT
- Durante a realização da Prova Adaptativa (CAT), o sistema **não deve exibir** se a resposta foi correta ou incorreta, nem mostrar a resolução, para evitar viés emocional ou comportamental no teste.

#### RN-EXE-011: Sessões de Treino de Reforço Ilimitado
- O estudante pode iniciar sessões de prática livre em qualquer volume ou tópico, recebendo fluxo contínuo de questões gêmeas geradas por IA.
