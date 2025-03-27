from enum import Enum

from pydantic import BaseModel


class TypeEnum(str, Enum):
    trip = "trip"
    home = "home"
    other = "other"


class GroupInput(BaseModel):
    name: str
    type: TypeEnum
