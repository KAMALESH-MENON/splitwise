from uuid import UUID
from src.app.services.unit_of_work import UserUnitOfWork

class ChangePasswordService:
    def __init__(self, uow: UserUnitOfWork):
        self.uow = uow

    def change_user_password(self, user_id: UUID, old_password: str, new_password: str) -> None:
        with self.uow:
            user = self.uow.user_repository.get(user_id)
            if not user:
                raise ValueError("User not found")

            if old_password != user.password:
                raise ValueError("Old password is incorrect")

            user.password = new_password
            
           