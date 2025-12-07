"""
Node validation utilities for mechanism referential integrity.

Ensures that mechanisms can only reference nodes that exist in the Node Bank.
This is a critical constraint: mechanisms cannot create ad-hoc nodes.

Usage:
    from backend.utils.node_validation import validate_mechanism_nodes

    # With database session
    errors = validate_mechanism_nodes(mechanism_dict, db)

    # With node set (for bulk validation)
    errors = validate_mechanism_nodes_against_set(mechanism_dict, valid_node_ids)
"""

from typing import Dict, List, Set, Optional
from pathlib import Path
import yaml


class NodeValidationError(Exception):
    """Raised when a mechanism references a non-existent node."""
    pass


def validate_mechanism_nodes(
    mechanism: Dict,
    db,
    node_model
) -> List[str]:
    """
    Validate that mechanism nodes exist in the database.

    Args:
        mechanism: Mechanism dictionary (from YAML or API)
        db: Database session
        node_model: The Node model class

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Extract node IDs from mechanism
    from_node_id = _extract_node_id(mechanism, 'from_node')
    to_node_id = _extract_node_id(mechanism, 'to_node')

    # Validate from_node exists
    if from_node_id:
        from_node = db.query(node_model).filter(node_model.id == from_node_id).first()
        if not from_node:
            errors.append(f"from_node '{from_node_id}' does not exist in Node Bank")

    # Validate to_node exists
    if to_node_id:
        to_node = db.query(node_model).filter(node_model.id == to_node_id).first()
        if not to_node:
            errors.append(f"to_node '{to_node_id}' does not exist in Node Bank")

    return errors


def validate_mechanism_nodes_against_set(
    mechanism: Dict,
    valid_node_ids: Set[str]
) -> List[str]:
    """
    Validate mechanism nodes against a pre-loaded set of valid node IDs.

    More efficient for bulk validation where node set is already loaded.

    Args:
        mechanism: Mechanism dictionary (from YAML or API)
        valid_node_ids: Set of valid node IDs from the Node Bank

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Extract node IDs from mechanism
    from_node_id = _extract_node_id(mechanism, 'from_node')
    to_node_id = _extract_node_id(mechanism, 'to_node')

    # Validate from_node exists
    if from_node_id and from_node_id not in valid_node_ids:
        errors.append(f"from_node '{from_node_id}' does not exist in Node Bank")

    # Validate to_node exists
    if to_node_id and to_node_id not in valid_node_ids:
        errors.append(f"to_node '{to_node_id}' does not exist in Node Bank")

    return errors


def _extract_node_id(mechanism: Dict, node_field: str) -> Optional[str]:
    """
    Extract node ID from mechanism, handling different formats.

    Supports:
    - MVP format: from_node: { node_id: "xyz" }
    - Quantified format: from_node_id: "xyz"
    - Direct format: from_node: "xyz"

    Args:
        mechanism: Mechanism dictionary
        node_field: Field name ('from_node' or 'to_node')

    Returns:
        Node ID string or None
    """
    # Try MVP format: from_node: { node_id: "xyz" }
    node_data = mechanism.get(node_field)
    if isinstance(node_data, dict):
        return node_data.get('node_id')

    # Try quantified format: from_node_id: "xyz"
    node_id = mechanism.get(f'{node_field}_id')
    if node_id:
        return node_id

    # Try direct format: from_node: "xyz"
    if isinstance(node_data, str):
        return node_data

    return None


def load_valid_node_ids_from_db(db, node_model) -> Set[str]:
    """
    Load all valid node IDs from the database.

    Args:
        db: Database session
        node_model: The Node model class

    Returns:
        Set of all node IDs in the database
    """
    nodes = db.query(node_model.id).all()
    return {node.id for node in nodes}


def load_valid_node_ids_from_yaml(node_bank_path: Path) -> Set[str]:
    """
    Load valid node IDs from YAML node bank files.

    Args:
        node_bank_path: Path to the node-bank directory or nodes file

    Returns:
        Set of all node IDs from YAML files
    """
    valid_ids = set()

    if node_bank_path.is_file():
        # Single file
        with open(node_bank_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, list):
                for node in data:
                    if isinstance(node, dict) and 'id' in node:
                        valid_ids.add(node['id'])
            elif isinstance(data, dict):
                # Could be a dict with nodes key
                nodes = data.get('nodes', [])
                for node in nodes:
                    if isinstance(node, dict) and 'id' in node:
                        valid_ids.add(node['id'])
    else:
        # Directory - find all YAML files
        yaml_files = list(node_bank_path.rglob('*.yml')) + list(node_bank_path.rglob('*.yaml'))
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and 'id' in data:
                        valid_ids.add(data['id'])
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'id' in item:
                                valid_ids.add(item['id'])
            except Exception:
                continue  # Skip files that can't be parsed

    return valid_ids


def validate_mechanism_file_nodes(
    mechanism_file: Path,
    valid_node_ids: Set[str]
) -> Dict[str, List[str]]:
    """
    Validate nodes in a mechanism YAML file.

    Args:
        mechanism_file: Path to mechanism YAML file
        valid_node_ids: Set of valid node IDs

    Returns:
        Dict with 'errors' and 'warnings' lists
    """
    result = {'errors': [], 'warnings': []}

    try:
        with open(mechanism_file, 'r', encoding='utf-8') as f:
            mechanism = yaml.safe_load(f)
    except Exception as e:
        result['errors'].append(f"Failed to load YAML: {e}")
        return result

    node_errors = validate_mechanism_nodes_against_set(mechanism, valid_node_ids)
    result['errors'].extend(node_errors)

    # Add suggestions for unknown nodes
    for error in node_errors:
        # Extract the node ID from the error message
        if "does not exist" in error:
            node_id = error.split("'")[1]
            suggestions = find_similar_nodes(node_id, valid_node_ids)
            if suggestions:
                result['warnings'].append(
                    f"Did you mean one of: {', '.join(suggestions[:3])}?"
                )

    return result


def find_similar_nodes(node_id: str, valid_node_ids: Set[str], max_distance: int = 3) -> List[str]:
    """
    Find similar node IDs using simple string matching.

    Args:
        node_id: The unknown node ID
        valid_node_ids: Set of valid node IDs
        max_distance: Maximum edit distance for suggestions

    Returns:
        List of similar node IDs
    """
    suggestions = []

    # Simple substring matching
    node_parts = node_id.lower().split('_')

    for valid_id in valid_node_ids:
        valid_parts = valid_id.lower().split('_')

        # Check for common parts
        common_parts = set(node_parts) & set(valid_parts)
        if len(common_parts) >= len(node_parts) // 2 + 1:
            suggestions.append(valid_id)

    # Sort by similarity (more common parts first)
    suggestions.sort(key=lambda x: -len(set(x.lower().split('_')) & set(node_parts)))

    return suggestions[:5]


class MechanismNodeValidator:
    """
    Validator class for checking mechanism node references.

    Provides both database and file-based validation.
    """

    def __init__(
        self,
        db=None,
        node_model=None,
        node_bank_path: Optional[Path] = None
    ):
        """
        Initialize validator with node source.

        Args:
            db: Database session (for DB-based validation)
            node_model: The Node model class
            node_bank_path: Path to node bank YAML files (for file-based validation)
        """
        self.db = db
        self.node_model = node_model
        self.node_bank_path = node_bank_path
        self._valid_node_ids: Optional[Set[str]] = None

    @property
    def valid_node_ids(self) -> Set[str]:
        """Lazy-load valid node IDs."""
        if self._valid_node_ids is None:
            if self.db and self.node_model:
                self._valid_node_ids = load_valid_node_ids_from_db(self.db, self.node_model)
            elif self.node_bank_path:
                self._valid_node_ids = load_valid_node_ids_from_yaml(self.node_bank_path)
            else:
                self._valid_node_ids = set()
        return self._valid_node_ids

    def validate(self, mechanism: Dict) -> List[str]:
        """
        Validate mechanism node references.

        Args:
            mechanism: Mechanism dictionary

        Returns:
            List of error messages
        """
        return validate_mechanism_nodes_against_set(mechanism, self.valid_node_ids)

    def validate_file(self, mechanism_file: Path) -> Dict[str, List[str]]:
        """
        Validate a mechanism YAML file.

        Args:
            mechanism_file: Path to mechanism YAML file

        Returns:
            Dict with 'errors' and 'warnings'
        """
        return validate_mechanism_file_nodes(mechanism_file, self.valid_node_ids)

    def validate_directory(
        self,
        mechanism_dir: Path,
        verbose: bool = True
    ) -> Dict[str, Dict[str, List[str]]]:
        """
        Validate all mechanism files in a directory.

        Args:
            mechanism_dir: Path to mechanisms directory
            verbose: Print progress

        Returns:
            Dict mapping filepath to validation results
        """
        results = {}
        yaml_files = list(mechanism_dir.rglob('*.yml')) + list(mechanism_dir.rglob('*.yaml'))

        if verbose:
            print(f"\n=== Validating node references in {len(yaml_files)} mechanism files ===\n")

        for yaml_file in yaml_files:
            result = self.validate_file(yaml_file)
            results[str(yaml_file)] = result

            if verbose and result['errors']:
                print(f"✗ {yaml_file.name}")
                for error in result['errors']:
                    print(f"  ERROR: {error}")
                for warning in result['warnings']:
                    print(f"  WARNING: {warning}")

        if verbose:
            error_count = sum(len(r['errors']) for r in results.values())
            files_with_errors = sum(1 for r in results.values() if r['errors'])
            print(f"\n=== Summary ===")
            print(f"Total files: {len(yaml_files)}")
            print(f"Files with node errors: {files_with_errors}")
            print(f"Total node errors: {error_count}")

        return results
