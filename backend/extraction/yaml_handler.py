"""
YAML file handling for mechanism storage.
Handles reading, writing, and validation.
"""
from pathlib import Path
from typing import Dict, Optional
import yaml


def write_mechanism_yaml(mechanism: Dict, category_dir: Path) -> Path:
    """
    Write mechanism to YAML file.

    Args:
        mechanism: Mechanism dict with 'id' and 'category'
        category_dir: Category directory path

    Returns:
        Path to written file
    """
    # Create category directory
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename from mechanism ID
    output_file = category_dir / f"{mechanism['id']}.yml"

    # Write YAML with proper formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(
            mechanism,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )

    return output_file


def read_mechanism_yaml(yaml_file: Path) -> Optional[Dict]:
    """
    Read mechanism from YAML file.

    Args:
        yaml_file: Path to YAML file

    Returns:
        Mechanism dict or None if read fails
    """
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {yaml_file}: {e}")
        return None


def validate_mechanism_schema(mechanism: Dict) -> tuple[bool, Optional[str]]:
    """
    Validate mechanism has required fields.

    Args:
        mechanism: Mechanism dict to validate

    Returns:
        (is_valid, error_message)
    """
    required_fields = [
        'id', 'name', 'from_node', 'to_node',
        'category', 'direction', 'evidence'
    ]

    for field in required_fields:
        if field not in mechanism:
            return False, f"Missing required field: {field}"

    # Validate nested structures
    if not isinstance(mechanism.get('from_node'), dict):
        return False, "from_node must be a dict"

    if not isinstance(mechanism.get('to_node'), dict):
        return False, "to_node must be a dict"

    if 'node_id' not in mechanism['from_node']:
        return False, "from_node missing node_id"

    if 'node_id' not in mechanism['to_node']:
        return False, "to_node missing node_id"

    return True, None
