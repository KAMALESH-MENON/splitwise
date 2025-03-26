from src.app.services.unit_of_work import UserUnitOfWork
from src.app.schemas.user_profile_schema import UserSchema
from uuid import UUID
from fastapi import HTTPException, status

class UserProfileService:
    """
    Service class responsible for user profile operations.
    This class uses the Unit of Work pattern to interact with the user repository
    and retrieve user profile details in a structured manner.
    """

    def __init__(self, unit_of_work: UserUnitOfWork):
        """
        Initializes the UserProfileService with a unit of work.
        Args:
            unit_of_work (UserUnitOfWork): An instance of the unit of work 
                                           that manages database operations.
        """
        self.unit_of_work = unit_of_work

    def get_user_profile(self, user_id: UUID) -> UserSchema:
        """
        Fetches the user profile based on the given user ID.
        Args:
            user_id (UUID): The unique identifier of the user.
        Returns:
            UserSchema: A Pydantic schema representing the user profile.
        Raises:
            HTTPException: If the user is not found in the database.
        """
        user = self.unit_of_work.user_repository.get(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserSchema.model_validate(user)
