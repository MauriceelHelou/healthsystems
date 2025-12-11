"""
Migration script to add scale column to nodes table.

This script:
1. Adds a scale column (INTEGER) to the nodes table
2. Populates scale from category using the existing inference logic
3. Validates all nodes have valid scale values (1-7)
4. Adds NOT NULL and CHECK constraints
5. Provides rollback instructions if migration fails

Usage: python -m backend.scripts.add_scale_column
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from models import Node, Base
from api.config import settings
from utils.scale_inference import infer_scale_from_name

# Category to scale mapping (first-pass)
CATEGORY_SCALE_MAPPING = {
    'political': 1,
    'built_environment': 2,
    'economic': 3,
    'social_services': 3,
    'social_environment': 4,
    'economic_individual': 4,
    'behavioral': 5,
    'psychosocial': 5,
    'healthcare_access': 6,
    'clinical': 6,
    'biological': 7,
    'crisis': 7
}


def get_node_scale(node_id: str, node_name: str, category: str) -> int:
    """
    Determine node scale using category mapping with name inference fallback.

    First tries the category mapping. If the category isn't mapped or is
    'social_environment' (which is overly broad), falls back to name-based
    inference for more accurate classification.
    """
    # First check category mapping
    category_scale = CATEGORY_SCALE_MAPPING.get(category)

    # If category gives us a clear answer (not social_environment which is too broad)
    if category_scale is not None and category != 'social_environment':
        return category_scale

    # Otherwise, use name-based inference for better accuracy
    inferred_scale = infer_scale_from_name(node_id, node_name)

    # If inference found a match, use it
    if inferred_scale != 4:  # 4 is the default when no pattern matches
        return inferred_scale

    # Fall back to category mapping if available
    if category_scale is not None:
        return category_scale

    # Final fallback
    return 4


def add_scale_column():
    """Execute the migration to add scale column to nodes table."""

    print("=" * 60)
    print("MIGRATION: Adding scale column to nodes table")
    print("=" * 60)

    # Get database URL
    database_url = settings.database_url
    is_sqlite = database_url.startswith("sqlite")
    print(f"\nDatabase: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    print(f"Database type: {'SQLite' if is_sqlite else 'PostgreSQL'}")

    # Create engine and session
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine = create_engine(database_url, echo=False, connect_args=connect_args)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if scale column already exists
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('nodes')]

        if 'scale' in columns:
            print("\n⚠️  Scale column already exists!")
            response = input("Do you want to re-populate scale values? (yes/no): ")
            if response.lower() != 'yes':
                print("Migration aborted.")
                return
            else:
                # Skip to step 2
                print("\nSkipping to Step 2: Re-populating scale values...")
                populate_scale_values(session)
                print("\n✓ Migration complete!")
                return

        # Step 1: Add scale column as nullable
        print("\nStep 1: Adding scale column (nullable INTEGER)...")
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE nodes ADD COLUMN scale INTEGER;"))
            conn.commit()
        print("✓ Scale column added")

        # Step 2: Populate scale from category
        print("\nStep 2: Populating scale from category inference...")
        updated_count = populate_scale_values(session)
        print(f"✓ Updated {updated_count} nodes with scale values")

        # Step 3: Validate all nodes have valid scale
        print("\nStep 3: Validating scale values...")
        validate_scale_values(session)
        print("✓ All nodes have valid scale (1-7)")

        # Step 4: Add NOT NULL and CHECK constraints
        print("\nStep 4: Adding constraints...")
        with engine.connect() as conn:
            if is_sqlite:
                # SQLite doesn't support ALTER TABLE constraints after creation
                # For SQLite, we rely on application-level validation
                print("✓ Constraints will be enforced at application level (SQLite limitation)")
            else:
                conn.execute(text("ALTER TABLE nodes ALTER COLUMN scale SET NOT NULL;"))
                # Check if constraint already exists
                result = conn.execute(text("""
                    SELECT constraint_name FROM information_schema.table_constraints
                    WHERE table_name = 'nodes' AND constraint_name = 'scale_range';
                """))
                if not result.fetchone():
                    conn.execute(text("""
                        ALTER TABLE nodes ADD CONSTRAINT scale_range
                        CHECK (scale >= 1 AND scale <= 7);
                    """))
                print("✓ Constraints added (NOT NULL, CHECK 1-7)")
            conn.commit()

        # Step 5: Verify final state
        print("\nStep 5: Final verification...")
        verify_migration(session)

        print("\n" + "=" * 60)
        print("✓ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update backend/models/mechanism.py to include scale field")
        print("2. Update API response models to include scale")
        print("3. Test API endpoints return scale in responses")
        print("4. Update /admin/load-from-yaml to set scale on new nodes")

    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print("\nROLLBACK INSTRUCTIONS:")
        print("To remove the scale column, run:")
        print("  ALTER TABLE nodes DROP COLUMN scale;")
        session.rollback()
        raise
    finally:
        session.close()


def populate_scale_values(session) -> int:
    """Populate scale values from category and name inference."""
    nodes = session.query(Node).all()
    updated_count = 0

    for node in nodes:
        if not hasattr(node, 'scale') or node.scale is None:
            inferred_scale = get_node_scale(node.id, node.name, node.category)
            # Use direct SQL update since the ORM model doesn't have scale yet
            session.execute(
                text("UPDATE nodes SET scale = :scale WHERE id = :node_id"),
                {"scale": inferred_scale, "node_id": node.id}
            )
            updated_count += 1
            print(f"  {node.id}: category={node.category} → scale={inferred_scale}")

    session.commit()
    return updated_count


def validate_scale_values(session):
    """Validate all nodes have valid scale values (1-7)."""
    # Query nodes with invalid scale using raw SQL
    result = session.execute(text("""
        SELECT id, scale FROM nodes
        WHERE scale IS NULL OR scale < 1 OR scale > 7
    """))
    invalid_nodes = result.fetchall()

    if invalid_nodes:
        print(f"\n✗ Found {len(invalid_nodes)} nodes with invalid scale:")
        for node_id, scale in invalid_nodes:
            print(f"  {node_id}: scale={scale}")
        raise ValueError("Some nodes have invalid scale values. Please fix before proceeding.")

    # Count total nodes
    total = session.execute(text("SELECT COUNT(*) FROM nodes")).scalar()
    print(f"✓ All {total} nodes have valid scale (1-7)")


def verify_migration(session):
    """Verify the migration completed successfully."""
    # Get distribution of nodes by scale
    result = session.execute(text("""
        SELECT scale, COUNT(*) as count
        FROM nodes
        GROUP BY scale
        ORDER BY scale
    """))

    nodes_by_scale = result.fetchall()

    print("\nNodes by scale:")
    for scale, count in nodes_by_scale:
        scale_labels = {
            1: "Structural Determinants (policy)",
            2: "Built Environment & Infrastructure",
            3: "Institutional Infrastructure",
            4: "Individual/Household Conditions",
            5: "Individual Behaviors & Psychosocial",
            6: "Intermediate Pathways",
            7: "Crisis Endpoints"
        }
        label = scale_labels.get(scale, "Unknown")
        print(f"  Scale {scale} ({label}): {count} nodes")

    total = sum(count for _, count in nodes_by_scale)
    print(f"\nTotal nodes: {total}")


if __name__ == "__main__":
    add_scale_column()
