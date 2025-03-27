from uuid import UUID
from src.app.services.unit_of_work import UserUnitOfWork

class ChangePasswordService:
    """
    Service responsible for handling user password changes.

    This service performs the following operations:
    - Validates if the user exists.
    - Checks if the provided current password matches the stored password.
    - Updates the password with a new one (without hashing).
    """

    def __init__(self, uow: UserUnitOfWork):
        """
        Initializes the ChangePasswordService with a Unit of Work (UoW).

        Args:
            uow (UserUnitOfWork): The Unit of Work instance that manages database transactions.
        """
        self.uow = uow

    def change_user_password(self, user_id: UUID, current_password: str, new_password: str) -> None:
        """
        Changes the user's password.

        Steps:
        1. Retrieves the user from the database using the provided user ID.
        2. Validates if the user exists.
        3. Compares the current password with the stored password.
        4. Updates the password with the new one if validation passes.
        5. Commits the changes to the database.

        Args:
            user_id (UUID): The unique identifier of the user.
            current_password (str): The current password that the user wants to change.
            new_password (str): The new password that the user wants to set.

        Raises:
            ValueError: If the user is not found in the database.
            ValueError: If the old password does not match the stored password.

        Returns:
            None
        """
        with self.uow:
            user = self.uow.user_repository.get(user_id)

 
            if not user:
                raise ValueError("User not found")

            if current_password != user.password:
                raise ValueError("current password is incorrect")

            user.password = new_password