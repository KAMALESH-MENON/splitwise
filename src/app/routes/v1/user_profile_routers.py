from fastapi import APIRouter, Depends, HTTPException, Response
from uuid import UUID
from src.app.schemas.user_profile_schema import DeleteUserSchema
from src.app.services.delete_user_service import UserService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork

router = APIRouter(tags=["User Profile Routes"])

@router.delete("/users/{user_id}")
def delete_user(
    user_id: UUID,
    data: DeleteUserSchema,
    uow: UserUnitOfWork = Depends(get_user_uow),
):
    """
    API route to delete a user after verifying the password.

    Args:
        user_id (UUID): User ID to be deleted (provided in the URL path).
        data (DeleteUserSchema): Request body containing the user's password.
        uow (UserUnitOfWork, optional): Dependency injection for user unit of work.

    Returns:
        dict: Success message if deletion is successful.

    Raises:
        HTTPException: If password is incorrect or an error occurs.
    """
    service = UserService(uow)

    try:
        service.delete_user(user_id, data.password)
        return Response(status_code=204)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
