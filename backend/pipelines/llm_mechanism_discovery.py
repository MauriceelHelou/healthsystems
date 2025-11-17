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
    evidence_quality: str = Field(description="'A', 'B', or 'C'")
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

### 4. EXTRACT EVIDENCE
- Quality rating: A (meta-analysis or 5+ studies), B (3-4 studies), C (1-2 studies)
- Number of studies supporting this mechanism in the paper
- Full Chicago-style citation with DOI if available

### 5. IDENTIFY MODERATORS (Qualitative only)
- Factors that strengthen or weaken the mechanism
- Rate strength as weak/moderate/strong
- Describe HOW the moderator operates

### 6. FLAG SPATIAL VARIATION
- Does the paper mention geographic variation?
- If yes, describe which contexts differ

### 7. STRUCTURAL COMPETENCY CHECK
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
  "evidence_quality": "A|B|C",
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
  "confidence": "high|medium|low"
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


if __name__ == "__main__":
    test_extraction()
