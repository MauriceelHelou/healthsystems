"""
End-to-End Mechanism Discovery Pipeline

Combines literature search + LLM extraction into a complete workflow:
1. Search for papers on a topic
2. Extract mechanisms from each paper
3. Validate and deduplicate
4. Save to mechanism bank

This is the main entry point for automated mechanism generation.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

from literature_search import LiteratureSearchAggregator, Paper
from llm_mechanism_discovery import LLMMechanismDiscovery, MechanismExtraction


class EndToEndDiscoveryPipeline:
    """
    Complete pipeline for discovering and cataloging mechanisms.

    Workflow:
    1. Search literature for papers on a topic
    2. Extract mechanisms from each paper using LLM
    3. Validate mechanisms for quality and structural competency
    4. Deduplicate similar mechanisms
    5. Save to mechanism bank with proper metadata
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        semantic_scholar_api_key: Optional[str] = None,
        pubmed_email: Optional[str] = None,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize the end-to-end pipeline.

        Args:
            anthropic_api_key: Claude API key
            semantic_scholar_api_key: Optional S2 API key
            pubmed_email: Email for PubMed (recommended)
            output_dir: Directory for mechanism bank (default: ../../mechanism-bank/mechanisms)
        """
        self.llm_discovery = LLMMechanismDiscovery(api_key=anthropic_api_key)
        self.literature_search = LiteratureSearchAggregator(
            semantic_scholar_api_key=semantic_scholar_api_key,
            pubmed_email=pubmed_email
        )

        if output_dir is None:
            # Default to mechanism bank
            self.output_dir = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"
        else:
            self.output_dir = output_dir

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Tracking
        self.discovered_mechanisms: List[MechanismExtraction] = []
        self.processed_papers: List[Paper] = []
        self.errors: List[Dict] = []

    def discover_mechanisms_for_topic(
        self,
        topic_query: str,
        max_papers: int = 10,
        year_range: Optional[tuple] = None,
        min_citations: int = 5,
        focus_area: Optional[str] = None
    ) -> List[MechanismExtraction]:
        """
        Discover mechanisms for a specific research topic.

        Args:
            topic_query: Search query (e.g., "eviction health outcomes")
            max_papers: Maximum papers to process
            year_range: (min_year, max_year) or None for all years
            min_citations: Minimum citation count filter
            focus_area: Optional focus area hint for LLM

        Returns:
            List of discovered mechanisms
        """
        print(f"\n{'='*80}")
        print(f"MECHANISM DISCOVERY PIPELINE: {topic_query}")
        print(f"{'='*80}\n")

        # Step 1: Search for papers
        print(f"[1/4] Searching for papers...")
        papers = self.literature_search.search(
            query=topic_query,
            limit_per_source=max_papers,
            year_range=year_range,
            min_citations=min_citations
        )

        if not papers:
            print("  [X] No papers found")
            return []

        print(f"  [OK] Found {len(papers)} papers\n")

        # Step 2: Extract mechanisms from each paper
        print(f"[2/4] Extracting mechanisms from papers...")
        mechanisms = []

        for i, paper in enumerate(papers, 1):
            print(f"\n  Processing paper {i}/{len(papers)}: {paper.title[:60]}...")

            # Skip papers without abstracts
            if not paper.abstract:
                print(f"    [!] Skipping (no abstract)")
                continue

            try:
                # Extract mechanisms using LLM
                extracted = self.llm_discovery.extract_mechanisms_from_paper(
                    paper_abstract=paper.abstract,
                    paper_title=paper.title,
                    focus_area=focus_area or topic_query
                )

                if extracted:
                    mechanisms.extend(extracted)
                    print(f"    [OK] Extracted {len(extracted)} mechanism(s)")

                    # Track paper
                    self.processed_papers.append(paper)

                else:
                    print(f"    [!] No mechanisms extracted")

            except Exception as e:
                error_info = {
                    "paper": paper.title,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.errors.append(error_info)
                print(f"    [X] Error: {e}")

        print(f"\n  [OK] Total mechanisms extracted: {len(mechanisms)}\n")

        # Step 3: Validate and filter
        print(f"[3/4] Validating mechanisms...")
        valid_mechanisms = self._validate_mechanisms(mechanisms)
        print(f"  [OK] {len(valid_mechanisms)}/{len(mechanisms)} mechanisms passed validation\n")

        # Step 4: Deduplicate
        print(f"[4/4] Deduplicating mechanisms...")
        unique_mechanisms = self._deduplicate_mechanisms(valid_mechanisms)
        print(f"  [OK] {len(unique_mechanisms)} unique mechanisms after deduplication\n")

        self.discovered_mechanisms = unique_mechanisms
        return unique_mechanisms

    def _validate_mechanisms(self, mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
        """
        Validate mechanisms for quality and structural competency.

        Filters out:
        - Low confidence extractions
        - Individual-level blame mechanisms
        - Duplicate IDs
        """
        valid = []
        seen_ids = set()

        for mech in mechanisms:
            # Generate ID
            mech_id = f"{mech.from_node_id}_to_{mech.to_node_id}"

            # Skip duplicates
            if mech_id in seen_ids:
                continue

            # Skip low confidence
            if mech.confidence == "low":
                print(f"    [!] Skipping low-confidence: {mech_id}")
                continue

            # Basic structural competency check
            # TODO: Enhance with more sophisticated validation
            if "individual" in mech.category.lower() or "behavioral" in mech.category.lower():
                # Allow only if explicitly structural
                if not mech.structural_competency_notes:
                    print(f"    [!] Skipping non-structural: {mech_id}")
                    continue

            seen_ids.add(mech_id)
            valid.append(mech)

        return valid

    def _deduplicate_mechanisms(self, mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
        """
        Deduplicate mechanisms with similar nodes.

        For now, uses exact node ID matching.
        Phase 2: Add semantic similarity deduplication.
        """
        unique_map: Dict[str, MechanismExtraction] = {}

        for mech in mechanisms:
            mech_id = f"{mech.from_node_id}_to_{mech.to_node_id}"

            if mech_id in unique_map:
                # Keep the higher confidence one
                existing = unique_map[mech_id]
                confidence_order = {"high": 3, "medium": 2, "low": 1}

                if confidence_order.get(mech.confidence, 0) > confidence_order.get(existing.confidence, 0):
                    unique_map[mech_id] = mech
            else:
                unique_map[mech_id] = mech

        return list(unique_map.values())

    def save_mechanisms(self) -> List[Path]:
        """
        Save all discovered mechanisms to the mechanism bank.

        Returns:
            List of file paths where mechanisms were saved
        """
        if not self.discovered_mechanisms:
            print("No mechanisms to save")
            return []

        print(f"\nSaving {len(self.discovered_mechanisms)} mechanisms to bank...")

        saved_paths = []

        for mech in self.discovered_mechanisms:
            try:
                file_path = self.llm_discovery.save_mechanism(
                    mechanism=mech,
                    output_dir=self.output_dir
                )
                saved_paths.append(file_path)

            except Exception as e:
                print(f"  [X] Error saving {mech.from_node_id}_to_{mech.to_node_id}: {e}")

        print(f"[OK] Saved {len(saved_paths)} mechanisms\n")
        return saved_paths

    def generate_discovery_report(self, output_file: Optional[Path] = None) -> Dict:
        """
        Generate a summary report of the discovery run.

        Args:
            output_file: Optional file to save JSON report

        Returns:
            Report dictionary
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "papers_processed": len(self.processed_papers),
                "mechanisms_discovered": len(self.discovered_mechanisms),
                "errors": len(self.errors)
            },
            "mechanisms": [
                {
                    "id": f"{m.from_node_id}_to_{m.to_node_id}",
                    "from": m.from_node_name,
                    "to": m.to_node_name,
                    "direction": m.direction,
                    "category": m.category,
                    "confidence": m.confidence,
                    "evidence_quality": m.evidence_quality
                }
                for m in self.discovered_mechanisms
            ],
            "papers": [
                {
                    "title": p.title,
                    "year": p.year,
                    "doi": p.doi,
                    "citations": p.citation_count
                }
                for p in self.processed_papers
            ],
            "errors": self.errors
        }

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Report saved to: {output_file}")

        return report

    def print_summary(self):
        """Print a human-readable summary of results"""
        print(f"\n{'='*80}")
        print("DISCOVERY SUMMARY")
        print(f"{'='*80}\n")

        print(f"Papers processed: {len(self.processed_papers)}")
        print(f"Mechanisms discovered: {len(self.discovered_mechanisms)}")
        print(f"Errors encountered: {len(self.errors)}\n")

        if self.discovered_mechanisms:
            print("Mechanisms by category:")
            categories = {}
            for mech in self.discovered_mechanisms:
                categories[mech.category] = categories.get(mech.category, 0) + 1

            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"  {cat}: {count}")

            print("\nMechanisms by confidence:")
            confidences = {}
            for mech in self.discovered_mechanisms:
                confidences[mech.confidence] = confidences.get(mech.confidence, 0) + 1

            for conf, count in sorted(confidences.items()):
                print(f"  {conf}: {count}")


def demo_housing_to_health():
    """
    Demo: Discover mechanisms for housing -> health pathway.

    This demo searches for papers on housing quality and health,
    extracts mechanisms, and saves them to the mechanism bank.
    """
    print("\n" + "="*80)
    print("DEMO: Housing Quality -> Health Mechanism Discovery")
    print("="*80 + "\n")

    # Initialize pipeline
    pipeline = EndToEndDiscoveryPipeline(
        pubmed_email="demo@healthsystems.org"  # Replace with your email
    )

    # Discover mechanisms
    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query="housing quality respiratory health asthma children",
        max_papers=5,  # Start small for demo
        year_range=(2015, 2024),  # Recent papers
        min_citations=10,
        focus_area="housing to health"
    )

    # Save mechanisms
    if mechanisms:
        saved_paths = pipeline.save_mechanisms()

        # Generate report
        report_path = Path("discovery_report_housing_health.json")
        pipeline.generate_discovery_report(output_file=report_path)

        # Print summary
        pipeline.print_summary()

        print(f"\n[OK] Demo complete!")
        print(f"  Mechanisms saved to: {pipeline.output_dir}")
        print(f"  Report saved to: {report_path}")

    else:
        print("\n[X] No mechanisms discovered")


def demo_eviction_to_health():
    """
    Demo: Discover mechanisms for eviction -> health pathway.
    """
    print("\n" + "="*80)
    print("DEMO: Eviction -> Health Mechanism Discovery")
    print("="*80 + "\n")

    pipeline = EndToEndDiscoveryPipeline(
        pubmed_email="demo@healthsystems.org"
    )

    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query="eviction housing displacement health outcomes emergency department",
        max_papers=5,
        year_range=(2015, 2024),
        min_citations=5,
        focus_area="housing policy to health"
    )

    if mechanisms:
        pipeline.save_mechanisms()
        pipeline.print_summary()

        # Show sample mechanism
        print("\n" + "="*80)
        print("SAMPLE MECHANISM")
        print("="*80 + "\n")

        sample = mechanisms[0]
        print(f"FROM: {sample.from_node_name}")
        print(f"TO: {sample.to_node_name}")
        print(f"Direction: {sample.direction}")
        print(f"Category: {sample.category}")
        print(f"\nPathway:")
        for i, step in enumerate(sample.mechanism_pathway, 1):
            print(f"  {i}. {step}")

        print(f"\nEvidence: {sample.evidence_quality} ({sample.n_studies} studies)")
        print(f"Confidence: {sample.confidence}")

        if sample.moderators:
            print(f"\nModerators:")
            for mod in sample.moderators:
                print(f"  - {mod['name']}: {mod['direction']} ({mod['strength']})")


if __name__ == "__main__":
    # Run housing demo
    demo_housing_to_health()

    # Uncomment to run eviction demo
    # demo_eviction_to_health()
