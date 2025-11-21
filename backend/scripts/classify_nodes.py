#!/usr/bin/env python3
"""
Unified CLI for node classification and mechanism grading.
Replaces 4 separate scripts.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.node_classification import NodeClassifier
from core.mechanism_grading import MechanismGrader
from models import get_db


def main():
    parser = argparse.ArgumentParser(
        prog='classify_nodes',
        description='Node classification and mechanism grading'
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Reclassify command
    reclassify = subparsers.add_parser('reclassify', help='Reclassify nodes')
    reclassify.add_argument('--auto', action='store_true', help='Auto-classify by keywords')
    reclassify.add_argument('--migrate', type=int, nargs=2, metavar=('FROM', 'TO'),
                           help='Migrate from old scale to new scale')
    reclassify.add_argument('--dry-run', action='store_true', help='Preview changes without committing')

    # Regrade command
    regrade = subparsers.add_parser('regrade', help='Regrade mechanisms')
    regrade.add_argument('--category', help='Regrade specific category only')
    regrade.add_argument('--dry-run', action='store_true', help='Preview changes without committing')

    # Stats command
    stats = subparsers.add_parser('stats', help='Show distribution statistics')
    stats.add_argument('--type', choices=['nodes', 'mechanisms'], default='nodes')

    args = parser.parse_args()

    # Get database session
    db = next(get_db())

    try:
        if args.command == 'reclassify':
            classifier = NodeClassifier(db, dry_run=args.dry_run)

            if args.auto:
                results = classifier.auto_classify_all()
            elif args.migrate:
                old_scale, new_scale = args.migrate
                results = classifier.migrate_scale_range(old_scale, new_scale)
            else:
                print("Error: Must specify --auto or --migrate")
                sys.exit(1)

            classifier.commit()
            classifier.stats.print_summary()

        elif args.command == 'regrade':
            grader = MechanismGrader(db, dry_run=args.dry_run)

            if args.category:
                results = grader.regrade_category(args.category)
            else:
                results = grader.regrade_all()

            grader.commit()
            grader.stats.print_summary()

        elif args.command == 'stats':
            if args.type == 'nodes':
                classifier = NodeClassifier(db)
                dist = classifier.get_scale_distribution()
                print("\nNode Scale Distribution:")
                for scale in sorted(dist.keys()):
                    print(f"  Scale {scale}: {dist[scale]} nodes")
            else:
                grader = MechanismGrader(db)
                dist = grader.get_grade_distribution()
                print("\nMechanism Grade Distribution:")
                for grade in ['A', 'B', 'C']:
                    count = dist.get(grade, 0)
                    print(f"  Grade {grade}: {count} mechanisms")

    finally:
        db.close()


if __name__ == "__main__":
    main()
