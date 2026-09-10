"""005_progress_tables

Revision ID: e5f617a89b02
Revises: de042328f643
Create Date: 2026-09-10 18:00:00.000000

"""
from typing import Sequence, Union
import uuid
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e5f617a89b02'
down_revision: Union[str, None] = 'de042328f643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criação da tabela historico_theta (Tabela 16)
    op.create_table(
        'historico_theta',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('usuario_id', sa.UUID(), nullable=False),
        sa.Column('disciplina_id', sa.UUID(), nullable=False),
        sa.Column('volume_id', sa.UUID(), nullable=True),
        sa.Column('grande_area', sa.String(length=50), nullable=False),
        sa.Column('theta_estimado', sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column('erro_padrao_se', sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column('origem_ajuste', sa.String(length=40), nullable=False),
        sa.Column('registrado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['volume_id'], ['volumes_didaticos.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_historico_theta_usuario_disciplina', 'historico_theta', ['usuario_id', 'disciplina_id', 'registrado_em'], unique=False)
    op.create_index(op.f('ix_historico_theta_disciplina_id'), 'historico_theta', ['disciplina_id'], unique=False)
    op.create_index(op.f('ix_historico_theta_usuario_id'), 'historico_theta', ['usuario_id'], unique=False)
    op.create_index(op.f('ix_historico_theta_volume_id'), 'historico_theta', ['volume_id'], unique=False)

    # 2. Backfill automático: converter provas_cat concluídas em registros de historico_theta
    conn = op.get_bind()
    provas_res = conn.execute(
        sa.text("SELECT id, usuario_id, disciplina_id, theta_geral, erro_padrao_se, scores_grandes_areas, finalizado_em, iniciado_em FROM provas_cat WHERE finalizado_em IS NOT NULL")
    ).fetchall()

    for prova in provas_res:
        p_id, u_id, d_id, theta_geral, se, scores_json, fin_em, ini_em = prova
        reg_time = fin_em or ini_em

        # Registro do theta global
        conn.execute(
            sa.text(
                "INSERT INTO historico_theta (id, usuario_id, disciplina_id, volume_id, grande_area, theta_estimado, erro_padrao_se, origem_ajuste, registrado_em) "
                "VALUES (:id, :u_id, :d_id, NULL, 'geral', :theta, :se, 'onboarding_cat', :reg_time)"
            ),
            {"id": uuid.uuid4(), "u_id": u_id, "d_id": d_id, "theta": theta_geral, "se": se, "reg_time": reg_time}
        )

        # Registros por grande área
        if scores_json:
            scores_dict = scores_json if isinstance(scores_json, dict) else json.loads(scores_json)
            for area, score in scores_dict.items():
                conn.execute(
                    sa.text(
                        "INSERT INTO historico_theta (id, usuario_id, disciplina_id, volume_id, grande_area, theta_estimado, erro_padrao_se, origem_ajuste, registrado_em) "
                        "VALUES (:id, :u_id, :d_id, NULL, :area, :theta, :se, 'onboarding_cat', :reg_time)"
                    ),
                    {"id": uuid.uuid4(), "u_id": u_id, "d_id": d_id, "area": area, "theta": score, "se": se, "reg_time": reg_time}
                )


def downgrade() -> None:
    op.drop_index(op.f('ix_historico_theta_volume_id'), table_name='historico_theta')
    op.drop_index(op.f('ix_historico_theta_usuario_id'), table_name='historico_theta')
    op.drop_index(op.f('ix_historico_theta_disciplina_id'), table_name='historico_theta')
    op.drop_index('idx_historico_theta_usuario_disciplina', table_name='historico_theta')
    op.drop_table('historico_theta')
