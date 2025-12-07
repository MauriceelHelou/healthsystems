#!/usr/bin/env python3
"""
Add Custom Nodes to Canonical Inventory

Adds frequently-used custom nodes from mechanisms to the canonical inventory.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
MAPPING_REPORT_PATH = BASE_DIR / 'backend' / 'reports' / 'node_mapping_report.json'

# Nodes to add based on mechanism usage (nodes with no canonical match)
# Format: (node_id, node_name, scale, domain, type, unit)
NODES_TO_ADD = [
    # Alcohol-related nodes (high usage)
    ("alcohol_consumption", "Alcohol Consumption", 3, "Behavioral Health", "Behavior", "Standard drinks per week"),
    ("alcohol_consumption_reduction", "Alcohol Consumption Reduction", 4, "Behavioral Health", "Outcome", "Percent reduction in consumption"),
    ("population_alcohol_per_capita_consumption", "Population Alcohol Per Capita Consumption", 2, "Behavioral Health", "Population Measure", "Liters of pure alcohol per capita per year"),
    ("hazardous_drinking", "Hazardous Drinking", 3, "Behavioral Health", "Behavior", "AUDIT score ≥8 or equivalent"),
    ("problem_gambling", "Problem Gambling", 3, "Behavioral Health", "Condition", "Problem Gambling Severity Index score"),

    # Alcohol policy nodes
    ("alcohol_warning_label_implementation", "Alcohol Warning Label Implementation", 1, "Policy", "Policy", "Binary (0=no labels, 1=labels implemented)"),
    ("alcohol_warning_label_policy", "Alcohol Health Warning Label Policy", 1, "Policy", "Policy", "Categorical (none, basic, comprehensive)"),
    ("alcohol_taxation", "Alcohol Taxation", 1, "Policy", "Policy", "Tax rate per unit alcohol"),
    ("minimum_unit_pricing", "Minimum Unit Pricing (MUP)", 1, "Policy", "Policy", "Price per unit in local currency"),

    # Alcohol treatment
    ("aud_pharmacotherapy_receipt", "AUD Pharmacotherapy Receipt", 4, "Healthcare System", "Treatment", "Percent of AUD patients receiving pharmacotherapy"),
    ("brief_alcohol_interventions", "Brief Alcohol Interventions", 4, "Healthcare System", "Intervention", "Binary (received/not received)"),

    # Violence and trauma
    ("ipv_trauma_recovery", "IPV Trauma Recovery", 4, "Behavioral Health", "Outcome", "Recovery status post-IPV"),

    # Traffic safety
    ("road_traffic_fatalities", "Road Traffic Fatalities", 5, "Health", "Outcome", "Deaths per 100k population"),
    ("texting_ban_while_driving", "Texting While Driving Ban", 1, "Policy", "Policy", "Categorical (none, secondary, primary enforcement)"),
    ("mobile_phone_use_while_driving", "Mobile Phone Use While Driving", 3, "Behavioral Health", "Behavior", "Percent of drivers"),
    ("handheld_mobile_phone_ban_primary_enforcement", "Hand-held Phone Ban (Primary Enforcement)", 1, "Policy", "Policy", "Binary (0=no, 1=yes)"),

    # Clinical/biological
    ("acute_pancreatitis", "Acute Pancreatitis", 5, "Health", "Condition", "Cases per 100k"),
    ("chronic_pancreatitis", "Chronic Pancreatitis", 5, "Health", "Condition", "Cases per 100k"),
    ("hypercalcemic_acute_pancreatitis", "Hypercalcemic Acute Pancreatitis", 5, "Health", "Condition", "Cases per 100k"),
    ("alcohol_associated_cirrhosis", "Alcohol-Associated Cirrhosis", 5, "Health", "Condition", "Cases per 100k"),

    # Prenatal/perinatal
    ("perinatal_suicidal_risk", "Perinatal Suicidal Risk", 5, "Health", "Risk", "Percent at risk"),
    ("light_prenatal_alcohol_consumption", "Light Prenatal Alcohol Consumption", 3, "Behavioral Health", "Exposure", "≤32 grams per week"),

    # Neurological
    ("adolescent_cannabis_exposure", "Adolescent Cannabis Exposure", 3, "Behavioral Health", "Exposure", "Binary or frequency"),
    ("cns_neurocognitive_impairment", "CNS Neurocognitive Impairment", 5, "Health", "Outcome", "Standardized cognitive score"),

    # Other behavioral
    ("alcohol_related_hookup_behavior", "Alcohol-Related Sexual Risk Behavior", 3, "Behavioral Health", "Behavior", "Frequency of alcohol-involved sexual encounters"),
    ("self_compassion", "Self-Compassion", 3, "Behavioral Health", "Psychological", "Self-Compassion Scale score"),
    ("poor_sleep_quality", "Poor Sleep Quality", 3, "Health", "Condition", "PSQI score"),

    # Demographics (as exposures)
    ("black_race", "Black/African American Race", 3, "Demographics", "Demographic", "Binary indicator"),

    # Treatment
    ("glucocorticoid_use", "Glucocorticoid Use", 4, "Healthcare System", "Treatment", "Binary or dose"),
    ("corticosteroid_treatment", "Corticosteroid Treatment", 4, "Healthcare System", "Treatment", "Binary or dose"),

    # Genetic/molecular
    ("dna_methylation_colca1_colca2", "DNA Methylation at COLCA1/COLCA2", 4, "Biological", "Biomarker", "Methylation level"),
]


def load_canonical_nodes():
    """Load current canonical inventory."""
    with open(CANONICAL_NODES_PATH, 'r') as f:
        return json.load(f)


def save_canonical_nodes(data):
    """Save updated canonical inventory."""
    with open(CANONICAL_NODES_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    print("=" * 70)
    print("ADDING NODES TO CANONICAL INVENTORY")
    print("=" * 70)

    # Load current inventory
    data = load_canonical_nodes()
    existing_ids = set(data['by_id'].keys())
    current_max_number = max(n['number'] for n in data['nodes'])

    print(f"\nCurrent inventory: {len(data['nodes'])} nodes")
    print(f"Highest node number: {current_max_number}")

    # Add new nodes
    added = 0
    skipped = 0

    for node_id, node_name, scale, domain, node_type, unit in NODES_TO_ADD:
        if node_id in existing_ids:
            print(f"  SKIP (exists): {node_id}")
            skipped += 1
            continue

        current_max_number += 1
        new_node = {
            'number': current_max_number,
            'id': node_id,
            'name': node_name,
            'scale': scale,
            'domain': domain,
            'type': node_type,
            'unit': unit
        }

        data['nodes'].append(new_node)
        data['by_id'][node_id] = new_node

        # Update by_scale
        scale_key = str(scale)
        if scale_key not in data['by_scale']:
            data['by_scale'][scale_key] = []
        data['by_scale'][scale_key].append(node_id)

        # Update by_domain
        if domain not in data['by_domain']:
            data['by_domain'][domain] = []
        data['by_domain'][domain].append(node_id)

        print(f"  ADD: {node_id} ({node_name})")
        added += 1

    # Update metadata
    data['metadata']['total_nodes'] = len(data['nodes'])

    # Save
    save_canonical_nodes(data)

    print(f"\n" + "=" * 70)
    print(f"SUMMARY")
    print(f"=" * 70)
    print(f"  Added: {added} nodes")
    print(f"  Skipped (already exist): {skipped}")
    print(f"  New total: {len(data['nodes'])} nodes")
    print(f"\n  Saved to: {CANONICAL_NODES_PATH}")


if __name__ == "__main__":
    main()
