from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Float, JSON
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class FeedbackType(enum.Enum):
    CODE_QUALITY = "code_quality"
    DOC_QUALITY = "doc_quality"
    TEST_QUALITY = "test_quality"
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    GENERAL = "general"

class Feedback(Base, TimestampMixin):
    """Feedback model for AI model feedback and rating."""
    
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Float)  # 1-5 scale
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    comment = Column(Text)
    extra_data = Column(JSON)  # Additional data about the context of the feedback
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    agent_task_id = Column(Integer, ForeignKey('agent_tasks.id'))
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'))
    code_snippet_id = Column(Integer, ForeignKey('code_snippets.id'))
    doc_generation_id = Column(Integer, ForeignKey('doc_generations.id'))
    test_case_id = Column(Integer, ForeignKey('test_cases.id'))
    
    # Relationships
    user = relationship("User")
    project = relationship("Project")
    agent_task = relationship("AgentTask")
    pull_request = relationship("PullRequest")
    code_snippet = relationship("CodeSnippet")
    doc_generation = relationship("DocGeneration")
    test_case = relationship("TestCase")
    
    def __repr__(self):
        return f"<Feedback {self.feedback_type.value}: {self.rating}/5>" 