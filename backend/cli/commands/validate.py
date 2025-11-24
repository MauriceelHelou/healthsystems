"""
Mechanism validation command
"""

import argparse
from pathlib import Path
from backend.cli.base import BaseCLI, add_common_arguments


class ValidateCommand(BaseCLI):
    """Validate mechanism YAML files for schema compliance."""

    def get_name(self) -> str:
        return 'validate'

    def get_description(self) -> str:
        return 'Validate mechanism YAML files for schema compliance and data quality'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'path',
            type=Path,
            help='Path to mechanism YAML file or directory containing YAML files'
        )
        parser.add_argument(
            '--schema',
            type=Path,
            help='Path to schema file (default: auto-detect)'
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to auto-fix common issues'
        )
        parser.add_argument(
            '--strict',
            action='store_true',
            help='Enable strict validation (fail on warnings)'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        """Execute validation command."""
        try:
            # Validate path exists
            if not args.path.exists():
                self.error_exit(f"Path not found: {args.path}")

            self.logger.info(f"Validating mechanisms in: {args.path}")

            if args.strict:
                self.logger.info("Strict mode enabled: warnings will cause validation to fail")

            if args.fix:
                if args.dry_run:
                    self.logger.info("[DRY RUN] Would attempt to fix issues, but no changes will be made")
                else:
                    self.logger.info("Auto-fix enabled: will attempt to fix common issues")

            # Collect YAML files
            yaml_files = []
            if args.path.is_file():
                if args.path.suffix in ['.yml', '.yaml']:
                    yaml_files = [args.path]
                else:
                    self.error_exit(f"File is not a YAML file: {args.path}")
            else:
                yaml_files = list(args.path.glob('**/*.yml')) + list(args.path.glob('**/*.yaml'))

            if not yaml_files:
                self.logger.warning(f"No YAML files found in: {args.path}")
                return 0

            self.logger.info(f"Found {len(yaml_files)} YAML files to validate")

            # Validate each file
            errors = 0
            warnings = 0

            for yaml_file in yaml_files:
                result = self._validate_file(yaml_file, args)
                errors += result['errors']
                warnings += result['warnings']

            # Print summary
            print("\n" + "="*60)
            print("VALIDATION SUMMARY")
            print("="*60)
            print(f"Files validated: {len(yaml_files)}")
            print(f"Errors: {errors}")
            print(f"Warnings: {warnings}")

            if errors == 0 and warnings == 0:
                print("\n[OK] All files passed validation!")
                return 0
            elif errors == 0:
                print(f"\n[WARNING] {warnings} warnings found")
                if args.strict:
                    self.logger.error("Strict mode: failing due to warnings")
                    return 1
                return 0
            else:
                print(f"\n[ERROR] {errors} errors found")
                return 1

        except Exception as e:
            self.error_exit(f"Validation failed: {e}")
            return 1

    def _validate_file(self, yaml_file: Path, args) -> dict:
        """Validate a single YAML file."""
        import yaml

        result = {'errors': 0, 'warnings': 0}

        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if args.verbose:
                self.logger.debug(f"Validating: {yaml_file.name}")

            # Basic schema validation
            required_fields = ['id', 'name', 'from_node', 'to_node', 'direction', 'category']
            missing = [field for field in required_fields if field not in data]

            if missing:
                result['errors'] += len(missing)
                print(f"\n[X] {yaml_file.name}")
                print(f"  Missing required fields: {', '.join(missing)}")
            else:
                # Check data quality
                if not data.get('evidence'):
                    result['warnings'] += 1
                    if args.verbose:
                        print(f"\n[!] {yaml_file.name}")
                        print("  Missing evidence section")

                if data.get('evidence', {}).get('n_studies', 0) == 0:
                    result['warnings'] += 1
                    if args.verbose:
                        print(f"\n[!] {yaml_file.name}")
                        print("  No studies cited (n_studies = 0)")

                # Validate direction
                if data.get('direction') not in ['positive', 'negative']:
                    result['errors'] += 1
                    print(f"\n[X] {yaml_file.name}")
                    print(f"  Invalid direction: {data.get('direction')}")

                # Validate evidence quality
                quality = data.get('evidence', {}).get('quality_rating')
                if quality and quality not in ['A', 'B', 'C']:
                    result['errors'] += 1
                    print(f"\n[X] {yaml_file.name}")
                    print(f"  Invalid evidence quality: {quality}")

        except yaml.YAMLError as e:
            result['errors'] += 1
            print(f"\n[X] {yaml_file.name}")
            print(f"  YAML parse error: {e}")
        except Exception as e:
            result['errors'] += 1
            print(f"\n[X] {yaml_file.name}")
            print(f"  Validation error: {e}")

        return result
