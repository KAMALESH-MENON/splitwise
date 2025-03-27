from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.schemas.group_schemas import GroupResponse
from src.app.services.group_services import list_user_groups
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])

authorization_header_scheme = HTTPBearer()


@router.get("/groups", response_model=List[GroupResponse])
def view_user_groups(
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
    """
    Endpoint to retrieve the list of groups that the authenticated user belongs to.

    Parameters:

        token (HTTPAuthorizationCredentials):
            The authentication token provided in the request header.

    Returns:

        List[GroupResponse]:
            A list of groups that the authenticated user is a member of.
    """
    unit_of_work = GroupUnitOfWork()
    return list_user_groups(unit_of_work=unit_of_work, token=token)
