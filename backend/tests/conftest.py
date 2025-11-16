"""
Pytest configuration and fixtures.
"""

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from api.main import app
from models.database import Base, get_db


# Test database URL (use in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.

    Yields:
        AsyncSession: Test database session
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with database override.

    Args:
        test_db: Test database session

    Yields:
        AsyncClient: Test HTTP client
    """
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sample_mechanism_data():
    """Sample mechanism data for testing."""
    return {
        "id": "test_mechanism",
        "name": "Test Mechanism → Test Outcome",
        "category": "test_category",
        "mechanism_type": "test_type",
        "effect_size_measure": "odds_ratio",
        "effect_size_point": 1.5,
        "effect_size_ci_lower": 1.2,
        "effect_size_ci_upper": 1.8,
        "effect_size_unit": "per unit change",
        "evidence_quality": "A",
        "evidence_n_studies": 10,
        "evidence_citation": "Test et al. (2024)",
        "version": "1.0",
    }
