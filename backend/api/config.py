"""
Application configuration management.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    environment: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    database_url: str = "postgresql://healthsystems_user:changeme@localhost:5432/healthsystems"

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

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
