from datetime import datetime

from src.app.models.data_models import Expense, User
from src.app.schemas.schemas import ExpenseSchema
from src.app.services.unit_of_work import ActivityUnitOfWork, ExpenseUnitOfWork


def add_expense(
    uow: ExpenseUnitOfWork,
    activity_uow: ActivityUnitOfWork,
    user_id: str,
    group_id: str,
    description: str,
    amount: float,
):
    """
    Add a new expense and log the activity.
    """
    with uow:
        user = uow.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")

        user_name = user.name

        expense = Expense(
            group_id=group_id,
            total_amount=amount,
            description=description,
            expense_type="GROUP",
            paid_by=user_id,
            created_at=datetime.now(),
        )
        uow.add_expense(expense)
        uow.session.refresh(expense)

        expense_data = ExpenseSchema.from_orm(expense)

    with activity_uow:
        activity_uow.log_activity(
            user_id,
            group_id,
            f"{user_name} added expense '{description}' of Rs.{amount}.",
        )

    return expense_data


def update_expense(
    uow: ExpenseUnitOfWork,
    activity_uow: ActivityUnitOfWork,
    user_id: str,
    group_id: str,
    expense_id: str,
    new_description: str,
    new_amount: float,
):
    """
    Update an existing expense and log the activity.
    """
    with uow:
        user = uow.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")

        user_name = user.name

    with uow:
        expense = uow.session.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise ValueError(f"Expense with ID {expense_id} does not exist.")
        expense.description = new_description
        expense.total_amount = new_amount
        uow.commit()

    with activity_uow:
        activity_uow.log_activity(
            user_id,
            group_id,
            f"{user_name} Updated expense '{new_description}' to Rs.{new_amount}",
        )
