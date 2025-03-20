from datetime import datetime, timezone

from fastapi.responses import JSONResponse
from passlib.context import CryptContext

from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import UserCreate
from src.app.services.unit_of_work import UserUnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service class for user authentication and registration.
    """

    @staticmethod
    def register(user: UserCreate, uow: UserUnitOfWork) -> JSONResponse:
        """
        Registers a new user in the system.

        Args:
            user (UserCreate): The user registration details.
            uow (UserUnitOfWork): The unit of work for handling database transactions.

        Returns:
            JSONResponse: A JSON response indicating success or failure.
                - 400 if the email or phone number already exists.
                - 201 if the user is successfully registered."
        """

        with uow:
            user_repo = UserRepository(uow.session)

            if user_repo.get(email=user.email):
                return JSONResponse(
                    status_code=409,
                    content={"error": "User with this email already exists"},
                )

            # Check if phone number already exists
            if user_repo.get(phone=user.phone):
                return JSONResponse(
                    status_code=409,
                    content={"error": "User with this phone number already exists"},
                )

            hashed_password = AuthService.get_password_hash(user.password)
            user_repo.add(
                name=user.name,
                email=user.email,
                phone=user.phone,
                profile_picture_url=user.profile_picture_url,
                created_at=datetime.now(timezone.utc),
                password=hashed_password,
            )
            return JSONResponse(
                status_code=201, content={"message": "User registered successfully"}
            )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashes the provided password using bcrypt.

        Args:
            password (str): The plaintext password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)
