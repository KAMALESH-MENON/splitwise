from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.config.database import get_db
from src.app.schemas.schemas import GroupSchema
from src.app.services.group_service import create_group
from src.app.services.unit_of_work import ActivityUnitOfWork, GroupUnitOfWork

router = APIRouter(tags=["Group Routes"])


@router.post("/groups/", response_model=GroupSchema)
def create_new_group(user_id: str, group_name: str, db: Session = Depends(get_db)):
    """
    Create a new group and log the activity.
    """
    uow = GroupUnitOfWork(session_factory=get_db)
    activity_uow = ActivityUnitOfWork(session_factory=get_db)
    group = create_group(uow, activity_uow, user_id, group_name)
    return group
