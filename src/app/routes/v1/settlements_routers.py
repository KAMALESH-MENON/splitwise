from typing import List
from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.payment_schemas import PaymentHistoryResponse
from src.app.services.payment_services import get_payment_history

router = APIRouter()


@router.get("/payment-history/{user_id}", response_model=List[PaymentHistoryResponse])
def payment_history(user_id: UUID):
    """
    API to get the payment history of a user.
    """
    return get_payment_history(user_id)
