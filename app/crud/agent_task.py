from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.agent_task import AgentTask, TaskStatus, TaskPriority
from .base import BaseRepository


class AgentTaskRepository(BaseRepository[AgentTask]):
    """Repository for AgentTask operations."""

    def __init__(self):
        super().__init__(AgentTask)

    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get agent tasks by project ID."""
        return db.query(AgentTask).filter(
            AgentTask.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_agent_type(self, db: Session, *, agent_type: str, skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get agent tasks by agent type."""
        return db.query(AgentTask).filter(
            AgentTask.agent_type == agent_type
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get agent tasks by status."""
        return db.query(AgentTask).filter(
            AgentTask.status == status
        ).offset(skip).limit(limit).all()
    
    def get_by_priority(self, db: Session, *, priority: TaskPriority, skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get agent tasks by priority."""
        return db.query(AgentTask).filter(
            AgentTask.priority == priority
        ).offset(skip).limit(limit).all()
    
    def get_subtasks(self, db: Session, *, parent_task_id: int, skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get subtasks for a parent task."""
        return db.query(AgentTask).filter(
            AgentTask.parent_task_id == parent_task_id
        ).offset(skip).limit(limit).all()
    
    def start_task(self, db: Session, *, task_id: int) -> Optional[AgentTask]:
        """Mark a task as started."""
        task = self.get(db, id=task_id)
        if not task:
            return None
        
        task.start()
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def complete_task(self, db: Session, *, task_id: int, output_data: Optional[dict] = None) -> Optional[AgentTask]:
        """Mark a task as completed."""
        task = self.get(db, id=task_id)
        if not task:
            return None
        
        task.complete(output_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def fail_task(self, db: Session, *, task_id: int, error_message: str) -> Optional[AgentTask]:
        """Mark a task as failed."""
        task = self.get(db, id=task_id)
        if not task:
            return None
        
        task.fail(error_message)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def cancel_task(self, db: Session, *, task_id: int) -> Optional[AgentTask]:
        """Mark a task as cancelled."""
        task = self.get(db, id=task_id)
        if not task:
            return None
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.utcnow()
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def get_pending_tasks(self, db: Session, *, project_id: Optional[int] = None, agent_type: Optional[str] = None, 
                        skip: int = 0, limit: int = 100) -> List[AgentTask]:
        """Get pending tasks, optionally filtered by project or agent type."""
        query = db.query(AgentTask).filter(AgentTask.status == TaskStatus.PENDING)
        
        if project_id:
            query = query.filter(AgentTask.project_id == project_id)
        if agent_type:
            query = query.filter(AgentTask.agent_type == agent_type)
            
        return query.order_by(AgentTask.priority.desc()).offset(skip).limit(limit).all() 