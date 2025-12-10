"""Initial migration - nodes, mechanisms, geographic_contexts

Revision ID: 516074b986c0
Revises:
Create Date: 2025-11-17 20:04:48.210708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '516074b986c0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    return table_name in inspector.get_table_names()


def index_exists(index_name: str, table_name: str) -> bool:
    """Check if an index exists on a table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    try:
        indexes = inspector.get_indexes(table_name)
        return any(idx['name'] == index_name for idx in indexes)
    except Exception:
        return False


def upgrade() -> None:
    """Upgrade schema - idempotent, skips existing tables."""
    # Create geographic_contexts table if it doesn't exist
    if not table_exists('geographic_contexts'):
        op.create_table('geographic_contexts',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('geography_type', sa.String(), nullable=False),
            sa.Column('fips_code', sa.String(), nullable=True),
            sa.Column('census_tract', sa.String(), nullable=True),
            sa.Column('state', sa.String(), nullable=True),
            sa.Column('county', sa.String(), nullable=True),
            sa.Column('medicaid_expansion', sa.Boolean(), nullable=True),
            sa.Column('medicaid_eligibility_threshold', sa.Integer(), nullable=True),
            sa.Column('housing_code_enforcement_strength', sa.String(), nullable=True),
            sa.Column('rental_assistance_availability', sa.String(), nullable=True),
            sa.Column('minimum_wage', sa.Float(), nullable=True),
            sa.Column('population', sa.Integer(), nullable=True),
            sa.Column('poverty_rate', sa.Float(), nullable=True),
            sa.Column('median_income', sa.Float(), nullable=True),
            sa.Column('uninsurance_rate', sa.Float(), nullable=True),
            sa.Column('racial_composition', sa.JSON(), nullable=True),
            sa.Column('baseline_mortality_rate', sa.Float(), nullable=True),
            sa.Column('baseline_asthma_rate', sa.Float(), nullable=True),
            sa.Column('baseline_diabetes_rate', sa.Float(), nullable=True),
            sa.Column('baseline_ed_utilization', sa.Float(), nullable=True),
            sa.Column('housing_quality_index', sa.Float(), nullable=True),
            sa.Column('air_quality_index', sa.Float(), nullable=True),
            sa.Column('walkability_index', sa.Float(), nullable=True),
            sa.Column('data_year', sa.Integer(), nullable=True),
            sa.Column('data_sources', sa.JSON(), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        if not index_exists('ix_geographic_contexts_id', 'geographic_contexts'):
            op.create_index(op.f('ix_geographic_contexts_id'), 'geographic_contexts', ['id'], unique=False)
        if not index_exists('ix_geographic_contexts_state', 'geographic_contexts'):
            op.create_index(op.f('ix_geographic_contexts_state'), 'geographic_contexts', ['state'], unique=False)

    # Create nodes table if it doesn't exist
    if not table_exists('nodes'):
        op.create_table('nodes',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('node_type', sa.String(), nullable=False),
            sa.Column('unit', sa.String(), nullable=True),
            sa.Column('measurement_method', sa.Text(), nullable=True),
            sa.Column('typical_range', sa.String(), nullable=True),
            sa.Column('data_sources', sa.JSON(), nullable=True),
            sa.Column('category', sa.String(), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        if not index_exists('ix_nodes_category', 'nodes'):
            op.create_index(op.f('ix_nodes_category'), 'nodes', ['category'], unique=False)
        if not index_exists('ix_nodes_id', 'nodes'):
            op.create_index(op.f('ix_nodes_id'), 'nodes', ['id'], unique=False)

    # Create mechanisms table if it doesn't exist
    if not table_exists('mechanisms'):
        op.create_table('mechanisms',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('from_node_id', sa.String(), nullable=False),
            sa.Column('to_node_id', sa.String(), nullable=False),
            sa.Column('direction', sa.String(), nullable=False),
            sa.Column('category', sa.String(), nullable=False),
            sa.Column('mechanism_pathway', sa.JSON(), nullable=True),
            sa.Column('evidence_quality', sa.String(), nullable=False),
            sa.Column('evidence_n_studies', sa.Integer(), nullable=False),
            sa.Column('evidence_primary_citation', sa.Text(), nullable=False),
            sa.Column('evidence_supporting_citations', sa.JSON(), nullable=True),
            sa.Column('evidence_doi', sa.String(), nullable=True),
            sa.Column('varies_by_geography', sa.Boolean(), nullable=True),
            sa.Column('variation_notes', sa.Text(), nullable=True),
            sa.Column('relevant_geographies', sa.JSON(), nullable=True),
            sa.Column('moderators', sa.JSON(), nullable=True),
            sa.Column('structural_competency_root_cause', sa.String(), nullable=True),
            sa.Column('structural_competency_avoids_victim_blaming', sa.Boolean(), nullable=True),
            sa.Column('structural_competency_equity_implications', sa.Text(), nullable=True),
            sa.Column('version', sa.String(), nullable=True),
            sa.Column('last_updated', sa.DateTime(), nullable=True),
            sa.Column('validated_by', sa.JSON(), nullable=True),
            sa.Column('llm_extracted_by', sa.String(), nullable=True),
            sa.Column('llm_extraction_date', sa.DateTime(), nullable=True),
            sa.Column('llm_extraction_confidence', sa.String(), nullable=True),
            sa.Column('llm_prompt_version', sa.String(), nullable=True),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('assumptions', sa.JSON(), nullable=True),
            sa.Column('limitations', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
            sa.ForeignKeyConstraint(['from_node_id'], ['nodes.id'], ),
            sa.ForeignKeyConstraint(['to_node_id'], ['nodes.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        if not index_exists('ix_mechanisms_category', 'mechanisms'):
            op.create_index(op.f('ix_mechanisms_category'), 'mechanisms', ['category'], unique=False)
        if not index_exists('ix_mechanisms_from_node_id', 'mechanisms'):
            op.create_index(op.f('ix_mechanisms_from_node_id'), 'mechanisms', ['from_node_id'], unique=False)
        if not index_exists('ix_mechanisms_id', 'mechanisms'):
            op.create_index(op.f('ix_mechanisms_id'), 'mechanisms', ['id'], unique=False)
        if not index_exists('ix_mechanisms_to_node_id', 'mechanisms'):
            op.create_index(op.f('ix_mechanisms_to_node_id'), 'mechanisms', ['to_node_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    if table_exists('mechanisms'):
        op.drop_index(op.f('ix_mechanisms_to_node_id'), table_name='mechanisms')
        op.drop_index(op.f('ix_mechanisms_id'), table_name='mechanisms')
        op.drop_index(op.f('ix_mechanisms_from_node_id'), table_name='mechanisms')
        op.drop_index(op.f('ix_mechanisms_category'), table_name='mechanisms')
        op.drop_table('mechanisms')
    if table_exists('nodes'):
        op.drop_index(op.f('ix_nodes_id'), table_name='nodes')
        op.drop_index(op.f('ix_nodes_category'), table_name='nodes')
        op.drop_table('nodes')
    if table_exists('geographic_contexts'):
        op.drop_index(op.f('ix_geographic_contexts_state'), table_name='geographic_contexts')
        op.drop_index(op.f('ix_geographic_contexts_id'), table_name='geographic_contexts')
        op.drop_table('geographic_contexts')
