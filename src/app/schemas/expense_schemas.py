from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ExpenseType(str, Enum):
    """Enum for expense types matching the database."""

    GROUP = "GROUP"
    NON_EXPENSE_GROUP = "NON-EXPENSE GROUP"


class ExpenseResponse(BaseModel):
    """Schema for viewing an expense."""

    id: UUID
    total_amount: Decimal
    description: Optional[str]
    group_id: Optional[UUID]
    paid_by: UUID
    created_at: datetime
    expense_type: ExpenseType
