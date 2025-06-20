from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class ReviewType(enum.Enum):
    COMMENT = "comment"
    SUGGESTION = "suggestion"
    APPROVAL = "approval"
    REQUEST_CHANGES = "request_changes"

class Review(Base, TimestampMixin):
    """Review model for storing review comments and suggestions."""
    
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    type = Column(Enum(ReviewType), default=ReviewType.COMMENT)
    line_number = Column(Integer)
    suggested_code = Column(Text)
    reviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'), nullable=False)
    code_snippet_id = Column(Integer, ForeignKey('code_snippets.id'))
    
    # Relationships
    reviewer = relationship("User", back_populates="reviews")
    pull_request = relationship("PullRequest", back_populates="reviews")
    code_snippet = relationship("CodeSnippet", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review {self.type.value} by {self.reviewer_id}>" 