"""
Test script for Crisis Endpoint Explorer endpoints.
Tests both GET /api/nodes/crisis-endpoints and POST /api/nodes/crisis-subgraph.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_crisis_endpoints():
    """Test GET /api/nodes/crisis-endpoints"""
    print("\n" + "="*60)
    print("TEST 1: GET /api/nodes/crisis-endpoints")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/api/nodes/crisis-endpoints")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Found {len(data)} crisis endpoints")

            if len(data) > 0:
                print(f"\nSample Crisis Endpoint:")
                print(json.dumps(data[0], indent=2))
                return data
            else:
                print("[WARNING] No crisis endpoints found in database")
                return []
        else:
            print(f"[FAILED] {response.text}")
            return None

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

def test_crisis_subgraph(crisis_node_ids=None):
    """Test POST /api/nodes/crisis-subgraph"""
    print("\n" + "="*60)
    print("TEST 2: POST /api/nodes/crisis-subgraph")
    print("="*60)

    # Use provided IDs or create test request
    if not crisis_node_ids:
        print("[WARNING] No crisis node IDs provided, using test IDs")
        crisis_node_ids = ["test_node_1"]

    request_data = {
        "crisis_node_ids": crisis_node_ids[:3],  # Test with max 3 nodes
        "max_degrees": 5,
        "min_strength": 2
    }

    print(f"\nRequest Payload:")
    print(json.dumps(request_data, indent=2))

    try:
        response = requests.post(
            f"{BASE_URL}/api/nodes/crisis-subgraph",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] SUCCESS - Subgraph generated")
            print(f"\nSubgraph Statistics:")
            if "stats" in data:
                stats = data["stats"]
                print(f"  Total Nodes: {stats.get('totalNodes', 'N/A')}")
                print(f"  Total Edges: {stats.get('totalEdges', 'N/A')}")
                print(f"  Policy Levers: {stats.get('policyLevers', 'N/A')}")
                print(f"  Avg Degree: {stats.get('avgDegree', 'N/A')}")

            if "nodes" in data:
                print(f"  Nodes in response: {len(data['nodes'])}")
                if len(data['nodes']) > 0:
                    print(f"\n  Sample Node:")
                    print(f"    {json.dumps(data['nodes'][0], indent=4)}")

            if "edges" in data:
                print(f"  Edges in response: {len(data['edges'])}")

            return data
        else:
            print(f"[FAILED] FAILED - {response.text}")
            return None

    except Exception as e:
        print(f"[FAILED] ERROR - {str(e)}")
        return None

def test_invalid_requests():
    """Test validation and error handling"""
    print("\n" + "="*60)
    print("TEST 3: Validation & Error Handling")
    print("="*60)

    test_cases = [
        {
            "name": "Empty crisis_node_ids array",
            "payload": {"crisis_node_ids": [], "max_degrees": 5},
            "expected_status": 422
        },
        {
            "name": "Too many crisis nodes (>10)",
            "payload": {
                "crisis_node_ids": [f"node_{i}" for i in range(15)],
                "max_degrees": 5
            },
            "expected_status": 422
        },
        {
            "name": "Invalid max_degrees (>8)",
            "payload": {"crisis_node_ids": ["node_1"], "max_degrees": 20},
            "expected_status": 422
        },
        {
            "name": "Invalid min_strength (>3)",
            "payload": {
                "crisis_node_ids": ["node_1"],
                "max_degrees": 5,
                "min_strength": 10
            },
            "expected_status": 422
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test 3.{i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/nodes/crisis-subgraph",
                json=test_case['payload'],
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == test_case['expected_status']:
                print(f"    [SUCCESS] Correct validation - Status {response.status_code}")
            else:
                print(f"    [FAILED] Expected {test_case['expected_status']}, got {response.status_code}")
                print(f"       Response: {response.text[:200]}")
        except Exception as e:
            print(f"    [FAILED] Error: {str(e)}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CRISIS ENDPOINT EXPLORER - API TESTING")
    print("="*60)

    # Test 1: Get crisis endpoints
    crisis_endpoints = test_crisis_endpoints()

    # Test 2: Generate crisis subgraph
    if crisis_endpoints:
        # Extract node IDs from crisis endpoints
        crisis_ids = [node.get("nodeId") or node.get("id") for node in crisis_endpoints[:3]]
        test_crisis_subgraph(crisis_ids)
    else:
        print("\n[WARNING]  Skipping subgraph test - no crisis endpoints available")

    # Test 3: Validation
    test_invalid_requests()

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
