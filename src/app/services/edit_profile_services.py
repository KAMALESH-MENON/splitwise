from src.app.services.unit_of_work import UserUnitOfWork
from src.app.schemas.user_profile_schema import UserSchema

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

    def get_user_profile(self, user_id: str) -> UserSchema:
        """
        Fetches the user profile based on the given user ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            UserSchema: A Pydantic schema representing the user profile.

        Raises:
            ValueError: If the user is not found in the database.
        """
        with self.unit_of_work as uow:
            user = uow.user_repository.get(id=user_id)
            if not user:
                raise ValueError("User not found")

            return UserSchema.from_orm(user)  # Note: `from_orm` is deprecated in Pydantic v2.
