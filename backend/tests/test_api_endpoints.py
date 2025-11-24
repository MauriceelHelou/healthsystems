"""
Backend API endpoint tests for Crisis Explorer and Pathway Explorer.

Tests cover:
- Crisis endpoints API
- Crisis subgraph API
- Pathways API
- Mechanisms API performance
"""

import pytest
from fastapi.testclient import TestClient
import time
from api.main import app

client = TestClient(app)


class TestCrisisEndpointsAPI:
    """Test /api/nodes/crisis-endpoints endpoint"""

    def test_crisis_endpoints_returns_200(self):
        """Verify endpoint returns success status"""
        response = client.get("/api/nodes/crisis-endpoints")
        assert response.status_code == 200

    def test_crisis_endpoints_returns_array(self):
        """Verify endpoint returns array of crisis nodes"""
        response = client.get("/api/nodes/crisis-endpoints")
        data = response.json()
        assert isinstance(data, list)

    def test_crisis_endpoints_not_empty(self):
        """Verify at least one crisis endpoint exists"""
        response = client.get("/api/nodes/crisis-endpoints")
        data = response.json()
        assert len(data) > 0, "No crisis endpoints found in database"

    def test_crisis_endpoint_structure(self):
        """Verify crisis endpoint objects have required fields"""
        response = client.get("/api/nodes/crisis-endpoints")
        data = response.json()

        if len(data) > 0:
            endpoint = data[0]
            assert "nodeId" in endpoint
            assert "label" in endpoint
            assert "category" in endpoint
            assert "scale" in endpoint
            assert endpoint["scale"] == 7, "Crisis endpoints should have scale=7"

    def test_crisis_endpoints_performance(self):
        """Verify endpoint responds within 1 second"""
        start = time.time()
        response = client.get("/api/nodes/crisis-endpoints")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 1.0, f"Crisis endpoints took {elapsed:.2f}s (should be <1s)"


class TestCrisisSubgraphAPI:
    """Test /api/nodes/crisis-subgraph endpoint"""

    def test_crisis_subgraph_requires_post(self):
        """Verify endpoint requires POST method"""
        response = client.get("/api/nodes/crisis-subgraph")
        assert response.status_code in [405, 404]  # Method not allowed or not found

    def test_crisis_subgraph_requires_crisis_ids(self):
        """Verify endpoint requires crisisNodeIds parameter"""
        response = client.post("/api/nodes/crisis-subgraph", json={})
        assert response.status_code in [422, 400]  # Validation error

    def test_crisis_subgraph_with_valid_input(self):
        """Test subgraph generation with valid crisis node"""
        # First get available crisis endpoints
        endpoints_response = client.get("/api/nodes/crisis-endpoints")
        endpoints = endpoints_response.json()

        if len(endpoints) == 0:
            pytest.skip("No crisis endpoints available for testing")

        # Use first crisis endpoint
        crisis_id = endpoints[0]["nodeId"]

        payload = {
            "crisisNodeIds": [crisis_id],
            "maxDegrees": 3,
            "minStrength": 1
        }

        response = client.post("/api/nodes/crisis-subgraph", json=payload)
        assert response.status_code == 200

    def test_crisis_subgraph_response_structure(self):
        """Verify subgraph response has required structure"""
        endpoints_response = client.get("/api/nodes/crisis-endpoints")
        endpoints = endpoints_response.json()

        if len(endpoints) == 0:
            pytest.skip("No crisis endpoints available")

        payload = {
            "crisisNodeIds": [endpoints[0]["nodeId"]],
            "maxDegrees": 3,
            "minStrength": 1
        }

        response = client.post("/api/nodes/crisis-subgraph", json=payload)
        data = response.json()

        assert "nodes" in data
        assert "edges" in data
        assert "stats" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)
        assert isinstance(data["stats"], dict)

    def test_crisis_subgraph_performance(self):
        """Verify subgraph generation completes within 5 seconds"""
        endpoints_response = client.get("/api/nodes/crisis-endpoints")
        endpoints = endpoints_response.json()

        if len(endpoints) == 0:
            pytest.skip("No crisis endpoints available")

        payload = {
            "crisisNodeIds": [endpoints[0]["nodeId"]],
            "maxDegrees": 5,
            "minStrength": 2
        }

        start = time.time()
        response = client.post("/api/nodes/crisis-subgraph", json=payload)
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0, f"Crisis subgraph took {elapsed:.2f}s (should be <5s)"


class TestPathwaysAPI:
    """Test /api/pathways endpoint"""

    def test_pathways_returns_200(self):
        """Verify endpoint returns success status"""
        response = client.get("/api/pathways")
        assert response.status_code == 200

    def test_pathways_returns_array(self):
        """Verify endpoint returns array"""
        response = client.get("/api/pathways")
        data = response.json()
        assert isinstance(data, list)

    def test_pathways_accepts_limit(self):
        """Verify limit parameter works"""
        response = client.get("/api/pathways?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5

    def test_pathways_performance(self):
        """Verify pathways endpoint responds within 2 seconds"""
        start = time.time()
        response = client.get("/api/pathways?limit=10")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 2.0, f"Pathways took {elapsed:.2f}s (should be <2s)"

    def test_pathways_with_filters(self):
        """Test pathways with category filter"""
        response = client.get("/api/pathways?category=economic&limit=5")
        assert response.status_code == 200

    def test_pathway_structure_if_exists(self):
        """Verify pathway objects have required fields (if any pathways exist)"""
        response = client.get("/api/pathways?limit=1")
        data = response.json()

        if len(data) > 0:
            pathway = data[0]
            assert "pathwayId" in pathway
            assert "title" in pathway
            assert "fromNodeLabel" in pathway
            assert "toNodeLabel" in pathway
            assert "pathLength" in pathway
            assert "avgEvidenceQuality" in pathway


class TestMechanismsAPIPerformance:
    """Test mechanisms API performance (N+1 query fix verification)"""

    def test_mechanisms_returns_200(self):
        """Verify endpoint returns success"""
        response = client.get("/api/mechanisms/")
        assert response.status_code == 200

    def test_mechanisms_performance(self):
        """Verify mechanisms endpoint has good performance (no N+1 queries)"""
        start = time.time()
        response = client.get("/api/mechanisms/?limit=100")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 2.0, f"Mechanisms took {elapsed:.2f}s (should be <2s with selectinload fix)"

    def test_mechanisms_returns_node_names(self):
        """Verify mechanism objects include from_node_name and to_node_name"""
        response = client.get("/api/mechanisms/?limit=10")
        data = response.json()

        if len(data) > 0:
            mechanism = data[0]
            assert "from_node_name" in mechanism
            assert "to_node_name" in mechanism
            assert "from_node_id" in mechanism
            assert "to_node_id" in mechanism


class TestPathfindingAPI:
    """Test /api/nodes/pathfinding endpoint"""

    def test_pathfinding_requires_post(self):
        """Verify endpoint requires POST"""
        response = client.get("/api/nodes/pathfinding")
        assert response.status_code in [405, 404]

    def test_pathfinding_with_valid_nodes(self):
        """Test pathfinding between two nodes"""
        # Get some nodes to test with
        mechanisms_response = client.get("/api/mechanisms/?limit=1")
        mechanisms = mechanisms_response.json()

        if len(mechanisms) == 0:
            pytest.skip("No mechanisms available for pathfinding test")

        from_node = mechanisms[0]["from_node_id"]
        to_node = mechanisms[0]["to_node_id"]

        payload = {
            "from_node": from_node,
            "to_node": to_node,
            "algorithm": "shortest",
            "max_depth": 5
        }

        response = client.post("/api/nodes/pathfinding", json=payload)
        # Should return 200 even if no path found
        assert response.status_code == 200

    def test_pathfinding_response_structure(self):
        """Verify pathfinding response structure"""
        mechanisms_response = client.get("/api/mechanisms/?limit=10")
        mechanisms = mechanisms_response.json()

        if len(mechanisms) < 2:
            pytest.skip("Need at least 2 mechanisms for test")

        payload = {
            "from_node": mechanisms[0]["from_node_id"],
            "to_node": mechanisms[1]["to_node_id"],
            "algorithm": "shortest",
            "max_depth": 5
        }

        response = client.post("/api/nodes/pathfinding", json=payload)
        data = response.json()

        assert "fromNode" in data
        assert "toNode" in data
        assert "algorithm" in data
        assert "pathsFound" in data
        assert "paths" in data
        assert isinstance(data["paths"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
