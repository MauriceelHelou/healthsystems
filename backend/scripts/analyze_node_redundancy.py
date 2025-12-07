#!/usr/bin/env python3
"""
Analyze Node Redundancy for Complete Inventory Rebuild

Loads all canonical nodes + custom mechanism nodes, clusters similar nodes,
and creates a deduplication mapping for the new YAML-based inventory.

Output: backend/reports/node_deduplication_map.json
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Set

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
COVERAGE_AUDIT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_coverage_audit.json'
OUTPUT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_deduplication_map.json'


# ============================================================================
# SEMANTIC GROUPINGS - define which concepts should be merged or kept separate
# ============================================================================

# Nodes that should be MERGED (same concept, different names)
MERGE_GROUPS = {
    # Alcohol consumption variations
    'alcohol_consumption': [
        'alcohol_consumption', 'alcohol_consumption_frequency',
        'alcohol_consumption_quantity', 'population_alcohol_per_capita_consumption'
    ],
    'hazardous_drinking': [
        'hazardous_drinking', 'binge_drinking', 'heavy_drinking',
        'heavy_episodic_drinking', 'risky_drinking', 'problem_drinking'
    ],
    'alcohol_use_disorder': [
        'alcohol_use_disorder', 'alcohol_dependence', 'alcohol_abuse',
        'alcohol_dependence_symptoms', 'aud'
    ],

    # Housing stability variations
    'housing_instability': [
        'housing_instability', 'housing_instability_multiple_moves',
        'housing_instability_risk'
    ],
    'homelessness': [
        'homelessness_rate', 'homelessness_rate_point_in_time',
        'unsheltered_homelessness_rate', 'family_homelessness_rate',
        'youth_homelessness_unaccompanied_rate'
    ],

    # Income/poverty variations
    'poverty': [
        'poverty_rate', 'deep_poverty_rate', 'child_poverty_rate'
    ],

    # Asthma-related
    'asthma_prevalence': [
        'asthma_prevalence_adults_revised_terminology_standardized',
        'asthma_prevalence_children_0_17_revised_terminology_standardized'
    ],

    # Digital access
    'digital_access': [
        'digital_inclusion_index_revised_consolidated_4_nodes',
        'digital_health_access_revised_healthcare_specific',
        'broadband_desert_no_access', 'broadband_affordability_crisis'
    ],

    # Employment/underemployment
    'unemployment': [
        'unemployment_rate_local', 'youth_16_24_unemployment_rate',
        'underemployment', 'underemployment_rate'
    ],

    # Heat exposure
    'extreme_heat_exposure': [
        'extreme_heat_days_exposure', 'extreme_heat_days_per_year',
        'extreme_heat_exposure_individual', 'heat_stress_exposure_occupational'
    ],

    # Criminal justice
    'criminal_justice_involvement': [
        'criminal_justice_system_contact_any_revised',
        'criminal_justice_involvement_intensity_revised_consolidated',
        'incarceration_rate'
    ],
}

# Nodes that are CLINICALLY DISTINCT and should NOT be merged
KEEP_SEPARATE = {
    # These look similar but measure different things
    'alcohol_use_disorder',  # Clinical diagnosis (DSM-5)
    'hazardous_drinking',    # AUDIT screening threshold
    'alcohol_consumption',   # Quantity/frequency measure

    # Different cancer types
    'breast_cancer_incidence',
    'lung_cancer_incidence',
    'colorectal_cancer_incidence',

    # Different SUD types
    'opioid_use_disorder',
    'cannabis_use_disorder',
    'stimulant_use_disorder',
}

# Nodes to DISCARD (over-specific, single-use, or methodological)
DISCARD_PATTERNS = [
    r'.*_revised$',                    # Cleanup naming artifacts
    r'.*_revised_.*',                  # Cleanup naming artifacts
    r'.*_consolidated.*',              # Cleanup naming artifacts
    r'.*generalizability.*',           # Methodological concerns, not nodes
    r'.*exclusion_from_trials.*',      # Methodological concerns
    r'.*epidemiological_rate_estimation.*',  # Methodological
    r'.*_sgm_poc$',                    # Over-specific intersectional
    r'.*_indigenous$',                 # Population-specific (use modifiers instead)
    r'birth_cohort_modernization',     # Temporal artifact
    r'policy_inaction_.*',             # Too abstract
    r'policy_focus_shift.*',           # Too abstract
    r'individual_responsibility_framing',  # Industry framing, not health node
    r'corporate_political_activity',   # Industry activity, not health node
]

# Scale descriptions for organizing output (1-7 scale per NODE_SYSTEM_DEFINITIONS.md)
SCALE_NAMES = {
    1: 'structural_determinants',
    2: 'built_environment',
    3: 'institutional',
    4: 'individual_household',
    5: 'behaviors_psychosocial',
    6: 'intermediate_pathways',
    7: 'crisis_endpoints'
}


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case node ID."""
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


def should_discard(node_id: str) -> bool:
    """Check if node matches discard patterns."""
    for pattern in DISCARD_PATTERNS:
        if re.match(pattern, node_id):
            return True
    return False


def find_merge_group(node_id: str) -> str | None:
    """Find if node belongs to a merge group, return canonical ID."""
    normalized = normalize_node_id(node_id)
    for canonical_id, members in MERGE_GROUPS.items():
        if normalized in [normalize_node_id(m) for m in members]:
            return canonical_id
    return None


def cluster_by_prefix(nodes: List[Dict]) -> Dict[str, List[Dict]]:
    """Group nodes by common prefix patterns."""
    clusters = defaultdict(list)

    for node in nodes:
        node_id = node['id']

        # Extract prefix (first 2-3 words typically indicate topic)
        parts = node_id.split('_')
        if len(parts) >= 3:
            prefix = '_'.join(parts[:3])
        elif len(parts) >= 2:
            prefix = '_'.join(parts[:2])
        else:
            prefix = parts[0]

        clusters[prefix].append(node)

    return dict(clusters)


def cluster_by_similarity(nodes: List[Dict], threshold: float = 0.75) -> List[List[Dict]]:
    """Cluster nodes by name/id similarity."""
    clusters = []
    used = set()

    for i, node1 in enumerate(nodes):
        if node1['id'] in used:
            continue

        cluster = [node1]
        used.add(node1['id'])

        for j, node2 in enumerate(nodes):
            if i >= j or node2['id'] in used:
                continue

            # Check ID similarity
            id_sim = similarity(node1['id'], node2['id'])

            # Check name similarity
            name_sim = similarity(
                node1.get('name', node1['id']),
                node2.get('name', node2['id'])
            )

            if id_sim >= threshold or name_sim >= threshold:
                cluster.append(node2)
                used.add(node2['id'])

        if len(cluster) > 1:
            clusters.append(cluster)

    return clusters


def load_all_nodes() -> Tuple[List[Dict], List[Dict]]:
    """Load canonical and custom nodes."""
    # Load canonical nodes
    with open(CANONICAL_NODES_PATH, 'r') as f:
        canonical_data = json.load(f)
    canonical_nodes = canonical_data['nodes']

    # Load custom nodes from coverage audit
    custom_nodes = []
    if COVERAGE_AUDIT_PATH.exists():
        with open(COVERAGE_AUDIT_PATH, 'r') as f:
            audit_data = json.load(f)
        for cn in audit_data.get('custom_nodes', []):
            custom_nodes.append({
                'id': cn['id'],
                'name': cn['names'][0] if cn['names'] else cn['id'].replace('_', ' ').title(),
                'scale': 3,  # Default to individual scale
                'domain': 'Unknown',
                'type': 'Unknown',
                'unit': 'TBD',
                'source': 'mechanism_extraction'
            })

    return canonical_nodes, custom_nodes


def analyze_redundancy():
    """Main analysis function."""
    print("=" * 70)
    print("NODE REDUNDANCY ANALYSIS")
    print("=" * 70)

    # Load nodes
    print("\n1. Loading nodes...")
    canonical_nodes, custom_nodes = load_all_nodes()
    print(f"   Canonical nodes: {len(canonical_nodes)}")
    print(f"   Custom nodes: {len(custom_nodes)}")

    # Combine all nodes
    all_nodes = canonical_nodes + custom_nodes
    all_nodes_by_id = {n['id']: n for n in all_nodes}

    # Initialize mapping
    mapping = {
        'keep': {},      # node_id -> node (unchanged)
        'merge': {},     # old_node_id -> new_canonical_id
        'discard': [],   # list of discarded node_ids
        'review': [],    # similar nodes that need manual review
    }

    # Step 1: Mark nodes for discard based on patterns
    print("\n2. Identifying nodes to discard...")
    discard_count = 0
    for node in all_nodes:
        if should_discard(node['id']):
            mapping['discard'].append({
                'id': node['id'],
                'reason': 'matches_discard_pattern'
            })
            discard_count += 1
    print(f"   Nodes to discard: {discard_count}")

    # Step 2: Apply explicit merge groups
    print("\n3. Applying merge groups...")
    merge_count = 0
    for canonical_id, members in MERGE_GROUPS.items():
        for member in members:
            normalized = normalize_node_id(member)
            if normalized in all_nodes_by_id and normalized != canonical_id:
                mapping['merge'][normalized] = canonical_id
                merge_count += 1
    print(f"   Explicit merges: {merge_count}")

    # Step 3: Find similar nodes by clustering
    print("\n4. Clustering similar nodes...")
    remaining_nodes = [
        n for n in all_nodes
        if n['id'] not in mapping['merge']
        and not any(d['id'] == n['id'] for d in mapping['discard'])
    ]

    similar_clusters = cluster_by_similarity(remaining_nodes, threshold=0.80)

    print(f"   Found {len(similar_clusters)} clusters of similar nodes")

    # Mark clusters for review
    for cluster in similar_clusters:
        if len(cluster) > 1:
            # Pick the shortest, most general ID as canonical
            canonical = min(cluster, key=lambda n: len(n['id']))
            for node in cluster:
                if node['id'] != canonical['id']:
                    mapping['review'].append({
                        'original': node['id'],
                        'suggested_canonical': canonical['id'],
                        'similarity': similarity(node['id'], canonical['id']),
                        'reason': 'high_similarity_cluster'
                    })

    # Step 4: Keep remaining nodes
    print("\n5. Finalizing kept nodes...")
    discarded_ids = set(d['id'] for d in mapping['discard'])
    merged_ids = set(mapping['merge'].keys())

    for node in all_nodes:
        if node['id'] not in discarded_ids and node['id'] not in merged_ids:
            mapping['keep'][node['id']] = {
                'id': node['id'],
                'name': node.get('name', node['id'].replace('_', ' ').title()),
                'scale': node.get('scale', 3),
                'domain': node.get('domain', 'Unknown'),
                'type': node.get('type', 'Unknown'),
                'unit': node.get('unit', 'TBD')
            }

    # Generate summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Original nodes: {len(all_nodes)}")
    print(f"   Kept as-is: {len(mapping['keep'])}")
    print(f"   Merged: {len(mapping['merge'])}")
    print(f"   Discarded: {len(mapping['discard'])}")
    print(f"   Need review: {len(mapping['review'])}")

    # Organize kept nodes by scale
    nodes_by_scale = defaultdict(list)
    for node_id, node in mapping['keep'].items():
        scale = node.get('scale', 3)
        nodes_by_scale[scale].append(node_id)

    print("\n   Nodes by scale:")
    for scale in sorted(nodes_by_scale.keys()):
        if scale in SCALE_NAMES:
            print(f"   Scale {scale} ({SCALE_NAMES[scale]}): {len(nodes_by_scale[scale])} nodes")

    # Print alcohol-related nodes for verification
    print("\n   Alcohol-related nodes kept:")
    alcohol_nodes = [nid for nid in mapping['keep'] if 'alcohol' in nid or 'aud' in nid or 'drinking' in nid]
    for nid in sorted(alcohol_nodes)[:20]:
        print(f"   - {nid}")
    if len(alcohol_nodes) > 20:
        print(f"   ... and {len(alcohol_nodes) - 20} more")

    # Print nodes needing review
    if mapping['review']:
        print(f"\n   TOP CLUSTERS NEEDING REVIEW:")
        for item in mapping['review'][:15]:
            print(f"   - {item['original']} → {item['suggested_canonical']} ({item['similarity']:.0%})")

    # Save report
    report = {
        'summary': {
            'original_total': len(all_nodes),
            'canonical_count': len(canonical_nodes),
            'custom_count': len(custom_nodes),
            'kept': len(mapping['keep']),
            'merged': len(mapping['merge']),
            'discarded': len(mapping['discard']),
            'needs_review': len(mapping['review'])
        },
        'mapping': mapping,
        'nodes_by_scale': {str(k): v for k, v in nodes_by_scale.items()}
    }

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n   Report saved: {OUTPUT_PATH}")

    return report


if __name__ == "__main__":
    analyze_redundancy()
