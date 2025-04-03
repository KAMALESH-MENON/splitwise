from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ExpenseType(str, Enum):
    """Enum for expense types matching the database."""

    GROUP = "GROUP"
    NON_EXPENSE_GROUP = "NON-EXPENSE GROUP"


class ExpenseSplitResponse(BaseModel):
    """Schema for viewing an expense split."""

    id: UUID
    user_id: UUID
    amount_owed: Decimal
    split_type: str
    updated_at: Optional[datetime]


class ExpenseResponse(BaseModel):
    """Schema for viewing an expense."""

    id: UUID
    total_amount: Decimal
    description: Optional[str]
    group_id: Optional[UUID]
    paid_by: UUID
    created_at: datetime
    expense_type: ExpenseType
    splits: List[ExpenseSplitResponse]
