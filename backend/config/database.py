"""
Database configuration for PostgreSQL/SQLite connections.
"""
import os
from typing import Optional


class DatabaseConfig:
    """Database configuration settings."""

    def __init__(self):
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql://localhost/healthsystems"
        )
        self.database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
        self.pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
        self.max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))
        self.pool_timeout: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
        self.pool_recycle: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))

    @property
    def is_sqlite(self) -> bool:
        """Check if database is SQLite."""
        return self.database_url.startswith("sqlite")

    @property
    def is_postgresql(self) -> bool:
        """Check if database is PostgreSQL."""
        return self.database_url.startswith("postgresql")

    def get_engine_args(self) -> dict:
        """Get SQLAlchemy engine arguments based on database type."""
        args = {
            "echo": self.database_echo,
        }

        if self.is_postgresql:
            args.update({
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
            })

        return args


# Global database configuration instance
db_config = DatabaseConfig()
