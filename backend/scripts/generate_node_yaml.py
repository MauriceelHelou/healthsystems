#!/usr/bin/env python3
"""
Generate Individual Node YAML Files

Creates YAML files for each node in the canonical inventory,
organized by scale in the nodes/by_scale/ directory structure.

Uses existing data where available and marks unknown fields as TBD.
"""

import json
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
DEDUP_MAP_PATH = BASE_DIR / 'backend' / 'reports' / 'node_deduplication_map.json'
OUTPUT_DIR = BASE_DIR / 'nodes' / 'by_scale'

# Scale directory names (1-7 scale per NODE_SYSTEM_DEFINITIONS.md)
SCALE_DIRS = {
    1: 'scale_1_structural_determinants',
    2: 'scale_2_built_environment',
    3: 'scale_3_institutional',
    4: 'scale_4_individual_household',
    5: 'scale_5_behaviors_psychosocial',
    6: 'scale_6_intermediate_pathways',
    7: 'scale_7_crisis_endpoints'
}

# Map domains to categories
DOMAIN_TO_CATEGORY = {
    'Healthcare System': 'healthcare_access',
    'Housing': 'built_environment',
    'Economic Security': 'economic',
    'Employment': 'economic',
    'Criminal Justice': 'social_environment',
    'Environmental': 'built_environment',
    'Behavioral Health': 'behavioral',
    'Education': 'social_environment',
    'Transportation': 'built_environment',
    'Food Systems': 'built_environment',
    'Social Support': 'social_environment',
    'Demographics': 'social_environment',
    'Biological': 'biological',
    'Policy': 'political',
    'Unknown': 'social_environment'
}

# Geographic variation heuristics by domain/type
GEO_VARIATION_HEURISTICS = {
    # Federal policies - uniform nationally
    'federal_policy': {'score': 1, 'level': 'federal'},
    # State policies - state variation
    'state_policy': {'score': 3, 'level': 'state'},
    # Local infrastructure - high variation
    'local_infrastructure': {'score': 4, 'level': 'county'},
    # Individual conditions - neighborhood variation
    'individual_condition': {'score': 4, 'level': 'neighborhood'},
    # Biomarkers - individual variation
    'biomarker': {'score': 5, 'level': 'neighborhood'},
    # Default
    'default': {'score': 3, 'level': 'state'}
}

# Data availability by domain
DATA_AVAILABILITY_HEURISTICS = {
    'Healthcare System': 'high',
    'Housing': 'moderate',
    'Economic Security': 'high',
    'Employment': 'high',
    'Criminal Justice': 'moderate',
    'Environmental': 'high',
    'Behavioral Health': 'moderate',
    'Education': 'high',
    'Transportation': 'moderate',
    'Food Systems': 'moderate',
    'Social Support': 'low',
    'Demographics': 'high',
    'Biological': 'moderate',
    'Policy': 'high',
    'Unknown': 'low'
}

# Common data sources by domain
DATA_SOURCES_BY_DOMAIN = {
    'Healthcare System': [
        {'name': 'CMS Medicare/Medicaid Data', 'granularity': 'county'},
        {'name': 'HRSA Area Health Resources Files', 'granularity': 'county'}
    ],
    'Housing': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'HUD Housing Data', 'granularity': 'county'}
    ],
    'Economic Security': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'Bureau of Labor Statistics', 'granularity': 'county'}
    ],
    'Employment': [
        {'name': 'Bureau of Labor Statistics', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Criminal Justice': [
        {'name': 'Bureau of Justice Statistics', 'granularity': 'state'},
        {'name': 'Vera Institute of Justice', 'granularity': 'county'}
    ],
    'Environmental': [
        {'name': 'EPA Environmental Data', 'granularity': 'county'},
        {'name': 'CDC PLACES', 'granularity': 'tract'}
    ],
    'Behavioral Health': [
        {'name': 'SAMHSA NSDUH', 'granularity': 'state'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Education': [
        {'name': 'NCES Education Statistics', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Transportation': [
        {'name': 'DOT Transportation Data', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Food Systems': [
        {'name': 'USDA Food Environment Atlas', 'granularity': 'county'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Social Support': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Demographics': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'CDC WONDER', 'granularity': 'county'}
    ],
    'Biological': [
        {'name': 'NHANES', 'granularity': 'national'},
        {'name': 'CDC WONDER', 'granularity': 'county'}
    ],
    'Policy': [
        {'name': 'NCSL State Policy Database', 'granularity': 'state'},
        {'name': 'Federal Register', 'granularity': 'national'}
    ]
}

# Alcohol-specific data sources
ALCOHOL_DATA_SOURCES = [
    {'name': 'NIAAA Alcohol Policy Information System (APIS)', 'granularity': 'state'},
    {'name': 'SAMHSA NSDUH', 'granularity': 'state'},
    {'name': 'CDC BRFSS', 'granularity': 'state'},
    {'name': 'NHTSA FARS (fatalities)', 'granularity': 'state'}
]


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case node ID."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def estimate_geo_variation(node: Dict) -> Dict:
    """Estimate geographic variation based on node properties (1-7 scale system)."""
    node_type = node.get('type', 'Unknown')
    scale = node.get('scale', 4)  # Default to individual/household
    node_id = node.get('id', '')

    # Scale 1: Structural Determinants (federal/state policy)
    if scale == 1:
        if 'federal' in node_id:
            return {'score': 1, 'level': 'federal', 'notes': 'Federal policy - uniform across states'}
        return {'score': 2, 'level': 'state', 'notes': 'State-level policy variation'}

    # Scale 2: Built Environment & Infrastructure
    if scale == 2:
        return {'score': 4, 'level': 'county', 'notes': 'Physical infrastructure varies by region and locality'}

    # Scale 3: Institutional Infrastructure
    if scale == 3:
        return {'score': 3, 'level': 'county', 'notes': 'Varies by local healthcare/service infrastructure'}

    # Scale 4: Individual/Household Conditions
    if scale == 4:
        return {'score': 4, 'level': 'county', 'notes': 'Varies by local socioeconomic conditions'}

    # Scale 5: Individual Behaviors & Psychosocial
    if scale == 5:
        return {'score': 4, 'level': 'county', 'notes': 'Behavioral patterns vary by community and culture'}

    # Scale 6: Intermediate Pathways
    if scale == 6:
        if 'biomarker' in node_id or node_type == 'Biomarker':
            return {'score': 5, 'level': 'neighborhood', 'notes': 'Individual-level measurement, high local variation'}
        return {'score': 3, 'level': 'state', 'notes': 'Moderate regional variation in clinical measures'}

    # Scale 7: Crisis Endpoints
    if scale == 7:
        return {'score': 4, 'level': 'county', 'notes': 'Varies by local healthcare access and demographics'}

    return {'score': 3, 'level': 'state', 'notes': 'Moderate geographic variation expected'}


def estimate_data_quality(node: Dict) -> Dict:
    """Estimate data quality fields based on node properties."""
    domain = node.get('domain', 'Unknown')
    node_id = node.get('id', '')

    availability = DATA_AVAILABILITY_HEURISTICS.get(domain, 'low')

    # Frequency heuristic
    if 'rate' in node_id or 'mortality' in node_id:
        frequency = 'annual'
    elif 'policy' in node_id or 'status' in node_id:
        frequency = 'periodic'
    else:
        frequency = 'annual'

    # Bias notes
    if 'self_report' in node_id or 'survey' in node_id:
        bias_notes = 'Self-reported data may have recall bias and social desirability effects'
    elif 'rate' in node_id:
        bias_notes = 'Administrative data - may reflect reporting variations across jurisdictions'
    else:
        bias_notes = 'Standard survey/administrative data limitations apply'

    # Data sources
    if 'alcohol' in node_id or 'drinking' in node_id or 'aud' in node_id:
        sources = ALCOHOL_DATA_SOURCES.copy()
    else:
        sources = DATA_SOURCES_BY_DOMAIN.get(domain, [{'name': 'TBD', 'granularity': 'state'}])

    return {
        'availability': availability,
        'frequency': frequency,
        'bias_notes': bias_notes,
        'primary_sources': sources
    }


def generate_description(node: Dict) -> str:
    """Generate a description from node properties."""
    name = clean_field(node.get('name', node['id'].replace('_', ' ').title()))
    unit = clean_field(node.get('unit', 'TBD'))
    node_type = clean_field(node.get('type', 'Measure'))
    domain = clean_field(node.get('domain', 'health'))

    base = f"Measures {name.lower()}"

    if node_type == 'Policy':
        base = f"Policy indicator measuring {name.lower()}"
    elif node_type == 'Rate':
        base = f"Rate measure of {name.lower()}"
    elif node_type == 'Outcome':
        base = f"Health outcome measure: {name.lower()}"
    elif node_type == 'Behavior':
        base = f"Behavioral measure of {name.lower()}"

    # Add unit info
    if unit and unit != 'TBD':
        base += f". Measured in {unit}."
    else:
        base += "."

    # Add domain context
    base += f" Part of the {domain} domain."

    # Ensure minimum length
    if len(base) < 50:
        base += " This node tracks changes in health determinants across populations."

    return base


def clean_field(value: str) -> str:
    """Clean corrupted field data (e.g., 'Domain | **Unit:** ...')."""
    if not value or not isinstance(value, str):
        return value or 'Unknown'
    # Remove markdown artifacts and pipe-separated suffixes
    if '|' in value:
        value = value.split('|')[0].strip()
    if '**' in value:
        value = value.split('**')[0].strip()
    return value if value else 'Unknown'


def create_node_yaml(node: Dict) -> Dict[str, Any]:
    """Create a complete YAML structure for a node."""
    node_id = normalize_node_id(node.get('id', ''))
    name = clean_field(node.get('name', node_id.replace('_', ' ').title()))
    scale = node.get('scale', 4)  # Default to scale 4 (individual/household)
    domain = clean_field(node.get('domain', 'Unknown'))
    node_type = clean_field(node.get('type', 'Unknown'))
    unit = clean_field(node.get('unit', 'TBD'))

    # Map domain to category
    category = DOMAIN_TO_CATEGORY.get(domain, 'social_environment')

    # Estimate geographic variation
    geo_var = estimate_geo_variation(node)

    # Estimate data quality
    data_qual = estimate_data_quality(node)

    # Generate description
    description = generate_description(node)

    return {
        'id': node_id,
        'name': name,
        'scale': scale,
        'domain': domain,
        'category': category,
        'stock': {
            'value': 'TBD',
            'unit': unit,
            'year': 2024,
            'source': 'TBD - needs population from authoritative source'
        },
        'geographic_variation': geo_var,
        'data_quality': data_qual,
        'description': description,
        'type': node_type if node_type != 'Unknown' else 'Rate'
    }


def load_nodes_to_generate() -> list:
    """Load nodes from deduplication map or canonical file."""
    # Try dedup map first
    if DEDUP_MAP_PATH.exists():
        with open(DEDUP_MAP_PATH, 'r') as f:
            dedup_data = json.load(f)
        nodes_to_keep = dedup_data.get('mapping', {}).get('keep', {})
        return list(nodes_to_keep.values())

    # Fall back to canonical nodes
    with open(CANONICAL_NODES_PATH, 'r') as f:
        data = json.load(f)
    return data['nodes']


def write_yaml_file(node_data: Dict, output_path: Path):
    """Write a single node YAML file with nice formatting."""

    # Custom YAML representer for multi-line strings
    def str_representer(dumper, data):
        if '\n' in data or len(data) > 80:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_representer)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(node_data, f,
                  default_flow_style=False,
                  allow_unicode=True,
                  sort_keys=False,
                  width=100)


def main():
    print("=" * 70)
    print("GENERATING NODE YAML FILES")
    print("=" * 70)

    # Load nodes
    print("\n1. Loading nodes...")
    nodes = load_nodes_to_generate()
    print(f"   Nodes to generate: {len(nodes)}")

    # Create output directories
    print("\n2. Creating directory structure...")
    for scale, dirname in SCALE_DIRS.items():
        dir_path = OUTPUT_DIR / dirname
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   Created: {dir_path}")

    # Generate YAML files
    print("\n3. Generating YAML files...")
    counts = defaultdict(int)
    errors = []

    for node in nodes:
        try:
            node_data = create_node_yaml(node)
            scale = node_data['scale']

            # Ensure valid scale (1-7)
            if scale not in SCALE_DIRS:
                scale = 4  # Default to scale 4 (individual/household)
                node_data['scale'] = scale

            # Output path
            scale_dir = SCALE_DIRS[scale]
            output_path = OUTPUT_DIR / scale_dir / f"{node_data['id']}.yaml"

            # Write file
            write_yaml_file(node_data, output_path)
            counts[scale] += 1

        except Exception as e:
            errors.append({'node': node.get('id', 'unknown'), 'error': str(e)})

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = sum(counts.values())
    print(f"   Total YAML files generated: {total}")
    print("\n   By scale:")
    for scale in sorted(counts.keys()):
        scale_name = SCALE_DIRS.get(scale, f'scale_{scale}')
        print(f"   - {scale_name}: {counts[scale]} nodes")

    if errors:
        print(f"\n   Errors: {len(errors)}")
        for err in errors[:10]:
            print(f"   - {err['node']}: {err['error']}")

    print(f"\n   Output directory: {OUTPUT_DIR}")

    return total, errors


if __name__ == "__main__":
    main()
