"""
LLM Mechanism Discovery Pipeline (MVP)

This module implements the core LLM-based mechanism discovery pipeline for the MVP.
Focuses on topology and direction extraction, not quantification.

MVP Scope:
- Extract FROM node -> TO node relationships
- Determine direction (positive/negative)
- Identify qualitative moderators
- Extract evidence citations
- Flag spatial variation
- Ensure structural competency

Phase 2 (Future): Add effect size extraction and meta-analysis
"""

import anthropic
import json
import yaml
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from pydantic import BaseModel, Field


class MechanismExtraction(BaseModel):
    """Pydantic model for LLM-extracted mechanism data"""

    from_node_id: str = Field(description="Source node ID (snake_case)")
    from_node_name: str = Field(description="Human-readable source node name")
    to_node_id: str = Field(description="Target node ID (snake_case)")
    to_node_name: str = Field(description="Human-readable target node name")
    direction: str = Field(description="'positive' or 'negative'")
    category: str = Field(description="Primary category")
    mechanism_pathway: List[str] = Field(description="Step-by-step causal pathway")
    evidence_quality: str = Field(description="'A', 'B', 'C', or 'D'")
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

    # Quantitative metrics (extract when available)
    effect_size_value: Optional[float] = Field(default=None, description="Numeric effect size")
    effect_size_type: Optional[str] = Field(default=None, description="OR, RR, HR, beta, cohen_d, SMD, correlation, percentage, IRR, rate_ratio, prevalence_ratio, etc.")
    confidence_interval_lower: Optional[float] = Field(default=None)
    confidence_interval_upper: Optional[float] = Field(default=None)
    standard_error: Optional[float] = Field(default=None)
    p_value: Optional[float] = Field(default=None)
    sample_size: Optional[int] = Field(default=None)

    # Meta-analysis metrics
    heterogeneity_i_squared: Optional[float] = Field(default=None, description="I² for meta-analyses (0-100%)")
    heterogeneity_tau_squared: Optional[float] = Field(default=None, description="τ² between-study variance")
    cochrans_q: Optional[float] = Field(default=None, description="Cochran's Q test statistic")
    cochrans_q_p: Optional[float] = Field(default=None, description="P-value for Cochran's Q")

    # Dose-response / gradient
    dose_response_trend: Optional[str] = Field(default=None, description="linear, nonlinear, threshold, u_shaped, j_shaped")
    dose_response_p_trend: Optional[float] = Field(default=None, description="P-value for trend test")

    # Stratified/subgroup effects
    effect_varies_by_subgroup: Optional[bool] = Field(default=False)
    subgroup_heterogeneity_p: Optional[float] = Field(default=None, description="P-value for subgroup differences")

    # Sensitivity analyses
    sensitivity_analysis_performed: Optional[bool] = Field(default=False)
    sensitivity_analysis_notes: Optional[str] = Field(default=None)

    # Publication bias
    publication_bias_assessed: Optional[bool] = Field(default=False)
    eggers_test_p: Optional[float] = Field(default=None)
    funnel_plot_asymmetry: Optional[str] = Field(default=None, description="symmetric, asymmetric, insufficient_studies")

    # Effect magnitude interpretation (7-point Likert scale for unmeasured effects)
    effect_magnitude_likert: Optional[int] = Field(default=None, description="1-7 scale: 1=very_weak, 2=weak, 3=small, 4=moderate, 5=substantial, 6=large, 7=very_large")
    effect_magnitude_rationale: Optional[str] = Field(default=None, description="Explanation for Likert rating when quantitative data unavailable")

    # Additional statistical metrics
    adjusted_for_confounders: Optional[bool] = Field(default=None)
    confounders_adjusted: Optional[List[str]] = Field(default=None)
    causal_inference_method: Optional[str] = Field(default=None, description="IV, RDD, DiD, propensity_score, RCT, observational, etc.")


class LLMMechanismDiscovery:
    """
    LLM-based mechanism discovery pipeline for MVP.

    Uses Claude API to extract causal mechanisms from literature.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM discovery pipeline.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet model
        self.prompt_version = "1.0-mvp"

    def create_topology_extraction_prompt(
        self,
        paper_abstract: str,
        paper_title: str,
        focus_area: Optional[str] = None
    ) -> str:
        """
        Create prompt for extracting mechanism topology and direction from a paper.

        Args:
            paper_abstract: Abstract text from the paper
            paper_title: Title of the paper
            focus_area: Optional focus area (e.g., "housing to health")

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert in public health, epidemiology, and structural determinants of health. Your task is to extract causal mechanisms from scientific literature for a health equity decision support system.

**CRITICAL MVP SCOPE**: You are extracting TOPOLOGY and DIRECTION only. Do NOT extract quantitative effect sizes, odds ratios, or numerical estimates. Those are for Phase 2.

**Paper Title**: {paper_title}

**Paper Abstract**:
{paper_abstract}

---

## TASK

Extract ALL causal mechanisms described in this paper that relate structural/environmental factors to health outcomes. For EACH mechanism:

### 1. IDENTIFY NODES (FROM -> TO)
- **FROM node**: The upstream factor (policy, environment, economic condition, etc.)
- **TO node**: The downstream factor (health behavior, biological pathway, health outcome, etc.)
- Use clear, measurable constructs (e.g., "eviction_rate" not "housing instability")

### 2. DETERMINE DIRECTION
- **positive**: Increase in FROM -> Increase in TO
- **negative**: Increase in FROM -> Decrease in TO

### 3. DESCRIBE PATHWAY
- List 2-5 intermediate steps explaining HOW the mechanism operates
- Focus on structural and biological processes, NOT individual behaviors as blame

### 4. EXTRACT EVIDENCE (CONSERVATIVE GRADING)
- **Quality rating** (BE VERY CONSERVATIVE):
  - **A**: Meta-analysis with I²<50% (low heterogeneity) OR systematic review with 10+ high-quality studies showing consistent results
  - **B**: Systematic review with 5-9 studies OR meta-analysis with I²>50% OR multiple cohort studies (5-9) with consistent findings
  - **C**: 2-4 studies OR single high-quality cohort study OR mixed evidence
  - **D**: Single study OR case series OR inconsistent/conflicting evidence
- Number of studies supporting this mechanism in the paper
- Full Chicago-style citation with DOI if available

### 5. EXTRACT QUANTITATIVE DATA (Comprehensive - When Available)
Extract ALL statistical measures when present in the abstract:

**PRIMARY EFFECT METRICS:**
- **Effect size value** (the numeric estimate)
- **Effect size type**: OR, RR, HR, beta, SMD (standardized mean difference), correlation, IRR (incidence rate ratio), prevalence ratio, percentage change, etc.
- **Confidence interval**: Lower and upper bounds (typically 95% CI)
- **Standard error**: If reported
- **P-value**: Statistical significance level
- **Sample size**: Total N across studies (or in single study)

**META-ANALYSIS METRICS:**
- **I² statistic**: Heterogeneity percentage (0-100%)
- **τ² (tau-squared)**: Between-study variance
- **Cochran's Q**: Test statistic and p-value
- **Funnel plot**: Symmetric, asymmetric, or insufficient studies
- **Egger's test**: P-value if publication bias assessed

**DOSE-RESPONSE/GRADIENT:**
- **Trend type**: Linear, nonlinear, threshold, U-shaped, J-shaped
- **P for trend**: Statistical significance of dose-response

**SUBGROUP/EFFECT MODIFICATION:**
- **Varies by subgroup**: Yes/No
- **P for heterogeneity**: Test for subgroup differences

**STUDY DESIGN:**
- **Adjusted for confounders**: Yes/No + list of confounders
- **Causal inference method**: RCT, IV (instrumental variable), RDD (regression discontinuity), DiD (difference-in-differences), propensity score matching, observational cohort, etc.
- **Sensitivity analyses**: Were they performed? What did they show?

**7-POINT LIKERT SCALE (For Unmeasured Effects):**
When quantitative data is NOT available but the mechanism is described:
- **Rating 1-7**: Rate the expected effect magnitude
  - **1**: Very weak effect (minimal/negligible impact)
  - **2**: Weak effect (detectable but small)
  - **3**: Small effect (noticeable but limited)
  - **4**: Moderate effect (clearly meaningful)
  - **5**: Substantial effect (strong and important)
  - **6**: Large effect (major impact)
  - **7**: Very large effect (dominant or transformative)
- **Rationale**: Explain WHY you assigned this rating (based on mechanism plausibility, biological/social pathways described, etc.)

**Important**: Only extract quantitative data if explicitly stated. For unmeasured effects, use Likert scale based on qualitative description.

### 6. IDENTIFY MODERATORS (Qualitative only)
- Factors that strengthen or weaken the mechanism
- Rate strength as weak/moderate/strong
- Describe HOW the moderator operates

### 7. FLAG SPATIAL VARIATION
- Does the paper mention geographic variation?
- If yes, describe which contexts differ

### 8. STRUCTURAL COMPETENCY CHECK
- Does this mechanism trace to structural root causes (policy, economic systems, spatial arrangements)?
- Does it avoid blaming individuals for structural problems?
- What are the equity implications?

---

## OUTPUT FORMAT

Return a JSON array of mechanisms. Each mechanism should have this structure:

```json
{{
  "from_node_id": "snake_case_id",
  "from_node_name": "Human Readable Name",
  "to_node_id": "snake_case_id",
  "to_node_name": "Human Readable Name",
  "direction": "positive" or "negative",
  "category": "built_environment|social_environment|economic|political|healthcare_access|biological|behavioral",
  "mechanism_pathway": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "evidence_quality": "A|B|C|D",
  "n_studies": <number>,
  "primary_citation": "Full Chicago-style citation",
  "supporting_citations": ["citation 1", "citation 2"],
  "doi": "10.xxxx/xxxxx",
  "varies_by_geography": true|false,
  "variation_notes": "Description of geographic variation if applicable",
  "moderators": [
    {{
      "name": "moderator_name",
      "direction": "strengthens|weakens|u_shaped",
      "strength": "weak|moderate|strong",
      "description": "How the moderator operates"
    }}
  ],
  "description": "Detailed description of the mechanism",
  "structural_competency_notes": "How this mechanism relates to structural determinants and equity",
  "confidence": "high|medium|low",
  "effect_size_value": <number or null>,
  "effect_size_type": "OR|RR|HR|beta|cohen_d|correlation|percentage|null",
  "confidence_interval_lower": <number or null>,
  "confidence_interval_upper": <number or null>,
  "p_value": <number or null>,
  "sample_size": <number or null>,
  "heterogeneity_i_squared": <number 0-100 or null>
}}
```

---

## STRUCTURAL COMPETENCY GUIDELINES

**PRIORITIZE mechanisms that:**
- Trace to policy, economic systems, or spatial arrangements
- Explain HOW structural factors produce health inequities
- Avoid individual-level blame (e.g., "poor health behaviors")
- Focus on root causes, not proximate symptoms

**AVOID mechanisms that:**
- Blame individuals for structural problems
- Medicalize social issues
- Ignore power, racism, or economic exploitation

**EQUITY LENS**:
- Always note if effects differ by race, class, gender, or other axes of inequality
- Explain HOW structural inequities create differential exposure or vulnerability

---

## EXAMPLES

**GOOD** (Structural, equity-focused):
```json
{{
  "from_node_id": "eviction_rate",
  "from_node_name": "Eviction Rate (per 100 renter households)",
  "to_node_id": "emergency_department_utilization",
  "to_node_name": "Emergency Department Utilization Rate",
  "direction": "positive",
  "category": "economic",
  "mechanism_pathway": [
    "Step 1: Eviction forces immediate housing displacement",
    "Step 2: Disrupts continuity with primary care providers (geographic dislocation)",
    "Step 3: Loss of health insurance due to job loss or Medicaid address changes",
    "Step 4: Unmet chronic disease needs escalate to emergency crises",
    "Step 5: Increased ED utilization for conditions manageable in primary care"
  ],
  "evidence_quality": "B",
  "n_studies": 4,
  "primary_citation": "Desmond, Matthew, and Rachel Tolbert Kimbro. 2015. 'Eviction's Fallout: Housing, Hardship, and Health.' Social Forces 94 (1): 295–324. https://doi.org/10.1093/sf/sov044",
  "doi": "10.1093/sf/sov044",
  "varies_by_geography": true,
  "variation_notes": "Effect stronger in states without Medicaid expansion (insurance loss more likely) and cities with low rental assistance availability",
  "moderators": [
    {{
      "name": "medicaid_expansion_status",
      "direction": "weakens",
      "strength": "moderate",
      "description": "Medicaid expansion states maintain coverage continuity despite address changes, reducing insurance loss"
    }},
    {{
      "name": "rental_assistance_availability",
      "direction": "weakens",
      "strength": "strong",
      "description": "Robust rental assistance programs prevent eviction cascades in the first place"
    }}
  ],
  "description": "Eviction creates healthcare discontinuity through forced geographic displacement and insurance loss, increasing reliance on emergency departments for primary care-manageable conditions.",
  "structural_competency_notes": "This mechanism demonstrates how housing policy failure (weak tenant protections, insufficient rental assistance) creates health system strain. Eviction is a policy choice, not an individual failure. Equity implication: Black renters face 2-3x higher eviction rates due to residential segregation and wage inequality.",
  "confidence": "high"
}}
```

**BAD** (Individual blame, not structural):
```json
{{
  "from_node_id": "poor_health_literacy",
  "from_node_name": "Poor Health Literacy",
  "to_node_id": "diabetes_control",
  "to_node_name": "Diabetes Control",
  "direction": "negative",
  // ... REJECT THIS - blames individuals, ignores structural determinants of literacy
}}
```

---

Now extract ALL mechanisms from the provided paper. Return ONLY valid JSON, no additional text.
"""

        if focus_area:
            prompt += f"\n\n**FOCUS AREA**: Prioritize mechanisms related to {focus_area}"

        return prompt

    def extract_mechanisms_from_paper(
        self,
        paper_abstract: str,
        paper_title: str,
        focus_area: Optional[str] = None,
        max_tokens: int = 4000
    ) -> List[MechanismExtraction]:
        """
        Extract mechanisms from a single paper using Claude.

        Args:
            paper_abstract: Abstract text
            paper_title: Title of the paper
            focus_area: Optional focus area
            max_tokens: Maximum tokens for response

        Returns:
            List of extracted mechanisms
        """
        prompt = self.create_topology_extraction_prompt(
            paper_abstract,
            paper_title,
            focus_area
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = response.content[0].text

            # Try to parse JSON
            try:
                mechanisms_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Sometimes Claude wraps JSON in markdown code blocks
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                    mechanisms_data = json.loads(response_text)
                else:
                    raise

            # Validate with Pydantic
            mechanisms = []
            if isinstance(mechanisms_data, list):
                for mech_data in mechanisms_data:
                    mechanisms.append(MechanismExtraction(**mech_data))
            else:
                # Single mechanism returned
                mechanisms.append(MechanismExtraction(**mechanisms_data))

            return mechanisms

        except Exception as e:
            print(f"Error extracting mechanisms: {e}")
            raise

    def mechanism_to_yaml(
        self,
        mechanism: MechanismExtraction,
        citation_context: Optional[Dict] = None
    ) -> str:
        """
        Convert extracted mechanism to YAML format for mechanism bank.

        Args:
            mechanism: Extracted mechanism data
            citation_context: Optional additional citation context

        Returns:
            YAML string
        """
        # Generate mechanism ID
        mech_id = f"{mechanism.from_node_id}_to_{mechanism.to_node_id}"

        # Build YAML structure
        yaml_data = {
            "id": mech_id,
            "name": f"{mechanism.from_node_name} -> {mechanism.to_node_name}",
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
            "effect_quantification": {},
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "description": mechanism.description
        }

        # Add optional fields
        if mechanism.supporting_citations:
            yaml_data["evidence"]["supporting_citations"] = mechanism.supporting_citations

        if mechanism.doi:
            yaml_data["evidence"]["doi"] = mechanism.doi

        if mechanism.varies_by_geography:
            yaml_data["spatial_variation"] = {
                "varies_by_geography": True,
                "variation_notes": mechanism.variation_notes
            }

        if mechanism.moderators:
            yaml_data["moderators"] = mechanism.moderators

        # Add quantitative metrics if available
        quant = {}

        # Primary effect metrics
        if mechanism.effect_size_value is not None:
            quant["effect_size"] = {
                "value": mechanism.effect_size_value,
                "type": mechanism.effect_size_type
            }
            if mechanism.confidence_interval_lower is not None:
                quant["effect_size"]["ci_lower"] = mechanism.confidence_interval_lower
            if mechanism.confidence_interval_upper is not None:
                quant["effect_size"]["ci_upper"] = mechanism.confidence_interval_upper
            if mechanism.standard_error is not None:
                quant["effect_size"]["standard_error"] = mechanism.standard_error
            if mechanism.p_value is not None:
                quant["effect_size"]["p_value"] = mechanism.p_value

        if mechanism.sample_size is not None:
            quant["sample_size"] = mechanism.sample_size

        # Meta-analysis metrics
        if any([mechanism.heterogeneity_i_squared, mechanism.heterogeneity_tau_squared, mechanism.cochrans_q]):
            quant["meta_analysis"] = {}
            if mechanism.heterogeneity_i_squared is not None:
                quant["meta_analysis"]["i_squared"] = mechanism.heterogeneity_i_squared
            if mechanism.heterogeneity_tau_squared is not None:
                quant["meta_analysis"]["tau_squared"] = mechanism.heterogeneity_tau_squared
            if mechanism.cochrans_q is not None:
                quant["meta_analysis"]["cochrans_q"] = mechanism.cochrans_q
            if mechanism.cochrans_q_p is not None:
                quant["meta_analysis"]["cochrans_q_p"] = mechanism.cochrans_q_p

        # Dose-response
        if mechanism.dose_response_trend:
            quant["dose_response"] = {
                "trend": mechanism.dose_response_trend
            }
            if mechanism.dose_response_p_trend is not None:
                quant["dose_response"]["p_trend"] = mechanism.dose_response_p_trend

        # Subgroup effects
        if mechanism.effect_varies_by_subgroup:
            quant["subgroup_effects"] = {
                "varies": True
            }
            if mechanism.subgroup_heterogeneity_p is not None:
                quant["subgroup_effects"]["p_heterogeneity"] = mechanism.subgroup_heterogeneity_p

        # Sensitivity analysis
        if mechanism.sensitivity_analysis_performed:
            quant["sensitivity_analysis"] = {
                "performed": True,
                "notes": mechanism.sensitivity_analysis_notes
            }

        # Publication bias
        if mechanism.publication_bias_assessed:
            quant["publication_bias"] = {
                "assessed": True
            }
            if mechanism.eggers_test_p is not None:
                quant["publication_bias"]["eggers_p"] = mechanism.eggers_test_p
            if mechanism.funnel_plot_asymmetry:
                quant["publication_bias"]["funnel_asymmetry"] = mechanism.funnel_plot_asymmetry

        # Effect magnitude Likert scale (for unmeasured effects)
        if mechanism.effect_magnitude_likert is not None:
            quant["effect_magnitude_proxy"] = {
                "likert_scale": mechanism.effect_magnitude_likert,
                "interpretation": {
                    1: "very_weak",
                    2: "weak",
                    3: "small",
                    4: "moderate",
                    5: "substantial",
                    6: "large",
                    7: "very_large"
                }.get(mechanism.effect_magnitude_likert, "unknown"),
                "rationale": mechanism.effect_magnitude_rationale
            }

        # Study design
        if mechanism.adjusted_for_confounders is not None:
            quant["study_design"] = {
                "adjusted_for_confounders": mechanism.adjusted_for_confounders
            }
            if mechanism.confounders_adjusted:
                quant["study_design"]["confounders"] = mechanism.confounders_adjusted
            if mechanism.causal_inference_method:
                quant["study_design"]["method"] = mechanism.causal_inference_method

        # Only add effect_quantification if we have data
        if quant:
            yaml_data["effect_quantification"] = quant
        else:
            del yaml_data["effect_quantification"]

        if mechanism.structural_competency_notes:
            yaml_data["structural_competency"] = {
                "equity_implications": mechanism.structural_competency_notes
            }

        # Add LLM metadata
        yaml_data["llm_metadata"] = {
            "extracted_by": self.model,
            "extraction_date": datetime.now().isoformat(),
            "extraction_confidence": mechanism.confidence,
            "prompt_version": self.prompt_version
        }

        # Convert to YAML with proper formatting
        yaml_str = yaml.dump(
            yaml_data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100
        )

        return yaml_str

    def save_mechanism(
        self,
        mechanism: MechanismExtraction,
        output_dir: Path,
        citation_context: Optional[Dict] = None
    ) -> Path:
        """
        Save extracted mechanism to YAML file in mechanism bank.

        Args:
            mechanism: Extracted mechanism
            output_dir: Directory to save mechanism files
            citation_context: Optional citation context

        Returns:
            Path to saved file
        """
        # Generate filename
        mech_id = f"{mechanism.from_node_id}_to_{mechanism.to_node_id}"
        filename = f"{mech_id}.yml"

        # Create category subdirectory
        category_dir = output_dir / mechanism.category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Convert to YAML
        yaml_content = self.mechanism_to_yaml(mechanism, citation_context)

        # Save file
        file_path = category_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        print(f"[OK] Saved mechanism: {file_path}")
        return file_path


def test_extraction():
    """Test function demonstrating the LLM discovery pipeline"""

    # Example paper abstract (housing -> health)
    test_abstract = """
    Poor housing quality is a major determinant of respiratory health, particularly among
    low-income populations. This study examines the relationship between housing conditions
    and asthma morbidity in an urban sample of 1,200 families. We measured housing quality
    through standardized home inspections assessing dampness, mold, ventilation, and pest
    infestation. Asthma outcomes included symptom frequency, emergency department visits,
    and missed school days. After controlling for socioeconomic factors, children in poor-quality
    housing had 1.8 times higher odds of asthma-related ED visits (95% CI: 1.4-2.3). The
    relationship was partially mediated by indoor air quality measurements. Effects were
    strongest in older buildings and humid climates. Interventions targeting housing code
    enforcement and remediation funds significantly reduced asthma morbidity.
    """

    test_title = "Housing Quality and Pediatric Asthma: A Longitudinal Study"

    # Initialize pipeline
    discovery = LLMMechanismDiscovery()

    # Extract mechanisms
    mechanisms = discovery.extract_mechanisms_from_paper(
        paper_abstract=test_abstract,
        paper_title=test_title,
        focus_area="housing to health"
    )

    # Print results
    print(f"\n[OK] Extracted {len(mechanisms)} mechanism(s):\n")
    for i, mech in enumerate(mechanisms, 1):
        print(f"\n--- Mechanism {i} ---")
        print(f"FROM: {mech.from_node_name}")
        print(f"TO: {mech.to_node_name}")
        print(f"Direction: {mech.direction}")
        print(f"Confidence: {mech.confidence}")
        print(f"Evidence Quality: {mech.evidence_quality} ({mech.n_studies} studies)")

        # Save to mechanism bank
        output_dir = Path("../../mechanism-bank/mechanisms")
        if output_dir.exists():
            file_path = discovery.save_mechanism(mech, output_dir)
            print(f"Saved to: {file_path}")


def validate_structural_competency(mechanism: dict, confidence_threshold: float = 0.7) -> dict:
    """
    Validate mechanism using LLM confidence scoring.

    Returns:
        dict with 'valid': bool, 'confidence': float, 'issues': List[str]
    """

    # Check 1: Category alignment
    category_score = check_category_alignment(mechanism)

    # Check 2: Scale consistency
    scale_score = check_scale_consistency(mechanism)

    # Check 3: Evidence quality
    evidence_score = check_evidence_plausibility(mechanism)

    # Aggregate
    overall_confidence = (category_score + scale_score + evidence_score) / 3

    issues = []
    if category_score < 0.6:
        issues.append("Category may not match mechanism type")
    if scale_score < 0.6:
        issues.append("Scale levels may be inconsistent with causal distance")
    if evidence_score < 0.6:
        issues.append("Evidence quality rating seems inconsistent with study count")

    return {
        'valid': overall_confidence >= confidence_threshold and len(issues) == 0,
        'confidence': overall_confidence,
        'category_score': category_score,
        'scale_score': scale_score,
        'evidence_score': evidence_score,
        'issues': issues
    }


def check_category_alignment(mechanism: dict) -> float:
    """
    Check if mechanism category aligns with node types.

    Returns confidence score [0, 1]
    """
    category = mechanism.get('category', '')
    from_node = mechanism.get('from_node_id', '')
    to_node = mechanism.get('to_node_id', '')

    # Infer categories from node names
    from_category = infer_node_category(from_node)
    to_category = infer_node_category(to_node)

    # Simple heuristic: category should match one of the node categories
    if category in [from_category, to_category]:
        return 1.0
    elif is_related_category(category, from_category) or is_related_category(category, to_category):
        return 0.7
    else:
        return 0.3


def infer_node_category(node_id: str) -> str:
    """
    Infer category from node ID based on keywords.

    Args:
        node_id: Node identifier (e.g., "housing_quality", "obesity")

    Returns:
        Inferred category
    """
    node_lower = node_id.lower()

    # Keyword mapping
    category_keywords = {
        'built_environment': ['housing', 'neighborhood', 'built', 'walkability', 'park', 'transportation', 'urban'],
        'social_environment': ['social', 'discrimination', 'stigma', 'isolation', 'support', 'violence'],
        'economic': ['income', 'poverty', 'employment', 'wage', 'economic', 'financial', 'insurance'],
        'political': ['policy', 'law', 'regulation', 'taxation', 'government'],
        'healthcare_access': ['healthcare', 'treatment', 'medical', 'hospital', 'insurance', 'medicaid'],
        'biological': ['inflammatory', 'metabolic', 'immune', 'hormonal', 'genetic', 'biological'],
        'behavioral': ['diet', 'physical_activity', 'smoking', 'alcohol', 'exercise', 'sedentary']
    }

    for category, keywords in category_keywords.items():
        if any(keyword in node_lower for keyword in keywords):
            return category

    return 'unknown'


def is_related_category(cat1: str, cat2: str) -> bool:
    """
    Check if two categories are related/compatible.

    Args:
        cat1, cat2: Category names

    Returns:
        True if categories are related
    """
    # Define related category pairs
    related_pairs = [
        ('built_environment', 'social_environment'),
        ('built_environment', 'behavioral'),
        ('economic', 'social_environment'),
        ('economic', 'healthcare_access'),
        ('social_environment', 'behavioral'),
        ('healthcare_access', 'biological'),
        ('behavioral', 'biological')
    ]

    # Check both directions
    return (cat1, cat2) in related_pairs or (cat2, cat1) in related_pairs


def check_scale_consistency(mechanism: dict) -> float:
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

    # Infer scales from node names (placeholder logic)
    from_scale = infer_scale_from_node(from_node)
    to_scale = infer_scale_from_node(to_node)

    if from_scale is None or to_scale is None:
        return 0.5  # Neutral if we can't determine

    # Check if causal direction makes sense (upstream -> downstream)
    if from_scale <= to_scale:
        # Good: structural/upstream factors -> downstream outcomes
        return 1.0
    elif from_scale == to_scale + 1:
        # Acceptable: adjacent levels
        return 0.8
    else:
        # Problematic: downstream -> upstream (reverse causality?)
        return 0.3


def infer_scale_from_node(node_id: str) -> Optional[int]:
    """
    Infer scale level from node ID.

    Returns:
        Scale level (1-7) or None if cannot determine
    """
    node_lower = node_id.lower()

    # Keywords for each scale
    scale_keywords = {
        1: ['policy', 'law', 'regulation', 'taxation', 'legislation'],
        2: ['built', 'environment', 'housing', 'neighborhood', 'urban', 'walkability'],
        3: ['institutional', 'healthcare_system', 'school', 'workplace'],
        4: ['poverty', 'employment', 'income', 'education', 'insurance'],
        5: ['behavior', 'diet', 'physical_activity', 'smoking', 'alcohol', 'adherence'],
        6: ['inflammation', 'metabolic', 'blood_pressure', 'cholesterol', 'stress'],
        7: ['disease', 'mortality', 'hospitalization', 'crisis', 'death', 'stroke', 'heart_failure']
    }

    for scale, keywords in scale_keywords.items():
        if any(keyword in node_lower for keyword in keywords):
            return scale

    return None


def check_evidence_plausibility(mechanism: dict) -> float:
    """
    Check if evidence quality rating is plausible given study count.

    Returns confidence score [0, 1]
    """
    quality = mechanism.get('evidence_quality', 'D')
    n_studies = mechanism.get('n_studies', 0)

    # Expected study counts for each quality grade
    expected_ranges = {
        'A': (10, 100),   # Meta-analysis with many studies
        'B': (5, 20),     # Systematic review or multiple cohorts
        'C': (2, 8),      # Few studies
        'D': (1, 3)       # Single study or weak evidence
    }

    if quality not in expected_ranges:
        return 0.5

    min_expected, max_expected = expected_ranges[quality]

    if min_expected <= n_studies <= max_expected:
        return 1.0
    elif n_studies < min_expected:
        # Fewer studies than expected for this quality grade
        return 0.6
    else:
        # More studies than expected (possibly good, but grade might be conservative)
        return 0.8


if __name__ == "__main__":
    test_extraction()
