"""
Functional Form Classifier

Automatically assigns functional forms to mechanisms based on:
- Mechanism description and characteristics
- Node types and scale levels
- Evidence patterns from literature
- Systems dynamics principles

Supports functional forms from 05_MECHANISM_BANK_STRUCTURE.md:
- sigmoid: Saturation effects (e.g., diminishing returns)
- threshold: Step functions (e.g., policy effects kick in at minimum level)
- logarithmic: Log transformations (e.g., income effects)
- multiplicative_dampening: Stock-dependent dampening
- linear: Simple linear relationships
"""

import anthropic
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class FunctionalFormAssignment:
    """Result of functional form classification."""
    form: str  # sigmoid, threshold, logarithmic, multiplicative_dampening, linear
    confidence: float  # 0-1
    reasoning: str
    suggested_parameters: Dict[str, any]
    alternative_forms: List[Tuple[str, float]]  # [(form, confidence), ...]


class FunctionalFormClassifier:
    """
    Classifies mechanisms into functional forms for Systems Dynamics.

    Uses LLM + heuristics to determine appropriate functional form
    based on mechanism characteristics.
    """

    FUNCTIONAL_FORMS = {
        'sigmoid': {
            'description': 'Saturation effect with diminishing returns',
            'equation': 'ΔStock_j = alpha × (L / (1 + exp(-k × (Stock_i - x0))))',
            'parameters': ['alpha', 'L', 'k', 'x0'],
            'typical_use_cases': [
                'Dose-response relationships',
                'Capacity saturation',
                'Behavioral change adoption',
                'Resource allocation with limits',
                'Treatment effectiveness plateaus'
            ]
        },
        'threshold': {
            'description': 'Step function with minimum activation level',
            'equation': 'ΔStock_j = alpha × max(0, Stock_i - threshold)',
            'parameters': ['alpha', 'threshold'],
            'typical_use_cases': [
                'Policy effects requiring minimum compliance',
                'Tipping points',
                'All-or-nothing phenomena',
                'Minimum effective dose',
                'Regulatory thresholds'
            ]
        },
        'logarithmic': {
            'description': 'Logarithmic relationship (each unit increase has smaller effect)',
            'equation': 'ΔStock_j = alpha × log(Stock_i + 1)',
            'parameters': ['alpha'],
            'typical_use_cases': [
                'Income/wealth effects',
                'Marginal utility',
                'Weber-Fechner law (perception)',
                'Population density effects',
                'Accumulation with decreasing marginal impact'
            ]
        },
        'multiplicative_dampening': {
            'description': 'Effect dampened by current level of outcome',
            'equation': 'ΔStock_j = alpha × Stock_i × (1 - Stock_j / Max_Stock_j)',
            'parameters': ['alpha', 'Max_Stock_j'],
            'typical_use_cases': [
                'Prevalence-limited spread',
                'Feedback loops',
                'Self-limiting growth',
                'Ceiling effects',
                'Resource depletion'
            ]
        },
        'linear': {
            'description': 'Simple linear relationship (constant marginal effect)',
            'equation': 'ΔStock_j = alpha × Stock_i',
            'parameters': ['alpha'],
            'typical_use_cases': [
                'Direct proportional effects',
                'Small-range approximations',
                'Well-controlled interventions',
                'Mechanical/physical relationships',
                'When no saturation expected'
            ]
        }
    }

    def __init__(self, anthropic_api_key: Optional[str] = None):
        """Initialize classifier with API key."""
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def classify(
        self,
        mechanism: Dict,
        verbose: bool = False
    ) -> FunctionalFormAssignment:
        """
        Classify mechanism into appropriate functional form.

        Args:
            mechanism: Mechanism dictionary (from YAML or extraction)
            verbose: Print progress

        Returns:
            FunctionalFormAssignment with form, confidence, reasoning
        """
        if verbose:
            from_node = mechanism.get('from_node_id', 'unknown')
            to_node = mechanism.get('to_node_id', 'unknown')
            print(f"\nClassifying: {from_node} → {to_node}")

        # Build prompt for LLM
        prompt = self._build_classification_prompt(mechanism)

        try:
            response = self.client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=1500,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            # Parse LLM response
            assignment = self._parse_classification_response(response_text, mechanism)

            if verbose:
                print(f"  Form: {assignment.form} (confidence: {assignment.confidence:.2f})")
                print(f"  Reasoning: {assignment.reasoning[:100]}...")

            return assignment

        except Exception as e:
            print(f"Error in classification: {e}")
            # Default to linear as fallback
            return FunctionalFormAssignment(
                form='linear',
                confidence=0.3,
                reasoning=f"Classification failed: {e}. Defaulting to linear.",
                suggested_parameters={'alpha': mechanism.get('effect_size', 0.5)},
                alternative_forms=[]
            )

    def _build_classification_prompt(self, mechanism: Dict) -> str:
        """Build prompt for LLM classification."""

        # Extract mechanism details
        from_node = mechanism.get('from_node_id', 'unknown')
        to_node = mechanism.get('to_node_id', 'unknown')
        description = mechanism.get('description', 'No description')
        category = mechanism.get('category', 'unknown')
        from_scale = mechanism.get('from_scale', 0)
        to_scale = mechanism.get('to_scale', 0)
        effect_size = mechanism.get('effect_size', 'N/A')
        evidence_quality = mechanism.get('evidence_quality', 'N/A')

        # Build functional forms reference
        forms_reference = ""
        for form_name, form_info in self.FUNCTIONAL_FORMS.items():
            forms_reference += f"\n### {form_name.upper()}\n"
            forms_reference += f"**Description**: {form_info['description']}\n"
            forms_reference += f"**Equation**: `{form_info['equation']}`\n"
            forms_reference += f"**Typical use cases**:\n"
            for use_case in form_info['typical_use_cases']:
                forms_reference += f"  - {use_case}\n"

        prompt = f"""You are a systems dynamics expert classifying health mechanisms into functional forms.

## Mechanism to Classify

- **From Node**: {from_node} (scale level: {from_scale})
- **To Node**: {to_node} (scale level: {to_scale})
- **Category**: {category}
- **Description**: {description}
- **Effect Size**: {effect_size}
- **Evidence Quality**: {evidence_quality}

## Available Functional Forms
{forms_reference}

## Classification Guidelines

1. **Consider Saturation**: Does the effect plateau at high levels of exposure?
   → If yes, consider **sigmoid** or **multiplicative_dampening**

2. **Consider Thresholds**: Does the effect only kick in after a minimum level?
   → If yes, consider **threshold**

3. **Consider Marginal Effects**: Does each additional unit have less impact?
   → If yes, consider **logarithmic** or **sigmoid**

4. **Consider Feedback**: Does the current level of outcome affect future changes?
   → If yes, consider **multiplicative_dampening**

5. **Consider Simplicity**: If no clear nonlinearity, prefer **linear**

## Scale Level Hints

- **Structural (1-3) → Individual (4-5)**: Often logarithmic (e.g., income effects)
- **Behavioral (5) → Outcomes (6-7)**: Often sigmoid (dose-response)
- **Policy (3) → Outcomes**: Often threshold (minimum policy strength)
- **Prevalence/Population**: Often multiplicative_dampening (saturation)

## Output Format

Provide your classification in this exact JSON format:

```json
{{
  "primary_form": "sigmoid" | "threshold" | "logarithmic" | "multiplicative_dampening" | "linear",
  "confidence": 0.85,
  "reasoning": "Brief explanation (2-3 sentences) of why this form fits best",
  "suggested_parameters": {{
    "alpha": 0.35,
    "L": 1.0,
    "k": 0.15,
    "x0": 150
    // Include parameters relevant to chosen form
  }},
  "alternative_forms": [
    {{"form": "logarithmic", "confidence": 0.65, "reason": "Could also fit if..."}},
    {{"form": "linear", "confidence": 0.40, "reason": "Simple approximation"}}
  ]
}}
```

**Important**:
- Base `alpha` on the effect_size from the mechanism ({effect_size})
- Suggest reasonable defaults for other parameters
- List 1-2 alternative forms with lower confidence
"""

        return prompt

    def _parse_classification_response(
        self,
        response_text: str,
        mechanism: Dict
    ) -> FunctionalFormAssignment:
        """Parse LLM response into FunctionalFormAssignment."""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[json_start:json_end]
            parsed = json.loads(json_str)

            primary_form = parsed.get('primary_form', 'linear')
            confidence = float(parsed.get('confidence', 0.5))
            reasoning = parsed.get('reasoning', 'No reasoning provided')
            suggested_parameters = parsed.get('suggested_parameters', {})
            alternative_forms_raw = parsed.get('alternative_forms', [])

            # Parse alternative forms
            alternative_forms = []
            for alt in alternative_forms_raw:
                alt_form = alt.get('form', '')
                alt_conf = float(alt.get('confidence', 0.0))
                alternative_forms.append((alt_form, alt_conf))

            return FunctionalFormAssignment(
                form=primary_form,
                confidence=confidence,
                reasoning=reasoning,
                suggested_parameters=suggested_parameters,
                alternative_forms=alternative_forms
            )

        except Exception as e:
            print(f"Error parsing classification response: {e}")
            # Fallback to linear
            effect_size = mechanism.get('effect_size', 0.5)
            return FunctionalFormAssignment(
                form='linear',
                confidence=0.3,
                reasoning=f"Parse error: {e}. Defaulting to linear.",
                suggested_parameters={'alpha': effect_size if effect_size != 'N/A' else 0.5},
                alternative_forms=[]
            )

    def classify_batch(
        self,
        mechanisms: List[Dict],
        verbose: bool = True
    ) -> List[Tuple[Dict, FunctionalFormAssignment]]:
        """
        Classify multiple mechanisms.

        Args:
            mechanisms: List of mechanism dictionaries
            verbose: Print progress

        Returns:
            List of (mechanism, assignment) tuples
        """
        results = []

        if verbose:
            print(f"\n=== Classifying {len(mechanisms)} Mechanisms ===\n")

        for i, mech in enumerate(mechanisms, 1):
            if verbose:
                print(f"[{i}/{len(mechanisms)}]", end=" ")

            assignment = self.classify(mech, verbose=verbose)
            results.append((mech, assignment))

        # Print summary
        if verbose:
            print(f"\n=== Classification Summary ===")
            form_counts = {}
            for _, assignment in results:
                form_counts[assignment.form] = form_counts.get(assignment.form, 0) + 1

            for form, count in sorted(form_counts.items(), key=lambda x: x[1], reverse=True):
                pct = 100 * count / len(mechanisms)
                print(f"  {form}: {count} ({pct:.1f}%)")

            avg_confidence = sum(a.confidence for _, a in results) / len(results)
            print(f"\nAverage confidence: {avg_confidence:.2f}")

        return results

    def apply_to_mechanism(
        self,
        mechanism: Dict,
        assignment: FunctionalFormAssignment,
        overwrite: bool = False
    ) -> Dict:
        """
        Apply functional form assignment to mechanism dictionary.

        Args:
            mechanism: Mechanism dictionary
            assignment: FunctionalFormAssignment
            overwrite: Overwrite existing functional_form if present

        Returns:
            Updated mechanism dictionary
        """
        if 'functional_form' in mechanism and not overwrite:
            print(f"Warning: Mechanism already has functional_form. Use overwrite=True to replace.")
            return mechanism

        # Add functional form info
        form_info = self.FUNCTIONAL_FORMS[assignment.form]

        mechanism['functional_form'] = assignment.form
        mechanism['equation'] = form_info['equation']
        mechanism['parameters'] = {}

        # Add suggested parameters
        for param_name, param_value in assignment.suggested_parameters.items():
            mechanism['parameters'][param_name] = {
                'value': param_value,
                'description': f"Auto-assigned by classifier (confidence: {assignment.confidence:.2f})",
                'source': 'Functional form classifier'
            }

        # Add metadata
        mechanism['functional_form_metadata'] = {
            'classifier_confidence': assignment.confidence,
            'reasoning': assignment.reasoning,
            'alternative_forms': [
                {'form': form, 'confidence': conf}
                for form, conf in assignment.alternative_forms
            ]
        }

        return mechanism


def test_classifier():
    """Test functional form classifier."""
    print("=== Testing Functional Form Classifier ===\n")

    # Sample mechanisms with different characteristics
    sample_mechanisms = [
        {
            'from_node_id': 'income',
            'to_node_id': 'health_outcomes',
            'from_scale': 1,
            'to_scale': 7,
            'category': 'economic',
            'description': 'Higher income improves health outcomes through better access to healthcare, nutrition, and reduced stress. Effect diminishes at very high income levels.',
            'effect_size': 0.25,
            'evidence_quality': 'A'
        },
        {
            'from_node_id': 'minimum_wage_policy',
            'to_node_id': 'poverty_rate',
            'from_scale': 3,
            'to_scale': 4,
            'category': 'policy',
            'description': 'Minimum wage increases reduce poverty only when set above a threshold level (living wage). Below this threshold, effects are minimal.',
            'effect_size': -0.15,
            'evidence_quality': 'B'
        },
        {
            'from_node_id': 'physical_activity',
            'to_node_id': 'cardiovascular_health',
            'from_scale': 5,
            'to_scale': 6,
            'category': 'behavioral',
            'description': 'Exercise improves cardiovascular health with dose-response relationship. Benefits plateau at high exercise levels (saturation effect).',
            'effect_size': 0.42,
            'evidence_quality': 'A'
        },
        {
            'from_node_id': 'vaccination_coverage',
            'to_node_id': 'disease_prevalence',
            'from_scale': 3,
            'to_scale': 7,
            'category': 'healthcare_access',
            'description': 'Vaccination programs reduce disease prevalence. Effect dampened as more of the population is already immune (multiplicative dampening).',
            'effect_size': -0.68,
            'evidence_quality': 'A'
        }
    ]

    # Initialize classifier
    classifier = FunctionalFormClassifier()

    # Classify
    results = classifier.classify_batch(sample_mechanisms, verbose=True)

    print("\n=== Detailed Results ===\n")
    for mech, assignment in results:
        print(f"Mechanism: {mech['from_node_id']} → {mech['to_node_id']}")
        print(f"  Functional Form: {assignment.form}")
        print(f"  Confidence: {assignment.confidence:.2f}")
        print(f"  Reasoning: {assignment.reasoning}")
        print(f"  Parameters: {assignment.suggested_parameters}")
        if assignment.alternative_forms:
            print(f"  Alternatives: {assignment.alternative_forms}")
        print()


if __name__ == "__main__":
    test_classifier()
