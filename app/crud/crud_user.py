"""
User CRUD operations
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser:
    """User CRUD operations"""
    
    def __init__(self):
        pass
    
    def get(self, db: Session, id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get multiple users"""
        return db.query(User).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Create new user"""
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> User:
        """Delete user"""
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj

# Create instance
user_crud = CRUDUser()