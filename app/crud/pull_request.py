from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.pull_request import PullRequest, PRStatus
from .base import BaseRepository


class PullRequestRepository(BaseRepository[PullRequest]):
    """Repository for PullRequest operations."""

    def __init__(self):
        super().__init__(PullRequest)

    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[PullRequest]:
        """Get pull requests by project ID."""
        return db.query(PullRequest).filter(
            PullRequest.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_author(self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100) -> List[PullRequest]:
        """Get pull requests by author ID."""
        return db.query(PullRequest).filter(
            PullRequest.author_id == author_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, project_id: int, status: PRStatus, skip: int = 0, limit: int = 100) -> List[PullRequest]:
        """Get pull requests by status within a project."""
        return db.query(PullRequest).filter(
            PullRequest.project_id == project_id,
            PullRequest.status == status
        ).offset(skip).limit(limit).all()
    
    def get_by_github_pr_id(self, db: Session, *, github_pr_id: int) -> Optional[PullRequest]:
        """Get a pull request by GitHub PR ID."""
        return db.query(PullRequest).filter(
            PullRequest.github_pr_id == github_pr_id
        ).first()
    
    def merge_pull_request(self, db: Session, *, pr_id: int) -> Optional[PullRequest]:
        """Mark a pull request as merged."""
        pr = self.get(db, id=pr_id)
        if not pr:
            return None
        
        pr.status = PRStatus.MERGED
        db.add(pr)
        db.commit()
        db.refresh(pr)
        return pr
    
    def close_pull_request(self, db: Session, *, pr_id: int) -> Optional[PullRequest]:
        """Mark a pull request as closed."""
        pr = self.get(db, id=pr_id)
        if not pr:
            return None
        
        pr.status = PRStatus.CLOSED
        db.add(pr)
        db.commit()
        db.refresh(pr)
        return pr 