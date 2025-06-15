"""Token models for authentication."""

from typing import Optional
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload model for JWT tokens."""
    sub: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    user_id: Optional[int] = None
    email: Optional[str] = None
    is_superuser: Optional[bool] = False