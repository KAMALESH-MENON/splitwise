from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.models.data_models import Expense
from src.app.schemas.expense_schemas import ExpenseCreate, ExpenseType, SplitType
from src.app.services.unit_of_work import ExpenseUnitOfWork


def round_amount(amount: Decimal) -> Decimal:
    """
    Rounds the given amount to two decimal places using ROUND_HALF_UP method.

    Parameters:
        amount (Decimal): The amount to be rounded.

    Returns:
        Decimal: The rounded amount.
    """
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_expense_data(expense_data: ExpenseCreate, uow: ExpenseUnitOfWork) -> None:
    """
    Validates the expense data.

    Parameters:
        expense_data (ExpenseCreate): The expense details from the request body.
        uow (ExpenseUnitOfWork): The database session manager.

    Raises:
        HTTPException: If the amount is invalid, user/group doesn't exist, or participants are invalid.
    """
    if expense_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    paid_by_user = uow.user.get(id=expense_data.paid_by)
    if not paid_by_user:
        raise HTTPException(status_code=400, detail="Paid-by user does not exist.")
    if expense_data.group_id:
        group_exists = uow.group.get(id=expense_data.group_id)
        if not group_exists:
            raise HTTPException(status_code=400, detail="Group ID does not exist.")
    invalid_participants = [
        p for p in expense_data.participants if not uow.user.get(id=p)
    ]
    if invalid_participants:
        raise HTTPException(
            status_code=400,
            detail=f"Participants with IDs {invalid_participants} do not exist.",
        )
    if expense_data.group_id:
        invalid_group_participants = [
            p
            for p in expense_data.participants
            if not uow.group_users.get_all(user_id=p, group_id=expense_data.group_id)
        ]
        if invalid_group_participants:
            raise HTTPException(
                status_code=400,
                detail=f"Participants with IDs {invalid_group_participants} are not in the specified group.",
            )


def handle_split(
    expense_data: ExpenseCreate, expense: Expense, uow: ExpenseUnitOfWork
) -> None:
    """
    Handles the splitting of the expense among participants.

    Parameters:
        expense_data (ExpenseCreate): The expense details from the request body.
        expense (Expense): The expense instance.
        uow (ExpenseUnitOfWork): The database session manager.

    Raises:
        HTTPException: If the split details are invalid.
    """
    total_amount_decimal = Decimal(expense_data.total_amount)
    tolerance = Decimal("0.01")

    if expense_data.split_type == SplitType.EQUALLY:
        handle_equally_split(expense_data, expense, uow, total_amount_decimal)
    elif expense_data.split_type == SplitType.UNEQUALLY:
        handle_unequally_split(
            expense_data, expense, uow, total_amount_decimal, tolerance
        )
    elif expense_data.split_type == SplitType.BY_SHARES:
        handle_by_shares_split(
            expense_data, expense, uow, total_amount_decimal, tolerance
        )
    elif expense_data.split_type == SplitType.BY_PERCENTAGE:
        handle_by_percentage_split(
            expense_data, expense, uow, total_amount_decimal, tolerance
        )
    elif expense_data.split_type == SplitType.BY_ADJUSTMENTS:
        handle_by_adjustments_split(
            expense_data, expense, uow, total_amount_decimal, tolerance
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid split type.")


def handle_equally_split(
    expense_data: ExpenseCreate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
) -> None:
    split_amount = round_amount(total_amount_decimal / len(expense_data.participants))
    for participant in expense_data.participants:
        uow.expense_split.add(
            expense_id=expense.id,
            user_id=participant,
            amount_owed=split_amount,
            split_type=SplitType.EQUALLY.value,
        )


def handle_unequally_split(
    expense_data: ExpenseCreate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    if not expense_data.amounts or len(expense_data.amounts) != len(
        expense_data.participants
    ):
        raise HTTPException(
            status_code=400, detail="Invalid amounts for UNEQUALLY split."
        )
    total_provided = sum(Decimal(amount) for amount in expense_data.amounts)
    if abs(total_provided - total_amount_decimal) > tolerance:
        difference = round_amount(total_amount_decimal - total_provided)
        if difference > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided amounts ({total_provided}) is less than total amount ({total_amount_decimal}) by {difference}.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided amounts ({total_provided}) is more than total amount ({total_amount_decimal}) by {-difference}.",
            )
    for participant, amount in zip(expense_data.participants, expense_data.amounts):
        uow.expense_split.add(
            expense_id=expense.id,
            user_id=participant,
            amount_owed=round_amount(Decimal(amount)),
            split_type=SplitType.UNEQUALLY.value,
        )


def handle_by_shares_split(
    expense_data: ExpenseCreate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    if not expense_data.shares or len(expense_data.shares) != len(
        expense_data.participants
    ):
        raise HTTPException(
            status_code=400, detail="Invalid shares for BY SHARES split."
        )
    total_shares = sum(expense_data.shares)
    if total_shares == 0:
        raise HTTPException(status_code=400, detail="Total shares cannot be zero.")
    total_provided = sum(
        (Decimal(share) / Decimal(total_shares)) * total_amount_decimal
        for share in expense_data.shares
    )
    if abs(total_provided - total_amount_decimal) > tolerance:
        difference = round_amount(total_amount_decimal - total_provided)
        if difference > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided shares does not match total amount ({total_amount_decimal}). Difference: {difference} less.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided shares does not match total amount ({total_amount_decimal}). Difference: {-difference} more.",
            )
    for participant, share in zip(expense_data.participants, expense_data.shares):
        amount_owed = round_amount(
            (Decimal(share) / Decimal(total_shares)) * total_amount_decimal
        )
        uow.expense_split.add(
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_SHARES.value,
        )


def handle_by_percentage_split(
    expense_data: ExpenseCreate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    if not expense_data.percentages or len(expense_data.percentages) != len(
        expense_data.participants
    ):
        raise HTTPException(
            status_code=400, detail="Invalid percentages for BY PERCENTAGE split."
        )
    total_percentage = sum(expense_data.percentages)
    if total_percentage != Decimal(100):
        raise HTTPException(
            status_code=400,
            detail=f"Sum of provided percentages ({total_percentage}) does not equal 100%.",
        )
    total_provided = sum(
        (Decimal(percentage) / Decimal(100)) * total_amount_decimal
        for percentage in expense_data.percentages
    )
    if abs(total_provided - total_amount_decimal) > tolerance:
        difference = round_amount(total_amount_decimal - total_provided)
        if difference > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided percentages does not match total amount ({total_amount_decimal}). Difference: {difference} less.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided percentages does not match total amount ({total_amount_decimal}). Difference: {-difference} more.",
            )
    for participant, percentage in zip(
        expense_data.participants, expense_data.percentages
    ):
        amount_owed = round_amount(
            (Decimal(percentage) / Decimal(100)) * total_amount_decimal
        )
        uow.expense_split.add(
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_PERCENTAGE.value,
        )


def handle_by_adjustments_split(
    expense_data: ExpenseCreate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    split_amount = round_amount(total_amount_decimal / len(expense_data.participants))
    adjustments = expense_data.adjustments or [0] * len(expense_data.participants)
    total_provided = sum(
        round_amount(split_amount + Decimal(adjustment)) for adjustment in adjustments
    )
    if abs(total_provided - total_amount_decimal) > tolerance:
        difference = round_amount(total_amount_decimal - total_provided)
        if difference > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided adjustments does not match total amount ({total_amount_decimal}). Difference: {difference} less.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided adjustments does not match total amount ({total_amount_decimal}). Difference: {-difference} more.",
            )
    for participant, adjustment in zip(expense_data.participants, adjustments):
        amount_owed = round_amount(split_amount + Decimal(adjustment))
        uow.expense_split.add(
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_ADJUSTMENTS.value,
        )


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
    with unit_of_work as uow:
        try:
            validate_expense_data(expense_data, uow)
            expense_type = (
                ExpenseType.GROUP
                if expense_data.group_id
                else ExpenseType.NON_EXPENSE_GROUP
            )
            expense_data_dict = {
                "group_id": expense_data.group_id,
                "total_amount": expense_data.total_amount,
                "description": expense_data.description,
                "expense_type": expense_type.value,
                "paid_by": expense_data.paid_by,
                "created_at": datetime.now(timezone.utc),
            }
            uow.expense.add(**expense_data_dict)
            expense = (
                uow.session.query(Expense)
                .filter_by(
                    group_id=expense_data.group_id,
                    total_amount=expense_data.total_amount,
                    description=expense_data.description,
                    expense_type=expense_type.value,
                    paid_by=expense_data.paid_by,
                    created_at=expense_data_dict["created_at"],
                )
                .first()
            )

            if not expense:
                raise HTTPException(
                    status_code=500, detail="Failed to retrieve the added expense."
                )

            handle_split(expense_data, expense, uow)
            return {"message": "Expense successfully added."}
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500, detail="Database error occurred while adding expense."
            )
