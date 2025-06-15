from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.review import Review, ReviewType
from .base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Repository for Review operations."""

    def __init__(self):
        super().__init__(Review)

    def get_by_pull_request(self, db: Session, *, pr_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        """Get reviews by pull request ID."""
        return db.query(Review).filter(
            Review.pull_request_id == pr_id
        ).offset(skip).limit(limit).all()
    
    def get_by_reviewer(self, db: Session, *, reviewer_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        """Get reviews by reviewer ID."""
        return db.query(Review).filter(
            Review.reviewer_id == reviewer_id
        ).offset(skip).limit(limit).all()
    
    def get_by_code_snippet(self, db: Session, *, snippet_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        """Get reviews by code snippet ID."""
        return db.query(Review).filter(
            Review.code_snippet_id == snippet_id
        ).offset(skip).limit(limit).all()
    
    def get_by_type(self, db: Session, *, pr_id: int, review_type: ReviewType, skip: int = 0, limit: int = 100) -> List[Review]:
        """Get reviews by type within a pull request."""
        return db.query(Review).filter(
            Review.pull_request_id == pr_id,
            Review.type == review_type
        ).offset(skip).limit(limit).all()
    
    def get_suggestions(self, db: Session, *, pr_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        """Get suggestions for a pull request."""
        return db.query(Review).filter(
            Review.pull_request_id == pr_id,
            Review.type == ReviewType.SUGGESTION,
            Review.suggested_code.isnot(None)
        ).offset(skip).limit(limit).all()

review_crud = ReviewRepository() 