from fastapi import APIRouter, Depends, Response

from constants import USER_ACCESS_TOKEN_KEY
from schemas import MessageSchema
from users.auth import create_access_token
from users.repository import UserRepository, get_user_repository
from users.schemas import (
    JwtTokenSchema,
    StatusCode401,
    StatusCode409,
    StatusCode422,
    UserAuthSchema,
    UserRegisterSchema,
    UserSchemaDB,
)
from users.utils import get_current_user
from users.validatiors import (
    check_email_duplicate,
    check_number_duplicate,
    validate_email,
    validate_password,
)

router = APIRouter()


@router.post(
    "/register/",
    summary="Регистрация пользователя.",
    description="Регистрирует вас как нового пользователя.",
    status_code=201,
    responses={
        201: {"model": UserSchemaDB},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def register_user(
    user_register: UserRegisterSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchemaDB:
    await check_email_duplicate(
        email=user_register.email, repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_register.phone_number, repository=user_repository
    )
    return await user_repository.create(user_register)


@router.post(
    "/login/",
    summary="Авторизация пользователя.",
    description="Авторизует вас и возвращает токен.",
    status_code=201,
    responses={
        201: {"model": JwtTokenSchema},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def auth_user(
    response: Response,
    user_auth: UserAuthSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> JwtTokenSchema:
    user = await validate_email(
        email=user_auth.email, repository=user_repository
    )
    validate_password(user=user, password=user_auth.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key=USER_ACCESS_TOKEN_KEY, value=access_token, httponly=True
    )
    return JwtTokenSchema(access_token=access_token, refresh_token=None)


@router.post(
    "/logout/",
    summary="Выйти из системы.",
    description="Выводит пользователя из ситемы.",
    status_code=200,
    responses={
        200: {"model": MessageSchema},
        401: {"model": StatusCode401},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def logout_user(
    response: Response, user: UserRepository = Depends(get_current_user)
) -> MessageSchema:
    response.delete_cookie(key=USER_ACCESS_TOKEN_KEY)
    return MessageSchema(message="Пользователь успешно вышел из системы.")
