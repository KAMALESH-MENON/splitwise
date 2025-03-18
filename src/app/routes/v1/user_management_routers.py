from fastapi import APIRouter, Depends

from src.app.schemas.user_schemas import LoginInput, LoginOutput, UserCreate
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.services.user_service import AuthService

router = APIRouter(tags=["User Management Routes"])


def get_uow() -> UserUnitOfWork:
    """
    Dependency function to get a Unit of Work instance.

    Returns:
        UserUnitOfWork: An instance of the unit of work for database transactions.
    """
    return UserUnitOfWork()


@router.post("/login", response_model=LoginOutput)
def login(login_user: LoginInput, uow: UserUnitOfWork = Depends(get_uow)):
    """
    Authenticates a user and returns an access token.

    Args:
        login_user (LoginInput): The login credentials (email and password).
        uow (UserUnitOfWork, optional): The unit of work dependency for database transactions. Defaults to using `get_uow()`.

    Returns:
        LoginOutput: A response containing the JWT access token and token type.
    """
    return AuthService().login(login_user, uow)
