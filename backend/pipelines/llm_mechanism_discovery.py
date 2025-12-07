"""
LLM Mechanism Discovery Pipeline (Version 2 - Citation Verified)

IMPROVEMENTS OVER V1:
1. DOI validation via Crossref API
2. Citation context passed from literature search
3. Prompt NO LONGER requests citation extraction from abstracts
4. Post-extraction validation of citations
5. Flags mechanisms needing manual review

This version prevents false/fabricated citations.
"""

import anthropic
import json
import yaml
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from pydantic import BaseModel, Field, validator
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.citation_validation import CitationValidator, verify_doi, format_chicago_citation
from utils.canonical_nodes import (
    load_canonical_nodes,
    find_matching_node,
    generate_compact_node_list,
    normalize_node_id,
    get_node_by_id,
    get_all_nodes
)

logger = logging.getLogger(__name__)


class MechanismExtraction(BaseModel):
    """Pydantic model for LLM-extracted mechanism data (V2 with citation validation)"""

    from_node_id: str = Field(description="Source node ID (snake_case)")
    from_node_name: str = Field(description="Human-readable source node name")
    to_node_id: str = Field(description="Target node ID (snake_case)")
    to_node_name: str = Field(description="Human-readable target node name")
    direction: str = Field(description="'positive' or 'negative'")
    category: str = Field(description="Primary category")
    mechanism_pathway: List[str] = Field(description="Step-by-step causal pathway")
    evidence_quality: str = Field(description="'A', 'B', or 'C' (no D grade)")
    n_studies: int = Field(description="Number of supporting studies")
    primary_citation: str = Field(description="Chicago-style citation")
    supporting_citations: Optional[List[str]] = Field(default=None)
    doi: Optional[str] = Field(default=None)
    varies_by_geography: bool = Field(default=False)
    variation_notes: Optional[str] = Field(default=None)
    moderators: Optional[List[Dict]] = Field(default=None)
    description: str = Field(description="Detailed mechanism description")
    structural_competency_notes: Optional[str] = Field(default=None)
    confidence: str = Field(description="'high', 'medium', or 'low'")

    # Citation validation metadata (V2 addition)
    citation_verified: bool = Field(default=False, description="Whether DOI was verified")
    needs_manual_review: bool = Field(default=False, description="Whether mechanism needs human review")
    citation_issues: Optional[List[str]] = Field(default=None, description="List of citation problems")

    # Quantitative metrics (extract when available)
    effect_size_value: Optional[float] = Field(default=None)
    effect_size_type: Optional[str] = Field(default=None)
    confidence_interval_lower: Optional[float] = Field(default=None)
    confidence_interval_upper: Optional[float] = Field(default=None)
    standard_error: Optional[float] = Field(default=None)
    p_value: Optional[float] = Field(default=None)
    sample_size: Optional[int] = Field(default=None)

    # Meta-analysis metrics
    heterogeneity_i_squared: Optional[float] = Field(default=None)
    heterogeneity_tau_squared: Optional[float] = Field(default=None)
    cochrans_q: Optional[float] = Field(default=None)
    cochrans_q_p: Optional[float] = Field(default=None)

    # Dose-response
    dose_response_trend: Optional[str] = Field(default=None)
    dose_response_p_trend: Optional[float] = Field(default=None)

    # Subgroup effects
    effect_varies_by_subgroup: Optional[bool] = Field(default=False)
    subgroup_heterogeneity_p: Optional[float] = Field(default=None)

    # Sensitivity analyses
    sensitivity_analysis_performed: Optional[bool] = Field(default=False)
    sensitivity_analysis_notes: Optional[str] = Field(default=None)

    # Publication bias
    publication_bias_assessed: Optional[bool] = Field(default=False)
    eggers_test_p: Optional[float] = Field(default=None)
    funnel_plot_asymmetry: Optional[str] = Field(default=None)

    # Effect magnitude interpretation (7-point Likert scale)
    effect_magnitude_likert: Optional[int] = Field(default=None)
    effect_magnitude_rationale: Optional[str] = Field(default=None)

    # Additional statistical metrics
    adjusted_for_confounders: Optional[bool] = Field(default=None)
    confounders_adjusted: Optional[List[str]] = Field(default=None)
    causal_inference_method: Optional[str] = Field(default=None)


class LLMMechanismDiscoveryV2:
    """
    LLM-based mechanism discovery pipeline V2 with citation verification.

    FIXES:
    - Validates DOIs via Crossref API
    - Accepts verified citation metadata from literature search
    - No longer asks LLM to extract citations from abstracts
    - Flags mechanisms needing review
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        validate_citations: bool = True,
        strict_validation: bool = True,
        validate_canonical_nodes: bool = True,
        minimum_supporting_citations: int = 3
    ):
        """
        Initialize the LLM discovery pipeline V2.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            validate_citations: Whether to validate DOIs (default: True)
            strict_validation: If True, reject mechanisms with invalid DOIs (default: True)
            validate_canonical_nodes: If True, reject mechanisms with non-canonical nodes (default: True)
            minimum_supporting_citations: Minimum required supporting citations (default: 3)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-opus-4-5-20251101"
        self.prompt_version = "2.1-canonical-validated"
        self.validate_citations = validate_citations
        self.strict_validation = strict_validation
        self.validate_canonical_nodes = validate_canonical_nodes
        self.minimum_supporting_citations = minimum_supporting_citations
        self.citation_validator = CitationValidator() if validate_citations else None

        # Load canonical node inventory for validation
        if validate_canonical_nodes:
            self._canonical_node_ids = set(n['id'] for n in get_all_nodes())
            logger.info(f"Loaded {len(self._canonical_node_ids)} canonical nodes for validation")

        logger.info(
            f"Initialized LLM Discovery V2.1 "
            f"(citation_validation={'ON' if validate_citations else 'OFF'}, "
            f"canonical_validation={'ON' if validate_canonical_nodes else 'OFF'}, "
            f"min_citations={minimum_supporting_citations})"
        )

    def validate_node_is_canonical(self, node_id: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a node ID exists in the canonical inventory.

        Args:
            node_id: Node ID to validate

        Returns:
            Tuple of (is_valid, suggested_canonical_id or None)
        """
        if not self.validate_canonical_nodes:
            return True, None

        # Check for NEW: prefix (proposed new nodes)
        if node_id.startswith("NEW:"):
            return False, None

        # Normalize and check exact match
        normalized_id = normalize_node_id(node_id)
        if normalized_id in self._canonical_node_ids:
            return True, normalized_id

        # Try fuzzy matching
        match, score = find_matching_node(node_id, threshold=0.8)
        if match:
            logger.warning(f"Node '{node_id}' not exact match, suggesting '{match['id']}' ({score:.0%})")
            return False, match['id']

        return False, None

    def create_extraction_prompt_with_verified_citation(
        self,
        paper_abstract: str,
        paper_title: str,
        citation_context: Dict,
        focus_area: Optional[str] = None,
        include_canonical_nodes: bool = True
    ) -> str:
        """
        Create prompt with VERIFIED citation context (V2 approach).

        KEY CHANGE: Does NOT ask LLM to extract citations from abstract.
        Instead, provides verified citation metadata.

        Args:
            paper_abstract: Abstract text
            paper_title: Paper title
            citation_context: Dict with authors, year, doi, journal (from literature search)
            focus_area: Optional focus area
            include_canonical_nodes: Whether to include canonical node list (default True)

        Returns:
            Formatted prompt
        """
        # Format verified citation for prompt
        verified_citation = self._format_verified_citation(citation_context)

        # Generate canonical node list for prompt
        canonical_node_section = ""
        if include_canonical_nodes:
            canonical_node_section = f"""
---

## CANONICAL NODE INVENTORY (REQUIRED)

You MUST match nodes to this canonical inventory. We have 840 pre-defined nodes.

**HOW TO USE:**
1. First check if your intended node matches a canonical node (exact or near match)
2. If match found: Use the canonical node_id EXACTLY as shown
3. If no match: Propose a NEW node with "NEW:" prefix in node_id (e.g., "NEW:proposed_node_name")

**Node Inventory (by domain):**

{generate_compact_node_list(max_per_domain=12)}

**CRITICAL**: Do NOT invent node IDs. Use canonical IDs when available. Mark new proposals clearly.

"""

        prompt = f"""You are an expert in public health, epidemiology, and structural determinants of health. Your task is to extract causal mechanisms from scientific literature for a health equity decision support system.

**Paper Title**: {paper_title}

**Paper Abstract**:
{paper_abstract}

**VERIFIED CITATION** (use this EXACTLY, do NOT modify):
{verified_citation}
{canonical_node_section}
---

## CRITICAL INSTRUCTIONS

**CITATION HANDLING**:
- You are PROVIDED with the verified citation above
- DO NOT attempt to extract or modify the citation from the abstract
- USE the provided citation EXACTLY as given
- For primary_citation field, use: {verified_citation}
- For doi field, use: {citation_context.get('doi', '')}

**SUPPORTING CITATIONS (MINIMUM 3 REQUIRED)**:
- Extract AT LEAST 3 supporting citations from the paper/abstract
- For META-ANALYSES: Extract citations of 3+ key studies included in the analysis
- For SYSTEMATIC REVIEWS: Extract citations of 3+ representative primary studies
- For PRIMARY STUDIES: Extract citations of 3+ prior studies mentioned in abstract
- Format each citation with author, year, and journal if available
- If fewer than 3 citations are extractable, list what is available and note "Additional citations require full-text access"

**EVIDENCE GRADING (STRICT CRITERIA)**:
- Grade is determined by STUDY COUNT in this paper:
  - **A**: Paper reports ≥5 studies (meta-analysis/systematic review with 5+ studies)
  - **B**: Paper reports 3-4 studies
  - **C**: Paper reports 1-2 studies OR single cohort/case-control
- n_studies MUST reflect the actual number stated in the abstract
- If abstract says "meta-analysis of 12 studies" → n_studies=12, grade=A
- If abstract describes a single cohort → n_studies=1, grade=C
- DO NOT inflate n_studies or grade

---

## TASK

Extract ALL causal mechanisms described in this paper that relate structural/environmental factors to health outcomes.

### 1. IDENTIFY NODES (FROM -> TO)
- **FROM node**: Upstream factor (policy, environment, economic condition)
- **TO node**: Downstream factor (health behavior, biological pathway, health outcome)
- **MUST** use canonical node IDs from the inventory when available
- Use snake_case format (e.g., "alcohol_outlet_density" not "Alcohol Outlet Density")

### 2. DETERMINE DIRECTION
- **positive**: Increase in FROM -> Increase in TO
- **negative**: Increase in FROM -> Decrease in TO

### 3. DESCRIBE PATHWAY
- List 2-5 intermediate steps explaining HOW the mechanism operates
- Focus on structural and biological processes, NOT individual behaviors as blame

### 4. EXTRACT QUANTITATIVE DATA (CRITICAL - extract ALL numeric values)
Extract these fields when explicitly stated in abstract:
- **effect_size_value**: The numeric point estimate (e.g., 1.5, 0.85, 2.3)
- **effect_size_type**: Type of measure (odds_ratio, relative_risk, hazard_ratio, risk_difference, percentage_change, beta_coefficient, correlation, standardized_mean_difference)
- **confidence_interval_lower**: Lower bound of CI (e.g., 1.2)
- **confidence_interval_upper**: Upper bound of CI (e.g., 1.9)
- **p_value**: Statistical significance (e.g., 0.001)
- **sample_size**: Total N or number of participants
- **heterogeneity_i_squared**: I² statistic for meta-analyses (e.g., 45.2)

### 5. IDENTIFY MODERATORS
- Factors that strengthen/weaken the mechanism
- Rate strength as weak/moderate/strong

### 6. FLAG SPATIAL VARIATION
- Does the paper mention geographic variation?

### 7. STRUCTURAL COMPETENCY
- Does this mechanism trace to structural root causes?
- Does it avoid blaming individuals?
- What are the equity implications?

---

## OUTPUT FORMAT

Return a JSON array of mechanisms:

```json
[
  {{
    "from_node_id": "canonical_snake_case_id",
    "from_node_name": "Human Readable Name",
    "to_node_id": "canonical_snake_case_id",
    "to_node_name": "Human Readable Name",
    "direction": "positive|negative",
    "category": "built_environment|social_environment|economic|political|healthcare_access|biological|behavioral",
    "mechanism_pathway": [
      "Step 1: ...",
      "Step 2: ...",
      "Step 3: ..."
    ],
    "evidence_quality": "A|B|C",
    "n_studies": <number>,
    "primary_citation": "{verified_citation}",
    "supporting_citations": [
      "Author1 et al. (Year). Journal Name.",
      "Author2 et al. (Year). Journal Name.",
      "Author3 et al. (Year). Journal Name."
    ],
    "doi": "{citation_context.get('doi', '')}",

    "effect_size_value": <number or null>,
    "effect_size_type": "odds_ratio|relative_risk|hazard_ratio|risk_difference|percentage_change|beta_coefficient|correlation|null",
    "confidence_interval_lower": <number or null>,
    "confidence_interval_upper": <number or null>,
    "p_value": <number or null>,
    "sample_size": <number or null>,
    "heterogeneity_i_squared": <number or null>,

    "varies_by_geography": true|false,
    "variation_notes": "...",
    "moderators": [
      {{
        "name": "moderator_name",
        "direction": "strengthens|weakens|u_shaped",
        "strength": "weak|moderate|strong",
        "description": "..."
      }}
    ],
    "description": "...",
    "structural_competency_notes": "...",
    "confidence": "high|medium|low"
  }}
]
```

**IMPORTANT**:
- For quantitative fields, extract the EXACT numeric values from the abstract. If not stated, use null.
- For node IDs, use canonical inventory IDs. Prefix new nodes with "NEW:".

---

## STRUCTURAL COMPETENCY GUIDELINES

**PRIORITIZE mechanisms that:**
- Trace to policy, economic systems, or spatial arrangements
- Explain HOW structural factors produce health inequities
- Avoid individual-level blame
- Focus on root causes, not proximate symptoms

**EQUITY LENS**:
- Always note if effects differ by race, class, gender
- Explain HOW structural inequities create differential exposure or vulnerability

---

Now extract ALL mechanisms from the provided paper. Return ONLY valid JSON, no additional text.
"""

        if focus_area:
            prompt += f"\n\n**FOCUS AREA**: Prioritize mechanisms related to {focus_area}"

        return prompt

    def _format_verified_citation(self, citation_context: Dict) -> str:
        """Format verified citation metadata as Chicago-style citation"""
        if not citation_context:
            return "Citation unavailable"

        # Use our citation validator to format
        return format_chicago_citation(citation_context)

    def extract_mechanisms_from_paper(
        self,
        paper_abstract: str,
        paper_title: str,
        citation_context: Optional[Dict] = None,
        focus_area: Optional[str] = None,
        max_tokens: int = 4000
    ) -> List[MechanismExtraction]:
        """
        Extract mechanisms from a paper with citation verification (V2).

        Args:
            paper_abstract: Abstract text
            paper_title: Paper title
            citation_context: REQUIRED dict with authors, year, doi, journal
            focus_area: Optional focus area
            max_tokens: Maximum tokens for response

        Returns:
            List of extracted and validated mechanisms
        """
        if not citation_context:
            logger.error("No citation_context provided - this is REQUIRED in V2")
            raise ValueError("citation_context is required in V2 to prevent false citations")

        # Create prompt with verified citation
        prompt = self.create_extraction_prompt_with_verified_citation(
            paper_abstract,
            paper_title,
            citation_context,
            focus_area
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            response_text = response.content[0].text

            try:
                mechanisms_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Handle markdown code blocks
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                    mechanisms_data = json.loads(response_text)
                else:
                    raise

            # Validate and verify each mechanism
            mechanisms = []
            if isinstance(mechanisms_data, list):
                for mech_data in mechanisms_data:
                    mech = MechanismExtraction(**mech_data)

                    # V2.1: Validate canonical nodes
                    if self.validate_canonical_nodes:
                        from_valid, from_suggestion = self.validate_node_is_canonical(mech.from_node_id)
                        to_valid, to_suggestion = self.validate_node_is_canonical(mech.to_node_id)

                        if not from_valid:
                            suggestion_msg = f" (suggested: {from_suggestion})" if from_suggestion else ""
                            logger.warning(
                                f"Rejecting mechanism: from_node '{mech.from_node_id}' is not canonical{suggestion_msg}"
                            )
                            continue

                        if not to_valid:
                            suggestion_msg = f" (suggested: {to_suggestion})" if to_suggestion else ""
                            logger.warning(
                                f"Rejecting mechanism: to_node '{mech.to_node_id}' is not canonical{suggestion_msg}"
                            )
                            continue

                    # V2.1: Check minimum supporting citations
                    supporting_count = len(mech.supporting_citations) if mech.supporting_citations else 0
                    if supporting_count < self.minimum_supporting_citations:
                        logger.warning(
                            f"Mechanism {mech.from_node_id}_to_{mech.to_node_id} has only "
                            f"{supporting_count} supporting citations (minimum: {self.minimum_supporting_citations})"
                        )
                        # Add to citation issues but don't reject - flag for review
                        if mech.citation_issues is None:
                            mech.citation_issues = []
                        mech.citation_issues.append(
                            f"Only {supporting_count} supporting citations (minimum: {self.minimum_supporting_citations})"
                        )

                    # V2: Validate citation
                    validated_mech = self._validate_mechanism_citation(
                        mech,
                        citation_context
                    )

                    if self.strict_validation and validated_mech.needs_manual_review:
                        logger.warning(
                            f"Skipping mechanism {validated_mech.from_node_id}_to_{validated_mech.to_node_id} "
                            f"due to citation issues: {validated_mech.citation_issues}"
                        )
                        continue

                    mechanisms.append(validated_mech)
            else:
                mech = MechanismExtraction(**mechanisms_data)

                # V2.1: Validate canonical nodes for single mechanism
                if self.validate_canonical_nodes:
                    from_valid, _ = self.validate_node_is_canonical(mech.from_node_id)
                    to_valid, _ = self.validate_node_is_canonical(mech.to_node_id)
                    if not from_valid or not to_valid:
                        logger.warning(f"Rejecting mechanism with non-canonical nodes")
                        return []

                validated_mech = self._validate_mechanism_citation(mech, citation_context)

                if not (self.strict_validation and validated_mech.needs_manual_review):
                    mechanisms.append(validated_mech)

            logger.info(f"Extracted {len(mechanisms)} validated mechanism(s)")
            return mechanisms

        except Exception as e:
            logger.error(f"Error extracting mechanisms: {e}")
            raise

    def _validate_mechanism_citation(
        self,
        mechanism: MechanismExtraction,
        citation_context: Dict
    ) -> MechanismExtraction:
        """
        Validate mechanism citation against verified metadata (V2 feature).

        Args:
            mechanism: Extracted mechanism
            citation_context: Verified citation metadata

        Returns:
            Mechanism with validation metadata added
        """
        issues = []

        if not self.validate_citations:
            mechanism.citation_verified = False
            mechanism.needs_manual_review = False
            return mechanism

        # Check 1: DOI validation
        if mechanism.doi:
            doi_result = self.citation_validator.verify_doi(mechanism.doi)

            if doi_result["valid"]:
                mechanism.citation_verified = True

                # Check if DOI matches source paper
                if citation_context.get('doi') and mechanism.doi != citation_context['doi']:
                    issues.append(f"DOI mismatch: mechanism has {mechanism.doi}, source has {citation_context['doi']}")

                # Check year consistency
                doi_year = doi_result["metadata"].get("year")
                context_year = citation_context.get("year")
                if doi_year and context_year and doi_year != context_year:
                    issues.append(f"Year mismatch: DOI shows {doi_year}, source is {context_year}")
            else:
                mechanism.citation_verified = False
                issues.append(f"DOI verification failed: {doi_result['error']}")
        else:
            mechanism.citation_verified = False
            issues.append("No DOI provided")

        # Check 2: Citation should match provided verified citation
        verified_citation = self._format_verified_citation(citation_context)
        if mechanism.primary_citation != verified_citation:
            issues.append("Primary citation doesn't match verified citation from literature search")

        # Set review flags
        mechanism.citation_issues = issues if issues else None
        mechanism.needs_manual_review = len(issues) > 0

        if issues:
            logger.warning(
                f"Citation issues for {mechanism.from_node_id}_to_{mechanism.to_node_id}: "
                f"{', '.join(issues)}"
            )

        return mechanism

    def mechanism_to_yaml(
        self,
        mechanism: MechanismExtraction,
        citation_context: Optional[Dict] = None
    ) -> str:
        """
        Convert mechanism to YAML with V2 citation validation metadata.

        Args:
            mechanism: Extracted mechanism
            citation_context: Optional citation context

        Returns:
            YAML string
        """
        mech_id = f"{mechanism.from_node_id}_to_{mechanism.to_node_id}"

        yaml_data = {
            "id": mech_id,
            "name": f"{mechanism.from_node_name} → {mechanism.to_node_name}",
            "from_node": {
                "node_id": mechanism.from_node_id,
                "node_name": mechanism.from_node_name
            },
            "to_node": {
                "node_id": mechanism.to_node_id,
                "node_name": mechanism.to_node_name
            },
            "direction": mechanism.direction,
            "category": mechanism.category,
            "mechanism_pathway": mechanism.mechanism_pathway,
            "evidence": {
                "quality_rating": mechanism.evidence_quality,
                "n_studies": mechanism.n_studies,
                "primary_citation": mechanism.primary_citation,
            },
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "version": "2.0",
            "description": mechanism.description
        }

        # Evidence metadata
        if mechanism.supporting_citations:
            yaml_data["evidence"]["supporting_citations"] = mechanism.supporting_citations
        if mechanism.doi:
            yaml_data["evidence"]["doi"] = mechanism.doi

        # V2: Citation validation metadata
        yaml_data["evidence"]["citation_verified"] = mechanism.citation_verified
        if mechanism.needs_manual_review:
            yaml_data["evidence"]["needs_manual_review"] = True
        if mechanism.citation_issues:
            yaml_data["evidence"]["citation_issues"] = mechanism.citation_issues

        # Quantitative effect data (CRITICAL - include when available)
        quantitative_data = {}
        if mechanism.effect_size_value is not None:
            quantitative_data["effect_size"] = {
                "value": mechanism.effect_size_value,
                "type": mechanism.effect_size_type
            }
            if mechanism.confidence_interval_lower is not None:
                quantitative_data["effect_size"]["ci_lower"] = mechanism.confidence_interval_lower
            if mechanism.confidence_interval_upper is not None:
                quantitative_data["effect_size"]["ci_upper"] = mechanism.confidence_interval_upper
        if mechanism.p_value is not None:
            quantitative_data["p_value"] = mechanism.p_value
        if mechanism.sample_size is not None:
            quantitative_data["sample_size"] = mechanism.sample_size
        if mechanism.heterogeneity_i_squared is not None:
            quantitative_data["heterogeneity_i_squared"] = mechanism.heterogeneity_i_squared
        if mechanism.heterogeneity_tau_squared is not None:
            quantitative_data["heterogeneity_tau_squared"] = mechanism.heterogeneity_tau_squared
        if mechanism.dose_response_trend is not None:
            quantitative_data["dose_response"] = {
                "trend": mechanism.dose_response_trend,
                "p_trend": mechanism.dose_response_p_trend
            }
        if mechanism.publication_bias_assessed:
            quantitative_data["publication_bias"] = {
                "assessed": True,
                "eggers_test_p": mechanism.eggers_test_p,
                "funnel_plot_asymmetry": mechanism.funnel_plot_asymmetry
            }

        if quantitative_data:
            yaml_data["quantitative_effects"] = quantitative_data

        # Spatial variation
        if mechanism.varies_by_geography:
            yaml_data["spatial_variation"] = {
                "varies_by_geography": True,
                "variation_notes": mechanism.variation_notes
            }

        # Moderators
        if mechanism.moderators:
            yaml_data["moderators"] = mechanism.moderators

        # Structural competency
        if mechanism.structural_competency_notes:
            yaml_data["structural_competency"] = {
                "equity_implications": mechanism.structural_competency_notes
            }

        # LLM metadata
        yaml_data["llm_metadata"] = {
            "extracted_by": self.model,
            "extraction_date": datetime.now().isoformat(),
            "extraction_confidence": mechanism.confidence,
            "prompt_version": self.prompt_version
        }

        return yaml.dump(
            yaml_data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100
        )

    def save_mechanism(
        self,
        mechanism: MechanismExtraction,
        output_dir: Path,
        citation_context: Optional[Dict] = None
    ) -> Path:
        """Save mechanism to YAML file"""
        mech_id = f"{mechanism.from_node_id}_to_{mechanism.to_node_id}"
        filename = f"{mech_id}.yml"

        category_dir = output_dir / mechanism.category
        category_dir.mkdir(parents=True, exist_ok=True)

        yaml_content = self.mechanism_to_yaml(mechanism, citation_context)

        file_path = category_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        status = "⚠️" if mechanism.needs_manual_review else "✅"
        logger.info(f"{status} Saved: {file_path}")

        return file_path


if __name__ == "__main__":
    # Test V2 with verified citation
    print("Testing LLM Discovery Pipeline V2 with Citation Verification")

    test_abstract = """Poor housing quality increases respiratory health risks in children.
    This study examined 1,200 families. Children in poor-quality housing had 1.8 times
    higher odds of asthma-related ED visits (95% CI: 1.4-2.3, p<0.001)."""

    test_title = "Housing Quality and Pediatric Asthma"

    # Simulate verified citation from literature search
    citation_context = {
        "authors": ["Smith, J.", "Jones, M.", "Brown, K."],
        "year": 2020,
        "doi": "10.1234/test.2020.001",
        "journal": "Journal of Public Health",
        "title": test_title
    }

    discovery = LLMMechanismDiscoveryV2(validate_citations=True)

    mechanisms = discovery.extract_mechanisms_from_paper(
        paper_abstract=test_abstract,
        paper_title=test_title,
        citation_context=citation_context
    )

    print(f"\n✅ Extracted {len(mechanisms)} mechanism(s)")

    for mech in mechanisms:
        print(f"\n{mech.from_node_name} → {mech.to_node_name}")
        print(f"Citation verified: {mech.citation_verified}")
        print(f"Needs review: {mech.needs_manual_review}")
        if mech.citation_issues:
            print(f"Issues: {mech.citation_issues}")
