"""User schemas for API requests and responses."""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserUpdate(UserBase):
    """Schema for updating an existing user."""
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """Base schema for user data stored in database."""
    id: Optional[int] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Schema for user data with all fields."""
    pass


class UserInDB(UserInDBBase):
    """Schema for user data including hashed password."""
    hashed_password: str


class UserResponse(UserInDBBase):
    """Schema for user response (excludes sensitive data)."""
    pass