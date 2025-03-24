from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.schemas.group_schemas import GroupInput
from src.app.services.group_services import add_group
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])

authorization_header_scheme = HTTPBearer()


@router.post("/groups", status_code=201)
def create_group(
    group: GroupInput,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
    """
    Create a new group in the Splitwise application.

    Parameters:
        group (NewGroup): The details of the group to create.

    Returns:
        GroupResponse: The details of the newly created group.
    """
    unit_of_work = GroupUnitOfWork()
    return add_group(
        unit_of_work=unit_of_work,
        group=group,
        token=token,
    )
