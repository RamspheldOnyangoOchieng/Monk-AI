from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    """Base project schema with common fields."""
    name: str
    description: Optional[str] = None
    repository_url: str
    programming_language: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    programming_language: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(ProjectBase):
    """Schema for project responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime