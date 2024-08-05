from fastapi import Depends
from fastapi import Header, HTTPException, status
from typing_extensions import Annotated

from src.services.tokens.TokenRepository import TokenRepository


def authenticate_middleware(
        token: Annotated[str, Header()],
        token_repo: TokenRepository = Depends(TokenRepository)
):
    if not token_repo.auth_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def auth_and_get_user_sign(token: Annotated[str, Header()],token_repo: TokenRepository = Depends(TokenRepository)):
    return token_repo.get_user_sign(token)
