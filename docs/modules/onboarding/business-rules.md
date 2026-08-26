---
title: Onboarding - Regras de Negócio
type: module
status: draft
related:
  - modules/onboarding/index.md
  - modules/onboarding/flow.md
  - modules/autenticacao/index.md
last_updated: "2026-08-26"
updated_by: claude
---

<!-- ai-summary
Regras de negócio do módulo Onboarding. Validações de campos, lógica do responsável (menor de 18), regras do CAT adaptativo,
política de cooldown (7 dias), classificação por nível (Básico, Intermediário, Avançado), escalabilidade do modelo hierárquico.
-->

# Onboarding — Regras de Negócio

## RN-ONB-001: Validação de Campos Obrigatórios

Todos os campos marcados como obrigatórios devem ser preenchidos para avançar para a próxima etapa do wizard. A validação é feita **por etapa** — o aluno não avança sem preencher todos os campos da etapa atual.

## RN-ONB-002: Validação de CPF

- O CPF deve ser validado com algoritmo de dígitos verificadores
- CPFs inválidos ou já cadastrados na plataforma são rejeitados
- Aplica-se tanto ao CPF do aluno quanto ao CPF do responsável

## RN-ONB-003: Validação de E-mail

- O e-mail deve ter formato válido
- E-mails já cadastrados são rejeitados
- Confirmação por e-mail é enviada após o cadastro (não bloqueia o onboarding)

## RN-ONB-004: Validação de Data de Nascimento

- A data deve ser válida e no passado
- A idade mínima não é restrita (a plataforma é acessível a qualquer idade)
- A idade é calculada automaticamente para determinar a exigência de responsável

## RN-ONB-005: Dados do Responsável (Condicional)

- Se a **idade do aluno < 18 anos** na data do cadastro, os campos de responsável são **obrigatórios**:
    - Nome do responsável
    - CPF do responsável (validado)
    - Telefone do responsável
- Se a **idade ≥ 18 anos**, os campos de responsável **não são exibidos**
- A idade é calculada com base na `data_nascimento` informada na Etapa 1

## RN-ONB-006: Auto-preenchimento por CEP

- Ao preencher o CEP, o sistema consulta uma API de CEP (ex: ViaCEP) e auto-preenche:
    - Estado
    - Cidade
    - Bairro
- O aluno pode editar os valores auto-preenchidos se necessário
- Se o CEP não for encontrado, os campos ficam editáveis manualmente

## RN-ONB-007: Foto de Perfil

- A foto de perfil é **opcional**
- Formatos aceitos: JPEG, PNG
- Tamanho máximo: 5 MB
- Se não enviada, um avatar padrão é atribuído (iniciais do nome)

## RN-ONB-008: Instituição de Ensino

- Campo de texto com **autocomplete** a partir de uma base de instituições
- O aluno pode digitar uma instituição não listada (cadastro livre)
- A base de instituições pode ser alimentada via integração com dados do INEP/MEC (futuro)

## RN-ONB-009: Série/Ano

- Campo select com opções dinâmicas baseadas no nível de ensino
- Para Ensino Médio: 1º ano, 2º ano, 3º ano
- Escalável: ao adicionar novos níveis de ensino, as opções se expandem automaticamente

---

## Prova de Proficiência

### RN-PRF-001: Gatilho da Prova

- A prova é sugerida **ao entrar numa matéria pela primeira vez**
- No onboarding, como só existe Matemática, o aluno é direcionado automaticamente à prova
- Para matérias futuras, a sugestão aparece ao clicar na matéria pela primeira vez

### RN-PRF-002: Pular Prova

- O aluno pode **pular** a prova de proficiência
- Ao pular, é classificado como **Básico** em **todas as áreas** da matéria
- Pode fazer a prova posteriormente (acessando pelo perfil ou dashboard da matéria)

### RN-PRF-003: Algoritmo CAT (Computerized Adaptive Testing)

- A prova inicia com uma questão de **dificuldade média**
- Acertou → próxima questão de **nível mais alto**
- Errou → próxima questão de **nível mais baixo**
- O algoritmo converge para o nível real do aluno em **~15-20 questões**
- Cada questão tem um parâmetro de dificuldade pré-calibrado

### RN-PRF-004: Níveis de Proficiência

| Nível | Código | Faixa de Score |
|-------|--------|----------------|
| Básico | `basic` | 0% - 33% |
| Intermediário | `intermediate` | 34% - 66% |
| Avançado | `advanced` | 67% - 100% |

- O nível é calculado **por área/tópico** dentro de cada matéria
- O score é um valor interno calculado pelo algoritmo CAT
- O aluno vê apenas o nível (Básico/Intermediário/Avançado), não o score numérico

### RN-PRF-005: Granularidade por Área

Cada matéria é dividida em áreas/tópicos. O nível é calculado independentemente para cada área:

```
Matemática (Ensino Médio):
├── Álgebra: [Básico | Intermediário | Avançado]
├── Geometria: [Básico | Intermediário | Avançado]
├── Trigonometria: [Básico | Intermediário | Avançado]
└── Estatística: [Básico | Intermediário | Avançado]
```

### RN-PRF-006: Tipos de Questão Suportados

| Tipo | Código | Correção |
|------|--------|----------|
| Múltipla escolha | `multiple_choice` | Automática — compara com resposta correta |
| Resposta numérica | `numeric_input` | Automática — compara valor numérico (com tolerância) |
| Resposta textual | `text_input` | Futuro — avaliação por IA |

- Cada questão define seu tipo
- O CAT funciona com qualquer tipo (avalia certo/errado)
- `numeric_input`: tolerância de ±0.01 para arredondamentos

### RN-PRF-007: Política de Refazer

- O aluno pode refazer a prova de proficiência de qualquer matéria
- **Cooldown mínimo: 7 dias** entre tentativas da mesma matéria
- Se tentar antes de 7 dias → exibe mensagem com a data em que poderá refazer
- O **nível ativo** é sempre o da **última tentativa**
- O **histórico de todas as tentativas** é salvo para acompanhar evolução

### RN-PRF-008: Resultado da Prova

Após completar a prova, o sistema exibe:

1. **Gráfico radar** — mostra visualmente o nível por área
2. **Resumo textual** — mensagem motivacional com pontos fortes e áreas para melhorar
3. **CTA (Call to Action)** — botão "Ir para minha trilha personalizada"
4. **Opção de refazer** — visível, mas com indicação do cooldown

### RN-PRF-009: Pós-Prova

- Ao clicar em "Ir para minha trilha", o aluno é levado ao **dashboard da matéria**
- O dashboard mostra as trilhas por área organizadas pelo nível do aluno
- O onboarding é marcado como **concluído** no perfil do aluno
- Uma tela de **boas-vindas/tutorial rápido** pode aparecer antes do dashboard

---

## Escalabilidade

### RN-ESC-001: Modelo Hierárquico

O sistema segue a hierarquia: **Nível de Ensino → Matéria → Área/Tópico**

- Cada entidade é genérica e independente
- Adicionar uma nova matéria = criar registro de Matéria + Áreas + Questões
- Adicionar um novo nível de ensino = criar registro de Nível + Matérias + Áreas + Questões

### RN-ESC-002: Acesso Livre

- O aluno tem **acesso livre a todas as matérias e níveis** disponíveis
- Não precisa selecionar matérias no cadastro
- A prova de proficiência é acionada ao entrar na matéria (RN-PRF-001)

### RN-ESC-003: Série/Ano Dinâmico

- O campo série/ano no cadastro é dinâmico
- As opções mudam conforme o nível de ensino
- A plataforma deve suportar: Ensino Básico, Fundamental, Médio, Superior, Mestrado (futuro)
