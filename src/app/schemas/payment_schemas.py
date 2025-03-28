from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PaymentHistoryResponse(BaseModel):
    id: UUID
    payer_id: UUID
    payee_id: UUID
    amount: float
    created_at: datetime
    is_settled: bool

    class Config:
        from_attributes = True
