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

    total_amount: Optional[Decimal] = Field(
        default=None,
        gt=0,
        description="Total expense amount, must be greater than zero.",
    )
    description: Optional[str] = Field(default=None)
    group_id: Optional[UUID] = Field(default=None)
    paid_by: Optional[UUID] = Field(default=None)


class ExpenseUpdate(ExpenseBase):
    """Schema for updating an expense."""

    participants: List[UUID] = Field(
        default=None,
        min_items=1,
        description="List of users participating in the expense.",
    )
    expense_type: Optional[ExpenseType] = Field(default=None)
