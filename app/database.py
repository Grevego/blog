from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

# Import Base from models to avoid circular import
from app.models.base import Base

# Create SQLAlchemy engine
def create_db_engine():
    """Create database engine with appropriate settings for SQLite or PostgreSQL."""
    database_url = settings.db_url
    
    if database_url.startswith("sqlite"):
        # SQLite specific settings
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},  # Needed for FastAPI
            echo=settings.debug,  # Log SQL queries in debug mode
        )
    else:
        # PostgreSQL settings
        engine = create_engine(
            database_url,
            echo=settings.debug,  # Log SQL queries in debug mode
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Validate connections before use
            pool_recycle=3600,   # Recycle connections every hour
        )
    
    return engine


# Create engine
engine = create_db_engine()

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base is imported from app.models.base to avoid circular imports


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables. Call this after importing all models."""
    # Import all models here to ensure they're registered with SQLAlchemy
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine) 