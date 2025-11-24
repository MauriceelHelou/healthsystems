"""
Tests for the focal subgraph API endpoint.

Tests cover:
- Bidirectional traversal (upstream + downstream)
- Upstream-only traversal
- Downstream-only traversal
- Category filtering
- Scale filtering
- Evidence quality filtering
- Max hops limits
- Error handling (nonexistent focal node)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import Mechanism, Node


@pytest.fixture
def setup_test_graph(test_db: Session):
    """Set up a small test graph for focal subgraph testing."""
    # Create nodes at different scales
    nodes = [
        Node(id="policy_1", name="Policy Intervention", node_type="stock", category="political", scale=1),
        Node(id="env_2", name="Environmental Factor", node_type="stock", category="built_environment", scale=2),
        Node(id="econ_3", name="Economic Condition", node_type="stock", category="economic", scale=3),
        Node(id="stress_5", name="Chronic Stress", node_type="stock", category="psychosocial", scale=5),
        Node(id="behavior_5", name="Health Behavior", node_type="stock", category="behavioral", scale=5),
        Node(id="pathway_6", name="Healthcare Access", node_type="stock", category="healthcare_access", scale=6),
        Node(id="crisis_7", name="Mortality", node_type="stock", category="crisis", scale=7),
    ]
    test_db.add_all(nodes)

    # Create mechanisms forming a chain
    mechanisms = [
        Mechanism(
            id="m1", name="Policy -> Environment", from_node_id="policy_1", to_node_id="env_2",
            direction="positive", category="political", mechanism_pathway=["test"],
            evidence_quality="A", evidence_n_studies=10, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
        Mechanism(
            id="m2", name="Environment -> Economic", from_node_id="env_2", to_node_id="econ_3",
            direction="positive", category="economic", mechanism_pathway=["test"],
            evidence_quality="B", evidence_n_studies=8, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
        Mechanism(
            id="m3", name="Economic -> Stress", from_node_id="econ_3", to_node_id="stress_5",
            direction="negative", category="psychosocial", mechanism_pathway=["test"],
            evidence_quality="A", evidence_n_studies=12, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
        Mechanism(
            id="m4", name="Stress -> Behavior", from_node_id="stress_5", to_node_id="behavior_5",
            direction="negative", category="behavioral", mechanism_pathway=["test"],
            evidence_quality="A", evidence_n_studies=15, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
        Mechanism(
            id="m5", name="Behavior -> Healthcare", from_node_id="behavior_5", to_node_id="pathway_6",
            direction="positive", category="healthcare_access", mechanism_pathway=["test"],
            evidence_quality="B", evidence_n_studies=7, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
        Mechanism(
            id="m6", name="Healthcare -> Mortality", from_node_id="pathway_6", to_node_id="crisis_7",
            direction="negative", category="clinical", mechanism_pathway=["test"],
            evidence_quality="A", evidence_n_studies=20, evidence_primary_citation="Test (2024)",
            description="Test"
        ),
    ]
    test_db.add_all(mechanisms)
    test_db.commit()
    return nodes, mechanisms


def test_focal_subgraph_with_test_data(client: TestClient, test_db: Session, setup_test_graph):
    """Test focal subgraph endpoint with actual test data."""
    nodes, mechanisms = setup_test_graph

    # Test both directions from middle node
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "stress_5",
        "traversal_direction": "both",
        "max_hops_upstream": 2,
        "max_hops_downstream": 2
    })

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "focal_node" in data
    assert "nodes" in data
    assert "edges" in data
    assert "stats" in data

    # Verify focal node
    assert data["focal_node"]["id"] == "stress_5"
    assert data["focal_node"]["name"] == "Chronic Stress"

    # Verify we have both upstream and downstream nodes
    stats = data["stats"]
    assert stats["focal_node_id"] == "stress_5"
    assert stats["traversal_direction"] == "both"
    assert stats["nodes_upstream"] > 0
    assert stats["nodes_downstream"] > 0

    # Should include upstream nodes (econ_3, env_2) and downstream nodes (behavior_5, pathway_6)
    node_ids = [n["id"] for n in data["nodes"]]
    assert "econ_3" in node_ids  # 1 hop upstream
    assert "behavior_5" in node_ids  # 1 hop downstream

    # Should have mechanisms connecting these nodes
    assert len(data["edges"]) > 0


def test_focal_subgraph_upstream_only_with_data(client: TestClient, test_db: Session, setup_test_graph):
    """Test upstream traversal with test data."""
    nodes, mechanisms = setup_test_graph

    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "stress_5",
        "traversal_direction": "upstream",
        "max_hops_upstream": 2
    })

    assert response.status_code == 200
    data = response.json()

    stats = data["stats"]
    assert stats["traversal_direction"] == "upstream"
    assert stats["nodes_downstream"] == 0
    assert stats["nodes_upstream"] > 0

    # Should have upstream nodes but not downstream ones
    node_ids = [n["id"] for n in data["nodes"]]
    assert "econ_3" in node_ids  # Upstream
    assert "behavior_5" not in node_ids  # Downstream should be excluded


def test_focal_subgraph_downstream_only_with_data(client: TestClient, test_db: Session, setup_test_graph):
    """Test downstream traversal with test data."""
    nodes, mechanisms = setup_test_graph

    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "stress_5",
        "traversal_direction": "downstream",
        "max_hops_downstream": 2
    })

    assert response.status_code == 200
    data = response.json()

    stats = data["stats"]
    assert stats["traversal_direction"] == "downstream"
    assert stats["nodes_upstream"] == 0
    assert stats["nodes_downstream"] > 0

    # Should have downstream nodes but not upstream ones
    node_ids = [n["id"] for n in data["nodes"]]
    assert "behavior_5" in node_ids  # Downstream
    assert "econ_3" not in node_ids  # Upstream should be excluded


def test_focal_subgraph_category_filter_with_data(client: TestClient, test_db: Session, setup_test_graph):
    """Test category filtering with test data."""
    nodes, mechanisms = setup_test_graph

    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "stress_5",
        "traversal_direction": "both",
        "include_categories": ["behavioral", "healthcare_access"]
    })

    assert response.status_code == 200
    data = response.json()

    # All mechanisms should be in allowed categories
    for edge in data["edges"]:
        assert edge["category"] in ["behavioral", "healthcare_access"], \
            f"Edge {edge['id']} has category {edge['category']} not in allowed list"


def test_focal_subgraph_evidence_filter_with_data(client: TestClient, test_db: Session, setup_test_graph):
    """Test evidence quality filtering with test data."""
    nodes, mechanisms = setup_test_graph

    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "stress_5",
        "traversal_direction": "both",
        "min_evidence_quality": "A"
    })

    assert response.status_code == 200
    data = response.json()

    # All mechanisms should have evidence quality A
    for edge in data["edges"]:
        assert edge["evidence_quality"] == "A", \
            f"Edge {edge['id']} has evidence quality {edge['evidence_quality']}, expected A"


def test_focal_subgraph_both_directions(client: TestClient):
    """Test bidirectional traversal from a focal node."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "both",
        "max_hops_upstream": 2,
        "max_hops_downstream": 2
    })

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "focal_node" in data
    assert "nodes" in data
    assert "edges" in data
    assert "stats" in data

    # Verify focal node
    assert data["focal_node"]["id"] == "chronic_stress"

    # Verify stats
    stats = data["stats"]
    assert stats["focal_node_id"] == "chronic_stress"
    assert "total_nodes" in stats
    assert "total_mechanisms" in stats
    assert "nodes_upstream" in stats
    assert "nodes_downstream" in stats
    assert stats["traversal_direction"] == "both"

    # Should have nodes in both directions
    assert stats["nodes_upstream"] > 0
    assert stats["nodes_downstream"] > 0

    # Total nodes should be sum of upstream + downstream + focal node
    assert stats["total_nodes"] == stats["nodes_upstream"] + stats["nodes_downstream"] + 1


def test_focal_subgraph_upstream_only(client: TestClient):
    """Test upstream traversal (causes of focal node)."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "alcohol_use_disorder",
        "traversal_direction": "upstream",
        "max_hops_upstream": 3
    })

    assert response.status_code == 200
    data = response.json()

    stats = data["stats"]
    assert stats["focal_node_id"] == "alcohol_use_disorder"
    assert stats["traversal_direction"] == "upstream"

    # Should have no downstream nodes
    assert stats["nodes_downstream"] == 0

    # Should have upstream nodes
    assert stats["nodes_upstream"] > 0

    # Total nodes should be upstream + focal node
    assert stats["total_nodes"] == stats["nodes_upstream"] + 1


def test_focal_subgraph_downstream_only(client: TestClient):
    """Test downstream traversal (effects of focal node)."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "housing_instability",
        "traversal_direction": "downstream",
        "max_hops_downstream": 3
    })

    assert response.status_code == 200
    data = response.json()

    stats = data["stats"]
    assert stats["focal_node_id"] == "housing_instability"
    assert stats["traversal_direction"] == "downstream"

    # Should have no upstream nodes
    assert stats["nodes_upstream"] == 0

    # Should have downstream nodes
    assert stats["nodes_downstream"] > 0

    # Total nodes should be downstream + focal node
    assert stats["total_nodes"] == stats["nodes_downstream"] + 1


def test_focal_subgraph_category_filter(client: TestClient):
    """Test category filtering in traversal."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "housing_instability",
        "traversal_direction": "downstream",
        "include_categories": ["economic", "behavioral", "healthcare_access"]
    })

    assert response.status_code == 200
    data = response.json()

    # All mechanisms should be in allowed categories
    for edge in data["edges"]:
        assert edge["category"] in ["economic", "behavioral", "healthcare_access"], \
            f"Edge {edge['id']} has category {edge['category']} not in allowed list"


def test_focal_subgraph_scale_filter(client: TestClient):
    """Test scale filtering."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "economic_hardship",
        "traversal_direction": "downstream",
        "include_scales": [4, 5, 7]  # Only household, behavioral, crisis
    })

    assert response.status_code == 200
    data = response.json()

    # All nodes should have scale in [4, 5, 7]
    for node in data["nodes"]:
        assert node["scale"] in [4, 5, 7], \
            f"Node {node['id']} has scale {node['scale']} not in allowed list [4, 5, 7]"

    # Stats should show only these scales
    stats = data["stats"]
    for scale in stats["scales_present"]:
        assert scale in [4, 5, 7]


def test_focal_subgraph_evidence_filter(client: TestClient):
    """Test evidence quality filtering."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "both",
        "min_evidence_quality": "B"
    })

    assert response.status_code == 200
    data = response.json()

    # All mechanisms should have evidence quality A or B
    for edge in data["edges"]:
        if edge["evidence_quality"] is not None:
            assert edge["evidence_quality"] in ["A", "B"], \
                f"Edge {edge['id']} has evidence quality {edge['evidence_quality']}, expected A or B"


def test_focal_subgraph_max_hops_upstream(client: TestClient):
    """Test max hops upstream limit."""
    # Test with max_hops_upstream = 1
    response_1_hop = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "upstream",
        "max_hops_upstream": 1
    })

    # Test with max_hops_upstream = 3
    response_3_hops = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "upstream",
        "max_hops_upstream": 3
    })

    assert response_1_hop.status_code == 200
    assert response_3_hops.status_code == 200

    data_1_hop = response_1_hop.json()
    data_3_hops = response_3_hops.json()

    # 3 hops should return more or equal nodes than 1 hop
    assert data_3_hops["stats"]["nodes_upstream"] >= data_1_hop["stats"]["nodes_upstream"]


def test_focal_subgraph_max_hops_downstream(client: TestClient):
    """Test max hops downstream limit."""
    # Test with max_hops_downstream = 1
    response_1_hop = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "housing_instability",
        "traversal_direction": "downstream",
        "max_hops_downstream": 1
    })

    # Test with max_hops_downstream = 3
    response_3_hops = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "housing_instability",
        "traversal_direction": "downstream",
        "max_hops_downstream": 3
    })

    assert response_1_hop.status_code == 200
    assert response_3_hops.status_code == 200

    data_1_hop = response_1_hop.json()
    data_3_hops = response_3_hops.json()

    # 3 hops should return more or equal nodes than 1 hop
    assert data_3_hops["stats"]["nodes_downstream"] >= data_1_hop["stats"]["nodes_downstream"]


def test_focal_subgraph_nonexistent_node(client: TestClient):
    """Test error handling for nonexistent focal node."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "nonexistent_node_12345",
        "traversal_direction": "both"
    })

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_focal_subgraph_default_values(client: TestClient):
    """Test endpoint with minimal parameters (using defaults)."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress"
    })

    assert response.status_code == 200
    data = response.json()

    # Should use default traversal_direction = "both"
    assert data["stats"]["traversal_direction"] == "both"

    # Should have both upstream and downstream nodes (unless focal node is isolated)
    stats = data["stats"]
    assert stats["nodes_upstream"] >= 0
    assert stats["nodes_downstream"] >= 0


def test_focal_subgraph_combined_filters(client: TestClient):
    """Test multiple filters applied together."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "housing_instability",
        "traversal_direction": "downstream",
        "max_hops_downstream": 2,
        "include_categories": ["behavioral", "healthcare_access", "clinical"],
        "include_scales": [5, 6, 7],
        "min_evidence_quality": "B"
    })

    assert response.status_code == 200
    data = response.json()

    # Verify all filters are applied
    for edge in data["edges"]:
        # Category filter
        assert edge["category"] in ["behavioral", "healthcare_access", "clinical"]

        # Evidence quality filter
        if edge["evidence_quality"] is not None:
            assert edge["evidence_quality"] in ["A", "B"]

    for node in data["nodes"]:
        # Scale filter
        assert node["scale"] in [5, 6, 7]

    # Stats should reflect filters
    stats = data["stats"]
    assert stats["traversal_direction"] == "downstream"
    assert stats["nodes_upstream"] == 0


def test_focal_subgraph_response_structure(client: TestClient):
    """Test that response has correct structure with all required fields."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "both"
    })

    assert response.status_code == 200
    data = response.json()

    # Check top-level structure
    assert "focal_node" in data
    assert "nodes" in data
    assert "edges" in data
    assert "stats" in data

    # Check focal_node structure
    focal_node = data["focal_node"]
    assert "id" in focal_node
    assert "name" in focal_node
    assert "category" in focal_node
    assert "scale" in focal_node

    # Check nodes structure (if any nodes exist)
    if len(data["nodes"]) > 0:
        node = data["nodes"][0]
        assert "id" in node
        assert "name" in node
        assert "category" in node
        assert "scale" in node

    # Check edges structure (if any edges exist)
    if len(data["edges"]) > 0:
        edge = data["edges"][0]
        assert "id" in edge
        assert "name" in edge
        assert "from_node_id" in edge
        assert "to_node_id" in edge
        assert "direction" in edge
        assert "category" in edge

    # Check stats structure
    stats = data["stats"]
    assert "focal_node_id" in stats
    assert "focal_node_scale" in stats
    assert "total_nodes" in stats
    assert "total_mechanisms" in stats
    assert "nodes_upstream" in stats
    assert "nodes_downstream" in stats
    assert "traversal_direction" in stats
    assert "scales_present" in stats


def test_focal_subgraph_unlimited_hops(client: TestClient):
    """Test traversal with no hop limits (unlimited)."""
    response = client.post("/api/nodes/focal-subgraph", json={
        "focal_node_id": "chronic_stress",
        "traversal_direction": "both"
        # No max_hops_upstream or max_hops_downstream specified
    })

    assert response.status_code == 200
    data = response.json()

    # Should successfully traverse without hop limits
    assert data["stats"]["total_nodes"] > 0
