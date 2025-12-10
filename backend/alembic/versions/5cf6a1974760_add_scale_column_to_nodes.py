"""add_scale_column_to_nodes

Revision ID: 5cf6a1974760
Revises: 516074b986c0
Create Date: 2025-11-23 17:38:00.377469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cf6a1974760'
down_revision: Union[str, Sequence[str], None] = '516074b986c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if column exists before adding (for idempotency)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('nodes')]

    if 'scale' not in columns:
        # Add scale column with default value for existing rows
        op.add_column('nodes', sa.Column('scale', sa.Integer(), nullable=True))
        # Update existing rows to have scale=4 (individual level as default)
        op.execute("UPDATE nodes SET scale = 4 WHERE scale IS NULL")

        # SQLite doesn't support ALTER COLUMN or CHECK constraints well
        if conn.dialect.name != 'sqlite':
            # Make column non-nullable after backfilling
            op.alter_column('nodes', 'scale', nullable=False)
            # Add check constraint
            op.create_check_constraint('scale_range', 'nodes', 'scale >= 1 AND scale <= 7')

        # Create index (check if it doesn't exist)
        try:
            op.create_index(op.f('ix_nodes_scale'), 'nodes', ['scale'], unique=False)
        except Exception:
            pass  # Index may already exist


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('nodes')]

    if 'scale' in columns:
        try:
            op.drop_index(op.f('ix_nodes_scale'), table_name='nodes')
        except Exception:
            pass
        if conn.dialect.name != 'sqlite':
            try:
                op.drop_constraint('scale_range', 'nodes', type_='check')
            except Exception:
                pass
        op.drop_column('nodes', 'scale')
