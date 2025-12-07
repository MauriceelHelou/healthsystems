#!/usr/bin/env python3
"""
Map Mechanism Nodes to Canonical Inventory

Uses fuzzy matching to map custom node IDs in mechanisms to canonical inventory.
Updates mechanism files with canonical node IDs where matches are found.
"""

import json
import yaml
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
MECHANISMS_DIR = BASE_DIR / 'mechanism-bank' / 'mechanisms'
MAPPING_REPORT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_mapping_report.json'


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def load_canonical_nodes():
    """Load canonical inventory."""
    with open(CANONICAL_NODES_PATH, 'r') as f:
        data = json.load(f)
    return data['nodes'], data['by_id']


def find_best_canonical_match(node_id: str, node_name: str, canonical_nodes: list, canonical_by_id: dict, threshold: float = 0.6):
    """Find the best matching canonical node."""

    # Exact ID match
    if node_id in canonical_by_id:
        return canonical_by_id[node_id], 1.0, 'exact_id'

    normalized_id = normalize_node_id(node_id)
    if normalized_id in canonical_by_id:
        return canonical_by_id[normalized_id], 1.0, 'normalized_id'

    # Exact name match
    for canon in canonical_nodes:
        if node_name.lower() == canon['name'].lower():
            return canon, 1.0, 'exact_name'

    # Fuzzy matching
    best_match = None
    best_score = 0

    for canon in canonical_nodes:
        # Match by ID
        id_score = similarity(normalized_id, canon['id'])
        if id_score > best_score:
            best_score = id_score
            best_match = canon

        # Match by name
        if node_name:
            name_score = similarity(node_name, canon['name'])
            if name_score > best_score:
                best_score = name_score
                best_match = canon

    if best_score >= threshold:
        return best_match, best_score, 'fuzzy'

    return None, 0, 'no_match'


def build_node_mapping(mechanisms_dir: Path, canonical_nodes: list, canonical_by_id: dict):
    """Build mapping from mechanism nodes to canonical nodes."""

    # Collect all unique nodes from mechanisms
    mech_nodes = {}

    for yaml_file in mechanisms_dir.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                continue

            for node_key in ['from_node', 'to_node']:
                node = data.get(node_key, {})
                node_id = node.get('node_id', '')
                node_name = node.get('node_name', '')

                if node_id and node_id not in mech_nodes:
                    mech_nodes[node_id] = {
                        'id': node_id,
                        'name': node_name,
                        'files': []
                    }
                if node_id:
                    mech_nodes[node_id]['files'].append(str(yaml_file))

        except Exception as e:
            print(f"Error reading {yaml_file}: {e}")

    # Find matches for each node
    mappings = {
        'exact': [],
        'fuzzy': [],
        'no_match': []
    }

    node_to_canonical = {}

    for node_id, info in mech_nodes.items():
        match, score, match_type = find_best_canonical_match(
            node_id, info['name'], canonical_nodes, canonical_by_id
        )

        if match:
            entry = {
                'original_id': node_id,
                'original_name': info['name'],
                'canonical_id': match['id'],
                'canonical_name': match['name'],
                'score': score,
                'file_count': len(info['files'])
            }

            if match_type in ['exact_id', 'normalized_id', 'exact_name']:
                mappings['exact'].append(entry)
            else:
                mappings['fuzzy'].append(entry)

            node_to_canonical[node_id] = match
        else:
            mappings['no_match'].append({
                'original_id': node_id,
                'original_name': info['name'],
                'file_count': len(info['files'])
            })

    return mappings, node_to_canonical


def update_mechanism_files(mechanisms_dir: Path, node_to_canonical: dict, dry_run: bool = False):
    """Update mechanism files with canonical node IDs."""

    updated_count = 0

    for yaml_file in mechanisms_dir.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                continue

            modified = False

            for node_key in ['from_node', 'to_node']:
                node = data.get(node_key, {})
                node_id = node.get('node_id', '')

                if node_id in node_to_canonical:
                    canonical = node_to_canonical[node_id]
                    if node_id != canonical['id']:
                        node['node_id'] = canonical['id']
                        node['node_name'] = canonical['name']
                        node['_original_id'] = node_id  # Keep reference
                        modified = True

            # Update mechanism ID if nodes changed
            if modified:
                from_id = data.get('from_node', {}).get('node_id', '')
                to_id = data.get('to_node', {}).get('node_id', '')
                if from_id and to_id:
                    data['id'] = f"{from_id}_to_{to_id}"
                    data['name'] = f"{data.get('from_node', {}).get('node_name', '')} → {data.get('to_node', {}).get('node_name', '')}"

                if not dry_run:
                    with open(yaml_file, 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

                updated_count += 1

        except Exception as e:
            print(f"Error updating {yaml_file}: {e}")

    return updated_count


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Map mechanism nodes to canonical inventory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    parser.add_argument('--threshold', type=float, default=0.6, help='Minimum similarity threshold for fuzzy matching')
    args = parser.parse_args()

    print("=" * 70)
    print("NODE MAPPING TO CANONICAL INVENTORY")
    print("=" * 70)

    # Load canonical nodes
    print("\n1. Loading canonical inventory...")
    canonical_nodes, canonical_by_id = load_canonical_nodes()
    print(f"   Canonical nodes: {len(canonical_nodes)}")

    # Build mappings
    print("\n2. Building node mappings...")
    mappings, node_to_canonical = build_node_mapping(
        MECHANISMS_DIR, canonical_nodes, canonical_by_id
    )

    exact_count = len(mappings['exact'])
    fuzzy_count = len(mappings['fuzzy'])
    no_match_count = len(mappings['no_match'])
    total = exact_count + fuzzy_count + no_match_count

    print(f"\n   MAPPING RESULTS:")
    print(f"   - Exact matches: {exact_count}")
    print(f"   - Fuzzy matches (≥{args.threshold*100:.0f}%): {fuzzy_count}")
    print(f"   - No match: {no_match_count}")
    print(f"   - Total unique nodes: {total}")

    # Show fuzzy matches for review
    print("\n3. Fuzzy matches (review these):")
    for m in sorted(mappings['fuzzy'], key=lambda x: -x['score'])[:20]:
        print(f"   '{m['original_id']}' → '{m['canonical_id']}' ({m['score']:.0%})")

    # Show nodes with no match
    print(f"\n4. Nodes with NO canonical match ({no_match_count}):")
    for m in sorted(mappings['no_match'], key=lambda x: -x['file_count'])[:20]:
        print(f"   - {m['original_id']}: {m['original_name']} ({m['file_count']} files)")

    # Update files
    if args.dry_run:
        print("\n5. [DRY RUN] Would update mechanism files...")
    else:
        print("\n5. Updating mechanism files...")

    updated = update_mechanism_files(MECHANISMS_DIR, node_to_canonical, dry_run=args.dry_run)
    print(f"   {'Would update' if args.dry_run else 'Updated'}: {updated} mechanism files")

    # Save report
    report = {
        'summary': {
            'total_nodes': total,
            'exact_matches': exact_count,
            'fuzzy_matches': fuzzy_count,
            'no_match': no_match_count,
            'threshold': args.threshold,
            'files_updated': updated
        },
        'exact_mappings': mappings['exact'],
        'fuzzy_mappings': sorted(mappings['fuzzy'], key=lambda x: -x['score']),
        'no_match': sorted(mappings['no_match'], key=lambda x: -x['file_count'])
    }

    MAPPING_REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(MAPPING_REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n   Report saved: {MAPPING_REPORT_PATH}")

    if not args.dry_run:
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print(f"""
1. Review fuzzy mappings in the report for accuracy
2. For nodes with no match, consider:
   - Adding them to canonical inventory
   - Manually mapping to existing nodes
3. Re-run node coverage audit to verify improvement
""")


if __name__ == "__main__":
    main()
