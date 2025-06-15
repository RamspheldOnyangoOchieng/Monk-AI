from typing import Annotated, Any, List

from typing import Any, List, Optional
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.crud.code_snippet import snippet_crud
from app.models.user import User
from app.schemas.snippet import SnippetCreate, SnippetResponse, SnippetUpdate

router = APIRouter()


@router.get("/", response_model=List[SnippetResponse])
async def read_snippets(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    project_id: int = None
) -> Any:
    """
    Retrieve snippets by project or all snippets for the current user.
    """
    if project_id:
        snippets = snippet_crud.get_multi_by_project(
            db=db, project_id=project_id, owner_id=current_user.id, skip=skip, limit=limit
        )
    else:
        snippets = snippet_crud.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return snippets


@router.post("/", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    *,
    db: Annotated[Session, Depends(get_db)],
    snippet_in: SnippetCreate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Create new code snippet.
    """
    snippet = snippet_crud.create_with_owner(
        db=db, obj_in=snippet_in, owner_id=current_user.id
    )
    return snippet


@router.get("/{snippet_id}", response_model=SnippetResponse)
async def read_snippet(
    *,
    db: Annotated[Session, Depends(get_db)],
    snippet_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Get code snippet by ID.
    """
    snippet = snippet_crud.get(db=db, id=snippet_id)
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snippet not found"
        )
    if snippet.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return snippet


@router.put("/{snippet_id}", response_model=SnippetResponse)
async def update_snippet(
    *,
    db: Annotated[Session, Depends(get_db)],
    snippet_id: int,
    snippet_in: SnippetUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Update a code snippet.
    """
    snippet = snippet_crud.get(db=db, id=snippet_id)
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snippet not found"
        )
    if snippet.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    snippet = snippet_crud.update(db=db, db_obj=snippet, obj_in=snippet_in)
    return snippet


@router.delete("/{snippet_id}", response_model=SnippetResponse)
async def delete_snippet(
    *,
    db: Annotated[Session, Depends(get_db)],
    snippet_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Delete a code snippet.
    """
    snippet = snippet_crud.get(db=db, id=snippet_id)
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snippet not found"
        )
    if snippet.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    snippet = snippet_crud.remove(db=db, id=snippet_id)
    return snippet