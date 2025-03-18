from uuid import UUID

from fastapi import HTTPException

from src.app.schemas.expense_schemas import ExpenseResponse, ExpenseType
from src.app.services.unit_of_work import ExpenseUnitOfWork


def get_expense_by_id(
    unit_of_work: ExpenseUnitOfWork, expense_id: UUID
) -> ExpenseResponse:
    """
    Service function to get an expense by ID.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_id (UUID): The ID of the expense to retrieve.

    Returns:
        ExpenseResponse: The details of the expense.

    Raises:
        HTTPException: If the expense is not found.
    """
    with unit_of_work as uow:
        expense = uow.expense.get(id=expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        return ExpenseResponse(
            id=expense.id,
            total_amount=expense.total_amount,
            description=expense.description,
            group_id=expense.group_id,
            paid_by=expense.paid_by,
            created_at=expense.created_at,
            expense_type=ExpenseType(expense.expense_type),
        )
