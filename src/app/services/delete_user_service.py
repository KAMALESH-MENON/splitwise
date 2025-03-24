from uuid import UUID
from src.app.services.unit_of_work import UserUnitOfWork

class UserService:
    """
    Service class for handling user-related operations.

    This class encapsulates the business logic for user management and 
    interacts with the database through a Unit of Work (UoW) pattern.

    Attributes:
        uow (UserUnitOfWork): The unit of work instance for managing database transactions.
    """

    def __init__(self, uow: UserUnitOfWork):
        """
        Initializes the UserService with a unit of work instance.

        Args:
            uow (UserUnitOfWork): The unit of work instance responsible for 
                                  managing database operations.
        """
        self.uow = uow

    def delete_user(self, user_id: UUID) -> None:
        """
        Deletes a user by their unique identifier.

        This method retrieves the user from the repository and deletes them if they exist.
        If the user is not found, it raises a ValueError.

        Args:
            user_id (UUID): The unique identifier of the user to be deleted.

        Raises:
            ValueError: If the user with the given ID does not exist.
        """
        with self.uow:
            user = self.uow.user_repository.get(id=user_id)
            if not user:
                raise ValueError("User not found")

            self.uow.user_repository.delete(id=user_id)
