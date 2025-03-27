from uuid import UUID
from src.app.services.unit_of_work import UserUnitOfWork

class UserService:
    """
    Service class for handling user-related operations.
    """

    def __init__(self, uow: UserUnitOfWork):
        """
        Initializes the UserService with a unit of work instance.
        """
        self.uow = uow

    def verify_password(self, user_id: UUID, password: str) -> bool:
        """
        Verifies if the provided password matches the user's stored password.

        Args:
            user_id (UUID): Unique identifier of the user.
            password (str): Password entered by the user.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            ValueError: If the user does not exist.
        """
        with self.uow:
            user = self.uow.user_repository.get(id=user_id)
            if not user:
                raise ValueError("User not found")

            if user.password != password:  
                return False
        return True

    def delete_user(self, user_id: UUID, password: str) -> None:
        """
        Deletes a user after verifying their password.

        Args:
            user_id (UUID): The unique identifier of the user to be deleted.
            password (str): The user's current password for authentication.

        Raises:
            ValueError: If the user does not exist or the password is incorrect.
        """
        if not self.verify_password(user_id, password):
            raise ValueError("Incorrect password")

        with self.uow:
            self.uow.user_repository.delete(id=user_id)
