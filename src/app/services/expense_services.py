from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.models.data_models import Expense, Group, User
from src.app.schemas.expense_schemas import (
    ExpenseCreate,
    ExpenseCreateResponse,
    ExpenseType,
)
from src.app.services.unit_of_work import ExpenseUnitOfWork


def add_expense(unit_of_work: ExpenseUnitOfWork, expense_data: ExpenseCreate):
    """
    Service function to add a new expense.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_data (ExpenseCreate): The expense details from the request body.

    Returns:
        ExpenseCreateResponse: Success message.

    Raises:
        HTTPException: If the amount is invalid or user/group doesn't exist.
    """
    if expense_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")

    with unit_of_work as uow:
        try:
            paid_by_user = (
                uow.session.query(User).filter(User.id == expense_data.paid_by).first()
            )
            if not paid_by_user:
                raise HTTPException(
                    status_code=400, detail="Paid-by user does not exist."
                )

            expense_type = ExpenseType.NON_EXPENSE_GROUP
            if expense_data.group_id:
                group_exists = (
                    uow.session.query(Group)
                    .filter(Group.id == expense_data.group_id)
                    .first()
                )
                if not group_exists:
                    raise HTTPException(
                        status_code=400, detail="Group ID does not exist."
                    )
                expense_type = ExpenseType.GROUP

            new_expense = Expense(
                id=uuid4(),
                group_id=expense_data.group_id,
                total_amount=expense_data.total_amount,
                description=expense_data.description,
                expense_type=expense_type.value,
                paid_by=expense_data.paid_by,
                created_at=datetime.utcnow(),
            )

            uow.expense.add(new_expense)

            return ExpenseCreateResponse()

        except SQLAlchemyError:
            raise HTTPException(
                status_code=500, detail="Database error occurred while adding expense."
            )
