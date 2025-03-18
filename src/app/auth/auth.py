from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from redis import Redis

from src.app.config.redis import settings
from src.app.config.settings import app_config

redis_client = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
)


class JWTBearer(HTTPBearer):
    """
    A custom security class that extends HTTPBearer to handle JWT authentication.

    This class:
    - Extracts the token from the request header.
    - Verifies that the token follows the Bearer authentication scheme.
    - Checks if the token is blacklisted (revoked) in Redis.
    - Provides methods to verify and extract user details from the JWT token.
    """

    def __init__(self, auto_error: bool = True):
        """
        Initializes the JWTBearer class.

        Args:
            auto_error (bool, optional): Whether to automatically raise an exception
                if authentication fails. Defaults to True.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Extracts and validates the JWT token from the request.

        Args:
            request (Request): The incoming FastAPI request.

        Returns:
            str: The extracted and validated JWT token.

        Raises:
            HTTPException: If the authentication scheme is invalid.
            HTTPException: If the token is revoked.
            HTTPException: If no valid authorization credentials are found.
        """
        credentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            token = credentials.credentials

            if redis_client.get(f"blacklist:{token}"):
                raise HTTPException(status_code=401, detail="Token has been revoked.")

            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> dict:
        """
        Verifies and decodes the JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            dict: The decoded JWT payload.

        Raises:
            HTTPException: If the token is invalid or expired.
            HTTPException: If the user_id is missing in the token.
        """
        try:
            payload = jwt.decode(
                token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]]
            )
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=401, detail="Invalid token: user_id not found"
                )
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

    def get_user_id_from_token(self, token: str) -> str:
        """
        Extracts the user ID from the JWT token.

        Args:
            token (str): The JWT token.

        Returns:
            str: The user ID extracted from the token.

        Raises:
            HTTPException: If the token is invalid or expired.
            HTTPException: If the user_id is missing from the token.
        """
        try:
            payload = self.verify_jwt(token)
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=401, detail="Invalid token: user_id not found"
                )
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
