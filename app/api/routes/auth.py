from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import user_crud
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_crud.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    db: Annotated[Session, Depends(get_db)],
    user_in: UserCreate
) -> Any:
    """
    Register a new user.
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    # Only allow user registration if it's enabled in settings
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is disabled"
        )
    
    user = user_crud.create(db, obj_in=user_in)
    return user 