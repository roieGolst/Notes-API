from typing import Optional

from fastapi import Depends
from fastapi import Header, HTTPException, status
from typing_extensions import Annotated

from ..common.types import TokenDep


def authenticate_middleware(
        token: Annotated[str, Header()],
        token_repo: TokenDep
):
    if not token_repo.auth_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def auth_and_get_user_sign(
        token: Annotated[str, Header()],
        token_repo: TokenDep
) -> Optional[dict]:
    if not token_repo.auth_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return token_repo.get_user_sign(token)


AuthAndGetSingDep = Annotated[Optional[dict], Depends(auth_and_get_user_sign)]
AuthDep = Depends(authenticate_middleware)