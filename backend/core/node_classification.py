"""
Node classification and scale management.
Handles node reclassification, scale validation, and migration.
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class ClassificationResult:
    """Result of a classification operation."""
    node_id: str
    old_scale: int
    new_scale: int
    changed: bool
    reason: str


@dataclass
class ClassificationStats:
    """Statistics for classification operations."""
    total: int = 0
    changed: int = 0
    unchanged: int = 0
    errors: int = 0

    def record_change(self, changed: bool):
        self.total += 1
        if changed:
            self.changed += 1
        else:
            self.unchanged += 1

    def record_error(self):
        self.errors += 1

    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"CLASSIFICATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total nodes: {self.total}")
        print(f"Changed: {self.changed}")
        print(f"Unchanged: {self.unchanged}")
        print(f"Errors: {self.errors}")
        if self.total > 0:
            change_rate = self.changed / self.total * 100
            print(f"Change rate: {change_rate:.1f}%")


class NodeClassifier:
    """
    Unified node classification engine.
    Handles reclassification, scale migration, and validation.
    """

    # Scale definitions (1=structural, 7=crisis)
    SCALE_DEFINITIONS = {
        1: "Structural Determinants (policy, law)",
        2: "Built Environment & Infrastructure",
        3: "Institutional Infrastructure",
        4: "Individual/Household Conditions",
        5: "Individual Health Behaviors",
        6: "Biological/Physiological Processes",
        7: "Health Outcomes & Crisis Endpoints"
    }

    # Keywords for automatic classification
    SCALE_KEYWORDS = {
        1: ["policy", "law", "regulation", "legislation", "government"],
        2: ["housing", "neighborhood", "infrastructure", "environment", "zoning"],
        3: ["healthcare", "education", "institution", "system", "service"],
        4: ["income", "employment", "poverty", "SES", "household"],
        5: ["behavior", "lifestyle", "diet", "exercise", "smoking"],
        6: ["biological", "physiological", "metabolic", "genetic", "inflammation"],
        7: ["mortality", "disease", "disorder", "crisis", "death"]
    }

    def __init__(self, session: Session, dry_run: bool = False):
        self.session = session
        self.dry_run = dry_run
        self.stats = ClassificationStats()

    def validate_scale(self, scale: int) -> Tuple[bool, Optional[str]]:
        """
        Validate scale value.

        Args:
            scale: Scale value to validate

        Returns:
            (is_valid, error_message)
        """
        if not isinstance(scale, int):
            return False, f"Scale must be integer, got {type(scale)}"

        if scale < 1 or scale > 7:
            return False, f"Scale must be 1-7, got {scale}"

        return True, None

    def classify_node_by_keywords(self, node) -> int:
        """
        Classify node based on name/description keywords.

        Args:
            node: Node to classify

        Returns:
            Suggested scale (1-7)
        """
        text = f"{node.name} {node.description or ''}".lower()

        # Score each scale by keyword matches
        scores = {}
        for scale, keywords in self.SCALE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[scale] = score

        if not scores:
            return node.scale  # Keep current if no match

        # Return scale with highest score
        return max(scores, key=scores.get)

    def reclassify_node(
        self,
        node,
        new_scale: int,
        reason: str = "Manual reclassification"
    ) -> ClassificationResult:
        """
        Reclassify a node to a new scale.

        Args:
            node: Node to reclassify
            new_scale: New scale value
            reason: Reason for reclassification

        Returns:
            ClassificationResult
        """
        old_scale = node.scale
        changed = old_scale != new_scale

        if changed and not self.dry_run:
            node.scale = new_scale
            self.session.flush()

        self.stats.record_change(changed)

        return ClassificationResult(
            node_id=node.id,
            old_scale=old_scale,
            new_scale=new_scale,
            changed=changed,
            reason=reason
        )

    def migrate_scale_range(
        self,
        old_scale: int,
        new_scale: int,
        distribution: str = "even"
    ) -> List[ClassificationResult]:
        """
        Migrate all nodes from one scale to another (or distribute across range).

        Args:
            old_scale: Source scale to migrate from
            new_scale: Target scale (or start of range)
            distribution: "even" or "weighted" distribution

        Returns:
            List of classification results
        """
        # Import here to avoid circular dependency
        from models import Node

        # Get all nodes at old scale
        nodes = self.session.query(Node).filter(Node.scale == old_scale).all()

        print(f"Migrating {len(nodes)} nodes from scale {old_scale} to {new_scale}")

        results = []
        for node in nodes:
            # Simple migration (could add intelligent distribution logic)
            result = self.reclassify_node(
                node,
                new_scale,
                reason=f"Scale migration: {old_scale} → {new_scale}"
            )
            results.append(result)

        return results

    def redistribute_scale(
        self,
        target_scale: int,
        distribution: Dict[int, float]
    ) -> List[ClassificationResult]:
        """
        Redistribute nodes from one scale across multiple scales.

        Args:
            target_scale: Scale to redistribute from
            distribution: Dict mapping new_scale → percentage (must sum to 1.0)

        Returns:
            List of classification results
        """
        # Import here to avoid circular dependency
        from models import Node

        # Validate distribution
        if abs(sum(distribution.values()) - 1.0) > 0.01:
            raise ValueError(f"Distribution must sum to 1.0, got {sum(distribution.values())}")

        # Get nodes
        nodes = self.session.query(Node).filter(Node.scale == target_scale).all()
        total = len(nodes)

        print(f"Redistributing {total} nodes from scale {target_scale}")

        # Calculate counts for each new scale
        assignments = []
        for new_scale, percentage in sorted(distribution.items()):
            count = int(total * percentage)
            assignments.extend([new_scale] * count)

        # Handle rounding by assigning remainder to most common scale
        while len(assignments) < total:
            most_common_scale = max(distribution, key=distribution.get)
            assignments.append(most_common_scale)

        # Apply reclassifications
        results = []
        for node, new_scale in zip(nodes, assignments):
            result = self.reclassify_node(
                node,
                new_scale,
                reason=f"Redistribution from scale {target_scale}"
            )
            results.append(result)

        return results

    def auto_classify_all(self) -> List[ClassificationResult]:
        """
        Auto-classify all nodes based on keywords.

        Returns:
            List of classification results
        """
        # Import here to avoid circular dependency
        from models import Node

        nodes = self.session.query(Node).all()

        print(f"Auto-classifying {len(nodes)} nodes...")

        results = []
        for node in nodes:
            suggested_scale = self.classify_node_by_keywords(node)
            result = self.reclassify_node(
                node,
                suggested_scale,
                reason="Auto-classification by keywords"
            )
            results.append(result)

        return results

    def commit(self):
        """Commit changes to database."""
        if not self.dry_run:
            self.session.commit()
            print("✓ Changes committed")
        else:
            self.session.rollback()
            print("✓ Dry run - no changes committed")

    def get_scale_distribution(self) -> Dict[int, int]:
        """Get current distribution of nodes across scales."""
        from sqlalchemy import func
        from models import Node

        result = self.session.query(
            Node.scale,
            func.count(Node.id)
        ).group_by(Node.scale).all()

        return {scale: count for scale, count in result}
