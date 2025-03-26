from fastapi import APIRouter, Depends, HTTPException
from src.app.schemas.user_profile_schema import ChangePasswordSchema
from src.app.services.password_service import ChangePasswordService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork
from uuid import UUID

router = APIRouter(tags=["User Profile Routes"])

@router.put("/users/{user_id}/password")
def change_password(user_id: UUID, data: ChangePasswordSchema, uow: UserUnitOfWork = Depends(get_user_uow)):
    """
    API endpoint to allow users to change their password.

    Args:
        user_id (UUID): The ID of the user whose password is being changed.
        data (ChangePasswordSchema): Request payload containing old_password and new_password.
        uow (UserUnitOfWork): Dependency-injected unit of work for database operations.

    Returns:
        dict: Success message if password is changed.

    Raises:
        HTTPException 401: If the current password is incorrect.
        HTTPException 404: If the user is not found.
    """
    service = ChangePasswordService(uow)
    
    try:
        service.change_user_password(user_id, data.current_password, data.new_password)
        return {"message": "Password changed successfully"}
    
    except ValueError as e:
        error_message = str(e).lower()

        if "incorrect" in error_message:
            raise HTTPException(status_code=401, detail=str(e))         
        raise HTTPException(status_code=404, detail=str(e))

