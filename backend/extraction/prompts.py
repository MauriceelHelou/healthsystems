"""
Prompt templates for mechanism extraction.
"""

GENERIC_EXTRACTION_PROMPT = """You are an expert in social epidemiology and public health systems.

Extract a causal mechanism from the following context.

TOPIC: {topic}
CATEGORY: {category}
FROM NODE: {from_node}
TO NODE: {to_node}

CONTEXT:
{source_context}

Return a valid JSON object with this exact structure:
{{
  "id": "unique_mechanism_id",
  "name": "Brief descriptive name",
  "from_node": {{
    "node_id": "{from_node}",
    "node_name": "Full name"
  }},
  "to_node": {{
    "node_id": "{to_node}",
    "node_name": "Full name"
  }},
  "category": "{category}",
  "direction": "positive or negative",
  "mechanism_pathway": ["step 1", "step 2", "step 3"],
  "evidence": {{
    "quality_rating": "A, B, or C",
    "n_studies": 0,
    "primary_citation": "Author et al. (Year). Title. Journal.",
    "supporting_citations": ["Citation 1", "Citation 2"],
    "doi": "10.xxxx/xxxxx"
  }},
  "description": "Detailed description of the mechanism"
}}
"""


def build_extraction_prompt(
    topic: str,
    category: str,
    from_node: str,
    to_node: str,
    source_context: str
) -> str:
    """
    Build extraction prompt from template.

    Args:
        topic: Topic area (e.g., "Alcoholism", "Obesity")
        category: Mechanism category
        from_node: Source node ID
        to_node: Target node ID
        source_context: Background context/literature

    Returns:
        Formatted prompt string
    """
    return GENERIC_EXTRACTION_PROMPT.format(
        topic=topic,
        category=category,
        from_node=from_node,
        to_node=to_node,
        source_context=source_context
    )
