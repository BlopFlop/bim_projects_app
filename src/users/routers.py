from fastapi import APIRouter, Depends, Response

from users.repository import UserRepository, get_user_repository
from users.schemas import UserRegister, UserAuth
from users.auth import get_password_hash, create_access_token
from users.validatiors import (
    check_email_duplicate,
    check_number_duplicate,
    validate_email_and_password
)
from constants import (
    USER_ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_KEY,
    REFRESH_TOKEN_KEY,
    SECRET_KEY,
    ALGORITHM_KEY
)

router = APIRouter()


@router.post(
    "/register/",
    summary="Регистрация пользователя.",
    description="Регистрирует вас как нового пользователя."
)
async def register_user(
    user_register: UserRegister,
    user_repository: UserRepository = Depends(get_user_repository)
) -> dict:
    await check_email_duplicate(
        email=user_register.email,
        repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_register.phone_number,
        repository=user_repository
    )
    user_register.password = get_password_hash(user_register.password)
    await user_repository.create(user_register)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post(
    "/login/",
    summary="Авторизация пользователя.",
    description="Авторизует вас и возвращает токен."
)
async def auth_user(
    response: Response,
    user_auth: UserAuth,
    user_repository: UserRepository = Depends(get_user_repository)
) -> dict:
    user = await validate_email_and_password(
        email=user_auth.email,
        password=user_auth.password,
        repository=user_repository
    )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key=USER_ACCESS_TOKEN_KEY,
        value=access_token,
        httponly=True
    )
    return {ACCESS_TOKEN_KEY: access_token, REFRESH_TOKEN_KEY: None}
