from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ExpenseType(str, Enum):
    """Enum for expense types matching the database."""

    GROUP = "GROUP"
    NON_EXPENSE_GROUP = "NON-EXPENSE GROUP"


class ExpenseBase(BaseModel):
    """Base schema for expenses."""

    total_amount: Decimal = Field(
        ..., gt=0, description="Total expense amount, must be greater than zero."
    )
    description: Optional[str] = None
    group_id: Optional[UUID] = None
    paid_by: UUID


class ExpenseCreate(ExpenseBase):
    """Schema for creating an expense."""

    participants: List[UUID] = Field(
        ..., min_items=1, description="List of users participating in the expense."
    )


class ExpenseCreateResponse(BaseModel):
    """Response schema for successfully creating an expense."""

    message: str = "Expense successfully added."
