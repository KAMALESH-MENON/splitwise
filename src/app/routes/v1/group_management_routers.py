from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.group_schemas import GroupResponse
from src.app.services.group_services import get_particular_group
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])


@router.get("/groups/{group_id}", response_model=GroupResponse)
def view_particular_group(group_id: UUID):
    """
    Retrieve details of a specific group by its unique identifier.

    Parameters:
        group_id (UUID): The unique identifier of the group.

    Returns:
        GroupResponse: The response model containing the group's details.
    """
    unit_of_work = GroupUnitOfWork()
    return get_particular_group(unit_of_work=unit_of_work, group_id=group_id)
