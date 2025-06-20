from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.agent_log import AgentLog, LogLevel
from .base import BaseRepository


class AgentLogRepository(BaseRepository[AgentLog]):
    """Repository for AgentLog operations."""

    def __init__(self):
        super().__init__(AgentLog)

    def get_by_agent_task(self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get logs by agent task ID."""
        return db.query(AgentLog).filter(
            AgentLog.agent_task_id == task_id
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get logs by project ID."""
        return db.query(AgentLog).filter(
            AgentLog.project_id == project_id
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_agent_type(self, db: Session, *, agent_type: str, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get logs by agent type."""
        return db.query(AgentLog).filter(
            AgentLog.agent_type == agent_type
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_level(self, db: Session, *, level: LogLevel, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get logs by level."""
        return db.query(AgentLog).filter(
            AgentLog.level == level
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get logs by user ID."""
        return db.query(AgentLog).filter(
            AgentLog.user_id == user_id
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_errors(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[AgentLog]:
        """Get error logs."""
        return db.query(AgentLog).filter(
            AgentLog.level.in_([LogLevel.ERROR, LogLevel.CRITICAL])
        ).order_by(AgentLog.created_at.desc()).offset(skip).limit(limit).all()
    
    def log_message(self, db: Session, *, agent_type: str, level: LogLevel, message: str, 
                  details: Optional[dict] = None, trace: Optional[str] = None,
                  project_id: Optional[int] = None, agent_task_id: Optional[int] = None, 
                  user_id: Optional[int] = None) -> AgentLog:
        """Create a log entry and return it."""
        log_data = {
            "agent_type": agent_type,
            "level": level,
            "message": message,
            "details": details,
            "trace": trace,
            "project_id": project_id,
            "agent_task_id": agent_task_id,
            "user_id": user_id
        }
        
        # Filter out None values
        log_data = {k: v for k, v in log_data.items() if v is not None}
        
        return self.create(db, obj_in=log_data) 