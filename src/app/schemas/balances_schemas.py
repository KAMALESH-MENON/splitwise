from enum import Enum

from pydantic import UUID4, BaseModel


class BalanceStatus(str, Enum):
    """
    Enum to represent the status of a user's balance.
    """

    OWES = "owes"
    OWED = "owed"
    SETTLED = "settled"


class BalanceResponse(BaseModel):
    """
    Schema for representing a user's balance details.

    Attributes:
        user_id (UUID4): The unique identifier of the user.
        balance (float): The balance amount for the user.
        status (BalanceStatus): The status of the user's balance (owes, owed, or settled).
    """

    user_id: UUID4
    balance: float
    status: BalanceStatus

    class Config:
        from_attributes = True
