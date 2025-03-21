from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.config.database import get_db
from src.app.schemas.schemas import ExpenseSchema
from src.app.services.expense_service import add_expense, update_expense
from src.app.services.unit_of_work import ActivityUnitOfWork, ExpenseUnitOfWork

router = APIRouter(tags=["Expense Routes"])


@router.post("/expenses/", response_model=ExpenseSchema)
def create_expense(
    user_id: str,
    group_id: str,
    description: str,
    amount: float,
    db: Session = Depends(get_db),
):
    """
    Add a new expense and log the activity.
    """
    uow = ExpenseUnitOfWork(session_factory=get_db)
    activity_uow = ActivityUnitOfWork(session_factory=get_db)
    expense = add_expense(uow, activity_uow, user_id, group_id, description, amount)
    return expense


@router.put("/expenses/{expense_id}")
def modify_expense(
    expense_id: str,
    user_id: str,
    group_id: str,
    new_description: str,
    new_amount: float,
    db: Session = Depends(get_db),
):
    """
    Update an existing expense and log the activity.
    """
    uow = ExpenseUnitOfWork(session_factory=get_db)
    activity_uow = ActivityUnitOfWork(session_factory=get_db)
    update_expense(
        uow, activity_uow, user_id, group_id, expense_id, new_description, new_amount
    )
    return {"message": "Expense updated successfully"}
