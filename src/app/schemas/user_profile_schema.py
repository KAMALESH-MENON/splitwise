from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserSchema(BaseModel):
    """
    Schema for representing user data.
    """

    id: UUID
    name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DeleteUserSchema(BaseModel):
    """
    Schema for deleting a user.

    Attributes:
        password (str): User's current password for authentication before deletion.
    """
    password: str
