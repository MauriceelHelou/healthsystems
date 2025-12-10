#!/usr/bin/env python3
"""
Find and optionally remove mechanisms with insufficient study support.

This script scans all mechanism YAML files and reports those where:
- evidence.n_studies is 0, 1, or missing
- Default threshold: n_studies < 2 (configurable via --min-studies)

Usage:
    # Report mechanisms with n_studies <= 1 (default):
    python filter_single_study_mechanisms.py

    # Report mechanisms with fewer than 3 studies:
    python filter_single_study_mechanisms.py --min-studies 3

    # Delete weak-evidence mechanism files:
    python filter_single_study_mechanisms.py --delete

    # Custom output path:
    python filter_single_study_mechanisms.py --output custom_report.json
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict


def load_mechanisms(mechanism_dir: Path) -> List[Dict]:
    """Load all mechanisms from YAML files with file path metadata."""
    mechanisms = []

    for yaml_file in mechanism_dir.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            data['_file_path'] = str(yaml_file)
            data['_relative_path'] = str(yaml_file.relative_to(mechanism_dir))
            mechanisms.append(data)

        except Exception as e:
            print(f"Warning: Error loading mechanism {yaml_file}: {e}")

    return mechanisms


def get_n_studies(mech_data: Dict) -> int:
    """Extract n_studies from mechanism data. Returns 0 if missing."""
    evidence = mech_data.get('evidence', {})
    n_studies = evidence.get('n_studies')

    if n_studies is None:
        return 0
    if isinstance(n_studies, int):
        return n_studies
    if isinstance(n_studies, str):
        try:
            return int(n_studies)
        except ValueError:
            return 0
    return 0


def find_weak_evidence_mechanisms(
    mechanisms: List[Dict],
    min_studies: int = 2
) -> List[Dict]:
    """
    Find mechanisms with fewer than min_studies.

    Returns list of weak-evidence mechanism records with details.
    """
    weak = []

    for mech in mechanisms:
        n_studies = get_n_studies(mech)

        if n_studies < min_studies:
            evidence = mech.get('evidence', {})
            weak.append({
                'id': mech.get('id', 'unknown'),
                'file_path': mech.get('_file_path', ''),
                'relative_path': mech.get('_relative_path', ''),
                'n_studies': n_studies,
                'quality_rating': evidence.get('quality_rating', 'unknown'),
                'primary_citation': (evidence.get('primary_citation', '') or '')[:100],
                'category': mech.get('category', 'unknown'),
            })

    return weak


def print_report(
    total_mechanisms: int,
    weak: List[Dict],
    min_studies: int
):
    """Print formatted report to console."""
    print("=" * 70)
    print("WEAK EVIDENCE MECHANISMS REPORT")
    print("=" * 70)

    print(f"\nSUMMARY")
    print("-" * 40)
    print(f"Minimum studies threshold: {min_studies}")
    print(f"Total mechanisms scanned: {total_mechanisms}")
    print(f"Mechanisms with >= {min_studies} studies: {total_mechanisms - len(weak)}")
    print(f"Mechanisms with < {min_studies} studies: {len(weak)}")

    if not weak:
        print(f"\nAll mechanisms have at least {min_studies} studies!")
        return

    # Group by n_studies
    by_n_studies = defaultdict(list)
    for m in weak:
        by_n_studies[m['n_studies']].append(m)

    print(f"\nBREAKDOWN BY N_STUDIES")
    print("-" * 40)
    for n in sorted(by_n_studies.keys()):
        count = len(by_n_studies[n])
        pct = 100 * count / len(weak)
        print(f"  n_studies = {n}: {count:5d} ({pct:5.1f}%)")

    # Group by category
    by_category = defaultdict(int)
    for m in weak:
        by_category[m['category']] += 1

    print(f"\nBREAKDOWN BY CATEGORY")
    print("-" * 40)
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(weak)
        print(f"  {cat}: {count:5d} ({pct:5.1f}%)")

    print(f"\nWEAK EVIDENCE MECHANISMS")
    print("-" * 40)

    for m in weak[:50]:  # Show first 50
        print(f"\n  {m['id']}")
        print(f"    File: {m['relative_path']}")
        print(f"    n_studies: {m['n_studies']}, quality: {m['quality_rating']}")
        if m['primary_citation']:
            print(f"    Citation: {m['primary_citation'][:60]}...")

    if len(weak) > 50:
        print(f"\n  ... and {len(weak) - 50} more (see JSON report for full list)")


def delete_weak_files(weak: List[Dict]) -> List[str]:
    """Delete weak-evidence mechanism files. Returns list of deleted paths."""
    deleted = []

    for m in weak:
        file_path = m['file_path']
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted.append(file_path)
                print(f"  Deleted: {m['relative_path']}")
            except Exception as e:
                print(f"  Error deleting {file_path}: {e}")

    return deleted


def main():
    parser = argparse.ArgumentParser(
        description='Find mechanisms with insufficient study support'
    )
    parser.add_argument(
        '--min-studies',
        type=int,
        default=2,
        help='Minimum number of studies required (default: 2)'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete weak-evidence mechanism files (requires confirmation)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output JSON report path (default: backend/reports/weak_evidence_mechanisms.json)'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt when deleting'
    )

    args = parser.parse_args()

    # Set up paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    mechanism_dir = project_root / 'mechanism-bank' / 'mechanisms'

    # Default output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = script_dir.parent / 'reports' / 'weak_evidence_mechanisms.json'

    # Load mechanisms
    print(f"Loading mechanisms from: {mechanism_dir}")
    mechanisms = load_mechanisms(mechanism_dir)
    print(f"Found {len(mechanisms)} mechanism files")

    # Find weak-evidence mechanisms
    weak = find_weak_evidence_mechanisms(mechanisms, args.min_studies)

    # Print report
    print_report(len(mechanisms), weak, args.min_studies)

    # Save JSON report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        'generated_at': datetime.now().isoformat(),
        'min_studies_threshold': args.min_studies,
        'summary': {
            'total_mechanisms': len(mechanisms),
            'weak_evidence_count': len(weak),
            'sufficient_evidence_count': len(mechanisms) - len(weak),
        },
        'weak_evidence_mechanisms': weak,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report saved to: {output_path}")

    # Delete if requested
    if args.delete and weak:
        print(f"\n{'=' * 70}")
        print(f"DELETE CONFIRMATION")
        print(f"{'=' * 70}")
        print(f"\nAbout to delete {len(weak)} mechanism files with < {args.min_studies} studies.")

        if not args.yes:
            response = input("Are you sure? (yes/no): ")
            if response.lower() != 'yes':
                print("Deletion cancelled.")
                return

        print("\nDeleting files...")
        deleted = delete_weak_files(weak)
        print(f"\nDeleted {len(deleted)} files.")

        # Update report with deleted files
        report['deleted_files'] = deleted
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
