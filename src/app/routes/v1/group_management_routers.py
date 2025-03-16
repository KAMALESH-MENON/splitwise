from uuid import UUID

from fastapi import APIRouter

from src.app.schemas.group_schemas import GroupResponse
from src.app.services.group_services import get_particular_group
from src.app.services.unit_of_work import GroupUnitOfWork

router = APIRouter(tags=["Group Management Routes"])


@router.get("/groups/{group_id}", response_model=GroupResponse)
def view_particular_group(group_id: UUID):
    unit_of_work = GroupUnitOfWork()
    return get_particular_group(unit_of_work=unit_of_work, id=group_id)
