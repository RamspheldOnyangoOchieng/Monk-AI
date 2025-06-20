from typing import Any, List
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.crud.project import project_crud
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()


@router.get("/", response_model=List[ProjectResponse])
async def read_projects(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve projects belonging to the current user.
    """
    projects = project_crud.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return projects


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    *,
    db: Annotated[Session, Depends(get_db)],
    project_in: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Create new project.
    """
    project = project_crud.create_with_owner(
        db=db, obj_in=project_in, owner_id=current_user.id
    )
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    *,
    db: Annotated[Session, Depends(get_db)],
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Get project by ID.
    """
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    *,
    db: Annotated[Session, Depends(get_db)],
    project_id: int,
    project_in: ProjectUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Update a project.
    """
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    project = project_crud.update(db=db, db_obj=project, obj_in=project_in)
    return project


@router.delete("/{project_id}", response_model=ProjectResponse)
async def delete_project(
    *,
    db: Annotated[Session, Depends(get_db)],
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Delete a project.
    """
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    project = project_crud.remove(db=db, id=project_id)
    return project