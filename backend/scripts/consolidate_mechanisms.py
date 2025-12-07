#!/usr/bin/env python3
"""
Mechanism Consolidation Pipeline

Groups mechanisms by pathway, merges evidence, upgrades grades.
Discards truly single-paper C-rated mechanisms.
"""

import os
import re
import yaml
import json
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

BASE_DIR = Path(__file__).parent.parent.parent
MECHANISM_DIR = BASE_DIR / 'mechanism-bank' / 'mechanisms'
CONSOLIDATED_DIR = BASE_DIR / 'mechanism-bank' / 'consolidated'
DISCARDED_DIR = BASE_DIR / 'mechanism-bank' / 'discarded'
CANONICAL_NODES_PATH = BASE_DIR / 'backend' / 'data' / 'canonical_nodes.json'
REPORT_PATH = BASE_DIR / 'backend' / 'reports' / 'consolidation_report.json'


def load_canonical_nodes():
    """Load canonical node inventory."""
    with open(CANONICAL_NODES_PATH, 'r') as f:
        return json.load(f)


def normalize_node_id(node_id: str) -> str:
    """Normalize node ID to snake_case."""
    if not node_id:
        return ""
    node_id = node_id.lower()
    node_id = re.sub(r'[^a-z0-9]+', '_', node_id)
    node_id = re.sub(r'^_|_$', '', node_id)
    node_id = re.sub(r'_+', '_', node_id)
    return node_id


def get_grade(n_studies: int) -> str:
    """Determine grade based on n_studies."""
    if n_studies is None or n_studies <= 0:
        return 'C'
    elif n_studies >= 5:
        return 'A'
    elif n_studies >= 3:
        return 'B'
    else:
        return 'C'


def load_all_mechanisms():
    """Load all mechanism YAML files."""
    mechanisms = []

    for yaml_file in MECHANISM_DIR.rglob('*.yaml'):
        if 'extraction_analytics' in yaml_file.name:
            continue
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if data:
                data['_source_file'] = str(yaml_file)
                data['_category'] = yaml_file.parent.name
                mechanisms.append(data)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return mechanisms


def group_by_pathway(mechanisms: list) -> dict:
    """Group mechanisms by normalized from->to pathway."""
    pathways = defaultdict(list)

    for mech in mechanisms:
        from_node = mech.get('from_node', {})
        to_node = mech.get('to_node', {})

        from_id = normalize_node_id(from_node.get('node_id', '') or from_node.get('node_name', ''))
        to_id = normalize_node_id(to_node.get('node_id', '') or to_node.get('node_name', ''))

        if from_id and to_id:
            pathway_key = f"{from_id}__to__{to_id}"
            pathways[pathway_key].append(mech)

    return pathways


def consolidate_pathway(pathway_key: str, mechanisms: list) -> dict:
    """Consolidate multiple mechanisms for the same pathway."""

    # Collect all evidence
    all_citations = []
    total_n_studies = 0
    all_pathways = []
    all_moderators = []
    categories = defaultdict(int)
    directions = defaultdict(int)
    source_files = []

    for mech in mechanisms:
        evidence = mech.get('evidence', {})

        # Citations
        primary = evidence.get('primary_citation', '')
        if primary:
            all_citations.append(primary)

        # Studies count
        n = evidence.get('n_studies')
        if n and isinstance(n, int):
            total_n_studies += n
        else:
            total_n_studies += 1  # At minimum, this paper is 1 study

        # Pathway descriptions
        pathway = mech.get('mechanism_pathway', [])
        if pathway:
            all_pathways.append(pathway)

        # Moderators
        mods = mech.get('moderators', [])
        if mods:
            all_moderators.extend(mods)

        # Category and direction
        cat = mech.get('category', 'unknown')
        categories[cat] += 1

        direction = mech.get('direction', 'positive')
        directions[direction] += 1

        # Track source
        source_files.append(mech.get('_source_file', ''))

    # Determine consolidated values
    best_category = max(categories.items(), key=lambda x: x[1])[0]
    best_direction = max(directions.items(), key=lambda x: x[1])[0]
    best_pathway = max(all_pathways, key=len) if all_pathways else []
    grade = get_grade(total_n_studies)

    # Use first mechanism as template
    template = mechanisms[0]
    from_node = template.get('from_node', {})
    to_node = template.get('to_node', {})

    # Deduplicate citations
    unique_citations = list(dict.fromkeys(all_citations))

    # Deduplicate moderators by name
    seen_mods = set()
    unique_moderators = []
    for mod in all_moderators:
        mod_name = mod.get('name', '') if isinstance(mod, dict) else str(mod)
        if mod_name and mod_name not in seen_mods:
            seen_mods.add(mod_name)
            unique_moderators.append(mod)

    consolidated = {
        'id': pathway_key.replace('__to__', '_to_'),
        'name': f"{from_node.get('node_name', '')} → {to_node.get('node_name', '')}",
        'from_node': from_node,
        'to_node': to_node,
        'direction': best_direction,
        'category': best_category,
        'mechanism_pathway': best_pathway,
        'evidence': {
            'quality_rating': grade,
            'n_studies': total_n_studies,
            'n_sources': len(mechanisms),
            'primary_citation': unique_citations[0] if unique_citations else '',
            'supporting_citations': unique_citations[1:10] if len(unique_citations) > 1 else [],
        },
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'consolidation_metadata': {
            'consolidated_from': len(mechanisms),
            'source_files': source_files,
            'consolidation_date': datetime.now().isoformat(),
        }
    }

    if unique_moderators:
        consolidated['moderators'] = unique_moderators[:10]

    return consolidated


def main():
    print("=" * 70)
    print("MECHANISM CONSOLIDATION PIPELINE")
    print("=" * 70)

    # Setup directories
    CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)
    DISCARDED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load mechanisms
    print("\n1. Loading mechanisms...")
    mechanisms = load_all_mechanisms()
    print(f"   Loaded {len(mechanisms)} mechanisms")

    # Group by pathway
    print("\n2. Grouping by pathway...")
    pathways = group_by_pathway(mechanisms)
    print(f"   Found {len(pathways)} unique pathways")

    # Analyze
    single_source = {k: v for k, v in pathways.items() if len(v) == 1}
    multi_source = {k: v for k, v in pathways.items() if len(v) > 1}

    print(f"   Single-source pathways: {len(single_source)}")
    print(f"   Multi-source pathways: {len(multi_source)}")

    # Consolidate
    print("\n3. Consolidating...")

    consolidated_count = 0
    discarded_count = 0
    upgraded_count = 0

    grade_before = defaultdict(int)
    grade_after = defaultdict(int)

    # Process multi-source pathways
    for pathway_key, mechs in multi_source.items():
        consolidated = consolidate_pathway(pathway_key, mechs)
        grade = consolidated['evidence']['quality_rating']
        grade_after[grade] += 1

        # Track original grades
        for m in mechs:
            orig_grade = m.get('evidence', {}).get('quality_rating', 'C')
            grade_before[orig_grade] += 1

        # Check if upgraded
        if grade in ['A', 'B']:
            upgraded_count += 1

        # Save consolidated mechanism
        category = consolidated['category']
        cat_dir = CONSOLIDATED_DIR / category
        cat_dir.mkdir(exist_ok=True)

        filename = f"{consolidated['id']}.yaml"
        with open(cat_dir / filename, 'w', encoding='utf-8') as f:
            yaml.dump(consolidated, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        consolidated_count += 1

    # Process single-source pathways
    for pathway_key, mechs in single_source.items():
        mech = mechs[0]
        evidence = mech.get('evidence', {})
        n_studies = evidence.get('n_studies', 1) or 1
        grade = get_grade(n_studies)

        grade_before[evidence.get('quality_rating', 'C')] += 1

        if grade in ['A', 'B']:
            # Keep - single source but already strong evidence
            grade_after[grade] += 1

            category = mech.get('category', 'general')
            cat_dir = CONSOLIDATED_DIR / category
            cat_dir.mkdir(exist_ok=True)

            # Correct the grade if needed
            mech['evidence']['quality_rating'] = grade
            mech['last_updated'] = datetime.now().strftime('%Y-%m-%d')

            filename = f"{normalize_node_id(mech.get('id', pathway_key))}.yaml"
            with open(cat_dir / filename, 'w', encoding='utf-8') as f:
                yaml.dump(mech, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            consolidated_count += 1
        else:
            # Discard - single source C-rated
            category = mech.get('category', 'general')
            cat_dir = DISCARDED_DIR / category
            cat_dir.mkdir(exist_ok=True)

            filename = f"{normalize_node_id(mech.get('id', pathway_key))}.yaml"
            with open(cat_dir / filename, 'w', encoding='utf-8') as f:
                yaml.dump(mech, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            discarded_count += 1

    # Report
    print("\n4. Results:")
    print(f"   Consolidated mechanisms: {consolidated_count}")
    print(f"   Discarded (single C): {discarded_count}")
    print(f"   Upgraded to A/B: {upgraded_count}")

    print("\n   Grade distribution BEFORE:")
    for g in ['A', 'B', 'C']:
        print(f"     {g}: {grade_before.get(g, 0)}")

    print("\n   Grade distribution AFTER (consolidated only):")
    for g in ['A', 'B', 'C']:
        print(f"     {g}: {grade_after.get(g, 0)}")

    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'input': {
            'total_mechanisms': len(mechanisms),
            'unique_pathways': len(pathways),
            'single_source': len(single_source),
            'multi_source': len(multi_source),
        },
        'output': {
            'consolidated': consolidated_count,
            'discarded': discarded_count,
            'upgraded_to_ab': upgraded_count,
        },
        'grade_before': dict(grade_before),
        'grade_after': dict(grade_after),
    }

    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n   Report saved: {REPORT_PATH}")
    print(f"   Consolidated: {CONSOLIDATED_DIR}")
    print(f"   Discarded: {DISCARDED_DIR}")


if __name__ == "__main__":
    main()
