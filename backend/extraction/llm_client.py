"""
LLM client for mechanism extraction.
Handles API calls to Anthropic Claude.
"""
import os
from anthropic import Anthropic
from typing import Optional


class LLMClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 16000,
        temperature: float = 0.0,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def call(self, prompt: str) -> str:
        """
        Call LLM with prompt and return response text.

        Args:
            prompt: Input prompt

        Returns:
            Response text content

        Raises:
            Exception: If API call fails
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text
