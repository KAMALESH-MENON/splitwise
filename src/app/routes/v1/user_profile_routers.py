from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.app.schemas.user_profile_schema import DeleteUserSchema
from src.app.services.delete_user_service import UserService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork

router = APIRouter(tags=["User Profile Routes"])


authorization_header_scheme = HTTPBearer()

@router.delete("/delete-user")
def delete_user(
    data: DeleteUserSchema, 
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme), 
    uow: UserUnitOfWork = Depends(get_user_uow)
):
    """
    API route to delete a user.

    This endpoint allows deleting a user from the system by providing a valid user ID.
    It utilizes a service layer to handle business logic and interacts with the database 
    through a Unit of Work (UoW) pattern.

    Args:
        data (DeleteUserSchema): Request body containing the user ID to be deleted.
        token (HTTPAuthorizationCredentials): Authorization token for verifying user identity.
        uow (UserUnitOfWork, optional): Dependency injection for the user unit of work 
                                         to manage database transactions. Defaults to Depends(get_user_uow).

    Returns:
        dict: A success message if the user is deleted.

    Raises:
        HTTPException: If authentication fails, user ID is invalid, or an error occurs during deletion.
    """
    token_str = token.credentials

    service = UserService(uow)

    try:
        user_id = service.verify_token(token_str)

        service.delete_user(data.user_id)
        
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized access")
