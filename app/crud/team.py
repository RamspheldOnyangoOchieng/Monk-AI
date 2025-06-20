from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.team import Team, TeamMembership, TeamRole
from app.models.project import Project
from .base import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """Repository for Team operations."""

    def __init__(self):
        super().__init__(Team)

    def get_by_name(self, db: Session, *, name: str) -> Optional[Team]:
        """Get a team by name."""
        return db.query(Team).filter(Team.name == name).first()
    
    def get_teams_for_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Team]:
        """Get all teams a user belongs to."""
        return (db.query(Team)
                .join(TeamMembership)
                .filter(TeamMembership.user_id == user_id, TeamMembership.is_active == True)
                .offset(skip).limit(limit).all())
    
    def add_project_to_team(self, db: Session, *, team_id: int, project_id: int) -> Optional[Team]:
        """Add a project to a team."""
        team = self.get(db, id=team_id)
        if not team:
            return None
        
        team.projects.append(db.query(Project).get(project_id))
        db.add(team)
        db.commit()
        db.refresh(team)
        return team
    
    def remove_project_from_team(self, db: Session, *, team_id: int, project_id: int) -> Optional[Team]:
        """Remove a project from a team."""
        team = self.get(db, id=team_id)
        if not team:
            return None
        
        project = db.query(Project).get(project_id)
        if project in team.projects:
            team.projects.remove(project)
            db.add(team)
            db.commit()
            db.refresh(team)
        
        return team


class TeamMembershipRepository(BaseRepository[TeamMembership]):
    """Repository for TeamMembership operations."""

    def __init__(self):
        super().__init__(TeamMembership)

    def get_by_team_and_user(self, db: Session, *, team_id: int, user_id: int) -> Optional[TeamMembership]:
        """Get a team membership by team and user IDs."""
        return db.query(TeamMembership).filter(
            TeamMembership.team_id == team_id,
            TeamMembership.user_id == user_id
        ).first()
    
    def get_team_members(self, db: Session, *, team_id: int, skip: int = 0, limit: int = 100) -> List[TeamMembership]:
        """Get all members of a team."""
        return db.query(TeamMembership).filter(
            TeamMembership.team_id == team_id,
            TeamMembership.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_role(self, db: Session, *, team_id: int, role: TeamRole, skip: int = 0, limit: int = 100) -> List[TeamMembership]:
        """Get team members by role."""
        return db.query(TeamMembership).filter(
            TeamMembership.team_id == team_id,
            TeamMembership.role == role,
            TeamMembership.is_active == True
        ).offset(skip).limit(limit).all()
    
    def update_role(self, db: Session, *, team_id: int, user_id: int, new_role: TeamRole) -> Optional[TeamMembership]:
        """Update a user's role in a team."""
        membership = self.get_by_team_and_user(db, team_id=team_id, user_id=user_id)
        if not membership:
            return None
        
        membership.role = new_role
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership
    
    def deactivate(self, db: Session, *, team_id: int, user_id: int) -> Optional[TeamMembership]:
        """Deactivate a team membership."""
        membership = self.get_by_team_and_user(db, team_id=team_id, user_id=user_id)
        if not membership:
            return None
        
        membership.is_active = False
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership
    
    def activate(self, db: Session, *, team_id: int, user_id: int) -> Optional[TeamMembership]:
        """Activate a team membership."""
        membership = self.get_by_team_and_user(db, team_id=team_id, user_id=user_id)
        if not membership:
            return None
        
        membership.is_active = True
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership 