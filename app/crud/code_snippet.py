from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.code_snippet import CodeSnippet
from .base import BaseRepository


class CodeSnippetRepository(BaseRepository[CodeSnippet]):
    """Repository for CodeSnippet operations."""

    def __init__(self):
        super().__init__(CodeSnippet)

    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[CodeSnippet]:
        """Get code snippets by project ID."""
        return db.query(CodeSnippet).filter(
            CodeSnippet.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_pull_request(self, db: Session, *, pr_id: int, skip: int = 0, limit: int = 100) -> List[CodeSnippet]:
        """Get code snippets by pull request ID."""
        return db.query(CodeSnippet).filter(
            CodeSnippet.pull_request_id == pr_id
        ).offset(skip).limit(limit).all()
    
    def get_by_filename(self, db: Session, *, project_id: int, filename: str) -> List[CodeSnippet]:
        """Get code snippets by filename within a project."""
        return db.query(CodeSnippet).filter(
            CodeSnippet.project_id == project_id,
            CodeSnippet.filename == filename
        ).all()
    
    def get_by_language(self, db: Session, *, project_id: int, language: str) -> List[CodeSnippet]:
        """Get code snippets by language within a project."""
        return db.query(CodeSnippet).filter(
            CodeSnippet.project_id == project_id,
            CodeSnippet.language == language
        ).all()


snippet_crud = CodeSnippetRepository()