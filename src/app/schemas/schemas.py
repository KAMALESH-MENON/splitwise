from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True


class ActivitySchema(BaseModel):
    id: UUID
    description: str
    timestamp: datetime
    user_id: UUID
    group_id: UUID | None

    class Config:
        from_attributes = True


class GroupSchema(BaseSchema):
    id: UUID
    name: str
    type: str
    created_by: UUID
    created_at: datetime


class GroupUserSchema(BaseSchema):
    id: UUID
    group_id: UUID
    user_id: UUID
    joined_at: datetime


class ExpenseSchema(BaseSchema):
    id: UUID
    group_id: UUID
    total_amount: float
    description: str
    expense_type: str
    paid_by: UUID
    created_at: datetime
