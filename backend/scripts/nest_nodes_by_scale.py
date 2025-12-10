#!/usr/bin/env python3
"""
Node Hierarchy Nesting Script

Uses LLM to identify taxonomic/definitional containment relationships
between nodes WITHIN each scale (not cross-scale).

This is NOT about causality (that's mechanisms). This is about taxonomy:
- Does node A definitionally contain node B?
- Like biological taxonomy: genus contains species
- Example: alcohol_use_disorder contains binge_drinking (both Scale 5)

Usage:
    # Dry run - generate relationships without applying (starts with Scale 7)
    python nest_nodes_by_scale.py --dry-run --scale 7

    # Process all scales
    python nest_nodes_by_scale.py --dry-run --all

    # Write hierarchy to YAML files (from pre-computed results)
    python nest_nodes_by_scale.py --scale 7 --input outputs/nesting_results/scale_7.json --write-yaml

    # Apply relationships to database after review
    python nest_nodes_by_scale.py --apply --scale 7 --input outputs/nesting_results/scale_7.json

    # Full pipeline: discover, write to YAML, and apply to DB
    python nest_nodes_by_scale.py --scale 5 --write-yaml --apply
"""

import os
import sys
import json
import yaml
import logging
import argparse
import time
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# Setup paths
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent

# Load environment
from dotenv import load_dotenv
load_dotenv(BACKEND_DIR / '.env')

import anthropic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Add parent directory to path for imports
sys.path.insert(0, str(BACKEND_DIR))

from models.database import Base
from models.mechanism import Node, node_hierarchy
from utils.hierarchy import (
    add_parent_child_relationship,
    update_node_hierarchy_fields,
    validate_hierarchy_integrity
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
NODES_DIR = BASE_DIR / 'nodes' / 'by_scale'
OUTPUT_DIR = BASE_DIR / 'backend' / 'scripts' / 'outputs' / 'nesting_results'

# Scale directory names
SCALE_DIRS = {
    1: 'scale_1_structural_determinants',
    2: 'scale_2_built_environment',
    3: 'scale_3_institutional',
    4: 'scale_4_individual_household',
    5: 'scale_5_behaviors_psychosocial',
    6: 'scale_6_intermediate_pathways',
    7: 'scale_7_crisis_endpoints'
}

SCALE_NAMES = {
    1: 'Structural Determinants (Policy)',
    2: 'Built Environment',
    3: 'Institutional Infrastructure',
    4: 'Individual/Household',
    5: 'Behaviors/Psychosocial',
    6: 'Intermediate Pathways',
    7: 'Crisis Endpoints'
}


@dataclass
class NodeInfo:
    """Lightweight node info for LLM processing."""
    id: str
    name: str
    description: str
    domain: str
    category: str


@dataclass
class NestingRelationship:
    """A parent-child nesting relationship."""
    parent_id: str
    parent_name: str
    child_id: str
    child_name: str
    confidence: str  # high, medium, low
    reasoning: str


@dataclass
class ScaleNestingResult:
    """Results of nesting analysis for a scale."""
    scale: int
    scale_name: str
    total_nodes: int
    relationships_found: int
    domain_roots_identified: int
    relationships: List[NestingRelationship] = field(default_factory=list)
    orphan_nodes: List[str] = field(default_factory=list)  # Nodes with no parent
    llm_metadata: Dict = field(default_factory=dict)


class NodeNestingPipeline:
    """Pipeline to discover and apply node hierarchy relationships."""

    # LLM settings
    MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 4096

    # Chunk size for large scales (process in batches by domain)
    MAX_NODES_PER_CHUNK = 80

    def __init__(
        self,
        database_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """Initialize pipeline."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Database setup
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite:///./healthsystems.db"
        )
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def load_nodes_for_scale(self, scale: int) -> List[NodeInfo]:
        """Load all nodes from YAML files for a given scale."""
        scale_dir = NODES_DIR / SCALE_DIRS[scale]

        if not scale_dir.exists():
            logger.warning(f"Scale directory not found: {scale_dir}")
            return []

        nodes = []
        yaml_files = list(scale_dir.glob("*.yaml")) + list(scale_dir.glob("*.yml"))

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if not data or 'id' not in data:
                    continue

                nodes.append(NodeInfo(
                    id=data.get('id', ''),
                    name=data.get('name', data.get('id', '').replace('_', ' ').title()),
                    description=data.get('description', ''),
                    domain=data.get('domain', 'Unknown'),
                    category=data.get('category', 'unknown')
                ))
            except Exception as e:
                logger.warning(f"Error loading {yaml_file}: {e}")

        logger.info(f"Loaded {len(nodes)} nodes for Scale {scale}")
        return nodes

    def chunk_nodes_by_domain(self, nodes: List[NodeInfo]) -> Dict[str, List[NodeInfo]]:
        """Group nodes by domain for chunked processing."""
        by_domain: Dict[str, List[NodeInfo]] = {}

        for node in nodes:
            domain = node.domain.split(',')[0].strip()  # Use first domain if multiple
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(node)

        return by_domain

    def build_nesting_prompt(self, nodes: List[NodeInfo], scale: int) -> str:
        """Build the LLM prompt for nesting analysis."""
        scale_name = SCALE_NAMES[scale]

        # Format nodes for prompt
        nodes_text = "\n".join([
            f"- ID: {n.id}\n  Name: {n.name}\n  Domain: {n.domain}\n  Description: {n.description[:200] if n.description else 'No description'}..."
            for n in nodes
        ])

        prompt = f"""You are analyzing health systems nodes to identify TAXONOMIC/DEFINITIONAL containment relationships.

## Task
Identify which nodes at Scale {scale} ({scale_name}) DEFINITIONALLY CONTAIN other nodes - like biological taxonomy where genus contains species.

## Critical Rules
1. A CHILD must ENTIRELY fit within the PARENT's definition (taxonomic containment)
2. This is NOT about causality (that's handled by mechanisms)
3. ALL nodes are at the SAME scale ({scale}) - we're finding DEPTH within this scale
4. A node can have MULTIPLE parents (DAG structure allowed)
5. Only propose relationships with HIGH confidence
6. Some nodes may be "orphans" with no parent - that's OK

## Examples of Good Relationships
- "alcohol_use_disorder" contains "binge_drinking" (binge drinking is a type/subset of AUD)
- "cancer_mortality" contains "liver_cancer_mortality" (liver cancer is a specific cancer)
- "chronic_disease" contains "diabetes" (diabetes is a type of chronic disease)

## Examples of BAD Relationships (Don't Do This)
- "stress" contains "alcohol_use" (stress may CAUSE alcohol use, but doesn't contain it)
- "income" contains "healthcare_access" (these are causally related, not taxonomically)

## Nodes to Analyze (Scale {scale}: {scale_name})
{nodes_text}

## Response Format
Return ONLY valid JSON (no markdown, no explanation outside JSON):
{{
  "relationships": [
    {{
      "parent_id": "parent_node_id",
      "child_id": "child_node_id",
      "confidence": "high",
      "reasoning": "Brief explanation of why child fits within parent's definition"
    }}
  ],
  "domain_roots": ["node_id1", "node_id2"],
  "notes": "Any observations about the hierarchy structure"
}}

Only include "high" confidence relationships. If uncertain, omit the relationship."""

        return prompt

    def call_llm(self, prompt: str) -> Optional[Dict]:
        """Call Claude API and parse JSON response."""
        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=self.MAX_TOKENS,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response.content[0].text.strip()

            # Handle markdown-wrapped JSON
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                json_lines = []
                in_json = False
                for line in lines:
                    if line.startswith("```json"):
                        in_json = True
                        continue
                    elif line.startswith("```"):
                        in_json = False
                        continue
                    if in_json:
                        json_lines.append(line)
                response_text = '\n'.join(json_lines)

            return json.loads(response_text)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Response was: {response_text[:500]}...")
            return None
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return None

    def discover_nesting_for_scale(self, scale: int) -> ScaleNestingResult:
        """Discover all nesting relationships for a scale using LLM."""
        nodes = self.load_nodes_for_scale(scale)

        result = ScaleNestingResult(
            scale=scale,
            scale_name=SCALE_NAMES[scale],
            total_nodes=len(nodes),
            relationships_found=0,
            domain_roots_identified=0,
            llm_metadata={
                "model": self.MODEL,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

        if not nodes:
            logger.warning(f"No nodes found for Scale {scale}")
            return result

        # For large scales, chunk by domain
        all_relationships = []
        all_domain_roots: Set[str] = set()

        if len(nodes) > self.MAX_NODES_PER_CHUNK:
            logger.info(f"Scale {scale} has {len(nodes)} nodes, processing by domain chunks")
            nodes_by_domain = self.chunk_nodes_by_domain(nodes)

            for domain, domain_nodes in nodes_by_domain.items():
                logger.info(f"Processing domain '{domain}' with {len(domain_nodes)} nodes...")

                # Further chunk if domain is too large
                chunks = [domain_nodes[i:i+self.MAX_NODES_PER_CHUNK]
                         for i in range(0, len(domain_nodes), self.MAX_NODES_PER_CHUNK)]

                for chunk_idx, chunk in enumerate(chunks):
                    if len(chunks) > 1:
                        logger.info(f"  Chunk {chunk_idx+1}/{len(chunks)}")

                    prompt = self.build_nesting_prompt(chunk, scale)
                    llm_result = self.call_llm(prompt)

                    if llm_result:
                        all_relationships.extend(llm_result.get("relationships", []))
                        all_domain_roots.update(llm_result.get("domain_roots", []))

                    # Rate limiting
                    time.sleep(1)
        else:
            # Process all at once
            prompt = self.build_nesting_prompt(nodes, scale)
            llm_result = self.call_llm(prompt)

            if llm_result:
                all_relationships = llm_result.get("relationships", [])
                all_domain_roots = set(llm_result.get("domain_roots", []))

        # Build node lookup for names
        node_lookup = {n.id: n.name for n in nodes}

        # Convert to NestingRelationship objects
        for rel in all_relationships:
            parent_id = rel.get("parent_id", "")
            child_id = rel.get("child_id", "")

            # Validate both nodes exist
            if parent_id not in node_lookup or child_id not in node_lookup:
                logger.warning(f"Skipping invalid relationship: {parent_id} -> {child_id}")
                continue

            result.relationships.append(NestingRelationship(
                parent_id=parent_id,
                parent_name=node_lookup.get(parent_id, parent_id),
                child_id=child_id,
                child_name=node_lookup.get(child_id, child_id),
                confidence=rel.get("confidence", "high"),
                reasoning=rel.get("reasoning", "")
            ))

        # Find orphan nodes (no parents assigned)
        child_ids = {r.child_id for r in result.relationships}
        result.orphan_nodes = [n.id for n in nodes if n.id not in child_ids]

        result.relationships_found = len(result.relationships)
        result.domain_roots_identified = len(all_domain_roots)

        logger.info(f"Scale {scale}: Found {result.relationships_found} relationships, "
                   f"{len(result.orphan_nodes)} orphan nodes")

        return result

    def save_results(self, result: ScaleNestingResult) -> Path:
        """Save nesting results to JSON file."""
        output_path = OUTPUT_DIR / f"scale_{result.scale}.json"

        # Convert to serializable dict
        output_data = {
            "scale": result.scale,
            "scale_name": result.scale_name,
            "total_nodes": result.total_nodes,
            "relationships_found": result.relationships_found,
            "domain_roots_identified": result.domain_roots_identified,
            "orphan_nodes_count": len(result.orphan_nodes),
            "orphan_nodes": result.orphan_nodes[:20],  # First 20 for review
            "relationships": [asdict(r) for r in result.relationships],
            "llm_metadata": result.llm_metadata
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)

        logger.info(f"Saved results to {output_path}")
        return output_path

    def load_results(self, input_path: Path) -> ScaleNestingResult:
        """Load previously saved nesting results."""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        relationships = [
            NestingRelationship(**r) for r in data.get("relationships", [])
        ]

        return ScaleNestingResult(
            scale=data["scale"],
            scale_name=data["scale_name"],
            total_nodes=data["total_nodes"],
            relationships_found=data["relationships_found"],
            domain_roots_identified=data.get("domain_roots_identified", 0),
            relationships=relationships,
            orphan_nodes=data.get("orphan_nodes", []),
            llm_metadata=data.get("llm_metadata", {})
        )

    def apply_relationships_to_db(self, result: ScaleNestingResult) -> Tuple[int, int]:
        """Apply nesting relationships to database."""
        session = self.SessionLocal()
        success_count = 0
        fail_count = 0

        try:
            for rel in result.relationships:
                if rel.confidence != "high":
                    logger.debug(f"Skipping non-high confidence: {rel.parent_id} -> {rel.child_id}")
                    continue

                success, msg = add_parent_child_relationship(
                    db=session,
                    parent_id=rel.parent_id,
                    child_id=rel.child_id,
                    node_model=Node,
                    node_hierarchy_table=node_hierarchy,
                    relationship_type="contains",
                    order_index=0
                )

                if success:
                    success_count += 1
                    logger.debug(f"Added: {rel.parent_id} -> {rel.child_id}")
                else:
                    fail_count += 1
                    logger.warning(f"Failed: {msg}")

            session.commit()
            logger.info(f"Applied {success_count} relationships, {fail_count} failed")

        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()

        return success_count, fail_count

    def validate_db_hierarchy(self) -> List[Tuple[str, str]]:
        """Run hierarchy validation on database."""
        session = self.SessionLocal()
        try:
            errors = validate_hierarchy_integrity(session, Node)
            if errors:
                logger.warning(f"Found {len(errors)} hierarchy integrity issues")
                for node_id, error_msg in errors[:10]:
                    logger.warning(f"  {node_id}: {error_msg}")
            else:
                logger.info("Hierarchy integrity check passed")
            return errors
        finally:
            session.close()

    # ========================================================================
    # YAML Writing Methods (for --write-yaml flag)
    # ========================================================================

    def find_yaml_path(self, node_id: str, scale: int) -> Optional[Path]:
        """Find the YAML file path for a given node ID."""
        scale_dir = NODES_DIR / SCALE_DIRS[scale]

        if not scale_dir.exists():
            return None

        # Search for YAML file containing this node
        for yaml_file in scale_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('id') == node_id:
                        return yaml_file
            except Exception:
                continue

        # Also check .yml extension
        for yaml_file in scale_dir.glob("*.yml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('id') == node_id:
                        return yaml_file
            except Exception:
                continue

        return None

    def compute_depths_from_relationships(
        self,
        relationships: List[NestingRelationship],
        all_node_ids: Set[str]
    ) -> Dict[str, int]:
        """
        Compute depths for all nodes using BFS from roots.

        Roots (depth=0) are nodes that have no parents.
        Depth = max(parent_depths) + 1
        """
        # Build parent lookup: child_id -> list of parent_ids
        child_to_parents: Dict[str, List[str]] = defaultdict(list)
        for rel in relationships:
            child_to_parents[rel.child_id].append(rel.parent_id)

        # Find roots (nodes with no parents)
        nodes_with_parents = set(child_to_parents.keys())
        roots = all_node_ids - nodes_with_parents

        # Initialize depths
        depths: Dict[str, int] = {}
        for root in roots:
            depths[root] = 0

        # BFS to compute depths
        # Process in waves: first all depth-0, then compute depth-1, etc.
        changed = True
        max_iterations = 20  # Safety limit

        iteration = 0
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for child_id, parent_ids in child_to_parents.items():
                if child_id in depths:
                    continue  # Already computed

                # Check if all parents have depths computed
                parent_depths = []
                all_parents_computed = True
                for pid in parent_ids:
                    if pid in depths:
                        parent_depths.append(depths[pid])
                    else:
                        all_parents_computed = False
                        break

                if all_parents_computed and parent_depths:
                    depths[child_id] = max(parent_depths) + 1
                    changed = True

        # Any remaining nodes without depth are orphans at depth 0
        for node_id in all_node_ids:
            if node_id not in depths:
                depths[node_id] = 0

        return depths

    def identify_grouping_nodes(
        self,
        relationships: List[NestingRelationship]
    ) -> Set[str]:
        """Identify which nodes are grouping/container nodes (have children)."""
        return {rel.parent_id for rel in relationships}

    def update_yaml_with_hierarchy(
        self,
        yaml_path: Path,
        parent_ids: List[str],
        depth: int,
        is_grouping_node: bool
    ) -> bool:
        """
        Update a YAML file with hierarchy information.

        Preserves existing content and adds/updates hierarchy section.
        """
        try:
            # Read existing content
            with open(yaml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                f.seek(0)
                data = yaml.safe_load(f)

            if not data:
                logger.warning(f"Empty YAML file: {yaml_path}")
                return False

            # Add/update hierarchy section
            data['hierarchy'] = {
                'parent_ids': parent_ids,
                'depth': depth,
                'is_grouping_node': is_grouping_node
            }

            # Write back with preserved formatting
            # Use safe_dump with default_flow_style=False for readable output
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    width=120
                )

            return True

        except Exception as e:
            logger.error(f"Failed to update {yaml_path}: {e}")
            return False

    def write_hierarchy_to_yaml(self, result: ScaleNestingResult) -> Tuple[int, int]:
        """
        Write hierarchy relationships back to YAML files.

        Returns (success_count, fail_count)
        """
        logger.info(f"Writing hierarchy to YAML files for Scale {result.scale}...")

        # Build child -> parents mapping
        child_to_parents: Dict[str, List[str]] = defaultdict(list)
        for rel in result.relationships:
            child_to_parents[rel.child_id].append(rel.parent_id)

        # Get all node IDs for this scale
        nodes = self.load_nodes_for_scale(result.scale)
        all_node_ids = {n.id for n in nodes}

        # Compute depths
        depths = self.compute_depths_from_relationships(result.relationships, all_node_ids)

        # Identify grouping nodes
        grouping_nodes = self.identify_grouping_nodes(result.relationships)

        # Update each node's YAML file
        success_count = 0
        fail_count = 0

        for node_id in all_node_ids:
            yaml_path = self.find_yaml_path(node_id, result.scale)

            if not yaml_path:
                logger.warning(f"Could not find YAML file for node: {node_id}")
                fail_count += 1
                continue

            parent_ids = child_to_parents.get(node_id, [])
            depth = depths.get(node_id, 0)
            is_grouping = node_id in grouping_nodes

            if self.update_yaml_with_hierarchy(yaml_path, parent_ids, depth, is_grouping):
                success_count += 1
                logger.debug(f"Updated {node_id}: depth={depth}, parents={parent_ids}")
            else:
                fail_count += 1

        logger.info(f"YAML updates: {success_count} succeeded, {fail_count} failed")
        return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description="Discover and apply node hierarchy relationships using LLM"
    )
    parser.add_argument(
        "--scale", type=int, choices=range(1, 8),
        help="Scale to process (1-7)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process all scales"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Only discover relationships, don't apply to database"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply relationships to database"
    )
    parser.add_argument(
        "--input", type=str,
        help="Input JSON file with pre-computed relationships (skip LLM)"
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Run hierarchy integrity validation"
    )
    parser.add_argument(
        "--write-yaml", action="store_true",
        help="Write hierarchy relationships back to YAML node files"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validation check
    if not args.scale and not args.all and not args.validate:
        parser.error("Must specify --scale N, --all, or --validate")

    try:
        pipeline = NodeNestingPipeline()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    # Validation only
    if args.validate:
        pipeline.validate_db_hierarchy()
        return

    # Determine scales to process
    scales = list(range(1, 8)) if args.all else [args.scale]

    for scale in scales:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing Scale {scale}: {SCALE_NAMES[scale]}")
        logger.info(f"{'='*60}")

        # Load pre-computed results or discover
        if args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                logger.error(f"Input file not found: {input_path}")
                continue
            result = pipeline.load_results(input_path)
        else:
            result = pipeline.discover_nesting_for_scale(scale)
            output_path = pipeline.save_results(result)
            logger.info(f"Results saved to: {output_path}")

        # Print summary
        print(f"\n--- Scale {scale} Summary ---")
        print(f"Total nodes: {result.total_nodes}")
        print(f"Relationships found: {result.relationships_found}")
        print(f"Orphan nodes: {len(result.orphan_nodes)}")

        if result.relationships:
            print(f"\nSample relationships:")
            for rel in result.relationships[:5]:
                print(f"  {rel.parent_name} -> {rel.child_name}")
                print(f"    Reason: {rel.reasoning[:80]}...")

        # Write to YAML files if requested
        if args.write_yaml:
            logger.info("Writing hierarchy to YAML files...")
            success, failed = pipeline.write_hierarchy_to_yaml(result)
            print(f"\nYAML updates: {success} succeeded, {failed} failed")

        # Apply to database if requested
        if args.apply and not args.dry_run:
            logger.info("Applying relationships to database...")
            success, failed = pipeline.apply_relationships_to_db(result)
            print(f"\nDatabase updates: {success} succeeded, {failed} failed")
        elif args.dry_run:
            print("\n[DRY RUN] Skipping database updates")

    logger.info("\nDone!")


if __name__ == "__main__":
    main()
