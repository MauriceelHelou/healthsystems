"""API routes for HealthSystems Platform."""

from api.routes.mechanisms import router as mechanisms_router
from api.routes.nodes import router as nodes_router
from api.routes.pathways import router as pathways_router

__all__ = ["mechanisms_router", "nodes_router", "pathways_router"]
