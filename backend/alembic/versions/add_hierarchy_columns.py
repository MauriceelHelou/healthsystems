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


def upgrade() -> None:
    """Add hierarchy fields to nodes and mechanisms, create junction table."""

    # Add hierarchy fields to nodes (scale column already exists from previous migration)
    op.add_column('nodes', sa.Column('depth', sa.Integer(), server_default='0', nullable=True))
    op.add_column('nodes', sa.Column('primary_path', sa.String(), nullable=True))
    op.add_column('nodes', sa.Column('all_ancestors', sa.JSON(), nullable=True))
    op.add_column('nodes', sa.Column('is_grouping_node', sa.Boolean(), server_default='0', nullable=True))
    op.add_column('nodes', sa.Column('display_order', sa.Integer(), server_default='0', nullable=True))

    # Create indexes for hierarchy fields (scale index already exists from previous migration)
    op.create_index('ix_nodes_depth', 'nodes', ['depth'])
    op.create_index('ix_nodes_is_grouping', 'nodes', ['is_grouping_node'])
    op.create_index('ix_nodes_scale_depth', 'nodes', ['scale', 'depth'])
    op.create_index('ix_nodes_primary_path', 'nodes', ['primary_path'])

    # Add hierarchy_level column to mechanisms
    op.add_column('mechanisms', sa.Column('hierarchy_level', sa.String(), server_default='leaf', nullable=True))
    op.create_index('ix_mechanisms_hierarchy_level', 'mechanisms', ['hierarchy_level'])

    # Create node_hierarchy junction table for DAG support
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

    # Drop node_hierarchy table
    op.drop_index('ix_node_hierarchy_child', table_name='node_hierarchy')
    op.drop_index('ix_node_hierarchy_parent', table_name='node_hierarchy')
    op.drop_table('node_hierarchy')

    # Drop hierarchy_level from mechanisms
    op.drop_index('ix_mechanisms_hierarchy_level', table_name='mechanisms')
    op.drop_column('mechanisms', 'hierarchy_level')

    # Drop hierarchy columns from nodes (scale index handled by previous migration)
    op.drop_index('ix_nodes_primary_path', table_name='nodes')
    op.drop_index('ix_nodes_scale_depth', table_name='nodes')
    op.drop_index('ix_nodes_is_grouping', table_name='nodes')
    op.drop_index('ix_nodes_depth', table_name='nodes')

    op.drop_column('nodes', 'display_order')
    op.drop_column('nodes', 'is_grouping_node')
    op.drop_column('nodes', 'all_ancestors')
    op.drop_column('nodes', 'primary_path')
    op.drop_column('nodes', 'depth')
