"""
Pytest configuration and fixtures.
"""

import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Set test database URL BEFORE importing any app code
# Using a file-based test database so it can be shared across connections
TEST_DATABASE_URL = "sqlite:///./test_healthsystems.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from api.main import app
from models.database import Base, get_db, engine
# Import all models to ensure they're registered with Base.metadata
from models.mechanism import Mechanism, Node, GeographicContext  # noqa: F401


@pytest.fixture(scope="function", autouse=True)
def test_db() -> Generator[Session, None, None]:
    """
    Create a test database session.

    This fixture runs before every test to ensure a clean database state.

    Yields:
        Session: Test database session
    """
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Rollback any uncommitted changes
        db.close()
        # Clean all data from tables (but keep the tables)
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()


@pytest.fixture
def client(test_db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database override.

    Args:
        test_db: Test database session

    Yields:
        TestClient: Test HTTP client
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # test_db is managed by test_db fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def sample_node_data():
    """Sample node data for testing."""
    return {
        "id": "test_node_1",
        "name": "Test Node 1",
        "node_type": "stock",
        "category": "test_category",
        "description": "A test node"
    }


@pytest.fixture
def sample_mechanism_data():
    """Sample mechanism data for testing (MVP - topology & direction only)."""
    return {
        "id": "test_mechanism",
        "name": "Test Exposure -> Test Outcome",
        "from_node_id": "test_node_1",
        "to_node_id": "test_node_2",
        "direction": "positive",
        "category": "built_environment",
        "mechanism_pathway": [
            "Step 1: Test exposure affects intermediate factor",
            "Step 2: Intermediate factor impacts outcome"
        ],
        "evidence_quality": "A",
        "evidence_n_studies": 10,
        "evidence_primary_citation": "Test et al. (2024)",
        "evidence_supporting_citations": ["Test2 et al. (2023)", "Test3 et al. (2022)"],
        "evidence_doi": "10.1234/test.2024",
        "varies_by_geography": True,
        "variation_notes": "Effect stronger in urban areas",
        "relevant_geographies": ["urban", "suburban"],
        "moderators": [
            {
                "name": "income_level",
                "direction": "strengthens",
                "strength": "strong",
                "evidence": "Higher income strengthens effect"
            }
        ],
        "structural_competency_equity_implications": "This mechanism disproportionately affects low-income populations",
        "description": "A test mechanism showing causal pathway",
        "version": "1.0"
    }
