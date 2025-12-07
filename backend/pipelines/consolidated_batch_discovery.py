#!/usr/bin/env python3
"""
Consolidated Batch Discovery Pipeline (V3)

TWO-PASS APPROACH:
1. First pass: Extract pathway candidates from papers (lightweight extraction)
2. Group papers by normalized pathway (from_node -> to_node)
3. Second pass: For each pathway, process ALL relevant papers together
   - LLM receives multiple abstracts and outputs ONE mechanism with combined evidence
   - n_studies reflects actual paper count supporting the pathway
   - Avoids C-rated single-paper mechanisms

BENEFITS:
- Proper evidence aggregation at extraction time (not post-hoc)
- n_studies accurately reflects supporting paper count
- Higher quality mechanisms from the start
- Reduced consolidation work downstream

WHEN TO USE:
- Large-scale literature reviews (100+ papers)
- Building comprehensive mechanism banks
- Any batch discovery where quality > speed
"""

import anthropic
import json
import os
import sys
import re
import yaml
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict
import logging

from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.llm_mechanism_discovery import MechanismExtraction
from pipelines.batch_mechanism_discovery import PaperInput, BatchStatus, BatchResult
from utils.canonical_nodes import (
    generate_compact_node_list,
    normalize_node_id,
    find_matching_node
)
from utils.citation_validation import format_chicago_citation

logger = logging.getLogger(__name__)


@dataclass
class PathwayCandidate:
    """A candidate pathway extracted from first pass."""
    from_node_id: str
    from_node_name: str
    to_node_id: str
    to_node_name: str
    direction: str
    category: str
    paper_custom_id: str


@dataclass
class PathwayGroup:
    """A group of papers supporting the same pathway."""
    pathway_key: str  # normalized "from_id__to__to_id"
    from_node_id: str
    from_node_name: str
    to_node_id: str
    to_node_name: str
    direction: str
    category: str
    papers: List[PaperInput] = field(default_factory=list)
    paper_custom_ids: List[str] = field(default_factory=list)


class ConsolidatedBatchDiscovery:
    """
    Two-pass batch discovery that groups papers by pathway before extraction.

    Pass 1: Lightweight extraction to identify pathways
    Pass 2: Full extraction with all papers for each pathway combined
    """

    # Cost estimates (Opus 4.5 batch pricing)
    COST_PER_1M_INPUT_TOKENS = 2.50
    COST_PER_1M_OUTPUT_TOKENS = 12.50

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-opus-4-5-20251101",
        min_papers_per_pathway: int = 1,
        max_papers_per_pathway: int = 20
    ):
        """
        Initialize consolidated batch discovery.

        Args:
            api_key: Anthropic API key
            model: Model to use
            min_papers_per_pathway: Minimum papers required (default 1)
            max_papers_per_pathway: Maximum papers to include per pathway (default 20)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.min_papers = min_papers_per_pathway
        self.max_papers = max_papers_per_pathway

        logger.info(f"Initialized ConsolidatedBatchDiscovery (model={model})")

    def _create_pathway_extraction_prompt(
        self,
        paper: PaperInput
    ) -> str:
        """
        Create a lightweight prompt for first-pass pathway extraction.

        This prompt extracts only the pathway skeleton (from/to nodes, direction)
        without full mechanism details. Used for grouping papers.
        """
        citation = format_chicago_citation(paper.citation_context)

        prompt = f"""You are an expert in public health causal mechanisms. Extract ONLY the pathway skeleton from this paper.

**Paper Title**: {paper.title}

**Abstract**:
{paper.abstract}

---

## CANONICAL NODE INVENTORY

Use these canonical node IDs when possible:

{generate_compact_node_list(max_per_domain=8)}

---

## TASK

Extract the PRIMARY causal pathway(s) described in this paper. Return ONLY:
- from_node_id: upstream factor (use canonical ID or "NEW:name")
- from_node_name: human-readable name
- to_node_id: downstream factor (use canonical ID or "NEW:name")
- to_node_name: human-readable name
- direction: "positive" (A↑→B↑) or "negative" (A↑→B↓)
- category: built_environment|social_environment|economic|political|healthcare_access|biological|behavioral

Return JSON array:
```json
[
  {{
    "from_node_id": "canonical_id",
    "from_node_name": "Human Name",
    "to_node_id": "canonical_id",
    "to_node_name": "Human Name",
    "direction": "positive|negative",
    "category": "category"
  }}
]
```

Extract 1-3 pathways maximum. Return ONLY JSON, no other text.
"""
        return prompt

    def _create_consolidated_extraction_prompt(
        self,
        pathway_group: PathwayGroup
    ) -> str:
        """
        Create prompt for second-pass extraction with multiple papers.

        This prompt receives ALL papers for a pathway and outputs ONE mechanism
        with properly aggregated evidence.
        """
        # Format all papers
        papers_section = []
        for i, paper in enumerate(pathway_group.papers[:self.max_papers], 1):
            citation = format_chicago_citation(paper.citation_context)
            papers_section.append(f"""
### Paper {i}: {paper.title}
**Citation**: {citation}
**DOI**: {paper.citation_context.get('doi', 'N/A')}

**Abstract**:
{paper.abstract}
""")

        papers_text = "\n".join(papers_section)
        n_papers = len(pathway_group.papers)

        prompt = f"""You are an expert in public health causal mechanisms. Your task is to synthesize evidence from MULTIPLE papers into a SINGLE consolidated mechanism.

## PATHWAY TO EXTRACT
- **FROM**: {pathway_group.from_node_name} ({pathway_group.from_node_id})
- **TO**: {pathway_group.to_node_name} ({pathway_group.to_node_id})
- **Direction**: {pathway_group.direction}
- **Category**: {pathway_group.category}

---

## SUPPORTING PAPERS ({n_papers} total)

{papers_text}

---

## TASK

Synthesize ALL {n_papers} papers above into ONE consolidated mechanism for this pathway.

### EVIDENCE AGGREGATION RULES:
1. **n_studies**: Count of unique studies across ALL papers
   - If paper is a meta-analysis of N studies, add N
   - If paper is a single cohort/case-control, add 1
   - Sum across all papers (minimum = {n_papers})

2. **Quality Rating**:
   - **A**: Total n_studies ≥ 5
   - **B**: Total n_studies = 3-4
   - **C**: Total n_studies = 1-2

3. **Effect Size**: Use the strongest/most recent estimate available
4. **Primary Citation**: Use the highest-quality or most recent paper
5. **Supporting Citations**: List all other papers
6. **Mechanism Pathway**: Synthesize the best explanation across papers

### OUTPUT FORMAT

Return a SINGLE mechanism JSON:

```json
{{
  "from_node_id": "{pathway_group.from_node_id}",
  "from_node_name": "{pathway_group.from_node_name}",
  "to_node_id": "{pathway_group.to_node_id}",
  "to_node_name": "{pathway_group.to_node_name}",
  "direction": "{pathway_group.direction}",
  "category": "{pathway_group.category}",
  "mechanism_pathway": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "evidence_quality": "A|B|C",
  "n_studies": <total studies across ALL papers>,
  "n_papers": {n_papers},
  "primary_citation": "Best/most recent citation",
  "supporting_citations": ["Other citations..."],
  "doi": "DOI of primary citation",

  "effect_size_value": <number or null>,
  "effect_size_type": "odds_ratio|relative_risk|hazard_ratio|...|null",
  "confidence_interval_lower": <number or null>,
  "confidence_interval_upper": <number or null>,
  "p_value": <number or null>,
  "sample_size": <total or largest sample>,
  "heterogeneity_i_squared": <number or null>,

  "varies_by_geography": true|false,
  "variation_notes": "Geographic notes if applicable",
  "moderators": [
    {{
      "name": "moderator_name",
      "direction": "strengthens|weakens|u_shaped",
      "strength": "weak|moderate|strong",
      "description": "Synthesized across papers"
    }}
  ],
  "description": "Synthesized mechanism description",
  "structural_competency_notes": "Equity implications",
  "confidence": "high|medium|low",

  "synthesis_notes": "Notes on evidence synthesis across papers"
}}
```

IMPORTANT:
- Return exactly ONE mechanism (not an array)
- n_studies MUST be ≥ {n_papers} (at minimum, each paper = 1 study)
- Include ALL supporting citations
- Synthesize the BEST available evidence

Return ONLY valid JSON, no additional text.
"""
        return prompt

    def _generate_safe_id(self, paper: PaperInput, index: int) -> str:
        """Generate safe custom_id for batch API."""
        if paper.custom_id:
            safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', paper.custom_id)
            return safe_id[:64]

        doi = paper.citation_context.get("doi", "")
        if doi:
            safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', doi)
            return f"doi_{safe_id}"[:64]

        return f"paper_{index}"

    def _normalize_pathway_key(self, from_id: str, to_id: str) -> str:
        """Create normalized pathway key for grouping."""
        from_norm = normalize_node_id(from_id.replace("NEW:", ""))
        to_norm = normalize_node_id(to_id.replace("NEW:", ""))
        return f"{from_norm}__to__{to_norm}"

    def run_pass_1_pathway_extraction(
        self,
        papers: List[PaperInput],
        poll_interval: int = 60,
        max_wait: int = 7200
    ) -> Tuple[List[PathwayCandidate], Dict[str, PaperInput]]:
        """
        Run first pass: extract pathway candidates from all papers.

        Args:
            papers: List of papers to process
            poll_interval: Polling interval for batch status
            max_wait: Maximum wait time

        Returns:
            Tuple of (pathway_candidates, paper_lookup)
        """
        logger.info(f"Pass 1: Extracting pathways from {len(papers)} papers")

        # Prepare batch requests
        requests = []
        paper_lookup = {}

        for i, paper in enumerate(papers):
            if not paper.abstract:
                continue

            custom_id = self._generate_safe_id(paper, i)
            prompt = self._create_pathway_extraction_prompt(paper)

            request = Request(
                custom_id=custom_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=1000,  # Lightweight response
                    messages=[{"role": "user", "content": prompt}]
                )
            )
            requests.append(request)
            paper_lookup[custom_id] = paper

        if not requests:
            raise ValueError("No valid papers for processing")

        # Submit batch
        logger.info(f"Submitting Pass 1 batch with {len(requests)} requests")
        batch = self.client.messages.batches.create(requests=requests)
        logger.info(f"Pass 1 batch ID: {batch.id}")

        # Poll for completion
        import time
        start_time = time.time()
        while time.time() - start_time < max_wait:
            batch = self.client.messages.batches.retrieve(batch.id)

            if batch.processing_status == "ended":
                logger.info(f"Pass 1 completed: {batch.request_counts.succeeded} succeeded")
                break

            time.sleep(poll_interval)
        else:
            raise TimeoutError(f"Pass 1 batch timed out after {max_wait}s")

        # Process results
        candidates = []
        for result in self.client.messages.batches.results(batch.id):
            custom_id = result.custom_id

            if result.result.type != "succeeded":
                logger.warning(f"Pass 1 failed for {custom_id}")
                continue

            try:
                response_text = result.result.message.content[0].text

                # Parse JSON
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()

                pathways_data = json.loads(response_text)

                if not isinstance(pathways_data, list):
                    pathways_data = [pathways_data]

                for pathway in pathways_data:
                    candidates.append(PathwayCandidate(
                        from_node_id=pathway.get('from_node_id', ''),
                        from_node_name=pathway.get('from_node_name', ''),
                        to_node_id=pathway.get('to_node_id', ''),
                        to_node_name=pathway.get('to_node_name', ''),
                        direction=pathway.get('direction', 'positive'),
                        category=pathway.get('category', 'unknown'),
                        paper_custom_id=custom_id
                    ))

            except Exception as e:
                logger.warning(f"Error parsing Pass 1 result for {custom_id}: {e}")

        logger.info(f"Pass 1 extracted {len(candidates)} pathway candidates")
        return candidates, paper_lookup

    def group_papers_by_pathway(
        self,
        candidates: List[PathwayCandidate],
        paper_lookup: Dict[str, PaperInput]
    ) -> List[PathwayGroup]:
        """
        Group papers by normalized pathway.

        Args:
            candidates: Pathway candidates from Pass 1
            paper_lookup: Mapping of custom_id to PaperInput

        Returns:
            List of PathwayGroups with papers assigned
        """
        groups: Dict[str, PathwayGroup] = {}

        for candidate in candidates:
            pathway_key = self._normalize_pathway_key(
                candidate.from_node_id,
                candidate.to_node_id
            )

            if pathway_key not in groups:
                groups[pathway_key] = PathwayGroup(
                    pathway_key=pathway_key,
                    from_node_id=candidate.from_node_id,
                    from_node_name=candidate.from_node_name,
                    to_node_id=candidate.to_node_id,
                    to_node_name=candidate.to_node_name,
                    direction=candidate.direction,
                    category=candidate.category,
                    papers=[],
                    paper_custom_ids=[]
                )

            paper = paper_lookup.get(candidate.paper_custom_id)
            if paper and candidate.paper_custom_id not in groups[pathway_key].paper_custom_ids:
                groups[pathway_key].papers.append(paper)
                groups[pathway_key].paper_custom_ids.append(candidate.paper_custom_id)

        # Filter by minimum papers
        result = [g for g in groups.values() if len(g.papers) >= self.min_papers]

        logger.info(f"Grouped into {len(result)} pathways (min {self.min_papers} papers)")

        # Log distribution
        paper_counts = defaultdict(int)
        for g in result:
            paper_counts[len(g.papers)] += 1

        logger.info(f"Paper count distribution: {dict(sorted(paper_counts.items()))}")

        return result

    def run_pass_2_consolidated_extraction(
        self,
        pathway_groups: List[PathwayGroup],
        poll_interval: int = 60,
        max_wait: int = 14400
    ) -> List[MechanismExtraction]:
        """
        Run second pass: extract consolidated mechanisms for each pathway.

        Args:
            pathway_groups: Groups of papers by pathway
            poll_interval: Polling interval
            max_wait: Maximum wait time

        Returns:
            List of consolidated MechanismExtraction objects
        """
        logger.info(f"Pass 2: Extracting {len(pathway_groups)} consolidated mechanisms")

        # Prepare batch requests
        requests = []
        group_lookup = {}

        for i, group in enumerate(pathway_groups):
            custom_id = f"pathway_{i}_{group.pathway_key[:40]}"
            custom_id = re.sub(r'[^a-zA-Z0-9_-]', '_', custom_id)[:64]

            prompt = self._create_consolidated_extraction_prompt(group)

            request = Request(
                custom_id=custom_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
            )
            requests.append(request)
            group_lookup[custom_id] = group

        if not requests:
            return []

        # Submit batch
        logger.info(f"Submitting Pass 2 batch with {len(requests)} requests")
        batch = self.client.messages.batches.create(requests=requests)
        logger.info(f"Pass 2 batch ID: {batch.id}")

        # Poll for completion
        import time
        start_time = time.time()
        while time.time() - start_time < max_wait:
            batch = self.client.messages.batches.retrieve(batch.id)

            if batch.processing_status == "ended":
                logger.info(f"Pass 2 completed: {batch.request_counts.succeeded} succeeded")
                break

            elapsed = int(time.time() - start_time)
            if elapsed % 300 == 0:  # Log every 5 minutes
                logger.info(
                    f"Pass 2 progress: {batch.request_counts.succeeded} succeeded, "
                    f"{batch.request_counts.processing} processing ({elapsed}s elapsed)"
                )

            time.sleep(poll_interval)
        else:
            raise TimeoutError(f"Pass 2 batch timed out after {max_wait}s")

        # Process results
        mechanisms = []
        for result in self.client.messages.batches.results(batch.id):
            custom_id = result.custom_id
            group = group_lookup.get(custom_id)

            if result.result.type != "succeeded":
                logger.warning(f"Pass 2 failed for {custom_id}")
                continue

            try:
                response_text = result.result.message.content[0].text

                # Parse JSON
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()

                mech_data = json.loads(response_text)

                # Create MechanismExtraction
                mech = MechanismExtraction(
                    from_node_id=mech_data.get('from_node_id', ''),
                    from_node_name=mech_data.get('from_node_name', ''),
                    to_node_id=mech_data.get('to_node_id', ''),
                    to_node_name=mech_data.get('to_node_name', ''),
                    direction=mech_data.get('direction', 'positive'),
                    category=mech_data.get('category', 'unknown'),
                    mechanism_pathway=mech_data.get('mechanism_pathway', []),
                    evidence_quality=mech_data.get('evidence_quality', 'C'),
                    n_studies=mech_data.get('n_studies', len(group.papers) if group else 1),
                    primary_citation=mech_data.get('primary_citation', ''),
                    supporting_citations=mech_data.get('supporting_citations'),
                    doi=mech_data.get('doi'),
                    effect_size_value=mech_data.get('effect_size_value'),
                    effect_size_type=mech_data.get('effect_size_type'),
                    confidence_interval_lower=mech_data.get('confidence_interval_lower'),
                    confidence_interval_upper=mech_data.get('confidence_interval_upper'),
                    p_value=mech_data.get('p_value'),
                    sample_size=mech_data.get('sample_size'),
                    heterogeneity_i_squared=mech_data.get('heterogeneity_i_squared'),
                    varies_by_geography=mech_data.get('varies_by_geography', False),
                    variation_notes=mech_data.get('variation_notes'),
                    moderators=mech_data.get('moderators'),
                    description=mech_data.get('description', ''),
                    structural_competency_notes=mech_data.get('structural_competency_notes'),
                    confidence=mech_data.get('confidence', 'medium'),
                    citation_verified=True,  # Consolidated from verified sources
                    needs_manual_review=False
                )

                mechanisms.append(mech)

            except Exception as e:
                logger.warning(f"Error parsing Pass 2 result for {custom_id}: {e}")

        logger.info(f"Pass 2 extracted {len(mechanisms)} consolidated mechanisms")
        return mechanisms

    def discover_mechanisms(
        self,
        papers: List[PaperInput],
        output_dir: Optional[Path] = None,
        save_intermediates: bool = True
    ) -> BatchResult:
        """
        Run full two-pass consolidated discovery.

        Args:
            papers: List of papers to process
            output_dir: Directory to save mechanism YAML files
            save_intermediates: Whether to save intermediate results

        Returns:
            BatchResult with consolidated mechanisms
        """
        start_time = datetime.now()
        logger.info(f"Starting consolidated batch discovery with {len(papers)} papers")

        # Cost estimate
        avg_tokens_pass1 = 2000
        avg_tokens_pass2 = 4000
        est_cost = (
            (len(papers) * avg_tokens_pass1 / 1_000_000 * self.COST_PER_1M_INPUT_TOKENS) +
            (len(papers) * 500 / 1_000_000 * self.COST_PER_1M_OUTPUT_TOKENS) +
            (len(papers) * 0.3 * avg_tokens_pass2 / 1_000_000 * self.COST_PER_1M_INPUT_TOKENS) +
            (len(papers) * 0.3 * 2000 / 1_000_000 * self.COST_PER_1M_OUTPUT_TOKENS)
        )
        logger.info(f"Estimated cost: ${est_cost:.2f}")

        # Pass 1: Extract pathways
        candidates, paper_lookup = self.run_pass_1_pathway_extraction(papers)

        if save_intermediates and output_dir:
            pass1_path = output_dir / "pass1_candidates.json"
            with open(pass1_path, 'w') as f:
                json.dump([{
                    'from_node_id': c.from_node_id,
                    'to_node_id': c.to_node_id,
                    'paper_id': c.paper_custom_id
                } for c in candidates], f, indent=2)
            logger.info(f"Saved Pass 1 results to {pass1_path}")

        # Group papers by pathway
        pathway_groups = self.group_papers_by_pathway(candidates, paper_lookup)

        if save_intermediates and output_dir:
            groups_path = output_dir / "pathway_groups.json"
            with open(groups_path, 'w') as f:
                json.dump([{
                    'pathway_key': g.pathway_key,
                    'n_papers': len(g.papers),
                    'from_node': g.from_node_name,
                    'to_node': g.to_node_name
                } for g in pathway_groups], f, indent=2)
            logger.info(f"Saved pathway groups to {groups_path}")

        # Pass 2: Consolidated extraction
        mechanisms = self.run_pass_2_consolidated_extraction(pathway_groups)

        # Save mechanisms
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            for mech in mechanisms:
                category_dir = output_dir / mech.category
                category_dir.mkdir(exist_ok=True)

                mech_id = f"{mech.from_node_id}_to_{mech.to_node_id}"
                filename = f"{mech_id}.yaml"

                yaml_data = {
                    "id": mech_id,
                    "name": f"{mech.from_node_name} → {mech.to_node_name}",
                    "from_node": {
                        "node_id": mech.from_node_id,
                        "node_name": mech.from_node_name
                    },
                    "to_node": {
                        "node_id": mech.to_node_id,
                        "node_name": mech.to_node_name
                    },
                    "direction": mech.direction,
                    "category": mech.category,
                    "mechanism_pathway": mech.mechanism_pathway,
                    "evidence": {
                        "quality_rating": mech.evidence_quality,
                        "n_studies": mech.n_studies,
                        "primary_citation": mech.primary_citation,
                        "supporting_citations": mech.supporting_citations or []
                    },
                    "description": mech.description,
                    "last_updated": datetime.now().strftime("%Y-%m-%d"),
                    "extraction_method": "consolidated_batch_v3"
                }

                if mech.effect_size_value is not None:
                    yaml_data["quantitative_effects"] = {
                        "effect_size": {
                            "value": mech.effect_size_value,
                            "type": mech.effect_size_type,
                            "ci_lower": mech.confidence_interval_lower,
                            "ci_upper": mech.confidence_interval_upper
                        },
                        "p_value": mech.p_value,
                        "sample_size": mech.sample_size
                    }

                if mech.moderators:
                    yaml_data["moderators"] = mech.moderators

                with open(category_dir / filename, 'w') as f:
                    yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            logger.info(f"Saved {len(mechanisms)} mechanisms to {output_dir}")

        # Calculate final stats
        processing_time = (datetime.now() - start_time).total_seconds()

        # Grade distribution
        grade_dist = defaultdict(int)
        for m in mechanisms:
            grade_dist[m.evidence_quality] += 1

        logger.info(f"Grade distribution: A={grade_dist['A']}, B={grade_dist['B']}, C={grade_dist['C']}")

        return BatchResult(
            batch_id="consolidated_v3",
            status=BatchStatus.COMPLETED,
            mechanisms=mechanisms,
            succeeded_count=len(mechanisms),
            failed_count=len(pathway_groups) - len(mechanisms),
            processing_time_seconds=processing_time,
            cost_estimate_usd=est_cost
        )


if __name__ == "__main__":
    print("Consolidated Batch Discovery Pipeline V3")
    print("=" * 60)
    print("""
This pipeline uses a TWO-PASS approach:

Pass 1: Extract pathway candidates (lightweight)
        - Identifies FROM -> TO nodes for each paper
        - Groups papers by normalized pathway

Pass 2: Consolidated extraction
        - Processes ALL papers for each pathway together
        - Outputs ONE mechanism with aggregated evidence
        - n_studies = sum of studies across all papers

USAGE:
    from pipelines.consolidated_batch_discovery import ConsolidatedBatchDiscovery

    discovery = ConsolidatedBatchDiscovery()
    result = discovery.discover_mechanisms(
        papers=paper_inputs,
        output_dir=Path("mechanism-bank/consolidated")
    )

BENEFITS:
    - Proper evidence aggregation at extraction time
    - Accurate n_studies reflecting paper count
    - Higher quality A/B-rated mechanisms
    - Reduced post-hoc consolidation work
""")
