from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from urllib.parse import urlparse


class URLCreate(BaseModel):
    original_url: str
    creator_email: EmailStr
    authorized_emails: list[EmailStr]


class AccessRequest(BaseModel):
    user_email: EmailStr
