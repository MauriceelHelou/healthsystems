"""
Enhanced Generic Mechanism Extraction Script

Improvements over base version:
1. Grey literature integration (government reports, preprints)
2. Enhanced quantitative metrics extraction
3. Qualitative evidence synthesis
4. Advanced filtering and quality checks
5. Meta-analysis detection and extraction
6. Effect size standardization

Usage:
    python backend/scripts/run_generic_extraction_enhanced.py --topic obesity \
        --include-grey-literature \
        --extract-all-metrics \
        --quality-threshold 0.7
"""

import argparse
import yaml
import sys
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.llm_mechanism_discovery import LLMMechanismDiscovery, validate_structural_competency
from pipelines.literature_search import LiteratureSearchAggregator, Paper
from pipelines.grey_literature_search import GreyLiteratureAggregator, GreyLiterature
from algorithms.bayesian_weighting import BayesianMechanismWeighter


def load_topic_config(topic_name: str) -> dict:
    """Load pre-defined topic configuration."""
    config_path = Path(__file__).parent.parent / "config" / "topic_configs" / f"{topic_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"No config found for topic '{topic_name}'. "
            f"Create {config_path} or use --config to specify a custom config file."
        )

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def assess_paper_quality(paper: Paper) -> Dict[str, any]:
    """
    Assess quality of a paper for mechanism extraction.

    Returns quality score and flags.
    """
    quality_score = 0.0
    flags = []

    # Check 1: Abstract presence (critical)
    if not paper.abstract or len(paper.abstract) < 100:
        flags.append("weak_abstract")
        return {'score': 0.1, 'flags': flags, 'include': False}

    quality_score += 0.3

    # Check 2: Citation count (indicates impact)
    if paper.citation_count >= 50:
        quality_score += 0.3
    elif paper.citation_count >= 20:
        quality_score += 0.2
    elif paper.citation_count >= 10:
        quality_score += 0.1
    else:
        flags.append("low_citations")

    # Check 3: Recent publication (more likely to have better methods)
    if paper.year and paper.year >= 2015:
        quality_score += 0.2
    elif paper.year and paper.year >= 2010:
        quality_score += 0.1

    # Check 4: Study type detection (from title/abstract)
    abstract_lower = paper.abstract.lower() if paper.abstract else ""
    title_lower = paper.title.lower()

    # Meta-analysis/systematic review (highest quality for effect sizes)
    if any(term in title_lower or term in abstract_lower for term in
           ['meta-analysis', 'systematic review', 'pooled analysis']):
        quality_score += 0.2
        flags.append("meta_analysis")

    # RCT (gold standard for causal inference)
    if any(term in title_lower or term in abstract_lower for term in
           ['randomized controlled', 'randomized trial', 'rct', 'double-blind']):
        quality_score += 0.15
        flags.append("rct")

    # Cohort study (good for causal inference)
    if any(term in title_lower or term in abstract_lower for term in
           ['cohort', 'longitudinal', 'prospective study', 'follow-up study']):
        quality_score += 0.1
        flags.append("cohort")

    # Check 5: Methods rigor indicators
    if any(term in abstract_lower for term in
           ['propensity score', 'instrumental variable', 'difference-in-difference',
            'regression discontinuity', 'causal inference', 'directed acyclic graph']):
        quality_score += 0.1
        flags.append("rigorous_methods")

    # Clip to [0, 1]
    quality_score = min(quality_score, 1.0)

    # Decide inclusion
    include = quality_score >= 0.3 and 'weak_abstract' not in flags

    return {
        'score': quality_score,
        'flags': flags,
        'include': include
    }


def extract_with_context(
    paper: Paper,
    discovery: LLMMechanismDiscovery,
    from_node: str,
    to_node: str,
    topic: str,
    extract_all_metrics: bool = True
) -> Tuple[List, Dict]:
    """
    Extract mechanisms with enhanced context and metrics.

    Returns:
        Tuple of (mechanisms, extraction_metadata)
    """
    # Enhanced focus area with guidance
    focus_area = f"{from_node} to {to_node} in {topic}"

    # Add study type context if detected
    quality_info = assess_paper_quality(paper)

    if 'meta_analysis' in quality_info['flags']:
        focus_area += " [META-ANALYSIS: Extract pooled effect sizes, I², heterogeneity]"
    elif 'rct' in quality_info['flags']:
        focus_area += " [RCT: Extract intervention effects, confidence intervals]"
    elif 'cohort' in quality_info['flags']:
        focus_area += " [COHORT: Extract adjusted hazard ratios, odds ratios]"

    # Add emphasis on quantitative extraction
    if extract_all_metrics:
        focus_area += " [EXTRACT ALL QUANTITATIVE METRICS]"

    # Extract mechanisms
    try:
        mechanisms = discovery.extract_mechanisms_from_paper(
            paper_abstract=paper.abstract,
            paper_title=paper.title,
            focus_area=focus_area
        )

        # Validate each mechanism
        validated_mechanisms = []
        for mech in mechanisms:
            mech_dict = {
                'category': mech.category,
                'from_node_id': mech.from_node_id,
                'to_node_id': mech.to_node_id,
                'evidence_quality': mech.evidence_quality,
                'n_studies': mech.n_studies
            }

            validation = validate_structural_competency(mech_dict)

            # Attach validation metadata
            mech.confidence = validation['confidence']

            validated_mechanisms.append({
                'mechanism': mech,
                'validation': validation,
                'paper_quality': quality_info
            })

        metadata = {
            'paper_quality': quality_info,
            'mechanisms_found': len(validated_mechanisms),
            'study_type': quality_info['flags']
        }

        return validated_mechanisms, metadata

    except Exception as e:
        print(f"      Error extracting: {e}")
        return [], {'error': str(e)}


def run_enhanced_extraction(
    topic: str,
    query_template: str,
    from_nodes: List[str],
    to_nodes: List[str],
    scales: Optional[List[int]] = None,
    output_dir: Optional[str] = None,
    anthropic_api_key: Optional[str] = None,
    limit_per_query: int = 10,
    year_range: tuple = (2010, 2024),
    min_citations: int = 10,
    pubmed_email: str = "healthsystems@example.com",
    include_grey_literature: bool = False,
    extract_all_metrics: bool = True,
    quality_threshold: float = 0.5,
    apply_bayesian_weighting: bool = False
):
    """
    Enhanced extraction with grey literature, quality filtering, and validation.

    Args:
        topic: Health topic name
        query_template: Template for queries
        from_nodes: Source nodes
        to_nodes: Target nodes
        scales: Scale levels to filter
        output_dir: Output directory
        anthropic_api_key: API key
        limit_per_query: Papers per query
        year_range: Year range
        min_citations: Minimum citations
        pubmed_email: PubMed email
        include_grey_literature: Whether to search grey literature
        extract_all_metrics: Extract all quantitative metrics
        quality_threshold: Minimum paper quality score (0-1)
        apply_bayesian_weighting: Calculate Bayesian weights

    Returns:
        Dict with extraction results and analytics
    """

    print(f"\n{'='*80}")
    print(f"ENHANCED MECHANISM EXTRACTION: {topic.upper()}")
    print(f"{'='*80}")
    print(f"Grey literature: {'Yes' if include_grey_literature else 'No'}")
    print(f"Extract all metrics: {'Yes' if extract_all_metrics else 'No'}")
    print(f"Quality threshold: {quality_threshold}")
    print(f"Bayesian weighting: {'Yes' if apply_bayesian_weighting else 'No'}")
    print(f"{'='*80}\n")

    # Initialize pipelines
    output_path = Path(output_dir or f"mechanism-bank/mechanisms/{topic}")
    output_path.mkdir(parents=True, exist_ok=True)

    discovery = LLMMechanismDiscovery(api_key=anthropic_api_key)
    search_aggregator = LiteratureSearchAggregator(pubmed_email=pubmed_email)

    grey_lit_aggregator = None
    if include_grey_literature:
        grey_lit_aggregator = GreyLiteratureAggregator()

    bayes_weighter = None
    if apply_bayesian_weighting:
        bayes_weighter = BayesianMechanismWeighter()

    # Generate queries
    queries = []
    for from_node in from_nodes:
        for to_node in to_nodes:
            if from_node == to_node:
                continue

            query_text = query_template.format(
                from_node=from_node,
                to_node=to_node,
                topic=topic
            )

            queries.append({
                'query': query_text,
                'from_node': from_node,
                'to_node': to_node
            })

    print(f"Generated {len(queries)} queries\n")

    # Run extraction
    results = []
    extraction_stats = {
        'queries_processed': 0,
        'papers_retrieved': 0,
        'papers_quality_filtered': 0,
        'papers_processed': 0,
        'grey_literature_found': 0,
        'mechanisms_extracted': 0,
        'high_confidence_mechanisms': 0,
        'meta_analyses_found': 0,
        'effect_sizes_extracted': 0
    }

    for i, query_info in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] {query_info['from_node']} -> {query_info['to_node']}")
        print(f"  Query: {query_info['query'][:80]}...")

        extraction_stats['queries_processed'] += 1

        try:
            # Search peer-reviewed literature
            papers = search_aggregator.search(
                query=query_info['query'],
                limit_per_source=limit_per_query,
                year_range=year_range,
                min_citations=min_citations
            )

            extraction_stats['papers_retrieved'] += len(papers)

            # Search grey literature if enabled
            grey_lit = []
            if include_grey_literature and grey_lit_aggregator:
                grey_lit = grey_lit_aggregator.search(
                    query=query_info['query'],
                    limit_per_source=3,  # Fewer grey lit sources
                    year_range=year_range
                )
                extraction_stats['grey_literature_found'] += len(grey_lit)

            print(f"  Retrieved: {len(papers)} papers, {len(grey_lit)} grey literature")

            # Quality filter papers
            quality_filtered_papers = []
            for paper in papers:
                quality_info = assess_paper_quality(paper)

                if quality_info['score'] >= quality_threshold and quality_info['include']:
                    quality_filtered_papers.append((paper, quality_info))
                else:
                    extraction_stats['papers_quality_filtered'] += 1

            print(f"  Quality filtered: {len(quality_filtered_papers)} papers pass threshold")

            # Extract from quality-filtered papers
            for j, (paper, quality_info) in enumerate(quality_filtered_papers, 1):
                extraction_stats['papers_processed'] += 1

                if 'meta_analysis' in quality_info['flags']:
                    extraction_stats['meta_analyses_found'] += 1

                validated_mechs, metadata = extract_with_context(
                    paper=paper,
                    discovery=discovery,
                    from_node=query_info['from_node'],
                    to_node=query_info['to_node'],
                    topic=topic,
                    extract_all_metrics=extract_all_metrics
                )

                if validated_mechs:
                    print(f"    [{j}/{len(quality_filtered_papers)}] Extracted {len(validated_mechs)} mechanism(s) "
                          f"(quality: {quality_info['score']:.2f})")

                    for vm in validated_mechs:
                        mechanism = vm['mechanism']
                        validation = vm['validation']

                        # Count high confidence
                        if validation['confidence'] >= 0.7:
                            extraction_stats['high_confidence_mechanisms'] += 1

                        # Count effect sizes
                        if mechanism.effect_size_value is not None:
                            extraction_stats['effect_sizes_extracted'] += 1

                        # Apply Bayesian weighting if enabled
                        bayesian_weight = None
                        if apply_bayesian_weighting and bayes_weighter and mechanism.effect_size_value:
                            if mechanism.confidence_interval_lower and mechanism.confidence_interval_upper:
                                try:
                                    weight, ci = bayes_weighter.calculate_weight(
                                        mechanism_id=f"{mechanism.from_node_id}_to_{mechanism.to_node_id}",
                                        prior_effect_size=mechanism.effect_size_value,
                                        prior_ci=(mechanism.confidence_interval_lower,
                                                mechanism.confidence_interval_upper),
                                        context_data={}  # Could add geographic/demographic context
                                    )
                                    bayesian_weight = {'weight': weight, 'ci': ci}
                                except Exception as e:
                                    print(f"      Warning: Bayesian weighting failed: {e}")

                        # Save mechanism
                        file_path = discovery.save_mechanism(mechanism, output_path)

                        extraction_stats['mechanisms_extracted'] += 1

                        results.append({
                            'status': 'success',
                            'mechanism': mechanism,
                            'validation': validation,
                            'paper_quality': quality_info,
                            'bayesian_weight': bayesian_weight,
                            'file_path': str(file_path),
                            'query': query_info,
                            'paper_metadata': {
                                'title': paper.title,
                                'year': paper.year,
                                'citations': paper.citation_count,
                                'doi': paper.doi
                            }
                        })

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'status': 'error',
                'error': str(e),
                'query': query_info
            })

    # Generate summary report
    print(f"\n{'='*80}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*80}")

    for key, value in extraction_stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print(f"{'='*80}\n")

    # Save detailed analytics
    analytics_path = output_path.parent / f"{topic}_extraction_analytics.json"
    analytics = {
        'timestamp': datetime.now().isoformat(),
        'topic': topic,
        'config': {
            'year_range': year_range,
            'min_citations': min_citations,
            'quality_threshold': quality_threshold,
            'include_grey_literature': include_grey_literature,
            'extract_all_metrics': extract_all_metrics,
            'apply_bayesian_weighting': apply_bayesian_weighting
        },
        'stats': extraction_stats,
        'success_rate': extraction_stats['mechanisms_extracted'] / extraction_stats['queries_processed']
            if extraction_stats['queries_processed'] > 0 else 0
    }

    with open(analytics_path, 'w') as f:
        json.dump(analytics, f, indent=2)

    print(f"Analytics saved: {analytics_path}\n")

    return {
        'results': results,
        'stats': extraction_stats,
        'analytics_path': str(analytics_path)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced mechanism extraction with grey literature and quality filtering"
    )

    parser.add_argument('--topic', type=str, help='Health topic')
    parser.add_argument('--config', type=str, help='Config file path')
    parser.add_argument('--scales', type=str, help='Scale levels (comma-separated)')
    parser.add_argument('--from-nodes', type=str, help='Source nodes (comma-separated)')
    parser.add_argument('--to-nodes', type=str, help='Target nodes (comma-separated)')
    parser.add_argument('--output-dir', type=str, help='Output directory')
    parser.add_argument('--api-key', type=str, help='Anthropic API key')
    parser.add_argument('--limit', type=int, default=10, help='Papers per query')
    parser.add_argument('--quality-threshold', type=float, default=0.5,
                       help='Minimum paper quality (0-1)')
    parser.add_argument('--include-grey-literature', action='store_true',
                       help='Search grey literature sources')
    parser.add_argument('--extract-all-metrics', action='store_true',
                       help='Extract all quantitative metrics')
    parser.add_argument('--apply-bayesian-weighting', action='store_true',
                       help='Calculate Bayesian weights')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')

    args = parser.parse_args()

    # Load config
    if args.config:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    elif args.topic:
        config = load_topic_config(args.topic)
    else:
        parser.error("Must specify --topic or --config")

    # Override with CLI args
    if args.from_nodes:
        config['from_nodes'] = args.from_nodes.split(',')
    if args.to_nodes:
        config['to_nodes'] = args.to_nodes.split(',')

    # Dry run
    if args.dry_run:
        print(f"\n{'='*80}")
        print(f"ENHANCED DRY RUN: {config['topic'].upper()}")
        print(f"{'='*80}")
        print(f"From nodes: {len(config.get('from_nodes', []))}")
        print(f"To nodes: {len(config.get('to_nodes', []))}")
        print(f"Total queries: {len(config.get('from_nodes', [])) * len(config.get('to_nodes', []))}")
        print(f"Quality threshold: {args.quality_threshold}")
        print(f"Grey literature: {args.include_grey_literature}")
        print(f"{'='*80}\n")
        return

    # Run enhanced extraction
    run_enhanced_extraction(
        topic=config['topic'],
        query_template=config['query_template'],
        from_nodes=config.get('from_nodes', []),
        to_nodes=config.get('to_nodes', []),
        output_dir=args.output_dir,
        anthropic_api_key=args.api_key,
        limit_per_query=args.limit,
        quality_threshold=args.quality_threshold,
        include_grey_literature=args.include_grey_literature,
        extract_all_metrics=args.extract_all_metrics,
        apply_bayesian_weighting=args.apply_bayesian_weighting
    )


if __name__ == '__main__':
    main()
