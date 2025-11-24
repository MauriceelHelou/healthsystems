"""
Week 1 Integration Pipeline

Integrates all critical Week 1 automation components:
1. Deduplication (mechanism_deduplication.py)
2. Functional form classification (functional_form_classifier.py)
3. Schema validation (validate_mechanism_schema.py)
4. Bidirectional detection (create_bidirectional_pairs.py)

This pipeline takes raw extracted mechanisms and produces MVP-ready mechanisms
that are deduplicated, functionally classified, validated, and bidirectional-complete.

Usage:
  # Full pipeline on extracted mechanisms
  python run_week1_pipeline.py --input-dir mechanism-bank/mechanisms/obesity/

  # Dry run to see what would happen
  python run_week1_pipeline.py --input-dir mechanism-bank/mechanisms/obesity/ --dry-run

  # Skip bidirectional detection (faster)
  python run_week1_pipeline.py --input-dir mechanism-bank/mechanisms/obesity/ --skip-bidirectional
"""

from pathlib import Path
import yaml
import argparse
from typing import Dict, List
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from pipelines.mechanism_deduplication import MechanismDeduplicator
from algorithms.functional_form_classifier import FunctionalFormClassifier
from scripts.validate_mechanism_schema import MechanismSchemaValidator
from scripts.create_bidirectional_pairs import BidirectionalMechanismDetector


class Week1Pipeline:
    """
    Integrates Week 1 critical automation:
    Raw mechanisms → Deduplicated → Functionally classified → Validated → Bidirectional-complete
    """

    def __init__(
        self,
        anthropic_api_key: str = None,
        pubmed_email: str = "healthsystems@example.com"
    ):
        """Initialize all components."""
        print("=== Initializing Week 1 Pipeline Components ===\n")

        self.deduplicator = MechanismDeduplicator(anthropic_api_key=anthropic_api_key)
        print("✓ Deduplicator initialized")

        self.classifier = FunctionalFormClassifier(anthropic_api_key=anthropic_api_key)
        print("✓ Functional form classifier initialized")

        self.validator = MechanismSchemaValidator(strict=False)
        print("✓ Schema validator initialized")

        self.bidirectional_detector = BidirectionalMechanismDetector(
            anthropic_api_key=anthropic_api_key,
            pubmed_email=pubmed_email
        )
        print("✓ Bidirectional detector initialized")

    def run_pipeline(
        self,
        input_dir: Path,
        output_dir: Path,
        skip_bidirectional: bool = False,
        dry_run: bool = False,
        verbose: bool = True
    ) -> Dict[str, any]:
        """
        Run full Week 1 pipeline.

        Args:
            input_dir: Directory with raw extracted mechanisms
            output_dir: Directory to save processed mechanisms
            skip_bidirectional: If True, skip bidirectional detection (faster)
            dry_run: If True, don't write files, just report what would happen
            verbose: Print progress

        Returns:
            Dict with pipeline stats
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)

        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        stats = {
            'input_mechanisms': 0,
            'deduplicated_mechanisms': 0,
            'classified_mechanisms': 0,
            'valid_mechanisms': 0,
            'invalid_mechanisms': 0,
            'bidirectional_pairs_created': 0,
            'total_output_mechanisms': 0
        }

        print(f"\n{'='*60}")
        print(f"WEEK 1 PIPELINE: {input_dir}")
        print(f"{'='*60}\n")

        # ===== STEP 1: DEDUPLICATION =====
        print("\n" + "="*60)
        print("STEP 1: DEDUPLICATION")
        print("="*60)

        deduplicated, dedup_stats = self.deduplicator.deduplicate_from_files(
            mechanism_dir=input_dir,
            output_dir=None,  # Don't save yet
            verbose=verbose
        )

        stats['input_mechanisms'] = dedup_stats['total_input']
        stats['deduplicated_mechanisms'] = dedup_stats['total_output']

        print(f"\n✓ Deduplication complete:")
        print(f"  Input: {stats['input_mechanisms']} mechanisms")
        print(f"  Output: {stats['deduplicated_mechanisms']} mechanisms")
        print(f"  Reduction: {dedup_stats['reduction_pct']:.1f}%")

        # ===== STEP 2: FUNCTIONAL FORM CLASSIFICATION =====
        print("\n" + "="*60)
        print("STEP 2: FUNCTIONAL FORM CLASSIFICATION")
        print("="*60)

        classified_mechanisms = []
        for mech in deduplicated:
            assignment = self.classifier.classify(mech, verbose=False)
            classified_mech = self.classifier.apply_to_mechanism(
                mech,
                assignment,
                overwrite=True
            )
            classified_mechanisms.append(classified_mech)

            if verbose:
                from_node = mech.get('from_node_id', 'unknown')
                to_node = mech.get('to_node_id', 'unknown')
                print(f"  {from_node} → {to_node}: {assignment.form} (conf: {assignment.confidence:.2f})")

        stats['classified_mechanisms'] = len(classified_mechanisms)

        print(f"\n✓ Classification complete: {stats['classified_mechanisms']} mechanisms classified")

        # ===== STEP 3: SCHEMA VALIDATION =====
        print("\n" + "="*60)
        print("STEP 3: SCHEMA VALIDATION")
        print("="*60)

        valid_mechanisms = []
        invalid_mechanisms = []

        for mech in classified_mechanisms:
            result = self.validator.validate(mech)

            if result.valid:
                valid_mechanisms.append(mech)
            else:
                invalid_mechanisms.append((mech, result))

                if verbose:
                    from_node = mech.get('from_node_id', 'unknown')
                    to_node = mech.get('to_node_id', 'unknown')
                    print(f"\n  ✗ INVALID: {from_node} → {to_node}")
                    for error in result.errors[:3]:
                        print(f"    - {error}")

        stats['valid_mechanisms'] = len(valid_mechanisms)
        stats['invalid_mechanisms'] = len(invalid_mechanisms)

        print(f"\n✓ Validation complete:")
        print(f"  Valid: {stats['valid_mechanisms']} mechanisms")
        print(f"  Invalid: {stats['invalid_mechanisms']} mechanisms")

        # ===== STEP 4: BIDIRECTIONAL DETECTION =====
        bidirectional_pairs = []

        if not skip_bidirectional:
            print("\n" + "="*60)
            print("STEP 4: BIDIRECTIONAL DETECTION")
            print("="*60)

            for mech in valid_mechanisms:
                # Skip if already marked as backward
                if mech.get('direction') == 'backward':
                    continue

                candidate = self.bidirectional_detector.detect_bidirectional(
                    mech,
                    search_literature=True,
                    verbose=False
                )

                if candidate.reverse_literature_found:
                    bidirectional_pairs.append((mech, candidate.reverse_mechanism))

                    if verbose:
                        from_node = mech.get('from_node_id', 'unknown')
                        to_node = mech.get('to_node_id', 'unknown')
                        print(f"  ✓ Bidirectional pair: {from_node} ↔ {to_node}")

            stats['bidirectional_pairs_created'] = len(bidirectional_pairs)

            print(f"\n✓ Bidirectional detection complete:")
            print(f"  Pairs created: {stats['bidirectional_pairs_created']}")

        # ===== STEP 5: SAVE RESULTS =====
        if not dry_run:
            print("\n" + "="*60)
            print("STEP 5: SAVING RESULTS")
            print("="*60)

            # Save valid mechanisms
            for mech in valid_mechanisms:
                self._save_mechanism(mech, output_dir)

            # Save reverse mechanisms from bidirectional pairs
            for _, reverse_mech in bidirectional_pairs:
                self._save_mechanism(reverse_mech, output_dir)

            stats['total_output_mechanisms'] = len(valid_mechanisms) + len(bidirectional_pairs)

            print(f"\n✓ Saved {stats['total_output_mechanisms']} mechanisms to: {output_dir}")

            # Save invalid mechanisms report
            if invalid_mechanisms:
                invalid_report_path = output_dir / "invalid_mechanisms_report.txt"
                with open(invalid_report_path, 'w', encoding='utf-8') as f:
                    f.write("INVALID MECHANISMS REPORT\n")
                    f.write("=" * 60 + "\n\n")

                    for mech, result in invalid_mechanisms:
                        from_node = mech.get('from_node_id', 'unknown')
                        to_node = mech.get('to_node_id', 'unknown')

                        f.write(f"Mechanism: {from_node} → {to_node}\n")
                        f.write(f"Errors:\n")
                        for error in result.errors:
                            f.write(f"  - {error}\n")
                        f.write(f"Warnings:\n")
                        for warning in result.warnings:
                            f.write(f"  - {warning}\n")
                        f.write("\n" + "-" * 60 + "\n\n")

                print(f"✓ Saved invalid mechanisms report to: {invalid_report_path}")

        else:
            print("\n" + "="*60)
            print("DRY RUN - No files written")
            print("="*60)
            stats['total_output_mechanisms'] = len(valid_mechanisms) + len(bidirectional_pairs)

        # ===== FINAL SUMMARY =====
        print("\n" + "="*60)
        print("PIPELINE SUMMARY")
        print("="*60)
        print(f"\nInput:  {stats['input_mechanisms']} raw mechanisms")
        print(f"\nStep 1 (Deduplication):  {stats['deduplicated_mechanisms']} mechanisms ({dedup_stats['reduction_pct']:.1f}% reduction)")
        print(f"Step 2 (Classification): {stats['classified_mechanisms']} mechanisms")
        print(f"Step 3 (Validation):     {stats['valid_mechanisms']} valid, {stats['invalid_mechanisms']} invalid")

        if not skip_bidirectional:
            print(f"Step 4 (Bidirectional):  +{stats['bidirectional_pairs_created']} reverse mechanisms")

        print(f"\nFinal Output: {stats['total_output_mechanisms']} MVP-ready mechanisms")

        if not dry_run:
            print(f"\nSaved to: {output_dir}")

        return stats

    def _save_mechanism(self, mechanism: Dict, output_dir: Path):
        """Save mechanism to YAML file."""
        category = mechanism.get('category', 'uncategorized')
        category_dir = output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        from_node = mechanism.get('from_node_id', 'unknown').replace('/', '_')
        to_node = mechanism.get('to_node_id', 'unknown').replace('/', '_')

        # Add suffix if backward
        suffix = "_backward" if mechanism.get('direction') == 'backward' else ""
        filename = f"{from_node}_to_{to_node}{suffix}.yml"

        output_path = category_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(mechanism, f, default_flow_style=False, allow_unicode=True)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Run Week 1 pipeline: dedup → classify → validate → bidirectional"
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Directory with raw extracted mechanisms'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory to save processed mechanisms (default: input-dir + "_processed")'
    )
    parser.add_argument(
        '--skip-bidirectional',
        action='store_true',
        help='Skip bidirectional detection (faster)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run: show what would happen without writing files'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or use ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = input_dir.parent / f"{input_dir.name}_processed"

    # Initialize pipeline
    pipeline = Week1Pipeline(anthropic_api_key=args.api_key)

    # Run pipeline
    stats = pipeline.run_pipeline(
        input_dir=input_dir,
        output_dir=output_dir,
        skip_bidirectional=args.skip_bidirectional,
        dry_run=args.dry_run,
        verbose=True
    )

    print("\n✓ Pipeline complete!\n")


if __name__ == "__main__":
    main()
