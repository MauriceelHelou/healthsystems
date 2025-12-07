#!/usr/bin/env python3
"""
Rebuild Node Index

Reads all individual YAML node files and regenerates:
1. nodes/canonical_nodes.json - Machine-readable index
2. nodes/INDEX.md - Human-readable index by scale/domain

Run after generating or modifying node YAML files.
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
NODES_DIR = BASE_DIR / 'nodes' / 'by_scale'
CANONICAL_OUTPUT = BASE_DIR / 'nodes' / 'canonical_nodes.json'
INDEX_OUTPUT = BASE_DIR / 'nodes' / 'INDEX.md'

# Scale names for documentation (1-7 scale per NODE_SYSTEM_DEFINITIONS.md)
SCALE_NAMES = {
    1: 'Structural Determinants (Federal/State Policy)',
    2: 'Built Environment & Infrastructure',
    3: 'Institutional Infrastructure',
    4: 'Individual/Household Conditions',
    5: 'Individual Behaviors & Psychosocial',
    6: 'Intermediate Pathways',
    7: 'Crisis Endpoints'
}


def load_all_nodes() -> list:
    """Load all node YAML files from by_scale directories."""
    nodes = []

    for yaml_file in NODES_DIR.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                node = yaml.safe_load(f)
            if node and 'id' in node:
                node['_source_file'] = str(yaml_file.relative_to(BASE_DIR))
                nodes.append(node)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return nodes


def build_canonical_json(nodes: list) -> dict:
    """Build the canonical_nodes.json structure."""
    # Sort by scale, then by id
    sorted_nodes = sorted(nodes, key=lambda n: (n.get('scale', 4), n.get('id', '')))

    # Build lookup structures
    by_id = {}
    by_scale = defaultdict(list)
    by_domain = defaultdict(list)

    for i, node in enumerate(sorted_nodes, 1):
        node_id = node.get('id', '')
        scale = node.get('scale', 4)
        domain = node.get('domain', 'Unknown')

        # Simplified node for the main list
        simple_node = {
            'number': i,
            'id': node_id,
            'name': node.get('name', node_id.replace('_', ' ').title()),
            'scale': scale,
            'domain': domain,
            'type': node.get('type', 'Unknown'),
            'unit': node.get('stock', {}).get('unit', 'TBD')
        }

        by_id[node_id] = simple_node
        by_scale[str(scale)].append(node_id)
        by_domain[domain].append(node_id)

    return {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source': 'nodes/by_scale/*.yaml',
            'total_nodes': len(sorted_nodes),
            'scales': {str(k): v for k, v in SCALE_NAMES.items()}
        },
        'nodes': [by_id[n['id']] for n in sorted_nodes],
        'by_id': by_id,
        'by_scale': dict(by_scale),
        'by_domain': dict(by_domain)
    }


def build_index_markdown(nodes: list) -> str:
    """Build the INDEX.md content."""
    lines = [
        "# Node Inventory Index",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Total Nodes:** {len(nodes)}",
        "",
        "---",
        "",
        "## By Scale",
        ""
    ]

    # Group by scale
    by_scale = defaultdict(list)
    for node in nodes:
        scale = node.get('scale', 4)
        by_scale[scale].append(node)

    for scale in sorted(by_scale.keys()):
        scale_name = SCALE_NAMES.get(scale, f'Scale {scale}')
        scale_nodes = sorted(by_scale[scale], key=lambda n: n.get('id', ''))

        lines.append(f"### Scale {scale}: {scale_name}")
        lines.append(f"*{len(scale_nodes)} nodes*")
        lines.append("")

        for node in scale_nodes:
            node_id = node.get('id', '')
            name = node.get('name', node_id)
            domain = node.get('domain', 'Unknown')
            lines.append(f"- `{node_id}` - {name} ({domain})")

        lines.append("")

    # Group by domain
    lines.extend([
        "---",
        "",
        "## By Domain",
        ""
    ])

    by_domain = defaultdict(list)
    for node in nodes:
        domain = node.get('domain', 'Unknown')
        by_domain[domain].append(node)

    for domain in sorted(by_domain.keys()):
        domain_nodes = sorted(by_domain[domain], key=lambda n: n.get('id', ''))

        lines.append(f"### {domain}")
        lines.append(f"*{len(domain_nodes)} nodes*")
        lines.append("")

        for node in domain_nodes[:20]:  # Limit to first 20 per domain in index
            node_id = node.get('id', '')
            name = node.get('name', node_id)
            scale = node.get('scale', 4)
            lines.append(f"- `{node_id}` - {name} (Scale {scale})")

        if len(domain_nodes) > 20:
            lines.append(f"- *... and {len(domain_nodes) - 20} more*")

        lines.append("")

    return '\n'.join(lines)


def main():
    print("=" * 70)
    print("REBUILDING NODE INDEX")
    print("=" * 70)

    # Load all nodes
    print("\n1. Loading node YAML files...")
    nodes = load_all_nodes()
    print(f"   Loaded: {len(nodes)} nodes")

    # Build canonical JSON
    print("\n2. Building canonical_nodes.json...")
    canonical = build_canonical_json(nodes)

    with open(CANONICAL_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(canonical, f, indent=2)
    print(f"   Saved: {CANONICAL_OUTPUT}")

    # Build INDEX.md
    print("\n3. Building INDEX.md...")
    index_md = build_index_markdown(nodes)

    with open(INDEX_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(index_md)
    print(f"   Saved: {INDEX_OUTPUT}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Total nodes: {len(nodes)}")
    print(f"\n   By scale:")

    by_scale = defaultdict(int)
    for node in nodes:
        by_scale[node.get('scale', 4)] += 1

    for scale in sorted(by_scale.keys()):
        scale_name = SCALE_NAMES.get(scale, f'Scale {scale}')
        print(f"   - Scale {scale} ({scale_name}): {by_scale[scale]} nodes")

    print(f"\n   By domain:")
    by_domain = defaultdict(int)
    for node in nodes:
        by_domain[node.get('domain', 'Unknown')] += 1

    for domain in sorted(by_domain.keys(), key=lambda d: -by_domain[d])[:10]:
        print(f"   - {domain}: {by_domain[domain]} nodes")

    if len(by_domain) > 10:
        print(f"   ... and {len(by_domain) - 10} more domains")


if __name__ == "__main__":
    main()
