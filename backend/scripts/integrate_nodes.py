#!/usr/bin/env python3
"""
Node Integration Script

Compares mechanism nodes to canonical inventory and generates:
1. Exact matches - keep as-is
2. Near matches - suggest merge
3. New nodes - suggest addition to inventory
"""

import re
import json
import yaml
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

BASE_DIR = Path(__file__).parent.parent.parent
CONSOLIDATED_DIR = BASE_DIR / 'mechanism-bank' / 'consolidated'
CANONICAL_NODES_PATH = BASE_DIR / 'backend' / 'data' / 'canonical_nodes.json'
REPORT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_integration_report.json'


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def load_canonical_nodes():
    """Load canonical nodes."""
    with open(CANONICAL_NODES_PATH, 'r') as f:
        data = json.load(f)
    return data['nodes'], data['by_id']


def load_mechanism_nodes():
    """Extract all unique nodes from consolidated mechanisms."""
    nodes = {}

    for yaml_file in CONSOLIDATED_DIR.rglob('*.yaml'):
        if yaml_file.name == 'canonical_nodes.json':
            continue
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                continue

            # Extract from_node
            from_node = data.get('from_node', {})
            from_id = from_node.get('node_id', '')
            from_name = from_node.get('node_name', '')
            if from_id or from_name:
                key = normalize(from_id or from_name)
                if key not in nodes:
                    nodes[key] = {
                        'id': from_id,
                        'name': from_name,
                        'normalized': key,
                        'occurrences': 0,
                        'type': 'from',
                    }
                nodes[key]['occurrences'] += 1

            # Extract to_node
            to_node = data.get('to_node', {})
            to_id = to_node.get('node_id', '')
            to_name = to_node.get('node_name', '')
            if to_id or to_name:
                key = normalize(to_id or to_name)
                if key not in nodes:
                    nodes[key] = {
                        'id': to_id,
                        'name': to_name,
                        'normalized': key,
                        'occurrences': 0,
                        'type': 'to',
                    }
                nodes[key]['occurrences'] += 1

        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return nodes


def find_matches(mech_nodes: dict, canonical_nodes: list, by_id: dict):
    """Find exact and near matches for mechanism nodes."""

    exact_matches = []
    near_matches = []
    new_nodes = []

    canonical_ids = set(by_id.keys())
    canonical_names = {n['name'].lower(): n for n in canonical_nodes}

    for key, node in mech_nodes.items():
        normalized_id = node['normalized']
        name = node.get('name', '')

        # Check exact ID match
        if normalized_id in canonical_ids:
            exact_matches.append({
                'mechanism_node': node,
                'canonical_node': by_id[normalized_id],
                'match_type': 'exact_id',
            })
            continue

        # Check exact name match
        if name.lower() in canonical_names:
            exact_matches.append({
                'mechanism_node': node,
                'canonical_node': canonical_names[name.lower()],
                'match_type': 'exact_name',
            })
            continue

        # Find best fuzzy match
        best_match = None
        best_score = 0

        for canon in canonical_nodes:
            # Compare IDs
            id_score = similarity(normalized_id, canon['id'])
            if id_score > best_score:
                best_score = id_score
                best_match = canon

            # Compare names
            if name:
                name_score = similarity(name, canon['name'])
                if name_score > best_score:
                    best_score = name_score
                    best_match = canon

        if best_score >= 0.7:
            near_matches.append({
                'mechanism_node': node,
                'canonical_node': best_match,
                'similarity': best_score,
            })
        else:
            new_nodes.append({
                'mechanism_node': node,
                'best_match': best_match,
                'best_similarity': best_score,
            })

    return exact_matches, near_matches, new_nodes


def main():
    print("=" * 70)
    print("NODE INTEGRATION ANALYSIS")
    print("=" * 70)

    # Load data
    print("\n1. Loading canonical nodes...")
    canonical_nodes, by_id = load_canonical_nodes()
    print(f"   Canonical nodes: {len(canonical_nodes)}")

    print("\n2. Loading mechanism nodes...")
    mech_nodes = load_mechanism_nodes()
    print(f"   Unique mechanism nodes: {len(mech_nodes)}")

    # Find matches
    print("\n3. Finding matches...")
    exact, near, new = find_matches(mech_nodes, canonical_nodes, by_id)

    print(f"   Exact matches: {len(exact)}")
    print(f"   Near matches (≥70% similar): {len(near)}")
    print(f"   New nodes: {len(new)}")

    # Coverage
    total = len(mech_nodes)
    coverage = (len(exact) + len(near)) / total * 100 if total > 0 else 0
    print(f"\n   Coverage: {coverage:.1f}%")

    # Show near matches for review
    print("\n4. Near matches (suggest merge):")
    for m in sorted(near, key=lambda x: -x['similarity'])[:15]:
        mech = m['mechanism_node']
        canon = m['canonical_node']
        print(f"   - '{mech['name']}' → '{canon['name']}' ({m['similarity']:.0%})")

    # Show new nodes
    print(f"\n5. New nodes ({len(new)} total, showing top by occurrence):")
    new_sorted = sorted(new, key=lambda x: -x['mechanism_node']['occurrences'])
    for n in new_sorted[:20]:
        node = n['mechanism_node']
        best = n['best_match']
        print(f"   - '{node['name']}' (used {node['occurrences']}x)")
        if best:
            print(f"     Closest: '{best['name']}' ({n['best_similarity']:.0%})")

    # Save report
    report = {
        'summary': {
            'canonical_nodes': len(canonical_nodes),
            'mechanism_nodes': len(mech_nodes),
            'exact_matches': len(exact),
            'near_matches': len(near),
            'new_nodes': len(new),
            'coverage_pct': coverage,
        },
        'exact_matches': [
            {
                'mechanism': m['mechanism_node']['name'],
                'canonical': m['canonical_node']['name'],
                'match_type': m['match_type'],
            }
            for m in exact
        ],
        'near_matches': [
            {
                'mechanism': m['mechanism_node']['name'],
                'canonical': m['canonical_node']['name'],
                'similarity': m['similarity'],
            }
            for m in sorted(near, key=lambda x: -x['similarity'])
        ],
        'new_nodes': [
            {
                'name': n['mechanism_node']['name'],
                'id': n['mechanism_node']['normalized'],
                'occurrences': n['mechanism_node']['occurrences'],
                'closest_match': n['best_match']['name'] if n['best_match'] else None,
                'similarity': n['best_similarity'],
            }
            for n in new_sorted
        ],
    }

    REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n   Report saved: {REPORT_PATH}")

    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    print(f"""
1. MERGE NEAR MATCHES: {len(near)} nodes should be mapped to canonical IDs
   - Review node_integration_report.json for suggested mappings

2. ADD NEW NODES: {len(new)} nodes need to be added to inventory
   - Review for redundancy first
   - Add to COMPLETE_NODE_INVENTORY.md

3. UPDATE EXTRACTION PROMPT:
   - Include canonical node list
   - Require matching or explicit "new node" proposal
""")


if __name__ == "__main__":
    main()
