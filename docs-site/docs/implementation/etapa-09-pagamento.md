---
title: "Etapa 9: Pagamento e Checkout"
type: implementation_step
status: completed
related: ["etapa-03-autenticacao"]
last_updated: "2026-09-11"
updated_by: antigravity
---

<!-- ai-summary
Implementação do sistema de pagamento e checkout do Tutor Inteligente utilizando Asaas (PIX e Cartão de Crédito). Inclui configuração do gateway, migrações de banco (matriculas_pagamentos, transacoes_financeiras), lógica de abatimento proporcional (upgrade), webhook idempotente para baixa de pagamentos, endpoints de checkout, e frontend de pagamento in-app com polling de status.
-->

# Etapa 9: Pagamento e Checkout

**Duração:** 1-2 semanas
**Pré-requisito:** Etapa 3 concluída (Autenticação)
**Entregável:** Compra de capítulo avulso via PIX e Cartão com ativação instantânea da matrícula.

Esta etapa aborda a integração com o gateway de pagamentos **Asaas** para habilitar transações financeiras na plataforma, incluindo compra de capítulos avulsos e volumes completos via PIX e Cartão de Crédito.

---

## 9.1 Configuração da Conta Asaas (Sandbox e Produção)

Para iniciar o desenvolvimento, usaremos o ambiente de testes (Sandbox) do Asaas.

> [!IMPORTANT]
> Nunca misture as chaves do Sandbox com as de Produção no seu arquivo `.env`.

1. **Criação da Conta Sandbox**:
   - Acesse [sandbox.asaas.com](https://sandbox.asaas.com/) e crie uma conta.
2. **Obtenção da API Key**:
   - No painel, vá em Configurações > Integrações > Gerar API Key.
3. **Configuração do Webhook**:
   - Na mesma tela de Integrações, ative a opção Webhook.
   - Defina a URL temporária (por exemplo, usando Ngrok: `https://seu-ngrok.app/api/v1/pagamentos/webhook`).
   - Adicione um "Token Secreto" (uma string aleatória forte) para que possamos validar as requisições que chegam ao backend.
4. **Variáveis no `.env`**:

```env
ASAAS_API_KEY=sua_chave_api_do_sandbox
ASAAS_WEBHOOK_SECRET_TOKEN=seu_token_secreto_configurado_no_asaas
ASAAS_ENVIRONMENT=sandbox # ou 'production' no ambiente produtivo
```

---

## 9.2 Migração Alembic: Tabelas Financeiras

Precisamos de duas novas tabelas para gerenciar as matrículas/assinaturas e o registro contábil de transações.

### Models (`backend/app/models/payment.py`)

Crie o arquivo `backend/app/models/payment.py`. Certifique-se de importá-lo no seu `Base` do SQLAlchemy para que o Alembic o reconheça.

```python
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MatriculaPagamento(Base):
    __tablename__ = 'matriculas_pagamentos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    tipo_produto = Column(String(50), nullable=False) # 'capitulo_50min' | 'volume_iezzi' | 'passe_global'
    referencia_produto_id = Column(UUID(as_uuid=True), nullable=True)
    data_inicio = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default='active') # 'active' | 'past_due' | 'canceled'
    valor_pago = Column(Numeric(10, 2), nullable=False)
    metodo_pagamento = Column(String(20)) # 'pix' | 'credit_card'
    transacao_gateway_id = Column(String(100))

    usuario = relationship("Usuario")
    transacoes = relationship("TransacaoFinanceira", back_populates="matricula")

class TransacaoFinanceira(Base):
    __tablename__ = 'transacoes_financeiras'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula_id = Column(UUID(as_uuid=True), ForeignKey('matriculas_pagamentos.id', ondelete='SET NULL'), nullable=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='RESTRICT'), nullable=False)
    gateway_transacao_id = Column(String(100), nullable=False, unique=True)
    valor_bruto = Column(Numeric(10, 2), nullable=False)
    taxa_gateway = Column(Numeric(10, 2), nullable=False)
    valor_liquido = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default='pending') # 'pending' | 'completed' | 'refunded' | 'failed'
    metodo = Column(String(20)) # 'pix' | 'credit_card'
    payload_resposta = Column(JSONB)
    criado_em = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    matricula = relationship("MatriculaPagamento", back_populates="transacoes")
```

### Gerando e executando a migração

No terminal, gere a migração:

```powershell
alembic revision --autogenerate -m "005_payment_tables"
alembic upgrade head
```

> [!NOTE]
> Para calcular `data_expiracao`, assumiremos 365 dias (1 ano) de acesso ao comprar um produto, definindo isso no ato da criação ou via trigger/aplicação.

---

## 9.3 Backend: Upgrade Proporcional e Idempotência de Webhook

### Calculadora de Upgrade (`upgrade_calculator.py`)

A regra de negócios permite abater 100% do valor gasto em capítulos avulsos na compra do volume completo.

```python
# backend/app/services/upgrade_calculator.py
from decimal import Decimal

def calcular_abatimento_volume(usuario_id: str, volume_id: str, valor_volume: Decimal, sessoes_compradas: list) -> dict:
    """
    Soma o valor das matrículas ativas de capítulos do volume_id
    e desconta do valor_volume. Retorna { "valor_final": Decimal, "abatimento": Decimal }
    """
    total_abatimento = sum(sessao.valor_pago for sessao in sessoes_compradas if sessao.status == 'active')
    valor_final = max(Decimal('0.00'), valor_volume - total_abatimento)
    
    return {
        "valor_final": valor_final,
        "abatimento": total_abatimento
    }
```

> [!TIP]
> Se o abatimento for igual ao preço do volume (saldo = 0), a matrícula deve ser ativada na hora, sem chamar a API do Asaas.

### Serviço de Webhook (`webhook_service.py`)

Garante que pagamentos do Asaas ativem os acessos com segurança e evitando transações duplicadas (idempotência).

```python
# backend/app/services/webhook_service.py
import hmac
import secrets
from sqlalchemy.orm import Session
from app.models.payment import TransacaoFinanceira, MatriculaPagamento

def validar_token(token_recebido: str, token_esperado: str) -> bool:
    """Usa compare_digest para evitar ataques de timing na verificação de token do webhook."""
    if not token_recebido or not token_esperado:
        return False
    return secrets.compare_digest(token_recebido.encode(), token_esperado.encode())

def processar_pagamento_webhook(db: Session, payload: dict):
    transacao_id = payload.get('payment', {}).get('id')
    event_type = payload.get('event')

    if not transacao_id or event_type != 'PAYMENT_RECEIVED':
        return
        
    # Idempotência: verifica se a transação já foi processada
    transacao = db.query(TransacaoFinanceira).filter_by(gateway_transacao_id=transacao_id).first()
    if transacao and transacao.status == 'completed':
        return

    # Atualiza ou cria transação, ativa matrícula (+365 dias)
    # Lógica de atualização de status, datas e valores
```

---

## 9.4 Backend: 6 Endpoints de Pagamento

Adicione os seguintes endpoints no roteador de pagamentos (`backend/app/api/v1/endpoints/pagamentos.py`):

1. **`GET /api/v1/pagamentos/calcular-upgrade/{volume_id}`**
   - Retorna o valor de abatimento.
2. **`POST /api/v1/pagamentos/checkout/pix`**
   - Emite PIX com Asaas, gerando payload com QRCode SVG/Base64 e chave copia-e-cola.
   - Configurar expiração da cobrança no gateway (geralmente 15 a 30 minutos).
3. **`POST /api/v1/pagamentos/checkout/cartao`**
   - Recebe token do cartão gerado no frontend (se aplicável) e processa pagamento direto.
4. **`GET /api/v1/pagamentos/status/{cobranca_id}`**
   - Usado para polling no frontend após gerar o PIX.
   - **IDOR Check**: Validar se o `usuario_id` dono da transação é o mesmo de `current_user.id`.
5. **`POST /api/v1/pagamentos/webhook`**
   - Rota sem auth padrão, apenas verificação por cabeçalho `asaas-access-token` usando o segredo salvo.
6. **`GET /api/v1/pagamentos/meus-produtos`**
   - Retorna as matrículas ativas para exibir quais capítulos/volumes o usuário possui, bem como dias restantes.

---

## 9.5 Frontend: Modal e Tela de Checkout In-App

No frontend Next.js 14, devemos oferecer uma experiência fluida para compras in-app. 

### Rota e Modal
- Implemente uma rota `/checkout` ou um **Modal Global de Compra** que surge quando o usuário tenta abrir um capítulo ou volume bloqueado.

### Abas de Pagamento
- **Aba PIX**: 
  - Exibe o QR Code e uma caixa com o texto "Copia e Cola". 
  - Incluir um componente `<ContadorRegressivo minutos={15} />`.
  - Inicia um polling a cada 3 segundos (`setInterval`) batendo no endpoint `/status/{cobranca_id}`.
  - Ao detectar sucesso, exibir uma animação de "Pagamento Confirmado", fechar o modal e redirecionar imediatamente à aula recém-comprada.
- **Aba Cartão**:
  - Formulário contendo Número do Cartão, Nome do Titular, CVV e Validade.
  - Select para opções de parcelamento.

> [!NOTE]
> Se você integrar o Asaas.js (ou tokenização de cartão), não precisará enviar os dados brutos de cartão pelo seu backend, garantindo maior conformidade com PCI-DSS.

---

## 9.6 Testes e Critérios de Aceitação

### Critérios de Aceitação

- [x] A conexão com o Asaas (Sandbox) está validada, emitindo PIX e Cartão de crédito corretamente.
- [x] As tabelas `matriculas_pagamentos` e `transacoes_financeiras` foram criadas através de migração Alembic.
- [x] Quando um usuário compra capítulos avulsos e depois escolhe o volume completo, o valor das compras passadas é abatido integralmente (100%).
- [x] Se o abatimento cobrir todo o preço do volume (R$0,00 a pagar), a matrícula no volume é feita instantaneamente sem ir ao gateway Asaas.
- [x] O Webhook do Asaas é protegido contra falhas de timing usando `secrets.compare_digest`.
- [x] O Webhook do Asaas possui mecanismo de idempotência, não ativando duas vezes o mesmo pagamento.
- [x] O endpoint de polling (`GET /status/{cobranca_id}`) verifica o IDOR (não permite ver status de cobranças de outros usuários).
- [x] O modal de Checkout no Frontend exibe QR code PIX em SVG ou Base64 e possui o botão de copiar a chave PIX.
- [x] A tela PIX faz polling automático e libera o conteúdo magicamente quando pago no app de banco.
- [x] Após a compra bem-sucedida, o usuário ganha 365 dias de acesso ao produto especificado.
