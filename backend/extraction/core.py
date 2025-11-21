"""
Core mechanism extraction logic.
Unified interface for single and batch extraction.
"""
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import json

from .llm_client import LLMClient
from .yaml_handler import write_mechanism_yaml
from .prompts import build_extraction_prompt
from .progress import ExtractionProgress


@dataclass
class ExtractionConfig:
    """Configuration for mechanism extraction."""
    topic: str
    category: str
    source_context: str
    output_dir: Path = Path("mechanism-bank/mechanisms")
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 16000
    temperature: float = 0.0
    max_retries: int = 3


class MechanismExtractor:
    """
    Unified mechanism extraction engine.
    Handles both single and batch extractions.
    """

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.llm_client = LLMClient(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )
        self.progress = ExtractionProgress()

    def extract_single(
        self,
        from_node: str,
        to_node: str,
        context: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Extract a single mechanism between two nodes.

        Args:
            from_node: Source node identifier
            to_node: Target node identifier
            context: Optional additional context

        Returns:
            Mechanism dict or None if extraction failed
        """
        # Build prompt
        prompt = build_extraction_prompt(
            topic=self.config.topic,
            category=self.config.category,
            from_node=from_node,
            to_node=to_node,
            source_context=context or self.config.source_context
        )

        # Call LLM with retries
        for attempt in range(self.config.max_retries):
            try:
                response = self.llm_client.call(prompt)
                mechanism = self._parse_response(response)

                if mechanism:
                    self.progress.record_success()
                    return mechanism

            except Exception as e:
                self.progress.record_error(str(e))
                if attempt == self.config.max_retries - 1:
                    print(f"Failed after {self.config.max_retries} attempts: {e}")
                    return None

        return None

    def extract_batch(
        self,
        node_pairs: List[tuple[str, str]],
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> List[Dict]:
        """
        Extract multiple mechanisms in batch.

        Args:
            node_pairs: List of (from_node, to_node) tuples
            on_progress: Optional callback for progress updates

        Returns:
            List of successfully extracted mechanisms
        """
        mechanisms = []

        for i, (from_node, to_node) in enumerate(node_pairs):
            mechanism = self.extract_single(from_node, to_node)

            if mechanism:
                mechanisms.append(mechanism)
                # Write immediately to avoid data loss
                self._write_mechanism(mechanism)

            # Progress callback
            if on_progress:
                on_progress(i + 1, len(node_pairs))

        return mechanisms

    def _parse_response(self, response: str) -> Optional[Dict]:
        """Parse LLM response into mechanism dict."""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start == -1 or end == 0:
                return None

            mechanism = json.loads(response[start:end])

            # Validate required fields
            required = ['id', 'name', 'from_node', 'to_node', 'category', 'direction']
            if not all(field in mechanism for field in required):
                return None

            return mechanism

        except json.JSONDecodeError:
            return None

    def _write_mechanism(self, mechanism: Dict):
        """Write mechanism to YAML file."""
        category_dir = self.config.output_dir / self.config.category
        write_mechanism_yaml(mechanism, category_dir)

    def get_summary(self) -> Dict:
        """Get extraction summary statistics."""
        return self.progress.get_summary()
