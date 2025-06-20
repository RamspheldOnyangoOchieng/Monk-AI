from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from pydantic import BaseModel

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository providing common CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], BaseModel]
    ) -> ModelType:
        """Update a record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Delete a record by ID."""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj 