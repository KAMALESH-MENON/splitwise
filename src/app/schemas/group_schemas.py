from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel


class TypeEnum(str, Enum):
    """
    Enumeration for different types of groups.
    Attributes:
        trip: Represents a group related to trips.
        home: Represents a home-related group.
        other: Represents any other type of group.
    """

    trip = "trip"
    home = "home"
    other = "other"


class GroupResponse(BaseModel):
    """
    Pydantic model representing a response for a group.

    Attributes:
        id (UUID4): Unique identifier for the group.
        name (str): Name of the group.
        type (TypeEnum): Type of the group (trip, home, or other).
        created_by (UUID4): Unique identifier of the user who created the group.
        created_at (datetime): Timestamp of when the group was created.
    """

    id: UUID4
    name: str
    type: TypeEnum
    created_by: UUID4
    created_at: datetime

    class Config:
        """Configuration settings for Pydantic model."""

        from_attributes = True


class GroupUpdateRequest(BaseModel):
    """
    Represents the request payload for updating a group's details.

    Attributes:
        name (Optional[str]):
            The new name of the group. Defaults to None if not provided.
        type (Optional[TypeEnum]):
            The updated type/category of the group. Defaults to None if not provided.
        created_by (Optional[UUID4]):
            The UUID of the user who originally created the group. Defaults to None if not provided.
    """

    name: Optional[str] = None
    type: Optional[TypeEnum] = None
    created_by: Optional[UUID4] = None
