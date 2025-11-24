"""
Integration tests for mechanisms API endpoints.

Tests CRUD operations and filtering for mechanisms.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import Mechanism, Node


class TestMechanismsListEndpoint:
    """Tests for GET /api/mechanisms/ endpoint."""

    def test_list_mechanisms_empty(self, client: TestClient):
        """Test listing mechanisms when database is empty."""
        response = client.get("/api/mechanisms/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_mechanisms_with_data(self, client: TestClient, test_db: Session):
        """Test listing mechanisms with data in database."""
        # Create nodes
        node1 = Node(
            id="node1",
            name="Housing Quality",
            node_type="stock",
            category="built_environment"
        )
        node2 = Node(
            id="node2",
            name="Asthma Incidence",
            node_type="stock",
            category="health_outcome"
        )
        test_db.add(node1)
        test_db.add(node2)

        # Create mechanism
        mechanism = Mechanism(
            id="mech1",
            name="Housing Quality -> Asthma Incidence",
            from_node_id="node1",
            to_node_id="node2",
            direction="negative",
            category="built_environment",
            mechanism_pathway=["Poor housing increases asthma risk"],
            evidence_quality="A",
            evidence_n_studies=15,
            evidence_primary_citation="Smith et al. (2023)",
            description="Test mechanism showing housing quality impact on asthma"
        )
        test_db.add(mechanism)
        test_db.commit()

        # Test list
        response = client.get("/api/mechanisms/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "mech1"
        assert data[0]["name"] == "Housing Quality -> Asthma Incidence"
        assert data[0]["direction"] == "negative"
        assert data[0]["evidence_quality"] == "A"

    def test_filter_by_category(self, client: TestClient, test_db: Session):
        """Test filtering mechanisms by category."""
        # Create nodes
        node1 = Node(id="node1", name="Node 1", node_type="stock", category="test")
        node2 = Node(id="node2", name="Node 2", node_type="stock", category="test")
        node3 = Node(id="node3", name="Node 3", node_type="stock", category="test")
        test_db.add_all([node1, node2, node3])

        # Create mechanisms with different categories
        mech1 = Mechanism(
            id="mech1",
            name="Mechanism 1",
            from_node_id="node1",
            to_node_id="node2",
            direction="positive",
            category="built_environment",
            mechanism_pathway=["test"],
            evidence_quality="A",
            evidence_n_studies=5,
            evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
        mech2 = Mechanism(
            id="mech2",
            name="Mechanism 2",
            from_node_id="node2",
            to_node_id="node3",
            direction="negative",
            category="economic",
            mechanism_pathway=["test"],
            evidence_quality="B",
            evidence_n_studies=3,
            evidence_primary_citation="Test2 (2024)",
            description="Test mechanism"
        )
        test_db.add_all([mech1, mech2])
        test_db.commit()

        # Filter by category
        response = client.get("/api/mechanisms/?category=built_environment")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "mech1"

    def test_filter_by_direction(self, client: TestClient, test_db: Session):
        """Test filtering mechanisms by direction."""
        # Create nodes
        node1 = Node(id="node1", name="Node 1", node_type="stock", category="test")
        node2 = Node(id="node2", name="Node 2", node_type="stock", category="test")
        test_db.add_all([node1, node2])

        # Create mechanisms with different directions
        mech1 = Mechanism(
            id="mech1",
            name="Positive Mech",
            from_node_id="node1",
            to_node_id="node2",
            direction="positive",
            category="test",
            mechanism_pathway=["test"],
            evidence_quality="A",
            evidence_n_studies=5,
            evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
        mech2 = Mechanism(
            id="mech2",
            name="Negative Mech",
            from_node_id="node1",
            to_node_id="node2",
            direction="negative",
            category="test",
            mechanism_pathway=["test"],
            evidence_quality="A",
            evidence_n_studies=5,
            evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
        test_db.add_all([mech1, mech2])
        test_db.commit()

        # Filter by direction
        response = client.get("/api/mechanisms/?direction=positive")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "mech1"

    def test_pagination(self, client: TestClient, test_db: Session):
        """Test pagination with limit and offset."""
        # Create nodes
        nodes = [Node(id=f"node{i}", name=f"Node {i}", node_type="stock", category="test") for i in range(3)]
        test_db.add_all(nodes)

        # Create multiple mechanisms
        mechanisms = [
            Mechanism(
                id=f"mech{i}",
                name=f"Mechanism {i}",
                from_node_id="node0",
                to_node_id=f"node{i}",
                direction="positive",
                category="test",
                mechanism_pathway=["test"],
                evidence_quality="A",
                evidence_n_studies=5,
                evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
            for i in range(5)
        ]
        test_db.add_all(mechanisms)
        test_db.commit()

        # Test limit
        response = client.get("/api/mechanisms/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Test offset
        response = client.get("/api/mechanisms/?offset=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestMechanismDetailEndpoint:
    """Tests for GET /api/mechanisms/{mechanism_id} endpoint."""

    def test_get_mechanism_not_found(self, client: TestClient):
        """Test getting mechanism that doesn't exist."""
        response = client.get("/api/mechanisms/nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_mechanism_success(self, client: TestClient, test_db: Session):
        """Test getting mechanism details."""
        # Create nodes
        node1 = Node(
            id="node1",
            name="Housing Quality",
            node_type="stock",
            category="built_environment"
        )
        node2 = Node(
            id="node2",
            name="Asthma Incidence",
            node_type="stock",
            category="health_outcome"
        )
        test_db.add_all([node1, node2])

        # Create mechanism with full details
        mechanism = Mechanism(
            id="mech1",
            name="Housing Quality -> Asthma Incidence",
            from_node_id="node1",
            to_node_id="node2",
            direction="negative",
            category="built_environment",
            mechanism_pathway=[
                "Step 1: Poor housing quality increases indoor allergens",
                "Step 2: Allergen exposure triggers asthma symptoms"
            ],
            evidence_quality="A",
            evidence_n_studies=15,
            evidence_primary_citation="Smith et al. (2023)",
            evidence_supporting_citations=["Jones et al. (2022)", "Brown et al. (2021)"],
            evidence_doi="10.1234/test.2023",
            varies_by_geography=True,
            variation_notes="Effect stronger in urban areas",
            relevant_geographies=["urban", "suburban"],
            moderators=[
                {
                    "name": "income_level",
                    "direction": "strengthens",
                    "strength": "strong",
                    "evidence": "Lower income strengthens effect"
                }
            ],
            structural_competency_equity_implications="Disproportionately affects low-income populations",
            description="Detailed mechanism description"
        )
        test_db.add(mechanism)
        test_db.commit()

        # Get mechanism
        response = client.get("/api/mechanisms/mech1")
        assert response.status_code == 200
        data = response.json()

        # Check basic fields
        assert data["id"] == "mech1"
        assert data["name"] == "Housing Quality -> Asthma Incidence"
        assert data["direction"] == "negative"
        assert data["category"] == "built_environment"

        # Check evidence
        assert data["evidence"]["quality_rating"] == "A"
        assert data["evidence"]["n_studies"] == 15
        assert data["evidence"]["primary_citation"] == "Smith et al. (2023)"

        # Check pathway
        assert len(data["mechanism_pathway"]) == 2

        # Check moderators
        assert len(data["moderators"]) == 1
        assert data["moderators"][0]["name"] == "income_level"


class TestStatsEndpoint:
    """Tests for GET /api/mechanisms/stats/summary endpoint."""

    def test_stats_empty_database(self, client: TestClient):
        """Test statistics with empty database."""
        response = client.get("/api/mechanisms/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["total_mechanisms"] == 0
        assert data["total_nodes"] == 0

    def test_stats_with_data(self, client: TestClient, test_db: Session):
        """Test statistics with data."""
        # Create nodes
        nodes = [Node(id=f"node{i}", name=f"Node {i}", node_type="stock", category="test") for i in range(3)]
        test_db.add_all(nodes)

        # Create mechanisms with different categories and directions
        mech1 = Mechanism(
            id="mech1",
            name="Mech 1",
            from_node_id="node0",
            to_node_id="node1",
            direction="positive",
            category="built_environment",
            mechanism_pathway=["test"],
            evidence_quality="A",
            evidence_n_studies=5,
            evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
        mech2 = Mechanism(
            id="mech2",
            name="Mech 2",
            from_node_id="node1",
            to_node_id="node2",
            direction="negative",
            category="economic",
            mechanism_pathway=["test"],
            evidence_quality="B",
            evidence_n_studies=3,
            evidence_primary_citation="Test (2024)",
            description="Test mechanism"
        )
        test_db.add_all([mech1, mech2])
        test_db.commit()

        # Get stats
        response = client.get("/api/mechanisms/stats/summary")
        assert response.status_code == 200
        data = response.json()

        assert data["total_mechanisms"] == 2
        assert data["total_nodes"] == 3
        assert data["by_category"]["built_environment"] == 1
        assert data["by_category"]["economic"] == 1
        assert data["by_direction"]["positive"] == 1
        assert data["by_direction"]["negative"] == 1
        assert data["by_evidence_quality"]["A"] == 1
        assert data["by_evidence_quality"]["B"] == 1
