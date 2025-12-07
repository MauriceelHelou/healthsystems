"""
Mechanism Deduplication Pipeline

Implements Stage 3 of LLM Topology Discovery (Doc 09):
- Semantic clustering of extracted mechanisms
- LLM-based consolidation for duplicate detection
- Evidence merging and variant identification

Reduces ~250-350 candidate mechanisms to ~100-150 deduplicated mechanisms.
"""

import numpy as np
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import anthropic
import os
from pathlib import Path
import yaml
import json

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import DBSCAN
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")


@dataclass
class MechanismCluster:
    """Represents a cluster of potentially duplicate mechanisms."""
    cluster_id: int
    mechanisms: List[Dict]
    consolidated: Optional[Dict] = None
    decision: Optional[str] = None  # "SAME", "VARIANTS", or "SEPARATE"
    reasoning: Optional[str] = None


class MechanismDeduplicator:
    """
    Deduplicates mechanisms using semantic clustering + LLM consolidation.

    Pipeline:
    1. Embed mechanism descriptions using SentenceTransformer
    2. Cluster with DBSCAN (eps=0.15 for strict similarity)
    3. For each cluster with 2+ mechanisms:
       - LLM decides: SAME (merge) or VARIANTS (keep separate)
       - If SAME: consolidate evidence, merge studies
       - If VARIANTS: keep separate, document differences
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        dbscan_eps: float = 0.15,
        dbscan_min_samples: int = 2
    ):
        """
        Initialize deduplicator.

        Args:
            anthropic_api_key: API key for Claude (for LLM consolidation)
            embedding_model: SentenceTransformer model name
            dbscan_eps: DBSCAN epsilon (similarity threshold, 0.15 = strict)
            dbscan_min_samples: Minimum cluster size
        """
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            print(f"Loading embedding model: {embedding_model}")
            self.embedder = SentenceTransformer(embedding_model)
        else:
            raise ImportError("sentence-transformers required. Install: pip install sentence-transformers")

        self.dbscan_eps = dbscan_eps
        self.dbscan_min_samples = dbscan_min_samples

    def deduplicate(
        self,
        mechanisms: List[Dict],
        verbose: bool = True
    ) -> Tuple[List[Dict], Dict[str, any]]:
        """
        Deduplicate mechanisms using semantic clustering + LLM consolidation.

        Args:
            mechanisms: List of mechanism dictionaries (from YAML files or extraction)
            verbose: Print progress

        Returns:
            Tuple of (deduplicated_mechanisms, stats_dict)
        """
        if verbose:
            print(f"\n=== Starting Deduplication ===")
            print(f"Input mechanisms: {len(mechanisms)}")

        # Step 1: Embed mechanism descriptions
        if verbose:
            print("\nStep 1: Embedding mechanism descriptions...")

        embeddings = self._embed_mechanisms(mechanisms)

        # Step 2: Cluster with DBSCAN
        if verbose:
            print(f"\nStep 2: Clustering with DBSCAN (eps={self.dbscan_eps})...")

        clusters = self._cluster_mechanisms(embeddings, mechanisms)

        if verbose:
            print(f"  Found {len(clusters)} clusters")
            multi_mechanism_clusters = [c for c in clusters if len(c.mechanisms) > 1]
            print(f"  {len(multi_mechanism_clusters)} clusters with 2+ mechanisms (need LLM review)")

        # Step 3: LLM consolidation for multi-mechanism clusters
        if verbose:
            print("\nStep 3: LLM consolidation...")

        consolidated_mechanisms = []
        consolidation_stats = {
            'merged': 0,
            'kept_separate': 0,
            'variants_identified': 0,
            'total_input': len(mechanisms),
            'clusters_processed': 0
        }

        for cluster in clusters:
            if len(cluster.mechanisms) == 1:
                # Singleton - keep as-is
                consolidated_mechanisms.append(cluster.mechanisms[0])
            else:
                # Multi-mechanism cluster - use LLM to decide
                consolidation_stats['clusters_processed'] += 1

                decision = self._consolidate_cluster(cluster, verbose=verbose)

                if decision['action'] == 'MERGE':
                    consolidated_mechanisms.append(decision['consolidated'])
                    consolidation_stats['merged'] += len(cluster.mechanisms) - 1
                elif decision['action'] == 'VARIANTS':
                    # Keep separate but mark as variants
                    for mech in decision['mechanisms']:
                        mech['is_variant'] = True
                        mech['variant_group'] = cluster.cluster_id
                        consolidated_mechanisms.append(mech)
                    consolidation_stats['variants_identified'] += len(cluster.mechanisms)
                else:  # SEPARATE
                    consolidated_mechanisms.extend(cluster.mechanisms)
                    consolidation_stats['kept_separate'] += len(cluster.mechanisms)

        consolidation_stats['total_output'] = len(consolidated_mechanisms)
        consolidation_stats['reduction_pct'] = (
            100 * (1 - consolidation_stats['total_output'] / consolidation_stats['total_input'])
            if consolidation_stats['total_input'] > 0 else 0
        )

        if verbose:
            print(f"\n=== Deduplication Complete ===")
            print(f"Input: {consolidation_stats['total_input']} mechanisms")
            print(f"Output: {consolidation_stats['total_output']} mechanisms")
            print(f"Reduction: {consolidation_stats['reduction_pct']:.1f}%")
            print(f"  - Merged: {consolidation_stats['merged']} duplicates")
            print(f"  - Variants: {consolidation_stats['variants_identified']} mechanisms")
            print(f"  - Kept separate: {consolidation_stats['kept_separate']} mechanisms")

        return consolidated_mechanisms, consolidation_stats

    def _embed_mechanisms(self, mechanisms: List[Dict]) -> np.ndarray:
        """Embed mechanism descriptions using SentenceTransformer."""
        texts = []
        for mech in mechanisms:
            # Combine key fields for embedding
            text_parts = [
                f"From: {mech.get('from_node_id', '')}",
                f"To: {mech.get('to_node_id', '')}",
                f"Description: {mech.get('description', '')}",
                f"Category: {mech.get('category', '')}"
            ]
            texts.append(" | ".join(text_parts))

        embeddings = self.embedder.encode(texts, show_progress_bar=False)
        return embeddings

    def _cluster_mechanisms(
        self,
        embeddings: np.ndarray,
        mechanisms: List[Dict]
    ) -> List[MechanismCluster]:
        """Cluster mechanisms using DBSCAN."""
        clustering = DBSCAN(
            eps=self.dbscan_eps,
            min_samples=self.dbscan_min_samples,
            metric='cosine'
        ).fit(embeddings)

        # Group by cluster label
        cluster_map = defaultdict(list)
        for idx, label in enumerate(clustering.labels_):
            cluster_map[label].append(mechanisms[idx])

        # Convert to MechanismCluster objects
        clusters = []
        for cluster_id, mechs in cluster_map.items():
            clusters.append(MechanismCluster(
                cluster_id=cluster_id,
                mechanisms=mechs
            ))

        return clusters

    def _consolidate_cluster(
        self,
        cluster: MechanismCluster,
        verbose: bool = True
    ) -> Dict[str, any]:
        """
        Use LLM to decide if mechanisms in cluster should be merged.

        Returns:
            Dict with 'action' (MERGE/VARIANTS/SEPARATE) and relevant data
        """
        if verbose:
            print(f"\n  Reviewing cluster {cluster.cluster_id} ({len(cluster.mechanisms)} mechanisms)...")

        # Build prompt for LLM
        prompt = self._build_consolidation_prompt(cluster)

        try:
            response = self.client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=2000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            # Parse LLM decision
            decision = self._parse_llm_decision(response_text, cluster)

            if verbose:
                print(f"    Decision: {decision['action']}")
                if 'reasoning' in decision:
                    print(f"    Reasoning: {decision['reasoning'][:100]}...")

            return decision

        except Exception as e:
            print(f"Error in LLM consolidation: {e}")
            # Default: keep separate on error
            return {'action': 'SEPARATE', 'mechanisms': cluster.mechanisms}

    def _build_consolidation_prompt(self, cluster: MechanismCluster) -> str:
        """Build prompt for LLM to decide on cluster consolidation."""

        mechanisms_text = ""
        for i, mech in enumerate(cluster.mechanisms, 1):
            mechanisms_text += f"\n### Mechanism {i}\n"
            mechanisms_text += f"- **From**: {mech.get('from_node_id', 'N/A')}\n"
            mechanisms_text += f"- **To**: {mech.get('to_node_id', 'N/A')}\n"
            mechanisms_text += f"- **Category**: {mech.get('category', 'N/A')}\n"
            mechanisms_text += f"- **Description**: {mech.get('description', 'N/A')}\n"
            mechanisms_text += f"- **Evidence Quality**: {mech.get('evidence_quality', 'N/A')}\n"
            mechanisms_text += f"- **Studies**: {mech.get('n_studies', 0)}\n"

            # Add quantitative data if available
            if mech.get('effect_size'):
                mechanisms_text += f"- **Effect Size**: {mech['effect_size']} (CI: {mech.get('ci_lower', '?')}-{mech.get('ci_upper', '?')})\n"

        prompt = f"""You are reviewing a cluster of potentially duplicate mechanisms extracted from health literature.

Your task: Determine if these mechanisms are:
1. **SAME** - Describing the same causal pathway (should be merged)
2. **VARIANTS** - Same pathway but in different contexts/populations (keep separate, mark as variants)
3. **SEPARATE** - Actually different mechanisms (keep separate)

## Mechanisms to Review:
{mechanisms_text}

## Decision Criteria:

**MERGE (SAME) if**:
- Same from_node and to_node
- Same category
- Descriptions are semantically equivalent (minor wording differences OK)
- Evidence sources likely overlap
- Example: "Food insecurity → obesity" vs "Limited food access → increased BMI"

**VARIANTS if**:
- Same pathway but different populations (adults vs children)
- Same pathway but different geographic contexts (US vs low-income countries)
- Same pathway but different time periods (acute vs chronic)
- Example: "Poverty → depression in adults" vs "Poverty → depression in adolescents"

**SEPARATE if**:
- Different intermediate pathways (even if same endpoints)
- Different mechanisms of action
- Different moderating factors that fundamentally change the relationship
- Example: "Exercise → cardiovascular health via improved lipids" vs "Exercise → cardiovascular health via reduced inflammation"

## Output Format:

Provide your decision in this exact format:

```json
{{
  "decision": "MERGE" | "VARIANTS" | "SEPARATE",
  "reasoning": "Brief explanation (1-2 sentences)",
  "consolidated": {{
    "from_node_id": "...",
    "to_node_id": "...",
    "category": "...",
    "description": "...",
    "evidence_quality": "...",
    "n_studies": <sum of all studies>,
    "effect_size": <averaged or most robust>,
    "ci_lower": <if merging>,
    "ci_upper": <if merging>,
    "source_ids": ["mech_1", "mech_2", ...]
  }} // ONLY if decision is MERGE
}}
```

If VARIANTS or SEPARATE, omit the "consolidated" field.
"""

        return prompt

    def _parse_llm_decision(
        self,
        response_text: str,
        cluster: MechanismCluster
    ) -> Dict[str, any]:
        """Parse LLM response into structured decision."""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[json_start:json_end]
            parsed = json.loads(json_str)

            decision = parsed.get('decision', 'SEPARATE')
            reasoning = parsed.get('reasoning', '')

            if decision == 'MERGE':
                consolidated = parsed.get('consolidated', {})
                # Add metadata
                consolidated['deduplication_metadata'] = {
                    'cluster_id': cluster.cluster_id,
                    'merged_count': len(cluster.mechanisms),
                    'reasoning': reasoning
                }
                return {
                    'action': 'MERGE',
                    'consolidated': consolidated,
                    'reasoning': reasoning
                }
            elif decision == 'VARIANTS':
                return {
                    'action': 'VARIANTS',
                    'mechanisms': cluster.mechanisms,
                    'reasoning': reasoning
                }
            else:  # SEPARATE
                return {
                    'action': 'SEPARATE',
                    'mechanisms': cluster.mechanisms,
                    'reasoning': reasoning
                }

        except Exception as e:
            print(f"Error parsing LLM decision: {e}")
            # Default to keeping separate
            return {'action': 'SEPARATE', 'mechanisms': cluster.mechanisms}

    def deduplicate_from_files(
        self,
        mechanism_dir: Path,
        output_dir: Optional[Path] = None,
        verbose: bool = True
    ) -> Tuple[List[Dict], Dict[str, any]]:
        """
        Load mechanisms from YAML files, deduplicate, and save results.

        Args:
            mechanism_dir: Directory containing mechanism YAML files
            output_dir: Directory to save deduplicated mechanisms (default: same as input)
            verbose: Print progress

        Returns:
            Tuple of (deduplicated_mechanisms, stats_dict)
        """
        mechanism_dir = Path(mechanism_dir)
        output_dir = output_dir or mechanism_dir

        if verbose:
            print(f"Loading mechanisms from: {mechanism_dir}")

        # Load all YAML files
        mechanisms = []
        for yaml_file in mechanism_dir.rglob("*.yml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    mech = yaml.safe_load(f)
                    mech['_source_file'] = str(yaml_file.relative_to(mechanism_dir))
                    mechanisms.append(mech)
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")

        if verbose:
            print(f"Loaded {len(mechanisms)} mechanisms")

        # Deduplicate
        deduplicated, stats = self.deduplicate(mechanisms, verbose=verbose)

        # Save deduplicated mechanisms
        if output_dir != mechanism_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            if verbose:
                print(f"\nSaving deduplicated mechanisms to: {output_dir}")

            for mech in deduplicated:
                # Preserve category structure
                category = mech.get('category', 'uncategorized')
                category_dir = output_dir / category
                category_dir.mkdir(parents=True, exist_ok=True)

                # Generate filename
                from_node = mech.get('from_node_id', 'unknown').replace('/', '_')
                to_node = mech.get('to_node_id', 'unknown').replace('/', '_')
                filename = f"{from_node}_to_{to_node}.yml"

                output_path = category_dir / filename

                # Save YAML
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(mech, f, default_flow_style=False, allow_unicode=True)

        # Save stats
        stats_path = output_dir / "deduplication_stats.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        if verbose:
            print(f"\nStats saved to: {stats_path}")

        return deduplicated, stats


def test_deduplication():
    """Test deduplication with sample mechanisms."""
    print("=== Testing Mechanism Deduplication ===\n")

    # Sample mechanisms (simulating extraction output)
    sample_mechanisms = [
        {
            'from_node_id': 'food_insecurity',
            'to_node_id': 'obesity',
            'category': 'economic',
            'description': 'Food insecurity leads to obesity through reliance on calorie-dense, nutrient-poor foods',
            'evidence_quality': 'A',
            'n_studies': 15,
            'effect_size': 1.35,
            'ci_lower': 1.15,
            'ci_upper': 1.58
        },
        {
            'from_node_id': 'food_insecurity',
            'to_node_id': 'obesity',
            'category': 'economic',
            'description': 'Limited food access increases obesity risk due to consumption of cheap, high-calorie foods',
            'evidence_quality': 'A',
            'n_studies': 12,
            'effect_size': 1.42,
            'ci_lower': 1.20,
            'ci_upper': 1.67
        },
        {
            'from_node_id': 'food_insecurity',
            'to_node_id': 'obesity',
            'category': 'economic',
            'description': 'Food insecurity in children leads to obesity through metabolic adaptations',
            'evidence_quality': 'B',
            'n_studies': 8,
            'effect_size': 1.25,
            'ci_lower': 1.05,
            'ci_upper': 1.48
        },
        {
            'from_node_id': 'physical_activity',
            'to_node_id': 'obesity',
            'category': 'behavioral',
            'description': 'Increased physical activity reduces obesity through energy expenditure',
            'evidence_quality': 'A',
            'n_studies': 25,
            'effect_size': 0.75,
            'ci_lower': 0.65,
            'ci_upper': 0.87
        }
    ]

    # Initialize deduplicator
    deduplicator = MechanismDeduplicator()

    # Deduplicate
    deduplicated, stats = deduplicator.deduplicate(sample_mechanisms, verbose=True)

    print(f"\n=== Deduplicated Mechanisms ===\n")
    for i, mech in enumerate(deduplicated, 1):
        print(f"{i}. {mech['from_node_id']} → {mech['to_node_id']}")
        print(f"   Category: {mech['category']}")
        print(f"   Description: {mech['description'][:80]}...")
        if mech.get('is_variant'):
            print(f"   [VARIANT - Group {mech['variant_group']}]")
        if mech.get('deduplication_metadata'):
            print(f"   [MERGED - {mech['deduplication_metadata']['merged_count']} mechanisms]")
        print()


if __name__ == "__main__":
    test_deduplication()
