"""Add node hierarchy columns and junction table

Revision ID: add_hierarchy_columns
Revises: 5cf6a1974760
Create Date: 2025-12-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_hierarchy_columns'
down_revision: Union[str, Sequence[str], None] = '5cf6a1974760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(inspector, table_name, column_name):
    """Check if a column exists in a table."""
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns


def _table_exists(inspector, table_name):
    """Check if a table exists."""
    return table_name in inspector.get_table_names()


def _index_exists(inspector, table_name, index_name):
    """Check if an index exists."""
    indexes = inspector.get_indexes(table_name)
    return any(idx['name'] == index_name for idx in indexes)


def upgrade() -> None:
    """Add hierarchy fields to nodes and mechanisms, create junction table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Add hierarchy fields to nodes (scale column already exists from previous migration)
    if not _column_exists(inspector, 'nodes', 'depth'):
        op.add_column('nodes', sa.Column('depth', sa.Integer(), server_default='0', nullable=True))
    if not _column_exists(inspector, 'nodes', 'primary_path'):
        op.add_column('nodes', sa.Column('primary_path', sa.String(), nullable=True))
    if not _column_exists(inspector, 'nodes', 'all_ancestors'):
        op.add_column('nodes', sa.Column('all_ancestors', sa.JSON(), nullable=True))
    if not _column_exists(inspector, 'nodes', 'is_grouping_node'):
        op.add_column('nodes', sa.Column('is_grouping_node', sa.Boolean(), server_default='0', nullable=True))
    if not _column_exists(inspector, 'nodes', 'display_order'):
        op.add_column('nodes', sa.Column('display_order', sa.Integer(), server_default='0', nullable=True))

    # Create indexes for hierarchy fields (scale index already exists from previous migration)
    if not _index_exists(inspector, 'nodes', 'ix_nodes_depth'):
        op.create_index('ix_nodes_depth', 'nodes', ['depth'])
    if not _index_exists(inspector, 'nodes', 'ix_nodes_is_grouping'):
        op.create_index('ix_nodes_is_grouping', 'nodes', ['is_grouping_node'])
    if not _index_exists(inspector, 'nodes', 'ix_nodes_scale_depth'):
        try:
            op.create_index('ix_nodes_scale_depth', 'nodes', ['scale', 'depth'])
        except Exception:
            pass  # May fail if scale column doesn't exist yet
    if not _index_exists(inspector, 'nodes', 'ix_nodes_primary_path'):
        op.create_index('ix_nodes_primary_path', 'nodes', ['primary_path'])

    # Add hierarchy_level column to mechanisms
    if not _column_exists(inspector, 'mechanisms', 'hierarchy_level'):
        op.add_column('mechanisms', sa.Column('hierarchy_level', sa.String(), server_default='leaf', nullable=True))
    if not _index_exists(inspector, 'mechanisms', 'ix_mechanisms_hierarchy_level'):
        op.create_index('ix_mechanisms_hierarchy_level', 'mechanisms', ['hierarchy_level'])

    # Create node_hierarchy junction table for DAG support
    if not _table_exists(inspector, 'node_hierarchy'):
        op.create_table(
            'node_hierarchy',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('parent_node_id', sa.String(), sa.ForeignKey('nodes.id', ondelete='CASCADE'), nullable=False),
            sa.Column('child_node_id', sa.String(), sa.ForeignKey('nodes.id', ondelete='CASCADE'), nullable=False),
            sa.Column('relationship_type', sa.String(), server_default='contains', nullable=True),
            sa.Column('order_index', sa.Integer(), server_default='0', nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.UniqueConstraint('parent_node_id', 'child_node_id', name='unique_parent_child'),
        )
        op.create_index('ix_node_hierarchy_parent', 'node_hierarchy', ['parent_node_id'])
        op.create_index('ix_node_hierarchy_child', 'node_hierarchy', ['child_node_id'])


def downgrade() -> None:
    """Remove hierarchy fields and junction table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Drop node_hierarchy table
    if _table_exists(inspector, 'node_hierarchy'):
        try:
            op.drop_index('ix_node_hierarchy_child', table_name='node_hierarchy')
        except Exception:
            pass
        try:
            op.drop_index('ix_node_hierarchy_parent', table_name='node_hierarchy')
        except Exception:
            pass
        op.drop_table('node_hierarchy')

    # Drop hierarchy_level from mechanisms
    if _column_exists(inspector, 'mechanisms', 'hierarchy_level'):
        try:
            op.drop_index('ix_mechanisms_hierarchy_level', table_name='mechanisms')
        except Exception:
            pass
        op.drop_column('mechanisms', 'hierarchy_level')

    # Drop hierarchy columns from nodes (scale index handled by previous migration)
    for idx in ['ix_nodes_primary_path', 'ix_nodes_scale_depth', 'ix_nodes_is_grouping', 'ix_nodes_depth']:
        try:
            op.drop_index(idx, table_name='nodes')
        except Exception:
            pass

    for col in ['display_order', 'is_grouping_node', 'all_ancestors', 'primary_path', 'depth']:
        if _column_exists(inspector, 'nodes', col):
            op.drop_column('nodes', col)
