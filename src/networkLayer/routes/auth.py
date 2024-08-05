from typing import Annotated

from fastapi import APIRouter, Response, status, Header, Depends
from beanie.operators import Or
from src.database.models.User import User, UserRegistrationResponse, UserRegistrationRequest, UserAuthRequest
from src.services.tokens.TokenRepository import TokenRepository
from src.services.tokens.common.tokenTypes import TokenPayload
from ..middlewares.authenticate import authenticate_middleware, auth_and_get_user_sign

router = APIRouter(prefix="/auth")


@router.post(
    path="/register",
    response_model=UserRegistrationResponse
)
async def register(user: UserRegistrationRequest):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )

    await new_user.insert()

    return UserRegistrationResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email
    )


@router.post(
    path="/login",
    response_model=UserRegistrationResponse,
)
async def login(
        auth: UserAuthRequest,
        token_repo: TokenRepository = Depends(TokenRepository.get_instance)
):
    query = Or(User.email == auth.username, User.username == auth.username)
    user = await User.find_one(query)
    user = user.model_dump()

    if not user:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    tokens = token_repo.generate_tokens(TokenPayload(id=user['id'], username=user["username"]))

    response_headers = {'token': tokens.access_token}
    response = Response(headers=response_headers)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token)

    response.body = UserRegistrationResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"]
    )

    return response


@router.get(
    path="/profile/"
)
async def profile(token: Annotated[str, Depends(auth_and_get_user_sign)]):
    print(token)