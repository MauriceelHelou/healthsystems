#!/usr/bin/env python3
"""
Node-Pair Driven Discovery Pipeline (V4)

NODE-PAIR FIRST approach:
1. Node pairs are defined UPFRONT from configuration
2. Literature search uses node-adjacent keywords for better coverage
3. For each node pair, search papers and consolidate into ONE mechanism
4. If no evidence exists, return null (DON'T force mechanisms)
5. Only use existing nodes from nodes/by_scale/ (NO new nodes)

KEY DIFFERENCES FROM V3:
- V3: Paper-first (extract pathways from papers, then group)
- V4: Node-first (define pairs upfront, search for evidence)

CRITICAL REQUIREMENTS:
- ONLY use node IDs from nodes/by_scale/
- Return null if insufficient evidence (don't force)
- Use node-adjacent keywords for broader search
- Consolidate multiple papers into ONE mechanism
- Minimum 3 citations per mechanism
"""

import anthropic
import json
import os
import sys
import re
import yaml
import time
import logging
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict

from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.batch_mechanism_discovery import PaperInput, BatchStatus, BatchResult
from pipelines.literature_search import LiteratureSearchAggregator

logger = logging.getLogger(__name__)


@dataclass
class NodePair:
    """A node pair to search for evidence."""
    from_node_id: str
    from_node_name: str
    to_node_id: str
    to_node_name: str
    expected_direction: str
    category: str
    priority: int
    from_keywords: List[str] = field(default_factory=list)
    to_keywords: List[str] = field(default_factory=list)


@dataclass
class NodePairEvidence:
    """Evidence collected for a node pair."""
    node_pair: NodePair
    papers: List[PaperInput] = field(default_factory=list)
    search_queries_used: List[str] = field(default_factory=list)


@dataclass
class MechanismResult:
    """Result of mechanism extraction for a node pair."""
    node_pair: NodePair
    mechanism: Optional[Dict[str, Any]] = None
    evidence_found: bool = False
    n_papers: int = 0
    insufficient_evidence: bool = False
    error: Optional[str] = None


class NodePairDiscovery:
    """
    Node-pair driven discovery pipeline.

    Process:
    1. Load node pairs from config
    2. Load node metadata from nodes/by_scale/
    3. For each pair, search literature using keywords
    4. Consolidate papers into ONE mechanism
    5. Return null if insufficient evidence
    """

    # Cost estimates (Claude Sonnet batch pricing)
    COST_PER_1M_INPUT_TOKENS = 1.50
    COST_PER_1M_OUTPUT_TOKENS = 7.50

    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        pubmed_email: Optional[str] = None,
        semantic_scholar_key: Optional[str] = None
    ):
        """
        Initialize node-pair discovery.

        Args:
            config_path: Path to node pairs config JSON
            api_key: Anthropic API key (only required for batch submission)
            model: Model to use
            pubmed_email: Email for PubMed API
            semantic_scholar_key: API key for Semantic Scholar
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Defer API key check to batch submission
        self.client = None
        self.model = model
        self.config_path = config_path
        self.config = None
        self.node_metadata: Dict[str, Dict] = {}

        # Literature search
        self.pubmed_email = pubmed_email or os.getenv("PUBMED_EMAIL")
        self.ss_key = semantic_scholar_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")

        logger.info(f"Initialized NodePairDiscovery (model={model})")

    def _ensure_client(self):
        """Initialize Anthropic client when needed."""
        if self.client is None:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def load_config(self, config_path: str) -> Dict:
        """Load node pairs configuration."""
        with open(config_path) as f:
            self.config = json.load(f)
        logger.info(f"Loaded config: {self.config.get('name', 'unnamed')}")
        return self.config

    def load_node_metadata(self, nodes_dir: str = "nodes/by_scale") -> Dict[str, Dict]:
        """
        Load node metadata from nodes/by_scale directory.

        Returns:
            Dict mapping node_id to full node metadata
        """
        nodes_path = Path(nodes_dir)
        if not nodes_path.exists():
            raise ValueError(f"Nodes directory not found: {nodes_dir}")

        self.node_metadata = {}

        for scale_dir in nodes_path.iterdir():
            if not scale_dir.is_dir():
                continue

            for yaml_file in scale_dir.glob("*.yaml"):
                try:
                    with open(yaml_file) as f:
                        node_data = yaml.safe_load(f)
                        if node_data and 'id' in node_data:
                            node_id = node_data['id']
                            self.node_metadata[node_id] = node_data
                except Exception as e:
                    logger.warning(f"Error loading {yaml_file}: {e}")

        logger.info(f"Loaded {len(self.node_metadata)} nodes from {nodes_dir}")
        return self.node_metadata

    def validate_node_exists(self, node_id: str) -> bool:
        """Check if a node exists in the loaded metadata."""
        return node_id in self.node_metadata

    def get_node_name(self, node_id: str) -> str:
        """Get human-readable name for a node."""
        if node_id in self.node_metadata:
            return self.node_metadata[node_id].get('name', node_id)
        return node_id.replace('_', ' ').title()

    def build_node_pairs(self) -> List[NodePair]:
        """
        Build NodePair objects from config, validating all nodes exist.

        Returns:
            List of validated NodePair objects
        """
        if not self.config:
            raise ValueError("Config not loaded. Call load_config() first.")

        if not self.node_metadata:
            self.load_node_metadata(self.config.get('node_source', 'nodes/by_scale'))

        node_keywords = self.config.get('node_keywords', {})
        pairs = []
        skipped = []

        for pair_config in self.config.get('node_pairs', []):
            from_id = pair_config['from_node_id']
            to_id = pair_config['to_node_id']

            # Validate both nodes exist
            from_exists = self.validate_node_exists(from_id)
            to_exists = self.validate_node_exists(to_id)

            if not from_exists or not to_exists:
                missing = []
                if not from_exists:
                    missing.append(f"from:{from_id}")
                if not to_exists:
                    missing.append(f"to:{to_id}")
                skipped.append((from_id, to_id, missing))
                logger.warning(f"Skipping pair {from_id} -> {to_id}: missing nodes {missing}")
                continue

            pair = NodePair(
                from_node_id=from_id,
                from_node_name=self.get_node_name(from_id),
                to_node_id=to_id,
                to_node_name=self.get_node_name(to_id),
                expected_direction=pair_config.get('expected_direction', 'positive'),
                category=pair_config.get('category', 'unknown'),
                priority=pair_config.get('priority', 2),
                from_keywords=node_keywords.get(from_id, []),
                to_keywords=node_keywords.get(to_id, [])
            )
            pairs.append(pair)

        logger.info(f"Built {len(pairs)} valid node pairs, skipped {len(skipped)}")
        return pairs

    def build_search_query(self, pair: NodePair) -> List[str]:
        """
        Build search queries for a node pair using keywords.

        Returns:
            List of search query strings
        """
        search_config = self.config.get('search_config', {})
        templates = search_config.get('search_templates', [
            "{from_keywords} AND {to_keywords} AND (systematic review OR meta-analysis)"
        ])

        # Build keyword strings
        from_terms = [pair.from_node_name] + pair.from_keywords
        to_terms = [pair.to_node_name] + pair.to_keywords

        # Use first few keywords for query
        from_query = " OR ".join(f'"{t}"' for t in from_terms[:3])
        to_query = " OR ".join(f'"{t}"' for t in to_terms[:3])

        queries = []
        for template in templates:
            query = template.format(
                from_keywords=f"({from_query})",
                to_keywords=f"({to_query})",
                from_node_name=pair.from_node_name,
                to_node_name=pair.to_node_name
            )
            queries.append(query)

        return queries

    def search_papers_for_pair(
        self,
        pair: NodePair,
        max_papers: int = 30
    ) -> NodePairEvidence:
        """
        Search for papers relevant to a node pair.

        Args:
            pair: NodePair to search for
            max_papers: Maximum papers to retrieve

        Returns:
            NodePairEvidence with papers found
        """
        if not self.pubmed_email:
            raise ValueError("PUBMED_EMAIL required for literature search")

        queries = self.build_search_query(pair)
        evidence = NodePairEvidence(
            node_pair=pair,
            search_queries_used=queries
        )

        # Initialize aggregator
        aggregator = LiteratureSearchAggregator(
            pubmed_email=self.pubmed_email,
            semantic_scholar_key=self.ss_key
        )

        all_papers = []
        seen_titles = set()

        for query in queries:
            try:
                papers = aggregator.search(query, limit_per_source=max_papers // 2)
                for p in papers:
                    # Deduplicate by title
                    title_lower = (p.title or '').lower()[:100]
                    if title_lower and title_lower not in seen_titles:
                        seen_titles.add(title_lower)
                        all_papers.append(p)
            except Exception as e:
                logger.warning(f"Search error for {pair.from_node_id}->{pair.to_node_id}: {e}")

        # Convert to PaperInput
        for i, paper in enumerate(all_papers[:max_papers]):
            pi = PaperInput(
                abstract=getattr(paper, 'abstract', '') or '',
                title=getattr(paper, 'title', '') or 'Unknown',
                citation_context={
                    'title': getattr(paper, 'title', ''),
                    'year': getattr(paper, 'year', None),
                    'doi': getattr(paper, 'doi', None),
                    'authors': getattr(paper, 'authors', []),
                    'journal': getattr(paper, 'journal', None)
                },
                custom_id=f"{pair.from_node_id}_{pair.to_node_id}_{i}"
            )
            if pi.abstract:  # Only include papers with abstracts
                evidence.papers.append(pi)

        logger.info(f"Found {len(evidence.papers)} papers for {pair.from_node_id} -> {pair.to_node_id}")
        return evidence

    def _create_consolidation_prompt(
        self,
        evidence: NodePairEvidence,
        existing_node_ids: List[str]
    ) -> str:
        """
        Create prompt for consolidated mechanism extraction.

        CRITICAL: This prompt explicitly:
        1. Uses ONLY existing node IDs
        2. Returns null if insufficient evidence
        3. Consolidates multiple papers into ONE mechanism
        """
        pair = evidence.node_pair
        n_papers = len(evidence.papers)

        # Format papers section
        papers_text = []
        for i, paper in enumerate(evidence.papers[:20], 1):
            citation = paper.citation_context
            papers_text.append(f"""
### Paper {i}: {paper.title}
**Year**: {citation.get('year', 'N/A')}
**DOI**: {citation.get('doi', 'N/A')}

**Abstract**:
{paper.abstract[:2000]}
""")

        papers_section = "\n".join(papers_text)

        prompt = f"""You are an expert in public health causal mechanisms. Your task is to determine if sufficient evidence exists for a causal relationship between two nodes, and if so, extract a consolidated mechanism.

## TARGET NODE PAIR
- **FROM NODE**: {pair.from_node_name} (ID: {pair.from_node_id})
- **TO NODE**: {pair.to_node_name} (ID: {pair.to_node_id})
- **Expected Direction**: {pair.expected_direction} (positive = A↑→B↑, negative = A↑→B↓)
- **Category**: {pair.category}

---

## CRITICAL INSTRUCTIONS

### 1. DO NOT FORCE MECHANISMS
If the evidence is insufficient, unclear, or the papers don't support a causal relationship between THESE SPECIFIC NODES, you MUST return:
```json
{{"mechanism": null, "reason": "Insufficient evidence for causal relationship"}}
```

### 2. USE ONLY THESE EXACT NODE IDs
You MUST use exactly these node IDs:
- from_node_id: "{pair.from_node_id}"
- to_node_id: "{pair.to_node_id}"

DO NOT create new node IDs. DO NOT modify the IDs. Use them EXACTLY as shown.

### 3. MINIMUM CITATION REQUIREMENT
A valid mechanism requires at least 3 supporting citations. If fewer than 3 papers provide relevant evidence, return null.

### 4. EVIDENCE ASSESSMENT
Before extracting, assess:
- Do the papers actually study the relationship between {pair.from_node_name} and {pair.to_node_name}?
- Is there consistent evidence of a causal (not just correlational) relationship?
- Are at least 3 papers providing relevant evidence?

---

## PAPERS TO ANALYZE ({n_papers} total)

{papers_section}

---

## OUTPUT FORMAT

If INSUFFICIENT EVIDENCE (return this if papers don't support the specific relationship):
```json
{{
  "mechanism": null,
  "reason": "Specific reason why evidence is insufficient"
}}
```

If SUFFICIENT EVIDENCE exists, return:
```json
{{
  "mechanism": {{
    "from_node_id": "{pair.from_node_id}",
    "from_node_name": "{pair.from_node_name}",
    "to_node_id": "{pair.to_node_id}",
    "to_node_name": "{pair.to_node_name}",
    "direction": "{pair.expected_direction}",
    "category": "{pair.category}",
    "mechanism_pathway": [
      "Step 1: How the upstream factor initiates the pathway",
      "Step 2: Intermediate mechanisms",
      "Step 3: How this leads to the downstream outcome"
    ],
    "evidence_quality": "A|B|C",
    "n_studies": <total studies supporting this>,
    "primary_citation": "Chicago-style citation of best paper",
    "supporting_citations": ["Citation 2", "Citation 3", "..."],
    "effect_size_value": <number or null>,
    "effect_size_type": "odds_ratio|relative_risk|hazard_ratio|beta|null",
    "confidence_interval_lower": <number or null>,
    "confidence_interval_upper": <number or null>,
    "p_value": <number or null>,
    "sample_size": <total sample size>,
    "description": "Synthesized description of the mechanism",
    "structural_competency_notes": "How structural factors influence this pathway"
  }},
  "reason": null
}}
```

### QUALITY RATING RULES:
- **A**: n_studies ≥ 5 (meta-analyses or multiple high-quality studies)
- **B**: n_studies = 3-4 (multiple studies with consistent findings)
- **C**: n_studies = 1-2 (limited evidence - should not be extracted)

IMPORTANT: Do NOT return quality C mechanisms. If you would rate it C, return null instead.

Return ONLY valid JSON. No additional text.
"""
        return prompt

    def run_batch_extraction(
        self,
        evidence_list: List[NodePairEvidence],
        min_papers: int = 3,
        poll_interval: int = 60,
        max_wait: int = 14400
    ) -> List[MechanismResult]:
        """
        Run batch extraction for all node pairs with evidence.

        Args:
            evidence_list: List of NodePairEvidence
            min_papers: Minimum papers required to attempt extraction
            poll_interval: Polling interval in seconds
            max_wait: Maximum wait time in seconds

        Returns:
            List of MechanismResult objects
        """
        # Ensure API client is initialized
        self._ensure_client()

        # Get existing node IDs
        existing_nodes = list(self.node_metadata.keys())

        # Filter evidence with sufficient papers
        valid_evidence = [e for e in evidence_list if len(e.papers) >= min_papers]
        insufficient = [e for e in evidence_list if len(e.papers) < min_papers]

        logger.info(f"Processing {len(valid_evidence)} pairs with sufficient papers")
        logger.info(f"Skipping {len(insufficient)} pairs with insufficient papers")

        # Create results for insufficient evidence
        results = []
        for e in insufficient:
            results.append(MechanismResult(
                node_pair=e.node_pair,
                mechanism=None,
                evidence_found=False,
                n_papers=len(e.papers),
                insufficient_evidence=True
            ))

        if not valid_evidence:
            return results

        # Prepare batch requests
        requests = []
        evidence_lookup = {}

        for i, evidence in enumerate(valid_evidence):
            pair = evidence.node_pair
            custom_id = f"np_{i}_{pair.from_node_id}_{pair.to_node_id}"
            custom_id = re.sub(r'[^a-zA-Z0-9_-]', '_', custom_id)[:64]

            prompt = self._create_consolidation_prompt(evidence, existing_nodes)

            request = Request(
                custom_id=custom_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
            )
            requests.append(request)
            evidence_lookup[custom_id] = evidence

        # Submit batch
        logger.info(f"Submitting batch with {len(requests)} requests")
        batch = self.client.messages.batches.create(requests=requests)
        logger.info(f"Batch ID: {batch.id}")

        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait:
            batch = self.client.messages.batches.retrieve(batch.id)

            if batch.processing_status == "ended":
                logger.info(f"Batch completed: {batch.request_counts.succeeded} succeeded")
                break

            elapsed = int(time.time() - start_time)
            if elapsed % 300 == 0:
                logger.info(
                    f"Progress: {batch.request_counts.succeeded} succeeded, "
                    f"{batch.request_counts.processing} processing ({elapsed}s)"
                )

            time.sleep(poll_interval)
        else:
            raise TimeoutError(f"Batch timed out after {max_wait}s")

        # Process results
        for result in self.client.messages.batches.results(batch.id):
            custom_id = result.custom_id
            evidence = evidence_lookup.get(custom_id)

            if not evidence:
                continue

            mech_result = MechanismResult(
                node_pair=evidence.node_pair,
                n_papers=len(evidence.papers)
            )

            if result.result.type != "succeeded":
                mech_result.error = f"Batch request failed: {result.result.type}"
                results.append(mech_result)
                continue

            try:
                response_text = result.result.message.content[0].text

                # Parse JSON
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()

                data = json.loads(response_text)

                if data.get('mechanism') is None:
                    # LLM determined insufficient evidence
                    mech_result.mechanism = None
                    mech_result.evidence_found = False
                    mech_result.insufficient_evidence = True
                    mech_result.error = data.get('reason', 'Insufficient evidence')
                else:
                    # Valid mechanism extracted
                    mech_result.mechanism = data['mechanism']
                    mech_result.evidence_found = True

            except Exception as e:
                mech_result.error = f"Parse error: {e}"
                logger.warning(f"Error parsing result for {custom_id}: {e}")

            results.append(mech_result)

        return results

    def save_mechanisms(
        self,
        results: List[MechanismResult],
        output_dir: str = "mechanism-bank/mechanisms"
    ) -> Dict[str, Any]:
        """
        Save extracted mechanisms to YAML files.

        Args:
            results: List of MechanismResult objects
            output_dir: Output directory

        Returns:
            Summary statistics
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved = 0
        skipped_insufficient = 0
        skipped_error = 0

        for result in results:
            if not result.evidence_found or not result.mechanism:
                if result.insufficient_evidence:
                    skipped_insufficient += 1
                else:
                    skipped_error += 1
                continue

            mech = result.mechanism
            pair = result.node_pair

            # Determine category directory
            category = mech.get('category', pair.category)
            category_dir = output_path / category
            category_dir.mkdir(exist_ok=True)

            # Build YAML structure
            mech_id = f"{mech['from_node_id']}_to_{mech['to_node_id']}"

            yaml_data = {
                "id": mech_id,
                "name": f"{mech['from_node_name']} -> {mech['to_node_name']}",
                "from_node": {
                    "node_id": mech['from_node_id'],
                    "node_name": mech['from_node_name']
                },
                "to_node": {
                    "node_id": mech['to_node_id'],
                    "node_name": mech['to_node_name']
                },
                "direction": mech.get('direction', 'positive'),
                "category": category,
                "mechanism_pathway": mech.get('mechanism_pathway', []),
                "evidence": {
                    "quality_rating": mech.get('evidence_quality', 'B'),
                    "n_studies": mech.get('n_studies', result.n_papers),
                    "primary_citation": mech.get('primary_citation', ''),
                    "supporting_citations": mech.get('supporting_citations', [])
                },
                "description": mech.get('description', ''),
                "structural_competency_notes": mech.get('structural_competency_notes', ''),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "extraction_method": "node_pair_discovery_v4"
            }

            # Add quantitative effects if present
            if mech.get('effect_size_value') is not None:
                yaml_data["quantitative_effects"] = {
                    "effect_size": {
                        "value": mech['effect_size_value'],
                        "type": mech.get('effect_size_type'),
                        "ci_lower": mech.get('confidence_interval_lower'),
                        "ci_upper": mech.get('confidence_interval_upper')
                    },
                    "p_value": mech.get('p_value'),
                    "sample_size": mech.get('sample_size')
                }

            # Save YAML
            filename = f"{mech_id}.yaml"
            with open(category_dir / filename, 'w') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            saved += 1

        summary = {
            "saved": saved,
            "skipped_insufficient_evidence": skipped_insufficient,
            "skipped_error": skipped_error,
            "total_processed": len(results)
        }

        logger.info(f"Saved {saved} mechanisms to {output_dir}")
        logger.info(f"Skipped {skipped_insufficient} (insufficient evidence), {skipped_error} (errors)")

        return summary

    def discover_mechanisms(
        self,
        config_path: str,
        output_dir: str = "mechanism-bank/mechanisms",
        search_papers: bool = True,
        papers_cache: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Run full node-pair discovery pipeline.

        Args:
            config_path: Path to node pairs config
            output_dir: Output directory for mechanisms
            search_papers: Whether to search for papers
            papers_cache: Path to cached papers JSON
            dry_run: If True, don't submit batch

        Returns:
            Discovery report
        """
        start_time = datetime.now()

        # Load config and nodes
        self.load_config(config_path)
        self.load_node_metadata(self.config.get('node_source', 'nodes/by_scale'))

        # Build node pairs
        pairs = self.build_node_pairs()
        logger.info(f"Built {len(pairs)} node pairs to process")

        # Search for evidence
        evidence_list = []

        if papers_cache and Path(papers_cache).exists():
            logger.info(f"Loading cached papers from {papers_cache}")
            # Load from cache - implement if needed
            pass
        elif search_papers:
            search_config = self.config.get('search_config', {})
            papers_per_pair = search_config.get('papers_per_pair', 30)

            for pair in pairs:
                evidence = self.search_papers_for_pair(pair, max_papers=papers_per_pair)
                evidence_list.append(evidence)
                time.sleep(1)  # Rate limiting

        # Report on evidence found
        total_papers = sum(len(e.papers) for e in evidence_list)
        pairs_with_evidence = sum(1 for e in evidence_list if len(e.papers) >= 3)

        logger.info(f"Found {total_papers} total papers across {len(pairs)} pairs")
        logger.info(f"Pairs with sufficient evidence (≥3 papers): {pairs_with_evidence}")

        if dry_run:
            return {
                "dry_run": True,
                "pairs_total": len(pairs),
                "pairs_with_evidence": pairs_with_evidence,
                "total_papers": total_papers
            }

        # Run batch extraction
        llm_config = self.config.get('llm_config', {})
        min_citations = llm_config.get('min_citations_per_mechanism', 3)

        results = self.run_batch_extraction(evidence_list, min_papers=min_citations)

        # Save mechanisms
        save_summary = self.save_mechanisms(results, output_dir)

        # Generate report
        processing_time = (datetime.now() - start_time).total_seconds()

        report = {
            "config_name": self.config.get('name', 'unnamed'),
            "timestamp": datetime.now().isoformat(),
            "processing_time_seconds": processing_time,
            "pairs_configured": len(pairs),
            "pairs_with_evidence": pairs_with_evidence,
            "total_papers_found": total_papers,
            "mechanisms_extracted": save_summary['saved'],
            "insufficient_evidence": save_summary['skipped_insufficient_evidence'],
            "errors": save_summary['skipped_error'],
            "extraction_method": "node_pair_discovery_v4"
        }

        # Save report
        report_path = Path(self.config.get('output_config', {}).get('report_path', 'backend/reports'))
        report_path.mkdir(parents=True, exist_ok=True)
        report_file = report_path / f"node_pair_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report saved to {report_file}")

        return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Node-Pair Driven Discovery Pipeline V4")
    parser.add_argument("--config", required=True, help="Path to node pairs config JSON")
    parser.add_argument("--output", default="mechanism-bank/mechanisms", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Don't submit batch, just show stats")
    parser.add_argument("--no-search", action="store_true", help="Skip paper search, use cache")
    parser.add_argument("--cache", help="Path to cached papers JSON")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    discovery = NodePairDiscovery()
    report = discovery.discover_mechanisms(
        config_path=args.config,
        output_dir=args.output,
        search_papers=not args.no_search,
        papers_cache=args.cache,
        dry_run=args.dry_run
    )

    print("\n" + "=" * 60)
    print("NODE-PAIR DISCOVERY REPORT")
    print("=" * 60)
    for key, value in report.items():
        print(f"  {key}: {value}")
