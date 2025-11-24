"""
LLM configuration for Anthropic Claude API.
"""
import os
from typing import Optional


class LLMConfig:
    """LLM configuration settings."""

    def __init__(self):
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "8192"))
        self.temperature: float = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7"))
        self.timeout: int = int(os.getenv("ANTHROPIC_TIMEOUT", "60"))

        # Rate limiting
        self.requests_per_minute: int = int(os.getenv("ANTHROPIC_RPM", "50"))
        self.tokens_per_minute: int = int(os.getenv("ANTHROPIC_TPM", "40000"))

        # Retry settings
        self.max_retries: int = int(os.getenv("ANTHROPIC_MAX_RETRIES", "3"))
        self.retry_delay: int = int(os.getenv("ANTHROPIC_RETRY_DELAY", "2"))

        # Feature flags
        self.enable_caching: bool = os.getenv("ANTHROPIC_ENABLE_CACHING", "true").lower() == "true"
        self.enable_logging: bool = os.getenv("ANTHROPIC_ENABLE_LOGGING", "false").lower() == "true"

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )
        return True

    @property
    def is_configured(self) -> bool:
        """Check if LLM is properly configured."""
        return bool(self.anthropic_api_key)


# Global LLM configuration instance
llm_config = LLMConfig()
