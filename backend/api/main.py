"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from api.config import settings
from api.middleware.logging import LoggingMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
# from api.routes import mechanisms, contexts, weights, visualizations, health
from models.database import init_db, close_db

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting HealthSystems Platform API...")
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    yield

    logger.info("Shutting down HealthSystems Platform API...")
    try:
        await close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Database shutdown failed: {e}")


# Create FastAPI application
app = FastAPI(
    title="HealthSystems Platform API",
    description=(
        "Decision support platform for quantifying how structural interventions "
        "propagate through social-spatial-biological systems to affect health outcomes."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(LoggingMiddleware)

if settings.rate_limit_enabled:
    app.add_middleware(RateLimitMiddleware)

# Include routers
from api.routes import mechanisms_router, nodes_router, pathways_router

app.include_router(mechanisms_router)
logger.info(f"Mechanisms router included with {len(mechanisms_router.routes)} routes")
app.include_router(nodes_router)
logger.info(f"Nodes router included with {len(nodes_router.routes)} routes: {[r.path for r in nodes_router.routes]}")
app.include_router(pathways_router)
logger.info(f"Pathways router included with {len(pathways_router.routes)} routes")
# app.include_router(contexts.router, prefix="/api/contexts", tags=["Contexts"])
# app.include_router(weights.router, prefix="/api/weights", tags=["Weights"])
# app.include_router(visualizations.router, prefix="/api/visualizations", tags=["Visualizations"])


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "HealthSystems Platform API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring.

    Returns:
        Health status and system information
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.environment,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )

