from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentMethod(str, Enum):
    """
    Enum for valid payment methods.
    """

    UPI = "UPI"
    CASH = "Cash"
    CARD = "Card"
    BANK_TRANSFER = "Bank Transfer"


class SettleUpRequest(BaseModel):
    """
    Pydantic model for settle-up request validation.
    """

    amount: float = Field(gt=0)
    payer_id: UUID
    receiver_id: UUID
    method: PaymentMethod


class SettleUpResponse(BaseModel):
    """
    Pydantic model for settle-up response.
    """

    message: str
    remaining_balance: float
    payer_id: UUID
    receiver_id: UUID
    settled_amount: float
