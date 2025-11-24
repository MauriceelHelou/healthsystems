# PROMPT 2: Consolidate Node Classification Scripts

## Context
The codebase contains **4 separate node classification scripts** with overlapping functionality, totaling **1,576 lines of code**. Each handles node reclassification, scale migration, or grading differently, creating confusion and maintenance burden.

## Current State

### Files to Consolidate (1,576 LOC → 700 LOC target)

**Classification scripts:**
- `backend/scripts/reclassify_nodes_v2.py` (433 LOC)
- `backend/scripts/apply_node_reclassification.py` (398 LOC)
- `backend/scripts/aggressive_redistribution.py` (270 LOC)
- `backend/scripts/regrade_mechanisms.py` (475 LOC)

### Redundancy Examples

**Example 1: Database Operations (duplicated 4 times)**
```python
# reclassify_nodes_v2.py (lines 89-95)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

try:
    nodes = session.query(Node).all()
    # ... process nodes
finally:
    session.close()

# apply_node_reclassification.py (lines 45-51) - IDENTICAL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

try:
    nodes = session.query(Node).all()
    # ... process nodes
finally:
    session.close()
```

**Example 2: Scale Validation (duplicated 3 times)**
```python
# reclassify_nodes_v2.py (lines 123-129)
def validate_scale(scale: int) -> bool:
    if scale < 1 or scale > 7:
        print(f"Invalid scale: {scale}. Must be 1-7.")
        return False
    return True

# aggressive_redistribution.py (lines 78-84) - IDENTICAL
def validate_scale(scale: int) -> bool:
    if scale < 1 or scale > 7:
        print(f"Invalid scale: {scale}. Must be 1-7.")
        return False
    return True
```

**Example 3: Statistics Reporting (duplicated 4 times)**
```python
# regrade_mechanisms.py (lines 389-401)
print(f"\n{'='*60}")
print(f"REGRADING COMPLETE")
print(f"{'='*60}")
print(f"Total mechanisms processed: {total}")
print(f"Upgraded: {upgraded}")
print(f"Downgraded: {downgraded}")
print(f"Unchanged: {unchanged}")

# apply_node_reclassification.py (lines 312-324) - VERY SIMILAR
print(f"\n{'='*60}")
print(f"RECLASSIFICATION COMPLETE")
print(f"{'='*60}")
print(f"Total nodes processed: {total}")
print(f"Changed: {changed}")
print(f"Unchanged: {unchanged}")
```

## Target Architecture

```
backend/
├── core/
│   ├── __init__.py
│   ├── node_classification.py          # 400 LOC - Core classification logic
│   │   ├── NodeClassifier               # Main classifier class
│   │   ├── reclassify_node()
│   │   ├── validate_scale()
│   │   └── migrate_node_scale()
│   │
│   └── mechanism_grading.py            # 300 LOC - Mechanism grading
│       ├── MechanismGrader
│       ├── regrade_mechanism()
│       └── calculate_evidence_score()
│
└── scripts/
    ├── classify_nodes.py               # 80 LOC - Unified CLI
    └── (delete 4 old scripts)
```

## Implementation Steps

### Step 1: Create Node Classification Module

**File: `backend/core/node_classification.py`**

```python
"""
Node classification and scale management.
Handles node reclassification, scale validation, and migration.
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

from models import Node, Mechanism


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

    def classify_node_by_keywords(self, node: Node) -> int:
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
        node: Node,
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

        result = self.session.query(
            Node.scale,
            func.count(Node.id)
        ).group_by(Node.scale).all()

        return {scale: count for scale, count in result}
```

### Step 2: Create Mechanism Grading Module

**File: `backend/core/mechanism_grading.py`**

```python
"""
Mechanism evidence grading and quality assessment.
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from dataclasses import dataclass

from models import Mechanism


@dataclass
class GradingResult:
    """Result of a grading operation."""
    mechanism_id: str
    old_grade: str
    new_grade: str
    changed: bool
    reason: str


@dataclass
class GradingStats:
    """Statistics for grading operations."""
    total: int = 0
    upgraded: int = 0
    downgraded: int = 0
    unchanged: int = 0

    def record_change(self, old_grade: str, new_grade: str):
        self.total += 1

        grade_order = {'A': 3, 'B': 2, 'C': 1}
        old_rank = grade_order.get(old_grade, 0)
        new_rank = grade_order.get(new_grade, 0)

        if new_rank > old_rank:
            self.upgraded += 1
        elif new_rank < old_rank:
            self.downgraded += 1
        else:
            self.unchanged += 1

    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"GRADING COMPLETE")
        print(f"{'='*60}")
        print(f"Total mechanisms: {self.total}")
        print(f"Upgraded: {self.upgraded}")
        print(f"Downgraded: {self.downgraded}")
        print(f"Unchanged: {self.unchanged}")


class MechanismGrader:
    """
    Mechanism evidence grading engine.
    Assesses and updates evidence quality ratings.
    """

    # Grading criteria
    GRADE_A_THRESHOLD = 10  # 10+ high-quality studies
    GRADE_B_THRESHOLD = 3   # 3-9 studies or strong single study

    def __init__(self, session: Session, dry_run: bool = False):
        self.session = session
        self.dry_run = dry_run
        self.stats = GradingStats()

    def calculate_evidence_grade(self, mechanism: Mechanism) -> str:
        """
        Calculate evidence grade based on quality indicators.

        Args:
            mechanism: Mechanism to grade

        Returns:
            Grade ('A', 'B', or 'C')
        """
        n_studies = mechanism.evidence_n_studies or 0
        has_doi = bool(mechanism.evidence_doi)
        has_primary = bool(mechanism.evidence_primary_citation)
        has_supporting = bool(mechanism.evidence_supporting_citations)

        # Grade A: Strong evidence
        if n_studies >= self.GRADE_A_THRESHOLD and has_doi:
            return 'A'

        # Grade B: Moderate evidence
        if n_studies >= self.GRADE_B_THRESHOLD and has_primary:
            return 'B'

        # Grade B: Strong single study with support
        if n_studies >= 1 and has_doi and has_supporting:
            return 'B'

        # Grade C: Limited evidence
        return 'C'

    def regrade_mechanism(self, mechanism: Mechanism) -> GradingResult:
        """
        Regrade a single mechanism.

        Args:
            mechanism: Mechanism to regrade

        Returns:
            GradingResult
        """
        old_grade = mechanism.evidence_quality
        new_grade = self.calculate_evidence_grade(mechanism)
        changed = old_grade != new_grade

        if changed and not self.dry_run:
            mechanism.evidence_quality = new_grade
            self.session.flush()

        self.stats.record_change(old_grade, new_grade)

        return GradingResult(
            mechanism_id=mechanism.id,
            old_grade=old_grade,
            new_grade=new_grade,
            changed=changed,
            reason=f"Evidence assessment: {mechanism.evidence_n_studies} studies"
        )

    def regrade_all(self) -> List[GradingResult]:
        """
        Regrade all mechanisms.

        Returns:
            List of grading results
        """
        mechanisms = self.session.query(Mechanism).all()

        print(f"Regrading {len(mechanisms)} mechanisms...")

        results = []
        for mechanism in mechanisms:
            result = self.regrade_mechanism(mechanism)
            results.append(result)

        return results

    def regrade_category(self, category: str) -> List[GradingResult]:
        """
        Regrade mechanisms in a specific category.

        Args:
            category: Category to regrade

        Returns:
            List of grading results
        """
        mechanisms = self.session.query(Mechanism).filter(
            Mechanism.category == category
        ).all()

        print(f"Regrading {len(mechanisms)} mechanisms in category '{category}'...")

        results = []
        for mechanism in mechanisms:
            result = self.regrade_mechanism(mechanism)
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

    def get_grade_distribution(self) -> Dict[str, int]:
        """Get current distribution of evidence grades."""
        from sqlalchemy import func

        result = self.session.query(
            Mechanism.evidence_quality,
            func.count(Mechanism.id)
        ).group_by(Mechanism.evidence_quality).all()

        return {grade: count for grade, count in result}
```

### Step 3: Create Unified CLI

**File: `backend/scripts/classify_nodes.py`**

```python
#!/usr/bin/env python3
"""
Unified CLI for node classification and mechanism grading.
Replaces 4 separate scripts.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.node_classification import NodeClassifier
from core.mechanism_grading import MechanismGrader
from models import get_db


def main():
    parser = argparse.ArgumentParser(
        prog='classify_nodes',
        description='Node classification and mechanism grading'
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Reclassify command
    reclassify = subparsers.add_parser('reclassify', help='Reclassify nodes')
    reclassify.add_argument('--auto', action='store_true', help='Auto-classify by keywords')
    reclassify.add_argument('--migrate', type=int, nargs=2, metavar=('FROM', 'TO'),
                           help='Migrate from old scale to new scale')
    reclassify.add_argument('--dry-run', action='store_true', help='Preview changes without committing')

    # Regrade command
    regrade = subparsers.add_parser('regrade', help='Regrade mechanisms')
    regrade.add_argument('--category', help='Regrade specific category only')
    regrade.add_argument('--dry-run', action='store_true', help='Preview changes without committing')

    # Stats command
    stats = subparsers.add_parser('stats', help='Show distribution statistics')
    stats.add_argument('--type', choices=['nodes', 'mechanisms'], default='nodes')

    args = parser.parse_args()

    # Get database session
    db = next(get_db())

    try:
        if args.command == 'reclassify':
            classifier = NodeClassifier(db, dry_run=args.dry_run)

            if args.auto:
                results = classifier.auto_classify_all()
            elif args.migrate:
                old_scale, new_scale = args.migrate
                results = classifier.migrate_scale_range(old_scale, new_scale)
            else:
                print("Error: Must specify --auto or --migrate")
                sys.exit(1)

            classifier.commit()
            classifier.stats.print_summary()

        elif args.command == 'regrade':
            grader = MechanismGrader(db, dry_run=args.dry_run)

            if args.category:
                results = grader.regrade_category(args.category)
            else:
                results = grader.regrade_all()

            grader.commit()
            grader.stats.print_summary()

        elif args.command == 'stats':
            if args.type == 'nodes':
                classifier = NodeClassifier(db)
                dist = classifier.get_scale_distribution()
                print("\nNode Scale Distribution:")
                for scale in sorted(dist.keys()):
                    print(f"  Scale {scale}: {dist[scale]} nodes")
            else:
                grader = MechanismGrader(db)
                dist = grader.get_grade_distribution()
                print("\nMechanism Grade Distribution:")
                for grade in ['A', 'B', 'C']:
                    count = dist.get(grade, 0)
                    print(f"  Grade {grade}: {count} mechanisms")

    finally:
        db.close()


if __name__ == "__main__":
    main()
```

### Step 4: Create Package Init

**File: `backend/core/__init__.py`**

```python
"""
Core business logic for HealthSystems platform.
"""
from .node_classification import NodeClassifier, ClassificationResult, ClassificationStats
from .mechanism_grading import MechanismGrader, GradingResult, GradingStats

__all__ = [
    'NodeClassifier',
    'ClassificationResult',
    'ClassificationStats',
    'MechanismGrader',
    'GradingResult',
    'GradingStats',
]
```

## Migration Checklist

### Phase 1: Setup (Day 1)
- [ ] Create `backend/core/` directory
- [ ] Create `node_classification.py` with all functions
- [ ] Create `mechanism_grading.py` with all functions
- [ ] Create unified CLI script
- [ ] Test imports: `python -c "from core import NodeClassifier, MechanismGrader"`

### Phase 2: Testing (Day 1-2)
- [ ] Test auto-classification: `python scripts/classify_nodes.py reclassify --auto --dry-run`
- [ ] Test scale migration: `python scripts/classify_nodes.py reclassify --migrate 2 3 --dry-run`
- [ ] Test regrading: `python scripts/classify_nodes.py regrade --dry-run`
- [ ] Test stats: `python scripts/classify_nodes.py stats`
- [ ] Verify results match old scripts

### Phase 3: Migration (Day 2)
- [ ] Update documentation
- [ ] Run on production data (with backup!)
- [ ] Verify database state

### Phase 4: Cleanup (Day 2)
- [ ] Delete 4 old scripts:
  - `reclassify_nodes_v2.py`
  - `apply_node_reclassification.py`
  - `aggressive_redistribution.py`
  - `regrade_mechanisms.py`
- [ ] Commit with message: "refactor: consolidate 4 classification scripts into unified framework"

## Success Criteria

- ✅ All 4 old scripts deleted
- ✅ Single unified CLI works for all operations
- ✅ Database operations match old behavior
- ✅ Statistics reporting preserved
- ✅ Dry-run mode working
- ✅ **876 LOC eliminated** (1,576 → 700)

## Estimated Effort
**2 days** (1 day implementation, 1 day testing/migration)
