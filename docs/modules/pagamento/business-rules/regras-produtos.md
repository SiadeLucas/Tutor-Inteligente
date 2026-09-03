---
title: Pagamento - 1. Produtos e Preços
type: module
status: draft
related:
  - modules/pagamento/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 1. Estrutura de Produtos e Formato de 50 Minutos

### 1.1 Modalidades de Venda

#### RN-PAG-001: Definição do Capítulo de 50 Minutos
- Cada capítulo dos 11 volumes do Iezzi é comercializado como uma unidade pedagógica autocontida dimensionada para 50 minutos de estudo (10 min teoria + 15 min exemplos + 10 min tutor IA + 15 min fixação).

#### RN-PAG-001.1: Política de Bloqueio Imediato (Zero Degustação)
- A plataforma opera em modelo 100% comercial pago.
- O Onboarding disponibiliza gratuitamente a Prova Adaptativa (CAT) diagnóstica e a emissão do Gráfico Radar de Entrada.
- Concluído o Onboarding, **todos os nós da Skill Tree em todos os 11 volumes iniciam em estado bloqueado (com ícone de cadeado)**, exigindo o pagamento de um capítulo avulso, de um volume ou da assinatura para liberar qualquer conteúdo de aula ou exercício.

#### RN-PAG-002: Venda Avulsa por Volume do Iezzi
- A compra de um volume completo confere desconto em relação à soma dos capítulos individuais e desbloqueia o Agente Especialista de IA correspondente àquele volume.

#### RN-PAG-003: Passe Global Ilimitado
- Assinatura com acesso irrestrito aos 11 volumes da coleção Iezzi, aos 11 Agentes Especialistas e a todas as avaliações e diagnósticos CAT.

#### RN-PAG-004: Precificação Flexível pelo Professor
- Os valores de cada modalidade são configuráveis no painel administrativo pelo professor gestor.

#### RN-PAG-005: Abatimento Integral de Upgrade (Desconto Progressivo por Volume)
- Se o estudante já adquiriu 1 ou mais capítulos avulsos de um volume específico e posteriormente optar por adquirir o Volume Completo, **100% do valor já investido nos capítulos avulsos é automaticamente deduzido** do preço final do volume no checkout:

$$\text{Valor a Pagar pelo Volume} = \max\left(0, \text{Preço do Volume} - \sum \text{Valores Pagos nos Capítulos do Volume}\right)$$

- Ao efetivar o upgrade, a vigência de 12 meses (365 dias) é reiniciada para o volume integral como um todo a partir da data da nova transação.
