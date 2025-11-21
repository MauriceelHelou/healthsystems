#!/usr/bin/env python3
"""
Unified CLI for mechanism extraction.
Replaces 6 separate extraction scripts.
"""
import argparse
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extraction.core import MechanismExtractor, ExtractionConfig


def main():
    parser = argparse.ArgumentParser(
        prog='extract_mechanisms',
        description='Extract causal mechanisms using LLM'
    )

    # Required arguments
    parser.add_argument('topic', help='Topic area (e.g., Alcoholism)')
    parser.add_argument('category', help='Mechanism category')
    parser.add_argument('--from-node', required=True, help='Source node')
    parser.add_argument('--to-node', required=True, help='Target node')

    # Optional arguments
    parser.add_argument('--context', help='Source context/literature')
    parser.add_argument('--context-file', help='File containing context')
    parser.add_argument('--output-dir', default='mechanism-bank/mechanisms', help='Output directory')
    parser.add_argument('--model', default='claude-3-5-sonnet-20241022', help='LLM model')
    parser.add_argument('--batch', help='CSV file with node pairs for batch extraction')

    args = parser.parse_args()

    # Load context
    if args.context_file:
        with open(args.context_file, 'r') as f:
            context = f.read()
    else:
        context = args.context or ""

    # Create config
    config = ExtractionConfig(
        topic=args.topic,
        category=args.category,
        source_context=context,
        output_dir=Path(args.output_dir),
        model=args.model
    )

    # Create extractor
    extractor = MechanismExtractor(config)

    # Single or batch extraction
    if args.batch:
        # Batch mode
        import csv
        with open(args.batch, 'r') as f:
            reader = csv.DictReader(f)
            node_pairs = [(row['from_node'], row['to_node']) for row in reader]

        print(f"Starting batch extraction of {len(node_pairs)} mechanisms...")

        def progress_callback(current, total):
            print(f"Progress: {current}/{total} ({current/total*100:.1f}%)")

        extractor.extract_batch(node_pairs, on_progress=progress_callback)

    else:
        # Single mode
        print(f"Extracting mechanism: {args.from_node} → {args.to_node}")
        mechanism = extractor.extract_single(args.from_node, args.to_node)

        if mechanism:
            print(f"✓ Success! Mechanism ID: {mechanism['id']}")
        else:
            print(f"✗ Extraction failed")
            sys.exit(1)

    # Print summary
    extractor.progress.print_summary()


if __name__ == "__main__":
    main()
