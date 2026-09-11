"""006_payment_tables

Revision ID: c6faafb7d266
Revises: e5f617a89b02
Create Date: 2026-09-11 14:56:56.966914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c6faafb7d266'
down_revision: Union[str, None] = 'e5f617a89b02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'matriculas_pagamentos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('usuario_id', sa.UUID(), nullable=False),
        sa.Column('tipo_produto', sa.String(length=30), nullable=False),
        sa.Column('referencia_produto_id', sa.UUID(), nullable=True),
        sa.Column('data_inicio', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('data_expiracao', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('valor_pago', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('metodo_pagamento', sa.String(length=20), nullable=False),
        sa.Column('transacao_gateway_id', sa.String(length=100), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_matriculas_produto', 'matriculas_pagamentos', ['tipo_produto', 'referencia_produto_id'], unique=False)
    op.create_index('idx_matriculas_usuario_status', 'matriculas_pagamentos', ['usuario_id', 'status'], unique=False)
    op.create_index(op.f('ix_matriculas_pagamentos_usuario_id'), 'matriculas_pagamentos', ['usuario_id'], unique=False)

    op.create_table(
        'transacoes_financeiras',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('matricula_id', sa.UUID(), nullable=True),
        sa.Column('usuario_id', sa.UUID(), nullable=False),
        sa.Column('gateway_transacao_id', sa.String(length=100), nullable=False),
        sa.Column('valor_bruto', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('taxa_gateway', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('valor_liquido', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('status_transacao', sa.String(length=30), nullable=False),
        sa.Column('metodo', sa.String(length=20), nullable=False),
        sa.Column('gateway_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('pago_em', sa.DateTime(timezone=True), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['matricula_id'], ['matriculas_pagamentos.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_transacoes_data', 'transacoes_financeiras', ['criado_em'], unique=False)
    op.create_index(op.f('ix_transacoes_financeiras_gateway_transacao_id'), 'transacoes_financeiras', ['gateway_transacao_id'], unique=True)
    op.create_index(op.f('ix_transacoes_financeiras_status_transacao'), 'transacoes_financeiras', ['status_transacao'], unique=False)
    op.create_index(op.f('ix_transacoes_financeiras_usuario_id'), 'transacoes_financeiras', ['usuario_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_transacoes_financeiras_usuario_id'), table_name='transacoes_financeiras')
    op.drop_index(op.f('ix_transacoes_financeiras_status_transacao'), table_name='transacoes_financeiras')
    op.drop_index(op.f('ix_transacoes_financeiras_gateway_transacao_id'), table_name='transacoes_financeiras')
    op.drop_index('idx_transacoes_data', table_name='transacoes_financeiras')
    op.drop_table('transacoes_financeiras')

    op.drop_index(op.f('ix_matriculas_pagamentos_usuario_id'), table_name='matriculas_pagamentos')
    op.drop_index('idx_matriculas_usuario_status', table_name='matriculas_pagamentos')
    op.drop_index('idx_matriculas_produto', table_name='matriculas_pagamentos')
    op.drop_table('matriculas_pagamentos')
