from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class DocType(enum.Enum):
    API = "api"
    README = "readme"
    USAGE = "usage"
    ARCHITECTURE = "architecture"
    INSTALLATION = "installation"

class DocGeneration(Base, TimestampMixin):
    """Documentation generation model for storing metadata about documentation generation."""
    
    __tablename__ = 'doc_generations'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    format = Column(String(64), default="markdown")
    doc_type = Column(Enum(DocType), nullable=False)
    is_published = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    project = relationship("Project")
    
    def __repr__(self):
        return f"<DocGeneration {self.title} ({self.doc_type.value})>" 