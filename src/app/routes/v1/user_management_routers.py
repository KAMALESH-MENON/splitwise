from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis import Redis

from src.app.auth.auth import JWTBearer
from src.app.config.redis import settings
from src.app.schemas.user_schemas import LoginInput, LoginOutput
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.services.user_service import UserService

router = APIRouter(tags=["User Management Routes"])
redis_client = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
)


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
    return UserService().login(login_user, uow)


@router.post("/logout")
def logout(token: str = Depends(JWTBearer())):
    """
    Logs out the user by blacklisting the provided JWT token.

    This endpoint ensures that a logged-out token is stored in Redis, preventing
    further use until it expires.

    Args:
        token (str): The JWT access token extracted from the request header
                     using the `JWTBearer` dependency.

    Returns:
        dict: A message confirming successful logout."
    """
    return UserService.logout(token)
