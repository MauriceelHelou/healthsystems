"""
End-to-End Mechanism Discovery Pipeline V3 (Full-Text Enhanced)

IMPROVEMENTS OVER V2:
1. Uses LLMMechanismDiscoveryV2 with citation verification
2. Passes verified citation metadata from literature search to LLM
3. Prevents false/fabricated citations
4. Flags mechanisms needing manual review
5. **NEW V3**: Multi-source full-text fetching via waterfall approach:
   - Unpaywall (free OA links)
   - PubMed Central (NIH OA)
   - Europe PMC (European OA)
   - CORE (global OA aggregator)
   - OpenAlex (OA metadata)
   - Elsevier ScienceDirect (institutional access)
   - Wiley TDM (institutional access)
   - Semantic Scholar (fallback)
   - Harvard Library Proxy (manual access)

Workflow:
1. Search literature for papers (abstracts + metadata)
2. Attempt full-text retrieval via multi-source fetcher
3. Extract mechanisms with VERIFIED citations + full-text when available
4. Validate mechanisms (including citation validation)
5. Deduplicate
6. Save to mechanism bank with review flags

Configuration:
    Set API keys in backend/.env (see .env.example for all options)
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import V2 components
from llm_mechanism_discovery import LLMMechanismDiscoveryV2, MechanismExtraction

# Import full-text fetcher (V3)
try:
    from utils.fulltext_fetcher import FullTextFetcher, FullTextResult, FullTextSource
    FULLTEXT_AVAILABLE = True
except ImportError:
    logging.warning("fulltext_fetcher module not found - full-text retrieval disabled")
    FullTextFetcher = None
    FullTextResult = None
    FullTextSource = None
    FULLTEXT_AVAILABLE = False

# Keep V1 literature search (unchanged)
try:
    from literature_search import LiteratureSearchAggregator, Paper
except ImportError:
    logging.warning("literature_search module not found - using mock")
    Paper = None
    LiteratureSearchAggregator = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EndToEndDiscoveryPipelineV3:
    """
    Complete pipeline for discovering and cataloging mechanisms with citation verification
    and multi-source full-text retrieval (V3).

    KEY FEATURES:
    - Passes verified citation metadata from literature search to LLM
    - Validates DOIs via Crossref API
    - Flags mechanisms needing manual review
    - Prevents false citations by NOT asking LLM to extract citations
    - **V3**: Multi-source full-text fetching (Unpaywall, PMC, Europe PMC, CORE,
              OpenAlex, Elsevier, Wiley, Semantic Scholar, Harvard Proxy)
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        semantic_scholar_api_key: Optional[str] = None,
        pubmed_email: Optional[str] = None,
        output_dir: Optional[Path] = None,
        validate_citations: bool = True,
        strict_validation: bool = False,
        # V3: Full-text fetcher options
        enable_fulltext: bool = True,
        elsevier_api_key: Optional[str] = None,
        wiley_tdm_token: Optional[str] = None,
        core_api_key: Optional[str] = None,
        enable_harvard_proxy: bool = True
    ):
        """
        Initialize V3 pipeline with citation verification and full-text fetching.

        Args:
            anthropic_api_key: Claude API key
            semantic_scholar_api_key: Optional S2 API key
            pubmed_email: Email for PubMed/Unpaywall APIs
            output_dir: Output directory for mechanisms
            validate_citations: Whether to validate DOIs (default: True)
            strict_validation: If True, reject invalid citations entirely (default: False)
            enable_fulltext: Enable multi-source full-text fetching (default: True)
            elsevier_api_key: Elsevier ScienceDirect API key
            wiley_tdm_token: Wiley TDM API token
            core_api_key: CORE API key (optional, for higher rate limits)
            enable_harvard_proxy: Enable Harvard Library proxy URLs (default: True)
        """
        # Use V2 discovery with citation validation
        self.llm_discovery = LLMMechanismDiscoveryV2(
            api_key=anthropic_api_key,
            validate_citations=validate_citations,
            strict_validation=strict_validation
        )

        # Literature search (unchanged from V1)
        if LiteratureSearchAggregator:
            self.literature_search = LiteratureSearchAggregator(
                semantic_scholar_api_key=semantic_scholar_api_key,
                pubmed_email=pubmed_email
            )
        else:
            self.literature_search = None
            logger.warning("Literature search not available")

        # V3: Initialize full-text fetcher
        self.fulltext_fetcher = None
        self.enable_fulltext = enable_fulltext and FULLTEXT_AVAILABLE

        if self.enable_fulltext:
            # Load from env if not provided
            email = pubmed_email or os.getenv("PUBMED_EMAIL") or os.getenv("UNPAYWALL_EMAIL")

            self.fulltext_fetcher = FullTextFetcher(
                unpaywall_email=email,
                pubmed_email=email,
                pubmed_api_key=os.getenv("PUBMED_API_KEY"),
                elsevier_api_key=elsevier_api_key or os.getenv("ELSEVIER_API_KEY"),
                elsevier_inst_token=os.getenv("ELSEVIER_INST_TOKEN"),
                wiley_tdm_token=wiley_tdm_token or os.getenv("WILEY_TDM_TOKEN"),
                core_api_key=core_api_key or os.getenv("CORE_API_KEY"),
                semantic_scholar_api_key=semantic_scholar_api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY"),
                enable_harvard_proxy=enable_harvard_proxy
            )
            logger.info(f"Full-text fetcher enabled with providers: {self.fulltext_fetcher.get_available_providers()}")
        else:
            logger.warning("Full-text fetching disabled or unavailable")

        # Output directory
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"
        else:
            self.output_dir = output_dir

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Tracking
        self.discovered_mechanisms: List[MechanismExtraction] = []
        self.processed_papers: List = []
        self.errors: List[Dict] = []
        self.review_queue: List[MechanismExtraction] = []

        # V3: Full-text tracking
        self.fulltext_results: Dict[str, FullTextResult] = {}  # DOI -> result
        self.fulltext_stats = {
            "attempted": 0,
            "successful": 0,
            "by_source": {}
        }

        logger.info(f"Initialized End-to-End Pipeline V3 (citation_validation=ON, fulltext={'ON' if self.enable_fulltext else 'OFF'})")

    def discover_mechanisms_for_topic(
        self,
        topic_query: str,
        max_papers: int = 10,
        year_range: Optional[tuple] = None,
        min_citations: int = 5,
        focus_area: Optional[str] = None,
        fetch_fulltext: bool = True
    ) -> List[MechanismExtraction]:
        """
        Discover mechanisms for a topic with citation verification and full-text retrieval (V3).

        Args:
            topic_query: Search query
            max_papers: Maximum papers to process
            year_range: (min_year, max_year) or None
            min_citations: Minimum citation count
            focus_area: Optional focus area
            fetch_fulltext: Attempt to fetch full-text PDFs (default: True)

        Returns:
            List of discovered and validated mechanisms
        """
        print(f"\n{'='*80}")
        print(f"MECHANISM DISCOVERY PIPELINE V3: {topic_query}")
        print(f"{'='*80}\n")

        # Step 1: Search for papers
        print(f"[1/6] Searching for papers...")

        if not self.literature_search:
            print("  [X] Literature search not available")
            return []

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

        # Step 2 (V3): Fetch full-text for papers with DOIs
        if fetch_fulltext and self.enable_fulltext and self.fulltext_fetcher:
            print(f"[2/6] Fetching full-text via multi-source API...")
            self._fetch_fulltext_for_papers(papers)
        else:
            print(f"[2/6] Skipping full-text fetch (disabled or unavailable)")

        # Step 3: Extract mechanisms with VERIFIED citations
        print(f"\n[3/6] Extracting mechanisms with citation verification...")
        mechanisms = []

        for i, paper in enumerate(papers, 1):
            print(f"\n  Processing paper {i}/{len(papers)}: {paper.title[:60]}...")

            if not paper.abstract:
                print(f"    [!] Skipping (no abstract)")
                continue

            try:
                # V2: Build verified citation context from literature search metadata
                citation_context = self._build_citation_context(paper)

                # V3: Add full-text info if available
                fulltext_info = self._get_fulltext_info(paper.doi) if paper.doi else None
                if fulltext_info:
                    citation_context["fulltext_available"] = True
                    citation_context["fulltext_source"] = fulltext_info.get("source")
                    citation_context["fulltext_url"] = fulltext_info.get("pdf_url")

                # Pass citation context to LLM
                extracted = self.llm_discovery.extract_mechanisms_from_paper(
                    paper_abstract=paper.abstract,
                    paper_title=paper.title,
                    citation_context=citation_context,
                    focus_area=focus_area or topic_query
                )

                if extracted:
                    mechanisms.extend(extracted)

                    # Count review flags
                    needs_review = sum(1 for m in extracted if m.needs_manual_review)
                    if needs_review:
                        print(f"    [OK] Extracted {len(extracted)} mechanism(s) ({needs_review} need review)")
                        self.review_queue.extend([m for m in extracted if m.needs_manual_review])
                    else:
                        ft_status = " [full-text]" if fulltext_info else ""
                        print(f"    [OK] Extracted {len(extracted)} verified mechanism(s){ft_status}")

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

        # Step 4: Validate structural competency
        print(f"[4/6] Validating structural competency...")
        valid_mechanisms = self._validate_mechanisms(mechanisms)
        print(f"  [OK] {len(valid_mechanisms)}/{len(mechanisms)} mechanisms passed validation\n")

        # Step 5: Deduplicate
        print(f"[5/6] Deduplicating mechanisms...")
        unique_mechanisms = self._deduplicate_mechanisms(valid_mechanisms)
        print(f"  [OK] {len(unique_mechanisms)} unique mechanisms\n")

        # Step 6: Report summary
        print(f"[6/6] Discovery summary...")

        # Citation verification stats
        verified = sum(1 for m in unique_mechanisms if m.citation_verified)
        needs_review = sum(1 for m in unique_mechanisms if m.needs_manual_review)
        print(f"  Citations: {verified}/{len(unique_mechanisms)} verified")
        if needs_review:
            print(f"  Review needed: {needs_review} mechanisms flagged")

        # Full-text stats
        if self.fulltext_stats["attempted"] > 0:
            ft_rate = self.fulltext_stats["successful"] / self.fulltext_stats["attempted"] * 100
            print(f"  Full-text: {self.fulltext_stats['successful']}/{self.fulltext_stats['attempted']} ({ft_rate:.0f}%) retrieved")
            if self.fulltext_stats["by_source"]:
                sources = ", ".join(f"{k}:{v}" for k, v in self.fulltext_stats["by_source"].items())
                print(f"  Sources: {sources}")

        self.discovered_mechanisms = unique_mechanisms
        return unique_mechanisms

    def _fetch_fulltext_for_papers(self, papers: List) -> None:
        """
        Fetch full-text for all papers with DOIs (V3 feature).

        Args:
            papers: List of Paper objects
        """
        papers_with_doi = [p for p in papers if p.doi]
        print(f"  Attempting full-text fetch for {len(papers_with_doi)}/{len(papers)} papers with DOIs...")

        for paper in papers_with_doi:
            try:
                self.fulltext_stats["attempted"] += 1

                result = self.fulltext_fetcher.fetch_fulltext(paper.doi)
                self.fulltext_results[paper.doi] = result

                if result.success:
                    self.fulltext_stats["successful"] += 1
                    source_name = result.source.value if result.source else "unknown"
                    self.fulltext_stats["by_source"][source_name] = \
                        self.fulltext_stats["by_source"].get(source_name, 0) + 1

                    oa_status = " (OA)" if result.is_open_access else ""
                    print(f"    [OK] {paper.doi[:40]}... via {source_name}{oa_status}")
                else:
                    logger.debug(f"No full-text for {paper.doi}: {result.error}")

            except Exception as e:
                logger.error(f"Error fetching full-text for {paper.doi}: {e}")

        success_rate = (
            self.fulltext_stats["successful"] / self.fulltext_stats["attempted"] * 100
            if self.fulltext_stats["attempted"] > 0 else 0
        )
        print(f"  [OK] Full-text retrieval: {self.fulltext_stats['successful']}/{self.fulltext_stats['attempted']} ({success_rate:.0f}%)")

    def _get_fulltext_info(self, doi: str) -> Optional[Dict]:
        """
        Get full-text info for a DOI if available.

        Args:
            doi: The DOI to look up

        Returns:
            Dict with source and pdf_url if available, None otherwise
        """
        if not doi or doi not in self.fulltext_results:
            return None

        result = self.fulltext_results[doi]
        if not result.success:
            return None

        return {
            "source": result.source.value if result.source else None,
            "pdf_url": result.pdf_url,
            "is_open_access": result.is_open_access,
            "license": result.license
        }

    def _build_citation_context(self, paper) -> Dict:
        """
        Build verified citation context from literature search metadata (V2).

        This is THE KEY FIX: We use the verified metadata from the literature
        search APIs instead of asking the LLM to extract citations from abstracts.

        Args:
            paper: Paper object from literature search

        Returns:
            Dict with authors, year, doi, journal, title
        """
        context = {
            "title": paper.title,
            "year": paper.year,
            "doi": paper.doi,
            "authors": [],
            "journal": getattr(paper, 'journal', None) or getattr(paper, 'venue', None)
        }

        # Extract author names
        if hasattr(paper, 'authors') and paper.authors:
            if isinstance(paper.authors, list):
                context["authors"] = [
                    f"{author.get('family', author.get('last', ''))}, {author.get('given', author.get('first', ''))[0]}."
                    if isinstance(author, dict)
                    else str(author)
                    for author in paper.authors[:5]  # Limit to first 5
                ]
            elif isinstance(paper.authors, str):
                context["authors"] = [paper.authors]

        return context

    def _validate_mechanisms(self, mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
        """
        Validate mechanisms for structural competency (unchanged from V1).

        V2 citation validation happens in extract_mechanisms_from_paper.
        """
        valid = []
        seen_ids = set()

        for mech in mechanisms:
            mech_id = f"{mech.from_node_id}_to_{mech.to_node_id}"

            if mech_id in seen_ids:
                continue

            if mech.confidence == "low":
                print(f"    [!] Skipping low-confidence: {mech_id}")
                continue

            if "individual" in mech.category.lower() or "behavioral" in mech.category.lower():
                if not mech.structural_competency_notes:
                    print(f"    [!] Skipping non-structural: {mech_id}")
                    continue

            seen_ids.add(mech_id)
            valid.append(mech)

        return valid

    def _deduplicate_mechanisms(self, mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
        """Deduplicate mechanisms (unchanged from V1)"""
        unique_map: Dict[str, MechanismExtraction] = {}

        for mech in mechanisms:
            mech_id = f"{mech.from_node_id}_to_{mech.to_node_id}"

            if mech_id in unique_map:
                existing = unique_map[mech_id]
                confidence_order = {"high": 3, "medium": 2, "low": 1}

                if confidence_order.get(mech.confidence, 0) > confidence_order.get(existing.confidence, 0):
                    unique_map[mech_id] = mech
            else:
                unique_map[mech_id] = mech

        return list(unique_map.values())

    def save_mechanisms(self) -> List[Path]:
        """
        Save mechanisms with V2 citation validation metadata.

        Returns:
            List of saved file paths
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
                logger.error(f"Error saving {mech.from_node_id}_to_{mech.to_node_id}: {e}")

        print(f"\n[OK] Saved {len(saved_paths)} mechanisms")

        # V2: Report review queue
        if self.review_queue:
            print(f"\n[⚠️] {len(self.review_queue)} mechanisms flagged for manual review:")
            for mech in self.review_queue[:5]:  # Show first 5
                print(f"  - {mech.from_node_id}_to_{mech.to_node_id}")
                if mech.citation_issues:
                    for issue in mech.citation_issues:
                        print(f"    • {issue}")

            if len(self.review_queue) > 5:
                print(f"  ... and {len(self.review_queue) - 5} more")

        return saved_paths

    def generate_discovery_report(self, output_file: Optional[Path] = None) -> Dict:
        """
        Generate V3 discovery report with citation validation and full-text stats.

        Args:
            output_file: Optional JSON file path

        Returns:
            Report dict
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_version": "3.0-fulltext-enhanced",
            "summary": {
                "papers_processed": len(self.processed_papers),
                "mechanisms_discovered": len(self.discovered_mechanisms),
                "citations_verified": sum(1 for m in self.discovered_mechanisms if m.citation_verified),
                "needs_manual_review": sum(1 for m in self.discovered_mechanisms if m.needs_manual_review),
                "errors": len(self.errors)
            },
            # V3: Full-text retrieval stats
            "fulltext_stats": {
                "attempted": self.fulltext_stats["attempted"],
                "successful": self.fulltext_stats["successful"],
                "success_rate": f"{self.fulltext_stats['successful'] / self.fulltext_stats['attempted'] * 100:.1f}%" if self.fulltext_stats["attempted"] > 0 else "N/A",
                "by_source": self.fulltext_stats["by_source"]
            },
            "mechanisms": [
                {
                    "id": f"{m.from_node_id}_to_{m.to_node_id}",
                    "from": m.from_node_name,
                    "to": m.to_node_name,
                    "direction": m.direction,
                    "category": m.category,
                    "confidence": m.confidence,
                    "evidence_quality": m.evidence_quality,
                    "citation_verified": m.citation_verified,
                    "needs_review": m.needs_manual_review,
                    "citation_issues": m.citation_issues
                }
                for m in self.discovered_mechanisms
            ],
            "papers": [
                {
                    "title": p.title,
                    "year": p.year,
                    "doi": p.doi,
                    "citations": getattr(p, 'citation_count', None),
                    # V3: Include full-text info
                    "fulltext_available": p.doi in self.fulltext_results and self.fulltext_results[p.doi].success if p.doi else False,
                    "fulltext_source": self.fulltext_results[p.doi].source.value if p.doi and p.doi in self.fulltext_results and self.fulltext_results[p.doi].success else None
                }
                for p in self.processed_papers
            ],
            "errors": self.errors
        }

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved to: {output_file}")

        return report

    def print_summary(self):
        """Print V3 summary with citation validation and full-text stats"""
        print(f"\n{'='*80}")
        print("DISCOVERY SUMMARY (V3)")
        print(f"{'='*80}\n")

        print(f"Papers processed: {len(self.processed_papers)}")
        print(f"Mechanisms discovered: {len(self.discovered_mechanisms)}")

        verified = sum(1 for m in self.discovered_mechanisms if m.citation_verified)
        needs_review = sum(1 for m in self.discovered_mechanisms if m.needs_manual_review)

        print(f"Citations verified: {verified}/{len(self.discovered_mechanisms)}")
        print(f"Flagged for review: {needs_review}")
        print(f"Errors encountered: {len(self.errors)}\n")

        # V3: Full-text stats
        if self.fulltext_stats["attempted"] > 0:
            ft_rate = self.fulltext_stats["successful"] / self.fulltext_stats["attempted"] * 100
            print(f"Full-text retrieval:")
            print(f"  Attempted: {self.fulltext_stats['attempted']}")
            print(f"  Successful: {self.fulltext_stats['successful']} ({ft_rate:.1f}%)")
            if self.fulltext_stats["by_source"]:
                print(f"  By source:")
                for source, count in sorted(self.fulltext_stats["by_source"].items(), key=lambda x: x[1], reverse=True):
                    print(f"    {source}: {count}")
            print()

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


def demo_v3():
    """Demo V3 pipeline with citation verification and full-text retrieval"""
    print("\n" + "="*80)
    print("DEMO: Mechanism Discovery Pipeline V3 (Full-Text Enhanced)")
    print("="*80 + "\n")

    # Initialize with environment variables
    pipeline = EndToEndDiscoveryPipelineV3(
        pubmed_email=os.getenv("PUBMED_EMAIL", "maurice_elhelou@gsd.harvard.edu"),
        validate_citations=True,
        strict_validation=False,  # Allow flagged mechanisms to save
        enable_fulltext=True,     # V3: Enable multi-source full-text
        enable_harvard_proxy=True # V3: Include Harvard proxy as fallback
    )

    print(f"Full-text providers: {pipeline.fulltext_fetcher.get_available_providers() if pipeline.fulltext_fetcher else 'None'}\n")

    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query="housing quality respiratory health asthma",
        max_papers=3,
        year_range=(2018, 2024),
        min_citations=10,
        focus_area="housing to health",
        fetch_fulltext=True  # V3: Attempt full-text retrieval
    )

    if mechanisms:
        pipeline.save_mechanisms()
        report_path = Path("discovery_report_v3.json")
        pipeline.generate_discovery_report(output_file=report_path)
        pipeline.print_summary()

        print(f"\nDemo complete!")
        print(f"  Mechanisms: {len(mechanisms)}")
        print(f"  Report: {report_path}")
    else:
        print("\nNo mechanisms discovered")


# Keep V2 alias for backwards compatibility
EndToEndDiscoveryPipelineV2 = EndToEndDiscoveryPipelineV3
demo_v2 = demo_v3


if __name__ == "__main__":
    demo_v3()
