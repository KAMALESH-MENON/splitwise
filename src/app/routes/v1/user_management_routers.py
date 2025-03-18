from fastapi import APIRouter, Depends

from src.app.config.database import SessionLocal
from src.app.schemas.user_schemas import UserCreate
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.services.user_service import AuthService

router = APIRouter(tags=["User Management Routes"])


def get_uow() -> UserUnitOfWork:
    """
    Dependency function to get a Unit of Work instance.

    Returns:
        UserUnitOfWork: An instance of the unit of work for database transactions.
    """
    return UserUnitOfWork(SessionLocal)


@router.post("/register")
def register(register_user: UserCreate, uow: UserUnitOfWork = Depends(get_uow)):
    """
    Registers a new user.

    Args:
        register_user (UserCreate): The user registration details.
        uow (UserUnitOfWork): The unit of work dependency for database operations. Defaults to using `get_uow()`.

    Returns:
        UserResponse: A response containing the registered user's details.
    """
    return AuthService().register(register_user, uow)
