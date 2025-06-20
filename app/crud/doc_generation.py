from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.doc_generation import DocGeneration, DocType
from .base import BaseRepository


class DocGenerationRepository(BaseRepository[DocGeneration]):
    """Repository for DocGeneration operations."""

    def __init__(self):
        super().__init__(DocGeneration)

    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[DocGeneration]:
        """Get documentation by project ID."""
        return db.query(DocGeneration).filter(
            DocGeneration.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_doc_type(self, db: Session, *, project_id: int, doc_type: DocType) -> Optional[DocGeneration]:
        """Get documentation by type within a project."""
        return db.query(DocGeneration).filter(
            DocGeneration.project_id == project_id,
            DocGeneration.doc_type == doc_type
        ).first()
    
    def get_published(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[DocGeneration]:
        """Get all published documentation for a project."""
        return db.query(DocGeneration).filter(
            DocGeneration.project_id == project_id,
            DocGeneration.is_published == True
        ).offset(skip).limit(limit).all()
    
    def publish(self, db: Session, *, doc_id: int) -> Optional[DocGeneration]:
        """Mark documentation as published."""
        doc = self.get(db, id=doc_id)
        if not doc:
            return None
        
        doc.is_published = True
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    
    def unpublish(self, db: Session, *, doc_id: int) -> Optional[DocGeneration]:
        """Mark documentation as unpublished."""
        doc = self.get(db, id=doc_id)
        if not doc:
            return None
        
        doc.is_published = False
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc 