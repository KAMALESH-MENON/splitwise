from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
import re

class UserSchema(BaseModel):
    """
    Schema for representing user data.

    This schema is used to validate and serialize user information, ensuring type consistency
    when exchanging data between the database and API responses.

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
    """
    Schema for validating password change requests.

    This schema ensures that:
    - The user ID is provided.
    - Both old and new passwords meet the minimum length requirement.
    - The new password adheres to security best practices.

    Attributes:
        user_id (UUID): Unique identifier of the user requesting a password change.
        current_password (str): The user's current password (must be at least 8 characters long).
        new_password (str): The user's new password, subject to additional validation.
    """

    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    def validate_password(cls, value):
        """
        Validates that the new password meets complexity requirements.

        The password must contain:
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)
        - At least one digit (0-9)
        - At least one special character (@#$%^&+=!)

        Args:
            value (str): The new password to validate.

        Raises:
            ValueError: If the password does not meet the complexity requirements.

        Returns:
            str: The validated password.
        """
        password_pattern = re.compile(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        )
        if not password_pattern.match(value):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@#$%^&+=!)"
            )
        return value
