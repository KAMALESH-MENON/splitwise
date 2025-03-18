from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.schemas.expense_schemas import ExpenseType, ExpenseUpdate
from src.app.services.unit_of_work import ExpenseUnitOfWork


def update_expense(
    unit_of_work: ExpenseUnitOfWork, expense_id: UUID, expense_data: ExpenseUpdate
) -> None:
    """
    Service function to update an expense.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_id (UUID): The ID of the expense to update.
        expense_data (ExpenseUpdate): The updated expense details from the request body.

    Raises:
        HTTPException: If the expense is not found or a database error occurs.
    """
    if expense_data.total_amount is not None and expense_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")

    with unit_of_work as uow:
        try:
            if expense_data.paid_by:
                paid_by_user = uow.user.get(id=expense_data.paid_by)
                if not paid_by_user:
                    raise HTTPException(
                        status_code=400, detail="Paid-by user does not exist."
                    )

            ExpenseType.NON_EXPENSE_GROUP
            if expense_data.group_id:
                group_exists = uow.group.get(id=expense_data.group_id)
                if not group_exists:
                    raise HTTPException(
                        status_code=400, detail="Group ID does not exist."
                    )
                ExpenseType.GROUP

            expense = uow.expense.get(id=expense_id)
            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            update_data = {
                key: value
                for key, value in expense_data.model_dump().items()
                if value is not None
            }
            if update_data:
                uow.expense.update(id=expense_id, **update_data)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error occurred while updating expense.",
            )
