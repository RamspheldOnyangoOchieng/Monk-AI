from sqlalchemy import Column, Integer, String, Text, Enum, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import Base, TimestampMixin

class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentTask(Base, TimestampMixin):
    """Agent Task model for managing tasks in a multi-agent system."""
    
    __tablename__ = 'agent_tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    agent_type = Column(String(64), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    parent_task_id = Column(Integer, ForeignKey('agent_tasks.id'))
    
    # Relationships
    project = relationship("Project")
    subtasks = relationship("AgentTask", backref="parent_task")
    
    def __repr__(self):
        return f"<AgentTask {self.title} ({self.status.value})>"
        
    def start(self):
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
        
    def complete(self, output_data=None):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if output_data:
            self.output_data = output_data
            
    def fail(self, error_message):
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()