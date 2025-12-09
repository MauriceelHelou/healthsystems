"""
Application configuration management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM API Keys
    anthropic_api_key: Optional[str] = Field(default=None, validation_alias="ANTHROPIC_API_KEY")

    # Literature Search APIs
    semantic_scholar_api_key: Optional[str] = None
    pubmed_email: Optional[str] = None
    pubmed_api_key: Optional[str] = None

    # Application
    environment: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = int(os.getenv("PORT", "8000"))
    api_reload: bool = True
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3002", "http://localhost:8000", "http://localhost:8002"]

    # Database - explicitly check DATABASE_URL env var
    database_url: str = Field(
        default="sqlite:///./backend/healthsystems.db",
        validation_alias="DATABASE_URL"
    )
    database_test_url: Optional[str] = None

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_enabled: bool = True
    cache_ttl: int = 3600

    # Neo4j (Optional)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"

    # External APIs
    census_api_key: str = ""
    cdc_api_key: str = ""
    epa_api_key: str = ""
    bls_api_key: str = ""

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/healthsystems.log"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60

    # Data Scraping
    scraping_enabled: bool = True
    scraping_user_agent: str = "HealthSystemsPlatform/1.0"
    scraping_rate_limit: int = 1

    # Scientific Computing
    bayesian_mcmc_samples: int = 2000
    bayesian_mcmc_chains: int = 4
    bayesian_random_seed: int = 42

    # Feature Flags
    enable_graph_database: bool = False
    enable_real_time_updates: bool = False
    enable_export_reports: bool = True

    # Mechanism Bank Settings
    mechanism_bank_path: str = "../mechanism-bank/mechanisms"
    mvp_extraction_max_tokens: int = 4000
    mvp_extraction_model: str = "claude-opus-4-5-20251101"
    min_evidence_quality: str = "C"
    min_confidence: str = "medium"
    enable_structural_competency_check: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env
        populate_by_name = True  # Allow both alias and field name


settings = Settings()
