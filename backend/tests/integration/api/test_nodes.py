"""
Simple test route for nodes.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/nodes-test", tags=["nodes-test"])


@router.get("/hello")
def test_hello():
    """Test endpoint"""
    return {"message": "Nodes router is working!"}
