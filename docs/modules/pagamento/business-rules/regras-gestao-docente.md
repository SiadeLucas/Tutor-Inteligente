---
title: Pagamento - 4. Gestão Comercial
type: module
status: draft
related:
  - modules/pagamento/business-rules/index.md
last_updated: "2026-09-02"
updated_by: claude
---

# 4. Integração com o Painel do Professor

### 4.1 Métricas Comerciais e Controle de Acessos

#### RN-PAG-016: Desdobramento de Receita por Categoria
- O Painel do Professor deve apresentar a segmentação exata da receita entre:
  1. Micro-compras de Capítulos de 50 min.
  2. Vendas de Volumes Completos do Iezzi.
  3. Receita Recorrente de Assinaturas (MRR).

#### RN-PAG-017: Termômetro Pedagógico de Vendas
- O painel exibe o ranking dos capítulos e volumes mais comprados, servindo como indicador pedagógico para o professor identificar quais tópicos demandam mais reforço na turma.

#### RN-PAG-018: Controle Granular de Acessos na Ficha do Aluno
- A ficha individual de cada estudante lista todos os capítulos e volumes desbloqueados, com data de início e término da vigência de 12 meses.

#### RN-PAG-019: Proibição de Liberação Manual (Acesso 100% Pago e Automatizado)
- O sistema veda expressamente qualquer concessão manual de acessos, cortesias ou bolsas gratuitas por parte do professor.
- Todo e qualquer desbloqueio de capítulo (50 min), volume ou assinatura ocorre exclusivamente de forma automática mediante compensação financeira aprovada pelo gateway de pagamento (webhook de PIX ou aprovação do cartão).

#### RN-PAG-020: Extrato de Transações e Métricas de Conversão
- Exibição de extrato auditável com identificação do aluno, valor líquido, taxas do gateway e meio utilizado (PIX vs Cartão).
