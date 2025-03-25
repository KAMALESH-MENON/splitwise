from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import jwt
from passlib.context import CryptContext

from src.app.config.settings import app_config
from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import LoginInput, LoginOutput, UserCreate
from src.app.services.unit_of_work import UserUnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service class for user authentication and registration.
    """

    @staticmethod
    def login(user: LoginInput, uow: UserUnitOfWork) -> LoginOutput:
        """
        Authenticates a user and generates a JWT access token.

        Args:
            user (LoginInput): The login credentials (email and password).
            uow (UserUnitOfWork): The unit of work for managing database transactions.

        Returns:
            LoginOutput: A response containing the JWT access token and token type.

        Raises:
            HTTPException: 400 Bad Request if authentication fails due to incorrect credentials.
        """
        with uow:
            user_repo = UserRepository(uow.session)
            db_user = user_repo.get(email=user.email)
            if not db_user or not AuthService.verify_password(
                user.password, db_user.password
            ):
                raise HTTPException(status_code=401, detail="Invalid email or password")
            access_token = AuthService.create_access_token({"user_id": str(db_user.id)})
            return LoginOutput(access_token=access_token, token_type="bearer")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        """
        Verifies a plaintext password against its hashed version.

        Args:
            plain_password (str): The plaintext password entered by the user.
            hashed_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict):
        """
        Generates a JWT access token with an expiration time.

        Args:
            data (dict): The payload data, typically containing `user_id`.

        Returns:
            str: A signed JWT token.
        """
        to_encode = data.copy()
        expire_minutes = int(app_config["ACCESS_TOKEN_EXPIRE_MINUTES"])
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})

        to_encode["user_id"] = data["user_id"]

        return jwt.encode(
            to_encode, app_config["SECRET_KEY"], algorithm=app_config["ALGORITHM"]
        )
