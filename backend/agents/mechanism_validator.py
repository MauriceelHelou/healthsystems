"""
Mechanism Validator Agent

Standalone agent for validating mechanism quality across multiple dimensions:
- Structural competency (equity lens, root causes)
- Category alignment (mechanism category matches node types)
- Scale consistency (upstream → downstream causal flow)
- Evidence plausibility (quality rating matches study count)
- Citation verification (DOI validation, metadata consistency)

This agent can be used to:
1. Validate newly extracted mechanisms before saving
2. Re-validate existing mechanism bank periodically
3. Check mechanisms from external collaborators
4. Provide detailed feedback for mechanism improvement

Usage:
    from backend.agents.mechanism_validator import MechanismValidator

    validator = MechanismValidator(confidence_threshold=0.70)
    result = validator.validate(mechanism_dict)

    if result.valid:
        print(f"Mechanism is valid (confidence: {result.overall_confidence:.2f})")
    else:
        print(f"Issues found:")
        for issue in result.issues:
            print(f"  - {issue}")
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfidenceTier(Enum):
    """Confidence tiers for mechanism validation"""
    HIGH = "high"           # ≥ 0.80 - Auto-approve
    MEDIUM = "medium"       # 0.60-0.79 - Curator review recommended
    LOW = "low"             # 0.40-0.59 - Revision needed
    VERY_LOW = "very_low"   # < 0.40 - Reject or major revision


@dataclass
class ValidationResult:
    """
    Result of mechanism validation.

    Attributes:
        valid: Whether mechanism passes validation threshold
        overall_confidence: Aggregated confidence score (0-1)
        confidence_tier: HIGH, MEDIUM, LOW, or VERY_LOW
        category_score: Category alignment score (0-1)
        scale_score: Scale consistency score (0-1)
        evidence_score: Evidence plausibility score (0-1)
        issues: List of validation issues/warnings
        recommendations: List of improvement recommendations
    """
    valid: bool
    overall_confidence: float
    confidence_tier: ConfidenceTier
    category_score: float
    scale_score: float
    evidence_score: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'valid': self.valid,
            'overall_confidence': self.overall_confidence,
            'confidence_tier': self.confidence_tier.value,
            'category_score': self.category_score,
            'scale_score': self.scale_score,
            'evidence_score': self.evidence_score,
            'issues': self.issues,
            'recommendations': self.recommendations
        }


class MechanismValidator:
    """
    Standalone mechanism validator agent.

    Validates mechanism quality across multiple dimensions and provides
    detailed feedback for improvement.
    """

    # Evidence quality requirements - aligned with mechanism_schema_mvp.json
    # Only A, B, C grades are supported (no D grade in schema)
    EVIDENCE_REQUIREMENTS = {
        'A': {
            'min_studies': 5,
            'max_studies': 100,
            'description': 'Meta-analysis or systematic review with 5+ high-quality studies'
        },
        'B': {
            'min_studies': 3,
            'max_studies': 10,
            'description': '3-4 studies or systematic review with moderate evidence'
        },
        'C': {
            'min_studies': 1,
            'max_studies': 4,
            'description': '1-2 studies or limited/emerging evidence'
        }
    }

    # Category keywords for inference
    CATEGORY_KEYWORDS = {
        'built_environment': ['housing', 'neighborhood', 'built', 'walkability', 'park', 'transportation', 'urban', 'pollution', 'air_quality'],
        'social_environment': ['social', 'discrimination', 'stigma', 'isolation', 'support', 'violence', 'crime', 'cohesion'],
        'economic': ['income', 'poverty', 'employment', 'wage', 'economic', 'financial', 'insurance', 'eviction', 'rent'],
        'political': ['policy', 'law', 'regulation', 'taxation', 'government', 'legislation', 'enforcement'],
        'healthcare_access': ['healthcare', 'treatment', 'medical', 'hospital', 'insurance', 'medicaid', 'medicare', 'care', 'provider'],
        'biological': ['inflammatory', 'metabolic', 'immune', 'hormonal', 'genetic', 'biological', 'liver', 'heart', 'kidney'],
        'behavioral': ['diet', 'physical_activity', 'smoking', 'alcohol', 'exercise', 'sedentary', 'drinking', 'binge']
    }

    # Scale level keywords (1=structural to 7=crisis endpoints)
    SCALE_KEYWORDS = {
        1: ['policy', 'law', 'regulation', 'taxation', 'legislation', 'government'],
        2: ['built', 'environment', 'housing', 'neighborhood', 'urban', 'walkability', 'pollution'],
        3: ['institutional', 'healthcare_system', 'school', 'workplace', 'hospital', 'provider'],
        4: ['poverty', 'employment', 'income', 'education', 'insurance', 'economic', 'social_support'],
        5: ['behavior', 'diet', 'physical_activity', 'smoking', 'alcohol', 'adherence', 'drinking'],
        6: ['inflammation', 'metabolic', 'blood_pressure', 'cholesterol', 'stress', 'biomarker', 'liver_enzyme'],
        7: ['disease', 'mortality', 'hospitalization', 'crisis', 'death', 'stroke', 'heart_failure', 'cirrhosis', 'failure']
    }

    # Related category pairs
    RELATED_CATEGORIES = [
        ('built_environment', 'social_environment'),
        ('built_environment', 'behavioral'),
        ('economic', 'social_environment'),
        ('economic', 'healthcare_access'),
        ('social_environment', 'behavioral'),
        ('healthcare_access', 'biological'),
        ('behavioral', 'biological'),
        ('political', 'economic'),
        ('political', 'healthcare_access')
    ]

    def __init__(
        self,
        confidence_threshold: float = 0.70,
        use_tiers: bool = True,
        validate_citations: bool = True
    ):
        """
        Initialize validator.

        Args:
            confidence_threshold: Minimum confidence for "valid" classification (default: 0.70)
            use_tiers: Use confidence tiers instead of binary valid/invalid (default: True)
            validate_citations: Enable citation validation if available (default: True)
        """
        self.confidence_threshold = confidence_threshold
        self.use_tiers = use_tiers
        self.validate_citations = validate_citations

        # Try to import citation validator
        if validate_citations:
            try:
                from utils.citation_validation import CitationValidator
                self.citation_validator = CitationValidator()
                logger.info("Citation validation enabled")
            except ImportError:
                logger.warning("Citation validator not available, skipping citation checks")
                self.citation_validator = None
        else:
            self.citation_validator = None

    def validate(self, mechanism: Dict) -> ValidationResult:
        """
        Validate mechanism across all dimensions.

        Args:
            mechanism: Mechanism dictionary with fields:
                - from_node_id (str)
                - to_node_id (str)
                - category (str)
                - evidence_quality (str): 'A', 'B', 'C', or 'D'
                - n_studies (int)
                - doi (str, optional)
                - primary_citation (str, optional)

        Returns:
            ValidationResult with scores, issues, and recommendations
        """
        issues = []
        recommendations = []

        # 1. Category alignment
        category_score = self._check_category_alignment(mechanism)
        if category_score < 0.6:
            issues.append("Category may not match node types")
            recommendations.append(
                f"Review if '{mechanism.get('category', 'unknown')}' is the most appropriate category. "
                f"Consider: {self._suggest_categories(mechanism)}"
            )

        # 2. Scale consistency
        scale_score = self._check_scale_consistency(mechanism)
        if scale_score < 0.6:
            issues.append("Scale levels may be inconsistent with causal distance")
            recommendations.append(
                "Verify causal direction flows from upstream (structural/policy) to downstream (outcomes/endpoints). "
                "Reverse causality may indicate mechanism needs revision."
            )
        elif scale_score < 0.8:
            recommendations.append(
                "Scale levels are adjacent or same-level. Consider if intermediate mechanisms exist."
            )

        # 3. Evidence plausibility
        evidence_score = self._check_evidence_plausibility(mechanism)
        if evidence_score < 0.6:
            issues.append("Evidence quality rating seems inconsistent with study count")
            quality = mechanism.get('evidence_quality', 'C')
            n_studies = mechanism.get('n_studies', 0)
            expected = self.EVIDENCE_REQUIREMENTS.get(quality, {})
            recommendations.append(
                f"Quality rating '{quality}' typically requires {expected.get('min_studies', 0)}-"
                f"{expected.get('max_studies', 100)} studies, but found {n_studies}. "
                f"Consider adjusting quality rating or study count."
            )

        # 4. Citation validation (if enabled and available)
        if self.citation_validator and mechanism.get('doi'):
            citation_valid, citation_issues = self._validate_citation(mechanism)
            if not citation_valid:
                issues.extend(citation_issues)
                recommendations.append(
                    "Verify DOI is correct and corresponds to the primary citation. "
                    "Check for typos or use DOI resolver (https://doi.org/) to confirm."
                )

        # Calculate overall confidence
        overall_confidence = (category_score + scale_score + evidence_score) / 3

        # Determine confidence tier
        if self.use_tiers:
            if overall_confidence >= 0.80:
                tier = ConfidenceTier.HIGH
            elif overall_confidence >= 0.60:
                tier = ConfidenceTier.MEDIUM
            elif overall_confidence >= 0.40:
                tier = ConfidenceTier.LOW
            else:
                tier = ConfidenceTier.VERY_LOW
        else:
            tier = ConfidenceTier.HIGH if overall_confidence >= self.confidence_threshold else ConfidenceTier.LOW

        # Determine validity
        if self.use_tiers:
            # With tiers, only VERY_LOW is invalid
            valid = tier != ConfidenceTier.VERY_LOW
        else:
            # Binary: pass threshold or fail
            valid = overall_confidence >= self.confidence_threshold and len(issues) == 0

        return ValidationResult(
            valid=valid,
            overall_confidence=overall_confidence,
            confidence_tier=tier,
            category_score=category_score,
            scale_score=scale_score,
            evidence_score=evidence_score,
            issues=issues,
            recommendations=recommendations
        )

    def _check_category_alignment(self, mechanism: Dict) -> float:
        """
        Check if mechanism category aligns with node types.

        Returns confidence score [0, 1]
        """
        category = mechanism.get('category', '')
        from_node = mechanism.get('from_node_id', '')
        to_node = mechanism.get('to_node_id', '')

        # Infer categories from node names
        from_category = self._infer_node_category(from_node)
        to_category = self._infer_node_category(to_node)

        # Perfect match: category matches one of the node categories
        if category in [from_category, to_category]:
            return 1.0

        # Good match: category is related to node categories
        if self._is_related_category(category, from_category) or \
           self._is_related_category(category, to_category):
            return 0.7

        # Poor match: category doesn't align with nodes
        return 0.3

    def _infer_node_category(self, node_id: str) -> str:
        """
        Infer category from node ID based on keywords.

        Args:
            node_id: Node identifier (e.g., "housing_quality", "obesity")

        Returns:
            Inferred category
        """
        node_lower = node_id.lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in node_lower for keyword in keywords):
                return category

        return 'unknown'

    def _is_related_category(self, cat1: str, cat2: str) -> bool:
        """
        Check if two categories are related/compatible.

        Args:
            cat1, cat2: Category names

        Returns:
            True if categories are related
        """
        return (cat1, cat2) in self.RELATED_CATEGORIES or \
               (cat2, cat1) in self.RELATED_CATEGORIES

    def _suggest_categories(self, mechanism: Dict) -> str:
        """Suggest alternative categories based on node types"""
        from_node = mechanism.get('from_node_id', '')
        to_node = mechanism.get('to_node_id', '')

        from_cat = self._infer_node_category(from_node)
        to_cat = self._infer_node_category(to_node)

        suggestions = []
        if from_cat != 'unknown':
            suggestions.append(from_cat)
        if to_cat != 'unknown' and to_cat not in suggestions:
            suggestions.append(to_cat)

        return ', '.join(suggestions) if suggestions else 'unclear from node names'

    def _check_scale_consistency(self, mechanism: Dict) -> float:
        """
        Check if scale levels are consistent with causal distance.

        Scale definitions:
        1: Structural (policy, laws)
        2: Built environment
        3: Institutional
        4: Individual conditions
        5: Behaviors
        6: Intermediate pathways
        7: Crisis endpoints

        Returns confidence score [0, 1]
        """
        from_node = mechanism.get('from_node_id', '')
        to_node = mechanism.get('to_node_id', '')

        from_scale = self._infer_scale_from_node(from_node)
        to_scale = self._infer_scale_from_node(to_node)

        if from_scale is None or to_scale is None:
            return 0.5  # Neutral if we can't determine

        # Good: structural/upstream factors → downstream outcomes
        if from_scale <= to_scale:
            return 1.0

        # Acceptable: adjacent levels (might be bidirectional relationship)
        if from_scale == to_scale + 1:
            return 0.8

        # Problematic: downstream → upstream (reverse causality)
        return 0.3

    def _infer_scale_from_node(self, node_id: str) -> Optional[int]:
        """
        Infer scale level from node ID.

        Returns:
            Scale level (1-7) or None if cannot determine
        """
        node_lower = node_id.lower()

        for scale, keywords in self.SCALE_KEYWORDS.items():
            if any(keyword in node_lower for keyword in keywords):
                return scale

        return None

    def _check_evidence_plausibility(self, mechanism: Dict) -> float:
        """
        Check if evidence quality rating is plausible given study count.

        Returns confidence score [0, 1]
        """
        quality = mechanism.get('evidence_quality', 'C')
        n_studies = mechanism.get('n_studies', 0)

        if quality not in self.EVIDENCE_REQUIREMENTS:
            return 0.5  # Unknown quality rating

        expected = self.EVIDENCE_REQUIREMENTS[quality]
        min_expected = expected['min_studies']
        max_expected = expected['max_studies']

        # Perfect: within expected range
        if min_expected <= n_studies <= max_expected:
            return 1.0

        # Acceptable: slightly below minimum (conservative grading)
        if n_studies < min_expected and n_studies >= min_expected - 2:
            return 0.8

        # Problematic: too few studies for quality grade
        if n_studies < min_expected:
            return 0.6

        # Acceptable: more studies than expected (conservative grade, which is good)
        return 0.8

    def _validate_citation(self, mechanism: Dict) -> Tuple[bool, List[str]]:
        """
        Validate citation DOI and metadata.

        Returns:
            (is_valid, list_of_issues)
        """
        if not self.citation_validator:
            return True, []

        issues = []
        doi = mechanism.get('doi', '')

        if not doi:
            return True, []  # No DOI to validate

        try:
            result = self.citation_validator.verify_doi(doi)

            if not result['valid']:
                issues.append(f"DOI validation failed: {result.get('error', 'Unknown error')}")
                return False, issues

            # Check year consistency if available
            if 'year' in mechanism:
                mech_year = mechanism['year']
                doi_year = result.get('metadata', {}).get('year')

                if doi_year and mech_year and doi_year != mech_year:
                    issues.append(f"Year mismatch: mechanism shows {mech_year}, DOI shows {doi_year}")

            return len(issues) == 0, issues

        except Exception as e:
            logger.error(f"Citation validation error: {e}")
            issues.append(f"Citation validation error: {str(e)}")
            return False, issues

    def validate_batch(
        self,
        mechanisms: List[Dict],
        verbose: bool = True
    ) -> Dict[str, ValidationResult]:
        """
        Validate a batch of mechanisms.

        Args:
            mechanisms: List of mechanism dictionaries
            verbose: Print progress

        Returns:
            Dict mapping mechanism ID to ValidationResult
        """
        results = {}

        for i, mech in enumerate(mechanisms, 1):
            mech_id = mech.get('id', f'mechanism_{i}')

            if verbose:
                print(f"Validating {i}/{len(mechanisms)}: {mech_id}")

            try:
                result = self.validate(mech)
                results[mech_id] = result

                if verbose:
                    tier_symbol = {
                        ConfidenceTier.HIGH: '✓✓',
                        ConfidenceTier.MEDIUM: '✓',
                        ConfidenceTier.LOW: '⚠',
                        ConfidenceTier.VERY_LOW: '✗'
                    }
                    symbol = tier_symbol.get(result.confidence_tier, '?')
                    print(f"  {symbol} {result.confidence_tier.value.upper()} "
                          f"(confidence: {result.overall_confidence:.2f})")

            except Exception as e:
                logger.error(f"Error validating {mech_id}: {e}")
                if verbose:
                    print(f"  ✗ ERROR: {e}")

        return results

    def generate_report(self, results: Dict[str, ValidationResult]) -> str:
        """
        Generate validation report for batch results.

        Args:
            results: Dict from validate_batch

        Returns:
            Formatted report string
        """
        total = len(results)
        if total == 0:
            return "No mechanisms validated."

        # Count by tier
        tier_counts = {tier: 0 for tier in ConfidenceTier}
        for result in results.values():
            tier_counts[result.confidence_tier] += 1

        # Calculate stats
        avg_confidence = sum(r.overall_confidence for r in results.values()) / total
        avg_category = sum(r.category_score for r in results.values()) / total
        avg_scale = sum(r.scale_score for r in results.values()) / total
        avg_evidence = sum(r.evidence_score for r in results.values()) / total

        # Generate report
        report = f"""
========================================
MECHANISM VALIDATION REPORT
========================================

Total Mechanisms: {total}

Confidence Tier Distribution:
  HIGH (≥0.80):      {tier_counts[ConfidenceTier.HIGH]:3d} ({100*tier_counts[ConfidenceTier.HIGH]/total:5.1f}%)
  MEDIUM (0.60-0.79): {tier_counts[ConfidenceTier.MEDIUM]:3d} ({100*tier_counts[ConfidenceTier.MEDIUM]/total:5.1f}%)
  LOW (0.40-0.59):    {tier_counts[ConfidenceTier.LOW]:3d} ({100*tier_counts[ConfidenceTier.LOW]/total:5.1f}%)
  VERY_LOW (<0.40):   {tier_counts[ConfidenceTier.VERY_LOW]:3d} ({100*tier_counts[ConfidenceTier.VERY_LOW]/total:5.1f}%)

Average Scores:
  Overall Confidence: {avg_confidence:.3f}
  Category Alignment: {avg_category:.3f}
  Scale Consistency:  {avg_scale:.3f}
  Evidence Plausibility: {avg_evidence:.3f}

Mechanisms Needing Review ({tier_counts[ConfidenceTier.LOW] + tier_counts[ConfidenceTier.VERY_LOW]} total):
"""

        # List mechanisms needing review
        review_needed = [(mid, r) for mid, r in results.items()
                        if r.confidence_tier in [ConfidenceTier.LOW, ConfidenceTier.VERY_LOW]]

        for mid, result in sorted(review_needed, key=lambda x: x[1].overall_confidence):
            report += f"\n  {mid} ({result.confidence_tier.value}, {result.overall_confidence:.2f}):\n"
            for issue in result.issues:
                report += f"    - {issue}\n"

        report += "\n========================================\n"

        return report


# Convenience function for CLI usage
def validate_mechanism_file(filepath: str, verbose: bool = True) -> ValidationResult:
    """
    Validate a mechanism from YAML file.

    Args:
        filepath: Path to mechanism YAML file
        verbose: Print result

    Returns:
        ValidationResult
    """
    import yaml
    from pathlib import Path

    with open(filepath, 'r', encoding='utf-8') as f:
        mechanism = yaml.safe_load(f)

    # Convert to validation format
    mech_dict = {
        'id': mechanism.get('id', Path(filepath).stem),
        'from_node_id': mechanism.get('from_node', {}).get('node_id', ''),
        'to_node_id': mechanism.get('to_node', {}).get('node_id', ''),
        'category': mechanism.get('category', ''),
        'evidence_quality': mechanism.get('evidence', {}).get('quality_rating', 'D'),
        'n_studies': mechanism.get('evidence', {}).get('n_studies', 0),
        'doi': mechanism.get('evidence', {}).get('doi', '')
    }

    validator = MechanismValidator()
    result = validator.validate(mech_dict)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Validation Result: {Path(filepath).name}")
        print(f"{'='*60}")
        print(f"Confidence Tier: {result.confidence_tier.value.upper()}")
        print(f"Overall Confidence: {result.overall_confidence:.3f}")
        print(f"  - Category Alignment: {result.category_score:.3f}")
        print(f"  - Scale Consistency: {result.scale_score:.3f}")
        print(f"  - Evidence Plausibility: {result.evidence_score:.3f}")

        if result.issues:
            print(f"\nIssues:")
            for issue in result.issues:
                print(f"  - {issue}")

        if result.recommendations:
            print(f"\nRecommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")

        print(f"{'='*60}\n")

    return result


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Validate mechanism quality")
    parser.add_argument('--file', type=str, help='Validate single YAML file')
    parser.add_argument('--dir', type=str, help='Validate directory of YAML files')
    parser.add_argument('--threshold', type=float, default=0.70, help='Confidence threshold')
    parser.add_argument('--report', action='store_true', help='Generate validation report')

    args = parser.parse_args()

    if args.file:
        result = validate_mechanism_file(args.file)
        exit(0 if result.valid else 1)

    elif args.dir:
        import yaml

        validator = MechanismValidator(confidence_threshold=args.threshold)
        mechanism_dir = Path(args.dir)
        yaml_files = list(mechanism_dir.rglob("*.yml")) + list(mechanism_dir.rglob("*.yaml"))

        mechanisms = []
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    mech = yaml.safe_load(f)

                mech_dict = {
                    'id': mech.get('id', yaml_file.stem),
                    'from_node_id': mech.get('from_node', {}).get('node_id', ''),
                    'to_node_id': mech.get('to_node', {}).get('node_id', ''),
                    'category': mech.get('category', ''),
                    'evidence_quality': mech.get('evidence', {}).get('quality_rating', 'D'),
                    'n_studies': mech.get('evidence', {}).get('n_studies', 0),
                    'doi': mech.get('evidence', {}).get('doi', '')
                }
                mechanisms.append(mech_dict)
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")

        results = validator.validate_batch(mechanisms, verbose=True)

        if args.report:
            print(validator.generate_report(results))

        # Exit with error if any mechanisms are VERY_LOW
        very_low_count = sum(1 for r in results.values() if r.confidence_tier == ConfidenceTier.VERY_LOW)
        exit(0 if very_low_count == 0 else 1)

    else:
        parser.print_help()
