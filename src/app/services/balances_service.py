from uuid import UUID

from src.app.schemas.balances_schemas import BalanceResponse, BalanceStatus
from src.app.services.unit_of_work import BalanceUnitOfWork


def calculate_balances(uow: BalanceUnitOfWork, group_id: UUID) -> list[BalanceResponse]:
    """
    Calculate the net balances for users in a group.

    Args:
        uow (BalanceUnitOfWork): Unit of Work instance to manage database transactions.
        group_id (UUID): The ID of the group for which balances are calculated.

    Returns:
        list[BalanceResponse]: A list of BalanceResponse objects containing user balances
        and their statuses (OWED or OWES or SETTLED).
    """

    with uow as uow:
        expense_splits = uow.expense_splits.get_all(expense_id=group_id)

        settlements = uow.settlements.get_all()

        expense_splits_data = [
            {
                "user_id": split.user_id,
                "amount_owed": split.amount_owed,
                "paid_by": split.expense.paid_by,
            }
            for split in expense_splits
        ]

        settlements_data = [
            {
                "payer_id": settlement.payer_id,
                "payee_id": settlement.payee_id,
                "amount": settlement.amount,
            }
            for settlement in settlements
        ]

    if not expense_splits_data and not settlements_data:
        return []

    balances = {}

    for split in expense_splits_data:
        user_id = split["user_id"]
        amount = split["amount_owed"]

        if split["paid_by"] == user_id:
            balances[user_id] = balances.get(user_id, 0) + amount
        else:
            balances[user_id] = balances.get(user_id, 0) - amount

    for settlement in settlements_data:
        payer_id = settlement["payer_id"]
        payee_id = settlement["payee_id"]
        amount = settlement["amount"]

        balances[payer_id] = balances.get(payer_id, 0) - amount

        balances[payee_id] = balances.get(payee_id, 0) + amount

    return [
        BalanceResponse(
            user_id=user_id,
            balance=balance,
            status=BalanceStatus.OWED if balance > 0 else BalanceStatus.OWES,
        )
        for user_id, balance in balances.items()
    ]
