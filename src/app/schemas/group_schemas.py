from uuid import UUID

from pydantic import BaseModel, EmailStr


class GroupMemberResponse(BaseModel):
    """
    Represents a response model for a group member.

    Attributes:
        id (UUID): The unique identifier of the group member.
        name (str): The name of the group member.
        email (EmailStr): The email address of the group member.
        profile_picture_url (str): The URL of the group member's profile picture.
    """

    id: UUID
    name: str
    email: EmailStr
    profile_picture_url: str

    class Config:
        """Configuration settings for Pydantic model."""

        form_attribute = True
