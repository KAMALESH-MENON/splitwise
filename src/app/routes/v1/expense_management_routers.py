from uuid import UUID

from fastapi import APIRouter

from src.app.services.expense_services import delete_expense_by_id
from src.app.services.unit_of_work import ExpenseUnitOfWork

router = APIRouter(tags=["Expense Management Routes"])


@router.delete("/expenses/{expense_id}", status_code=200)
def delete_expense(expense_id: UUID):
    """
    API route to delete a particular expense by ID.

    Parameters:
        expense_id (UUID): The ID of the expense to delete.

    Returns:
        dict: Confirmation message indicating the expense has been deleted.
    """
    with ExpenseUnitOfWork() as unit_of_work:
        delete_expense_by_id(unit_of_work=unit_of_work, expense_id=expense_id)
        return {
            "message": f"Expense with ID {expense_id} has been deleted successfully."
        }
