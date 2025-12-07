#!/usr/bin/env python3
"""
Track New Mechanisms Utility

Lists and summarizes mechanisms added/modified within a given time period.
Useful for tracking batch discovery results and monitoring mechanism bank changes.

Usage:
    python backend/scripts/track_new_mechanisms.py                    # Last 24 hours
    python backend/scripts/track_new_mechanisms.py --hours 48         # Last 48 hours
    python backend/scripts/track_new_mechanisms.py --since 2025-12-06 # Since specific date
    python backend/scripts/track_new_mechanisms.py --output report.json # Save to JSON
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def list_new_mechanisms(
    mechanism_dir: Path,
    since: datetime,
    include_content: bool = False
) -> List[Dict]:
    """
    List mechanism files modified since a given datetime.

    Args:
        mechanism_dir: Path to mechanism-bank/mechanisms
        since: Cutoff datetime
        include_content: If True, include full YAML content

    Returns:
        List of mechanism file info dicts
    """
    new_files = []

    for yaml_file in mechanism_dir.rglob("*.yaml"):
        try:
            mtime = datetime.fromtimestamp(yaml_file.stat().st_mtime)
            if mtime > since:
                info = {
                    "file": str(yaml_file.relative_to(mechanism_dir)),
                    "category": yaml_file.parent.name,
                    "mechanism_id": yaml_file.stem,
                    "modified": mtime.isoformat(),
                    "size_bytes": yaml_file.stat().st_size
                }

                if include_content:
                    try:
                        import yaml
                        with open(yaml_file, 'r', encoding='utf-8') as f:
                            info["content"] = yaml.safe_load(f)
                    except Exception as e:
                        info["content_error"] = str(e)

                new_files.append(info)
        except Exception as e:
            print(f"Warning: Could not process {yaml_file}: {e}", file=sys.stderr)

    return sorted(new_files, key=lambda x: x["modified"], reverse=True)


def summarize_by_category(mechanisms: List[Dict]) -> Dict[str, int]:
    """Summarize mechanism counts by category."""
    counts = defaultdict(int)
    for m in mechanisms:
        counts[m["category"]] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def get_mechanism_stats(mechanisms: List[Dict]) -> Dict:
    """Calculate statistics for mechanisms."""
    if not mechanisms:
        return {
            "total": 0,
            "by_category": {},
            "earliest": None,
            "latest": None,
            "total_size_kb": 0
        }

    times = [datetime.fromisoformat(m["modified"]) for m in mechanisms]

    return {
        "total": len(mechanisms),
        "by_category": summarize_by_category(mechanisms),
        "earliest": min(times).isoformat(),
        "latest": max(times).isoformat(),
        "total_size_kb": sum(m["size_bytes"] for m in mechanisms) / 1024
    }


def print_summary(mechanisms: List[Dict], since: datetime):
    """Print a human-readable summary."""
    stats = get_mechanism_stats(mechanisms)

    print("\n" + "=" * 60)
    print("MECHANISM TRACKING REPORT")
    print("=" * 60)
    print(f"Time Range: {since.strftime('%Y-%m-%d %H:%M')} to {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Total New/Modified: {stats['total']} mechanisms")
    print(f"Total Size: {stats['total_size_kb']:.1f} KB")

    if stats["by_category"]:
        print("\nBy Category:")
        for category, count in stats["by_category"].items():
            print(f"  {category}: {count}")

    if mechanisms:
        print("\nMost Recent 10:")
        for m in mechanisms[:10]:
            print(f"  - [{m['category']}] {m['mechanism_id']}")
            print(f"    Modified: {m['modified']}")

    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Track new and modified mechanisms in the mechanism bank",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Show mechanisms from last 24 hours
  %(prog)s --hours 48                # Last 48 hours
  %(prog)s --since 2025-12-06        # Since specific date
  %(prog)s --output report.json      # Export to JSON
  %(prog)s --category political      # Filter by category
  %(prog)s --list-all                # List all mechanism filenames
        """
    )

    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Look back N hours (default: 24)"
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Look back since date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
    )
    parser.add_argument(
        "--mechanism-dir",
        type=Path,
        default=Path("mechanism-bank/mechanisms"),
        help="Path to mechanism bank directory"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file path"
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Filter by category (e.g., 'political', 'behavioral')"
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all mechanism filenames (one per line)"
    )
    parser.add_argument(
        "--include-content",
        action="store_true",
        help="Include full YAML content in output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON (to stdout)"
    )

    args = parser.parse_args()

    # Determine cutoff time
    if args.since:
        try:
            if " " in args.since:
                since = datetime.strptime(args.since, "%Y-%m-%d %H:%M")
            else:
                since = datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format '{args.since}'. Use YYYY-MM-DD or YYYY-MM-DD HH:MM", file=sys.stderr)
            sys.exit(1)
    else:
        since = datetime.now() - timedelta(hours=args.hours)

    # Check mechanism directory exists
    if not args.mechanism_dir.exists():
        print(f"Error: Mechanism directory not found: {args.mechanism_dir}", file=sys.stderr)
        sys.exit(1)

    # Get mechanisms
    mechanisms = list_new_mechanisms(
        args.mechanism_dir,
        since,
        include_content=args.include_content
    )

    # Filter by category if specified
    if args.category:
        mechanisms = [m for m in mechanisms if m["category"] == args.category]

    # Output
    if args.list_all:
        for m in mechanisms:
            print(m["file"])
    elif args.json:
        output = {
            "query": {
                "since": since.isoformat(),
                "category_filter": args.category,
                "mechanism_dir": str(args.mechanism_dir)
            },
            "stats": get_mechanism_stats(mechanisms),
            "mechanisms": mechanisms
        }
        print(json.dumps(output, indent=2))
    elif args.output:
        output = {
            "query": {
                "since": since.isoformat(),
                "category_filter": args.category,
                "generated": datetime.now().isoformat()
            },
            "stats": get_mechanism_stats(mechanisms),
            "mechanisms": mechanisms
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Report saved to: {args.output}")
        print_summary(mechanisms, since)
    else:
        print_summary(mechanisms, since)


if __name__ == "__main__":
    main()
