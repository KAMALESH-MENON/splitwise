from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.app.config.settings import app_config
from src.app.schemas.group_schemas import GroupMemberResponse
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
        unit_of_work (GroupUnitOfWork):
            The unit of work instance to handle database operations.

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


def get_group_members(
    unit_of_work: GroupUnitOfWork,
    group_id: UUID,
    token: HTTPAuthorizationCredentials,
) -> List[GroupMemberResponse]:
    """
    Retrieves the list of members in a specified group.

    Args:
        unit_of_work (GroupUnitOfWork):
            The unit of work instance to handle database operations.
        group_id (UUID):
            The unique identifier of the group.
        token (HTTPAuthorizationCredentials):
            The authentication token of the requesting user.

    Returns:
        List[GroupMemberResponse]:
            A list of group members with their details.

    Raises:
        HTTPException:
            If the requesting user is not a member of the specified group.
    """
    with unit_of_work as uow:
        user_id_from_token = decode_jwt(token)
        if not is_group_member(group_id, user_id_from_token, uow):
            raise HTTPException(
                status_code=403, detail="User is not a member of the group"
            )

        user_list = []
        users = uow.group_user.get_all(group_id=group_id)

        for user in users:
            user_details = uow.user.get(user.user_id)
            user_list.append(GroupMemberResponse.model_validate(user_details.__dict__))

    return user_list
