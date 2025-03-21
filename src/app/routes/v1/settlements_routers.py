from fastapi import APIRouter, Depends, HTTPException

from src.app.schemas.settleup_schemas import SettleUpRequest, SettleUpResponse
from src.app.services.settleup_services import settle_up_service
from src.app.services.unit_of_work import SettleUpUnitOfWork

router = APIRouter()


@router.patch("/settle-up", response_model=SettleUpResponse)
def settle_up(
    request: SettleUpRequest,
):
    """
    API endpoint to settle up a transaction.
    """
    unit_of_work = SettleUpUnitOfWork()
    response = settle_up_service(unit_of_work, request.dict())
    return response
