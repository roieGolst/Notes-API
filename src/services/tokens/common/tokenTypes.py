from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel


class ExpirationType(IntEnum):
    Access = 0
    Refresh = 1


class TokenHeaders(BaseModel):
    alg: str = 'HS256'
    typ: str = 'JWT'
    exp: str


class TokenPayload(BaseModel):
    id: str
    username: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
