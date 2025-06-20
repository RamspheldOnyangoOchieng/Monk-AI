from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class LogLevel(enum.Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AgentLog(Base, TimestampMixin):
    """Agent Log model for tracking agent activities, errors, and audits."""
    
    __tablename__ = 'agent_logs'
    
    id = Column(Integer, primary_key=True)
    agent_type = Column(String(64), nullable=False)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON)
    trace = Column(Text)
    project_id = Column(Integer, ForeignKey('projects.id'))
    agent_task_id = Column(Integer, ForeignKey('agent_tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    project = relationship("Project")
    agent_task = relationship("AgentTask")
    user = relationship("User")
    
    def __repr__(self):
        return f"<AgentLog {self.level.value}: {self.message[:30]}...>" 