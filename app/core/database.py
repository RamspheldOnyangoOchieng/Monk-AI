import os
import time
import logging
from typing import Generator, Any, Dict
from contextlib import contextmanager
from sqlalchemy import create_engine, text, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Get database URL from settings
DATABASE_URL = settings.DATABASE_URI

# Configure engine with optimized pooling settings
engine = create_engine(
    DATABASE_URL,
    # For SQLite, connect_args needed for multi-threading
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    # Pool settings
    poolclass=QueuePool,
    pool_size=10,  # Maximum number of connections to keep open
    max_overflow=20,  # Maximum number of connections to create above pool_size
    pool_timeout=30,  # Seconds to wait before timeout on getting connection from pool
    pool_recycle=1800,  # Recycle connections after this many seconds
    pool_pre_ping=True  # Check connection before using from pool
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Set up connection events for monitoring and diagnostics
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > 0.5:  # Log slow queries (>500ms)
        logger.warning(f"Slow query ({total:.2f}s): {statement}")

def get_db() -> Generator[Session, None, None]:
    """
    Get database session generator.
    
    Usage:
        db = next(get_db())
        try:
            # use db
        finally:
            db.close()
            
    Or with FastAPI dependency:
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_transaction():
    """
    Context manager for database transactions.
    
    Usage:
        with db_transaction() as db:
            db.add(some_object)
            # Will automatically commit or rollback
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
def execute_with_retry(query: str, params: Dict[str, Any] = None) -> Any:
    """Execute raw SQL with retry logic for transient database errors."""
    with db_transaction() as db:
        result = db.execute(text(query), params or {})
        return result

def init_db() -> None:
    """Initialize the database by creating all tables."""
    try:
        # Import all models here to ensure they're registered with Base
        # For example:
        # from app.models.user import User
        # from app.models.item import Item
        
        # Create all tables (use Alembic for migrations in production)
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def check_db_connection() -> bool:
    """Check if the database connection is working."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return False

def create_demo_data() -> None:
    """Create demo data in database if it doesn't exist."""
    try:
        db = SessionLocal()
        try:
            # Check if we need to create demo data (e.g., if users table is empty)
            # user_count = db.query(User).count()
            # if user_count == 0:
            #     demo_user = User(
            #         username="demo",
            #         email="demo@example.com",
            #         hashed_password="$2b$12$F7FJ/vfAUwTZ/r7zIQJBBOK1WzCRv.reKCX9LW4XUVFnwfsFX6xaO"  # "password"
            #     )
            #     db.add(demo_user)
            #     db.commit()
            pass
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error creating demo data: {str(e)}")


# Initialize database if this module is run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Checking database connection...")
    if check_db_connection():
        logger.info("Database connection successful")
        logger.info("Initializing database...")
        init_db()
        logger.info("Creating demo data...")
        create_demo_data()
        logger.info("Database setup complete.")
    else:
        logger.error("Failed to connect to database. Please check your configuration.") 