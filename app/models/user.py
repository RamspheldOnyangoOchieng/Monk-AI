from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    """User model for storing user data and authentication information."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(128))
    is_active = Column(Boolean, default=True)
    github_username = Column(String(64))
    avatar_url = Column(String(256))
    
    # Relationships
    projects = relationship("Project", back_populates="owner")
    pull_requests = relationship("PullRequest", back_populates="author")
    reviews = relationship("Review", back_populates="reviewer")
    
    def __repr__(self):
        return f"<User {self.username}>" 