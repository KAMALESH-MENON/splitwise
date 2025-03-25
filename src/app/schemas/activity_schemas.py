from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Base schema class that other schemas can inherit from.
    Configures Pydantic to allow attribute-based initialization.
    """

    class Config:
        from_attributes = True


class ActivitySchema(BaseModel):
    """
    Schema representing an activity in the system.

    Attributes:
        id (UUID): Unique identifier for the activity.
        description (str): Description of the activity.
        timestamp (datetime): The time when the activity occurred.
        user_id (UUID): Unique identifier of the user associated with the activity.
        group_id (UUID | None): Optional unique identifier of the group associated with the activity.
    """

    id: UUID
    description: str
    timestamp: datetime
    user_id: UUID
    group_id: UUID | None

    class Config:
        from_attributes = True
