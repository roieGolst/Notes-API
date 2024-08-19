from fastapi import APIRouter, Response, status
from beanie.operators import Or

from src.core.database.models.User import User, UserRegistrationResponse, UserRegistrationRequest, UserAuthRequest, UserProfile
from src.services.tokens.common.tokenTypes import TokenPayload

from ..common.types import PasswordDep
from ..common.types import TokenDep
from ..middlewares.authenticate import AuthAndGetSingDep

router = APIRouter(prefix="/auth")


@router.post(
    path="/register",
    response_model=UserRegistrationResponse
)
async def register(user: UserRegistrationRequest, password_service: PasswordDep):
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
        password_service: PasswordDep,
        token_repo: TokenDep
):
    query = Or(User.email == auth.username, User.username == auth.username)
    user = await User.find_one(query)

    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="User not exits")

    user = user.model_dump()

    if not password_service.check_password(auth.password, user['hashed_password']):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content='Password wrong')

    # TODO: Add the tokens within dedicated user document
    # TODO: Added MongoDB exp indexed that removes expired refresh tokens
    tokens = token_repo.generate_tokens(TokenPayload(id=user['id'], username=user["username"]))

    response_headers = {'token': tokens.access_token}
    response = Response(headers=response_headers)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token)

    return response


@router.get(
    path="/profile/",
    response_model=UserProfile
)
async def profile(token: AuthAndGetSingDep):
    user = await User.get(token['id'])

    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="User not exits")

    return UserProfile(
        id=user.id,
        username=user.username,
        email=user.email
    )
