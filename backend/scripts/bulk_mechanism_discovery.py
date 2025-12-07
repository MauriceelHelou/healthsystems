"""
Bulk Mechanism Discovery Script

Searches multiple health topics to discover new mechanisms using the V3 pipeline
with full-text retrieval.

Usage:
    python backend/scripts/bulk_mechanism_discovery.py
    python backend/scripts/bulk_mechanism_discovery.py --max-per-topic 15
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Setup paths
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent

# Load environment
load_dotenv(BACKEND_DIR / '.env')

# Add paths
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(BACKEND_DIR / 'pipelines'))

from pipelines.end_to_end_discovery import EndToEndDiscoveryPipelineV3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Topics to search - focused on structural determinants of health
DISCOVERY_TOPICS = [
    # Housing & Built Environment
    {
        "query": "lead paint exposure childhood neurodevelopment",
        "focus": "housing hazards to child development",
        "category": "built_environment"
    },
    {
        "query": "housing instability chronic disease outcomes",
        "focus": "housing stability to health",
        "category": "economic"
    },
    {
        "query": "green space access mental health urban",
        "focus": "built environment to mental health",
        "category": "built_environment"
    },
    {
        "query": "walkability physical activity obesity neighborhood",
        "focus": "neighborhood design to health behaviors",
        "category": "built_environment"
    },

    # Food & Nutrition Security
    {
        "query": "food desert access chronic disease cardiovascular",
        "focus": "food environment to cardiovascular health",
        "category": "built_environment"
    },
    {
        "query": "SNAP benefits food security child health outcomes",
        "focus": "food assistance policy to child health",
        "category": "political"
    },
    {
        "query": "food insecurity maternal health pregnancy outcomes",
        "focus": "food security to maternal health",
        "category": "economic"
    },

    # Transportation & Access
    {
        "query": "public transportation healthcare access chronic disease management",
        "focus": "transportation to healthcare access",
        "category": "built_environment"
    },
    {
        "query": "medical transportation barriers medication adherence",
        "focus": "transportation barriers to treatment",
        "category": "healthcare_access"
    },

    # Economic Factors
    {
        "query": "minimum wage health outcomes population health",
        "focus": "wage policy to health",
        "category": "political"
    },
    {
        "query": "job insecurity stress cardiovascular disease",
        "focus": "employment precarity to health",
        "category": "economic"
    },
    {
        "query": "medical debt health outcomes financial toxicity",
        "focus": "healthcare costs to health",
        "category": "economic"
    },
    {
        "query": "paid sick leave infectious disease workplace health",
        "focus": "labor policy to health",
        "category": "political"
    },

    # Criminal Justice & Health
    {
        "query": "incarceration mental health post-release outcomes",
        "focus": "incarceration to mental health",
        "category": "political"
    },
    {
        "query": "mass incarceration community health family outcomes",
        "focus": "carceral policy to community health",
        "category": "social_environment"
    },

    # Education & Health
    {
        "query": "educational attainment health outcomes socioeconomic",
        "focus": "education to health",
        "category": "social_environment"
    },
    {
        "query": "school health programs childhood obesity prevention",
        "focus": "school policy to child health",
        "category": "political"
    },

    # Environmental Justice
    {
        "query": "industrial pollution proximity respiratory disease environmental justice",
        "focus": "pollution exposure to health disparities",
        "category": "built_environment"
    },
    {
        "query": "climate change heat exposure mortality vulnerable populations",
        "focus": "climate to health equity",
        "category": "built_environment"
    },
    {
        "query": "water quality contamination health outcomes community",
        "focus": "water infrastructure to health",
        "category": "built_environment"
    },

    # Healthcare System
    {
        "query": "community health worker chronic disease management outcomes",
        "focus": "workforce models to health",
        "category": "healthcare_access"
    },
    {
        "query": "implicit bias healthcare racial disparities outcomes",
        "focus": "provider bias to health disparities",
        "category": "healthcare_access"
    },
    {
        "query": "federally qualified health center access outcomes underserved",
        "focus": "safety net to health access",
        "category": "healthcare_access"
    },

    # Social Environment
    {
        "query": "social isolation mortality cardiovascular older adults",
        "focus": "social connection to health",
        "category": "social_environment"
    },
    {
        "query": "discrimination stress hypertension racial health disparities",
        "focus": "discrimination to cardiovascular health",
        "category": "social_environment"
    },
    {
        "query": "community violence exposure child mental health trauma",
        "focus": "violence exposure to child health",
        "category": "social_environment"
    },
]


class BulkMechanismDiscovery:
    """Runs discovery across multiple topics"""

    def __init__(
        self,
        max_papers_per_topic: int = 10,
        year_range: tuple = (2018, 2024),
        min_citations: int = 5
    ):
        self.max_papers_per_topic = max_papers_per_topic
        self.year_range = year_range
        self.min_citations = min_citations

        # Initialize pipeline
        self.pipeline = EndToEndDiscoveryPipelineV3(
            pubmed_email=os.getenv("PUBMED_EMAIL"),
            validate_citations=True,
            strict_validation=False,
            enable_fulltext=True,
            enable_harvard_proxy=True
        )

        # Tracking
        self.all_mechanisms = []
        self.topic_results = []
        self.total_papers = 0
        self.total_fulltext = 0

        logger.info(f"Initialized bulk discovery (max {max_papers_per_topic} papers/topic)")

    def run(self, topics: Optional[List[Dict]] = None) -> Dict:
        """Run discovery across all topics"""
        topics = topics or DISCOVERY_TOPICS

        print(f"\n{'='*80}")
        print(f"BULK MECHANISM DISCOVERY")
        print(f"{'='*80}")
        print(f"\nSearching {len(topics)} topics, max {self.max_papers_per_topic} papers each")
        print(f"Year range: {self.year_range[0]}-{self.year_range[1]}")
        print(f"Min citations: {self.min_citations}\n")

        for i, topic in enumerate(topics, 1):
            print(f"\n{'='*80}")
            print(f"TOPIC {i}/{len(topics)}: {topic['query'][:60]}")
            print(f"{'='*80}")

            try:
                # Reset pipeline state for each topic
                self.pipeline.discovered_mechanisms = []
                self.pipeline.processed_papers = []
                self.pipeline.errors = []
                self.pipeline.review_queue = []
                self.pipeline.fulltext_results = {}
                self.pipeline.fulltext_stats = {
                    "attempted": 0,
                    "successful": 0,
                    "by_source": {}
                }

                # Run discovery
                mechanisms = self.pipeline.discover_mechanisms_for_topic(
                    topic_query=topic["query"],
                    max_papers=self.max_papers_per_topic,
                    year_range=self.year_range,
                    min_citations=self.min_citations,
                    focus_area=topic.get("focus"),
                    fetch_fulltext=True
                )

                # Save mechanisms
                if mechanisms:
                    saved = self.pipeline.save_mechanisms()

                    self.all_mechanisms.extend(mechanisms)
                    self.total_papers += len(self.pipeline.processed_papers)
                    self.total_fulltext += self.pipeline.fulltext_stats.get("successful", 0)

                    self.topic_results.append({
                        "topic": topic["query"],
                        "focus": topic.get("focus"),
                        "category": topic.get("category"),
                        "papers_processed": len(self.pipeline.processed_papers),
                        "mechanisms_found": len(mechanisms),
                        "mechanisms_saved": len(saved),
                        "fulltext_retrieved": self.pipeline.fulltext_stats.get("successful", 0)
                    })

                    print(f"\n  Topic complete: {len(mechanisms)} mechanisms saved")
                else:
                    self.topic_results.append({
                        "topic": topic["query"],
                        "focus": topic.get("focus"),
                        "category": topic.get("category"),
                        "papers_processed": 0,
                        "mechanisms_found": 0,
                        "mechanisms_saved": 0,
                        "fulltext_retrieved": 0
                    })
                    print(f"\n  No mechanisms found for this topic")

            except Exception as e:
                logger.error(f"Error processing topic '{topic['query']}': {e}")
                self.topic_results.append({
                    "topic": topic["query"],
                    "error": str(e)
                })

        # Print final summary
        self._print_summary()

        return self._generate_report()

    def _print_summary(self):
        """Print discovery summary"""
        print(f"\n{'='*80}")
        print("BULK DISCOVERY COMPLETE")
        print(f"{'='*80}\n")

        print(f"Topics searched:      {len(self.topic_results)}")
        print(f"Total papers:         {self.total_papers}")
        print(f"Total full-text:      {self.total_fulltext}")
        print(f"Total mechanisms:     {len(self.all_mechanisms)}")

        # By category
        categories = {}
        for mech in self.all_mechanisms:
            cat = mech.category
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\nMechanisms by category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")

        # Top topics
        print(f"\nTop topics by mechanisms found:")
        sorted_topics = sorted(
            [t for t in self.topic_results if t.get("mechanisms_found", 0) > 0],
            key=lambda x: x.get("mechanisms_found", 0),
            reverse=True
        )[:10]

        for t in sorted_topics:
            print(f"  {t['mechanisms_found']:3d} - {t['topic'][:50]}")

    def _generate_report(self) -> Dict:
        """Generate discovery report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "topics_searched": len(self.topic_results),
                "total_papers": self.total_papers,
                "total_fulltext": self.total_fulltext,
                "total_mechanisms": len(self.all_mechanisms)
            },
            "by_category": {},
            "topic_results": self.topic_results,
            "mechanisms": [
                {
                    "id": f"{m.from_node_id}_to_{m.to_node_id}",
                    "from": m.from_node_name,
                    "to": m.to_node_name,
                    "category": m.category,
                    "direction": m.direction,
                    "confidence": m.confidence,
                    "evidence_quality": m.evidence_quality
                }
                for m in self.all_mechanisms
            ]
        }

        # Count by category
        for mech in self.all_mechanisms:
            cat = mech.category
            report["by_category"][cat] = report["by_category"].get(cat, 0) + 1

        # Save report
        report_path = BACKEND_DIR / f"bulk_discovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\nReport saved to: {report_path}")

        return report


def main():
    parser = argparse.ArgumentParser(description="Bulk mechanism discovery")
    parser.add_argument('--max-per-topic', type=int, default=10,
                        help="Max papers per topic (default: 10)")
    parser.add_argument('--min-citations', type=int, default=5,
                        help="Minimum citation count (default: 5)")
    parser.add_argument('--year-start', type=int, default=2018,
                        help="Start year (default: 2018)")
    parser.add_argument('--year-end', type=int, default=2024,
                        help="End year (default: 2024)")

    args = parser.parse_args()

    discovery = BulkMechanismDiscovery(
        max_papers_per_topic=args.max_per_topic,
        year_range=(args.year_start, args.year_end),
        min_citations=args.min_citations
    )

    discovery.run()


if __name__ == "__main__":
    main()
