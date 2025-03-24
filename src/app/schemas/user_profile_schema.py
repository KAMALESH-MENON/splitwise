from pydantic import BaseModel, EmailStr
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

        Enables ORM mode to allow compatibility with SQLAlchemy models 
        and ensures attributes can be mapped from ORM objects.
        """
        from_attributes = True


class DeleteUserSchema(BaseModel):
    """
    Schema for deleting a user.

    This schema is used to validate the request payload when deleting a user. 
    It ensures that the user ID is provided in the correct UUID format.

    Attributes:
        user_id (UUID): Unique identifier of the user to be deleted.
    """
    
    user_id: UUID
