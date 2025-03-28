from uuid import UUID

from sqlalchemy.orm import joinedload

from src.app.models.data_models import Settlements
from src.app.schemas.payment_schemas import PaymentHistoryResponse
from src.app.services.unit_of_work import PaymentUnitOfWork


def get_payment_history(user_id: UUID):
    """
    Service function to retrieve payment history for a user.
    """
    with PaymentUnitOfWork() as uow:
        transactions = (
            uow.settlement_repository.session.query(Settlements)
            .options(
                joinedload(Settlements.payer),
                joinedload(Settlements.payee),
                joinedload(Settlements.expense_split),
            )
            .filter(
                (Settlements.payer_id == user_id) | (Settlements.payee_id == user_id)
            )
            .order_by(Settlements.created_at.desc())
            .all()
        )

        return [PaymentHistoryResponse.model_validate(txn) for txn in transactions]
