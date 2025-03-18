from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.services.edit_profile_services import UserProfileService
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.config.database import get_db
from src.app.schemas.user_profile_schema import UserSchema

router = APIRouter(tags=["User Profile Routes"])

@router.get("/profile", response_model=UserSchema)
def view_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile details of a user by their unique user ID.

    Args:
        user_id (str): The unique identifier of the user whose profile is to be fetched.
        db (Session, optional): The database session dependency.

    Returns:
        UserSchema: A Pydantic model containing the user's profile information.

    Raises:
        HTTPException (404): If the user with the given ID is not found.
    """
    unit_of_work = UserUnitOfWork(session_factory=get_db)
    user_profile_service = UserProfileService(unit_of_work)
    try:
        user = user_profile_service.get_user_profile(user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
