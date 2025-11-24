"""
Bidirectional Mechanism Detector and Creator

Analyzes existing unidirectional mechanisms and:
1. Detects potential feedback loops (A→B where B→A may also exist)
2. Searches literature for reverse direction evidence
3. Creates bidirectional mechanism pairs when evidence found

Based on 05_MECHANISM_BANK_STRUCTURE.md bidirectional encoding requirements.

Usage:
  python create_bidirectional_pairs.py --input-dir mechanism-bank/mechanisms/obesity/
  python create_bidirectional_pairs.py --mechanism mechanism.yml --output-dir mechanism-bank/mechanisms/
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import yaml
import anthropic
import os
from dataclasses import dataclass
import argparse

# Import literature search
import sys
sys.path.append(str(Path(__file__).parent.parent))
from pipelines.literature_search import LiteratureSearchAggregator
from pipelines.llm_mechanism_discovery import LLMMechanismDiscovery


@dataclass
class BidirectionalCandidate:
    """Candidate for bidirectional mechanism."""
    forward_mechanism: Dict
    reverse_direction_plausible: bool
    reverse_literature_found: bool
    reverse_mechanism: Optional[Dict] = None
    reasoning: str = ""


class BidirectionalMechanismDetector:
    """
    Detects and creates bidirectional mechanism pairs.

    Pipeline:
    1. Analyze forward mechanism (A→B)
    2. LLM assesses plausibility of reverse direction (B→A)
    3. If plausible, search literature for B→A evidence
    4. If evidence found, extract reverse mechanism
    5. Create bidirectional pair (both A→B and B→A as separate files)
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        pubmed_email: str = "healthsystems@example.com"
    ):
        """Initialize detector with API keys."""
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.literature_search = LiteratureSearchAggregator(pubmed_email=pubmed_email)
        self.llm_discovery = LLMMechanismDiscovery(anthropic_api_key=self.api_key)

    def detect_bidirectional(
        self,
        mechanism: Dict,
        search_literature: bool = True,
        verbose: bool = True
    ) -> BidirectionalCandidate:
        """
        Detect if mechanism should have bidirectional pair.

        Args:
            mechanism: Forward mechanism (A→B)
            search_literature: If True, search for reverse evidence
            verbose: Print progress

        Returns:
            BidirectionalCandidate with results
        """
        from_node = mechanism.get('from_node_id', 'unknown')
        to_node = mechanism.get('to_node_id', 'unknown')

        if verbose:
            print(f"\nAnalyzing: {from_node} → {to_node}")

        # Step 1: Assess plausibility of reverse direction
        plausibility = self._assess_reverse_plausibility(mechanism, verbose=verbose)

        if not plausibility['plausible']:
            if verbose:
                print(f"  Reverse direction not plausible: {plausibility['reasoning']}")

            return BidirectionalCandidate(
                forward_mechanism=mechanism,
                reverse_direction_plausible=False,
                reverse_literature_found=False,
                reasoning=plausibility['reasoning']
            )

        if verbose:
            print(f"  Reverse direction plausible: {plausibility['reasoning']}")

        # Step 2: Search literature for reverse direction (if requested)
        reverse_mechanism = None
        literature_found = False

        if search_literature:
            if verbose:
                print(f"  Searching literature for: {to_node} → {from_node}...")

            reverse_mechanism, literature_found = self._search_reverse_direction(
                mechanism,
                plausibility,
                verbose=verbose
            )

        return BidirectionalCandidate(
            forward_mechanism=mechanism,
            reverse_direction_plausible=True,
            reverse_literature_found=literature_found,
            reverse_mechanism=reverse_mechanism,
            reasoning=plausibility['reasoning']
        )

    def _assess_reverse_plausibility(
        self,
        mechanism: Dict,
        verbose: bool = True
    ) -> Dict[str, any]:
        """Use LLM to assess if reverse direction is plausible."""

        from_node = mechanism.get('from_node_id', 'unknown')
        to_node = mechanism.get('to_node_id', 'unknown')
        description = mechanism.get('description', 'No description')
        category = mechanism.get('category', 'unknown')

        prompt = f"""You are a health systems expert assessing potential feedback loops.

## Forward Mechanism (Established)

- **From**: {from_node}
- **To**: {to_node}
- **Category**: {category}
- **Description**: {description}

## Question

Is the **reverse direction** ({to_node} → {from_node}) plausible?

## Examples of Plausible Bidirectional Mechanisms

**Healthcare Continuity ↔ Healthcare Seeking**:
- Forward: Better continuity → more seeking (trust builds)
- Backward: More seeking → better continuity (repeated contact)

**ED Utilization ↔ Hospital Capacity**:
- Forward: High ED use → capacity expansion (hospital response)
- Backward: More capacity → more ED use (induced demand)

**Health Status ↔ Healthcare Access**:
- Forward: Better access → improved health (treatment)
- Backward: Better health → less need for access (self-limiting)

## Examples of Unidirectional Mechanisms (No Feedback)

**Income → Obesity**: Implausible reverse (obesity doesn't cause income changes at population level)

**Policy Strength → Eviction Rate**: Implausible reverse (eviction rates don't determine policy)

**Air Quality → Respiratory Health**: Implausible reverse (individual health doesn't affect air quality)

## Assessment Criteria

Consider:
1. **Temporal dynamics**: Can the outcome affect the cause over time?
2. **System response**: Does the downstream stock trigger upstream changes?
3. **Feedback loops**: Are there known feedback mechanisms?
4. **Biological/social plausibility**: Does the reverse direction make sense?
5. **Scale levels**: Outcomes (6-7) rarely feed back to structural factors (1-3)

## Output Format

```json
{{
  "plausible": true | false,
  "confidence": 0.85,
  "reasoning": "Brief explanation (2-3 sentences)",
  "suggested_reverse_description": "If plausible, describe the reverse mechanism",
  "expected_functional_form": "sigmoid | threshold | logarithmic | multiplicative_dampening | linear"
}}
```
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            # Parse JSON
            import json
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            parsed = json.loads(json_str)

            return parsed

        except Exception as e:
            print(f"Error in plausibility assessment: {e}")
            return {
                'plausible': False,
                'confidence': 0.0,
                'reasoning': f"Assessment failed: {e}"
            }

    def _search_reverse_direction(
        self,
        forward_mechanism: Dict,
        plausibility: Dict,
        verbose: bool = True
    ) -> Tuple[Optional[Dict], bool]:
        """Search literature for reverse direction evidence."""

        from_node = forward_mechanism.get('from_node_id', 'unknown')
        to_node = forward_mechanism.get('to_node_id', 'unknown')

        # Build search query for reverse direction
        query = f"{to_node} {from_node} causal feedback relationship"

        if verbose:
            print(f"    Query: {query}")

        # Search literature
        try:
            papers = self.literature_search.search(
                query=query,
                limit_per_source=5,
                year_range=(2010, 2024),
                sources=['semantic_scholar', 'pubmed']
            )

            if not papers:
                if verbose:
                    print(f"    No papers found")
                return None, False

            if verbose:
                print(f"    Found {len(papers)} papers, extracting mechanisms...")

            # Try to extract reverse mechanism from papers
            for paper in papers:
                if not paper.abstract or len(paper.abstract) < 100:
                    continue

                # Extract mechanisms
                focus_area = f"{to_node} to {from_node} (reverse direction feedback)"
                mechanisms = self.llm_discovery.extract_mechanisms_from_paper(
                    paper.abstract,
                    paper.title,
                    focus_area
                )

                # Check if any mechanism matches reverse direction
                for mech in mechanisms:
                    if (mech.from_node_id == to_node or to_node in mech.from_node_id) and \
                       (mech.to_node_id == from_node or from_node in mech.to_node_id):

                        if verbose:
                            print(f"    ✓ Found reverse mechanism in: {paper.title[:60]}...")

                        # Build reverse mechanism dict
                        reverse_mechanism = {
                            'from_node_id': to_node,
                            'to_node_id': from_node,
                            'direction': 'backward',  # Mark as feedback
                            'category': mech.category,
                            'description': mech.description,
                            'functional_form': plausibility.get('expected_functional_form', 'linear'),
                            'equation': '',  # Will be filled by functional form classifier
                            'parameters': {},
                            'evidence_quality': mech.evidence_quality,
                            'n_studies': mech.n_studies,
                            'effect_size': mech.effect_size,
                            'ci_lower': mech.ci_lower,
                            'ci_upper': mech.ci_upper,
                            'bidirectional_pair': {
                                'forward_from': from_node,
                                'forward_to': to_node,
                                'is_feedback_loop': True
                            },
                            'llm_metadata': {
                                'source_paper': paper.title,
                                'doi': paper.doi,
                                'extraction_confidence': 'medium'
                            }
                        }

                        return reverse_mechanism, True

            if verbose:
                print(f"    No reverse mechanism found in papers")

            return None, False

        except Exception as e:
            print(f"Error searching literature: {e}")
            return None, False

    def process_directory(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        search_literature: bool = True,
        verbose: bool = True
    ) -> Dict[str, BidirectionalCandidate]:
        """
        Process all mechanisms in directory to find bidirectional pairs.

        Args:
            input_dir: Directory with forward mechanisms
            output_dir: Directory to save reverse mechanisms (default: same as input)
            search_literature: If True, search for reverse evidence
            verbose: Print progress

        Returns:
            Dict mapping mechanism file to BidirectionalCandidate
        """
        input_dir = Path(input_dir)
        output_dir = output_dir or input_dir

        yaml_files = list(input_dir.rglob("*.yml"))

        if verbose:
            print(f"\n=== Processing {len(yaml_files)} mechanisms for bidirectionality ===")

        results = {}

        for yaml_file in yaml_files:
            try:
                # Load mechanism
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    mechanism = yaml.safe_load(f)

                # Skip if already marked as backward
                if mechanism.get('direction') == 'backward':
                    if verbose:
                        print(f"\nSkipping {yaml_file.name} (already marked as backward)")
                    continue

                # Detect bidirectional
                candidate = self.detect_bidirectional(
                    mechanism,
                    search_literature=search_literature,
                    verbose=verbose
                )

                results[str(yaml_file)] = candidate

                # Save reverse mechanism if found
                if candidate.reverse_mechanism:
                    self._save_reverse_mechanism(
                        candidate.reverse_mechanism,
                        output_dir,
                        verbose=verbose
                    )

            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")

        # Print summary
        if verbose:
            self._print_summary(results)

        return results

    def _save_reverse_mechanism(
        self,
        reverse_mechanism: Dict,
        output_dir: Path,
        verbose: bool = True
    ):
        """Save reverse mechanism to YAML file."""
        output_dir = Path(output_dir)

        # Get category
        category = reverse_mechanism.get('category', 'uncategorized')
        category_dir = output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        from_node = reverse_mechanism.get('from_node_id', 'unknown').replace('/', '_')
        to_node = reverse_mechanism.get('to_node_id', 'unknown').replace('/', '_')
        filename = f"{from_node}_to_{to_node}_backward.yml"

        output_path = category_dir / filename

        # Save
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(reverse_mechanism, f, default_flow_style=False, allow_unicode=True)

        if verbose:
            print(f"    Saved reverse mechanism: {output_path}")

    def _print_summary(self, results: Dict[str, BidirectionalCandidate]):
        """Print summary of bidirectional detection."""
        total = len(results)
        plausible = sum(1 for c in results.values() if c.reverse_direction_plausible)
        found = sum(1 for c in results.values() if c.reverse_literature_found)

        print(f"\n=== Bidirectional Detection Summary ===")
        print(f"Total mechanisms analyzed: {total}")
        print(f"Reverse direction plausible: {plausible} ({100*plausible/total:.1f}%)")
        print(f"Reverse mechanisms found in literature: {found} ({100*found/total:.1f}%)")

        if found > 0:
            print(f"\nBidirectional pairs created:")
            for filepath, candidate in results.items():
                if candidate.reverse_literature_found:
                    fwd = candidate.forward_mechanism
                    print(f"  - {fwd['from_node_id']} ↔ {fwd['to_node_id']}")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Detect and create bidirectional mechanism pairs"
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Directory containing forward mechanisms'
    )
    parser.add_argument(
        '--mechanism',
        type=str,
        help='Single mechanism file to analyze'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory to save reverse mechanisms (default: same as input)'
    )
    parser.add_argument(
        '--no-search',
        action='store_true',
        help='Only assess plausibility, do not search literature'
    )

    args = parser.parse_args()

    detector = BidirectionalMechanismDetector()

    if args.mechanism:
        # Process single mechanism
        filepath = Path(args.mechanism)
        with open(filepath, 'r', encoding='utf-8') as f:
            mechanism = yaml.safe_load(f)

        output_dir = Path(args.output_dir) if args.output_dir else filepath.parent

        candidate = detector.detect_bidirectional(
            mechanism,
            search_literature=not args.no_search,
            verbose=True
        )

        if candidate.reverse_mechanism:
            detector._save_reverse_mechanism(
                candidate.reverse_mechanism,
                output_dir,
                verbose=True
            )

    elif args.input_dir:
        # Process directory
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir) if args.output_dir else input_dir

        detector.process_directory(
            input_dir,
            output_dir,
            search_literature=not args.no_search,
            verbose=True
        )

    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
