from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.services.edit_profile_services import UserProfileService
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.config.database import get_db
from src.app.schemas.user_profile_schema import UserSchema
from uuid import UUID

router = APIRouter(tags=["User Profile Routes"])

@router.get("/profile", response_model=UserSchema)
def view_profile(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve the profile details of a user by their unique user ID.

    This endpoint fetches the profile information of a user from the database
    using the provided user ID. If the user does not exist, an HTTP 404 error is raised.

    Args:
        user_id (UUID): The unique identifier of the user whose profile is to be retrieved.
        db (Session, optional): The database session dependency, injected using FastAPI's Depends.

    Returns:
        UserSchema: A Pydantic model containing the user's profile details.

    Raises:
        HTTPException: 
            - 404 Not Found: If no user exists with the given ID.
    """
    unit_of_work = UserUnitOfWork(session_factory=get_db)
    user_profile_service = UserProfileService(unit_of_work)
    try:
        user = user_profile_service.get_user_profile(user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
