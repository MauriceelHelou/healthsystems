#!/usr/bin/env python3
"""
Extract canonical nodes from COMPLETE_NODE_INVENTORY.md

Creates backend/data/canonical_nodes.json with structured node data.
"""

import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
INVENTORY_PATH = BASE_DIR / 'docs' / 'nodes' / 'COMPLETE_NODE_INVENTORY.md'
OUTPUT_PATH = BASE_DIR / 'backend' / 'data' / 'canonical_nodes.json'


def extract_nodes(content: str) -> list:
    """Extract all nodes with their metadata."""
    nodes = []

    # Split into node blocks
    # Pattern: ### Node N: Name followed by metadata
    node_pattern = r'### Node (\d+): (.+?)(?=\n)'

    # Find all node headers
    matches = list(re.finditer(node_pattern, content))

    for i, match in enumerate(matches):
        node_num = int(match.group(1))
        node_name = match.group(2).strip()

        # Get the text block for this node (until next node or section)
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        block = content[start:end]

        # Extract metadata from block
        scale = None
        domain = None
        node_type = None
        unit = None

        scale_match = re.search(r'\*\*Scale:\*\*\s*(\d+)', block)
        if scale_match:
            scale = int(scale_match.group(1))

        domain_match = re.search(r'\*\*Domain:\*\*\s*(.+?)(?:\n|$)', block)
        if domain_match:
            domain = domain_match.group(1).strip()

        type_match = re.search(r'\*\*Type:\*\*\s*(.+?)(?:\n|$)', block)
        if type_match:
            node_type = type_match.group(1).strip()

        unit_match = re.search(r'\*\*Unit:\*\*\s*(.+?)(?:\n|$)', block)
        if unit_match:
            unit = unit_match.group(1).strip()

        # Create snake_case ID
        node_id = node_name.lower()
        node_id = re.sub(r'[^a-z0-9]+', '_', node_id)
        node_id = re.sub(r'^_|_$', '', node_id)
        node_id = re.sub(r'_+', '_', node_id)

        nodes.append({
            'number': node_num,
            'id': node_id,
            'name': node_name,
            'scale': scale,
            'domain': domain,
            'type': node_type,
            'unit': unit,
        })

    return nodes


def main():
    print(f"Reading: {INVENTORY_PATH}")

    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    nodes = extract_nodes(content)
    print(f"Extracted {len(nodes)} nodes")

    # Create lookup structures
    output = {
        'metadata': {
            'source': 'docs/nodes/COMPLETE_NODE_INVENTORY.md',
            'total_nodes': len(nodes),
            'scales': {
                1: 'Structural Determinants',
                2: 'Institutional Infrastructure',
                3: 'Individual/Household Conditions',
                4: 'Intermediate Pathways',
                5: 'Crisis Endpoints',
            }
        },
        'nodes': nodes,
        'by_id': {n['id']: n for n in nodes},
        'by_scale': {},
        'by_domain': {},
    }

    # Group by scale
    for node in nodes:
        scale = node.get('scale')
        if scale:
            if scale not in output['by_scale']:
                output['by_scale'][scale] = []
            output['by_scale'][scale].append(node['id'])

    # Group by domain
    for node in nodes:
        domain = node.get('domain')
        if domain:
            if domain not in output['by_domain']:
                output['by_domain'][domain] = []
            output['by_domain'][domain].append(node['id'])

    # Save
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Saved to: {OUTPUT_PATH}")

    # Print summary
    print("\nSummary by Scale:")
    for scale, desc in output['metadata']['scales'].items():
        count = len(output['by_scale'].get(scale, []))
        print(f"  Scale {scale} ({desc}): {count} nodes")

    print(f"\nDomains: {len(output['by_domain'])}")
    for domain, node_ids in sorted(output['by_domain'].items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {domain}: {len(node_ids)} nodes")


if __name__ == "__main__":
    main()
