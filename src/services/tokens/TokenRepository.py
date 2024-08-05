import json
import os
import threading
from datetime import datetime
from datetime import timedelta
from typing import Optional

import jwt
from jsonschema import validate
from typing_extensions import Self

from src.database.models.User import User
from .TokenRepositoryInterface import TokenRepositoryInterface
from .common.tokenTypes import ExpirationType, Tokens, TokenHeaders, TokenPayload

dir_path = os.path.dirname(os.path.abspath(__file__))


class TokenRepository(TokenRepositoryInterface):
    __INSTANCE: Self = None
    __lock = threading.Lock()
    __CONFIG_SCHEMA: dict = {
        "type": "object",
        "properties": {
            "SECRET": {
                "type": "string"
            },
            "REFRESH_TOKEN_DAYS_VALIDITY": {
                "type": "integer"
            },
            "TOKEN_MINUTES_VALIDITY": {
                "type": "integer"
            },
            "ALGORITHM": {
                "type": "string"
            }
        },
        "required": [
            "SECRET",
            "REFRESH_TOKEN_DAYS_VALIDITY",
            "TOKEN_MINUTES_VALIDITY",
            "ALGORITHM",
            "PASSWORD_SALT_ROUNDS"
        ]
    }
    __SECRET: str
    __REFRESH_TOKEN_DAYS_VALIDITY: int
    __TOKEN_MINUTES_VALIDITY: int
    __ALGORITHM: str

    def __new__(cls):
        if not cls.__INSTANCE:
            with cls.__lock:
                if not cls.__INSTANCE:
                    cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(self):
        super().__init__()
        self.__load_configs()

    def __load_configs(self):
        with open(os.path.join(dir_path, '..', '..', '..', 'configs', 'jwt.json'), "r") as configs:
            target = json.load(configs)
            validate(target, self.__CONFIG_SCHEMA)

        self.__SECRET = target["SECRET"]
        self.__REFRESH_TOKEN_DAYS_VALIDITY = target["REFRESH_TOKEN_DAYS_VALIDITY"]
        self.__TOKEN_MINUTES_VALIDITY = target['TOKEN_MINUTES_VALIDITY']
        self.__ALGORITHM = target['ALGORITHM']

    def generate_tokens(self, payload: TokenPayload) -> Tokens:
        return Tokens(
            access_token=self._generate_token(payload, ExpirationType.Access),
            refresh_token=self._generate_token(payload, ExpirationType.Refresh)
        )

    def _generate_token(self, payload: TokenPayload, exp_type: ExpirationType) -> str:
        exp: str = {
            0: datetime.utcnow() + timedelta(minutes=self.__TOKEN_MINUTES_VALIDITY),
            1: datetime.utcnow() + timedelta(days=self.__REFRESH_TOKEN_DAYS_VALIDITY)
        }[exp_type.value].isoformat()

        headers = TokenHeaders(exp=exp)

        return jwt.encode(
            payload=payload.dict(),
            key=self.__SECRET,
            headers=headers.dict(),
            algorithm=self.__ALGORITHM
        )

    async def get_new_token(self, refresh_token: str, user_db: User) -> str:
        try:
            if refresh_token not in user_db.tokens.refresh_token:
                raise Exception('Refresh token not exists')

            user_sing = jwt.decode(
                refresh_token,
                self.__SECRET,
                algorithms=[self.__ALGORITHM])

            return self._generate_token(
                payload=TokenPayload(id=user_sing.id, username=user_db.username),
                exp_type=ExpirationType.Access
            )

        except jwt.ExpiredSignatureError as err:
            print(err)
            raise Exception("Refresh token forbidden")

    def auth_token(self, token: str) -> bool:
        if not self.get_user_sign(token):
            return False

        return True

    def get_user_sign(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token,
                self.__SECRET,
                algorithms=[self.__ALGORITHM]
            )

        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_instance():
        if not TokenRepository.__INSTANCE:
            TokenRepository()

        return TokenRepository.__INSTANCE
