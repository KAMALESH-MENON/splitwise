from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
import phonenumbers
import re

class UserSchema(BaseModel):
    """Schema for representing user data."""
    id: UUID
    name: str
    email: Optional[EmailStr] = None  
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class EditProfileSchema(BaseModel):
    """Schema for updating user profile details."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None

    @field_validator("phone", mode="before")
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v  
        
        v = re.sub(r"[ \-()]", "", v)  

        if not v.isdigit() and not v.startswith("+"):
            raise ValueError("Phone number can only contain digits and an optional leading '+'.")

        try:
           
            if v.startswith("+"):
                parsed_phone = phonenumbers.parse(v, None)
            else:
                if not (7 <= len(v) <= 14):
                    raise ValueError("Phone number must be between 7 and 14 digits long.")
                return v 

            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number format.")

            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format.")

