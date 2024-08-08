from typing import Annotated

from fastapi import APIRouter, Response, HTTPException, status, Depends
from beanie.operators import Or
from src.database.models.User import User, UserRegistrationResponse, UserRegistrationRequest, UserAuthRequest
from src.services.tokens.TokenRepository import TokenRepository
from src.services.tokens.common.tokenTypes import TokenPayload
from src.services.password.PasswordService import PasswordService

from ..middlewares.authenticate import authenticate_middleware, auth_and_get_user_sign

router = APIRouter(prefix="/auth")


@router.post(
    path="/register",
    response_model=UserRegistrationResponse
)
async def register(user: UserRegistrationRequest, password_service: Annotated[PasswordService, Depends()]):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=password_service.hash_password(user.password)
    )

    await new_user.insert()

    return UserRegistrationResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email
    )


@router.post(
    path="/login"
)
async def login(
        auth: UserAuthRequest,
        password_service: Annotated[PasswordService, Depends()],
        token_repo: TokenRepository = Depends(TokenRepository.get_instance)
):
    query = Or(User.email == auth.username, User.username == auth.username)
    user = await User.find_one(query)

    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="User not exits")

    user = user.model_dump()

    if not password_service.check_password(auth.password, user['hashed_password']):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content='Password wrong')

    tokens = token_repo.generate_tokens(TokenPayload(id=user['id'], username=user["username"]))

    response_headers = {'token': tokens.access_token}
    response = Response(headers=response_headers)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token)

    return response


@router.get(
    path="/profile/",
    dependencies=[Depends(authenticate_middleware)]
)
async def profile(token: Annotated[str, Depends(auth_and_get_user_sign)]):
    print(token)