from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel


class TypeEnum(str, Enum):
    trip = "trip"
    home = "home"
    other = "other"


class GroupResponse(BaseModel):
    id: UUID4
    name: str
    type: TypeEnum
    created_by: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
