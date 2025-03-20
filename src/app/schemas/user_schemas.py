from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Common fields shared by multiple schemas."""

    name: str
    email: EmailStr
    phone: Optional[str] = Field(
        None, min_length=10, max_length=10, pattern=r"^\d{10}$"
    )
    profile_picture_url: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str


class UserResponse(BaseModel):
    """Schema for user details response."""

    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user details"""

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        None, min_length=10, max_length=10, pattern=r"^\d{10}$"
    )
    profile_picture_url: Optional[str] = None


class LoginInput(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class LoginOutput(BaseModel):
    """Schema for returning access tokens."""

    token_type: str
    access_token: str
