from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin

class CodeSnippet(Base, TimestampMixin):
    """Code snippet model for storing code for review and analysis."""
    
    __tablename__ = 'code_snippets'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    start_line = Column(Integer)
    end_line = Column(Integer)
    language = Column(String(64))
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'))
    
    # Relationships
    project = relationship("Project", back_populates="code_snippets")
    pull_request = relationship("PullRequest", back_populates="code_snippets")
    reviews = relationship("Review", back_populates="code_snippet")
    
    def __repr__(self):
        return f"<CodeSnippet {self.filename}:{self.start_line}-{self.end_line}>" 