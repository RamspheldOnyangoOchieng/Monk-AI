from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus
from .base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project operations."""

    def __init__(self):
        super().__init__(Project)

    def get_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by owner ID."""
        return db.query(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit).all()
    
    def get_active_projects(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all active projects."""
        return db.query(Project).filter(Project.status == ProjectStatus.ACTIVE).offset(skip).limit(limit).all()
    
    def get_by_repository_url(self, db: Session, *, repository_url: str) -> Optional[Project]:
        """Get a project by its repository URL."""
        return db.query(Project).filter(Project.repository_url == repository_url).first()
    
    def archive_project(self, db: Session, *, project_id: int) -> Optional[Project]:
        """Archive a project."""
        project = self.get(db, id=project_id)
        if not project:
            return None
        
        project.status = ProjectStatus.ARCHIVED
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    def restore_project(self, db: Session, *, project_id: int) -> Optional[Project]:
        """Restore an archived project."""
        project = self.get(db, id=project_id)
        if not project:
            return None
        
        project.status = ProjectStatus.ACTIVE
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
        
    def get_by_language(self, db: Session, *, language: str, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by programming language."""
        return (db.query(Project)
                .filter(Project.programming_language == language)
                .filter(Project.status == ProjectStatus.ACTIVE)
                .offset(skip).limit(limit).all())


# Create instance for import
project_crud = ProjectRepository()