from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ExpenseType(str, Enum):
    """Enum for expense types matching the database."""

    GROUP = "GROUP"
    NON_EXPENSE_GROUP = "NON-EXPENSE GROUP"


class SplitType(str, Enum):
    """Enum for split types."""

    EQUALLY = "EQUALLY"
    UNEQUALLY = "UNEQUALLY"
    BY_SHARES = "BY SHARES"
    BY_PERCENTAGE = "BY PERCENTAGE"
    BY_ADJUSTMENTS = "BY ADJUSTMENTS"


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
    expense_type: Optional[ExpenseType] = Field(default=None)


class ExpenseUpdate(ExpenseBase):
    """Schema for updating an expense."""

    participants: List[UUID] = Field(
        default=None,
        min_items=1,
        description="List of users participating in the expense.",
    )
    split_type: Optional[SplitType] = Field(
        default=None,
        description="Type of split (UNEQUALLY, EQUALLY, BY SHARES, BY PERCENTAGE, BY ADJUSTMENTS).",
    )
    amounts: Optional[List[Decimal]] = Field(
        default=None,
        description="List of amounts for each participant (for UNEQUALLY split).",
    )
    shares: Optional[List[int]] = Field(
        default=None,
        description="List of shares for each participant (for BY SHARES split).",
    )
    percentages: Optional[List[Decimal]] = Field(
        default=None,
        description="List of percentages for each participant (for BY PERCENTAGE split).",
    )
    adjustments: Optional[List[Decimal]] = Field(
        default=None,
        description="List of adjustments for each participant (for BY ADJUSTMENTS split).",
    )
