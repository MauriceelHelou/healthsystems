"""
Mechanism regrading command
"""

import argparse
from pathlib import Path
from backend.cli.base import BaseCLI, add_common_arguments


class RegradeCommand(BaseCLI):
    """Regrade mechanisms based on evidence quality."""

    def get_name(self) -> str:
        return 'regrade'

    def get_description(self) -> str:
        return 'Regrade mechanisms based on evidence quality and study counts'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--category',
            help='Regrade specific category only (e.g., economic, social_environment)'
        )
        parser.add_argument(
            '--input',
            type=Path,
            help='Input directory containing mechanism YAML files (default: mechanism-bank/mechanisms/)'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        """Execute regrading command."""
        try:
            # Import here to avoid import errors if dependencies not installed
            import sys
            backend_path = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(backend_path))

            from core.mechanism_grading import MechanismGrader
            from models import get_db

            self.logger.info("Starting mechanism regrading...")

            if args.dry_run:
                self.logger.info("[DRY RUN] No changes will be committed to database")

            if args.category:
                self.logger.info(f"Regrading category: {args.category}")

            # Get database session
            db = next(get_db())

            try:
                grader = MechanismGrader(db, dry_run=args.dry_run)

                if args.category:
                    results = grader.regrade_category(args.category)
                else:
                    self.logger.info("Regrading all mechanisms...")
                    results = grader.regrade_all()

                if not args.dry_run:
                    grader.commit()

                grader.stats.print_summary()
                self.logger.info("Regrading complete")

            finally:
                db.close()

            return 0

        except ImportError as e:
            self.error_exit(f"Failed to import required modules: {e}")
            return 1
        except Exception as e:
            self.error_exit(f"Regrading failed: {e}")
            return 1
