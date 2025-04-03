from uuid import UUID

from fastapi import HTTPException

from src.app.services.unit_of_work import ExpenseUnitOfWork


def delete_expense_by_id(unit_of_work: ExpenseUnitOfWork, expense_id: UUID) -> None:
    """
    Service function to delete an expense by ID.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_id (UUID): The ID of the expense to delete.

    Raises:
        HTTPException: If the expense is not found.
    """
    with unit_of_work as uow:
        expense = uow.expense.get(id=expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        for split in expense.splits:
            uow.expense_split.delete(id=split.id)

        uow.expense.delete(id=expense_id)
