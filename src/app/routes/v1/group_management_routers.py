from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.schemas.group_schemas import GroupMemberResponse
from src.app.services.group_services import get_group_members
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])

authorization_header_scheme = HTTPBearer()


@router.get("/groups/{group_id}/members", response_model=List[GroupMemberResponse])
def list_group_members(
    group_id: UUID,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
    """
    API endpoint to retrieve the list of members in a specified group.

    Args:

        group_id (UUID):
            The unique identifier of the group.

        token (HTTPAuthorizationCredentials):
            The authentication token extracted from the request header.

    Returns:

        List[GroupMemberResponse]:
            A list of group members with their details.

    Raises:

        HTTPException:
            If the requesting user is not authorized to view the group members.
    """
    unit_of_work = GroupUnitOfWork()
    return get_group_members(
        unit_of_work=unit_of_work,
        group_id=group_id,
        token=token,
    )
