from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.schemas.expense_schemas import ExpenseResponse
from src.app.services.group_services import get_expense_from_group
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])

authorization_header_scheme = HTTPBearer()


@router.get("/groups/{group_id}/expenses", response_model=List[ExpenseResponse])
def get_group_expenses(
    group_id: UUID,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
    """
    Retrieve all expenses associated with a specific group.

    Args:

        group_id (UUID):
            The unique identifier of the group.

        token (HTTPAuthorizationCredentials):
            The JWT authorization token extracted from the request header.

    Returns:

        List[ExpenseResponse]:
            A list of expenses belonging to the specified group.

    Raises:

        HTTPException:
            If the user is unauthorized or the group does not exist.
    """
    unit_of_work = GroupUnitOfWork()
    return get_expense_from_group(
        unit_of_work=unit_of_work,
        group_id=group_id,
        token=token,
    )
