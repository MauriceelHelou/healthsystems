#!/usr/bin/env python
"""
Validate mechanism files against schema.

Usage:
    python validate_mechanisms.py                          # Validate all
    python validate_mechanisms.py --file path/to/file.yml  # Validate one
"""

import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from jsonschema import validate, ValidationError
from datetime import datetime


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load JSON schema."""
    with open(schema_path) as f:
        return json.load(f)


def load_mechanism(mechanism_path: Path) -> Dict[str, Any]:
    """Load mechanism YAML file."""
    with open(mechanism_path) as f:
        return yaml.safe_load(f)


def validate_mechanism(
    mechanism_data: Dict[str, Any],
    schema: Dict[str, Any]
) -> tuple[bool, List[str]]:
    """
    Validate mechanism against schema.

    Args:
        mechanism_data: Mechanism data to validate
        schema: JSON schema

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Schema validation
    try:
        validate(instance=mechanism_data, schema=schema)
    except ValidationError as e:
        errors.append(f"Schema validation failed: {e.message}")
        return False, errors

    # Additional validations

    # Check CI is valid
    ci = mechanism_data['effect_size']['confidence_interval']
    if ci[0] >= ci[1]:
        errors.append(
            f"Invalid confidence interval: lower ({ci[0]}) >= upper ({ci[1]})"
        )

    # Check date is not in future
    last_updated = datetime.strptime(
        mechanism_data['last_updated'], '%Y-%m-%d'
    )
    if last_updated > datetime.now():
        errors.append(
            f"Last updated date is in the future: {mechanism_data['last_updated']}"
        )

    # Check evidence requirements
    rating = mechanism_data['evidence']['quality_rating']
    n_studies = mechanism_data['evidence']['n_studies']

    if rating == 'A' and n_studies < 3:
        errors.append(
            f"Quality rating A requires ≥3 studies, found {n_studies}"
        )

    # Check citation format (basic check)
    citation = mechanism_data['evidence']['citation']
    if 'http' not in citation and 'doi' not in citation.lower():
        errors.append(
            "Citation should include DOI or URL"
        )

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_all_mechanisms(
    mechanisms_dir: Path,
    schema_path: Path
) -> Dict[str, Any]:
    """
    Validate all mechanism files.

    Returns:
        Dict with validation results
    """
    schema = load_schema(schema_path)
    results = {
        'valid': [],
        'invalid': [],
        'total': 0
    }

    # Find all YAML files
    mechanism_files = list(mechanisms_dir.rglob('*.yml')) + \
                      list(mechanisms_dir.rglob('*.yaml'))

    for mechanism_file in mechanism_files:
        results['total'] += 1

        try:
            mechanism_data = load_mechanism(mechanism_file)
            is_valid, errors = validate_mechanism(mechanism_data, schema)

            if is_valid:
                results['valid'].append(str(mechanism_file))
                print(f"✓ {mechanism_file.relative_to(mechanisms_dir)}")
            else:
                results['invalid'].append({
                    'file': str(mechanism_file),
                    'errors': errors
                })
                print(f"✗ {mechanism_file.relative_to(mechanisms_dir)}")
                for error in errors:
                    print(f"  - {error}")

        except Exception as e:
            results['invalid'].append({
                'file': str(mechanism_file),
                'errors': [f"Failed to load: {str(e)}"]
            })
            print(f"✗ {mechanism_file.relative_to(mechanisms_dir)}")
            print(f"  - Failed to load: {str(e)}")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate mechanism files'
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='Validate a single file'
    )
    args = parser.parse_args()

    # Paths
    project_root = Path(__file__).parent.parent
    schema_path = project_root / 'schemas' / 'mechanism_schema.json'
    mechanisms_dir = project_root / 'mechanisms'

    if args.file:
        # Validate single file
        schema = load_schema(schema_path)
        mechanism_data = load_mechanism(args.file)
        is_valid, errors = validate_mechanism(mechanism_data, schema)

        if is_valid:
            print(f"✓ {args.file} is valid")
            return 0
        else:
            print(f"✗ {args.file} is invalid:")
            for error in errors:
                print(f"  - {error}")
            return 1

    else:
        # Validate all files
        print("Validating all mechanisms...\n")
        results = validate_all_mechanisms(mechanisms_dir, schema_path)

        print(f"\n{'='*60}")
        print(f"Total: {results['total']}")
        print(f"Valid: {len(results['valid'])}")
        print(f"Invalid: {len(results['invalid'])}")
        print(f"{'='*60}")

        if results['invalid']:
            return 1
        return 0


if __name__ == '__main__':
    exit(main())
