from fastapi import APIRouter, Depends

from src.app.schemas.expense_schemas import ExpenseCreate
from src.app.services.expense_services import add_expense
from src.app.services.unit_of_work import ExpenseUnitOfWork

router = APIRouter(tags=["Expense Management Routes"])


@router.post("/expenses/")
def create_expense(expense_data: ExpenseCreate):
    """
    API route to add a new expense.

    Parameters:
        expense_data (ExpenseCreate): The expense details from the request body.

    Returns:
        dict: Success message.
    """
    with ExpenseUnitOfWork() as unit_of_work:
        return add_expense(unit_of_work=unit_of_work, expense_data=expense_data)
