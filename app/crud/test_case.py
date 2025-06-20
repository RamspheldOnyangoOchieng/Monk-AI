from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.test_case import TestCase, TestStatus, TestType
from .base import BaseRepository


class TestCaseRepository(BaseRepository[TestCase]):
    """Repository for TestCase operations."""

    def __init__(self):
        super().__init__(TestCase)

    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get test cases by project ID."""
        return db.query(TestCase).filter(
            TestCase.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_code_snippet(self, db: Session, *, snippet_id: int, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get test cases by code snippet ID."""
        return db.query(TestCase).filter(
            TestCase.code_snippet_id == snippet_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, project_id: int, status: TestStatus, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get test cases by status within a project."""
        return db.query(TestCase).filter(
            TestCase.project_id == project_id,
            TestCase.status == status
        ).offset(skip).limit(limit).all()
    
    def get_by_test_type(self, db: Session, *, project_id: int, test_type: TestType, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get test cases by type within a project."""
        return db.query(TestCase).filter(
            TestCase.project_id == project_id,
            TestCase.test_type == test_type
        ).offset(skip).limit(limit).all()
    
    def update_test_status(self, db: Session, *, test_id: int, status: TestStatus, 
                         execution_time: Optional[int] = None, 
                         error_message: Optional[str] = None) -> Optional[TestCase]:
        """Update test case status and related fields."""
        test = self.get(db, id=test_id)
        if not test:
            return None
        
        test.status = status
        if execution_time is not None:
            test.execution_time = execution_time
        if error_message is not None:
            test.error_message = error_message
            
        db.add(test)
        db.commit()
        db.refresh(test)
        return test
    
    def get_failed_tests(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get all failed tests for a project."""
        return db.query(TestCase).filter(
            TestCase.project_id == project_id,
            TestCase.status == TestStatus.FAILED
        ).offset(skip).limit(limit).all()
    
    def get_passed_tests(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get all passed tests for a project."""
        return db.query(TestCase).filter(
            TestCase.project_id == project_id,
            TestCase.status == TestStatus.PASSED
        ).offset(skip).limit(limit).all() 