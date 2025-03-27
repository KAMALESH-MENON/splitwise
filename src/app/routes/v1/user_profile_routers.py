from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from uuid import UUID
from typing import Optional
from pydantic import ValidationError
from src.app.services.edit_profile_service import EditProfileService
from src.app.services.unit_of_work import UserUnitOfWork, get_user_uow
from src.app.schemas.user_profile_schema import UserSchema, EditProfileSchema

router = APIRouter(tags=["User Profile Routes"])

@router.patch("/profile/edit/{user_id}", response_model=UserSchema)
def edit_profile(
    user_id: UUID,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    unit_of_work: UserUnitOfWork = Depends(get_user_uow)
):
    """
    Edit the profile details of a user, including profile picture.

    Args:
        user_id (UUID): The unique identifier of the user.
        name (Optional[str]): New name.
        email (Optional[str]): New email.
        phone (Optional[str]): New phone number.
        profile_picture (Optional[UploadFile]): New profile picture.
        unit_of_work (UserUnitOfWork): Injected UoW instance.

    Returns:
        UserSchema: Updated profile details.
    """

    name = name.strip() if name else None
    email = email.strip() if email else None
    phone = phone.strip() if phone else None

    try:
        validated_data = EditProfileSchema(name=name, email=email, phone=phone)
    except ValidationError as e:
        error_messages = [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]
        raise HTTPException(status_code=400, detail=error_messages)

    edit_profile_service = EditProfileService(unit_of_work)

    try:
        updated_user = edit_profile_service.update_user_profile(
            user_id, validated_data.name, validated_data.email, validated_data.phone, profile_picture
        )
        return updated_user
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
