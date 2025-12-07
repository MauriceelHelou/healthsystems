#!/usr/bin/env python3
"""
Create Domain Root Nodes for Hierarchy

Creates the 17 top-level domain nodes (depth=0) that form the root
of the node hierarchy. These are grouping nodes that organize all
other nodes by thematic area.

Usage:
    python backend/scripts/create_domain_nodes.py
    python backend/scripts/create_domain_nodes.py --dry-run
    python backend/scripts/create_domain_nodes.py --force  # Replace existing
"""

import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from models.database import SessionLocal, engine, Base
from models.mechanism import Node

# ==========================================
# Domain Definitions (17 Domains)
# ==========================================

DOMAIN_DEFINITIONS = [
    {
        "id": "healthcare_system",
        "name": "Healthcare System",
        "description": "Insurance, providers, access, utilization, outcomes. Spans from federal policy (Medicaid expansion) to crisis endpoints (avoidable ED visits).",
        "scale": 1,  # Domain nodes are policy-level by default
        "node_type": "stock",
        "display_order": 1,
    },
    {
        "id": "housing",
        "name": "Housing",
        "description": "Policy, stock, affordability, quality, homelessness. Spans from rent control policy to homelessness rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 2,
    },
    {
        "id": "economic_security",
        "name": "Economic Security",
        "description": "Income, poverty, debt, safety net programs. Spans from minimum wage policy to medical bankruptcy rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 3,
    },
    {
        "id": "employment_occupational",
        "name": "Employment & Occupational",
        "description": "Labor laws, workplace safety, job quality. Spans from OSHA standards to occupational fatality rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 4,
    },
    {
        "id": "food_security",
        "name": "Food Security",
        "description": "SNAP, food retail, access, nutrition. Spans from SNAP benefit levels to malnutrition hospitalizations.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 5,
    },
    {
        "id": "education",
        "name": "Education",
        "description": "Policy, schools, attainment, child development. Spans from education funding formulas to school dropout rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 6,
    },
    {
        "id": "built_environment_transportation",
        "name": "Built Environment & Transportation",
        "description": "Transit, parks, walkability, active transport. Spans from transit funding to traffic fatality rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 7,
    },
    {
        "id": "environmental_climate",
        "name": "Environmental & Climate",
        "description": "Pollution, climate, exposures, environmental health. Spans from Clean Air Act enforcement to heat stroke deaths.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 8,
    },
    {
        "id": "criminal_justice",
        "name": "Criminal Justice",
        "description": "Sentencing, policing, incarceration, reentry. Spans from bail reform policy to recidivism rates.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 9,
    },
    {
        "id": "social_environment",
        "name": "Social Environment",
        "description": "Discrimination, social support, community cohesion. Spans from civil rights enforcement to social isolation mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 10,
    },
    {
        "id": "behavioral_health",
        "name": "Behavioral Health",
        "description": "Mental health, substance use, treatment, crisis. Spans from mental health parity laws to overdose mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 11,
    },
    {
        "id": "long_term_services_supports",
        "name": "Long-Term Services & Supports",
        "description": "LTSS, disability, caregiving, aging. Spans from Medicaid HCBS waivers to nursing home mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 12,
    },
    {
        "id": "maternal_child_health",
        "name": "Maternal & Child Health",
        "description": "Pregnancy, birth, child development, pediatrics. Spans from pregnancy Medicaid to infant mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 13,
    },
    {
        "id": "specialized_clinical",
        "name": "Specialized Clinical",
        "description": "Cancer, kidney, transplant, oral, vision, pain, geriatrics. Spans from cancer screening mandates to cancer mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 14,
    },
    {
        "id": "public_health_infrastructure",
        "name": "Public Health Infrastructure",
        "description": "Funding, departments, surveillance, preparedness. Spans from public health funding to outbreak mortality.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 15,
    },
    {
        "id": "digital_information_access",
        "name": "Digital & Information Access",
        "description": "Broadband, telehealth, digital literacy. Spans from broadband subsidy policy to digital divide health disparities.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 16,
    },
    {
        "id": "civic_political_engagement",
        "name": "Civic & Political Engagement",
        "description": "Voting, civic participation, political power. Spans from voting rights laws to disenfranchisement health impacts.",
        "scale": 1,
        "node_type": "stock",
        "display_order": 17,
    },
]


def create_domain_nodes(db: Session, dry_run: bool = False, force: bool = False) -> dict:
    """
    Create the 17 domain root nodes.

    Args:
        db: Database session
        dry_run: If True, don't commit changes
        force: If True, replace existing domain nodes

    Returns:
        dict with 'created', 'skipped', 'updated' counts
    """
    results = {"created": 0, "skipped": 0, "updated": 0, "errors": []}

    for domain_def in DOMAIN_DEFINITIONS:
        domain_id = domain_def["id"]

        # Check if domain already exists
        existing = db.query(Node).filter(Node.id == domain_id).first()

        if existing:
            if force:
                # Update existing node
                existing.name = domain_def["name"]
                existing.description = domain_def["description"]
                existing.scale = domain_def["scale"]
                existing.node_type = domain_def["node_type"]
                existing.category = domain_id  # Use domain ID as category for backward compatibility
                existing.depth = 0
                existing.is_grouping_node = True
                existing.display_order = domain_def["display_order"]
                existing.primary_path = domain_id
                existing.all_ancestors = []
                results["updated"] += 1
                print(f"  Updated: {domain_id} ({domain_def['name']})")
            else:
                results["skipped"] += 1
                print(f"  Skipped (exists): {domain_id}")
        else:
            # Create new domain node
            node = Node(
                id=domain_id,
                name=domain_def["name"],
                description=domain_def["description"],
                scale=domain_def["scale"],
                node_type=domain_def["node_type"],
                category=domain_id,  # Use domain ID as category for backward compatibility
                depth=0,
                is_grouping_node=True,
                display_order=domain_def["display_order"],
                primary_path=domain_id,
                all_ancestors=[],
            )
            db.add(node)
            results["created"] += 1
            print(f"  Created: {domain_id} ({domain_def['name']})")

    if not dry_run:
        try:
            db.commit()
            print(f"\n✓ Changes committed to database")
        except Exception as e:
            db.rollback()
            results["errors"].append(str(e))
            print(f"\n✗ Error committing: {e}")
    else:
        print(f"\n(Dry run - no changes committed)")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Create 17 domain root nodes for hierarchy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without committing"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Update existing domain nodes"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Creating Domain Root Nodes (depth=0)")
    print("=" * 60)
    print(f"\nDomains to create: {len(DOMAIN_DEFINITIONS)}")
    print(f"Dry run: {args.dry_run}")
    print(f"Force update: {args.force}")
    print()

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Create domain nodes
    db = SessionLocal()
    try:
        results = create_domain_nodes(db, dry_run=args.dry_run, force=args.force)

        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  Created: {results['created']}")
        print(f"  Updated: {results['updated']}")
        print(f"  Skipped: {results['skipped']}")
        if results["errors"]:
            print(f"  Errors: {len(results['errors'])}")
            for err in results["errors"]:
                print(f"    - {err}")
        print("=" * 60)

        return 0 if not results["errors"] else 1

    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
