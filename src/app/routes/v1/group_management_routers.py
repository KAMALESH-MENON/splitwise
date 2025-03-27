from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.schemas.group_schemas import GroupResponse, GroupUpdateRequest
from src.app.services.group_services import update_group
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])

authorization_header_scheme = HTTPBearer()


@router.patch("/groups/{group_id}", response_model=GroupResponse)
def update_group_details(
    group_id: UUID,
    group_update: GroupUpdateRequest,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
    """
    Update the details of a specific group by its unique identifier.

    Parameters:

        group_id (UUID):
            The unique identifier of the group.

        group_update (GroupUpdateRequest):
            The request body containing the updated group details.

        token (HTTPAuthorizationCredentials):
            The authentication token provided in the request header.

    Returns:

        GroupResponse:
            The response model containing the updated group's details.
    """
    unit_of_work = GroupUnitOfWork()
    return update_group(
        unit_of_work=unit_of_work,
        group_id=group_id,
        group_update=group_update,
        token=token,
    )
