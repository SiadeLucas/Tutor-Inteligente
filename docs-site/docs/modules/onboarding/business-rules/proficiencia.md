---
title: Onboarding - 2. Prova de Proficiência
type: module
status: draft
related:
  - modules/onboarding/business-rules/index.md
  - modules/onboarding/business-rules/escalabilidade.md
last_updated: "2026-09-07"
updated_by: buffy
---

# 2. Prova de Proficiência Adaptativa

### 2.1 Mecanismo e Gatilhos de Avaliação

#### RN-CAT-001: Gatilho de Ativação por Matéria
- A prova diagnóstica é disparada na primeira vez em que o aluno acessa qualquer matéria curricular.
- O wizard de cadastro tem **3 etapas e não inicializa sessão CAT**: imediatamente após a finalização do cadastro, o aluno é direcionado ao dashboard de matérias e, ao entrar em Matemática pela primeira vez, a prova é apresentada.

#### RN-CAT-002: Opção de Pular e Classificação Padrão
- O aluno tem autonomia para pular a prova de proficiência caso deseje iniciar diretamente.
- Ao optar por pular, o aluno é classificado preventivamente como nível **Básico** em todas as áreas da matéria.
- Uma notificação informativa destaca que a prova pode ser feita a qualquer momento para recalibrar a trilha.

#### RN-CAT-003: Algoritmo Adaptativo (Computerized Adaptive Testing - CAT)
- A prova se inicia com uma questão calibrada em dificuldade média ($\theta = 0$).
- A cada acerto, o motor seleciona uma questão com parâmetro de discriminação e dificuldade superior.
- A cada erro, o motor busca uma questão de menor dificuldade para identificar a fronteira exata de domínio do aluno.
- Critério de parada: finalização após **12 a 20 questões** respondidas ou quando o erro padrão da estimativa de proficiência for menor que o limiar pré-definido ($\text{SE}(\theta) \le 0.30$).

#### RN-CAT-003.1: Prova Oculta com Feedback Apenas no Final (Blind Adaptive Testing)
- **Zero Feedback Imediato**: Durante a execução da prova diagnóstica, o estudante não recebe confirmação de acerto ou erro em cada questão e não visualiza o cálculo provisório de seu $\theta$.
- **Redução de Ansiedade**: A interface apresenta apenas o contador ordinal neutro `Questão X (Progresso: 12 a 20 questões)`.
- **Revelação Diagnóstica**: Os resultados detalhados, o escore $\theta$ oficial de entrada e a plotagem do Gráfico Radar são revelados exclusivamente na tela de conclusão do teste.

---

### 2.2 Estrutura de Níveis e Áreas

#### RN-CAT-004: Escala de 3 Níveis de Proficiência
O resultado de domínio do aluno é categorizado em 3 patamares didáticos:

| Nível | Código | Faixa de Domínio ($\theta$) | Descrição Pedagógica |
|:---|:---|:---|:---|
| **Básico** | `basic` | 0% a 33% | Requer consolidação de conceitos fundamentais e pré-requisitos |
| **Intermediário** | `intermediate` | 34% a 66% | Compreende os conceitos centrais, necessita de aprofundamento prático |
| **Avançado** | `advanced` | 67% a 100% | Domínio pleno dos tópicos, apto a exercícios complexos e desafios |

#### RN-CAT-005: Granularidade por Área/Tópico
A classificação de proficiência não é global, mas sim **independente por área temática**:

```
Matemática (2º Grau):
├── Álgebra e Funções                     → [ Básico | Intermediário | Avançado ]
├── Geometria e Trigonometria             → [ Básico | Intermediário | Avançado ]
├── Álgebra Linear e Sequências           → [ Básico | Intermediário | Avançado ]
└── Matemática Aplicada e Estatística     → [ Básico | Intermediário | Avançado ]
```

---

### 2.3 Formato de Questões e Avaliação

#### RN-CAT-006: Tipos de Questão e Regras de Correção
O banco de itens do teste adaptativo suporta múltiplos formatos de entrada:

| Tipo | Identificador | Regra de Correção | Escopo de Aplicação |
|:---|:---|:---|:---|
| **Múltipla Escolha** | `multiple_choice` | Comparação binária com o gabarito oficial | Universal (todas as matérias) |
| **Entrada Numérica** | `numeric_input` | Avaliação de valor exato com tolerância configurada ($\pm 0.01$) | Exatas (Matemática, Física, Química) |
| **Entrada de Texto** | `text_input` | Avaliação semântica assistida por IA (futuro) | Humanas e Linguagens (Português, História) |

---

### 2.4 Políticas de Retentativa e Conclusão

#### RN-CAT-007: Política de Cooldown para Retentativa
- O aluno pode refazer o diagnóstico de qualquer matéria para atualizar sua classificação.
- É aplicado um **cooldown obrigatório de 7 dias corridos** entre tentativas da mesma disciplina para garantir tempo hábil de estudo.
- O nível ativo refletido na plataforma corresponde sempre à **tentativa mais recente**.
- Todo o histórico de pontuações e evoluções temporais é preservado para consulta analítica.

#### RN-CAT-008: Apresentação Visual dos Resultados
Ao encerrar o teste, a tela exibe:
- **Gráfico Radar Multiaxial** mostrando o nível em cada uma das áreas temáticas.
- **Parecer Diagnóstico Resumido** com feedbacks motivacionais e prioridades de estudo.
- **Botão de Ação Primária**: "Ir para minha trilha personalizada".

#### RN-CAT-009: Transição e Conclusão do Onboarding
- O acionamento da conclusão direciona o estudante diretamente ao **Dashboard da Matéria**.
- O status do usuário é atualizado para `onboarding_completed: true`.
- As trilhas de aprendizagem são organizadas e ordenadas dando prioridade às áreas classificadas com nível inferior.

