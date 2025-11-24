"""
Mechanism extraction command
"""

import argparse
import json
from pathlib import Path
from backend.cli.base import BaseCLI, add_common_arguments


class ExtractCommand(BaseCLI):
    """Extract mechanisms using LLM pipeline."""

    def get_name(self) -> str:
        return 'extract'

    def get_description(self) -> str:
        return 'Extract mechanisms using LLM pipeline (alcohol or generic topics)'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'extractor',
            choices=['alcohol', 'generic'],
            help='Extraction type: alcohol-specific or generic topic'
        )
        parser.add_argument(
            '--config',
            type=Path,
            help='Config JSON file for generic extraction (required for generic extractor)'
        )
        parser.add_argument(
            '--phases',
            type=str,
            help='Comma-separated phase numbers to run (e.g., "1,2,3" or "all")',
            default='all'
        )
        parser.add_argument(
            '--output-dir',
            type=Path,
            help='Output directory for extracted mechanisms (default: mechanism-bank/mechanisms/)'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        """Execute extraction command."""
        try:
            # Validate arguments
            if args.extractor == 'generic' and not args.config:
                self.error_exit("--config is required for generic extraction")

            if args.config:
                self.validate_file_exists(args.config, "Config file")

            # Parse phases
            if args.phases.lower() == 'all':
                phases = [1, 2, 3]
            else:
                try:
                    phases = [int(p.strip()) for p in args.phases.split(',')]
                    if not all(1 <= p <= 3 for p in phases):
                        self.error_exit("Phase numbers must be between 1 and 3")
                except ValueError:
                    self.error_exit("Invalid phases format. Use comma-separated numbers or 'all'")

            if args.dry_run:
                self.logger.info("[DRY RUN] No mechanisms will be written to disk")
                self.logger.info(f"Would run {args.extractor} extraction with phases: {phases}")
                if args.config:
                    self.logger.info(f"Config file: {args.config}")
                return 0

            # Import extraction modules
            import sys
            backend_path = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(backend_path))

            if args.extractor == 'alcohol':
                self._run_alcohol_extraction(phases, args)
            elif args.extractor == 'generic':
                self._run_generic_extraction(args.config, phases, args)

            self.logger.info("Extraction complete")
            return 0

        except Exception as e:
            self.error_exit(f"Extraction failed: {e}")
            return 1

    def _run_alcohol_extraction(self, phases, args):
        """Run alcohol-specific extraction."""
        from pipelines.llm_mechanism_discovery import UnifiedExtractionPipeline

        self.logger.info("Starting alcohol mechanism extraction...")
        self.logger.info(f"Running phases: {phases}")

        # Configure for alcohol extraction
        config = {
            'topic': 'alcohol use disorder and liver disease',
            'output_prefix': 'alcohol_',
            'phases': phases,
        }

        if args.output_dir:
            config['output_dir'] = str(args.output_dir)

        pipeline = UnifiedExtractionPipeline(config)
        results = pipeline.run()

        self.logger.info(f"Extracted {len(results)} mechanisms")

    def _run_generic_extraction(self, config_path, phases, args):
        """Run generic topic extraction."""
        from pipelines.llm_mechanism_discovery import UnifiedExtractionPipeline

        self.logger.info(f"Starting generic extraction from config: {config_path}")
        self.logger.info(f"Running phases: {phases}")

        # Load config
        with open(config_path, 'r') as f:
            config = json.load(f)

        config['phases'] = phases

        if args.output_dir:
            config['output_dir'] = str(args.output_dir)

        pipeline = UnifiedExtractionPipeline(config)
        results = pipeline.run()

        self.logger.info(f"Extracted {len(results)} mechanisms")
        self.logger.info(f"Results saved to: {config.get('output_dir', 'mechanism-bank/mechanisms/')}")
