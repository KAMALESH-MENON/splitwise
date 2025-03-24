from fastapi import APIRouter, Depends, HTTPException
from src.app.schemas.user_profile_schema import ChangePasswordSchema
from src.app.services.password_service import ChangePasswordService
from src.app.services.unit_of_work import get_user_uow, UserUnitOfWork

router = APIRouter(tags=["User Profile Routes"])

@router.post("/change-password")
def change_password(data: ChangePasswordSchema, uow: UserUnitOfWork = Depends(get_user_uow)):
    service = ChangePasswordService(uow)
    try:
        service.change_user_password(data.user_id, data.old_password, data.new_password)
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))