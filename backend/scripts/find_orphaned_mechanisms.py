#!/usr/bin/env python3
"""
Find mechanisms that reference nodes NOT defined in nodes/by_scale/.

This script scans all mechanism YAML files and reports those where:
- from_node.node_id doesn't exist in nodes/by_scale/
- to_node.node_id doesn't exist in nodes/by_scale/
- Either node has a NEW: prefix (proposed/candidate nodes)

Usage:
    # Report only (no changes):
    python find_orphaned_mechanisms.py

    # Delete orphaned mechanism files:
    python find_orphaned_mechanisms.py --delete

    # Custom output path:
    python find_orphaned_mechanisms.py --output custom_report.json
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime


def load_valid_node_ids(nodes_dir: Path) -> Set[str]:
    """
    Load all valid node IDs from nodes/by_scale/ directory.

    Returns set of node_id strings.
    """
    valid_ids = set()

    if not nodes_dir.exists():
        print(f"Error: Nodes directory not found: {nodes_dir}")
        return valid_ids

    for yaml_file in nodes_dir.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            # Node ID is typically the 'id' field or derived from filename
            node_id = data.get('id') or data.get('node_id')
            if node_id:
                valid_ids.add(node_id)
            else:
                # Fallback: use filename without extension
                valid_ids.add(yaml_file.stem)

        except Exception as e:
            print(f"Warning: Error loading node file {yaml_file}: {e}")

    return valid_ids


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


def extract_node_ids(mech_data: Dict) -> Tuple[str, str]:
    """
    Extract from_node_id and to_node_id from mechanism data.

    Returns tuple of (from_node_id, to_node_id).
    """
    from_node = mech_data.get('from_node', {})
    to_node = mech_data.get('to_node', {})

    from_node_id = from_node.get('node_id', '')
    to_node_id = to_node.get('node_id', '')

    # Fallback: parse from mechanism ID if structured data missing
    if not from_node_id or not to_node_id:
        mech_id = mech_data.get('id', '')
        if '_to_' in mech_id:
            parts = mech_id.split('_to_')
            from_node_id = from_node_id or parts[0]
            to_node_id = to_node_id or '_to_'.join(parts[1:])

    return from_node_id, to_node_id


def find_orphaned_mechanisms(
    mechanisms: List[Dict],
    valid_node_ids: Set[str]
) -> List[Dict]:
    """
    Find mechanisms that reference nodes not in valid_node_ids.

    Returns list of orphaned mechanism records with details.
    """
    orphaned = []

    for mech in mechanisms:
        from_node_id, to_node_id = extract_node_ids(mech)

        missing_from = False
        missing_to = False
        has_new_prefix = False

        # Check for NEW: prefix
        if 'NEW:' in from_node_id or 'NEW:' in to_node_id:
            has_new_prefix = True

        # Check if nodes exist
        if from_node_id and from_node_id not in valid_node_ids:
            missing_from = True
        if to_node_id and to_node_id not in valid_node_ids:
            missing_to = True

        if missing_from or missing_to or has_new_prefix:
            orphaned.append({
                'id': mech.get('id', 'unknown'),
                'file_path': mech.get('_file_path', ''),
                'relative_path': mech.get('_relative_path', ''),
                'from_node_id': from_node_id,
                'to_node_id': to_node_id,
                'missing_from_node': missing_from,
                'missing_to_node': missing_to,
                'has_new_prefix': has_new_prefix,
            })

    return orphaned


def print_report(
    total_mechanisms: int,
    orphaned: List[Dict],
    valid_node_count: int
):
    """Print formatted report to console."""
    print("=" * 70)
    print("ORPHANED MECHANISMS REPORT")
    print("=" * 70)

    print(f"\nSUMMARY")
    print("-" * 40)
    print(f"Valid nodes in nodes/by_scale/: {valid_node_count}")
    print(f"Total mechanisms scanned: {total_mechanisms}")
    print(f"Mechanisms with valid nodes: {total_mechanisms - len(orphaned)}")
    print(f"Mechanisms with orphaned nodes: {len(orphaned)}")

    if not orphaned:
        print("\nAll mechanisms reference valid nodes!")
        return

    # Categorize orphaned mechanisms
    new_prefix = [m for m in orphaned if m['has_new_prefix']]
    missing_from = [m for m in orphaned if m['missing_from_node'] and not m['has_new_prefix']]
    missing_to = [m for m in orphaned if m['missing_to_node'] and not m['has_new_prefix']]

    print(f"\nBREAKDOWN")
    print("-" * 40)
    print(f"With NEW: prefix (proposed nodes): {len(new_prefix)}")
    print(f"Missing from_node: {len(missing_from)}")
    print(f"Missing to_node: {len(missing_to)}")

    print(f"\nORPHANED MECHANISMS")
    print("-" * 40)

    for m in orphaned[:50]:  # Show first 50
        print(f"\n  {m['id']}")
        print(f"    File: {m['relative_path']}")
        if m['has_new_prefix']:
            print(f"    Issue: Contains NEW: prefix (proposed node)")
        if m['missing_from_node']:
            print(f"    Missing from_node: {m['from_node_id']}")
        if m['missing_to_node']:
            print(f"    Missing to_node: {m['to_node_id']}")

    if len(orphaned) > 50:
        print(f"\n  ... and {len(orphaned) - 50} more (see JSON report for full list)")


def delete_orphaned_files(orphaned: List[Dict]) -> List[str]:
    """Delete orphaned mechanism files. Returns list of deleted paths."""
    deleted = []

    for m in orphaned:
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
        description='Find mechanisms referencing nodes not in nodes/by_scale/'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete orphaned mechanism files (requires confirmation)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output JSON report path (default: backend/reports/orphaned_mechanisms.json)'
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
    nodes_dir = project_root / 'nodes' / 'by_scale'
    mechanism_dir = project_root / 'mechanism-bank' / 'mechanisms'

    # Default output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = script_dir.parent / 'reports' / 'orphaned_mechanisms.json'

    # Load valid nodes
    print(f"Loading nodes from: {nodes_dir}")
    valid_node_ids = load_valid_node_ids(nodes_dir)
    print(f"Found {len(valid_node_ids)} valid node IDs")

    # Load mechanisms
    print(f"Loading mechanisms from: {mechanism_dir}")
    mechanisms = load_mechanisms(mechanism_dir)
    print(f"Found {len(mechanisms)} mechanism files")

    # Find orphaned
    orphaned = find_orphaned_mechanisms(mechanisms, valid_node_ids)

    # Print report
    print_report(len(mechanisms), orphaned, len(valid_node_ids))

    # Save JSON report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'valid_nodes_count': len(valid_node_ids),
            'total_mechanisms': len(mechanisms),
            'orphaned_count': len(orphaned),
            'valid_count': len(mechanisms) - len(orphaned),
        },
        'orphaned_mechanisms': orphaned,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report saved to: {output_path}")

    # Delete if requested
    if args.delete and orphaned:
        print(f"\n{'=' * 70}")
        print(f"DELETE CONFIRMATION")
        print(f"{'=' * 70}")
        print(f"\nAbout to delete {len(orphaned)} mechanism files.")

        if not args.yes:
            response = input("Are you sure? (yes/no): ")
            if response.lower() != 'yes':
                print("Deletion cancelled.")
                return

        print("\nDeleting files...")
        deleted = delete_orphaned_files(orphaned)
        print(f"\nDeleted {len(deleted)} files.")

        # Update report with deleted files
        report['deleted_files'] = deleted
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
