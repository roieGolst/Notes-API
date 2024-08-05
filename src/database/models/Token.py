from typing import List
from pydantic import BaseModel


class UserTokens(BaseModel):
    refresh_token: List[str] = []
    active_token: List[str] = []
