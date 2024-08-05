from beanie import Document, PydanticObjectId
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


class User(Document):
    _id: PydanticObjectId
    username: str
    email: EmailStr
    hashed_password: str
    tokens: UserTokens = UserTokens()
    last_sentiment: Optional[str] = None
    note_ids: List[PydanticObjectId] = []
    sentiments: List[str] = []

    class Settings:
        name = "users"
