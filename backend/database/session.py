"""Database session lifecycle and engine setup supporting MySQL and SQLite."""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.core.config import settings
from backend.core.logging import logger

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding database session per request."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initializes tables for development/testing if they don't already exist."""
    from backend.database.base import Base
    import backend.models  # Ensures all models are imported and registered
    logger.info(f"Initializing database schema on {settings.DATABASE_URL.split('://')[0]}...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema initialized successfully.")
