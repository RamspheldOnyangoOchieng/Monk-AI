from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db
)
from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_superuser)],
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve users. Only accessible to superusers.
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: Annotated[Session, Depends(get_db)],
    user_in: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_superuser)]
) -> Any:
    """
    Create new user. Only accessible to superusers.
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: Annotated[Session, Depends(get_db)],
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Update own user.
    """
    user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Get a specific user by id.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_superuser)]
) -> Any:
    """
    Update a user. Only accessible to superusers.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    *,
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_superuser)]
) -> Any:
    """
    Delete a user. Only accessible to superusers.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = user_crud.remove(db, id=user_id)
    return user 