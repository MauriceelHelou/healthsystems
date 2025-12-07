#!/usr/bin/env python3
"""
Canonical Node Utilities

Provides access to the canonical 840-node inventory for use in
LLM extraction prompts and node matching.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import re

# Path to canonical nodes JSON
CANONICAL_NODES_PATH = Path(__file__).parent.parent / 'data' / 'canonical_nodes.json'

# Cache for loaded data
_cached_data: Optional[Dict] = None


def load_canonical_nodes() -> Dict:
    """Load and cache canonical nodes data."""
    global _cached_data
    if _cached_data is None:
        with open(CANONICAL_NODES_PATH, 'r') as f:
            _cached_data = json.load(f)
    return _cached_data


def get_all_nodes() -> List[Dict]:
    """Get list of all canonical nodes."""
    return load_canonical_nodes()['nodes']


def get_node_by_id(node_id: str) -> Optional[Dict]:
    """Get a node by its ID."""
    data = load_canonical_nodes()
    return data['by_id'].get(node_id)


def get_nodes_by_scale(scale: int) -> List[str]:
    """Get node IDs for a given scale."""
    data = load_canonical_nodes()
    return data['by_scale'].get(str(scale), [])


def get_nodes_by_domain(domain: str) -> List[str]:
    """Get node IDs for a given domain."""
    data = load_canonical_nodes()
    return data['by_domain'].get(domain, [])


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case node ID format."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matching_node(
    query: str,
    threshold: float = 0.7
) -> Tuple[Optional[Dict], float]:
    """
    Find best matching canonical node for a given query.

    Args:
        query: Node name or ID to match
        threshold: Minimum similarity score (default 0.7)

    Returns:
        Tuple of (matched_node, similarity_score) or (None, 0) if no match
    """
    nodes = get_all_nodes()
    normalized_query = normalize_node_id(query)

    best_match = None
    best_score = 0

    for node in nodes:
        # Check exact ID match
        if normalized_query == node['id']:
            return node, 1.0

        # Check exact name match (case-insensitive)
        if query.lower() == node['name'].lower():
            return node, 1.0

        # Fuzzy match on ID
        id_score = similarity(normalized_query, node['id'])
        if id_score > best_score:
            best_score = id_score
            best_match = node

        # Fuzzy match on name
        name_score = similarity(query, node['name'])
        if name_score > best_score:
            best_score = name_score
            best_match = node

    if best_score >= threshold:
        return best_match, best_score

    return None, 0


def generate_node_list_for_prompt(
    domains: Optional[List[str]] = None,
    scales: Optional[List[int]] = None,
    max_nodes: int = 200
) -> str:
    """
    Generate a formatted node list for inclusion in LLM prompts.

    Args:
        domains: Filter by domains (e.g., ['Housing', 'Healthcare System'])
        scales: Filter by scales (e.g., [1, 2, 5])
        max_nodes: Maximum nodes to include

    Returns:
        Formatted string for LLM prompt
    """
    nodes = get_all_nodes()

    # Filter by domain/scale if specified
    if domains:
        domains_lower = [d.lower() for d in domains]
        nodes = [n for n in nodes if n.get('domain', '').lower() in domains_lower]

    if scales:
        nodes = [n for n in nodes if n.get('scale') in scales]

    # Limit to max_nodes
    nodes = nodes[:max_nodes]

    # Format as compact list
    lines = []
    current_domain = None

    for node in nodes:
        domain = node.get('domain', 'Unknown')
        if domain != current_domain:
            if current_domain is not None:
                lines.append("")  # Empty line between domains
            lines.append(f"## {domain}")
            current_domain = domain

        lines.append(f"- {node['id']}: {node['name']}")

    return "\n".join(lines)


def generate_compact_node_list(max_per_domain: int = 15) -> str:
    """
    Generate a compact node list grouped by domain for LLM prompts.

    This creates a condensed format suitable for inclusion in extraction prompts.
    """
    data = load_canonical_nodes()
    nodes = data['nodes']

    # Group by domain
    by_domain: Dict[str, List[Dict]] = {}
    for node in nodes:
        domain = node.get('domain', 'Other')
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(node)

    lines = []
    for domain in sorted(by_domain.keys()):
        domain_nodes = by_domain[domain][:max_per_domain]
        node_ids = [n['id'] for n in domain_nodes]

        if len(by_domain[domain]) > max_per_domain:
            remaining = len(by_domain[domain]) - max_per_domain
            node_ids.append(f"...+{remaining} more")

        lines.append(f"**{domain}**: {', '.join(node_ids)}")

    return "\n".join(lines)


def get_scale_description(scale: int) -> str:
    """Get description for a scale number."""
    scales = {
        1: "Structural Determinants (policy, systemic)",
        2: "Institutional Infrastructure",
        3: "Individual/Household Conditions",
        4: "Intermediate Pathways",
        5: "Crisis Endpoints"
    }
    return scales.get(scale, f"Scale {scale}")


if __name__ == "__main__":
    # Test the utilities
    print("Canonical Nodes Utility Test\n")

    data = load_canonical_nodes()
    print(f"Total nodes: {len(data['nodes'])}")
    print(f"Domains: {len(data['by_domain'])}")
    print(f"Scales: {list(data['by_scale'].keys())}")

    # Test matching
    print("\n--- Node Matching Test ---")
    test_queries = [
        "medicaid expansion",
        "housing quality",
        "alcohol use",
        "respiratory_disease",
        "nonexistent_node_xyz"
    ]

    for query in test_queries:
        match, score = find_matching_node(query)
        if match:
            print(f"'{query}' → '{match['id']}' ({score:.0%})")
        else:
            print(f"'{query}' → No match")

    # Show compact list sample
    print("\n--- Compact Node List (sample) ---")
    print(generate_compact_node_list(max_per_domain=5))
