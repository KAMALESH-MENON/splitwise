from pydantic import ValidationError

from src.app.schemas.settleup_schemas import SettleUpRequest, SettleUpResponse
from src.app.services.unit_of_work import SettleUpUnitOfWork


def settle_up_service(
    unit_of_work: SettleUpUnitOfWork, request_data: dict
) -> SettleUpResponse:
    """
    Service function to handle settle-up logic.

    param unit_of_work: Instance of SettleUpUnitOfWork.
    param request_data: Dictionary containing settle-up request data.
    return: SettleUpResponse object.
    """
    try:
        request = SettleUpRequest(**request_data)

        with unit_of_work as uow:
            settlement = uow.settlement_repository.get_all(
                payer_id=request.payer_id,
                payee_id=request.receiver_id,
                is_settled=False,
            )

            if not settlement:
                return SettleUpResponse(
                    message="No unsettled balance found between the payer and receiver.",
                    remaining_balance=0.0,
                    payer_id=request.payer_id,
                    receiver_id=request.receiver_id,
                    settled_amount=0.0,
                )

            settlement = settlement[0]
            if settlement.amount < request.amount:
                raise ValueError("Amount exceeds the outstanding balance.")

            settlement.amount -= request.amount
            if settlement.amount == 0:
                settlement.is_settled = True

            uow.settlement_repository.update(
                settlement.id,
                amount=settlement.amount,
                is_settled=settlement.is_settled,
            )

            return SettleUpResponse(
                message="Settlement completed successfully.",
                remaining_balance=settlement.amount,
                payer_id=request.payer_id,
                receiver_id=request.receiver_id,
                settled_amount=request.amount,
            )

    except ValidationError as e:
        raise ValueError(f"Invalid request data: {e}")
    except Exception as e:
        raise ValueError(f"Error during settlement: {e}")
