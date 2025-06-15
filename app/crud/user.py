from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get a user by email."""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get a user by username."""
        return db.query(User).filter(User.username == username).first()
    
    def get_active_users(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users."""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_github_username(self, db: Session, *, github_username: str) -> Optional[User]:
        """Get a user by GitHub username."""
        return db.query(User).filter(User.github_username == github_username).first()
    
    def deactivate(self, db: Session, *, user_id: int) -> Optional[User]:
        """Deactivate a user."""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        user.is_active = False
        db.add(user)
        db.commit()
        db.refresh(user)
        return user