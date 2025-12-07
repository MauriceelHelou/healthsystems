#!/usr/bin/env python3
"""
Audit Node Coverage

Compares canonical node inventory against nodes actually used in mechanisms.
Identifies:
1. Canonical nodes used in mechanisms (coverage)
2. Canonical nodes NOT used (gaps)
3. Mechanism nodes NOT in canonical inventory (new/custom nodes)
"""

import json
import yaml
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
MECHANISMS_DIR = BASE_DIR / 'mechanism-bank' / 'mechanisms'
REPORT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_coverage_audit.json'


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case node ID."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def load_canonical_nodes():
    """Load canonical node inventory."""
    with open(CANONICAL_NODES_PATH, 'r') as f:
        data = json.load(f)
    return data['nodes'], data['by_id']


def extract_mechanism_nodes():
    """Extract all unique nodes from mechanisms."""
    nodes_used = defaultdict(lambda: {'count': 0, 'mechanisms': [], 'names': set()})

    for yaml_file in MECHANISMS_DIR.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                continue

            mech_id = data.get('id', yaml_file.stem)

            # Extract from_node
            from_node = data.get('from_node', {})
            from_id = normalize_node_id(from_node.get('node_id', ''))
            from_name = from_node.get('node_name', '')
            if from_id:
                nodes_used[from_id]['count'] += 1
                nodes_used[from_id]['mechanisms'].append(mech_id)
                if from_name:
                    nodes_used[from_id]['names'].add(from_name)

            # Extract to_node
            to_node = data.get('to_node', {})
            to_id = normalize_node_id(to_node.get('node_id', ''))
            to_name = to_node.get('node_name', '')
            if to_id:
                nodes_used[to_id]['count'] += 1
                nodes_used[to_id]['mechanisms'].append(mech_id)
                if to_name:
                    nodes_used[to_id]['names'].add(to_name)

        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    # Convert sets to lists for JSON serialization
    for node_id in nodes_used:
        nodes_used[node_id]['names'] = list(nodes_used[node_id]['names'])

    return dict(nodes_used)


def audit_coverage(canonical_nodes, canonical_by_id, mechanism_nodes):
    """Audit coverage between canonical and mechanism nodes."""

    canonical_ids = set(canonical_by_id.keys())
    mechanism_ids = set(mechanism_nodes.keys())

    # Nodes in both
    used_canonical = canonical_ids & mechanism_ids

    # Canonical nodes not used
    unused_canonical = canonical_ids - mechanism_ids

    # Mechanism nodes not in canonical (custom/new)
    custom_nodes = mechanism_ids - canonical_ids

    return {
        'used_canonical': used_canonical,
        'unused_canonical': unused_canonical,
        'custom_nodes': custom_nodes
    }


def main():
    print("=" * 70)
    print("NODE COVERAGE AUDIT")
    print("=" * 70)

    # Load data
    print("\n1. Loading canonical nodes...")
    canonical_nodes, canonical_by_id = load_canonical_nodes()
    print(f"   Canonical inventory: {len(canonical_nodes)} nodes")

    print("\n2. Extracting mechanism nodes...")
    mechanism_nodes = extract_mechanism_nodes()
    print(f"   Unique nodes in mechanisms: {len(mechanism_nodes)}")

    # Audit
    print("\n3. Auditing coverage...")
    audit = audit_coverage(canonical_nodes, canonical_by_id, mechanism_nodes)

    used = len(audit['used_canonical'])
    unused = len(audit['unused_canonical'])
    custom = len(audit['custom_nodes'])

    coverage_pct = used / len(canonical_nodes) * 100 if canonical_nodes else 0

    print(f"\n   RESULTS:")
    print(f"   - Canonical nodes USED in mechanisms: {used} ({coverage_pct:.1f}%)")
    print(f"   - Canonical nodes NOT used: {unused}")
    print(f"   - Custom nodes (not in canonical): {custom}")

    # Show top used nodes
    print("\n4. Top 20 most-used nodes:")
    sorted_nodes = sorted(mechanism_nodes.items(), key=lambda x: -x[1]['count'])
    for node_id, info in sorted_nodes[:20]:
        in_canonical = "✓" if node_id in canonical_by_id else "✗"
        names = ', '.join(info['names'][:2])
        print(f"   {in_canonical} {node_id}: {info['count']} uses ({names})")

    # Show custom nodes (not in canonical)
    print(f"\n5. Custom nodes NOT in canonical inventory ({custom} total):")
    custom_sorted = sorted(
        [(nid, mechanism_nodes[nid]) for nid in audit['custom_nodes']],
        key=lambda x: -x[1]['count']
    )
    for node_id, info in custom_sorted[:30]:
        names = ', '.join(info['names'][:1])
        print(f"   - {node_id}: {info['count']} uses ({names})")

    # Show unused canonical by domain
    print(f"\n6. Unused canonical nodes by domain:")
    unused_by_domain = defaultdict(list)
    for node_id in audit['unused_canonical']:
        node = canonical_by_id.get(node_id, {})
        domain = node.get('domain', 'Unknown')
        unused_by_domain[domain].append(node_id)

    for domain in sorted(unused_by_domain.keys(), key=lambda d: -len(unused_by_domain[d]))[:10]:
        count = len(unused_by_domain[domain])
        print(f"   {domain}: {count} unused nodes")

    # Save report
    report = {
        'summary': {
            'canonical_total': len(canonical_nodes),
            'mechanism_nodes_total': len(mechanism_nodes),
            'canonical_used': used,
            'canonical_unused': unused,
            'custom_nodes': custom,
            'coverage_pct': coverage_pct
        },
        'used_canonical_nodes': sorted(list(audit['used_canonical'])),
        'unused_canonical_nodes': sorted(list(audit['unused_canonical'])),
        'custom_nodes': [
            {
                'id': nid,
                'count': mechanism_nodes[nid]['count'],
                'names': mechanism_nodes[nid]['names']
            }
            for nid, _ in custom_sorted
        ],
        'unused_by_domain': {k: sorted(v) for k, v in unused_by_domain.items()}
    }

    REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n   Report saved: {REPORT_PATH}")

    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    print(f"""
1. NODE COVERAGE: {coverage_pct:.1f}% of canonical nodes are used
   - {used} nodes have supporting mechanisms
   - {unused} nodes have NO mechanisms yet

2. CUSTOM NODES: {custom} nodes in mechanisms are not in canonical inventory
   - Review these for potential addition to inventory
   - Or map them to existing canonical nodes

3. PRIORITY GAPS: Focus mechanism discovery on unused nodes in key domains
""")


if __name__ == "__main__":
    main()
