from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

class Project(Base, TimestampMixin):
    """Project model for storing project-level data."""
    
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    repository_url = Column(String(256), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
    programming_language = Column(String(64))
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    code_snippets = relationship("CodeSnippet", back_populates="project")
    pull_requests = relationship("PullRequest", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.name}>" 