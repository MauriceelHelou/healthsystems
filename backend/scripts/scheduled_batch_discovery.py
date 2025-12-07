#!/usr/bin/env python3
"""
Scheduled Batch Discovery Script

Run mechanism discovery on a schedule (nightly, weekly) using Claude's Batch API
for 50% cost savings. Designed for cron jobs or task schedulers.

Usage:
    # Single topic discovery
    python scheduled_batch_discovery.py --topic "housing quality respiratory health"

    # Multiple topics from config file
    python scheduled_batch_discovery.py --config discovery_topics.json

    # Resume/check existing batch
    python scheduled_batch_discovery.py --check-batch msgbatch_xxx

    # List recent batches
    python scheduled_batch_discovery.py --list-batches

Scheduling Examples:
    # Cron (Linux/Mac) - Run nightly at 2 AM
    0 2 * * * cd /path/to/healthsystems && python backend/scripts/scheduled_batch_discovery.py --config topics.json

    # Task Scheduler (Windows) - Run weekly
    schtasks /create /tn "MechanismDiscovery" /tr "python backend/scripts/scheduled_batch_discovery.py --config topics.json" /sc weekly /d SUN /st 02:00

    # GitHub Actions - See .github/workflows/mechanism-discovery.yml
"""

import argparse
import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / "backend" / ".env")

from pipelines.batch_mechanism_discovery import (
    BatchMechanismDiscovery,
    PaperInput,
    BatchResult,
    BatchStatus,
    papers_from_literature_search
)
from pipelines.consolidated_batch_discovery import ConsolidatedBatchDiscovery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / "backend" / "logs" / "batch_discovery.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)


# Default discovery topics targeting CANONICAL NODE PAIRS
# Each topic targets mechanisms between specific nodes in canonical_nodes.json
# Queries are constructed from canonical node names to discover causal pathways
#
# CANONICAL NODE PAIRS TARGETED:
# 1. housing_cost_burden → emergency_department_visit_rate
# 2. food_insecurity_rate → diabetes_diagnosis
# 3. eviction_filing_rate → emergency_department_visit_rate
# 4. medicaid_expansion_status → all_cause_mortality_rate
# 5. ambient_air_pollution_pm2_5 → asthma_prevalence
# 6. incarceration_rate → all_cause_mortality_rate
# 7. primary_care_physician_density → avoidable_ed_visit_rate
# 8. minimum_wage_level → all_cause_mortality_rate
#
DEFAULT_TOPICS = [
    {
        # FROM: housing_cost_burden (Scale 3) → TO: emergency_department_visit_rate (Scale 5)
        "query": "housing cost burden emergency department utilization health outcomes meta-analysis OR systematic review",
        "category": "built_environment",
        "focus_area": "housing_cost_burden → emergency_department_visit_rate",
        "from_node": "housing_cost_burden",
        "to_node": "emergency_department_visit_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: food_insecurity_rate (Scale 3) → TO: diabetes_diagnosis (Scale 4)
        "query": "food insecurity diabetes glycemic control chronic disease meta-analysis",
        "category": "economic",
        "focus_area": "food_insecurity_rate → diabetes_diagnosis",
        "from_node": "food_insecurity_rate",
        "to_node": "diabetes_diagnosis",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: eviction_filing_rate (Scale 3) → TO: emergency_department_visit_rate (Scale 5)
        "query": "eviction housing displacement emergency department health outcomes systematic review",
        "category": "economic",
        "focus_area": "eviction_filing_rate → emergency_department_visit_rate",
        "from_node": "eviction_filing_rate",
        "to_node": "emergency_department_visit_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: medicaid_expansion_status (Scale 1) → TO: all_cause_mortality_rate (Scale 5)
        "query": "medicaid expansion mortality health outcomes meta-analysis",
        "category": "political",
        "focus_area": "medicaid_expansion_status → all_cause_mortality_rate",
        "from_node": "medicaid_expansion_status",
        "to_node": "all_cause_mortality_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: ambient_air_pollution_pm2_5 (Scale 2) → TO: asthma_prevalence_adults (Scale 4)
        "query": "air pollution PM2.5 asthma respiratory mortality meta-analysis",
        "category": "built_environment",
        "focus_area": "ambient_air_pollution_pm2_5 → asthma_prevalence",
        "from_node": "ambient_air_pollution_pm2_5_revised_consolidated_with_node_226",
        "to_node": "asthma_prevalence_adults_revised_terminology_standardized",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 20
    },
    {
        # FROM: incarceration_rate (Scale 2) → TO: all_cause_mortality_rate (Scale 5)
        "query": "incarceration prison jail mortality chronic disease health outcomes systematic review",
        "category": "social_environment",
        "focus_area": "incarceration_rate → all_cause_mortality_rate",
        "from_node": "incarceration_rate",
        "to_node": "all_cause_mortality_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: primary_care_physician_density (Scale 2) → TO: avoidable_ed_visit_rate (Scale 5)
        "query": "primary care physician density avoidable emergency department preventable hospitalization meta-analysis",
        "category": "healthcare_access",
        "focus_area": "primary_care_physician_density → avoidable_ed_visit_rate",
        "from_node": "primary_care_physician_density",
        "to_node": "avoidable_ed_visit_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    },
    {
        # FROM: minimum_wage_level (Scale 1) → TO: all_cause_mortality_rate (Scale 5)
        "query": "minimum wage health outcomes mortality morbidity systematic review",
        "category": "political",
        "focus_area": "minimum_wage_level → all_cause_mortality_rate",
        "from_node": "minimum_wage_level",
        "to_node": "all_cause_mortality_rate",
        "max_papers": 40,
        "year_range": [2000, 2024],
        "min_citations": 10
    }
]

# Extended year range configuration for deeper literature search
EXPANDED_SEARCH_CONFIG = {
    "default_year_range": (2000, 2024),  # Changed from (2015, 2024)
    "min_citations_by_age": {
        # Older papers need more citations to ensure quality
        "2000-2010": 50,
        "2011-2015": 25,
        "2016-2020": 10,
        "2021-2024": 3
    },
    "priority_publication_types": [
        "meta-analysis",
        "systematic review",
        "pooled analysis",
        "umbrella review"
    ],
    "search_modifiers": [
        "meta-analysis",
        "systematic review",
        "pooled analysis",
        "umbrella review",
        "Cochrane review"
    ]
}


class ScheduledBatchDiscovery:
    """
    Orchestrates scheduled batch discovery runs.

    Features:
    - Multi-topic discovery in single batch
    - Progress tracking and resumption
    - Cost reporting
    - Error handling with notifications
    - TWO MODES:
      1. Standard: Per-paper extraction (fast, may produce C-rated single-paper mechanisms)
      2. Consolidated: Two-pass extraction grouping papers by pathway (higher quality A/B mechanisms)
    """

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        report_dir: Optional[Path] = None,
        use_consolidated_mode: bool = False
    ):
        """
        Initialize scheduled discovery.

        Args:
            output_dir: Where to save mechanism YAML files
            report_dir: Where to save discovery reports
            use_consolidated_mode: If True, use two-pass consolidated extraction
                                   that groups papers by pathway before extraction.
                                   This produces higher quality A/B mechanisms but
                                   takes longer due to the two-pass approach.
        """
        self.output_dir = output_dir or PROJECT_ROOT / "mechanism-bank" / "mechanisms"
        self.report_dir = report_dir or PROJECT_ROOT / "backend" / "reports"
        self.use_consolidated_mode = use_consolidated_mode

        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT / "backend" / "logs").mkdir(parents=True, exist_ok=True)

        # Initialize batch client(s)
        self.batch_client = BatchMechanismDiscovery()
        if use_consolidated_mode:
            self.consolidated_client = ConsolidatedBatchDiscovery()
            logger.info("Using CONSOLIDATED MODE (two-pass extraction)")
        else:
            self.consolidated_client = None
            logger.info("Using STANDARD MODE (per-paper extraction)")

        # Track run metadata
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_stats = {
            "start_time": datetime.now().isoformat(),
            "topics_processed": 0,
            "papers_submitted": 0,
            "mechanisms_extracted": 0,
            "total_cost_usd": 0.0,
            "errors": [],
            "mode": "consolidated" if use_consolidated_mode else "standard"
        }

    def search_papers_for_topic(
        self,
        query: str,
        max_papers: int = 30,
        year_range: tuple = (2000, 2024),
        min_citations: int = 5,
        prioritize_meta_analyses: bool = True
    ) -> List:
        """
        Search for papers on a topic.

        Args:
            query: Search query
            max_papers: Maximum papers to retrieve
            year_range: (min_year, max_year)
            min_citations: Minimum citation count
            prioritize_meta_analyses: If True, boost meta-analyses in results

        Returns:
            List of Paper objects
        """
        try:
            from pipelines.literature_search import LiteratureSearchAggregator
        except ImportError:
            logger.error("literature_search module not found")
            return []

        aggregator = LiteratureSearchAggregator(
            pubmed_email=os.getenv("PUBMED_EMAIL", "healthsystems@example.com"),
            semantic_scholar_api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        )

        papers = aggregator.search(
            query=query,
            limit_per_source=max_papers // 2,
            year_range=year_range,
            min_citations=min_citations
        )

        # Prioritize meta-analyses and systematic reviews
        if prioritize_meta_analyses and papers:
            meta_keywords = ['meta-analysis', 'systematic review', 'pooled analysis', 'umbrella review']

            def is_meta_analysis(paper):
                title_lower = (paper.title or '').lower()
                abstract_lower = (paper.abstract or '').lower()
                return any(kw in title_lower or kw in abstract_lower for kw in meta_keywords)

            meta_papers = [p for p in papers if is_meta_analysis(p)]
            other_papers = [p for p in papers if not is_meta_analysis(p)]

            # Sort others by citations
            other_papers.sort(key=lambda p: getattr(p, 'citation_count', 0) or 0, reverse=True)

            # Put meta-analyses first
            papers = meta_papers + other_papers
            logger.info(f"Found {len(meta_papers)} meta-analyses/systematic reviews out of {len(papers)} papers")

        logger.info(f"Found {len(papers)} papers for query: {query}")
        return papers

    def run_discovery(
        self,
        topics: List[Dict],
        wait_for_completion: bool = True,
        year_range: tuple = (2000, 2024)
    ) -> BatchResult:
        """
        Run batch discovery for multiple topics.

        Args:
            topics: List of topic configs with query, category, focus_area, max_papers,
                   year_range (optional), min_citations (optional)
            wait_for_completion: Whether to wait for batch to complete
            year_range: Default year range for literature search (now 2000-2024)

        Returns:
            BatchResult with all extracted mechanisms
        """
        logger.info(f"Starting scheduled discovery run {self.run_id}")
        logger.info(f"Topics to process: {len(topics)}")
        logger.info(f"Default year range: {year_range}")

        all_papers = []

        # Collect papers from all topics
        for topic in topics:
            query = topic["query"]
            max_papers = topic.get("max_papers", 40)
            focus_area = topic.get("focus_area", topic.get("category", ""))
            # Allow topic-specific year range and citation thresholds
            topic_year_range = tuple(topic.get("year_range", year_range))
            topic_min_citations = topic.get("min_citations", 5)

            logger.info(f"Searching: {query}")
            logger.info(f"  Year range: {topic_year_range}, Min citations: {topic_min_citations}")

            papers = self.search_papers_for_topic(
                query=query,
                max_papers=max_papers,
                year_range=topic_year_range,
                min_citations=topic_min_citations,
                prioritize_meta_analyses=True
            )

            if papers:
                # Convert to PaperInput format with focus area
                paper_inputs = [
                    PaperInput(
                        abstract=p.abstract or "",
                        title=p.title,
                        citation_context={
                            "title": p.title,
                            "year": p.year,
                            "doi": p.doi,
                            "authors": getattr(p, 'authors', []),
                            "journal": getattr(p, 'journal', None) or getattr(p, 'venue', None)
                        },
                        focus_area=focus_area
                    )
                    for p in papers
                    if p.abstract
                ]
                all_papers.extend(paper_inputs)
                self.run_stats["topics_processed"] += 1
            else:
                self.run_stats["errors"].append({
                    "topic": query,
                    "error": "No papers found"
                })

        if not all_papers:
            logger.error("No papers found for any topic")
            return BatchResult(
                batch_id="",
                status=BatchStatus.FAILED,
                error_details=[{"error": "No papers found for any topic"}]
            )

        # Deduplicate papers by DOI to avoid batch API rejection
        seen_dois = set()
        unique_papers = []
        for paper in all_papers:
            doi = paper.citation_context.get("doi", "")
            if doi:
                if doi not in seen_dois:
                    seen_dois.add(doi)
                    unique_papers.append(paper)
            else:
                # Papers without DOI - use title hash as fallback
                title_key = paper.title.lower().strip()[:100]
                if title_key not in seen_dois:
                    seen_dois.add(title_key)
                    unique_papers.append(paper)

        logger.info(f"Deduplicated: {len(all_papers)} -> {len(unique_papers)} unique papers")
        all_papers = unique_papers

        self.run_stats["papers_submitted"] = len(all_papers)

        # Estimate and log cost
        cost_est = self.batch_client.estimate_cost(all_papers)
        logger.info(f"Total papers: {len(all_papers)}")
        logger.info(f"Estimated cost: ${cost_est['batch_cost_usd']} (saves ${cost_est['savings_usd']} vs real-time)")

        # Run discovery (standard or consolidated mode)
        if self.use_consolidated_mode and self.consolidated_client:
            logger.info("Running CONSOLIDATED two-pass extraction...")
            result = self.consolidated_client.discover_mechanisms(
                papers=all_papers,
                output_dir=self.output_dir,
                save_intermediates=True
            )
        else:
            # Standard per-paper extraction
            result = self.batch_client.discover_mechanisms_batch(
                papers=all_papers,
                output_dir=self.output_dir,
                wait_for_completion=wait_for_completion,
                save_report=True,
                report_path=self.report_dir / f"batch_report_{self.run_id}.json"
            )

        # Update stats
        self.run_stats["mechanisms_extracted"] = len(result.mechanisms)
        self.run_stats["total_cost_usd"] = result.cost_estimate_usd or cost_est["batch_cost_usd"]
        self.run_stats["end_time"] = datetime.now().isoformat()
        self.run_stats["batch_id"] = result.batch_id
        self.run_stats["status"] = result.status.value

        # Save run summary
        self._save_run_summary()

        return result

    def check_batch(self, batch_id: str) -> Dict:
        """
        Check status of an existing batch.

        Args:
            batch_id: ID of batch to check

        Returns:
            Status dict
        """
        return self.batch_client.get_batch_status(batch_id)

    def list_recent_batches(self, limit: int = 10) -> List[Dict]:
        """
        List recent batches.

        Args:
            limit: Maximum number to return

        Returns:
            List of batch info dicts
        """
        return self.batch_client.list_batches(limit=limit)

    def _save_run_summary(self):
        """Save run summary to file."""
        summary_path = self.report_dir / f"run_summary_{self.run_id}.json"

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(self.run_stats, f, indent=2)

        logger.info(f"Run summary saved: {summary_path}")

        # Print summary
        print("\n" + "="*60)
        print("DISCOVERY RUN SUMMARY")
        print("="*60)
        print(f"Run ID: {self.run_id}")
        print(f"Status: {self.run_stats.get('status', 'unknown')}")
        print(f"Topics processed: {self.run_stats['topics_processed']}")
        print(f"Papers submitted: {self.run_stats['papers_submitted']}")
        print(f"Mechanisms extracted: {self.run_stats['mechanisms_extracted']}")
        print(f"Estimated cost: ${self.run_stats['total_cost_usd']:.2f}")
        if self.run_stats["errors"]:
            print(f"Errors: {len(self.run_stats['errors'])}")
        print("="*60 + "\n")


def load_topics_config(config_path: Path) -> List[Dict]:
    """
    Load topics configuration from JSON file.

    Expected format:
    {
        "topics": [
            {
                "query": "housing quality respiratory health",
                "category": "built_environment",
                "focus_area": "housing to health",
                "max_papers": 30
            },
            ...
        ],
        "year_range": [2015, 2024],
        "min_citations": 5
    }
    """
    with open(config_path, 'r') as f:
        config = json.load(f)

    return config.get("topics", [])


def main():
    parser = argparse.ArgumentParser(
        description="Scheduled batch mechanism discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover mechanisms for a single topic
  python scheduled_batch_discovery.py --topic "housing quality respiratory health"

  # Run discovery for topics in config file
  python scheduled_batch_discovery.py --config discovery_topics.json

  # Check status of existing batch
  python scheduled_batch_discovery.py --check-batch msgbatch_abc123

  # List recent batches
  python scheduled_batch_discovery.py --list-batches

  # Run with default topics (comprehensive health determinants)
  python scheduled_batch_discovery.py --default-topics
        """
    )

    parser.add_argument(
        "--topic",
        type=str,
        help="Single topic query to discover mechanisms for"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to JSON config file with topics"
    )

    parser.add_argument(
        "--default-topics",
        action="store_true",
        help="Use default comprehensive topic list"
    )

    parser.add_argument(
        "--check-batch",
        type=str,
        metavar="BATCH_ID",
        help="Check status of existing batch"
    )

    parser.add_argument(
        "--process-batch",
        type=str,
        metavar="BATCH_ID",
        help="Process results from completed batch"
    )

    parser.add_argument(
        "--list-batches",
        action="store_true",
        help="List recent batches"
    )

    parser.add_argument(
        "--max-papers",
        type=int,
        default=30,
        help="Maximum papers per topic (default: 30)"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for mechanism YAML files"
    )

    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Submit batch and exit without waiting for completion"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually running"
    )

    parser.add_argument(
        "--consolidated",
        action="store_true",
        help="""Use consolidated two-pass extraction mode.

        Pass 1: Extract pathway candidates from all papers
        Pass 2: Group papers by pathway, then extract ONE mechanism per pathway
                with evidence aggregated from ALL supporting papers

        BENEFITS:
        - Produces higher quality A/B mechanisms (n_studies = paper count)
        - Avoids single-paper C-rated mechanisms
        - Proper evidence synthesis at extraction time

        TRADE-OFF:
        - Takes longer (two batch runs)
        - Higher cost (but better quality)
        """
    )

    args = parser.parse_args()

    # Initialize scheduler
    scheduler = ScheduledBatchDiscovery(
        output_dir=args.output_dir,
        use_consolidated_mode=args.consolidated
    )

    # Handle different modes
    if args.list_batches:
        print("\nRecent Batches:")
        print("-" * 80)
        batches = scheduler.list_recent_batches()
        for batch in batches:
            print(f"  {batch['id']}: {batch['status']} "
                  f"(succeeded={batch['succeeded']}, errored={batch['errored']})")
        return

    if args.check_batch:
        status = scheduler.check_batch(args.check_batch)
        print(f"\nBatch Status: {args.check_batch}")
        print("-" * 40)
        for key, value in status.items():
            print(f"  {key}: {value}")
        return

    if args.process_batch:
        print(f"\nProcessing results for batch: {args.process_batch}")
        mechanisms = scheduler.batch_client.process_results(args.process_batch)
        print(f"Extracted {len(mechanisms)} mechanisms")

        # Save mechanisms
        for mech in mechanisms:
            scheduler.batch_client.v2_discovery.save_mechanism(
                mech, scheduler.output_dir
            )
        print(f"Saved to: {scheduler.output_dir}")
        return

    # Determine topics
    topics = []

    if args.topic:
        topics = [{
            "query": args.topic,
            "category": "general",
            "focus_area": args.topic,
            "max_papers": args.max_papers
        }]
    elif args.config:
        topics = load_topics_config(args.config)
    elif args.default_topics:
        topics = DEFAULT_TOPICS
    else:
        parser.print_help()
        print("\nError: Must specify --topic, --config, --default-topics, or another action")
        sys.exit(1)

    # Dry run - just show what would happen
    if args.dry_run:
        print("\n[DRY RUN] Would process the following topics:")
        print("-" * 60)
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic['query']}")
            print(f"     Category: {topic.get('category', 'general')}")
            print(f"     Max papers: {topic.get('max_papers', 30)}")

        # Estimate total papers and cost
        est_papers = sum(t.get('max_papers', 30) for t in topics)
        est_cost = est_papers * 0.01  # Rough estimate
        print(f"\nEstimated total papers: ~{est_papers}")
        print(f"Estimated batch cost: ~${est_cost:.2f}")
        return

    # Run discovery
    print(f"\nStarting batch discovery for {len(topics)} topics...")

    result = scheduler.run_discovery(
        topics=topics,
        wait_for_completion=not args.no_wait
    )

    if args.no_wait:
        print(f"\nBatch submitted: {result.batch_id}")
        print("Check status with:")
        print(f"  python scheduled_batch_discovery.py --check-batch {result.batch_id}")
    else:
        print(f"\nDiscovery complete!")
        print(f"Mechanisms extracted: {len(result.mechanisms)}")
        print(f"Saved to: {scheduler.output_dir}")


if __name__ == "__main__":
    main()
