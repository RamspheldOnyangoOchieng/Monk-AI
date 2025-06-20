from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SnippetBase(BaseModel):
    """Base snippet schema with common fields."""
    filename: str
    content: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    language: Optional[str] = None


class SnippetCreate(SnippetBase):
    """Schema for creating a new code snippet."""
    project_id: int
    pull_request_id: Optional[int] = None


class SnippetUpdate(BaseModel):
    """Schema for updating an existing code snippet."""
    filename: Optional[str] = None
    content: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    language: Optional[str] = None
    project_id: Optional[int] = None
    pull_request_id: Optional[int] = None


class SnippetResponse(SnippetBase):
    """Schema for code snippet responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    project_id: int
    pull_request_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime