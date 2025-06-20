from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class TestStatus(enum.Enum):
    PENDING = "pending"
    GENERATED = "generated"
    EXECUTED = "executed"
    PASSED = "passed"
    FAILED = "failed"

class TestType(enum.Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"

class TestCase(Base, TimestampMixin):
    """Test Case model for storing test case generation results."""
    
    __tablename__ = 'test_cases'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text)
    test_code = Column(Text, nullable=False)
    test_type = Column(Enum(TestType), nullable=False)
    status = Column(Enum(TestStatus), default=TestStatus.PENDING)
    execution_time = Column(Integer)  # in milliseconds
    error_message = Column(Text)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    code_snippet_id = Column(Integer, ForeignKey('code_snippets.id'))
    
    # Relationships
    project = relationship("Project")
    code_snippet = relationship("CodeSnippet")
    
    def __repr__(self):
        return f"<TestCase {self.name} ({self.test_type.value})>" 