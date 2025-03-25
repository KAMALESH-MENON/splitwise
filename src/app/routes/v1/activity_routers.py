from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.config.database import get_db
from src.app.models.data_models import Activity
from src.app.schemas.activity_schemas import ActivitySchema
from src.app.services.unit_of_work import BaseUnitOfWork

router = APIRouter(tags=["Activity Routes"])


@router.get("/activities/", response_model=List[ActivitySchema])
def get_activities(db: Session = Depends(get_db)):
    """
    Fetch all activities from the database.

    Parameters:
        db (Session): The database session.

    Returns:
        List[ActivitySchema]: A list of activities.
    """
    with BaseUnitOfWork(session_factory=get_db) as uow:
        activities = uow.session.query(Activity).all()

        activity_schemas = [
            ActivitySchema.from_orm(activity) for activity in activities
        ]

        return activity_schemas
