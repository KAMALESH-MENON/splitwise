from uuid import UUID

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.app.config.settings import app_config
from src.app.schemas.group_schemas import GroupInput
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


def add_group(
    unit_of_work: GroupUnitOfWork,
    group: GroupInput,
    token: HTTPAuthorizationCredentials,
) -> dict:
    """
    Adds a new group to the database.

    Args:
        unit_of_work (GroupUnitOfWork): The unit of work instance to manage database transactions.
        group (NewGroup): The group details to be added.
        token (HTTPAuthorizationCredentials): The authorization token containing user credentials.

    Returns:
        dict: A success message indicating that the group has been added.

    Raises:
        Exception: If there is an issue with the database transaction or JWT decoding.
    """

    with unit_of_work as uow:
        user_id_from_token = decode_jwt(token)
        uow.group.add(**group.model_dump(), created_by=user_id_from_token)

    return {"message": "New group added successfully"}
