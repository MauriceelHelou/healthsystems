"""
Quick test of the LLM mechanism discovery with a single abstract.
This bypasses literature search to test just the extraction.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

from llm_mechanism_discovery import LLMMechanismDiscovery

# Test abstract about housing and health
test_abstract = """
Housing quality represents a critical social determinant of health, particularly
for respiratory outcomes in urban children. This longitudinal study examined 1,200
low-income families across multiple cities. Housing quality assessments included
standardized inspections measuring dampness, mold growth, ventilation adequacy,
and pest infestation levels. Primary outcomes were asthma incidence, exacerbation
frequency, emergency department visits, and respiratory symptom days.

Results showed children living in poor-quality housing had significantly higher
asthma rates (OR=1.8, 95% CI: 1.4-2.3, p<0.001) compared to those in adequate
housing. Mediation analysis revealed that indoor air quality measurements partially
explained this relationship. Effects were most pronounced in older buildings (built
pre-1978) and in humid climates. Mold remediation interventions reduced asthma
symptoms by 34% within 6 months. Policy implications suggest that housing code
enforcement and remediation funding could significantly improve pediatric respiratory health.
"""

test_title = "Housing Quality and Pediatric Asthma: A Multi-City Longitudinal Study"

print("="*80)
print("QUICK TEST: LLM Mechanism Extraction")
print("="*80)
print()

try:
    # Initialize LLM discovery
    print("[1/3] Initializing Claude API...")
    discovery = LLMMechanismDiscovery()
    print("  [OK] Connected to Claude")
    print()

    # Extract mechanisms
    print("[2/3] Extracting mechanisms from test abstract...")
    print(f"  Paper: {test_title}")
    print()

    mechanisms = discovery.extract_mechanisms_from_paper(
        paper_abstract=test_abstract,
        paper_title=test_title,
        focus_area="housing to health"
    )

    print(f"  [OK] Extracted {len(mechanisms)} mechanism(s)")
    print()

    # Display results
    print("[3/3] Results:")
    print("="*80)

    for i, mech in enumerate(mechanisms, 1):
        print(f"\n[ Mechanism {i} ]")
        print(f"FROM: {mech.from_node_name} (ID: {mech.from_node_id})")
        print(f"TO:   {mech.to_node_name} (ID: {mech.to_node_id})")
        print(f"Direction: {mech.direction}")
        print(f"Category: {mech.category}")
        print(f"Confidence: {mech.confidence}")
        print(f"Evidence: {mech.evidence_quality} rating ({mech.n_studies} studies)")
        print(f"\nPathway:")
        for j, step in enumerate(mech.mechanism_pathway, 1):
            print(f"  {j}. {step}")

        if mech.moderators:
            print(f"\nModerators:")
            for mod in mech.moderators:
                print(f"  - {mod['name']}: {mod['direction']} (strength: {mod['strength']})")

        print("-"*80)

    # Save mechanisms
    output_dir = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSaving mechanisms to: {output_dir}")
    for mech in mechanisms:
        file_path = discovery.save_mechanism(mech, output_dir)
        print(f"  [OK] Saved: {file_path.name}")

    print("\n" + "="*80)
    print("TEST COMPLETE!")
    print("="*80)

except Exception as e:
    print(f"\n[X] Error: {e}")
    import traceback
    traceback.print_exc()
