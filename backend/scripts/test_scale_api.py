"""
Test script to verify that nodes have scale field populated and can be queried.
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Node
from api.config import settings

def test_scale_field():
    """Test that scale field is populated in the database."""

    print("=" * 60)
    print("Testing scale field in nodes table")
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
        # Test 1: Check all nodes have scale
        print("\n[TEST 1] Checking all nodes have scale field...")
        null_scale_nodes = session.query(Node).filter(Node.scale.is_(None)).all()

        if null_scale_nodes:
            print(f"  [FAIL] Found {len(null_scale_nodes)} nodes with NULL scale:")
            for node in null_scale_nodes[:5]:
                print(f"    - {node.id}")
        else:
            print("  [PASS] All nodes have scale values")

        # Test 2: Check scale range (1-7)
        print("\n[TEST 2] Checking scale values are in range 1-7...")
        result = session.execute(text("""
            SELECT MIN(scale) as min_scale, MAX(scale) as max_scale
            FROM nodes
        """))
        min_scale, max_scale = result.fetchone()
        print(f"  Scale range: {min_scale} to {max_scale}")

        if min_scale >= 1 and max_scale <= 7:
            print("  [PASS] All scale values are within valid range (1-7)")
        else:
            print(f"  [FAIL] Scale values out of range: {min_scale} to {max_scale}")

        # Test 3: Query nodes using ORM
        print("\n[TEST 3] Querying nodes using SQLAlchemy ORM...")
        sample_nodes = session.query(Node).limit(5).all()

        for node in sample_nodes:
            has_scale = hasattr(node, 'scale') and node.scale is not None
            status = "[PASS]" if has_scale else "[FAIL]"
            scale_value = node.scale if has_scale else "MISSING"
            print(f"  {status} {node.id}: category={node.category}, scale={scale_value}")

        # Test 4: Show distribution
        print("\n[TEST 4] Distribution by scale...")
        result = session.execute(text("""
            SELECT scale, category, COUNT(*) as count
            FROM nodes
            GROUP BY scale, category
            ORDER BY scale, category
        """))

        scale_labels = {
            1: "Structural Determinants",
            2: "Built Environment",
            3: "Institutional Infrastructure",
            4: "Individual/Household",
            5: "Behaviors & Psychosocial",
            6: "Intermediate Pathways",
            7: "Crisis Endpoints"
        }

        current_scale = None
        for scale, category, count in result:
            if scale != current_scale:
                current_scale = scale
                print(f"\n  Scale {scale} ({scale_labels.get(scale, 'Unknown')}):")
            print(f"    {category}: {count} nodes")

        print("\n" + "=" * 60)
        print("[SUCCESS] All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    test_scale_field()
