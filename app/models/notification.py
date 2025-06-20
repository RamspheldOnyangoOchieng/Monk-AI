from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class NotificationType(enum.Enum):
    SYSTEM = "system"
    PR_CREATED = "pr_created"
    PR_UPDATED = "pr_updated"
    PR_MERGED = "pr_merged"
    PR_COMMENTED = "pr_commented"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_SUBMITTED = "review_submitted"
    TEST_COMPLETED = "test_completed"
    DOC_GENERATED = "doc_generated"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TEAM_INVITATION = "team_invitation"

class Notification(Base, TimestampMixin):
    """Notification model for user notifications and activity feed."""
    
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    extra_data = Column(JSON)  # Additional data related to the notification
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'))
    
    # Relationships
    recipient = relationship("User", foreign_keys=[recipient_id])
    sender = relationship("User", foreign_keys=[sender_id])
    project = relationship("Project")
    pull_request = relationship("PullRequest")
    
    def __repr__(self):
        return f"<Notification {self.type.value} for user {self.recipient_id}: {self.title}>"
    
    def mark_as_read(self):
        self.is_read = True 