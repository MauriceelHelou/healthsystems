"""
API server configuration for FastAPI.
"""
import os
from typing import List


class APIConfig:
    """API server configuration settings."""

    def __init__(self):
        # Server settings
        self.host: str = os.getenv("API_HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
        self.reload: bool = os.getenv("API_RELOAD", "true").lower() == "true"
        self.workers: int = int(os.getenv("API_WORKERS", "1"))

        # Environment
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"

        # CORS settings
        self.cors_origins: List[str] = self._parse_cors_origins()
        self.cors_credentials: bool = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
        self.cors_methods: List[str] = self._parse_list(
            os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
        )
        self.cors_headers: List[str] = self._parse_list(
            os.getenv("CORS_HEADERS", "*")
        )

        # Rate limiting
        self.enable_rate_limiting: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        self.rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.enable_request_logging: bool = os.getenv("ENABLE_REQUEST_LOGGING", "true").lower() == "true"

    def _parse_cors_origins(self) -> List[str]:
        """Parse CORS origins from environment variable."""
        origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
        if origins_str == "*":
            return ["*"]
        return [origin.strip() for origin in origins_str.split(",") if origin.strip()]

    def _parse_list(self, value: str) -> List[str]:
        """Parse comma-separated list from string."""
        if value == "*":
            return ["*"]
        return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"


# Global API configuration instance
api_config = APIConfig()
