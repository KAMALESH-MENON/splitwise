from uuid import UUID

from fastapi import HTTPException

from src.app.schemas.group_schemas import GroupResponse
from src.app.services.unit_of_work import GroupUnitOfWork


def get_particular_group(unit_of_work: GroupUnitOfWork, id: UUID):
    with unit_of_work as uow:
        group = uow.group.get(id=id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        group_response = GroupResponse.model_validate(group)
    return group_response
