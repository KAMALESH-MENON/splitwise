from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.app.config.settings import app_config
from src.app.schemas.group_schemas import GroupResponse
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


def list_user_groups(
    unit_of_work: GroupUnitOfWork, token: HTTPAuthorizationCredentials
) -> List[GroupResponse]:
    """
    Retrieves the list of groups that a user belongs to based on the provided authentication token.

    parameters:
        unit_of_work (GroupUnitOfWork):
            The unit of work responsible for handling database transactions related to groups and
                user-group associations.
        auth_token (HTTPAuthorizationCredentials):
            The authentication token containing the user's identity.

    Returns:
        List[GroupResponse]:
            A list of groups that the authenticated user is a member of.
    """
    user_id = decode_jwt(token)
    with unit_of_work as uow:
        user_group_associations = uow.group_user.get_all(user_id=user_id)
        user_groups = [
            GroupResponse.model_validate(uow.group.get(id=group_user.group_id))
            for group_user in user_group_associations
        ]

        return user_groups
