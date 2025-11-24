"""
Generate node YAML files from COMPLETE_NODE_INVENTORY.md

This script parses the structured node inventory and creates individual
YAML files for each node with metadata including scale, domain, type,
unit, description, baseline values, and data sources.

Usage:
    python -m backend.scripts.generate_node_yamls

Output:
    Creates YAML files in mechanism-bank/nodes/ directory
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import yaml


def parse_node_inventory(inventory_path: Path) -> List[Dict]:
    """
    Parse COMPLETE_NODE_INVENTORY.md and extract node specifications.

    The inventory is structured with Scale sections (1-7), each containing
    node definitions with metadata fields.
    """
    with open(inventory_path, 'r', encoding='utf-8') as f:
        content = f.read()

    nodes = []
    current_scale = None
    current_node = None

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect scale headers: "## Scale N: Description"
        scale_match = re.match(r'^##\s+Scale\s+(\d+):', line)
        if scale_match:
            current_scale = int(scale_match.group(1))
            i += 1
            continue

        # Detect node entries: "### Node ID: node_name"
        node_match = re.match(r'^###\s+(?:Node\s+ID:?\s*)?(.+)', line)
        if node_match and current_scale:
            # Save previous node if exists
            if current_node and current_node.get('id'):
                nodes.append(current_node)

            # Start new node
            node_id_or_name = node_match.group(1).strip()
            # Try to extract ID from format "node_id - Node Name" or just use as-is
            if ' - ' in node_id_or_name:
                node_id, node_name = node_id_or_name.split(' - ', 1)
                node_id = node_id.strip()
                node_name = node_name.strip()
            else:
                # Convert to snake_case for ID
                node_id = node_id_or_name.lower().replace(' ', '_').replace('-', '_')
                node_name = node_id_or_name

            current_node = {
                'id': node_id,
                'name': node_name,
                'scale': current_scale,
                'category': infer_category_from_scale(current_scale),
                'type': 'Rate',  # Default
            }
            i += 1
            continue

        # Parse metadata fields
        if current_node and line.startswith('**') and ':' in line:
            # Extract field name and value
            field_match = re.match(r'\*\*(.+?):\*\*\s*(.+)', line)
            if field_match:
                field_name = field_match.group(1).strip()
                field_value = field_match.group(2).strip()

                # Map field names to YAML keys
                field_mapping = {
                    'Domain': 'domain',
                    'Type': 'type',
                    'Unit': 'unit',
                    'Description': 'description',
                    'Measurement Method': 'measurement_method',
                    'Typical Range': 'typical_range',
                    'Baseline (US)': 'baseline_us',
                    'Data Source': 'data_source',
                    'Data Granularity': 'data_granularity',
                    'Data Limitations': 'limitations',
                }

                yaml_key = field_mapping.get(field_name)
                if yaml_key:
                    current_node[yaml_key] = field_value

        i += 1

    # Add last node
    if current_node and current_node.get('id'):
        nodes.append(current_node)

    return nodes


def infer_category_from_scale(scale: int) -> str:
    """Map scale to appropriate category"""
    scale_to_category = {
        1: 'political',
        2: 'built_environment',
        3: 'economic',
        4: 'economic',
        5: 'behavioral',
        6: 'healthcare_access',
        7: 'biological'
    }
    return scale_to_category.get(scale, 'default')


def generate_yaml_files(nodes: List[Dict], output_dir: Path):
    """Generate individual YAML files for each node"""
    output_dir.mkdir(parents=True, exist_ok=True)

    for node in nodes:
        yaml_path = output_dir / f"{node['id']}.yml"

        # Format the YAML content
        yaml_content = f"""# Node Definition: {node['name']}
# Scale {node['scale']} - {get_scale_description(node['scale'])}

"""

        # Write as structured YAML
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            yaml.dump(node, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"Created {yaml_path.name}")


def get_scale_description(scale: int) -> str:
    """Get human-readable scale description"""
    descriptions = {
        1: 'Structural Determinants (Policy)',
        2: 'Built Environment & Infrastructure',
        3: 'Institutional Infrastructure',
        4: 'Household Conditions',
        5: 'Individual Behaviors & Psychosocial',
        6: 'Intermediate Pathways',
        7: 'Crisis Endpoints'
    }
    return descriptions.get(scale, 'Unknown')


def main():
    """Main execution"""
    # Paths
    project_root = Path(__file__).parent.parent.parent
    inventory_path = project_root / "Nodes" / "COMPLETE_NODE_INVENTORY.md"
    output_dir = project_root / "mechanism-bank" / "nodes"

    # Check if inventory exists
    if not inventory_path.exists():
        print(f"❌ Error: COMPLETE_NODE_INVENTORY.md not found at {inventory_path}")
        print("\nThis script expects the inventory at:")
        print(f"  {inventory_path}")
        print("\nPlease ensure the file exists before running this script.")
        return

    print(f"📖 Reading node inventory from {inventory_path.name}...")
    nodes = parse_node_inventory(inventory_path)

    if not nodes:
        print("⚠️  Warning: No nodes parsed from inventory")
        print("\nThis might be because:")
        print("  1. The inventory format has changed")
        print("  2. The file is empty")
        print("  3. The parser needs to be updated")
        return

    print(f"✓ Parsed {len(nodes)} nodes from inventory")
    print(f"\n📝 Generating YAML files in {output_dir}...")

    generate_yaml_files(nodes, output_dir)

    print(f"\n✅ Success! Generated {len(nodes)} node YAML files")
    print(f"\nNext steps:")
    print(f"  1. Review generated files in: {output_dir}")
    print(f"  2. Edit/enhance metadata as needed")
    print(f"  3. Load into database: POST /api/mechanisms/admin/load-nodes-from-yaml")


if __name__ == "__main__":
    main()
