---
title: Autenticação - Gestão de Sessão Única e Heartbeat
type: module
status: draft
related:
  - modules/autenticacao/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 2. Gestão de Sessão Única e Desconexão Concorrente

Implementação executável da regra de **1 dispositivo concorrente por aluno**, revogação atômica no servidor e verificação de heartbeat.

---

## Código Fonte (`backend/app/modules/auth/session_service.py`)

```python
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_

from app.models.user import SessaoAtiva, Usuario


class SessionManager:
    """Gerenciador de sessões ativas e política de concorrência."""

    @staticmethod
    async def registrar_nova_sessao(
        db: AsyncSession,
        usuario_id: UUID,
        ip_address: str,
        user_agent: str,
        refresh_token_hash: str
    ) -> SessaoAtiva:
        """
        Invalida atomicamente qualquer sessão ativa anterior do estudante
        e instancia a nova sessão como a única autorizada.
        """
        # 1. Revoga todas as sessões anteriores do usuário que ainda estejam abertas
        stmt_revogar = (
            update(SessaoAtiva)
            .where(
                and_(
                    SessaoAtiva.usuario_id == usuario_id,
                    SessaoAtiva.revogado == False
                )
            )
            .values(revogado=True)
        )
        await db.execute(stmt_revogar)

        # 2. Cria a nova sessão ativa
        nova_sessao = SessaoAtiva(
            id=uuid4(),
            usuario_id=usuario_id,
            session_token=str(uuid4()),
            refresh_token_hash=refresh_token_hash,
            ip_address=ip_address,
            user_agent=user_agent,
            ultimo_heartbeat=datetime.utcnow(),
            revogado=False
        )
        db.add(nova_sessao)
        await db.commit()
        await db.refresh(nova_sessao)

        return nova_sessao

    @staticmethod
    async def validar_sessao_ativa(
        db: AsyncSession,
        session_id: UUID,
        usuario_id: UUID
    ) -> SessaoAtiva:
        """
        Verifica se a sessão especificada ainda é válida e não foi revogada.
        Se revogada por um novo login, dispara 401 com CONCURRENT_SESSION_REVOKED.
        """
        stmt = select(SessaoAtiva).where(
            and_(
                SessaoAtiva.id == session_id,
                SessaoAtiva.usuario_id == usuario_id
            )
        )
        result = await db.execute(stmt)
        sessao = result.scalar_one_or_none()

        if not sessao or sessao.revogado:
            # Sessão inexistente ou revogada por login concorrente em outro dispositivo
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "detail": "CONCURRENT_SESSION_REVOKED",
                    "mensagem": "Sua conta foi conectada em outro dispositivo. Se não foi você, redefina sua senha imediatamente.",
                    "horario_desconexao": datetime.utcnow().strftime("%H:%M")
                }
            )

        return sessao

    @staticmethod
    async def atualizar_heartbeat(
        db: AsyncSession,
        session_id: UUID
    ) -> None:
        """Atualiza a estampa temporal de atividade a cada 30 segundos."""
        stmt = (
            update(SessaoAtiva)
            .where(SessaoAtiva.id == session_id)
            .values(ultimo_heartbeat=datetime.utcnow())
        )
        await db.execute(stmt)
        await db.commit()
```

---

## Hook de Heartbeat no Frontend (`frontend/src/hooks/useHeartbeat.ts`)

```typescript
import { useEffect } from "react";
import { api } from "@/lib/api";

export function useHeartbeat(onConcurrentSessionRevoked: (data: any) => void) {
  useEffect(() => {
    // Dispara a cada 30 segundos
    const interval = setInterval(async () => {
      try {
        await api.get("/api/v1/auth/heartbeat");
      } catch (err: any) {
        if (err.response?.data?.detail === "CONCURRENT_SESSION_REVOKED") {
          // 1. Pausa o cronômetro de estudo
          // 2. Dispara o modal de congelamento na tela
          onConcurrentSessionRevoked(err.response.data);
        }
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [onConcurrentSessionRevoked]);
}
```
