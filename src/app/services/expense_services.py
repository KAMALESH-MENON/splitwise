from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.schemas.expense_schemas import ExpenseCreate, ExpenseType
from src.app.services.unit_of_work import ExpenseUnitOfWork


def add_expense(unit_of_work: ExpenseUnitOfWork, expense_data: ExpenseCreate) -> dict:
    """
    Service function to add a new expense.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_data (ExpenseCreate): The expense details from the request body.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the amount is invalid, user/group doesn't exist, or a database error occurs.
    """
    if expense_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")

    with unit_of_work as uow:
        try:
            paid_by_user = uow.user.get(id=expense_data.paid_by)
            if not paid_by_user:
                raise HTTPException(
                    status_code=400, detail="Paid-by user does not exist."
                )

            expense_type = ExpenseType.NON_EXPENSE_GROUP
            if expense_data.group_id:
                group_exists = uow.group.get(id=expense_data.group_id)
                if not group_exists:
                    raise HTTPException(
                        status_code=400, detail="Group ID does not exist."
                    )
                expense_type = ExpenseType.GROUP

            uow.expense.add(
                group_id=expense_data.group_id,
                total_amount=expense_data.total_amount,
                description=expense_data.description,
                expense_type=expense_type.value,
                paid_by=expense_data.paid_by,
                created_at=datetime.utcnow(),
            )

            return {"message": "Expense successfully added."}

        except SQLAlchemyError:
            raise HTTPException(
                status_code=500, detail="Database error occurred while adding expense."
            )
