"""
Mechanism Schema Validator

Validates mechanism YAML files against the schema defined in:
05_MECHANISM_BANK_STRUCTURE.md

Checks for:
- Required fields (from_node, to_node, functional_form, etc.)
- Bidirectional encoding (direction field)
- Parameter structure (alpha, L, k, x0 for sigmoid, etc.)
- Moderator structure (policy, demographic, geographic, implementation)
- Version control and lineage
- Parameter bounds and plausibility
- Evidence structure

Usage:
  python validate_mechanism_schema.py --file mechanism.yml
  python validate_mechanism_schema.py --dir mechanism-bank/mechanisms/
"""

from typing import Dict, List, Tuple, Optional
from pathlib import Path
import yaml
from dataclasses import dataclass
import argparse


@dataclass
class ValidationResult:
    """Result of schema validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]


class MechanismSchemaValidator:
    """
    Validates mechanism YAML files against 05_MECHANISM_BANK_STRUCTURE.md schema.
    """

    # Required top-level fields
    REQUIRED_FIELDS = [
        'from_node_id',
        'to_node_id',
        'category',
        'description',
        'functional_form',
        'parameters',
        'evidence_quality'
    ]

    # Valid functional forms
    VALID_FUNCTIONAL_FORMS = [
        'sigmoid',
        'threshold',
        'logarithmic',
        'multiplicative_dampening',
        'saturating_linear',
        'linear'
    ]

    # Required parameters by functional form
    FORM_REQUIRED_PARAMS = {
        'sigmoid': ['alpha', 'L', 'k', 'x0'],
        'threshold': ['alpha', 'threshold'],
        'logarithmic': ['alpha'],
        'multiplicative_dampening': ['alpha', 'Max_Stock_j'],
        'saturating_linear': ['alpha', 'saturation_point'],
        'linear': ['alpha']
    }

    # Valid moderator types
    VALID_MODERATOR_TYPES = ['policy', 'demographic', 'geographic', 'implementation']

    # Valid evidence quality grades
    VALID_EVIDENCE_GRADES = ['A', 'B', 'C', 'D']

    def __init__(self, strict: bool = False):
        """
        Initialize validator.

        Args:
            strict: If True, warnings are treated as errors
        """
        self.strict = strict

    def validate(self, mechanism: Dict) -> ValidationResult:
        """
        Validate a mechanism dictionary.

        Args:
            mechanism: Mechanism dictionary (loaded from YAML)

        Returns:
            ValidationResult with errors, warnings, info
        """
        errors = []
        warnings = []
        info = []

        # 1. Check required fields
        missing_fields = self._check_required_fields(mechanism)
        if missing_fields:
            errors.extend([f"Missing required field: {field}" for field in missing_fields])

        # If critical fields missing, cannot continue validation
        if not mechanism.get('functional_form') or not mechanism.get('from_node_id'):
            return ValidationResult(valid=False, errors=errors, warnings=warnings, info=info)

        # 2. Validate functional form
        form_errors, form_warnings = self._validate_functional_form(mechanism)
        errors.extend(form_errors)
        warnings.extend(form_warnings)

        # 3. Validate parameters
        param_errors, param_warnings = self._validate_parameters(mechanism)
        errors.extend(param_errors)
        warnings.extend(param_warnings)

        # 4. Validate moderators (if present)
        if 'moderators' in mechanism:
            mod_errors, mod_warnings = self._validate_moderators(mechanism)
            errors.extend(mod_errors)
            warnings.extend(mod_warnings)

        # 5. Validate evidence structure
        ev_errors, ev_warnings = self._validate_evidence(mechanism)
        errors.extend(ev_errors)
        warnings.extend(ev_warnings)

        # 6. Check bidirectional encoding
        dir_warnings = self._check_directionality(mechanism)
        warnings.extend(dir_warnings)

        # 7. Check version control (warning if missing)
        vc_warnings = self._check_version_control(mechanism)
        warnings.extend(vc_warnings)

        # 8. Validate bounds and plausibility
        bound_warnings = self._validate_bounds(mechanism)
        warnings.extend(bound_warnings)

        # Determine validity
        valid = len(errors) == 0
        if self.strict and warnings:
            valid = False

        return ValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            info=info
        )

    def _check_required_fields(self, mechanism: Dict) -> List[str]:
        """Check for missing required fields."""
        missing = []
        for field in self.REQUIRED_FIELDS:
            if field not in mechanism:
                missing.append(field)
        return missing

    def _validate_functional_form(self, mechanism: Dict) -> Tuple[List[str], List[str]]:
        """Validate functional form specification."""
        errors = []
        warnings = []

        functional_form = mechanism.get('functional_form', '')

        # Check if form is valid
        if functional_form not in self.VALID_FUNCTIONAL_FORMS:
            errors.append(
                f"Invalid functional_form: '{functional_form}'. "
                f"Must be one of: {', '.join(self.VALID_FUNCTIONAL_FORMS)}"
            )
            return errors, warnings

        # Check if equation is present
        if 'equation' not in mechanism:
            warnings.append(f"Missing 'equation' field for {functional_form} form")

        return errors, warnings

    def _validate_parameters(self, mechanism: Dict) -> Tuple[List[str], List[str]]:
        """Validate parameter structure."""
        errors = []
        warnings = []

        functional_form = mechanism.get('functional_form', '')
        parameters = mechanism.get('parameters', {})

        if not parameters:
            errors.append("'parameters' field is empty or missing")
            return errors, warnings

        # Check for required parameters based on functional form
        if functional_form in self.FORM_REQUIRED_PARAMS:
            required_params = self.FORM_REQUIRED_PARAMS[functional_form]
            for param in required_params:
                if param not in parameters:
                    errors.append(
                        f"Missing required parameter '{param}' for {functional_form} form"
                    )

        # Validate parameter structure
        for param_name, param_value in parameters.items():
            # Parameters should be dictionaries with 'value' field
            if isinstance(param_value, dict):
                if 'value' not in param_value:
                    errors.append(f"Parameter '{param_name}' missing 'value' field")

                # Check for recommended fields
                if 'description' not in param_value:
                    warnings.append(f"Parameter '{param_name}' missing 'description'")
                if 'source' not in param_value:
                    warnings.append(f"Parameter '{param_name}' missing 'source'")
            else:
                # Parameter is a raw value (acceptable but not best practice)
                warnings.append(
                    f"Parameter '{param_name}' is a raw value. "
                    "Consider using dict with 'value', 'description', 'source'"
                )

        return errors, warnings

    def _validate_moderators(self, mechanism: Dict) -> Tuple[List[str], List[str]]:
        """Validate moderator structure."""
        errors = []
        warnings = []

        moderators = mechanism.get('moderators', [])

        if not isinstance(moderators, list):
            errors.append("'moderators' must be a list")
            return errors, warnings

        for i, moderator in enumerate(moderators):
            if not isinstance(moderator, dict):
                errors.append(f"Moderator {i} is not a dictionary")
                continue

            # Check required moderator fields
            required_mod_fields = [
                'moderator_type',
                'factor_name',
                'adjustment_type',
                'adjustment_value'
            ]

            for field in required_mod_fields:
                if field not in moderator:
                    errors.append(f"Moderator {i} missing '{field}'")

            # Validate moderator_type
            mod_type = moderator.get('moderator_type', '')
            if mod_type not in self.VALID_MODERATOR_TYPES:
                errors.append(
                    f"Moderator {i} has invalid type '{mod_type}'. "
                    f"Must be one of: {', '.join(self.VALID_MODERATOR_TYPES)}"
                )

            # Validate adjustment_type
            adj_type = moderator.get('adjustment_type', '')
            if adj_type not in ['additive', 'multiplicative']:
                errors.append(
                    f"Moderator {i} has invalid adjustment_type '{adj_type}'. "
                    "Must be 'additive' or 'multiplicative'"
                )

            # Check for evidence
            if 'evidence' not in moderator:
                warnings.append(f"Moderator {i} missing 'evidence' field")

        return errors, warnings

    def _validate_evidence(self, mechanism: Dict) -> Tuple[List[str], List[str]]:
        """Validate evidence structure."""
        errors = []
        warnings = []

        # Check evidence_quality
        evidence_quality = mechanism.get('evidence_quality', '')
        if evidence_quality not in self.VALID_EVIDENCE_GRADES:
            errors.append(
                f"Invalid evidence_quality '{evidence_quality}'. "
                f"Must be one of: {', '.join(self.VALID_EVIDENCE_GRADES)}"
            )

        # Check for n_studies
        if 'n_studies' not in mechanism:
            warnings.append("Missing 'n_studies' field")
        else:
            n_studies = mechanism.get('n_studies', 0)
            if not isinstance(n_studies, int) or n_studies < 0:
                errors.append(f"'n_studies' must be a non-negative integer, got: {n_studies}")

        # Check for effect size data
        if 'effect_size' in mechanism:
            # If effect_size present, should have CI
            if 'ci_lower' not in mechanism or 'ci_upper' not in mechanism:
                warnings.append("'effect_size' present but missing confidence interval (ci_lower/ci_upper)")

            # Validate CI contains point estimate
            if all(k in mechanism for k in ['effect_size', 'ci_lower', 'ci_upper']):
                effect = mechanism['effect_size']
                ci_lower = mechanism['ci_lower']
                ci_upper = mechanism['ci_upper']

                if not (ci_lower <= effect <= ci_upper):
                    errors.append(
                        f"Confidence interval [{ci_lower}, {ci_upper}] does not contain "
                        f"point estimate {effect}"
                    )

        return errors, warnings

    def _check_directionality(self, mechanism: Dict) -> List[str]:
        """Check for bidirectional encoding (direction field)."""
        warnings = []

        if 'direction' not in mechanism:
            warnings.append(
                "Missing 'direction' field. Should be 'forward', 'backward', or 'horizontal' "
                "(see 05_MECHANISM_BANK_STRUCTURE.md)"
            )
        else:
            direction = mechanism.get('direction', '')
            if direction not in ['forward', 'backward', 'horizontal']:
                warnings.append(
                    f"Invalid direction '{direction}'. "
                    "Should be 'forward', 'backward', or 'horizontal'"
                )

        return warnings

    def _check_version_control(self, mechanism: Dict) -> List[str]:
        """Check for version control metadata."""
        warnings = []

        if 'version' not in mechanism:
            warnings.append("Missing 'version' field (recommended for version control)")

        if 'lineage' not in mechanism:
            warnings.append(
                "Missing 'lineage' field (recommended to track mechanism evolution)"
            )

        return warnings

    def _validate_bounds(self, mechanism: Dict) -> List[str]:
        """Validate parameter bounds and plausibility."""
        warnings = []

        # Check effect size plausibility
        if 'effect_size' in mechanism:
            effect_size = mechanism['effect_size']

            # For standardized effect sizes (Cohen's d, etc.)
            effect_size_type = mechanism.get('effect_size_type', 'unknown')

            if 'cohen' in effect_size_type.lower() or 'standardized' in effect_size_type.lower():
                if abs(effect_size) > 1.5:
                    warnings.append(
                        f"Large effect size |d| = {abs(effect_size)} (>1.5). "
                        "Requires extra scrutiny (see 05_MECHANISM_BANK_STRUCTURE.md)"
                    )

        # Check functional form parameters
        functional_form = mechanism.get('functional_form', '')
        parameters = mechanism.get('parameters', {})

        if functional_form == 'sigmoid':
            L = self._get_param_value(parameters, 'L')
            k = self._get_param_value(parameters, 'k')

            if L is not None and (L < 0 or L > 2.0):
                warnings.append(f"Sigmoid parameter L = {L} outside typical bounds [0, 2.0]")

            if k is not None and (k < 0.01 or k > 5.0):
                warnings.append(f"Sigmoid parameter k = {k} outside typical bounds [0.01, 5.0]")

        return warnings

    def _get_param_value(self, parameters: Dict, param_name: str) -> Optional[float]:
        """Extract parameter value (handles both raw values and dicts)."""
        if param_name not in parameters:
            return None

        param = parameters[param_name]
        if isinstance(param, dict):
            return param.get('value')
        else:
            return param

    def validate_file(self, filepath: Path, verbose: bool = True) -> ValidationResult:
        """
        Validate a mechanism YAML file.

        Args:
            filepath: Path to YAML file
            verbose: Print validation results

        Returns:
            ValidationResult
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                mechanism = yaml.safe_load(f)
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Failed to load YAML: {e}"],
                warnings=[],
                info=[]
            )

        result = self.validate(mechanism)

        if verbose:
            self._print_result(filepath, result)

        return result

    def validate_directory(
        self,
        directory: Path,
        verbose: bool = True,
        summary: bool = True
    ) -> Dict[str, ValidationResult]:
        """
        Validate all YAML files in a directory.

        Args:
            directory: Path to directory
            verbose: Print per-file results
            summary: Print summary at end

        Returns:
            Dict mapping filepath to ValidationResult
        """
        directory = Path(directory)
        results = {}

        yaml_files = list(directory.rglob("*.yml")) + list(directory.rglob("*.yaml"))

        if verbose:
            print(f"\n=== Validating {len(yaml_files)} mechanism files ===\n")

        for yaml_file in yaml_files:
            result = self.validate_file(yaml_file, verbose=False)
            results[str(yaml_file)] = result

            if verbose:
                status = "✓ VALID" if result.valid else "✗ INVALID"
                print(f"{status}: {yaml_file.name}")
                if result.errors:
                    for error in result.errors:
                        print(f"  ERROR: {error}")
                if result.warnings and not result.valid:
                    for warning in result.warnings[:3]:  # Show first 3 warnings
                        print(f"  WARNING: {warning}")

        if summary:
            self._print_summary(results)

        return results

    def _print_result(self, filepath: Path, result: ValidationResult):
        """Print validation result for a single file."""
        print(f"\n=== Validation Result: {filepath.name} ===")

        if result.valid:
            print("✓ VALID")
        else:
            print("✗ INVALID")

        if result.errors:
            print("\nErrors:")
            for error in result.errors:
                print(f"  - {error}")

        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  - {warning}")

        if result.info:
            print("\nInfo:")
            for info in result.info:
                print(f"  - {info}")

    def _print_summary(self, results: Dict[str, ValidationResult]):
        """Print summary of validation results."""
        total = len(results)
        valid = sum(1 for r in results.values() if r.valid)
        invalid = total - valid

        total_errors = sum(len(r.errors) for r in results.values())
        total_warnings = sum(len(r.warnings) for r in results.values())

        print(f"\n=== Validation Summary ===")
        print(f"Total files: {total}")
        print(f"Valid: {valid} ({100*valid/total:.1f}%)")
        print(f"Invalid: {invalid} ({100*invalid/total:.1f}%)")
        print(f"Total errors: {total_errors}")
        print(f"Total warnings: {total_warnings}")

        if invalid > 0:
            print("\nInvalid files:")
            for filepath, result in results.items():
                if not result.valid:
                    print(f"  - {Path(filepath).name}: {len(result.errors)} errors")


def main():
    """Command-line interface for validator."""
    parser = argparse.ArgumentParser(
        description="Validate mechanism YAML files against schema"
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to single YAML file to validate'
    )
    parser.add_argument(
        '--dir',
        type=str,
        help='Path to directory of YAML files to validate'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    validator = MechanismSchemaValidator(strict=args.strict)

    if args.file:
        filepath = Path(args.file)
        result = validator.validate_file(filepath, verbose=True)
        exit(0 if result.valid else 1)

    elif args.dir:
        directory = Path(args.dir)
        results = validator.validate_directory(directory, verbose=True, summary=True)
        invalid_count = sum(1 for r in results.values() if not r.valid)
        exit(0 if invalid_count == 0 else 1)

    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
