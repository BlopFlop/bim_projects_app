from fastapi import APIRouter, Depends, Response

from users.repository import UserRepository, get_user_repository
from users.schemas import (
    UserRegisterSchema,
    UserAuthSchema,
    UserChangePassword,
    UserSchemaDB,
    UserUpdateSchema,
    JwtTokenSchema
)
from users.auth import (
    get_token,
    create_access_token,
    get_current_user,
    get_current_admin_user
)
from users.validatiors import (
    check_email_duplicate,
    check_number_duplicate,
    validate_email,
    validate_password,
    validate_user_id
)
from constants import (
    USER_ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_KEY,
    REFRESH_TOKEN_KEY,
)
from schemas import MessageSchema

router = APIRouter()


@router.post(
    "/register/",
    response_model=UserSchemaDB,
    summary="Регистрация пользователя.",
    description="Регистрирует вас как нового пользователя.",
    status_code=201,
)
async def register_user(
    user_register: UserRegisterSchema,
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
    return await user_repository.create(user_register)


@router.post(
    "/login/",
    response_model=JwtTokenSchema,
    summary="Авторизация пользователя.",
    description="Авторизует вас и возвращает токен.",
    status_code=201,
)
async def auth_user(
    response: Response,
    user_auth: UserAuthSchema,
    user_repository: UserRepository = Depends(get_user_repository)
) -> dict:
    user = await validate_email(
        email=user_auth.email,
        repository=user_repository
    )
    validate_password(user=user, password=user_auth.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key=USER_ACCESS_TOKEN_KEY,
        value=access_token,
        httponly=True
    )
    return JwtTokenSchema(
        access_token=access_token,
        refresh_token=None
    )


@router.get(
    "/me/",
    response_model=UserSchemaDB,
    summary="Получить пользователя.",
    description="Получает текущего пользователя выполнившего запрос."
)
async def get_me(
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    return await get_current_user(token, user_repository)


@router.patch(
    "/me/",
    response_model=UserSchemaDB,
    summary="Изменить пользователя.",
    description="Изменяет текущего пользователя выполнившего запрос.",
    status_code=201,
)
async def change_me(
    user_update: UserUpdateSchema,
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    user = await get_current_user(token, user_repository)
    await check_email_duplicate(
        email=user_update.email,
        repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_update.phone_number,
        repository=user_repository
    )
    return await user_repository.update(user, user_update)


@router.delete(
    "/me/",
    summary="Удалить пользователя.",
    description="Удаляет текущего пользователя выполнившего запрос.",
    status_code=204
)
async def change_me(
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    user = await get_current_user(token, user_repository)
    await user_repository.remove(user)
    return MessageSchema(message="Вы были удалены.")


@router.patch(
    "/me/change_password/",
    response_model=MessageSchema,
    summary="Изменить пароль пользователя.",
    description="Изменяет пароль текущего пользователя выполнившего запрос.",
    status_code=201,
)
async def change_password(
    change_pass_data: UserChangePassword,
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
) -> dict:
    user = await get_current_user(token, user_repository)
    validate_password(
        user=user,
        password=change_pass_data.old_password
    )
    await user_repository.change_password(
        db_obj=user,
        password=change_pass_data.new_password
    )
    return MessageSchema(message="Пароль успешно изменен.")


@router.post(
    "/logout/",
    response_model=MessageSchema,
    summary="Выйти из системы.",
    description="Выводит пользователя из ситемы."
)
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key=USER_ACCESS_TOKEN_KEY)
    return MessageSchema(message="Пользователь успешно вышел из системы.")


@router.get(
    "/users/",
    response_model=list[UserSchemaDB],
    summary="Получить всех пользователей.",
    description=(
        "Получает всех пользователей если у вас есть права администратора."
    )
)
async def get_all_users(
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    await get_current_admin_user(token, user_repository)
    return await user_repository.get_multi()


@router.get(
    "/users/{user_id}/",
    response_model=UserSchemaDB,
    summary="Получить пользователя по id",
    description=(
        "Получает пользователя по id если у вас есть права администратора."
    )
)
async def get_user(
    user_id: int,
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    await get_current_admin_user(token, user_repository)
    return await validate_user_id(user_id, user_repository=user_repository)


@router.patch(
    "/users/{user_id}/",
    response_model=UserSchemaDB,
    summary="Изменить пользователя по id",
    description=(
        "Изменяет пользователя по id если у вас есть права администратора."
    ),
    status_code=201
)
async def change_user(
    user_id: int,
    user_update: UserUpdateSchema,
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    await get_current_admin_user(token, user_repository)
    user = await validate_user_id(
        id=user_id,
        user_repository=user_repository
    )
    await check_email_duplicate(
        email=user_update.email,
        repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_update.phone_number,
        repository=user_repository
    )
    return await user_repository.update(user, user_update)


@router.delete(
    "/users/{user_id}/",
    summary="Удалить пользователя по id",
    description=(
        "Удаляет пользователя по id если у вас есть права администратора."
    ),
    status_code=204
)
async def delete_user(
    user_id: int,
    token: str = Depends(get_token),
    user_repository: UserRepository = Depends(get_user_repository)
):
    await get_current_admin_user(token, user_repository)
    user = await validate_user_id(
        id=user_id,
        user_repository=user_repository
    )
    await user_repository.remove(user)
    return MessageSchema(message="Пользователь удален.")
