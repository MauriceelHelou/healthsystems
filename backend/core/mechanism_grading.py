"""
Mechanism evidence grading and quality assessment.
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from dataclasses import dataclass


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

    def calculate_evidence_grade(self, mechanism) -> str:
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

    def regrade_mechanism(self, mechanism) -> GradingResult:
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
        # Import here to avoid circular dependency
        from models import Mechanism

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
        # Import here to avoid circular dependency
        from models import Mechanism

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
        from models import Mechanism

        result = self.session.query(
            Mechanism.evidence_quality,
            func.count(Mechanism.id)
        ).group_by(Mechanism.evidence_quality).all()

        return {grade: count for grade, count in result}
