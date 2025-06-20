from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType
from .base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification operations."""

    def __init__(self):
        super().__init__(Notification)

    def get_by_recipient(self, db: Session, *, recipient_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get notifications by recipient ID."""
        return db.query(Notification).filter(
            Notification.recipient_id == recipient_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_sender(self, db: Session, *, sender_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get notifications by sender ID."""
        return db.query(Notification).filter(
            Notification.sender_id == sender_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get notifications by project ID."""
        return db.query(Notification).filter(
            Notification.project_id == project_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_pull_request(self, db: Session, *, pr_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get notifications by pull request ID."""
        return db.query(Notification).filter(
            Notification.pull_request_id == pr_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_unread(self, db: Session, *, recipient_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get unread notifications for a recipient."""
        return db.query(Notification).filter(
            Notification.recipient_id == recipient_id,
            Notification.is_read == False
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def mark_as_read(self, db: Session, *, notification_id: int) -> Optional[Notification]:
        """Mark a notification as read."""
        notification = self.get(db, id=notification_id)
        if not notification:
            return None
        
        notification.mark_as_read()
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    def mark_all_as_read(self, db: Session, *, recipient_id: int) -> int:
        """Mark all notifications as read for a recipient."""
        result = db.query(Notification).filter(
            Notification.recipient_id == recipient_id,
            Notification.is_read == False
        ).update({Notification.is_read: True})
        
        db.commit()
        return result
    
    def get_by_type(self, db: Session, *, recipient_id: int, notification_type: NotificationType, 
                  skip: int = 0, limit: int = 100) -> List[Notification]:
        """Get notifications by type for a recipient."""
        return db.query(Notification).filter(
            Notification.recipient_id == recipient_id,
            Notification.type == notification_type
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all() 