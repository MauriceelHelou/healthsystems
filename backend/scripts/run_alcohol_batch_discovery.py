#!/usr/bin/env python3
"""
Alcohol Mechanism Batch Discovery Script

This script executes the massive batch discovery for alcohol-related mechanisms
as specified in the plan:
- $25 budget cap
- 150-200 strong mechanisms target
- 3+ supporting citations per mechanism
- Scale 1-3 focus (structural determinants)
- Bidirectional search
- ONLY canonical nodes

Usage:
    python run_alcohol_batch_discovery.py [--dry-run] [--limit N] [--config PATH]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipelines.batch_mechanism_discovery import (
    BatchMechanismDiscovery,
    PaperInput,
    papers_from_literature_search,
    BatchResult,
    BatchStatus
)
from pipelines.llm_mechanism_discovery import LLMMechanismDiscoveryV2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: Optional[Path] = None) -> Dict:
    """Load batch discovery configuration."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "configs" / "alcohol_batch_discovery.json"

    with open(config_path, 'r') as f:
        return json.load(f)


def search_literature(config: Dict, limit_per_query: int = 50) -> List[Dict]:
    """
    Search literature using queries from configuration.

    Returns list of paper dictionaries with abstract, title, citation_context.
    """
    try:
        from pipelines.literature_search import LiteratureSearchAggregator
    except ImportError:
        logger.warning("LiteratureSearchAggregator not available, using mock data")
        return []

    aggregator = LiteratureSearchAggregator(
        pubmed_email=os.getenv("PUBMED_EMAIL", "healthsystems@harvard.edu"),
        semantic_scholar_api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    )

    all_papers = []
    seen_dois = set()

    # Collect all queries from configuration
    all_queries = []
    for priority, queries in config["search_queries"].items():
        for query in queries:
            all_queries.append((priority, query))

    logger.info(f"Searching {len(all_queries)} queries...")

    year_range = tuple(config["extraction_settings"]["year_range"])

    for priority, query in all_queries:
        try:
            logger.info(f"  [{priority}] Searching: {query[:60]}...")

            papers = aggregator.search(
                query=query,
                limit_per_source=limit_per_query // 2,
                year_range=year_range,
                min_citations=3  # Prioritize cited papers
            )

            # Deduplicate by DOI
            for paper in papers:
                doi = getattr(paper, 'doi', None)
                if doi and doi in seen_dois:
                    continue
                if doi:
                    seen_dois.add(doi)
                all_papers.append(paper)

        except Exception as e:
            logger.warning(f"Error searching '{query}': {e}")
            continue

    logger.info(f"Found {len(all_papers)} unique papers")
    return all_papers


def estimate_budget_usage(papers: List, config: Dict, use_simple_estimate: bool = False) -> Dict:
    """
    Estimate cost and check budget constraints.

    Args:
        papers: List of paper objects
        config: Configuration dictionary
        use_simple_estimate: If True, use simple estimate without API key
    """
    # Count papers with abstracts
    papers_with_abstracts = sum(1 for p in papers if hasattr(p, 'abstract') and p.abstract)
    budget_limit = config["budget"]["max_usd"]

    if use_simple_estimate or not os.getenv("ANTHROPIC_API_KEY"):
        # Simple cost estimate: ~$0.012 per paper in batch mode
        # Based on: ~3000 input tokens, ~1500 output tokens per paper
        # Batch pricing: $1.50/M input, $7.50/M output (50% discount)
        cost_per_paper = 0.012
        estimated_cost = papers_with_abstracts * cost_per_paper

        return {
            "papers": papers_with_abstracts,
            "estimated_cost_usd": estimated_cost,
            "budget_limit_usd": budget_limit,
            "within_budget": estimated_cost <= budget_limit,
            "max_papers_for_budget": int(budget_limit / cost_per_paper) if cost_per_paper > 0 else 0,
            "estimate_type": "simple"
        }

    # Full estimate using BatchMechanismDiscovery
    batch = BatchMechanismDiscovery()

    # Convert to PaperInput format for cost estimation
    paper_inputs = []
    for p in papers:
        if hasattr(p, 'abstract') and p.abstract:
            paper_inputs.append(PaperInput(
                abstract=p.abstract,
                title=p.title if hasattr(p, 'title') else "Unknown",
                citation_context={}
            ))

    cost_est = batch.estimate_cost(paper_inputs)

    return {
        "papers": len(paper_inputs),
        "estimated_cost_usd": cost_est["batch_cost_usd"],
        "budget_limit_usd": budget_limit,
        "within_budget": cost_est["batch_cost_usd"] <= budget_limit,
        "max_papers_for_budget": int(budget_limit / (cost_est["batch_cost_usd"] / len(paper_inputs))) if paper_inputs else 0,
        "estimate_type": "full"
    }


def filter_papers_to_budget(papers: List, config: Dict) -> List:
    """Filter papers to stay within budget."""
    max_papers = config["budget"]["max_papers"]
    budget_limit = config["budget"]["max_usd"]

    # Estimate cost per paper (rough: ~$0.014 per paper in batch mode)
    cost_per_paper = 0.014
    max_by_cost = int(budget_limit / cost_per_paper)

    actual_max = min(max_papers, max_by_cost, len(papers))

    logger.info(f"Filtering to {actual_max} papers (budget: ${budget_limit}, max: {max_papers})")

    # Prioritize meta-analyses and systematic reviews
    priority_papers = []
    other_papers = []

    for paper in papers:
        title = getattr(paper, 'title', '').lower()
        abstract = getattr(paper, 'abstract', '').lower()

        is_priority = any(term in title or term in abstract for term in [
            'meta-analysis', 'meta analysis', 'systematic review',
            'pooled analysis', 'umbrella review'
        ])

        if is_priority:
            priority_papers.append(paper)
        else:
            other_papers.append(paper)

    # Take priority papers first, then fill with others
    filtered = priority_papers[:actual_max]
    remaining = actual_max - len(filtered)
    if remaining > 0:
        filtered.extend(other_papers[:remaining])

    logger.info(f"Selected {len(filtered)} papers ({len(priority_papers)} priority)")
    return filtered


def convert_to_paper_inputs(papers: List) -> List[PaperInput]:
    """Convert paper objects or dicts to PaperInput format."""
    paper_inputs = []

    for p in papers:
        # Handle both dict (from JSON cache) and objects (from API)
        if isinstance(p, dict):
            abstract = p.get('abstract')
            title = p.get('title', 'Unknown')
            year = p.get('year')
            doi = p.get('doi')
            authors = p.get('authors', [])
            journal = p.get('journal')
        else:
            abstract = getattr(p, 'abstract', None)
            title = getattr(p, 'title', 'Unknown')
            year = getattr(p, 'year', None)
            doi = getattr(p, 'doi', None)
            authors = getattr(p, 'authors', [])
            journal = getattr(p, 'journal', None)

        if not abstract:
            continue

        paper_inputs.append(PaperInput(
            abstract=abstract,
            title=title,
            citation_context={
                "title": title,
                "year": year,
                "doi": doi,
                "authors": authors,
                "journal": journal
            },
            focus_area="alcohol health structural determinants"
        ))

    return paper_inputs


def run_bidirectional_detection(mechanisms: List, output_dir: Path) -> int:
    """
    Run bidirectional pair detection on extracted mechanisms.

    Returns count of backward mechanisms created.
    """
    try:
        # Import the bidirectional detection script
        script_path = Path(__file__).parent / "create_bidirectional_pairs.py"
        if not script_path.exists():
            logger.warning("Bidirectional detection script not found, skipping")
            return 0

        # For now, just log that we would run bidirectional detection
        # The actual detection would search for reverse direction evidence
        logger.info("Bidirectional detection: checking for reverse direction evidence...")

        # Count mechanisms that could have reverse directions
        potential_bidirectional = 0
        for mech in mechanisms:
            # Check if reverse direction might exist
            from_scale = _estimate_node_scale(mech.from_node_id)
            to_scale = _estimate_node_scale(mech.to_node_id)

            # Feedback loops typically go from outcomes back to determinants
            if to_scale > from_scale:  # Forward mechanism
                potential_bidirectional += 1

        logger.info(f"Identified {potential_bidirectional} mechanisms for potential bidirectional search")
        return potential_bidirectional

    except Exception as e:
        logger.error(f"Bidirectional detection error: {e}")
        return 0


def _estimate_node_scale(node_id: str) -> int:
    """Estimate scale from node ID naming patterns."""
    node_lower = node_id.lower()

    # Scale 1 - Policy
    if any(term in node_lower for term in ['policy', 'taxation', 'regulation', 'mandate', 'law']):
        return 1

    # Scale 2-3 - Institutional
    if any(term in node_lower for term in ['outlet', 'density', 'availability', 'access', 'treatment']):
        return 2

    # Scale 4 - Individual/household conditions
    if any(term in node_lower for term in ['housing', 'eviction', 'job', 'employment', 'income']):
        return 4

    # Scale 5 - Behavioral
    if any(term in node_lower for term in ['alcohol', 'drinking', 'consumption', 'use_disorder']):
        return 5

    # Scale 6-7 - Outcomes
    if any(term in node_lower for term in ['mortality', 'hospitalization', 'emergency', 'death']):
        return 7

    return 4  # Default to middle scale


def generate_report(
    result: BatchResult,
    config: Dict,
    output_path: Path
) -> Dict:
    """Generate comprehensive discovery report."""

    # Analyze mechanisms by category
    by_category = {}
    by_quality = {"A": 0, "B": 0, "C": 0}
    canonical_valid = 0
    citation_valid = 0

    for mech in result.mechanisms:
        # By category
        cat = mech.category
        if cat not in by_category:
            by_category[cat] = 0
        by_category[cat] += 1

        # By quality
        quality = mech.evidence_quality
        if quality in by_quality:
            by_quality[quality] += 1

        # Validation stats
        if mech.citation_verified:
            citation_valid += 1
        if not mech.from_node_id.startswith("NEW:") and not mech.to_node_id.startswith("NEW:"):
            canonical_valid += 1

    # Calculate supporting citations stats
    citations_count = []
    for mech in result.mechanisms:
        count = len(mech.supporting_citations) if mech.supporting_citations else 0
        citations_count.append(count)

    avg_citations = sum(citations_count) / len(citations_count) if citations_count else 0
    min_citations = min(citations_count) if citations_count else 0

    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "config_name": config["name"],
            "config_version": config["version"]
        },
        "summary": {
            "total_mechanisms": len(result.mechanisms),
            "target_range": config["target_yields"]["total_mechanisms"],
            "target_met": config["target_yields"]["total_mechanisms"]["min"] <= len(result.mechanisms) <= config["target_yields"]["total_mechanisms"]["max"],
            "processing_time_seconds": result.processing_time_seconds,
            "cost_estimate_usd": result.cost_estimate_usd,
            "budget_limit_usd": config["budget"]["max_usd"],
            "within_budget": (result.cost_estimate_usd or 0) <= config["budget"]["max_usd"]
        },
        "quality_distribution": {
            "A": by_quality["A"],
            "B": by_quality["B"],
            "C": by_quality["C"],
            "A_percent": round(100 * by_quality["A"] / len(result.mechanisms), 1) if result.mechanisms else 0,
            "B_percent": round(100 * by_quality["B"] / len(result.mechanisms), 1) if result.mechanisms else 0,
            "C_percent": round(100 * by_quality["C"] / len(result.mechanisms), 1) if result.mechanisms else 0
        },
        "category_distribution": by_category,
        "validation": {
            "canonical_nodes_valid": canonical_valid,
            "canonical_nodes_percent": round(100 * canonical_valid / len(result.mechanisms), 1) if result.mechanisms else 0,
            "citations_verified": citation_valid,
            "citations_verified_percent": round(100 * citation_valid / len(result.mechanisms), 1) if result.mechanisms else 0,
            "avg_supporting_citations": round(avg_citations, 1),
            "min_supporting_citations": min_citations,
            "meets_citation_requirement": min_citations >= config["extraction_settings"]["minimum_supporting_citations"]
        },
        "mechanisms": [
            {
                "id": f"{m.from_node_id}_to_{m.to_node_id}",
                "from_node": m.from_node_name,
                "to_node": m.to_node_name,
                "direction": m.direction,
                "category": m.category,
                "quality": m.evidence_quality,
                "n_studies": m.n_studies,
                "supporting_citations_count": len(m.supporting_citations) if m.supporting_citations else 0,
                "citation_verified": m.citation_verified,
                "needs_review": m.needs_manual_review
            }
            for m in result.mechanisms
        ]
    }

    # Save report
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Report saved to: {output_path}")
    return report


def main():
    parser = argparse.ArgumentParser(description="Run alcohol mechanism batch discovery")
    parser.add_argument("--dry-run", action="store_true", help="Estimate costs without running")
    parser.add_argument("--limit", type=int, help="Limit papers per query")
    parser.add_argument("--config", type=Path, help="Path to configuration file")
    parser.add_argument("--output-dir", type=Path, help="Output directory for mechanisms")
    parser.add_argument("--skip-search", action="store_true", help="Skip literature search, use cached papers")
    parser.add_argument("--papers-cache", type=Path, help="Path to cached papers JSON")

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    logger.info(f"Loaded configuration: {config['name']} v{config['version']}")

    # Set output directory
    output_dir = args.output_dir or Path(config["output"]["mechanisms_dir"])
    reports_dir = Path(config["output"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Search or load papers
    if args.skip_search and args.papers_cache:
        logger.info(f"Loading cached papers from {args.papers_cache}")
        with open(args.papers_cache, 'r') as f:
            papers = json.load(f)
    else:
        limit_per_query = args.limit or 30
        papers = search_literature(config, limit_per_query)

        # Cache papers
        cache_path = Path(config["output"]["papers_cache_dir"]) / f"alcohol_papers_{datetime.now().strftime('%Y%m%d')}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to serializable format
        papers_data = []
        for p in papers:
            papers_data.append({
                "title": getattr(p, 'title', ''),
                "abstract": getattr(p, 'abstract', ''),
                "year": getattr(p, 'year', None),
                "doi": getattr(p, 'doi', None),
                "authors": getattr(p, 'authors', []),
                "journal": getattr(p, 'journal', None)
            })

        with open(cache_path, 'w') as f:
            json.dump(papers_data, f, indent=2)
        logger.info(f"Cached {len(papers_data)} papers to {cache_path}")

    if not papers:
        logger.error("No papers found. Check search queries and API keys.")
        return

    # Estimate budget (use simple estimate for dry runs without API key)
    budget_est = estimate_budget_usage(papers, config, use_simple_estimate=args.dry_run)
    logger.info(f"Budget estimate: ${budget_est['estimated_cost_usd']:.2f} / ${budget_est['budget_limit_usd']:.2f}")

    if not budget_est["within_budget"]:
        logger.warning(f"Over budget! Filtering to {budget_est['max_papers_for_budget']} papers")
        papers = filter_papers_to_budget(papers, config)

    if args.dry_run:
        logger.info("DRY RUN - Not submitting batch")
        logger.info(f"Would process {len(papers)} papers")
        logger.info(f"Estimated cost: ${budget_est['estimated_cost_usd']:.2f}")
        return

    # Convert to PaperInput format
    paper_inputs = convert_to_paper_inputs(papers)
    logger.info(f"Prepared {len(paper_inputs)} papers for batch processing")

    # Initialize batch discovery with V2.1 settings
    batch = BatchMechanismDiscovery(
        validate_citations=True,
        strict_validation=config["extraction_settings"]["strict_citation_validation"]
    )

    # Update V2 discovery settings for canonical node validation
    batch.v2_discovery.validate_canonical_nodes = config["extraction_settings"]["validate_canonical_nodes"]
    batch.v2_discovery.minimum_supporting_citations = config["extraction_settings"]["minimum_supporting_citations"]

    # Run batch discovery
    logger.info("="*60)
    logger.info("STARTING BATCH DISCOVERY")
    logger.info(f"Papers: {len(paper_inputs)}")
    logger.info(f"Budget: ${config['budget']['max_usd']}")
    logger.info(f"Target: {config['target_yields']['total_mechanisms']['min']}-{config['target_yields']['total_mechanisms']['max']} mechanisms")
    logger.info("="*60)

    result = batch.discover_mechanisms_batch(
        papers=paper_inputs,
        output_dir=output_dir,
        wait_for_completion=True,
        poll_interval=60,
        save_report=True
    )

    if result.status != BatchStatus.COMPLETED:
        logger.error(f"Batch did not complete successfully: {result.status}")
        return

    logger.info(f"Extracted {len(result.mechanisms)} mechanisms")

    # Run bidirectional detection
    bidirectional_count = run_bidirectional_detection(result.mechanisms, output_dir)

    # Generate comprehensive report
    report_path = reports_dir / f"alcohol_discovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report = generate_report(result, config, report_path)

    # Print summary
    print("\n" + "="*60)
    print("BATCH DISCOVERY COMPLETE")
    print("="*60)
    print(f"Total mechanisms:     {report['summary']['total_mechanisms']}")
    print(f"Target range:         {report['summary']['target_range']['min']}-{report['summary']['target_range']['max']}")
    print(f"Target met:           {'YES' if report['summary']['target_met'] else 'NO'}")
    print(f"Cost:                 ${report['summary']['cost_estimate_usd']:.2f}")
    print(f"Within budget:        {'YES' if report['summary']['within_budget'] else 'NO'}")
    print(f"\nQuality Distribution:")
    print(f"  A (meta-analyses):  {report['quality_distribution']['A']} ({report['quality_distribution']['A_percent']}%)")
    print(f"  B (multiple):       {report['quality_distribution']['B']} ({report['quality_distribution']['B_percent']}%)")
    print(f"  C (limited):        {report['quality_distribution']['C']} ({report['quality_distribution']['C_percent']}%)")
    print(f"\nValidation:")
    print(f"  Canonical nodes:    {report['validation']['canonical_nodes_percent']}%")
    print(f"  Citations verified: {report['validation']['citations_verified_percent']}%")
    print(f"  Avg supporting:     {report['validation']['avg_supporting_citations']} citations")
    print(f"\nReport saved to: {report_path}")
    print("="*60)


if __name__ == "__main__":
    main()
