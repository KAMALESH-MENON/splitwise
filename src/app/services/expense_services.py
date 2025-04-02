from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.models.data_models import Expense
from src.app.schemas.expense_schemas import ExpenseType, ExpenseUpdate, SplitType
from src.app.services.unit_of_work import ExpenseUnitOfWork


def round_amount(amount: Decimal) -> Decimal:
    """
    Rounds the given amount to two decimal places using the ROUND_HALF_UP method.

    Parameters:
        amount (Decimal): The amount to be rounded.

    Returns:
        Decimal: The rounded amount.
    """
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def update_expense(
    unit_of_work: ExpenseUnitOfWork, expense_id: UUID, expense_data: ExpenseUpdate
) -> None:
    """
    Updates an expense with the provided data.

    Parameters:
        unit_of_work (ExpenseUnitOfWork): The database session manager.
        expense_id (UUID): The ID of the expense to update.
        expense_data (ExpenseUpdate): The updated expense details.

    Raises:
        HTTPException: If validation fails or a database error occurs.
    """
    if expense_data.total_amount is not None and expense_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")

    with unit_of_work as uow:
        try:
            if expense_data.paid_by:
                paid_by_user = uow.user.get(id=expense_data.paid_by)
                if not paid_by_user:
                    raise HTTPException(
                        status_code=400, detail="Paid-by user does not exist."
                    )

            if expense_data.group_id:
                group_exists = uow.group.get(id=expense_data.group_id)
                if not group_exists:
                    raise HTTPException(
                        status_code=400, detail="Group ID does not exist."
                    )

            expense = uow.expense.get(id=expense_id)
            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            update_data = {
                key: value
                for key, value in expense_data.model_dump().items()
                if value is not None
            }

            if expense_data.expense_type == ExpenseType.NON_EXPENSE_GROUP:
                update_data["group_id"] = None

            if update_data:
                if all(
                    expense.__dict__.get(key) == value
                    for key, value in update_data.items()
                ):
                    raise HTTPException(
                        status_code=400, detail="No changes detected, data is the same."
                    )
                update_data["updated_at"] = datetime.now(timezone.utc)
                uow.expense.update(id=expense_id, **update_data)

            total_amount = (
                expense_data.total_amount
                if expense_data.total_amount is not None
                else expense.total_amount
            )

            if total_amount is not None:
                if not expense_data.participants:
                    expense_data.participants = [
                        split.user_id for split in expense.splits
                    ]
                if not expense_data.split_type:
                    expense_data.split_type = expense.splits[0].split_type
                handle_split_update(expense_data, expense, uow, total_amount)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Database error occurred while updating expense.",
            )


def handle_split_update(
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount: Decimal,
) -> None:
    """
    Handles the update of expense splits based on the split type.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount (Decimal): The total amount of the expense.

    Raises:
        HTTPException: If the split type is invalid or participants are missing.
    """
    if not expense_data.participants:
        raise HTTPException(status_code=400, detail="Participants must be provided.")

    total_amount_decimal = Decimal(total_amount)
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
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
) -> None:
    """
    Handles the EQUALLY split type by dividing the total amount equally among participants.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount_decimal (Decimal): The total amount of the expense.

    Raises:
        HTTPException: If the calculated split amounts do not match the total amount.
    """
    split_amount = round_amount(total_amount_decimal / len(expense_data.participants))
    total_provided = split_amount * len(expense_data.participants)
    if total_provided != total_amount_decimal:
        difference = round_amount(total_amount_decimal - total_provided)
        if difference > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided amounts does not match total amount ({total_amount_decimal}). Difference: {difference} more.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided amounts does not match total amount ({total_amount_decimal}). Difference: {-difference} less.",
            )
    for participant, split in zip(expense_data.participants, expense.splits):
        uow.expense_split.update(
            id=split.id,
            expense_id=expense.id,
            user_id=participant,
            amount_owed=split_amount,
            split_type=SplitType.EQUALLY.value,
            updated_at=datetime.now(timezone.utc),
        )


def handle_unequally_split(
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    """
    Handles the UNEQUALLY split type by assigning specific amounts to each participant.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount_decimal (Decimal): The total amount of the expense.
        tolerance (Decimal): The allowed tolerance for rounding differences.

    Raises:
        HTTPException: If the provided amounts are invalid or do not match the total amount.
    """
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
                detail=f"Sum of provided amounts does not match total amount ({total_amount_decimal}). Difference: {difference} more.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided amounts does not match total amount ({total_amount_decimal}). Difference: {-difference} less.",
            )
    for participant, amount, split in zip(
        expense_data.participants, expense_data.amounts, expense.splits
    ):
        uow.expense_split.update(
            id=split.id,
            expense_id=expense.id,
            user_id=participant,
            amount_owed=round_amount(Decimal(amount)),
            split_type=SplitType.UNEQUALLY.value,
            updated_at=datetime.now(timezone.utc),
        )


def handle_by_shares_split(
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    """
    Handles the BY SHARES split type by dividing the total amount based on the shares provided for each participant.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount_decimal (Decimal): The total amount of the expense.
        tolerance (Decimal): The allowed tolerance for rounding differences.

    Raises:
        HTTPException: If the shares are invalid, total shares are zero, or the calculated amounts do not match the total amount.
    """
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
                detail=f"Sum of provided shares does not match total amount ({total_amount_decimal}). Difference: {difference} more.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided shares does not match total amount ({total_amount_decimal}). Difference: {-difference} less.",
            )
    for participant, share, split in zip(
        expense_data.participants, expense_data.shares, expense.splits
    ):
        amount_owed = round_amount(
            (Decimal(share) / Decimal(total_shares)) * total_amount_decimal
        )
        uow.expense_split.update(
            id=split.id,
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_SHARES.value,
            updated_at=datetime.now(timezone.utc),
        )


def handle_by_percentage_split(
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    """
    Handles the BY PERCENTAGE split type by dividing the total amount based on the percentages provided for each participant.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount_decimal (Decimal): The total amount of the expense.
        tolerance (Decimal): The allowed tolerance for rounding differences.

    Raises:
        HTTPException: If the percentages are invalid, their sum is not equal to 100%,
                       or the calculated amounts do not match the total amount.
    """
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
                detail=f"Sum of provided percentages does not match total amount ({total_amount_decimal}). Difference: {difference} more.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided percentages does not match total amount ({total_amount_decimal}). Difference: {-difference} less.",
            )
    for participant, percentage, split in zip(
        expense_data.participants, expense_data.percentages, expense.splits
    ):
        amount_owed = round_amount(
            (Decimal(percentage) / Decimal(100)) * total_amount_decimal
        )
        uow.expense_split.update(
            id=split.id,
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_PERCENTAGE.value,
            updated_at=datetime.now(timezone.utc),
        )


def handle_by_adjustments_split(
    expense_data: ExpenseUpdate,
    expense: Expense,
    uow: ExpenseUnitOfWork,
    total_amount_decimal: Decimal,
    tolerance: Decimal,
) -> None:
    """
    Handles the BY ADJUSTMENTS split type by dividing the total amount equally among participants
    and applying individual adjustments to each participant's share.

    Parameters:
        expense_data (ExpenseUpdate): The updated expense details.
        expense (Expense): The existing expense instance.
        uow (ExpenseUnitOfWork): The database session manager.
        total_amount_decimal (Decimal): The total amount of the expense.
        tolerance (Decimal): The allowed tolerance for rounding differences.

    Raises:
        HTTPException: If the adjustments are invalid or the calculated amounts do not match the total amount.
    """
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
                detail=f"Sum of provided adjustments does not match total amount ({total_amount_decimal}). Difference: {difference} more.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Sum of provided adjustments does not match total amount ({total_amount_decimal}). Difference: {-difference} less.",
            )
    for participant, adjustment, split in zip(
        expense_data.participants, adjustments, expense.splits
    ):
        amount_owed = round_amount(split_amount + Decimal(adjustment))
        uow.expense_split.update(
            id=split.id,
            expense_id=expense.id,
            user_id=participant,
            amount_owed=amount_owed,
            split_type=SplitType.BY_ADJUSTMENTS.value,
            updated_at=datetime.now(timezone.utc),
        )
