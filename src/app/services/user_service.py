from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from redis import Redis

from src.app.config.redis import settings
from src.app.config.settings import app_config
from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import LoginInput, LoginOutput, UserCreate
from src.app.services.unit_of_work import UserUnitOfWork

redis_client = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
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
            if not db_user or not UserService.verify_password(
                user.password, db_user.password
            ):
                raise HTTPException(status_code=400, detail="Invalid email or password")
            access_token = UserService.create_access_token({"user_id": str(db_user.id)})
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

        if isinstance(data.get("user_id"), UUID):
            to_encode["user_id"] = str(data["user_id"])
        else:
            to_encode["user_id"] = data["user_id"]

        return jwt.encode(
            to_encode, app_config["SECRET_KEY"], algorithm=app_config["ALGORITHM"]
        )

    def logout(token: str):
        """

        Blacklists a JWT token by storing it in Redis until it expires.

        This function ensures that a logged-out token cannot be reused by adding it to
        Redis with an expiration time equal to its remaining lifetime.

        Args:
            token (str): The JWT access token that needs to be revoked.

        Returns:
            dict: A message indicating the logout was successful.

        Raises:
            HTTPException (401 Unauthorized): If the token is invalid or cannot be decoded.
        """
        try:
            payload = jwt.decode(
                token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]]
            )
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                expiry_time = datetime.fromtimestamp(
                    exp_timestamp, tz=timezone.utc
                ) - datetime.now(timezone.utc)
                redis_client.setex(
                    f"blacklist:{token}", int(expiry_time.total_seconds()), "revoked"
                )
            return {"message": "Logout successful"}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
