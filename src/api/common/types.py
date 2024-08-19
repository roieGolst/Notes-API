from typing import Annotated

from fastapi import Depends

from src.services.password.PasswordService import PasswordService
from src.services.tokens.TokenRepository import TokenRepository
from src.services.tokens.TokenRepositoryInterface import TokenRepositoryInterface

TokenDep = Annotated[TokenRepositoryInterface,  Depends(TokenRepository)]
PasswordDep = Annotated[PasswordService, Depends()]