from beanie import Document, PydanticObjectId
from beanie import Indexed
from pydantic import EmailStr, BaseModel
from typing import List, Optional

from .Token import UserTokens


class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRegistrationResponse(BaseModel):
    id: PydanticObjectId
    username: str
    email: str


class UserAuthRequest(BaseModel):
    username: str
    password: str


class UserAuthResponse(BaseModel):
    token: str


class UserProfile(BaseModel):
    id: PydanticObjectId
    username: str
    email: EmailStr


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    tokens: UserTokens = UserTokens()
    last_sentiment: Optional[str] = None
    note_ids: List[PydanticObjectId] = []
    sentiments: List[str] = []

    class Settings:
        name = "users"
