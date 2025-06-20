from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum, Table
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

# Association table for team projects
team_projects = Table(
    'team_projects',
    Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)

class TeamRole(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

class Team(Base, TimestampMixin):
    """Team model for organization and team structure."""
    
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    avatar_url = Column(String(256))
    
    # Relationships
    memberships = relationship("TeamMembership", back_populates="team")
    projects = relationship("Project", secondary=team_projects)
    
    def __repr__(self):
        return f"<Team {self.name}>"
        
    @property
    def members_count(self):
        return len(self.memberships)

class TeamMembership(Base, TimestampMixin):
    """TeamMembership model for managing user memberships in teams."""
    
    __tablename__ = 'team_memberships'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    team = relationship("Team", back_populates="memberships")
    user = relationship("User")
    
    def __repr__(self):
        return f"<TeamMembership {self.user_id} in {self.team_id} as {self.role.value}>" 