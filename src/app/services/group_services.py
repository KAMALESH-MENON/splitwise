from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.app.config.settings import app_config
from src.app.schemas.expense_schemas import ExpenseResponse
from src.app.services.unit_of_work import GroupUnitOfWork


def decode_jwt(token: HTTPAuthorizationCredentials) -> UUID:
    """
    Decodes a JWT token and extracts the user ID.
    Parameters:
        token (HTTPAuthorizationCredentials):
            The JWT token extracted from the request header.
    Returns:
        UUID:
            The extracted user ID from the decoded token.
    Raises:
        HTTPException:
            If the token is invalid, expired, or missing the user_id.
    """
    try:
        decoded_payload = jwt.decode(
            token.credentials,
            app_config["SECRET_KEY"],
            algorithms=[app_config["ALGORITHM"]],
        )
        user_id = decoded_payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token: user_id not found"
            )
        return UUID(user_id)
    except JWTError as jwt_error:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token"
        ) from jwt_error


def get_expense_from_group(
    unit_of_work: GroupUnitOfWork,
    group_id: UUID,
    token: HTTPAuthorizationCredentials,
) -> List[ExpenseResponse]:
    """
    Retrieves all expenses for a given group.

    Args:
        unit_of_work (GroupUnitOfWork):
            The unit of work to manage database transactions.

        group_id (UUID):
            The unique identifier of the group.

        token (HTTPAuthorizationCredentials):
            The JWT authorization token used to authenticate the request.

    Returns:
        List[ExpenseResponse]:
            A list of expenses associated with the specified group.

    Raises:
        HTTPException (403):
            If the user is not a member of the specified group.

        HTTPException (404):
            If no expenses are found for the given group.
    """
    with unit_of_work as uow:
        user_id_from_token = decode_jwt(token)
        if not is_group_member(group_id, user_id_from_token, uow):
            raise HTTPException(
                status_code=403, detail="User is not a member of the group"
            )

        expense_list = uow.expense.get_all(group_id=group_id)
        if expense_list:
            group_expense_list = [
                ExpenseResponse.model_validate(expense.__dict__)
                for expense in expense_list
            ]
        else:
            group_expense_list = []  # return an empty list if no expenses are found

    return group_expense_list


def is_group_member(
    group_id: UUID,
    user_id: UUID,
    unit_of_work: GroupUnitOfWork,
) -> bool:
    """
    Checks if a user is a member of the specified group.
    Parameters:
        group_id (UUID):
            The unique identifier of the group.
        user_id (UUID):
            The unique identifier of the user.
    Returns:
        bool:
            True if the user is a member of the group, False otherwise.
    """
    with unit_of_work as uow:
        group = uow.group.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        if group.created_by == user_id:
            return True
        group_user = uow.group_user.get_all(group_id=group_id, user_id=user_id)
        if group_user:
            return True
        return False
