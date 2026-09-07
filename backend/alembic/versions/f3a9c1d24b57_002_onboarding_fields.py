"""002_onboarding_fields

Revision ID: f3a9c1d24b57
Revises: 452e8214a3fc
Create Date: 2026-09-07

Alinha a tabela `usuarios` às especificações do módulo Onboarding
(campos gênero, telefone, logradouro e número) e ajusta os índices
ao dicionário de dados oficial (`knowledge/database/01-usuarios.md`
e `02-sessoes-ativas.md`).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a9c1d24b57'
down_revision: Union[str, None] = '452e8214a3fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Novos campos do Onboarding (módulo 4: wizard de 3 etapas) ---
    op.add_column(
        'usuarios',
        sa.Column('genero', sa.String(length=20), nullable=False, server_default='nao_informar')
    )
    op.add_column(
        'usuarios',
        sa.Column('telefone', sa.String(length=15), nullable=False, server_default='')
    )
    op.add_column(
        'usuarios',
        sa.Column('logradouro', sa.String(length=200), nullable=True)
    )
    op.add_column(
        'usuarios',
        sa.Column('numero', sa.String(length=20), nullable=True)
    )

    # --- Índices previstos no dicionário de dados oficial ---
    # Métricas demográficas do Painel do Professor (Etapa 10): filtros por região.
    op.create_index('idx_usuarios_uf_cidade', 'usuarios', ['uf', 'cidade'], unique=False)

    # Índice parcial de sessões ativas (busca sub-1ms apenas de sessões válidas),
    # substituindo o índice integral equivalente.
    op.drop_index('ix_sessoes_ativas_usuario_id', table_name='sessoes_ativas')
    op.create_index(
        'idx_sessoes_ativas_usuario',
        'sessoes_ativas',
        ['usuario_id'],
        unique=False,
        postgresql_where=sa.text('revogado = FALSE')
    )


def downgrade() -> None:
    op.drop_index('idx_sessoes_ativas_usuario', table_name='sessoes_ativas')
    op.create_index(
        op.f('ix_sessoes_ativas_usuario_id'),
        'sessoes_ativas',
        ['usuario_id'],
        unique=False
    )
    op.drop_index('idx_usuarios_uf_cidade', table_name='usuarios')

    op.drop_column('usuarios', 'numero')
    op.drop_column('usuarios', 'logradouro')
    op.drop_column('usuarios', 'telefone')
    op.drop_column('usuarios', 'genero')
