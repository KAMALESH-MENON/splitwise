from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserSchema(BaseModel):
    """
    Schema for representing user data.

    This schema is used to validate and serialize user information, 
    ensuring type consistency when exchanging data between the database 
    and API responses.

    Attributes:
        id (UUID): Unique identifier for the user.
        name (str): Full name of the user.
        email (EmailStr): User's email address, validated as a proper email format.
        phone (Optional[str]): User's phone number (optional).
        profile_picture_url (Optional[str]): URL of the user's profile picture (optional).
        created_at (datetime): Timestamp indicating when the user was created.
    """

    id: UUID
    name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime

    class Config:
        """
        Pydantic configuration class.

        Enables attribute population from ORM models by mapping 
        database fields to Pydantic model attributes.
        """
        from_attributes = True

class ChangePasswordSchema(BaseModel):
    user_id: UUID
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
