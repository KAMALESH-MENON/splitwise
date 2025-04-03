from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.app.schemas.expense_schemas import ExpenseResponse
from src.app.services.expense_services import get_expense_by_id
from src.app.services.unit_of_work import ExpenseUnitOfWork

router = APIRouter(tags=["Expense Management Routes"])


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def view_expense(expense_id: UUID):
    """
    API route to view a particular expense by ID.

    Parameters:
        expense_id (UUID): The ID of the expense to retrieve.

    Returns:
        ExpenseResponse: The details of the expense.
    """
    with ExpenseUnitOfWork() as unit_of_work:
        expense = get_expense_by_id(unit_of_work=unit_of_work, expense_id=expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense
