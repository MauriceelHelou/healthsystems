#!/usr/bin/env python3
"""
Analyze mechanism quality ratings and identify issues.

This script examines the mechanism bank to understand:
1. Why so many mechanisms are C-rated
2. Which mechanisms are misrated (wrong grade for n_studies)
3. Duplicate mechanisms from different papers
4. Recommendations for quality thresholds
"""

import os
import yaml
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import re

def load_mechanisms(mechanism_dir: Path) -> List[Dict]:
    """Load all mechanisms from YAML files."""
    mechanisms = []

    for yaml_file in mechanism_dir.rglob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            data['_file'] = str(yaml_file.relative_to(mechanism_dir))
            mechanisms.append(data)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return mechanisms


def get_correct_grade(n_studies: int) -> str:
    """Determine correct grade based on n_studies."""
    if n_studies is None or n_studies == 0:
        return 'C'
    elif n_studies >= 5:
        return 'A'
    elif n_studies >= 3:
        return 'B'
    else:
        return 'C'


def analyze_quality_distribution(mechanisms: List[Dict]) -> Dict:
    """Analyze quality rating distribution."""
    stats = {
        'total': len(mechanisms),
        'by_quality': defaultdict(int),
        'by_n_studies': defaultdict(int),
        'by_category': defaultdict(int),
        'misrated': [],
        'correctly_rated': [],
        'no_citation': [],
        'duplicate_pathways': defaultdict(list),
    }

    for m in mechanisms:
        evidence = m.get('evidence', {})
        quality = evidence.get('quality_rating', 'unknown')
        n_studies = evidence.get('n_studies', 0)
        citation = evidence.get('primary_citation', '')
        category = m.get('category', 'unknown')

        # Handle None
        if n_studies is None:
            n_studies = 0

        stats['by_quality'][quality] += 1
        stats['by_n_studies'][n_studies] += 1
        stats['by_category'][category] += 1

        # Check for misrating
        correct_grade = get_correct_grade(n_studies)
        if quality != correct_grade and quality in ['A', 'B', 'C']:
            stats['misrated'].append({
                'id': m.get('id', 'unknown'),
                'file': m.get('_file', ''),
                'current_grade': quality,
                'correct_grade': correct_grade,
                'n_studies': n_studies,
                'citation': citation[:100] if citation else '',
            })
        else:
            stats['correctly_rated'].append(m)

        # Check for missing citations
        if not citation or citation.strip() == '':
            stats['no_citation'].append(m.get('id', 'unknown'))

        # Track pathway duplicates
        from_node = m.get('from_node', {}).get('node_id', '')
        to_node = m.get('to_node', {}).get('node_id', '')
        if from_node and to_node:
            pathway_key = f"{from_node} -> {to_node}"
            stats['duplicate_pathways'][pathway_key].append({
                'id': m.get('id'),
                'file': m.get('_file'),
                'n_studies': n_studies,
                'quality': quality,
            })

    return stats


def find_consolidation_candidates(stats: Dict) -> List[Dict]:
    """Find mechanisms that could be consolidated."""
    candidates = []

    for pathway, mechs in stats['duplicate_pathways'].items():
        if len(mechs) > 1:
            # Multiple mechanisms for same pathway
            total_studies = sum(m['n_studies'] for m in mechs if m['n_studies'])
            candidates.append({
                'pathway': pathway,
                'count': len(mechs),
                'mechanisms': mechs,
                'total_studies_if_merged': total_studies,
                'could_upgrade_to': get_correct_grade(total_studies),
            })

    return sorted(candidates, key=lambda x: -x['count'])


def print_report(stats: Dict, consolidation: List[Dict]):
    """Print analysis report."""
    print("=" * 80)
    print("MECHANISM QUALITY ANALYSIS REPORT")
    print("=" * 80)

    print(f"\n📊 OVERVIEW")
    print("-" * 40)
    print(f"Total mechanisms: {stats['total']}")

    print(f"\n📈 QUALITY DISTRIBUTION")
    print("-" * 40)
    for grade in ['A', 'B', 'C', 'unknown']:
        count = stats['by_quality'].get(grade, 0)
        pct = 100 * count / stats['total'] if stats['total'] > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {grade}: {count:5d} ({pct:5.1f}%) {bar}")

    print(f"\n📊 N_STUDIES DISTRIBUTION")
    print("-" * 40)
    n_studies_sorted = sorted(stats['by_n_studies'].items(), key=lambda x: -x[1])
    for n, count in n_studies_sorted[:10]:
        pct = 100 * count / stats['total']
        print(f"  n_studies={n}: {count:5d} ({pct:5.1f}%)")

    print(f"\n⚠️  MISRATED MECHANISMS")
    print("-" * 40)
    print(f"Total misrated: {len(stats['misrated'])}")

    # Group by error type
    should_be_a = [m for m in stats['misrated'] if m['correct_grade'] == 'A']
    should_be_b = [m for m in stats['misrated'] if m['correct_grade'] == 'B']

    print(f"  Should be A (n>=5 studies): {len(should_be_a)}")
    print(f"  Should be B (n=3-4 studies): {len(should_be_b)}")

    if should_be_a[:5]:
        print("\n  Examples that should be A:")
        for m in should_be_a[:5]:
            print(f"    - {m['id'][:50]}... (n={m['n_studies']}, currently {m['current_grade']})")

    print(f"\n🔄 CONSOLIDATION OPPORTUNITIES")
    print("-" * 40)
    multi_source = [c for c in consolidation if c['count'] >= 2]
    print(f"Pathways with multiple mechanisms: {len(multi_source)}")

    # Show top consolidation opportunities
    upgradeable = [c for c in multi_source if c['could_upgrade_to'] in ['A', 'B']]
    print(f"Could upgrade to A/B if consolidated: {len(upgradeable)}")

    if upgradeable[:5]:
        print("\n  Top consolidation opportunities:")
        for c in upgradeable[:5]:
            print(f"    - {c['pathway']}")
            print(f"      {c['count']} mechanisms, {c['total_studies_if_merged']} total studies → Grade {c['could_upgrade_to']}")

    print(f"\n🎯 RECOMMENDATIONS")
    print("-" * 40)

    c_only = stats['by_quality'].get('C', 0)
    a_b = stats['by_quality'].get('A', 0) + stats['by_quality'].get('B', 0)

    print(f"""
1. FIX MISRATING: {len(stats['misrated'])} mechanisms have wrong grades
   - Run regrade script to fix quality ratings based on n_studies

2. CONSOLIDATE DUPLICATES: {len(multi_source)} pathways have multiple sources
   - Merging could upgrade {len(upgradeable)} pathways to A/B level

3. ACCEPTANCE THRESHOLD OPTIONS:

   Option A - Strict (A/B only):
   - Keep: {a_b} mechanisms ({100*a_b/stats['total']:.1f}%)
   - Discard: {c_only} C-rated mechanisms

   Option B - After consolidation + regrade:
   - Estimated A/B: {a_b + len(upgradeable)} mechanisms
   - Much stronger evidence base

   Option C - Tiered weighting:
   - Keep all, but weight by quality in calculations
   - A: 1.0 weight, B: 0.7 weight, C: 0.3 weight
""")

    return {
        'total': stats['total'],
        'by_quality': dict(stats['by_quality']),
        'misrated_count': len(stats['misrated']),
        'consolidation_opportunities': len(multi_source),
        'upgradeable_if_consolidated': len(upgradeable),
    }


def main():
    mechanism_dir = Path(__file__).parent.parent.parent / 'mechanism-bank' / 'mechanisms'

    if not mechanism_dir.exists():
        print(f"Error: Mechanism directory not found: {mechanism_dir}")
        return

    print(f"Loading mechanisms from: {mechanism_dir}")
    mechanisms = load_mechanisms(mechanism_dir)

    print(f"Analyzing {len(mechanisms)} mechanisms...")
    stats = analyze_quality_distribution(mechanisms)
    consolidation = find_consolidation_candidates(stats)

    summary = print_report(stats, consolidation)

    # Save detailed report
    report_path = Path(__file__).parent.parent / 'reports' / 'quality_analysis.json'
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump({
            'summary': summary,
            'misrated': stats['misrated'][:100],  # First 100
            'consolidation_top': consolidation[:50],  # Top 50
        }, f, indent=2)

    print(f"\nDetailed report saved to: {report_path}")


if __name__ == "__main__":
    main()
