from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class PRStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"

class PullRequest(Base, TimestampMixin):
    """Pull Request model for storing PR structure and metadata."""
    
    __tablename__ = 'pull_requests'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    branch_name = Column(String(128), nullable=False)
    base_branch = Column(String(128), nullable=False, default="main")
    status = Column(Enum(PRStatus), default=PRStatus.OPEN)
    github_pr_url = Column(String(256))
    github_pr_id = Column(Integer)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="pull_requests")
    project = relationship("Project", back_populates="pull_requests")
    code_snippets = relationship("CodeSnippet", back_populates="pull_request")
    reviews = relationship("Review", back_populates="pull_request")
    
    def __repr__(self):
        return f"<PullRequest {self.title}>" 