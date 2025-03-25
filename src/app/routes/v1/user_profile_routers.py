from fastapi import APIRouter, Depends, HTTPException
from src.app.schemas.user_profile_schema import ChangePasswordSchema
from src.app.services.password_service import ChangePasswordService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork

router = APIRouter(tags=["User Profile Routes"])

@router.post("/change-password")
def change_password(data: ChangePasswordSchema, uow: UserUnitOfWork = Depends(get_user_uow)):
    """
    API endpoint to allow users to change their password.

    This endpoint:
    - Validates the old password before updating.
    - Updates the password in the database.
    - Enforces password validation rules defined in ChangePasswordSchema.

    Args:
        data (ChangePasswordSchema): The request payload containing user_id, old_password, and new_password.
        uow (UserUnitOfWork): Dependency-injected unit of work to manage database operations.

    Returns:
        dict: Success message if the password is changed.

    Raises:
        HTTPException 403: If the old password is incorrect.
        HTTPException 404: If the user is not found.
    """
    service = ChangePasswordService(uow)
    
    try:
        service.change_user_password(data.user_id, data.old_password, data.new_password)
        return {"message": "Password changed successfully"}
    
    except ValueError as e:
        error_message = str(e).lower()

        if "incorrect" in error_message:
            raise HTTPException(status_code=403, detail=str(e))         
        raise HTTPException(status_code=404, detail=str(e)) 
