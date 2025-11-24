"""
Node classification command
"""

import argparse
from pathlib import Path
from backend.cli.base import BaseCLI, add_common_arguments


class ClassifyCommand(BaseCLI):
    """Classify nodes using the 7-scale taxonomy."""

    def get_name(self) -> str:
        return 'classify'

    def get_description(self) -> str:
        return 'Classify nodes in inventory file using 7-scale taxonomy'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'action',
            choices=['reclassify', 'stats'],
            help='Action to perform'
        )
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Auto-classify nodes by keywords (for reclassify)'
        )
        parser.add_argument(
            '--migrate',
            type=int,
            nargs=2,
            metavar=('FROM', 'TO'),
            help='Migrate from old scale to new scale (for reclassify)'
        )
        parser.add_argument(
            '--type',
            choices=['nodes', 'mechanisms'],
            default='nodes',
            help='Type of statistics to show (for stats)'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        """Execute classification command."""
        try:
            # Import here to avoid import errors if dependencies not installed
            import sys
            from pathlib import Path

            # Add backend to path
            backend_path = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(backend_path))

            from core.node_classification import NodeClassifier
            from core.mechanism_grading import MechanismGrader
            from models import get_db

            # Get database session
            db = next(get_db())

            try:
                if args.action == 'reclassify':
                    self._run_reclassify(db, args)
                elif args.action == 'stats':
                    self._run_stats(db, args)
                else:
                    self.error_exit(f"Unknown action: {args.action}")

            finally:
                db.close()

            return 0

        except ImportError as e:
            self.error_exit(f"Failed to import required modules: {e}")
            return 1
        except Exception as e:
            self.error_exit(f"Classification failed: {e}")
            return 1

    def _run_reclassify(self, db, args):
        """Run reclassification."""
        from core.node_classification import NodeClassifier

        self.logger.info("Starting node reclassification...")

        if args.dry_run:
            self.logger.info("[DRY RUN] No changes will be committed to database")

        classifier = NodeClassifier(db, dry_run=args.dry_run)

        if args.auto:
            self.logger.info("Running auto-classification by keywords...")
            results = classifier.auto_classify_all()
        elif args.migrate:
            old_scale, new_scale = args.migrate
            self.logger.info(f"Migrating nodes from scale {old_scale} to scale {new_scale}...")
            results = classifier.migrate_scale_range(old_scale, new_scale)
        else:
            self.error_exit("Must specify --auto or --migrate for reclassify action")

        if not args.dry_run:
            classifier.commit()

        classifier.stats.print_summary()
        self.logger.info("Reclassification complete")

    def _run_stats(self, db, args):
        """Show distribution statistics."""
        if args.type == 'nodes':
            from core.node_classification import NodeClassifier

            classifier = NodeClassifier(db)
            dist = classifier.get_scale_distribution()

            print("\nNode Scale Distribution:")
            for scale in sorted(dist.keys()):
                print(f"  Scale {scale}: {dist[scale]} nodes")
        else:
            from core.mechanism_grading import MechanismGrader

            grader = MechanismGrader(db)
            dist = grader.get_grade_distribution()

            print("\nMechanism Grade Distribution:")
            for grade in ['A', 'B', 'C']:
                count = dist.get(grade, 0)
                print(f"  Grade {grade}: {count} mechanisms")
