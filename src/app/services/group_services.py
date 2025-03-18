from uuid import UUID

from fastapi import HTTPException

from src.app.schemas.group_schemas import GroupResponse
from src.app.services.unit_of_work import GroupUnitOfWork


def get_particular_group(
    unit_of_work: GroupUnitOfWork, group_id: UUID
) -> GroupResponse:
    """
    Retrieve a particular group by its ID.

    Parameters:
        unit_of_work (GroupUnitOfWork): The unit of work used for database operations.
        group_id (UUID): The ID of the group to retrieve.

    Returns:
        GroupResponse: The details of the group.

    Raises:
        HTTPException: If the group is not found.
    """
    with unit_of_work as uow:
        group = uow.group.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        group_response = GroupResponse.model_validate(group)
    return group_response
