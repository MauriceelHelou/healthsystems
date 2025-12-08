"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import logging

from api.config import settings

logger = logging.getLogger(__name__)

# Determine if we're using SQLite or PostgreSQL
database_url = settings.database_url
is_sqlite = database_url.startswith("sqlite")

# Create synchronous engine (for Alembic migrations and sync operations)
if is_sqlite:
    # SQLite uses synchronous engine
    sync_engine = create_engine(
        database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False} if is_sqlite else {}
    )
    # For SQLite, we use sync sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
    AsyncSessionLocal = None  # Not used for SQLite
    engine = sync_engine  # Alembic needs this
else:
    # PostgreSQL - create both sync and async engines
    # Sync engine for Alembic migrations
    sync_engine = create_engine(
        database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
    engine = sync_engine  # Alembic needs sync engine

    # Async engine for runtime operations
    async_database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        async_database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

# Base class for models
Base = declarative_base()


async def init_db():
    """Initialize database tables."""
    if is_sqlite:
        # For SQLite, use synchronous approach
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created (SQLite)")
    else:
        # For PostgreSQL, use async approach
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created (PostgreSQL)")


async def close_db():
    """Close database connections."""
    if is_sqlite:
        engine.dispose()
        logger.info("Database connections closed (SQLite)")
    else:
        await async_engine.dispose()
        logger.info("Database connections closed (PostgreSQL)")


def get_db():
    """
    Dependency for getting database sessions.

    For SQLite: Returns synchronous Session
    For PostgreSQL: Returns AsyncSession

    Yields:
        Session: Database session
    """
    if is_sqlite:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # For async PostgreSQL, this should be async
        # But FastAPI Depends works with both sync and async
        async def _get_async_db():
            async with AsyncSessionLocal() as session:
                try:
                    yield session
                finally:
                    await session.close()
        return _get_async_db()
