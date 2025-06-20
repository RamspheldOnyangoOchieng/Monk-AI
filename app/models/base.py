from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Base class that includes timestamp functionality for all models."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 