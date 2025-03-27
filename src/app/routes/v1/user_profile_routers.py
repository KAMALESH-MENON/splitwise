from fastapi import APIRouter, Depends
from uuid import UUID
from src.app.services.edit_profile_services import UserProfileService
from src.app.services.unit_of_work import UserUnitOfWork, get_user_uow
from src.app.schemas.user_profile_schema import UserSchema

router = APIRouter(tags=["User Profile Routes"])

@router.get("/users/{user_id}", response_model=UserSchema)
def view_profile(user_id: UUID, unit_of_work: UserUnitOfWork = Depends(get_user_uow)):

    """
    Retrieve the profile details of a user by their unique user ID.
    This endpoint fetches the profile information of a user from the database
    using the provided user ID. If the user does not exist, an HTTP 404 error is raised.

    Args:
        user_id (UUID): The unique identifier of the user whose profile is to be retrieved.
        unit_of_work (UserUnitOfWork): The Unit of Work dependency injected by FastAPI.

    Returns:
        UserSchema: A Pydantic model containing the user's profile details.

    Raises:
        HTTPException (404): If no user exists with the given ID.
    """
    user_profile_service = UserProfileService(unit_of_work)
    return user_profile_service.get_user_profile(user_id)
