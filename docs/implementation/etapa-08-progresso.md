---
title: "Etapa 8: Progresso e Analytics"
type: "implementation"
status: "planned"
related: ["etapa-07-exercicios.md"]
last_updated: "2026-09-06"
---
<!-- ai-summary: Implementação do dashboard de progresso, heatmap de domínio, histórico theta, gerador de PDF vetorial com ReportLab e controle de horas de estudo. -->

# Etapa 8: Progresso e Analytics

**Duração estimada:** 1 semana
**Pré-requisito:** Etapa 7 concluída (Exercícios e CAT)
**Entregável:** Dashboard de progresso completo com gráficos interativos e download de Boletim PDF.

Esta etapa foca na consolidação dos dados de aprendizado gerados durante a interação do aluno (exercícios e CAT). Vamos estruturar tabelas de analytics avançado, criar a inteligência de micro-ajuste estocástico de proficiência (theta) e construir um dashboard completo de acompanhamento.

> [!IMPORTANT]
> A precisão dos dados salvos no heatmap afetará as recomendações do motor pedagógico no futuro. A performance de agregação é crucial para evitar o problema de N+1 queries.

---

## 8.1. Migração Alembic: Tabelas de Progresso

Primeiro, criaremos os modelos para estruturar os dados de proficiência e domínio de capítulos. Crie o arquivo `backend/app/models/progress.py`.

```python
# backend/app/models/progress.py
import uuid
from datetime import date, datetime
from typing import Literal
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class HeatmapDominio(Base):
    __tablename__ = "heatmap_dominio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    capitulo_id = Column(UUID(as_uuid=True), ForeignKey("capitulos.id", ondelete="CASCADE"), nullable=False)
    taxa_acertos_ponderada = Column(Numeric(5, 2), nullable=False, default=0.0) # 0.00 a 100.00
    status_cor = Column(String, nullable=False, default="cinza") # cinza, vermelho, amarelo, verde
    aula_concluida = Column(Boolean, nullable=False, default=False)
    total_questoes_respondidas = Column(Integer, nullable=False, default=0)
    ultima_interacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("usuario_id", "capitulo_id", name="uq_heatmap_usuario_capitulo"),
    )

class HistoricoTheta(Base):
    __tablename__ = "historico_theta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    disciplina_id = Column(UUID(as_uuid=True), ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False)
    volume_id = Column(UUID(as_uuid=True), ForeignKey("volumes_didaticos.id", ondelete="SET NULL"), nullable=True)
    grande_area = Column(String, nullable=False) # 'algebra_funcoes' | 'geometria' | 'algebra_linear' | 'aplicada'
    theta_estimado = Column(Numeric(5, 3), nullable=False) # -3.000 a +3.000
    erro_padrao_se = Column(Numeric(5, 3), nullable=False)
    origem_ajuste = Column(String, nullable=False) # 'onboarding_cat' | 'marco_cat' | 'micro_ajuste_exercicio'
    registrado_em = Column(DateTime(timezone=True), server_default=func.now())

class HorasEstudoDiarias(Base):
    __tablename__ = "horas_estudo_diarias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    data = Column(Date, nullable=False, default=date.today)
    minutos_ativos = Column(Integer, nullable=False, default=0)
    ultima_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("usuario_id", "data", name="uq_horas_usuario_data"),
    )
```

Gere a migração executando no Windows PowerShell:

```powershell
cd backend
alembic revision --autogenerate -m "004_progress_tables"
alembic upgrade head
```

> [!WARNING]
> Verifique se o módulo `app.models.progress` foi importado no arquivo `backend/app/db/base.py` antes de rodar o comando `--autogenerate`.

---

## 8.2. Backend: Micro-Ajuste do Theta e Heatmap Service

### `theta_updater.py`

Crie uma rotina para micro-ajustar a proficiência após exercícios.

```python
# backend/app/services/theta_updater.py
from decimal import Decimal
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.progress import HistoricoTheta, HeatmapDominio

async def atualizar_heatmap(
    db: AsyncSession, usuario_id: str, capitulo_id: str,
    acerto: bool, dificuldade_questao: float
):
    """
    Atualiza o domínio no formato upsert, reclassificando a cor sem gerar N+1.
    """
    # Lógica de upsert e recálculo da taxa ponderada seria aqui.
    # Fórmula:
    # Vermelho: < 40%
    # Amarelo: 40% a 79%
    # Verde: >= 80% (com aula_concluida = True)
    # Cinza: 0 tentativas
    pass

async def micro_ajuste_theta(
    db: AsyncSession, usuario_id: str, disciplina_id: str,
    grande_area: str, acerto: bool, dificuldade: float, theta_atual: float
):
    """
    Aplica micro-ajuste estocástico após baterias.
    """
    # Ajuste simples baseado na diferença (theta - dificuldade)
    pass
```

### `heatmap_service.py`

Responsável por listar os pontos críticos (top 3):

```python
# backend/app/services/heatmap_service.py
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.progress import HeatmapDominio

async def get_top_criticos(db: AsyncSession, usuario_id: str, limit: int = 3):
    """
    Lista os tópicos com pior taxa de acerto ponderada (excluindo os cinzas).
    """
    stmt = (
        select(HeatmapDominio)
        .where(HeatmapDominio.usuario_id == usuario_id)
        .where(HeatmapDominio.status_cor == 'vermelho')
        .order_by(asc(HeatmapDominio.taxa_acertos_ponderada))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
```

---

## 8.3. Backend: Gerador de Boletim PDF (ReportLab)

Para gerar relatórios institucionais com qualidade vetorial, usaremos o `reportlab`.

> [!TIP]
> Não esqueça de instalar a dependência: `pip install reportlab`. Adicione ao `requirements.txt`.

```python
# backend/app/services/pdf_generator.py
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

async def gerar_boletim_pdf(usuario_dados: dict, estatisticas: dict) -> io.BytesIO:
    """
    Gera PDF de alta resolução com cabeçalho institucional, máscara de CPF e métricas.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Tutor Inteligente - Boletim de Proficiência")
    
    # Dados do Aluno (CPF mascarado)
    cpf_mask = f"***.{usuario_dados['cpf'][3:6]}.{usuario_dados['cpf'][6:9]}-**"
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Aluno: {usuario_dados['nome']}")
    c.drawString(50, 755, f"CPF: {cpf_mask}")
    
    # Adicionar gráficos/radar (geralmente gerados como imagem PNG via Matplotlib ou similar e embutidos, ou desenhados via paths)
    c.drawString(50, 700, f"Horas Totais: {estatisticas['horas_totais']}h")
    c.drawString(50, 680, f"Aulas Concluídas: {estatisticas['aulas_concluidas']}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer
```

---

## 8.4. Backend: Endpoints de Progresso

No arquivo `backend/app/api/v1/endpoints/progresso.py`:

```python
# backend/app/api/v1/endpoints/progresso.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.api import deps
from app.models.progress import HorasEstudoDiarias
from app.services import pdf_generator

router = APIRouter()

@router.get("/geral")
async def get_indicadores_gerais(db: AsyncSession = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    # Retornar theta, radar e streak
    return {"theta_global": 1.5, "streak_dias": 5}

@router.get("/heatmap/{volume_id}")
async def get_heatmap_volume(volume_id: str, db: AsyncSession = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    return []

@router.get("/top-criticos")
async def get_top_criticos(db: AsyncSession = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    return []

@router.get("/boletim-pdf")
async def download_boletim(db: AsyncSession = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    buffer = await pdf_generator.gerar_boletim_pdf(
        {"nome": current_user.nome, "cpf": current_user.cpf},
        {"horas_totais": 12, "aulas_concluidas": 4}
    )
    return StreamingResponse(
        buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=boletim.pdf"}
    )

@router.post("/tempo-estudo")
async def registrar_tempo(minutos: int, db: AsyncSession = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    stmt = insert(HorasEstudoDiarias).values(
        usuario_id=current_user.id,
        minutos_ativos=minutos
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['usuario_id', 'data'],
        set_=dict(minutos_ativos=HorasEstudoDiarias.minutos_ativos + minutos)
    )
    await db.execute(stmt)
    await db.commit()
    return {"status": "ok"}
```

---

## 8.5. Frontend: Dashboard de Progresso

### Hook `useStudyTimer`

Responsável por cronometrar a atividade e pausar após inatividade.

```typescript
// frontend/src/hooks/useStudyTimer.ts
import { useEffect, useRef, useState } from 'react';

export function useStudyTimer() {
  const [isActive, setIsActive] = useState(true);
  const timeoutRef = useRef<NodeJS.Timeout>();
  
  useEffect(() => {
    const handleActivity = () => {
      setIsActive(true);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => setIsActive(false), 3 * 60 * 1000); // 3 min inativo
    };

    window.addEventListener('mousemove', handleActivity);
    window.addEventListener('keydown', handleActivity);
    
    // Timer para bater no endpoint a cada X minutos...
    
    return () => {
      window.removeEventListener('mousemove', handleActivity);
      window.removeEventListener('keydown', handleActivity);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return { isActive };
}
```

### Gráficos com Recharts

Crie o arquivo `frontend/src/app/(student)/progresso/page.tsx` para agrupar os componentes:
- **`RadarChart`**: Plote os 4 eixos (`Álgebra e Funções`, `Geometria`, `Álgebra Linear`, `Matemática Aplicada`).
- **`HeatmapMatrix`**: Um grid iterando pelos capítulos. Cada quadrado recebe uma classe Tailwind baseada na cor (ex: `bg-red-500`, `bg-green-500`).
- **`TimelineTheta`**: Gráfico de linha mostrando a evolução do `theta_estimado`.

---

## 8.6. Critérios de Aceitação

- [ ] Modelos `HeatmapDominio`, `HistoricoTheta` e `HorasEstudoDiarias` criados e migrados com Alembic sem erros.
- [ ] A cor do heatmap transita corretamente pelas 4 fases (cinza, vermelho, amarelo, verde) baseada na fórmula de taxa ponderada.
- [ ] O endpoint `POST /api/v1/progresso/tempo-estudo` utiliza UPSERT (`ON CONFLICT DO UPDATE`) para somar minutos do dia.
- [ ] O Boletim PDF é gerado corretamente utilizando vetores e faz streaming para o navegador via rota `GET`.
- [ ] A página `/progresso` exibe corretamente os três gráficos (`RadarChart`, heatmap e timeline) sem erros de hidratação.
- [ ] O hook `useStudyTimer` no frontend pausa após 3 minutos cravados de ausência de mouse/teclado.
- [ ] Testes de API desenvolvidos com `pytest-asyncio` confirmam atualização de minutos e status do heatmap.
