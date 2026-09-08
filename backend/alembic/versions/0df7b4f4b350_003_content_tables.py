"""003_content_tables

Revision ID: 0df7b4f4b350
Revises: f3a9c1d24b57
Create Date: 2026-09-07 21:48:23.755427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '0df7b4f4b350'
down_revision: Union[str, None] = 'f3a9c1d24b57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Ativação da extensão oficial de vetores (pgvector)
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')

    # 2. Tabela disciplinas (Tabela 06)
    op.create_table('disciplinas',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('nivel_ensino', sa.String(length=50), nullable=False),
        sa.Column('icone', sa.String(length=50), nullable=False, server_default='school'),
        sa.Column('cor_tema', sa.String(length=20), nullable=False, server_default='#F57C00'),
        sa.Column('ordem', sa.Integer(), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_disciplinas_slug'), 'disciplinas', ['slug'], unique=True)

    # 3. Tabela volumes_didaticos (Tabela 07)
    op.create_table('volumes_didaticos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('disciplina_id', sa.UUID(), nullable=False),
        sa.Column('nome_colecao', sa.String(length=150), nullable=False),
        sa.Column('numero_volume', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=150), nullable=False),
        sa.Column('grande_area', sa.String(length=50), nullable=False),
        sa.Column('ordem_exibicao', sa.Integer(), nullable=False),
        sa.Column('preco_padrao', sa.Numeric(precision=10, scale=2), nullable=False, server_default='49.90'),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['disciplina_id'], ['disciplinas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('disciplina_id', 'numero_volume', name='uk_volume_disciplina_numero')
    )
    op.create_index('idx_volumes_disciplina', 'volumes_didaticos', ['disciplina_id', 'ordem_exibicao'], unique=False)
    op.create_index(op.f('ix_volumes_didaticos_disciplina_id'), 'volumes_didaticos', ['disciplina_id'], unique=False)

    # 4. Tabela capitulos (Tabela 08)
    op.create_table('capitulos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('volume_id', sa.UUID(), nullable=False),
        sa.Column('numero_capitulo', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('tempo_estimado_min', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('preco_avulso', sa.Numeric(precision=10, scale=2), nullable=False, server_default='9.90'),
        sa.Column('pre_requisitos_ids', postgresql.ARRAY(sa.UUID()), nullable=True),
        sa.Column('ordem', sa.Integer(), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['volume_id'], ['volumes_didaticos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_capitulos_volume', 'capitulos', ['volume_id', 'ordem'], unique=False)
    op.create_index(op.f('ix_capitulos_volume_id'), 'capitulos', ['volume_id'], unique=False)

    # 5. Tabela aulas (Tabela 09)
    op.create_table('aulas',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('capitulo_id', sa.UUID(), nullable=False),
        sa.Column('bloco1_teoria_katex', sa.Text(), nullable=False),
        sa.Column('bloco2_exemplos_katex', sa.Text(), nullable=False),
        sa.Column('bloco3_dicas_ia', sa.Text(), nullable=False),
        sa.Column('video_url', sa.Text(), nullable=True),
        sa.Column('publicado', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('atualizado_por', sa.UUID(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['atualizado_por'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['capitulo_id'], ['capitulos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('capitulo_id')
    )

    # 6. Tabela documentos_vetoriais_rag (Tabela 10)
    op.create_table('documentos_vetoriais_rag',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('volume_id', sa.UUID(), nullable=False),
        sa.Column('capitulo_id', sa.UUID(), nullable=True),
        sa.Column('trecho_conteudo', sa.Text(), nullable=False),
        sa.Column('metadados', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['capitulo_id'], ['capitulos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['volume_id'], ['volumes_didaticos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_rag_volume', 'documentos_vetoriais_rag', ['volume_id'], unique=False)
    op.create_index(op.f('ix_documentos_vetoriais_rag_capitulo_id'), 'documentos_vetoriais_rag', ['capitulo_id'], unique=False)
    op.create_index(op.f('ix_documentos_vetoriais_rag_volume_id'), 'documentos_vetoriais_rag', ['volume_id'], unique=False)

    # 7. Índice HNSW com distância cosseno para recuperação sub-5ms
    op.execute("CREATE INDEX IF NOT EXISTS idx_rag_embedding_hnsw ON documentos_vetoriais_rag USING hnsw (embedding vector_cosine_ops);")

    # 8. Tabela heatmap_dominio (Tabela 15) — RN-PRG-012 / RN-CNT-010
    op.create_table('heatmap_dominio',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('usuario_id', sa.UUID(), nullable=False),
        sa.Column('capitulo_id', sa.UUID(), nullable=False),
        sa.Column('total_questoes_respondidas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('taxa_acertos_ponderada', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.00'),
        sa.Column('status_cor', sa.String(length=20), nullable=False, server_default='cinza'),
        sa.Column('aula_concluida', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('ultima_interacao', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['capitulo_id'], ['capitulos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'capitulo_id', name='uk_heatmap_usuario_capitulo')
    )
    op.create_index('idx_heatmap_usuario', 'heatmap_dominio', ['usuario_id'], unique=False)
    op.create_index('idx_heatmap_usuario_cor', 'heatmap_dominio', ['usuario_id', 'status_cor'], unique=False)
    op.create_index(op.f('ix_heatmap_dominio_capitulo_id'), 'heatmap_dominio', ['capitulo_id'], unique=False)

    # 9. Tabela horas_estudo_diarias (Tabela 17) — RN-PRG-003
    op.create_table('horas_estudo_diarias',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('usuario_id', sa.UUID(), nullable=False),
        sa.Column('data_registro', sa.Date(), nullable=False),
        sa.Column('segundos_ativos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('aulas_concluidas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('exercicios_submetidos', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'data_registro', name='uk_horas_usuario_data')
    )
    op.create_index('idx_horas_estudo_usuario', 'horas_estudo_diarias', ['usuario_id', 'data_registro'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_horas_estudo_usuario', table_name='horas_estudo_diarias')
    op.drop_table('horas_estudo_diarias')
    op.drop_index(op.f('ix_heatmap_dominio_capitulo_id'), table_name='heatmap_dominio')
    op.drop_index('idx_heatmap_usuario_cor', table_name='heatmap_dominio')
    op.drop_index('idx_heatmap_usuario', table_name='heatmap_dominio')
    op.drop_table('heatmap_dominio')
    op.execute("DROP INDEX IF EXISTS idx_rag_embedding_hnsw;")
    op.drop_index(op.f('ix_documentos_vetoriais_rag_volume_id'), table_name='documentos_vetoriais_rag')
    op.drop_index(op.f('ix_documentos_vetoriais_rag_capitulo_id'), table_name='documentos_vetoriais_rag')
    op.drop_index('idx_rag_volume', table_name='documentos_vetoriais_rag')
    op.drop_table('documentos_vetoriais_rag')
    op.drop_table('aulas')
    op.drop_index(op.f('ix_capitulos_volume_id'), table_name='capitulos')
    op.drop_index('idx_capitulos_volume', table_name='capitulos')
    op.drop_table('capitulos')
    op.drop_index(op.f('ix_volumes_didaticos_disciplina_id'), table_name='volumes_didaticos')
    op.drop_index('idx_volumes_disciplina', table_name='volumes_didaticos')
    op.drop_table('volumes_didaticos')
    op.drop_index(op.f('ix_disciplinas_slug'), table_name='disciplinas')
    op.drop_table('disciplinas')
