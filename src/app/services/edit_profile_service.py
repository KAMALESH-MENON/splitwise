from uuid import UUID
from fastapi import UploadFile
from typing import Optional
from src.app.services.unit_of_work import UserUnitOfWork
from src.app.schemas.user_profile_schema import UserSchema
from src.app.config.config_uploadcare import uploadcare

class EditProfileService:
    """
    Service class responsible for editing user profile.
    """

    def __init__(self, unit_of_work: UserUnitOfWork):
        self.unit_of_work = unit_of_work

    def upload_to_uploadcare(self, profile_picture: UploadFile) -> str:
        """
        Securely uploads an image to Uploadcare and returns the file URL.
        """
        try:
            uploaded_file = uploadcare.upload(profile_picture.file)
            return uploaded_file.cdn_url  
        except Exception as e:
            raise ValueError(f"Upload failed: {str(e)}")

    def update_user_profile(
        self,
        user_id: UUID,
        name: Optional[str],
        email: Optional[str],
        phone: Optional[str],
        profile_picture: Optional[UploadFile] = None
    ) -> UserSchema:
        """
        Updates user profile details.

        Args:
            user_id (UUID): User ID.
            name (Optional[str]): New name.
            email (Optional[str]): New email.
            phone (Optional[str]): New phone number.
            profile_picture (Optional[UploadFile]): New profile picture.

        Returns:
            UserSchema: Updated user details.
        """
        with self.unit_of_work as uow:
            user = uow.user_repository.get(id=user_id)
            if not user:
                raise ValueError("User not found")

            changes_made = False

            if name and name != user.name:
                user.name = name
                changes_made = True
            if email and email != user.email:
                user.email = email if email.strip() else None
                changes_made = True
            if phone and phone != user.phone:
                user.phone = phone
                changes_made = True

            if profile_picture:
                user.profile_picture_url = self.upload_to_uploadcare(profile_picture)
                changes_made = True

            if not changes_made:
                return UserSchema.model_validate(user)

            return UserSchema.model_validate(user)
