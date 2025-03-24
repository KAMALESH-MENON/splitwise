from fastapi import APIRouter, Depends, HTTPException
from src.app.schemas.user_profile_schema import DeleteUserSchema
from src.app.services.delete_user_service import UserService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork

router = APIRouter(tags=["User Profile Routes"])

@router.delete("/delete-user")
def delete_user(data: DeleteUserSchema, uow: UserUnitOfWork = Depends(get_user_uow)):
    """
    API route to delete a user.

    This endpoint allows deleting a user from the system by providing a valid user ID.
    It utilizes a service layer to handle business logic and interacts with the database 
    through a Unit of Work (UoW) pattern.

    Args:
        data (DeleteUserSchema): Request body containing the user ID to be deleted.
        uow (UserUnitOfWork, optional): Dependency injection for the user unit of work 
                                         to manage database transactions. Defaults to Depends(get_user_uow).

    Returns:
        dict: A success message if the user is deleted.

    Raises:
        HTTPException: If the provided user ID is invalid or if an error occurs during deletion.
    """
    service = UserService(uow)
    try:
        service.delete_user(data.user_id)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
