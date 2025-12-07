"""
Batch Mechanism Discovery Pipeline using Claude's Message Batches API.

BENEFITS OVER REAL-TIME PROCESSING:
1. **50% cost reduction** on all LLM calls
2. **Bulk discovery runs** - process 100s-1000s of papers in parallel
3. **No per-minute rate limits** - submit all at once
4. **Idempotent results** - available for 29 days

WHEN TO USE:
- Bulk discovery (50+ papers)
- Nightly/weekly scheduled runs
- Cost-sensitive workloads
- Large-scale literature reviews

WHEN NOT TO USE:
- Interactive single-paper extraction (use real-time)
- Testing/debugging prompts (use real-time)
- Results needed immediately (<1 hour)

API Reference: https://platform.claude.com/docs/en/build-with-claude/batch-processing
"""

import anthropic
import time
import json
import os
import sys
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import logging

from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.llm_mechanism_discovery import LLMMechanismDiscoveryV2, MechanismExtraction

logger = logging.getLogger(__name__)


class BatchStatus(Enum):
    """Batch processing status."""
    SUBMITTED = "submitted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class BatchResult:
    """Result of a batch discovery operation."""
    batch_id: str
    status: BatchStatus
    mechanisms: List[MechanismExtraction] = field(default_factory=list)
    succeeded_count: int = 0
    failed_count: int = 0
    error_details: List[Dict] = field(default_factory=list)
    processing_time_seconds: Optional[float] = None
    cost_estimate_usd: Optional[float] = None


@dataclass
class PaperInput:
    """Input format for a paper to be processed."""
    abstract: str
    title: str
    citation_context: Dict  # {authors, year, doi, journal, title}
    focus_area: Optional[str] = None
    custom_id: Optional[str] = None  # If not provided, will be generated from DOI


class BatchMechanismDiscovery:
    """
    Batch-enabled mechanism discovery using Claude's Message Batches API.

    Benefits:
    - 50% cost reduction compared to real-time API
    - Process 100s-1000s of papers in parallel
    - No per-minute rate limits during processing
    - Results available for 29 days

    Usage:
        batch_discovery = BatchMechanismDiscovery()

        # Option 1: Submit and wait
        result = batch_discovery.discover_mechanisms_batch(
            papers=papers,
            output_dir=Path("mechanism-bank/mechanisms"),
            wait_for_completion=True
        )

        # Option 2: Submit and poll later
        batch_id = batch_discovery.submit_batch(papers)
        # ... later ...
        result = batch_discovery.get_batch_results(batch_id, papers)
    """

    # Batch API limits
    MAX_REQUESTS_PER_BATCH = 100_000
    MAX_BATCH_SIZE_BYTES = 256 * 1024 * 1024  # 256 MB
    MAX_WAIT_TIME_SECONDS = 86400  # 24 hours
    DEFAULT_POLL_INTERVAL = 60  # 1 minute

    # Cost estimates (as of 2025, 50% discount vs real-time)
    COST_PER_1M_INPUT_TOKENS = 2.50  # Claude Opus batch pricing
    COST_PER_1M_OUTPUT_TOKENS = 12.50

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-opus-4-5-20251101",
        validate_citations: bool = True,
        strict_validation: bool = False
    ):
        """
        Initialize batch discovery pipeline.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use (default: claude-opus-4-5-20251101)
            validate_citations: Whether to validate DOIs via Crossref (default: True)
            strict_validation: If True, reject mechanisms with invalid DOIs (default: False)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

        # Reuse V2 discovery for prompt generation and validation
        self.v2_discovery = LLMMechanismDiscoveryV2(
            api_key=self.api_key,
            validate_citations=validate_citations,
            strict_validation=strict_validation
        )

        # Track active batches
        self._active_batches: Dict[str, Dict] = {}

        logger.info(f"Initialized BatchMechanismDiscovery (model={model})")

    def _generate_custom_id(self, paper: PaperInput, index: int) -> str:
        """
        Generate a safe custom_id for a paper.

        Args:
            paper: Paper input object
            index: Index in the batch

        Returns:
            Safe string ID for the batch request (alphanumeric, underscore, hyphen only, max 64 chars)
        """
        import re

        if paper.custom_id:
            # Sanitize provided custom_id
            safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', paper.custom_id)
            return safe_id[:64]

        # Use DOI if available, otherwise use index
        doi = paper.citation_context.get("doi", "")
        if doi:
            # Make DOI safe for use as ID (only alphanumeric, underscore, hyphen)
            safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', doi)
            safe_id = f"doi_{safe_id}"
            return safe_id[:64]  # Max 64 chars

        return f"paper_{index}"

    def prepare_batch_requests(
        self,
        papers: List[PaperInput],
        max_tokens: int = 4000
    ) -> Tuple[List[Request], Dict[str, PaperInput]]:
        """
        Convert papers to batch request format.

        Args:
            papers: List of PaperInput objects
            max_tokens: Maximum tokens for each response

        Returns:
            Tuple of (list of Request objects, mapping of custom_id to paper)
        """
        requests = []
        paper_lookup = {}

        for i, paper in enumerate(papers):
            # Skip papers without abstracts
            if not paper.abstract:
                logger.warning(f"Skipping paper {i} (no abstract): {paper.title[:50]}...")
                continue

            # Generate safe custom_id
            custom_id = self._generate_custom_id(paper, i)

            # Create extraction prompt using V2 logic
            prompt = self.v2_discovery.create_extraction_prompt_with_verified_citation(
                paper_abstract=paper.abstract,
                paper_title=paper.title,
                citation_context=paper.citation_context,
                focus_area=paper.focus_area
            )

            # Create batch request
            request = Request(
                custom_id=custom_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
            )

            requests.append(request)
            paper_lookup[custom_id] = paper

        logger.info(f"Prepared {len(requests)} batch requests from {len(papers)} papers")
        return requests, paper_lookup

    def estimate_cost(self, papers: List[PaperInput]) -> Dict:
        """
        Estimate cost for processing papers in batch mode.

        Args:
            papers: List of papers to process

        Returns:
            Dict with cost estimates
        """
        # Estimate tokens (rough averages)
        avg_abstract_tokens = 400
        avg_prompt_overhead_tokens = 2000  # System prompt + formatting
        avg_output_tokens = 800

        total_papers = len(papers)
        input_tokens = total_papers * (avg_abstract_tokens + avg_prompt_overhead_tokens)
        output_tokens = total_papers * avg_output_tokens

        batch_cost = (
            (input_tokens / 1_000_000) * self.COST_PER_1M_INPUT_TOKENS +
            (output_tokens / 1_000_000) * self.COST_PER_1M_OUTPUT_TOKENS
        )

        # Real-time would be 2x (no 50% discount)
        realtime_cost = batch_cost * 2

        return {
            "papers": total_papers,
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "batch_cost_usd": round(batch_cost, 2),
            "realtime_cost_usd": round(realtime_cost, 2),
            "savings_usd": round(realtime_cost - batch_cost, 2),
            "savings_percent": 50
        }

    def submit_batch(
        self,
        papers: List[PaperInput],
        max_tokens: int = 4000
    ) -> str:
        """
        Submit papers for batch processing.

        Args:
            papers: List of PaperInput objects
            max_tokens: Maximum tokens per response

        Returns:
            Batch ID for tracking

        Raises:
            ValueError: If batch exceeds limits
        """
        requests, paper_lookup = self.prepare_batch_requests(papers, max_tokens)

        if len(requests) == 0:
            raise ValueError("No valid papers to process (all missing abstracts?)")

        if len(requests) > self.MAX_REQUESTS_PER_BATCH:
            raise ValueError(
                f"Batch size {len(requests)} exceeds maximum {self.MAX_REQUESTS_PER_BATCH}. "
                "Split into multiple batches."
            )

        # Submit to API
        logger.info(f"Submitting batch with {len(requests)} requests...")
        batch = self.client.messages.batches.create(requests=requests)

        # Track batch metadata
        self._active_batches[batch.id] = {
            "paper_lookup": paper_lookup,
            "submitted_at": datetime.now().isoformat(),
            "request_count": len(requests)
        }

        logger.info(f"Batch submitted: {batch.id}")
        logger.info(f"Status: {batch.processing_status}")

        # Log cost estimate
        cost_est = self.estimate_cost(papers)
        logger.info(f"Estimated cost: ${cost_est['batch_cost_usd']} (saves ${cost_est['savings_usd']} vs real-time)")

        return batch.id

    def get_batch_status(self, batch_id: str) -> Dict:
        """
        Get current status of a batch.

        Args:
            batch_id: ID returned from submit_batch

        Returns:
            Dict with status information
        """
        batch = self.client.messages.batches.retrieve(batch_id)

        return {
            "batch_id": batch_id,
            "status": batch.processing_status,
            "created_at": batch.created_at,
            "ended_at": batch.ended_at,
            "request_counts": {
                "processing": batch.request_counts.processing,
                "succeeded": batch.request_counts.succeeded,
                "errored": batch.request_counts.errored,
                "canceled": batch.request_counts.canceled
            }
        }

    def poll_until_complete(
        self,
        batch_id: str,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        max_wait: int = MAX_WAIT_TIME_SECONDS,
        progress_callback: Optional[callable] = None
    ) -> Dict:
        """
        Poll batch until completion.

        Args:
            batch_id: ID returned from submit_batch
            poll_interval: Seconds between status checks (default: 60)
            max_wait: Maximum wait time in seconds (default: 24 hours)
            progress_callback: Optional callback(status_dict) for progress updates

        Returns:
            Dict with final status
        """
        start_time = time.time()
        last_log_time = 0

        logger.info(f"Polling batch {batch_id} (interval={poll_interval}s, max_wait={max_wait}s)")

        while time.time() - start_time < max_wait:
            batch = self.client.messages.batches.retrieve(batch_id)

            status_info = {
                "batch_id": batch_id,
                "status": batch.processing_status,
                "succeeded": batch.request_counts.succeeded,
                "errored": batch.request_counts.errored,
                "processing": batch.request_counts.processing,
                "elapsed_seconds": int(time.time() - start_time)
            }

            # Log progress every 5 minutes or on status change
            current_time = time.time()
            if current_time - last_log_time >= 300:
                logger.info(
                    f"[{datetime.now().strftime('%H:%M:%S')}] "
                    f"Batch {batch_id}: {batch.processing_status} "
                    f"(succeeded={status_info['succeeded']}, "
                    f"errored={status_info['errored']}, "
                    f"processing={status_info['processing']})"
                )
                last_log_time = current_time

            # Call progress callback if provided
            if progress_callback:
                progress_callback(status_info)

            # Check if complete
            if batch.processing_status == "ended":
                elapsed = time.time() - start_time
                logger.info(f"Batch completed in {elapsed:.0f} seconds")
                return {
                    "status": BatchStatus.COMPLETED,
                    "succeeded": batch.request_counts.succeeded,
                    "failed": batch.request_counts.errored,
                    "batch_id": batch_id,
                    "processing_time_seconds": elapsed
                }

            time.sleep(poll_interval)

        # Timeout
        elapsed = time.time() - start_time
        logger.warning(f"Batch {batch_id} timed out after {elapsed:.0f} seconds")
        return {
            "status": BatchStatus.TIMEOUT,
            "batch_id": batch_id,
            "processing_time_seconds": elapsed
        }

    def cancel_batch(self, batch_id: str) -> bool:
        """
        Cancel a running batch.

        Args:
            batch_id: ID of batch to cancel

        Returns:
            True if cancellation was requested
        """
        try:
            self.client.messages.batches.cancel(batch_id)
            logger.info(f"Cancellation requested for batch {batch_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel batch {batch_id}: {e}")
            return False

    def process_results(
        self,
        batch_id: str,
        paper_lookup: Optional[Dict[str, PaperInput]] = None
    ) -> List[MechanismExtraction]:
        """
        Process batch results and validate mechanisms.

        Args:
            batch_id: ID of completed batch
            paper_lookup: Mapping of custom_id to PaperInput (if not tracked internally)

        Returns:
            List of validated MechanismExtraction objects
        """
        # Get paper lookup from tracked batches if not provided
        if paper_lookup is None:
            if batch_id in self._active_batches:
                paper_lookup = self._active_batches[batch_id]["paper_lookup"]
            else:
                raise ValueError(
                    f"No paper lookup found for batch {batch_id}. "
                    "Provide paper_lookup argument or use a batch submitted in this session."
                )

        mechanisms = []
        errors = []

        logger.info(f"Processing results for batch {batch_id}...")

        for result in self.client.messages.batches.results(batch_id):
            custom_id = result.custom_id
            paper = paper_lookup.get(custom_id)

            if result.result.type == "succeeded":
                try:
                    # Parse LLM response
                    response_text = result.result.message.content[0].text

                    # Handle JSON parsing (may be wrapped in markdown)
                    try:
                        mechanisms_data = json.loads(response_text)
                    except json.JSONDecodeError:
                        if "```json" in response_text:
                            json_start = response_text.find("```json") + 7
                            json_end = response_text.find("```", json_start)
                            response_text = response_text[json_start:json_end].strip()
                            mechanisms_data = json.loads(response_text)
                        else:
                            raise

                    # Ensure list format
                    if not isinstance(mechanisms_data, list):
                        mechanisms_data = [mechanisms_data]

                    # Validate each mechanism
                    for mech_data in mechanisms_data:
                        try:
                            mech = MechanismExtraction(**mech_data)

                            # Validate citation using V2 logic
                            if paper:
                                validated = self.v2_discovery._validate_mechanism_citation(
                                    mech, paper.citation_context
                                )
                                mechanisms.append(validated)
                            else:
                                mechanisms.append(mech)

                        except Exception as e:
                            errors.append({
                                "custom_id": custom_id,
                                "error": f"Mechanism validation error: {e}",
                                "data": mech_data
                            })

                except Exception as e:
                    errors.append({
                        "custom_id": custom_id,
                        "error": f"Response parsing error: {e}",
                        "response": response_text[:500] if response_text else None
                    })

            else:
                # Request failed
                error_type = result.result.type
                # Handle error object - it's an object with attributes, not a dict
                error_obj = getattr(result.result, 'error', None)
                if error_obj:
                    error_msg = getattr(error_obj, 'message', str(error_obj))
                else:
                    error_msg = 'Unknown error'
                errors.append({
                    "custom_id": custom_id,
                    "error": f"{error_type}: {error_msg}"
                })

        logger.info(f"Processed {len(mechanisms)} mechanisms, {len(errors)} errors")

        if errors:
            logger.warning(f"Batch had {len(errors)} errors:")
            for err in errors[:5]:  # Show first 5
                logger.warning(f"  - {err['custom_id']}: {err['error']}")
            if len(errors) > 5:
                logger.warning(f"  ... and {len(errors) - 5} more")

        return mechanisms

    def discover_mechanisms_batch(
        self,
        papers: List[PaperInput],
        output_dir: Optional[Path] = None,
        wait_for_completion: bool = True,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        save_report: bool = True,
        report_path: Optional[Path] = None
    ) -> BatchResult:
        """
        Full batch discovery workflow.

        Args:
            papers: List of PaperInput objects
            output_dir: Where to save YAML files (optional)
            wait_for_completion: If False, return batch_id immediately
            poll_interval: Seconds between status checks
            save_report: Whether to save a JSON report
            report_path: Path for report (default: discovery_batch_report.json)

        Returns:
            BatchResult with status and mechanisms
        """
        start_time = time.time()

        # Log cost estimate
        cost_est = self.estimate_cost(papers)
        logger.info(f"Batch discovery: {len(papers)} papers")
        logger.info(f"Estimated cost: ${cost_est['batch_cost_usd']} (batch) vs ${cost_est['realtime_cost_usd']} (real-time)")
        logger.info(f"Savings: ${cost_est['savings_usd']} ({cost_est['savings_percent']}%)")

        # Submit batch
        batch_id = self.submit_batch(papers)

        if not wait_for_completion:
            return BatchResult(
                batch_id=batch_id,
                status=BatchStatus.SUBMITTED
            )

        # Wait for completion
        poll_result = self.poll_until_complete(batch_id, poll_interval)

        if poll_result["status"] != BatchStatus.COMPLETED:
            return BatchResult(
                batch_id=batch_id,
                status=poll_result["status"],
                processing_time_seconds=poll_result.get("processing_time_seconds")
            )

        # Process results
        mechanisms = self.process_results(batch_id)

        # Save to mechanism bank if output_dir provided
        saved_count = 0
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            for mech in mechanisms:
                try:
                    self.v2_discovery.save_mechanism(mech, output_dir)
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving mechanism: {e}")

            logger.info(f"Saved {saved_count} mechanisms to {output_dir}")

        # Calculate final stats
        processing_time = time.time() - start_time

        result = BatchResult(
            batch_id=batch_id,
            status=BatchStatus.COMPLETED,
            mechanisms=mechanisms,
            succeeded_count=poll_result["succeeded"],
            failed_count=poll_result["failed"],
            processing_time_seconds=processing_time,
            cost_estimate_usd=cost_est["batch_cost_usd"]
        )

        # Save report
        if save_report:
            report_path = report_path or Path("discovery_batch_report.json")
            self._save_report(result, papers, report_path)

        return result

    def _save_report(
        self,
        result: BatchResult,
        papers: List[PaperInput],
        report_path: Path
    ):
        """Save batch discovery report to JSON."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "batch_id": result.batch_id,
            "status": result.status.value,
            "summary": {
                "papers_submitted": len(papers),
                "requests_succeeded": result.succeeded_count,
                "requests_failed": result.failed_count,
                "mechanisms_extracted": len(result.mechanisms),
                "processing_time_seconds": result.processing_time_seconds,
                "cost_estimate_usd": result.cost_estimate_usd
            },
            "mechanisms": [
                {
                    "id": f"{m.from_node_id}_to_{m.to_node_id}",
                    "from": m.from_node_name,
                    "to": m.to_node_name,
                    "direction": m.direction,
                    "category": m.category,
                    "confidence": m.confidence,
                    "citation_verified": m.citation_verified,
                    "needs_review": m.needs_manual_review
                }
                for m in result.mechanisms
            ]
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Report saved to: {report_path}")

    def list_batches(self, limit: int = 10) -> List[Dict]:
        """
        List recent batches.

        Args:
            limit: Maximum number of batches to return

        Returns:
            List of batch info dicts
        """
        batches = []

        for batch in self.client.messages.batches.list(limit=limit):
            batches.append({
                "id": batch.id,
                "status": batch.processing_status,
                "created_at": batch.created_at,
                "ended_at": batch.ended_at,
                "succeeded": batch.request_counts.succeeded,
                "errored": batch.request_counts.errored,
                "processing": batch.request_counts.processing
            })

        return batches


# Convenience functions for common use cases

def papers_from_literature_search(papers: List) -> List[PaperInput]:
    """
    Convert papers from LiteratureSearchAggregator to PaperInput format.

    Args:
        papers: List of Paper objects from literature_search.py

    Returns:
        List of PaperInput objects ready for batch processing
    """
    return [
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
            custom_id=None  # Will be generated from DOI
        )
        for p in papers
        if p.abstract  # Only include papers with abstracts
    ]


def quick_batch_discovery(
    topic_query: str,
    max_papers: int = 50,
    output_dir: Optional[Path] = None,
    wait: bool = True
) -> BatchResult:
    """
    Quick batch discovery for a single topic.

    Example:
        result = quick_batch_discovery(
            topic_query="housing quality respiratory health asthma",
            max_papers=100,
            output_dir=Path("mechanism-bank/mechanisms")
        )
        print(f"Extracted {len(result.mechanisms)} mechanisms")

    Args:
        topic_query: Search query for literature
        max_papers: Maximum papers to process
        output_dir: Where to save mechanisms
        wait: Whether to wait for completion

    Returns:
        BatchResult
    """
    # Import here to avoid circular imports
    try:
        from pipelines.literature_search import LiteratureSearchAggregator
    except ImportError:
        from backend.pipelines.literature_search import LiteratureSearchAggregator

    # Search for papers
    aggregator = LiteratureSearchAggregator(
        pubmed_email=os.getenv("PUBMED_EMAIL", "healthsystems@example.com")
    )

    papers = aggregator.search(
        query=topic_query,
        limit_per_source=max_papers // 2,
        year_range=(2015, 2024),
        min_citations=5
    )

    if not papers:
        logger.warning(f"No papers found for query: {topic_query}")
        return BatchResult(
            batch_id="",
            status=BatchStatus.FAILED,
            error_details=[{"error": "No papers found"}]
        )

    # Convert to batch format
    paper_inputs = papers_from_literature_search(papers)

    # Run batch discovery
    batch = BatchMechanismDiscovery()
    return batch.discover_mechanisms_batch(
        papers=paper_inputs,
        output_dir=output_dir,
        wait_for_completion=wait
    )


if __name__ == "__main__":
    # Demo: Batch discovery
    print("\n" + "="*80)
    print("DEMO: Batch Mechanism Discovery (50% cost savings)")
    print("="*80 + "\n")

    # Example papers (in production, these come from literature search)
    demo_papers = [
        PaperInput(
            abstract="""Poor housing quality increases respiratory health risks in children.
            This systematic review examined 15 studies with 50,000 participants. Children
            in poor-quality housing had 1.8 times higher odds of asthma-related ED visits
            (95% CI: 1.4-2.3, p<0.001). Mold exposure was the strongest predictor.""",
            title="Housing Quality and Pediatric Asthma: A Systematic Review",
            citation_context={
                "authors": ["Smith, J.", "Jones, M.", "Brown, K."],
                "year": 2023,
                "doi": "10.1234/test.2023.001",
                "journal": "Journal of Public Health",
                "title": "Housing Quality and Pediatric Asthma: A Systematic Review"
            },
            focus_area="housing to respiratory health"
        ),
        PaperInput(
            abstract="""Food insecurity is associated with increased risk of type 2 diabetes.
            This meta-analysis of 12 cohort studies found food insecure adults had 2.1 times
            higher risk of developing diabetes (RR=2.1, 95% CI: 1.7-2.6). The association
            was stronger among low-income populations.""",
            title="Food Insecurity and Diabetes Risk: A Meta-Analysis",
            citation_context={
                "authors": ["Garcia, A.", "Lee, S."],
                "year": 2024,
                "doi": "10.5678/demo.2024.002",
                "journal": "Diabetes Care",
                "title": "Food Insecurity and Diabetes Risk: A Meta-Analysis"
            },
            focus_area="food security to chronic disease"
        )
    ]

    # Estimate cost
    batch = BatchMechanismDiscovery()
    cost_est = batch.estimate_cost(demo_papers)

    print(f"Papers to process: {cost_est['papers']}")
    print(f"Estimated batch cost: ${cost_est['batch_cost_usd']}")
    print(f"Real-time cost would be: ${cost_est['realtime_cost_usd']}")
    print(f"Savings: ${cost_est['savings_usd']} ({cost_est['savings_percent']}%)")

    print("\n[Demo mode - not actually submitting batch]")
    print("In production, run:")
    print("  result = batch.discover_mechanisms_batch(papers, output_dir=...)")
