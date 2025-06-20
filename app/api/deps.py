from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.crud.crud_user import user_crud
from app.models.user import User
from app.models.token import TokenPayload

# Setup OAuth2 with Password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

def get_db():
    """
    Dependency for database session
    """
    # This would be implemented with a database connection
    # For now, we'll use a placeholder that would be replaced with actual implementation
    db = None
    try:
        yield db
    finally:
        if db:
            db.close()


async def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Validate the token and return the current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        
        if token_data.sub is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = user_crud.get(db, id=token_data.sub)
    if not user:
        raise credentials_exception
        
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Validate that the current user is active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Validate that the current user is a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user 