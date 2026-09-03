---
title: Arquitetura de Dados e Ciclo Inter-Módulos
type: knowledge
status: complete
related:
  - knowledge/project-context.md
  - modules/index.md
  - modules/conteudo/index.md
  - modules/exercicios/index.md
  - modules/progresso/index.md
last_updated: "2026-09-02"
updated_by: claude
---

<!-- ai-summary
Arquitetura de dados, modelagem relacional e fluxo de integração inter-módulos da plataforma Tutor Inteligente.
Detalhamento do ciclo fechado da Tríade Pedagógica: Conteúdo (11 Volumes Iezzi) <-> Exercícios (CAT & Questões Gêmeas) <-> Progresso (TRI, Heatmap e Recomendações).
Diagrama de Entidade-Relacionamento (ERD) e ciclo de vida dos dados desde o Onboarding até a consolidação no Painel do Professor.
-->

# Arquitetura de Dados e Integração Inter-Módulos

Documentação técnica do fluxo de dados e relacionamentos entre os 8 módulos da plataforma **Tutor Inteligente**, com foco especial na integração da **Tríade Pedagógica**:

$$\text{Conteúdo (Iezzi \& 11 IAs)} \longleftrightarrow \text{Exercícios (CAT \& Questões Gêmeas)} \longleftrightarrow \text{Progresso (TRI } \theta \text{, Heatmap \& Recomendações)}$$

---

## 1. Diagrama de Entidade-Relacionamento (ERD)

A base de dados centraliza as informações cadastrais do **Onboarding**, os contratos comerciais de **Pagamento** e a trilha de aprendizagem contínua:

```mermaid
erDiagram
    USUARIOS ||--o{ SESSOES_ATIVAS : "mantem (max 1)"
    USUARIOS ||--o{ MATRICULAS_PAGAMENTOS : "adquire"
    USUARIOS ||--o{ TENTATIVAS_EXERCICIOS : "submete"
    USUARIOS ||--o{ CAIXA_REFORCO : "acumula"
    USUARIOS ||--o{ HISTORICO_THETA : "registra"
    USUARIOS ||--o{ HEATMAP_DOMINIO : "possui"
    
    VOLUMES_IEZZI ||--|{ CAPITULOS : "contem"
    CAPITULOS ||--|{ AULAS : "estrutura em 4 blocos"
    AULAS ||--|{ LISTAS_FIXACAO : "possui"
    LISTAS_FIXACAO ||--|{ ITENS_EXERCICIOS : "compoe (3 a 5)"
    
    ITENS_EXERCICIOS ||--o{ QUESTOES_GEMEAS : "gera variacoes SymPy"
    ITENS_EXERCICIOS ||--o{ TENTATIVAS_EXERCICIOS : "avalia"
    ITENS_EXERCICIOS ||--o{ CAIXA_REFORCO : "arquiva erros"

    USUARIOS {
        uuid id PK
        string cpf UK
        string email UK
        string nome_completo
        date data_nascimento
        int idade_anos
        string uf
        string cidade
        string cep
        string instituicao_ensino
        string serie_ano
        string role "student | teacher"
        string nome_responsavel "se menor de 18"
        string cpf_responsavel "se menor de 18"
        string telefone_responsavel "se menor de 18"
    }

    MATRICULAS_PAGAMENTOS {
        uuid id PK
        uuid usuario_id FK
        string tipo_produto "capitulo_50min | volume_iezzi | passe_global"
        uuid referencia_produto_id "id do capitulo ou volume"
        datetime data_inicio
        datetime data_expiracao "data_inicio + 365 dias"
        string status "active | past_due | canceled"
        decimal valor_pago
        string metodo "pix | credit_card"
    }

    HISTORICO_THETA {
        uuid id PK
        uuid usuario_id FK
        int volume_iezzi_id
        decimal theta_estimado "escala -3.0 a +3.0"
        decimal erro_padrao_se
        string origem_calibragem "onboarding_cat | marco_cat | micro_ajuste_exercicio"
        datetime timestamp
    }

    HEATMAP_DOMINIO {
        uuid id PK
        uuid usuario_id FK
        uuid capitulo_id FK
        decimal taxa_acertos_ponderada "0 a 100%"
        string status_cor "cinza | vermelho | amarelo | verde"
        int total_questoes_respondidas
        datetime ultima_atualizacao
    }
```

---

## 2. O Ciclo Fechado da Tríade Pedagógica

A aprendizagem do estudante opera em circuito fechado (*closed-loop learning*):

```mermaid
flowchart TD
    subgraph S1["1. Conteúdo (50 min)"]
        A["Blocos 1, 2 e 3: Teoria KaTeX + Exemplos + Dicas IA"] --> B["Bloco 4: Bateria de Fixação (3 a 5 itens)"]
    end
    
    subgraph S2["2. Exercícios & IA"]
        B --> C{"1ª Tentativa"}
        C -->|Acerto| D["Pontuação 100% (1.0) \n Micro-ajuste pleno no Theta"]
        C -->|Erro| E["2ª Chance + Pista Socrática da IA"]
        E -->|Acerto na 2ª| F["Pontuação 50% (0.5) \n Micro-ajuste atenuado"]
        E -->|Erro Duplo| G["Pontuação 0% (0.0) + Resolução KaTeX \n Envio para Caixa de Reforço"]
        G --> H{"Tentar Questão Gêmea?"}
        H -->|Sim| I["IA gera gêmea via SymPy \n Acerto atenua 50% da perda"]
        H -->|Não| J["Continua a lista"]
    end
    
    subgraph S3["3. Progresso & Heatmap"]
        D --> K["Atualização do Heatmap dos 11 Volumes"]
        F --> K
        I --> K
        G --> K
        K --> L{"Submeteu todos os itens?"}
        L -->|Sim| M["Aula 100% Concluída \n Desbloqueia próximo capítulo na Skill Tree"]
        K --> N["Radar dos 3 Tópicos Críticos \n (Menor taxa de acerto ponderada)"]
    end
    
    subgraph S4["4. Loop de Recomendação"]
        N --> O["Hub de Ação na Tela de Progresso"]
        O -->|Revisar Teoria| A
        O -->|Praticar Reforço| P["Bateria Dinâmica de 5 Questões \n (Caixa de Reforço + Gêmeas)"]
        P --> S2
    end
```

---

## 3. Regras Matemáticas de Integração Inter-Módulos

### 3.1 Ponderação da Taxa de Acertos do Capítulo
Para cada questão da bateria de fixação:

$$\text{Score}(q) = \begin{cases} 
1.0, & \text{se acertada na 1ª tentativa} \\ 
0.5, & \text{se acertada na 2ª tentativa (com auxílio de dica)} \\ 
0.0, & \text{se errada nas 2 tentativas} 
\end{cases}$$

A taxa ponderada de maestria do capítulo no Heatmap é dada por:

$$\text{Taxa Ponderada} (\%) = \left( \frac{\sum_{q=1}^{N} \text{Score}(q)}{N} \right) \times 100$$

### 3.2 Thresholds de Cores do Heatmap
- **Cinza (Neutro)**: $N < 3$ questões respondidas no capítulo.
- **Vermelho (Crítico)**: $N \ge 3$ e $\text{Taxa Ponderada} < 50\%$.
- **Amarelo (Em Desenvolvimento)**: $N \ge 3$ e $50\% \le \text{Taxa Ponderada} < 75\%$.
- **Verde (Consolidado)**: $N \ge 3$ e $\text{Taxa Ponderada} \ge 75\%$.

---

## 4. Integração com o Painel do Professor

Todos os eventos gerados pela Tríade Pedagógica são consumidos pelo **Painel do Professor**:
- **Filtro Demográfico**: Cruza a Taxa Ponderada com a Rede de Ensino (Pública vs Privada) e Região/UF do Onboarding.
- **Dossiê Individual**: O professor abre a Ficha do Aluno e inspeciona em quais capítulos o estudante solicitou mais Questões Gêmeas e quais estão arquivados na Caixa de Reforço.
- **Intervenção Docente**: O professor pode emitir uma lista extra de reforço com 1 clique diretamente para o aluno com dificuldades.

---

## 5. Arquitetura de Sessões, Segurança e Roteamento

A segurança de acesso e a proteção de rotas operam com validação distribuída em camadas:

```mermaid
flowchart TD
    subgraph Cliente["Navegador do Aluno"]
        Req["Requisição de API"] --> Interceptor["HTTP Interceptor"]
        Interceptor -->|Token a 2 min de expirar| RefreshCall["POST /auth/refresh silencioso"]
        Interceptor -->|Token válido| Dispatch["Header Authorization: Bearer"]
    end
    
    subgraph Servidor["Middleware de Autenticação"]
        Dispatch --> AuthCheck{"Token Válido & Session ID Ativo?"}
        AuthCheck -->|Sim| RoleCheck{"Verifica Permissão (Role)"}
        AuthCheck -->|Sessão invalidada por 2º aparelho| Freeze["Erro 401: Dispara Modal de Congelamento com Salvamento"]
        
        RoleCheck -->|"Rota /teacher/* acessada por 'student'"| Redirect["Log de Segurança + Redireciona para /dashboard com Toast"]
        RoleCheck -->|Permitido| Endpoint["Processa requisição e retorna dados"]
    end
```
