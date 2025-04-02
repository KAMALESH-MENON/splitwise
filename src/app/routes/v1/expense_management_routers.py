from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.expense_schemas import ExpenseUpdate
from src.app.services.expense_services import update_expense
from src.app.services.unit_of_work import ExpenseUnitOfWork

router = APIRouter(tags=["Expense Management Routes"])


@router.patch("/expenses/{expense_id}")
def edit_expense(expense_id: UUID, expense_data: ExpenseUpdate):
    """
    API route to edit an existing expense.

    Parameters:
        expense_id (UUID): The ID of the expense to update.
        expense_data (ExpenseUpdate): The updated expense details from the request body.

    Returns:
        dict: Success message.
    """
    with ExpenseUnitOfWork() as unit_of_work:
        update_expense(
            unit_of_work=unit_of_work, expense_id=expense_id, expense_data=expense_data
        )
        return {"message": "Expense successfully updated."}
