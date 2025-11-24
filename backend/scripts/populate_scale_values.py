"""
Populate scale values for all nodes based on category.

This script updates existing nodes with scale values inferred from their category.
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from api.config import settings

def get_node_scale_from_category(category: str) -> int:
    """
    Determine node scale based on category.

    7-scale taxonomy mapping:
    - political -> 1 (structural determinants - policy)
    - built_environment -> 2 (built environment & infrastructure)
    - economic, social_services -> 3 (institutional infrastructure)
    - social_environment, economic_individual -> 4 (individual/household conditions)
    - behavioral, psychosocial -> 5 (individual behaviors & psychosocial)
    - healthcare_access, clinical -> 6 (intermediate pathways)
    - biological, crisis -> 7 (crisis endpoints)
    """
    scale_mapping = {
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

    return scale_mapping.get(category, 4)  # Default to scale 4


def populate_scale_values():
    """Populate scale values from category inference."""

    print("=" * 60)
    print("Populating scale values for nodes")
    print("=" * 60)

    # Get database URL
    database_url = settings.database_url
    print(f"\nDatabase: {database_url}")

    # Create engine and session
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, echo=False, connect_args=connect_args)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get all nodes
        result = session.execute(text("SELECT id, category, scale FROM nodes"))
        nodes = result.fetchall()

        print(f"\nFound {len(nodes)} nodes")
        print("\nUpdating scale values...")

        updated_count = 0
        for node_id, category, current_scale in nodes:
            inferred_scale = get_node_scale_from_category(category)

            # Update if scale is NULL or different from inferred value
            if current_scale is None or current_scale != inferred_scale:
                session.execute(
                    text("UPDATE nodes SET scale = :scale WHERE id = :node_id"),
                    {"scale": inferred_scale, "node_id": node_id}
                )
                updated_count += 1
                print(f"  {node_id}: category={category} -> scale={inferred_scale}")

        session.commit()
        print(f"\n[OK] Updated {updated_count} nodes")

        # Show distribution by scale
        print("\nDistribution by scale:")
        result = session.execute(text("""
            SELECT scale, COUNT(*) as count
            FROM nodes
            GROUP BY scale
            ORDER BY scale
        """))

        scale_labels = {
            1: "Structural Determinants (policy)",
            2: "Built Environment & Infrastructure",
            3: "Institutional Infrastructure",
            4: "Individual/Household Conditions",
            5: "Individual Behaviors & Psychosocial",
            6: "Intermediate Pathways",
            7: "Crisis Endpoints"
        }

        for scale, count in result:
            label = scale_labels.get(scale, "Unknown")
            print(f"  Scale {scale} ({label}): {count} nodes")

        print("\n[OK] Migration complete!")

    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_scale_values()
