from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.balances_schemas import BalanceResponse
from src.app.services.balances_service import calculate_balances
from src.app.services.unit_of_work import BalanceUnitOfWork

router = APIRouter(tags=["balances"])


@router.get("/balances", response_model=list[BalanceResponse])
def view_balance(id: UUID):
    """
    API to view a user's balance.

    param id: UUID of the user.
    return: List of BalanceResponse containing net balance and breakdown.
    """
    unit_of_work = BalanceUnitOfWork()
    return calculate_balances(uow=unit_of_work, group_id=id)
