from uuid import UUID

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from src.app.config.settings import app_config
from src.app.schemas.group_schemas import GroupResponse, GroupUpdateRequest
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


def update_group(
    unit_of_work: GroupUnitOfWork,
    group_id: UUID,
    group_update: GroupUpdateRequest,
    token: HTTPAuthorizationCredentials,
) -> GroupResponse:
    """
    Update the details of a specific group by its unique identifier.

    Parameters:
        unit_of_work (GroupUnitOfWork):
            The unit of work used for database operations.
        group_id (UUID):
            The unique identifier of the group.
        group_update (GroupUpdateRequest):
            The request body containing the updated group details.
        token (HTTPAuthorizationCredentials):
            The authentication token provided in the request header.

    Returns:
        GroupResponse:
            The response model containing the updated group's details.

    Raises:
        HTTPException:
            If the group is not found or if the user is not authorized to update the group.
    """
    with unit_of_work as uow:
        group = uow.group.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        user_id_from_token = decode_jwt(token)

        # Verify if the user is an admin
        if group.created_by != user_id_from_token:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update the group, User is not admin",
            )

        # To update only non-None fields
        update_data = {
            key: value
            for key, value in group_update.model_dump().items()
            if value is not None
        }
        if update_data:
            uow.group.update(id=group_id, **update_data)

        group = uow.group.get(id=group_id)
        updated_group_details = GroupResponse.model_validate(group)
    return updated_group_details
