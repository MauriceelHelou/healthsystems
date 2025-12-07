#!/usr/bin/env python3
"""
Run Node-Pair Driven Discovery

This script runs the V4 node-pair discovery pipeline for a specific topic config.

Usage:
    python backend/scripts/run_node_pair_discovery.py --config backend/configs/alcohol_node_pairs.json
    python backend/scripts/run_node_pair_discovery.py --config backend/configs/alcohol_node_pairs.json --dry-run
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.node_pair_discovery import NodePairDiscovery


def main():
    parser = argparse.ArgumentParser(
        description="Run Node-Pair Driven Discovery Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run to see what would be processed
    python backend/scripts/run_node_pair_discovery.py \\
        --config backend/configs/alcohol_node_pairs.json \\
        --dry-run

    # Full run with paper search
    python backend/scripts/run_node_pair_discovery.py \\
        --config backend/configs/alcohol_node_pairs.json

    # Run with cached papers (skip search)
    python backend/scripts/run_node_pair_discovery.py \\
        --config backend/configs/alcohol_node_pairs.json \\
        --no-search \\
        --cache backend/data/alcohol_papers.json
"""
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to node pairs config JSON"
    )
    parser.add_argument(
        "--output",
        default="mechanism-bank/mechanisms",
        help="Output directory for mechanisms (default: mechanism-bank/mechanisms)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't submit batch, just show stats"
    )
    parser.add_argument(
        "--no-search",
        action="store_true",
        help="Skip paper search, require --cache"
    )
    parser.add_argument(
        "--cache",
        help="Path to cached papers JSON"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Validate
    if args.no_search and not args.cache:
        parser.error("--no-search requires --cache")

    if not Path(args.config).exists():
        parser.error(f"Config file not found: {args.config}")

    # Check environment variables
    required_env = ["ANTHROPIC_API_KEY"]
    if not args.dry_run and not args.no_search:
        required_env.append("PUBMED_EMAIL")

    missing = [v for v in required_env if not os.getenv(v)]
    if missing:
        print(f"ERROR: Missing required environment variables: {missing}")
        print("\nSet them with:")
        for v in missing:
            print(f"  export {v}=your_value")
        sys.exit(1)

    print("=" * 60)
    print("NODE-PAIR DRIVEN DISCOVERY PIPELINE V4")
    print("=" * 60)
    print(f"\nConfig: {args.config}")
    print(f"Output: {args.output}")
    print(f"Dry run: {args.dry_run}")
    print(f"Search papers: {not args.no_search}")
    if args.cache:
        print(f"Papers cache: {args.cache}")
    print()

    # Run discovery
    discovery = NodePairDiscovery(
        pubmed_email=os.getenv("PUBMED_EMAIL"),
        semantic_scholar_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    )

    report = discovery.discover_mechanisms(
        config_path=args.config,
        output_dir=args.output,
        search_papers=not args.no_search,
        papers_cache=args.cache,
        dry_run=args.dry_run
    )

    print("\n" + "=" * 60)
    print("DISCOVERY REPORT")
    print("=" * 60)
    for key, value in report.items():
        print(f"  {key}: {value}")

    if args.dry_run:
        print("\n[DRY RUN - No mechanisms saved]")
    else:
        print(f"\nMechanisms saved to: {args.output}")


if __name__ == "__main__":
    main()
