"""
Extract Quantitative Effects from Mechanism YAML Files

This script parses mechanism YAML files and extracts quantitative effect data
(odds ratios, relative risks, percentages, fold-changes, etc.) from the narrative text.

The extracted data is saved in a structured JSON format that can be used for
future quantification phases while the MVP schema handles display.

Usage:
    python extract_quantitative_effects.py
    python extract_quantitative_effects.py --mechanism childhood_aces_to_alcohol_use_disorder
    python extract_quantitative_effects.py --output quantitative_effects.json
"""

import re
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EffectMeasure:
    """Structured effect measure extracted from text."""
    measure_type: str
    value: float
    lower_ci: Optional[float] = None
    upper_ci: Optional[float] = None
    unit: Optional[str] = None
    exposure: Optional[str] = None
    outcome: Optional[str] = None
    comparison: Optional[str] = None
    population: Optional[str] = None
    timeframe: Optional[str] = None
    source_text: Optional[str] = None
    source_field: Optional[str] = None
    citation: Optional[str] = None


@dataclass
class ModeratorEffect:
    """Quantified moderator effect."""
    moderator_name: str
    effect_modification: str
    effect_size: Optional[float] = None
    effect_size_type: Optional[str] = None
    range_low: Optional[float] = None
    range_high: Optional[float] = None
    source_text: Optional[str] = None


@dataclass
class ProgressionRate:
    """Disease/outcome progression rate."""
    stage_from: str
    stage_to: str
    percentage: Optional[float] = None
    timeframe: Optional[str] = None
    timeframe_years_low: Optional[float] = None
    timeframe_years_high: Optional[float] = None
    population: Optional[str] = None
    source_text: Optional[str] = None


@dataclass
class GeographicEffect:
    """Geographic variation in effect."""
    comparison_type: str
    variation_magnitude: Optional[float] = None
    high_region: Optional[str] = None
    low_region: Optional[str] = None
    notes: Optional[str] = None
    source_text: Optional[str] = None


@dataclass
class QuantitativeEffects:
    """All quantitative effects for a mechanism."""
    mechanism_id: str
    extraction_date: str = field(default_factory=lambda: datetime.now().isoformat())
    effects: List[EffectMeasure] = field(default_factory=list)
    moderator_effects: List[ModeratorEffect] = field(default_factory=list)
    progression_rates: List[ProgressionRate] = field(default_factory=list)
    geographic_variation: List[GeographicEffect] = field(default_factory=list)
    raw_numeric_mentions: List[Dict[str, Any]] = field(default_factory=list)


class QuantitativeExtractor:
    """Extract quantitative data from mechanism YAML files."""

    # Regex patterns for different effect types
    PATTERNS = {
        # Percentage patterns
        'percentage': r'(\d+(?:\.\d+)?)\s*(?:%|percent)',
        'percentage_range': r'(\d+(?:\.\d+)?)\s*[-–to]+\s*(\d+(?:\.\d+)?)\s*(?:%|percent)',
        'risk_increase': r'(?:increas|rais|elevat)\w*\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*(?:%|percent|fold)',
        'risk_decrease': r'(?:decreas|reduc|lower)\w*\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*(?:%|percent|fold)',

        # Fold-change patterns
        'fold_change': r'(\d+(?:\.\d+)?)\s*[-–]?\s*fold',
        'fold_range': r'(\d+(?:\.\d+)?)\s*[-–to]+\s*(\d+(?:\.\d+)?)\s*[-–]?\s*fold',
        'x_times': r'(\d+(?:\.\d+)?)\s*[xX×]\s+(?:higher|greater|more|lower|less)',

        # Odds ratio / relative risk patterns
        'odds_ratio': r'(?:OR|odds\s+ratio)\s*[=:of]*\s*(\d+(?:\.\d+)?)',
        'relative_risk': r'(?:RR|relative\s+risk|risk\s+ratio)\s*[=:of]*\s*(\d+(?:\.\d+)?)',
        'hazard_ratio': r'(?:HR|hazard\s+ratio)\s*[=:of]*\s*(\d+(?:\.\d+)?)',

        # Confidence interval patterns
        'ci_pattern': r'(?:CI|confidence\s+interval)[:\s]*\(?(\d+(?:\.\d+)?)\s*[-–,to]+\s*(\d+(?:\.\d+)?)\)?',
        'range_pattern': r'\((\d+(?:\.\d+)?)\s*[-–,to]+\s*(\d+(?:\.\d+)?)\)',

        # Time patterns
        'years_range': r'(\d+(?:\.\d+)?)\s*[-–to]+\s*(\d+(?:\.\d+)?)\s*years?',
        'years_single': r'(\d+(?:\.\d+)?)\s*years?',

        # Rate patterns
        'per_population': r'(\d+(?:\.\d+)?)\s+per\s+(\d+(?:,\d+)?)',
        'prevalence': r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s+(?:of|prevalence)',
    }

    def __init__(self, mechanism_bank_path: Optional[Path] = None):
        """Initialize extractor with path to mechanism bank."""
        if mechanism_bank_path is None:
            # Default to mechanism-bank relative to this script
            self.mechanism_bank_path = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"
        else:
            self.mechanism_bank_path = Path(mechanism_bank_path)

    def extract_from_text(self, text: str, source_field: str = "unknown") -> List[Dict[str, Any]]:
        """Extract all numeric mentions from text."""
        extractions = []

        if not text:
            return extractions

        text_lower = text.lower()

        # Check each pattern
        for pattern_name, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                extraction = {
                    'pattern_type': pattern_name,
                    'match': match.group(0),
                    'values': match.groups(),
                    'source_field': source_field,
                    'source_text': text[:200] + '...' if len(text) > 200 else text
                }
                extractions.append(extraction)

        return extractions

    def extract_effect_measures(self, mechanism: Dict) -> List[EffectMeasure]:
        """Extract structured effect measures from mechanism."""
        effects = []

        # Check mechanism_pathway
        for i, step in enumerate(mechanism.get('mechanism_pathway', [])):
            matches = self.extract_from_text(step, f'mechanism_pathway[{i}]')
            for m in matches:
                effect = self._parse_effect_from_match(m)
                if effect:
                    effects.append(effect)

        # Check description
        desc = mechanism.get('description', '')
        if desc:
            matches = self.extract_from_text(desc, 'description')
            for m in matches:
                effect = self._parse_effect_from_match(m)
                if effect:
                    effects.append(effect)

        # Check limitations
        for i, limitation in enumerate(mechanism.get('limitations', [])):
            matches = self.extract_from_text(limitation, f'limitations[{i}]')
            for m in matches:
                effect = self._parse_effect_from_match(m)
                if effect:
                    effects.append(effect)

        return effects

    def _parse_effect_from_match(self, match: Dict) -> Optional[EffectMeasure]:
        """Parse a regex match into an EffectMeasure."""
        pattern_type = match['pattern_type']
        values = match['values']

        if not values or not values[0]:
            return None

        try:
            value = float(values[0].replace(',', ''))
        except (ValueError, TypeError):
            return None

        # Determine measure type based on pattern
        measure_type_map = {
            'percentage': 'percentage_change',
            'percentage_range': 'percentage_change',
            'risk_increase': 'percentage_increase',
            'risk_decrease': 'risk_reduction',
            'fold_change': 'fold_change',
            'fold_range': 'fold_change',
            'x_times': 'fold_change',
            'odds_ratio': 'odds_ratio',
            'relative_risk': 'relative_risk',
            'hazard_ratio': 'hazard_ratio',
            'per_population': 'incidence_rate',
            'prevalence': 'prevalence',
        }

        measure_type = measure_type_map.get(pattern_type, 'unknown')

        # Handle ranges
        lower_ci = None
        upper_ci = None
        if len(values) > 1 and values[1]:
            try:
                upper_ci = float(values[1].replace(',', ''))
                lower_ci = value
                value = (lower_ci + upper_ci) / 2  # Use midpoint as value
            except (ValueError, TypeError):
                pass

        return EffectMeasure(
            measure_type=measure_type,
            value=value,
            lower_ci=lower_ci,
            upper_ci=upper_ci,
            source_text=match.get('source_text'),
            source_field=match.get('source_field')
        )

    def extract_moderator_effects(self, mechanism: Dict) -> List[ModeratorEffect]:
        """Extract quantified moderator effects."""
        effects = []

        for mod in mechanism.get('moderators', []):
            mod_name = mod.get('name', 'unknown')
            direction = mod.get('direction', 'unknown')
            description = mod.get('description', '')

            # Extract numeric values from description
            matches = self.extract_from_text(description, f'moderator:{mod_name}')

            effect_size = None
            range_low = None
            range_high = None

            for m in matches:
                values = m['values']
                if values and values[0]:
                    try:
                        if len(values) > 1 and values[1]:
                            range_low = float(values[0].replace(',', ''))
                            range_high = float(values[1].replace(',', ''))
                            effect_size = (range_low + range_high) / 2
                        else:
                            effect_size = float(values[0].replace(',', ''))
                    except (ValueError, TypeError):
                        continue

            if effect_size or description:
                effects.append(ModeratorEffect(
                    moderator_name=mod_name,
                    effect_modification=direction,
                    effect_size=effect_size,
                    range_low=range_low,
                    range_high=range_high,
                    source_text=description
                ))

        return effects

    def extract_progression_rates(self, mechanism: Dict) -> List[ProgressionRate]:
        """Extract disease/outcome progression rates."""
        rates = []

        # Look in limitations and mechanism_pathway for progression language
        texts_to_check = []
        texts_to_check.extend([(l, 'limitations') for l in mechanism.get('limitations', [])])
        texts_to_check.extend([(s, 'mechanism_pathway') for s in mechanism.get('mechanism_pathway', [])])

        for text, source in texts_to_check:
            text_lower = text.lower()

            # Look for progression patterns
            if any(word in text_lower for word in ['progress', 'develop', 'transition', 'convert']):
                # Extract percentages and timeframes
                pct_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]?\s*(\d+(?:\.\d+)?)?\s*(?:%|percent)', text_lower)
                time_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]?\s*(\d+(?:\.\d+)?)?\s*years?', text_lower)

                if pct_match:
                    percentage = float(pct_match.group(1))
                    if pct_match.group(2):
                        percentage = (percentage + float(pct_match.group(2))) / 2

                    timeframe = None
                    timeframe_low = None
                    timeframe_high = None

                    if time_match:
                        timeframe_low = float(time_match.group(1))
                        if time_match.group(2):
                            timeframe_high = float(time_match.group(2))
                            timeframe = f"{timeframe_low}-{timeframe_high} years"
                        else:
                            timeframe = f"{timeframe_low} years"

                    rates.append(ProgressionRate(
                        stage_from="exposure",
                        stage_to="outcome",
                        percentage=percentage,
                        timeframe=timeframe,
                        timeframe_years_low=timeframe_low,
                        timeframe_years_high=timeframe_high,
                        source_text=text
                    ))

        return rates

    def extract_geographic_variation(self, mechanism: Dict) -> List[GeographicEffect]:
        """Extract geographic variation data."""
        effects = []

        spatial = mechanism.get('spatial_variation', {})
        if not spatial.get('varies_by_geography', False):
            return effects

        variation_notes = spatial.get('variation_notes', '')

        # Look for fold-variation patterns
        fold_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]?\s*fold', variation_notes.lower())
        if fold_match:
            effects.append(GeographicEffect(
                comparison_type='regional',
                variation_magnitude=float(fold_match.group(1)),
                notes=variation_notes,
                source_text=variation_notes
            ))

        # Look for multiplier patterns (3-5x, etc.)
        mult_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]?\s*(\d+(?:\.\d+)?)?\s*[xX×]', variation_notes)
        if mult_match:
            low = float(mult_match.group(1))
            high = float(mult_match.group(2)) if mult_match.group(2) else low
            effects.append(GeographicEffect(
                comparison_type='subgroup',
                variation_magnitude=(low + high) / 2,
                notes=variation_notes,
                source_text=variation_notes
            ))

        return effects

    def extract_from_mechanism(self, mechanism: Dict) -> QuantitativeEffects:
        """Extract all quantitative data from a mechanism."""
        mech_id = mechanism.get('id', 'unknown')

        return QuantitativeEffects(
            mechanism_id=mech_id,
            effects=self.extract_effect_measures(mechanism),
            moderator_effects=self.extract_moderator_effects(mechanism),
            progression_rates=self.extract_progression_rates(mechanism),
            geographic_variation=self.extract_geographic_variation(mechanism)
        )

    def extract_all(self) -> Dict[str, QuantitativeEffects]:
        """Extract quantitative data from all mechanism YAML files."""
        results = {}

        yaml_files = list(self.mechanism_bank_path.rglob("*.yml")) + \
                     list(self.mechanism_bank_path.rglob("*.yaml"))

        logger.info(f"Found {len(yaml_files)} mechanism files")

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    mechanism = yaml.safe_load(f)

                if mechanism:
                    extracted = self.extract_from_mechanism(mechanism)
                    results[extracted.mechanism_id] = extracted

                    # Log if we found quantitative data
                    total_effects = (
                        len(extracted.effects) +
                        len(extracted.moderator_effects) +
                        len(extracted.progression_rates) +
                        len(extracted.geographic_variation)
                    )
                    if total_effects > 0:
                        logger.info(f"  {extracted.mechanism_id}: {total_effects} quantitative measures found")

            except Exception as e:
                logger.error(f"Error processing {yaml_file}: {e}")

        return results

    def save_results(self, results: Dict[str, QuantitativeEffects], output_path: Path):
        """Save extraction results to JSON."""
        output_data = {
            'extraction_date': datetime.now().isoformat(),
            'total_mechanisms': len(results),
            'mechanisms_with_effects': sum(
                1 for r in results.values()
                if r.effects or r.moderator_effects or r.progression_rates or r.geographic_variation
            ),
            'mechanisms': {
                mech_id: asdict(data) for mech_id, data in results.items()
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, default=str)

        logger.info(f"Saved results to {output_path}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract quantitative effects from mechanism YAML files")
    parser.add_argument('--mechanism', type=str, help='Extract from single mechanism ID')
    parser.add_argument('--output', type=str, default='quantitative_effects.json', help='Output file path')
    parser.add_argument('--mechanism-bank', type=str, help='Path to mechanism-bank/mechanisms directory')

    args = parser.parse_args()

    extractor = QuantitativeExtractor(
        mechanism_bank_path=Path(args.mechanism_bank) if args.mechanism_bank else None
    )

    if args.mechanism:
        # Find and extract single mechanism
        yaml_files = list(extractor.mechanism_bank_path.rglob(f"*{args.mechanism}*.yml"))
        if not yaml_files:
            logger.error(f"Mechanism not found: {args.mechanism}")
            return

        with open(yaml_files[0], 'r', encoding='utf-8') as f:
            mechanism = yaml.safe_load(f)

        result = extractor.extract_from_mechanism(mechanism)
        print(json.dumps(asdict(result), indent=2, default=str))
    else:
        # Extract all
        results = extractor.extract_all()
        output_path = Path(args.output)
        extractor.save_results(results, output_path)

        # Print summary
        print(f"\n=== Extraction Summary ===")
        print(f"Total mechanisms: {len(results)}")

        with_effects = sum(
            1 for r in results.values()
            if r.effects or r.moderator_effects or r.progression_rates or r.geographic_variation
        )
        print(f"Mechanisms with quantitative data: {with_effects}")

        total_effects = sum(len(r.effects) for r in results.values())
        total_moderators = sum(len(r.moderator_effects) for r in results.values())
        total_progression = sum(len(r.progression_rates) for r in results.values())
        total_geographic = sum(len(r.geographic_variation) for r in results.values())

        print(f"\nEffect measures extracted: {total_effects}")
        print(f"Moderator effects extracted: {total_moderators}")
        print(f"Progression rates extracted: {total_progression}")
        print(f"Geographic variations extracted: {total_geographic}")


if __name__ == "__main__":
    main()
