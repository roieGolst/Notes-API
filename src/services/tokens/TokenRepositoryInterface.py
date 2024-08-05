from abc import ABC, abstractmethod
from pydantic import BaseModel

from src.database.models.User import User
from src.services.tokens.common.tokenTypes import ExpirationType, TokenPayload, Tokens


class TokenRepositoryInterface(ABC):
    @abstractmethod
    def generate_tokens(self, payload: TokenPayload) -> Tokens:
        pass

    @abstractmethod
    def _generate_token(self, payload: TokenPayload, exp_type: ExpirationType) -> str:
        pass

    @abstractmethod
    async def get_new_token(self, refresh_token: str, user_db: User) -> str:
        pass

    @abstractmethod
    def auth_token(self, token: str) -> bool:
        pass
