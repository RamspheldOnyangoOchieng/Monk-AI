from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.feedback import Feedback, FeedbackType
from .base import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    """Repository for Feedback operations."""

    def __init__(self):
        super().__init__(Feedback)

    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by user ID."""
        return db.query(Feedback).filter(
            Feedback.user_id == user_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by project ID."""
        return db.query(Feedback).filter(
            Feedback.project_id == project_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_agent_task(self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by agent task ID."""
        return db.query(Feedback).filter(
            Feedback.agent_task_id == task_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_pull_request(self, db: Session, *, pr_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by pull request ID."""
        return db.query(Feedback).filter(
            Feedback.pull_request_id == pr_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_code_snippet(self, db: Session, *, snippet_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by code snippet ID."""
        return db.query(Feedback).filter(
            Feedback.code_snippet_id == snippet_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_doc_generation(self, db: Session, *, doc_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by document generation ID."""
        return db.query(Feedback).filter(
            Feedback.doc_generation_id == doc_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_test_case(self, db: Session, *, test_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by test case ID."""
        return db.query(Feedback).filter(
            Feedback.test_case_id == test_id
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_feedback_type(self, db: Session, *, feedback_type: FeedbackType, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by type."""
        return db.query(Feedback).filter(
            Feedback.feedback_type == feedback_type
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_rating_range(self, db: Session, *, min_rating: float, max_rating: float, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Get feedback by rating range."""
        return db.query(Feedback).filter(
            Feedback.rating >= min_rating,
            Feedback.rating <= max_rating
        ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_average_rating(self, db: Session, *, project_id: Optional[int] = None, 
                         feedback_type: Optional[FeedbackType] = None) -> Optional[float]:
        """Get average rating, optionally filtered by project and/or feedback type."""
        query = db.query(db.func.avg(Feedback.rating))
        
        if project_id:
            query = query.filter(Feedback.project_id == project_id)
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
            
        result = query.scalar()
        return float(result) if result is not None else None 