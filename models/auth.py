from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenRequest(BaseModel):
    token: str

class MicrosoftAuthResponse(BaseModel):
    user_id: str
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

class GoogleAuthResponse(BaseModel):
    user_id: str
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

class LinkedInAuthResponse(BaseModel):
    user_id: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None

class AuthErrorResponse(BaseModel):
    detail: str